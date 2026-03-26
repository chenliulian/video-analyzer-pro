#!/usr/bin/env python3
"""
阿里云 Qwen ASR 语音转文字模块
使用 qwen3-asr-flash 模型进行音频识别
支持大文件自动切分处理
"""

import os
import sys
import tempfile
from typing import List, Tuple, Optional

try:
    import dashscope
except ImportError:
    print("错误: 未安装 dashscope SDK")
    print("安装方法: pip3 install dashscope")
    sys.exit(1)

import subprocess
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("警告: 未安装 python-dotenv, 将从环境变量读取配置")


class QwenASR:
    """阿里云 Qwen ASR 语音识别类"""
    
    # 文件大小限制 (字节)
    MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB (保守值,API限制约10MB)
    CHUNK_DURATION_MS = 120000  # 每段2分钟
    
    def __init__(self, api_key: Optional[str] = None, region: str = "intl"):
        """
        初始化 Qwen ASR
        
        参数:
            api_key: 阿里云 API Key (可选,从环境变量 DASHSCOPE_API_KEY 读取)
            region: 地域 ("intl" 新加坡国际版, "cn" 北京版)
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        
        if not self.api_key:
            print("警告: 未设置 DASHSCOPE_API_KEY")
            print("请在 .env 文件中添加: DASHSCOPE_API_KEY=your-api-key")
            print("或设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
            print("\n获取 API Key: https://help.aliyun.com/zh/model-studio/get-api-key")
            raise ValueError("DASHSCOPE_API_KEY 未配置")
        
        # 设置 API 地址
        if region == "intl":
            dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
            print("✓ 使用国际版 API (新加坡)")
        else:
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            print("✓ 使用国内版 API (北京)")
        
        self.model = "qwen3-asr-flash"
        self.region = region
        print(f"✓ Qwen ASR 初始化成功")
        print(f"  模型: {self.model}")
        print(f"  文件大小限制: {self.MAX_FILE_SIZE / 1024 / 1024:.1f} MB")
    
    def transcribe_audio(self, 
                         audio_file_path: str, 
                         language: Optional[str] = None,
                         enable_itn: bool = False,
                         system_prompt: str = "",
                         auto_split: bool = True) -> Optional[str]:
        """
        转录单个音频文件 (支持大文件自动切分)
        
        参数:
            audio_file_path: 音频文件的绝对路径
            language: 语言代码 (如 "zh", "en", 可选)
            enable_itn: 是否启用反向文本规范化 (数字、日期等格式化)
            system_prompt: 系统提示词 (可用于定制化识别)
            auto_split: 是否自动切分大文件
            
        返回:
            转录文本,失败返回 None
        """
        # 检查文件是否存在
        if not os.path.exists(audio_file_path):
            print(f"错误: 音频文件不存在: {audio_file_path}")
            return None
        
        # 检查文件大小
        file_size = os.path.getsize(audio_file_path)
        print(f"  音频文件大小: {file_size / 1024 / 1024:.2f} MB")
        
        # 如果文件过大且支持切分,则使用切分方式
        if auto_split and file_size > self.MAX_FILE_SIZE:
            print(f"  文件过大,将自动切分为多段处理...")
            return self._transcribe_large_file(audio_file_path, language, enable_itn, system_prompt)
        else:
            return self._transcribe_single_file(audio_file_path, language, enable_itn, system_prompt)
    
    def _transcribe_single_file(self,
                                audio_file_path: str,
                                language: Optional[str] = None,
                                enable_itn: bool = False,
                                system_prompt: str = "") -> Optional[str]:
        """转录单个文件 (内部方法)"""
        # 构建 file:// URL
        if not audio_file_path.startswith("file://"):
            audio_file_url = f"file://{os.path.abspath(audio_file_path)}"
        else:
            audio_file_url = audio_file_path
        
        # 构建消息
        messages = [
            {"role": "system", "content": [{"text": system_prompt}]},
            {"role": "user", "content": [{"audio": audio_file_url}]}
        ]
        
        # 构建 ASR 选项
        asr_options = {
            "enable_itn": enable_itn
        }
        if language:
            asr_options["language"] = language
        
        try:
            print(f"  正在识别: {os.path.basename(audio_file_path)}...")
            
            response = dashscope.MultiModalConversation.call(
                api_key=self.api_key,
                model=self.model,
                messages=messages,
                result_format="message",
                asr_options=asr_options
            )
            
            # 检查响应状态
            if response.status_code != 200:
                print(f"  错误: API 返回状态码 {response.status_code}")
                print(f"  详情: {response}")
                return None
            
            # 提取转录文本
            if hasattr(response, 'output') and response.output:
                choices = response.output.get('choices', [])
                if choices and len(choices) > 0:
                    message = choices[0].get('message', {})
                    content = message.get('content', [])
                    
                    # 提取文本内容
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and 'text' in item:
                            text_parts.append(item['text'])
                    
                    if text_parts:
                        result = ' '.join(text_parts).strip()
                        print(f"  ✓ 识别成功: {len(result)} 字符")
                        return result
            
            print(f"  警告: 无法解析响应内容")
            print(f"  响应: {response}")
            return None
            
        except Exception as e:
            print(f"  错误: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_audio_duration(self, audio_file_path: str) -> float:
        """使用ffprobe获取音频时长"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'json',
                audio_file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            return duration
        except Exception as e:
            print(f"    警告: 无法获取音频时长: {e}")
            return 0.0
    
    def _transcribe_large_file(self,
                               audio_file_path: str,
                               language: Optional[str] = None,
                               enable_itn: bool = False,
                               system_prompt: str = "") -> Optional[str]:
        """处理大文件:使用ffmpeg切分为多段,分别转录后合并"""
        try:
            # 获取音频时长
            print(f"  正在获取音频信息...")
            duration_sec = self._get_audio_duration(audio_file_path)
            
            if duration_sec <= 0:
                print(f"  错误: 无法获取音频时长")
                return None
            
            print(f"  音频时长: {duration_sec:.1f} 秒 ({duration_sec / 60:.1f} 分钟)")
            
            # 计算需要切分的段数 (每段2分钟)
            chunk_duration = 120  # 秒
            num_chunks = int((duration_sec + chunk_duration - 1) / chunk_duration)
            print(f"  将切分为 {num_chunks} 段 (每段约 {chunk_duration / 60:.1f} 分钟)")
            
            # 创建临时目录
            temp_dir = tempfile.mkdtemp(prefix="qwen_asr_")
            all_texts = []
            
            try:
                for i in range(num_chunks):
                    start_sec = i * chunk_duration
                    end_sec = min(start_sec + chunk_duration, duration_sec)
                    segment_duration = end_sec - start_sec
                    
                    print(f"\n  处理第 {i + 1}/{num_chunks} 段 ({start_sec:.1f}s - {end_sec:.1f}s)...")
                    
                    # 使用ffmpeg切分音频
                    temp_file = os.path.join(temp_dir, f"chunk_{i:04d}.mp3")
                    
                    cmd = [
                        'ffmpeg',
                        '-i', audio_file_path,
                        '-ss', str(start_sec),
                        '-t', str(segment_duration),
                        '-ac', '1',  # 转为单声道
                        '-ar', '16000',  # 16kHz采样率
                        '-b:a', '64k',  # 64kbps比特率
                        '-y',  # 覆盖输出文件
                        temp_file
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode != 0:
                        print(f"    ⚠️  ffmpeg切分失败: {result.stderr[:200]}")
                        continue
                    
                    chunk_size = os.path.getsize(temp_file)
                    print(f"    切片大小: {chunk_size / 1024 / 1024:.2f} MB")
                    
                    # 转录
                    text = self._transcribe_single_file(temp_file, language, enable_itn, system_prompt)
                    
                    if text:
                        all_texts.append(text)
                        print(f"    ✓ 第 {i + 1} 段识别成功: {len(text)} 字符")
                    else:
                        print(f"    ⚠️  第 {i + 1} 段识别失败")
                    
                    # 删除临时文件
                    os.remove(temp_file)
                
                # 合并所有文本
                if all_texts:
                    combined_text = ' '.join(all_texts)
                    print(f"\n  ✓ 全部识别完成!")
                    print(f"    总字符数: {len(combined_text)}")
                    print(f"    成功段数: {len(all_texts)}/{num_chunks}")
                    return combined_text
                else:
                    print(f"\n  ⚠️  所有段落识别均失败")
                    return None
                    
            finally:
                # 清理临时目录
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
                
        except Exception as e:
            print(f"  错误: 处理大文件失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def transcribe_audio_with_timestamps(self, 
                                          audio_file_path: str,
                                          language: Optional[str] = None,
                                          enable_itn: bool = False) -> List[Tuple[float, float, str]]:
        """
        转录音频并尝试生成时间戳 (简化版)
        
        注意: Qwen ASR 默认不返回词级时间戳,此方法返回整段文本
        
        参数:
            audio_file_path: 音频文件路径
            language: 语言代码
            enable_itn: 是否启用反向文本规范化
            
        返回:
            [(start_time, end_time, text), ...] 格式的列表
        """
        text = self.transcribe_audio(audio_file_path, language, enable_itn)
        
        if text:
            # 返回整段文本,时间戳为 0 到音频时长
            # 注意: 这是简化处理,实际时长需要从音频文件读取
            return [(0.0, 0.0, text)]
        else:
            return []


def transcribe_audio_file(audio_file_path: str, 
                          api_key: Optional[str] = None,
                          language: Optional[str] = "zh",
                          enable_itn: bool = False) -> Optional[str]:
    """
    便捷函数: 转录单个音频文件
    
    参数:
        audio_file_path: 音频文件路径
        api_key: API Key (可选)
        language: 语言代码 (默认 "zh")
        enable_itn: 是否启用反向文本规范化
        
    返回:
        转录文本
    """
    try:
        asr = QwenASR(api_key=api_key)
        return asr.transcribe_audio(audio_file_path, language=language, enable_itn=enable_itn)
    except Exception as e:
        print(f"转录失败: {e}")
        return None


# 测试代码
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Qwen ASR 语音转文字测试")
    parser.add_argument("--audio", type=str, required=True, help="音频文件路径")
    parser.add_argument("--language", type=str, default="zh", help="语言代码 (zh/en)")
    parser.add_argument("--enable-itn", action="store_true", help="启用反向文本规范化")
    parser.add_argument("--region", type=str, default="intl", choices=["intl", "cn"], 
                       help="地域 (intl=新加坡, cn=北京)")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Qwen ASR 测试")
    print("=" * 70)
    
    try:
        # 初始化
        asr = QwenASR(region=args.region)
        
        # 转录
        print(f"\n音频文件: {args.audio}")
        result = asr.transcribe_audio(
            args.audio, 
            language=args.language,
            enable_itn=args.enable_itn
        )
        
        if result:
            print("\n" + "=" * 70)
            print("转录结果:")
            print("=" * 70)
            print(result)
            print("\n" + "=" * 70)
            print(f"总字符数: {len(result)}")
        else:
            print("\n转录失败")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
