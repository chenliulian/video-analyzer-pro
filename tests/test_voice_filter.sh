#!/bin/bash
# 测试人声过滤功能

echo "========================================================================"
echo "              人声过滤功能测试"
echo "========================================================================"
echo ""

# 检查依赖
echo "【检查依赖】"
echo "----------------------------------------------------------------------"

# 检查 ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✓ ffmpeg: $(ffmpeg -version 2>&1 | head -1)"
else
    echo "❌ ffmpeg 未安装"
    echo ""
    echo "安装方法:"
    echo "  macOS:    brew install ffmpeg"
    echo "  Ubuntu:   sudo apt install ffmpeg"
    echo ""
    exit 1
fi

# 检查 pydub
if python3 -c "import pydub" 2>/dev/null; then
    echo "✓ pydub 已安装"
else
    echo "⚠️  pydub 未安装"
    echo "正在安装..."
    pip3 install pydub -q
    
    if [ $? -eq 0 ]; then
        echo "✓ pydub 安装成功"
    else
        echo "❌ pydub 安装失败"
        echo "请手动安装: pip3 install pydub"
        exit 1
    fi
fi

# 检查 whisper
if python3 -c "import whisper" 2>/dev/null; then
    echo "✓ Whisper 已安装"
else
    echo "❌ Whisper 未安装"
    echo "请安装: pip3 install openai-whisper"
    exit 1
fi

echo ""

# 检查视频文件
echo "【检查视频文件】"
echo "----------------------------------------------------------------------"

VIDEO_FILE="1732328440969754.mp4"

if [ -f "$VIDEO_FILE" ]; then
    echo "✓ 找到视频文件: $VIDEO_FILE"
    FILE_SIZE=$(du -h "$VIDEO_FILE" | cut -f1)
    echo "  文件大小: $FILE_SIZE"
else
    echo "❌ 未找到视频文件: $VIDEO_FILE"
    echo ""
    echo "请将视频文件放在当前目录，或修改脚本中的 VIDEO_FILE 变量"
    exit 1
fi

echo ""

# 运行测试
echo "【运行人声过滤转录】"
echo "========================================================================"
echo "配置:"
echo "  模型: base（快速+准确平衡）"
echo "  静音阈值: -40 dBFS"
echo "  最小静音: 500ms"
echo "  VAD过滤: 启用"
echo "  音频预处理: 启用"
echo "========================================================================"
echo ""

python3 extract_audio_to_text_enhanced.py \
  --video "$VIDEO_FILE" \
  --model base \
  --silence-thresh -40 \
  --min-silence 500

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================================================"
    echo "                    测试完成！"
    echo "========================================================================"
    echo ""
    echo "生成的文件:"
    echo "  1. ${VIDEO_FILE%.mp4}.mp3 - 原始音频"
    echo "  2. ${VIDEO_FILE%.mp4}_voice_only.mp3 - 人声音频"
    echo "  3. ${VIDEO_FILE%.mp4}_transcript_enhanced.txt - 转录结果 ⭐"
    echo ""
    echo "对比查看:"
    echo "  原始转录: cat ${VIDEO_FILE%.mp4}_transcript.txt"
    echo "  增强转录: cat ${VIDEO_FILE%.mp4}_transcript_enhanced.txt"
    echo ""
    echo "📚 详细说明: cat VOICE_FILTER_GUIDE.md"
    echo "========================================================================"
else
    echo ""
    echo "❌ 转录失败，请查看错误信息"
    exit 1
fi
