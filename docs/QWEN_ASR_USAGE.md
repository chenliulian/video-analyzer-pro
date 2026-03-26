# Qwen ASR 使用指南

## 📋 简介

`audio_qwen.py` 提供了基于阿里云 **Qwen3-ASR-Flash** 模型的语音转文字功能,可以作为 Whisper 的替代方案。

### 优势
- ✅ **云端识别**: 无需本地GPU,速度快
- ✅ **中文优化**: 针对中文语音优化,识别准确率高
- ✅ **低资源消耗**: 不占用本地计算资源

### 限制
- ⚠️ **需要网络**: 必须联网才能使用
- ⚠️ **无时间戳**: 默认不返回段落级时间戳 (返回完整文本)
- ⚠️ **收费服务**: 需要阿里云 API Key (有免费额度)

---

## 🔧 安装

### 1. 安装依赖
```bash
pip3 install dashscope
```

### 2. 获取 API Key
访问: https://help.aliyun.com/zh/model-studio/get-api-key

### 3. 配置 API Key
在项目根目录的 `.env` 文件中添加:
```bash
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
```

---

## 🚀 使用方法

### 方法1: 单独使用 audio_qwen.py

```bash
# 基本用法
python3 audio_qwen.py --audio path/to/audio.mp3

# 指定语言
python3 audio_qwen.py --audio path/to/audio.mp3 --language zh

# 启用反向文本规范化 (数字、日期格式化)
python3 audio_qwen.py --audio path/to/audio.mp3 --enable-itn

# 使用国内版 API (北京)
python3 audio_qwen.py --audio path/to/audio.mp3 --region cn
```

### 方法2: 在 video_analyzer_pro.py 中使用

```bash
# 使用 Qwen ASR 进行语音识别
python3 video_analyzer_pro.py --video data/video.mp4 --asr-engine qwen

# 或者继续使用 Whisper (默认)
python3 video_analyzer_pro.py --video data/video.mp4 --asr-engine whisper
```

### 方法3: 在 Python 代码中使用

```python
from audio_qwen import QwenASR, transcribe_audio_file

# 方式1: 使用便捷函数
text = transcribe_audio_file(
    audio_file_path="path/to/audio.mp3",
    language="zh",
    enable_itn=False
)
print(text)

# 方式2: 使用类
asr = QwenASR(region="intl")  # "intl" 或 "cn"
text = asr.transcribe_audio(
    audio_file_path="path/to/audio.mp3",
    language="zh",
    enable_itn=False,
    system_prompt="这是一节课堂讲座"  # 可选
)
print(text)
```

---

## 📝 video_analyzer_pro.py 集成示例

### 修改 __init__ 参数

```python
from video_analyzer_pro import VideoAnalyzerPro

# 使用 Qwen ASR
analyzer = VideoAnalyzerPro(
    video_file="data/video.mp4",
    asr_engine="qwen",  # 选择 Qwen ASR
    asr_config={
        "api_key": "sk-xxx",  # 可选,默认从环境变量读取
        "region": "intl",     # "intl" 新加坡 或 "cn" 北京
        "language": "zh",     # 语言代码
        "enable_itn": False   # 是否启用反向文本规范化
    }
)

# 使用 Whisper (默认)
analyzer = VideoAnalyzerPro(
    video_file="data/video.mp4",
    asr_engine="whisper",
    whisper_model="base"
)
```

---

## 🔍 参数说明

### QwenASR 类参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `api_key` | str | 环境变量 | 阿里云 API Key |
| `region` | str | "intl" | 地域: "intl"(新加坡) 或 "cn"(北京) |

### transcribe_audio 方法参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `audio_file_path` | str | 必填 | 音频文件的绝对路径 |
| `language` | str | None | 语言代码 (如 "zh", "en") |
| `enable_itn` | bool | False | 是否启用反向文本规范化 |
| `system_prompt` | str | "" | 系统提示词 (可用于定制化识别) |

### video_analyzer_pro.py 参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| `asr_engine` | str | "whisper" | 语音引擎: "whisper" 或 "qwen" |
| `asr_config` | dict | {} | Qwen ASR 配置字典 |

---

## 📊 Qwen ASR vs Whisper 对比

| 特性 | Qwen ASR | Whisper |
|-----|----------|---------|
| **识别准确率** | ⭐⭐⭐⭐⭐ (中文) | ⭐⭐⭐⭐ |
| **速度** | ⭐⭐⭐⭐⭐ (云端) | ⭐⭐⭐ (本地CPU) |
| **资源消耗** | ⭐⭐⭐⭐⭐ (无) | ⭐⭐ (CPU密集) |
| **时间戳支持** | ❌ 无段落时间戳 | ✅ 精确时间戳 |
| **离线使用** | ❌ 需要联网 | ✅ 可离线 |
| **成本** | 💰 收费 (有免费额度) | 🆓 免费 |

### 选择建议

**使用 Qwen ASR** 适合:
- ✅ 主要处理中文内容
- ✅ 对速度要求高
- ✅ 本地资源有限 (如云服务器)
- ✅ 不需要精确的时间戳

**使用 Whisper** 适合:
- ✅ 需要精确的段落时间戳
- ✅ 需要离线使用
- ✅ 处理多语言混合内容
- ✅ 对成本敏感 (完全免费)

---

## ⚠️ 注意事项

### 1. 时间戳限制
Qwen ASR 默认**不返回段落级时间戳**,只返回完整文本。如果您的应用严重依赖时间戳信息,建议使用 Whisper。

**解决方案**:
- 使用 Whisper 进行转录 (推荐)
- 或者手动添加 VAD (语音活动检测) 来分段

### 2. 文件格式要求
- 支持常见音频格式: MP3, WAV, M4A, FLAC 等
- 文件路径必须是**绝对路径**
- 自动转换为 `file://` URL 格式

### 3. API Key 安全
- ❌ 不要在代码中硬编码 API Key
- ✅ 使用环境变量或 `.env` 文件
- ✅ 将 `.env` 添加到 `.gitignore`

### 4. 网络要求
- 需要稳定的网络连接
- 国际版 API (新加坡) 在中国大陆可能较慢
- 国内用户建议使用 `region="cn"`

---

## 🐛 常见问题

### Q1: 提示 "未设置 DASHSCOPE_API_KEY"
**解决方案**: 
```bash
# 在 .env 文件中添加
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx

# 或使用环境变量
export DASHSCOPE_API_KEY='sk-xxxxxxxxxxxxxxxx'
```

### Q2: 转录结果为空或失败
**可能原因**:
- API Key 无效或过期
- 网络连接问题
- 音频文件格式不支持
- API 额度用完

**解决方案**:
- 检查 API Key 是否正确
- 测试网络连接
- 转换音频格式为 MP3 或 WAV
- 查看阿里云控制台的额度使用情况

### Q3: 如何获取带时间戳的转录?
**解决方案**: Qwen ASR 不支持时间戳,请使用 Whisper:
```python
analyzer = VideoAnalyzerPro(
    video_file="data/video.mp4",
    asr_engine="whisper",  # 使用 Whisper
    whisper_model="base"
)
```

### Q4: 国际版 API 太慢怎么办?
**解决方案**: 使用国内版 API (需要国内的 API Key):
```python
asr = QwenASR(region="cn")
```

---

## 📚 相关链接

- **阿里云模型工作室**: https://help.aliyun.com/zh/model-studio/
- **API Key 获取**: https://help.aliyun.com/zh/model-studio/get-api-key
- **Qwen ASR 文档**: https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-audio-models
- **Dashscope SDK**: https://help.aliyun.com/zh/dashscope/developer-reference/sdk-overview

---

## 📄 示例代码

### 完整示例: 视频分析使用 Qwen ASR

```python
#!/usr/bin/env python3
from video_analyzer_pro import VideoAnalyzerPro

# 配置
video_file = "data/lecture.mp4"

# 使用 Qwen ASR
analyzer = VideoAnalyzerPro(
    video_file=video_file,
    use_llm=True,
    asr_engine="qwen",
    asr_config={
        "region": "intl",
        "language": "zh",
        "enable_itn": False
    },
    ocr_config={
        "model": "qwen-vl-max"
    },
    skip_existing=True
)

# 运行分析
analyzer.run()

print("\n分析完成!")
print(f"PDF 文件: results/{analyzer.video_id}_frames_pro.pdf")
```

---

## 🎯 总结

`audio_qwen.py` 提供了一个**快速、准确的云端中文语音识别方案**,特别适合:
- 中文为主的教学视频分析
- 对速度有要求的批量处理
- 本地资源有限的环境

虽然没有时间戳支持,但在许多场景下,完整的文本转录已经足够满足需求。如果您需要精确的时间对应,建议继续使用 Whisper。
