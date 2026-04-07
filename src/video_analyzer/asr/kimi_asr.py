#!/usr/bin/env python3
"""
基于 Kimi k2.5 的语音识别模块
使用多模态能力进行音频转录
"""
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    print("请安装 openai SDK:")
    print("pip3 install openai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class KimiASR:
    """Kimi k2.5 语音识别类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = "kimi-k2.5"):
        """
        初始化 Kimi ASR
        
        参数:
            api_key: API 密钥（从 .env 或环境变量读取 LLM_API_KEY）
            base_url: API 基础 URL
            model: 模型名称，默认为 kimi-k2.5
        """
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://coding.dashscope.aliyuncs.com/v1")
        self.model = model
        
        if not self.api_key:
            print("❌ 错误: 未设置 LLM_API_KEY")
            print("\n请在 .env 文件中配置:")
            print("  LLM_API_KEY=sk-xxxxxxxxxxxxxxxx")
            print("\n或使用环境变量:")
            print("  export LLM_API_KEY='sk-xxxxxxxxxxxxxxxx'")
            raise ValueError("未设置 API 密钥")
        
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        print(f"✓ Kimi ASR 初始化成功")
        print(f"  模型: {self.model}")
    
    def transcribe_audio(self, audio_path: str, language: str = "zh") -> str:
        """
        转录音频文件
        
        参数:
            audio_path: 音频文件路径
            language: 语言代码 (默认: zh)
            
        返回:
            转录的文字内容
        """
        # 检查音频文件
        abs_path = os.path.abspath(audio_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"音频文件不存在: {abs_path}")
        
        file_size = os.path.getsize(abs_path) / 1024 / 1024  # MB
        print(f"📁 音频文件: {Path(audio_path).name} ({file_size:.1f} MB)")
        
        # 对于大文件，需要切分处理
        # 这里使用简单的提示词直接转录
        prompt = """请仔细听取这段音频，将内容转录为文字。
要求：
1. 准确识别所有语音内容
2. 保持原文的语句结构和标点
3. 如果有多个说话人，请标注说话人
4. 输出纯文本，不要添加解释"""
        
        try:
            # 读取音频文件并转换为 base64
            import base64
            with open(abs_path, "rb") as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
            
            # 调用 API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "audio_url",
                                "audio_url": {
                                    "url": f"data:audio/mp3;base64,{audio_base64}"
                                }
                            }
                        ]
                    }
                ]
            )
            
            # 提取文字
            text = response.choices[0].message.content
            return text.strip()
            
        except Exception as e:
            print(f"❌ 转录失败: {e}")
            return ""
