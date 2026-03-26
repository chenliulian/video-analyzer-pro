#!/usr/bin/env python3
"""
VideoAnalyzer Pro - 智能视频分析工具
主入口文件
"""

import sys
from pathlib import Path

# 添加src到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from video_analyzer.core.analyzer import main

if __name__ == "__main__":
    main()
