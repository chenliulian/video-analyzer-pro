"""
VideoAnalyzer Pro - 智能视频分析工具

一个功能强大的视频内容分析工具，能够自动提取视频中的关键帧、
音频转录、OCR文字识别，并通过大语言模型整合生成结构化的PDF和Word文档。
"""

__version__ = "2.0.0"
__author__ = "VideoAnalyzer Team"
__email__ = "support@videoanalyzer.com"

from .core.analyzer import VideoAnalyzerPro
from .ocr.kimi_ocr import KimiOCR
from .llm.refine_agent import TextRefineAgent

# 尝试导入 QwenASR，如果 dashscope 未安装则跳过
try:
    from .asr.qwen_asr import QwenASR
    __all__ = [
        "VideoAnalyzerPro",
        "KimiOCR",
        "QwenASR",
        "TextRefineAgent",
    ]
except ImportError:
    __all__ = [
        "VideoAnalyzerPro",
        "KimiOCR",
        "TextRefineAgent",
    ]