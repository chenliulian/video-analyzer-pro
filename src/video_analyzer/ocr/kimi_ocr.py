#!/usr/bin/env python3
"""
基于 Kimi k2.5 多模态模型的 OCR 识别模块
支持图片文字识别
"""
import os
import sys
import base64
from pathlib import Path
from typing import Optional, List, Dict

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


class KimiOCR:
    """Kimi k2.5 多模态 OCR 识别器"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = "kimi-k2.5"):
        """
        初始化 OCR 识别器
        
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
        
        print(f"✓ Kimi OCR 初始化成功")
        print(f"  模型: {self.model}")
        print(f"  API URL: {self.base_url}")
    
    def _encode_image(self, image_path: str) -> str:
        """将图片转换为 base64 编码"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def recognize_image(self, image_path: str, prompt: Optional[str] = None) -> str:
        """
        识别单张图片中的文字
        
        参数:
            image_path: 图片路径（本地路径）
            prompt: 自定义提示词（默认为 OCR 提示）
            
        返回:
            识别到的文字内容
        """
        # 检查图片是否存在
        abs_path = os.path.abspath(image_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"图片不存在: {abs_path}")
        
        # 默认 OCR 提示词
        if prompt is None:
            prompt = """请识别图片中的所有文字内容。
要求:
1. 按从上到下、从左到右的顺序识别
2. 保持原文的段落结构和换行
3. 忽略水印、logo等非正文内容
4. 如果有表格，请尽量保持表格结构
5. 只输出识别的文字，不要添加任何解释"""
        
        # 将图片转换为 base64
        base64_image = self._encode_image(abs_path)
        
        try:
            # 调用 API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
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
            print(f"❌ 识别失败: {e}")
            return ""
    
    def recognize_images_batch(self, image_paths: List[str], 
                              prompt: Optional[str] = None,
                              show_progress: bool = True) -> Dict[str, str]:
        """
        批量识别多张图片
        
        参数:
            image_paths: 图片路径列表
            prompt: 自定义提示词
            show_progress: 是否显示进度
            
        返回:
            {图片路径: 识别文字} 的字典
        """
        results = {}
        total = len(image_paths)
        
        for i, image_path in enumerate(image_paths, 1):
            if show_progress:
                print(f"\r识别进度: {i}/{total} - {os.path.basename(image_path)}", end="", flush=True)
            
            text = self.recognize_image(image_path, prompt)
            results[image_path] = text
        
        if show_progress:
            print()  # 换行
        
        return results
