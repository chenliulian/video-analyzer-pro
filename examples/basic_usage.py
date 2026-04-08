#!/usr/bin/env python3
"""
VideoAnalyzer Pro - 基础使用示例
"""

import sys
from pathlib import Path

# 添加src到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from video_analyzer import VideoAnalyzerPro


def basic_example():
    """基础使用示例"""
    
    # 配置
    video_file = "data/lecture.mp4"  # 替换为你的视频文件
    
    # 创建分析器实例
    analyzer = VideoAnalyzerPro(
        video_file=video_file,
        use_llm=True,  # 使用LLM精炼
        whisper_model="base",  # Whisper模型大小
        asr_engine="whisper",  # 语音识别引擎
        skip_existing=True  # 跳过已存在的文件
    )
    
    # 运行完整流程
    analyzer.run_full_pipeline()


def advanced_example():
    """高级使用示例 - 自定义配置"""
    
    video_file = "data/lecture.mp4"
    
    # LLM配置
    llm_config = {
        "api_key": "your-api-key",  # 或从.env读取
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4"
    }
    
    # OCR配置 (使用 Kimi)
    ocr_config = {
        "api_key": "your-api-key",  # 或从.env读取
        "base_url": "https://api.openai.com/v1",
        "model": "kimi-k2.5"
    }
    
    # ASR配置 (使用 Kimi)
    asr_config = {
        "api_key": "your-api-key",
        "base_url": "https://api.openai.com/v1",
        "model": "kimi-k2.5",
        "language": "zh"
    }
    
    # 创建分析器
    analyzer = VideoAnalyzerPro(
        video_file=video_file,
        use_llm=True,
        llm_config=llm_config,
        ocr_config=ocr_config,
        whisper_model="base",
        asr_engine="kimi",  # 使用 Kimi ASR
        asr_config=asr_config,
        skip_existing=True
    )
    
    # 运行
    analyzer.run_full_pipeline()


def batch_example():
    """批量处理示例"""
    
    import glob
    
    # 获取所有视频文件
    video_files = glob.glob("data/*.mp4")
    
    for video_file in video_files:
        print(f"\n处理视频: {video_file}")
        print("=" * 70)
        
        try:
            analyzer = VideoAnalyzerPro(
                video_file=video_file,
                use_llm=True,
                skip_existing=True
            )
            analyzer.run_full_pipeline()
        except Exception as e:
            print(f"处理失败: {e}")
            continue


if __name__ == "__main__":
    # 运行基础示例
    basic_example()
    
    # 或运行高级示例
    # advanced_example()
    
    # 或运行批量处理
    # batch_example()
