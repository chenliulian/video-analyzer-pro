#!/usr/bin/env python3
"""
VideoAnalyzer Pro - API使用示例
展示如何单独使用各个模块
"""

import sys
from pathlib import Path

# 添加src到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from video_analyzer.ocr import QwenOCR
from video_analyzer.asr import QwenASR
from video_analyzer.llm import TextRefineAgent


def ocr_example():
    """OCR识别示例"""
    
    # 初始化OCR
    ocr = QwenOCR(
        api_key="your-dashscope-api-key",  # 或从环境变量读取
        model="qwen-vl-max"
    )
    
    # 识别单张图片
    text = ocr.recognize_image("path/to/image.jpg")
    print(f"识别结果:\n{text}")
    
    # 批量识别
    image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
    results = ocr.recognize_images_batch(image_paths)
    
    for path, text in results.items():
        print(f"\n{path}:")
        print(text)


def asr_example():
    """语音识别示例"""
    
    # 初始化ASR
    asr = QwenASR(
        api_key="your-dashscope-api-key",
        region="intl"  # 或 "cn" 国内版
    )
    
    # 转录音频
    text = asr.transcribe_audio(
        audio_file_path="path/to/audio.mp3",
        language="zh",
        enable_itn=False
    )
    
    print(f"转录结果:\n{text}")


def llm_example():
    """LLM文本精炼示例"""
    
    # 初始化Agent
    agent = TextRefineAgent(
        api_key="your-llm-api-key",
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
        use_batch_mode=True
    )
    
    # 准备数据
    transcript_segments = [
        (0.0, 5.0, "今天我们要学习的内容是"),
        (5.0, 10.0, "关于人工智能的基础知识"),
    ]
    
    ocr_text = "人工智能基础\n第一章 绪论"
    
    # 精炼
    refined = agent.refine_transcript_with_ocr(
        transcript_segments=transcript_segments,
        ocr_text=ocr_text,
        frame_time=0.0
    )
    
    print(f"精炼结果:\n{refined}")


if __name__ == "__main__":
    # 运行示例
    # ocr_example()
    # asr_example()
    # llm_example()
    pass
