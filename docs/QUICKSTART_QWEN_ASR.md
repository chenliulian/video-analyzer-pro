# Qwen ASR 快速开始 🚀

## 5分钟快速上手

### 1️⃣ 安装依赖
```bash
pip3 install dashscope
```

### 2️⃣ 配置 API Key
在项目根目录创建 `.env` 文件:
```bash
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
```

获取 API Key: https://help.aliyun.com/zh/model-studio/get-api-key

### 3️⃣ 测试语音识别
```bash
# 测试单个音频文件
python3 audio_qwen.py --audio results/1732328440969754.mp3

# 查看帮助
python3 audio_qwen.py --help
```

### 4️⃣ 在视频分析中使用
```bash
# 方式1: 使用 Qwen ASR
python3 video_analyzer_pro.py --video data/video.mp4 --asr-engine qwen

# 方式2: 使用 Whisper (默认)
python3 video_analyzer_pro.py --video data/video.mp4 --asr-engine whisper
```

---

## 命令行参数

### audio_qwen.py 参数
```bash
python3 audio_qwen.py \
  --audio <音频文件路径> \
  [--language zh] \
  [--enable-itn] \
  [--region intl|cn]
```

### video_analyzer_pro.py 新增参数
```bash
python3 video_analyzer_pro.py \
  --video <视频文件> \
  --asr-engine qwen|whisper \  # 选择语音引擎
  [其他参数...]
```

---

## Python 代码示例

### 示例1: 单独使用
```python
from audio_qwen import transcribe_audio_file

text = transcribe_audio_file(
    audio_file_path="path/to/audio.mp3",
    language="zh"
)
print(text)
```

### 示例2: 在视频分析中使用
```python
from video_analyzer_pro import VideoAnalyzerPro

analyzer = VideoAnalyzerPro(
    video_file="data/video.mp4",
    asr_engine="qwen",
    asr_config={
        "region": "intl",
        "language": "zh"
    }
)
analyzer.run()
```

---

## 常见问题

### Q: Qwen ASR 和 Whisper 哪个好?
**A**: 
- **Qwen ASR**: 中文准确率高,速度快,但无时间戳,需要联网
- **Whisper**: 有精确时间戳,可离线,免费,但速度较慢

### Q: 如何切换引擎?
**A**: 使用 `--asr-engine` 参数:
```bash
# Qwen ASR
python3 video_analyzer_pro.py --video data/video.mp4 --asr-engine qwen

# Whisper
python3 video_analyzer_pro.py --video data/video.mp4 --asr-engine whisper
```

### Q: 需要修改现有代码吗?
**A**: 不需要! 默认继续使用 Whisper,只有指定 `--asr-engine qwen` 时才切换。

---

## 详细文档

查看完整文档: `docs/QWEN_ASR_USAGE.md`

---

## 快速对比

| 特性 | Qwen ASR | Whisper |
|-----|----------|---------|
| 中文准确率 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 速度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 时间戳 | ❌ | ✅ |
| 离线使用 | ❌ | ✅ |
| 成本 | 💰 | 🆓 |

**推荐**: 
- 需要时间戳 → 使用 **Whisper**
- 纯文本识别 + 速度优先 → 使用 **Qwen ASR**
