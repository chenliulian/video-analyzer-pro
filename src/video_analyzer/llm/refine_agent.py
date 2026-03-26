#!/usr/bin/env python3
"""
大模型Agent模块 - 整合OCR和语音文字，纠错并整理段落
增强功能: 繁简转换、智能纠错、标点添加、段落分层
"""
import os
import sys
import json
import re
from typing import List, Tuple, Dict

try:
    from dotenv import load_dotenv
except ImportError:
    print("警告: 未安装python-dotenv，无法从.env文件加载配置")
    print("安装: pip3 install python-dotenv")
    load_dotenv = None

try:
    # 使用OpenAI API（兼容各种大模型服务）
    from openai import OpenAI
except ImportError:
    print("请安装OpenAI SDK: pip3 install openai")
    sys.exit(1)

# 加载.env文件
if load_dotenv:
    load_dotenv()


class TextRefineAgent:
    """文字精炼Agent - 结合OCR和语音转录，纠错并整理"""
    
    def __init__(self, api_key=None, base_url=None, model=None, use_batch_mode=True):
        """
        初始化Agent
        
        参数:
            api_key: API密钥（如果不提供，从.env文件或环境变量读取）
            base_url: API地址（可选，用于使用第三方服务，从.env读取LLM_BASE_URL）
            model: 模型名称（从.env读取LLM_MODEL）
        """
        # 从环境变量或参数获取配置（优先级：参数 > 环境变量）
        self.api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
        self.model = model or os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL")
        self.use_batch_mode = use_batch_mode  # 新增: 是否使用批处理模式 
        
        if not self.api_key:
            print("警告: 未设置API密钥")
            print("请在项目根目录创建 .env 文件并配置:")
            print("  LLM_API_KEY=your-api-key")
            print("  LLM_BASE_URL=https://api.openai.com/v1  # 可选")
            print("  LLM_MODEL=gpt-4  # 可选")
            print("或使用环境变量: export LLM_API_KEY='your-api-key'")
            self.client = None
        else:
            # 初始化客户端
            if self.base_url:
                self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            else:
                self.client = OpenAI(api_key=self.api_key)
            
            print(f"✓ LLM Agent初始化成功")
            print(f"  模型: {self.model}")
            print(f"  模式: {'批处理模式(整体精炼)' if use_batch_mode else '逐帧模式'}")
            if self.base_url:
                print(f"  API地址: {self.base_url}")
    
    def refine_transcript_with_ocr(self, 
                                  transcript_segments: List[Tuple[float, float, str]],
                                  ocr_text: str,
                                  frame_time: float,
                                  global_context: str = "") -> str:
        """
        结合OCR文字纠错和整理语音转录
        
        参数:
            transcript_segments: 语音转录段落 [(start, end, text), ...]
            ocr_text: 对应图片的OCR识别文字
            frame_time: 图片对应的时间点
            
        返回:
            refined_text: 精炼后的文字
        """
        if not self.client:
            # 如果没有配置API，直接返回原文
            return self._format_segments_simple(transcript_segments)
        
        # 合并转录文字
        transcript_text = " ".join([text for _, _, text in transcript_segments])
        
        # 构建提示词 - 传入全局上下文
        prompt = self._build_refine_prompt(transcript_text, ocr_text, frame_time, global_context)
        
        try:
            # 调用大模型
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是文字编辑助手,擅长整理课堂讲座文字。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800  # 优化: 减少token限制,加快响应
            )
            
            refined_text = response.choices[0].message.content.strip()
            return refined_text
            
        except Exception as e:
            print(f"LLM调用出错: {e}")
            return self._format_segments_simple(transcript_segments)
    
    def _build_refine_prompt(self, transcript_text: str, ocr_text: str, frame_time: float, global_context: str = "") -> str:
        """构建提示词 - 优化版(更简洁)"""
        
        # 简化的提示词 - 减少不必要的说明
        prompt = f"""整理课堂讲座文字,添加标点符号。

OCR课件文字: {ocr_text.strip() if ocr_text.strip() else "[无]"}

语音转录: {transcript_text.strip()}

要求:
1. 参考OCR纠正转录错误(专业术语、课文标题)
2. 添加标点符号(。,、;:?!)
3. 分段清晰
4. 忠实原文,直接输出结果"""
        
        return prompt
    
    def _format_segments_simple(self, segments: List[Tuple[float, float, str]]) -> str:
        """简单格式化（不使用LLM）"""
        if not segments:
            return ""
        
        # 简单地合并文字并分段
        text = " ".join([s[2] for s in segments])
        
        # 按句子分段
        sentences = re.split(r'[。！？\n]+', text)
        formatted = "\n\n".join([s.strip() for s in sentences if s.strip()])
        
        return formatted
    
    def generate_global_context(self, transcript_segments: List[Tuple[float, float, str]]) -> str:
        """
        生成全局上下文提示词 - 优化版(可选功能,默认不使用)
        
        参数:
            transcript_segments: 所有语音转录段落
            
        返回:
            global_context: 全局上下文描述
        """
        # 优化: 暂时禁用全局上下文生成,减少API调用
        return ""
    
    def batch_refine_all_frames(self, 
                                transcript_segments: List[Tuple[float, float, str]],
                                ocr_results: Dict[str, str],
                                image_times: List[Tuple[float, str]]) -> Dict[str, str]:
        """
        批量处理所有帧的文字精炼
        
        参数:
            transcript_segments: 所有语音转录段落
            ocr_results: OCR识别结果 {image_path: text}
            image_times: 图片时间列表 [(time, path), ...]
            
        返回:
            refined_results: {image_path: refined_text}
        """
        print("=" * 70)
        
        # 检查是否使用批处理模式
        if self.use_batch_mode:
            print("使用批处理模式 - 一次性精炼整个转录")
            print("=" * 70)
            
            # 合并所有转录文字
            full_transcript = " ".join([text for _, _, text in transcript_segments])
            
            # 一次性精炼
            refined_transcript = self.batch_refine_entire_transcript(
                full_transcript,
                ocr_results
            )
            
            # 按帧切分
            refined_results = self.batch_split_by_frames(
                refined_transcript,
                image_times
            )
            
            # 统计
            success_count = sum(1 for text in refined_results.values() if text.strip())
            print(f"\n📊 精炼统计:")
            print(f"  总帧数: {len(refined_results)}")
            print(f"  有内容: {success_count} 个")
            print(f"  空结果: {len(refined_results) - success_count} 个")
            
            return refined_results
        
        # 原来的逐帧模式
        print("使用逐帧模式 - 逐个精炼每一帧")
        print("=" * 70)
        
        # 调试: 检查OCR结果
        ocr_count = sum(1 for text in ocr_results.values() if text.strip())
        print(f"📊 OCR数据检查: 共 {len(ocr_results)} 张图片, {ocr_count} 张有OCR文字")
        
        refined_results = {}
        total = len(image_times)
        success_count = 0
        ocr_used_count = 0
        
        for i, (img_time, img_path) in enumerate(image_times, 1):
            if i < len(image_times):
                end_time = image_times[i][0]
            else:
                end_time = img_time + 60
            
            matching_segments = []
            for seg_start, seg_end, seg_text in transcript_segments:
                seg_mid = (seg_start + seg_end) / 2
                if img_time <= seg_mid < end_time:
                    matching_segments.append((seg_start, seg_end, seg_text))
            
            if not matching_segments:
                refined_results[img_path] = ""
                if i <= 3:
                    print(f"  [{i}/{total}] 无匹配文字 - {os.path.basename(img_path)}")
                continue
            
            ocr_text = ocr_results.get(img_path, "")
            
            if i <= 5 or (i % max(1, total // 10) == 0) or i == total:
                img_basename = os.path.basename(img_path)
                ocr_length = len(ocr_text.strip()) if ocr_text else 0
                time_range = f"[{img_time:.1f}s - {end_time:.1f}s]"
                print(f"  [{i}/{total}] {img_basename} {time_range}, OCR: {ocr_length}字, 转录: {len(matching_segments)}段")
            
            if ocr_text.strip():
                ocr_used_count += 1
            
            refined = self.refine_transcript_with_ocr(
                matching_segments,
                ocr_text,
                img_time,
                ""
            )
            
            if refined.strip():
                success_count += 1
            
            refined_results[img_path] = refined
        
        print(f"  精炼完成: {total}/{total}")
        
        print(f"\n📊 精炼统计:")
        print(f"  总帧数: {len(refined_results)}")
        print(f"  成功精炼: {success_count} 个")
        print(f"  使用了OCR: {ocr_used_count} 个")
        print(f"  空结果: {total - success_count} 个")
        
        return refined_results


    def batch_refine_entire_transcript(self, 
                                       full_transcript: str,
                                       ocr_results: Dict[str, str]) -> str:
        """
        批处理模式: 一次性精炼整个转录文本
        
        参数:
            full_transcript: 完整的转录文本(无标点)
            ocr_results: 所有OCR识别结果 {frame_name: text}
            
        返回:
            refined_transcript: 精炼后的完整文本(有标点、纠错、分段)
        """
        print("=" * 70)
        print("批处理模式: 一次性精炼整个转录文本")
        print("=" * 70)
        
        if not self.client:
            print("⚠️  LLM未配置,返回原文")
            return full_transcript
        
        # 合并所有OCR文字作为参考
        all_ocr_text = "\n".join([
            f"[{name}] {text}" 
            for name, text in ocr_results.items() 
            if text.strip()
        ])
        
        ocr_count = sum(1 for text in ocr_results.values() if text.strip())
        print(f"📊 输入数据:")
        print(f"  - 转录文字: {len(full_transcript)} 字符")
        print(f"  - OCR帧总数: {len(ocr_results)} 个")
        print(f"  - OCR有内容: {ocr_count} 个帧")
        print(f"  - OCR文本长度: {len(all_ocr_text)} 字符")
        
        # 构建简化的批处理prompt
        prompt = f"""你是语文课堂文字整理专家。请为这段课堂讲座录音转写添加标点符号，并结合OCR课件文字纠正错误。

**OCR课件文字(关键参考):**
```
{all_ocr_text[:3000] if len(all_ocr_text) > 3000 else all_ocr_text}
{"...(后续省略)" if len(all_ocr_text) > 3000 else ""}
```

**录音转写文字(需要添加标点和纠错):**
```
{full_transcript[:8000] if len(full_transcript) > 8000 else full_transcript}
{"...(后续省略)" if len(full_transcript) > 8000 else ""}
```

**要求:**
1. 参考OCR纠正转写中的错误(专业术语、课文标题、人名等)
2. 添加准确的标点符号(。,、;:?!等)
3. 适当分段,使内容层次清晰
4. 保持原文意思,不要添加或删除内容
5. 直接输出整理后的文字,不要添加说明

请开始整理:"""
        
        try:
            print(f"⏳ 正在调用LLM精炼 (这需要10-30秒)...")
            import time
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是专业的文字编辑助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10000
            )
            
            elapsed = time.time() - start_time
            
            if response and hasattr(response, 'choices') and response.choices:
                refined_text = response.choices[0].message.content.strip()
                
                print(f"✓ 精炼完成 (耗时: {elapsed:.1f}秒)")
                print(f"  - 输出长度: {len(refined_text)} 字符")
                print(f"  - 效率提升: {len(ocr_results)}帧只需1次API调用!")
                
                return refined_text
            else:
                print(f"⚠️  响应结构异常,返回原文")
                return full_transcript
                
        except Exception as e:
            print(f"❌ LLM调用失败: {e}")
            import traceback
            traceback.print_exc()
            return full_transcript
    
    
    def batch_split_by_frames(self,
                              refined_transcript: str,
                              image_times: List[Tuple[float, str]]) -> Dict[str, str]:
        """
        将整体精炼后的文本按帧时间切分
        
        参数:
            refined_transcript: 精炼后的完整文本
            image_times: 图片时间列表 [(time, path), ...]
            
        返回:
            frame_texts: {frame_name: text}
        """
        print(f"\n⏳ 将精炼文本按帧切分...")
        
        # 简单策略: 按段落数量平均分配
        paragraphs = [p.strip() for p in refined_transcript.split('\n\n') if p.strip()]
        
        if not paragraphs:
            paragraphs = [p.strip() for p in refined_transcript.split('\n') if p.strip()]
        
        frame_count = len(image_times)
        frame_texts = {}
        
        # 计算每帧大约分配多少段落
        paras_per_frame = max(1, len(paragraphs) // frame_count)
        
        for i, (img_time, img_path) in enumerate(image_times):
            frame_name = os.path.basename(img_path)
            
            # 为每帧分配段落
            start_idx = i * paras_per_frame
            end_idx = start_idx + paras_per_frame if i < frame_count - 1 else len(paragraphs)
            
            frame_paras = paragraphs[start_idx:end_idx]
            frame_text = '\n\n'.join(frame_paras)
            
            frame_texts[frame_name] = frame_text
        
        print(f"✓ 切分完成: {len(frame_texts)} 个帧")
        
        return frame_texts


def test_agent():
    """测试Agent"""
    agent = TextRefineAgent()
    
    # 测试数据
    transcript_segments = [
        (0.0, 5.0, "今天我们要学习的科目"),
        (5.0, 10.0, "是关于拜歌的"),
    ]
    
    ocr_text = "我的白鸽\n——陈忠实"
    
    refined = agent.refine_transcript_with_ocr(
        transcript_segments,
        ocr_text,
        0.0
    )
    
    print("=" * 70)
    print("精炼结果:")
    print("=" * 70)
    print(refined)


if __name__ == "__main__":
    test_agent()
