"""ASR模块 - 语音识别"""

from .kimi_asr import KimiASR

# 尝试导入 QwenASR，如果 dashscope 未安装则跳过
try:
    from .qwen_asr import QwenASR
    __all__ = ["KimiASR", "QwenASR"]
except ImportError:
    __all__ = ["KimiASR"]