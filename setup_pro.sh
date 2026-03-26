#!/bin/bash
# 视频分析器Pro版安装脚本

echo "=================================="
echo "视频分析器 Pro 版安装脚本"
echo "=================================="

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 安装基础依赖
echo ""
echo "【1/3】安装基础依赖..."
pip3 install moviepy pillow numpy opencv-python openai-whisper torch

# 安装OCR依赖
echo ""
echo "【2/3】安装OCR依赖..."
echo "选择OCR引擎："
echo "  1) PaddleOCR (推荐，中文识别效果最好)"
echo "  2) Tesseract"
echo "  3) 两者都安装"
read -p "请选择 [1-3]: " ocr_choice

case $ocr_choice in
    1)
        echo "安装PaddleOCR..."
        pip3 install paddleocr paddlepaddle
        ;;
    2)
        echo "安装Tesseract..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "检测到macOS，使用Homebrew安装..."
            brew install tesseract tesseract-lang
        fi
        pip3 install pytesseract
        ;;
    3)
        echo "安装PaddleOCR和Tesseract..."
        pip3 install paddleocr paddlepaddle
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install tesseract tesseract-lang
        fi
        pip3 install pytesseract
        ;;
    *)
        echo "无效选择，跳过OCR安装"
        ;;
esac

# 安装LLM依赖
echo ""
echo "【3/3】安装LLM依赖..."
pip3 install openai

echo ""
echo "=================================="
echo "✓ 安装完成！"
echo "=================================="
echo ""
echo "下一步："
echo "1. 配置API密钥（如果使用LLM功能）："
echo "   export OPENAI_API_KEY='your-api-key'"
echo ""
echo "2. 运行测试："
echo "   python3 video_analyzer_pro.py --video test.mp4 --no-llm"
echo ""
echo "3. 查看完整文档："
echo "   cat PRO_VERSION_GUIDE.md"
echo ""
