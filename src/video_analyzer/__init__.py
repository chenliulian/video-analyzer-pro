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
from .asr.kimi_asr import KimiASR
from .llm.refine_agent import TextRefineAgent

__all__ = [
    "VideoAnalyzerPro",
    "KimiOCR",
    "KimiASR",
    "TextRefineAgent",
]
