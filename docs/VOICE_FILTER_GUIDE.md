# 人声过滤功能指南

> 自动过滤音乐和背景噪音，只识别人声并转文字

## 🎯 功能特性

### 增强版音频转文字 (v4.2)

✅ **三重过滤机制：**

1. **音频预处理** - 基于静音检测提取有效音频片段
2. **Whisper VAD过滤** - 使用Whisper内置的语音活动检测
3. **智能后处理** - 过滤低置信度和音乐关键词

### 对比标准版

| 功能 | 标准版 | 增强版 |
|------|--------|--------|
| 基础转录 | ✅ | ✅ |
| 静音检测 | ❌ | ✅ |
| VAD过滤 | ❌ | ✅ |
| 音乐过滤 | ❌ | ✅ |
| 置信度过滤 | ❌ | ✅ |
| 人声提取 | ❌ | ✅ |

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装Python依赖
pip3 install pydub

# macOS安装ffmpeg（必需）
brew install ffmpeg

# 或查看完整依赖
pip3 install -r requirements.txt
```

### 2. 基础使用

```bash
# 使用默认参数
python3 extract_audio_to_text_enhanced.py --video your_video.mp4

# 指定模型大小
python3 extract_audio_to_text_enhanced.py --video your_video.mp4 --model medium
```

### 3. 高级参数

```bash
# 完整参数示例
python3 extract_audio_to_text_enhanced.py \
  --video your_video.mp4 \
  --model base \
  --silence-thresh -40 \
  --min-silence 500 \
  --no-vad \
  --no-preprocess
```

## 📊 参数说明

### 基础参数

| 参数 | 说明 | 默认值 | 推荐值 |
|------|------|--------|--------|
| `--video` | 视频文件路径 | 必需 | - |
| `--model` | Whisper模型 | base | base/medium |

### 音频预处理参数

| 参数 | 说明 | 默认值 | 调整建议 |
|------|------|--------|----------|
| `--silence-thresh` | 静音阈值（dBFS） | -40 | 背景音大用-35，安静用-45 |
| `--min-silence` | 最小静音长度（ms） | 500 | 快节奏用300，慢节奏用700 |
| `--no-preprocess` | 禁用音频预处理 | 启用 | 音频干净可禁用 |

### VAD参数

| 参数 | 说明 | 默认值 | 建议 |
|------|------|--------|------|
| `--no-vad` | 禁用VAD过滤 | 启用 | 建议启用 |

### Whisper模型选择

| 模型 | 大小 | 速度 | 准确度 | 推荐场景 |
|------|------|------|--------|----------|
| tiny | 39MB | 最快 | ⭐⭐ | 快速预览 |
| base | 74MB | 快 | ⭐⭐⭐ | 日常使用 ⭐ |
| small | 244MB | 中等 | ⭐⭐⭐⭐ | 准确度优先 |
| medium | 769MB | 慢 | ⭐⭐⭐⭐⭐ | 最佳准确度 |
| large | 1550MB | 最慢 | ⭐⭐⭐⭐⭐ | 专业用途 |

## 🔧 工作原理

### 处理流程

```
视频文件
    ↓
提取音频 (MP3)
    ↓
【步骤1】音频预处理
  - 检测静音片段
  - 提取非静音片段（可能包含人声）
  - 合并人声片段
    ↓
人声音频 (MP3)
    ↓
【步骤2】Whisper转录
  - no_speech_threshold=0.6（过滤纯音乐）
  - condition_on_previous_text=False（减少幻听）
  - vad_filter=True（VAD过滤）
    ↓
原始转录结果
    ↓
【步骤3】智能后处理
  - 过滤太短文本（<2字符）
  - 过滤音乐关键词（♪、music等）
  - 过滤低置信度片段（avg_logprob < -1.0）
  - 过滤高无语音概率片段（no_speech_prob > 0.6）
    ↓
最终转录结果（纯人声）
```

### 关键技术

#### 1. 静音检测（pydub）

```python
# 检测非静音片段
nonsilent_ranges = detect_nonsilent(
    audio,
    min_silence_len=500,  # 最小静音长度
    silence_thresh=-40    # 静音阈值
)
```

**参数调优：**
- 背景音乐大：`silence_thresh=-35`（提高阈值）
- 环境安静：`silence_thresh=-45`（降低阈值）
- 语速快：`min_silence_len=300`（缩短静音）
- 语速慢：`min_silence_len=700`（延长静音）

#### 2. Whisper VAD过滤

```python
result = model.transcribe(
    audio_path,
    no_speech_threshold=0.6,  # 无语音阈值（越高越严格）
    logprob_threshold=-1.0,   # 置信度阈值
    vad_filter=True           # 启用VAD
)
```

**参数说明：**
- `no_speech_threshold`: 0.6-0.8（音乐多用0.7-0.8）
- `logprob_threshold`: -1.0（标准），-0.5（更严格）

#### 3. 后处理过滤

```python
# 过滤条件
1. 文本长度 < 2字符
2. 包含音乐关键词（♪、music、lalala等）
3. 平均对数概率 < -1.0（置信度低）
4. 无语音概率 > 0.6（可能是音乐）
```

## 💡 使用场景

### 场景1：在线课程（有背景音乐）

```bash
# 推荐配置
python3 extract_audio_to_text_enhanced.py \
  --video course.mp4 \
  --model base \
  --silence-thresh -35 \
  --min-silence 500
```

### 场景2：会议录音（环境安静）

```bash
# 可以禁用预处理，加快速度
python3 extract_audio_to_text_enhanced.py \
  --video meeting.mp4 \
  --model small \
  --no-preprocess
```

### 场景3：纪录片（音乐+解说）

```bash
# 使用更严格的过滤
python3 extract_audio_to_text_enhanced.py \
  --video documentary.mp4 \
  --model medium \
  --silence-thresh -30
```

### 场景4：快速预览

```bash
# 使用tiny模型快速转录
python3 extract_audio_to_text_enhanced.py \
  --video video.mp4 \
  --model tiny
```

## 📈 效果对比

### 标准版（无过滤）

```
[0.00s - 2.60s] 好 passed our 1000 m
[20.32s - 21.92s] 今天我們要學習的柯文 ende
[21.92s - 23.42s] 過的白歌
...
（包含音乐、噪音、幻听）
```

### 增强版（三重过滤）

```
[20.32s - 21.92s] 今天我们要学习的课文
[21.92s - 23.42s] 我的白鸽
[24.94s - 26.54s] 在阅读文章之前
...
（仅保留清晰的人声）
```

**改进效果：**
- ✅ 过滤掉开头的音乐片段
- ✅ 去除背景噪音识别
- ✅ 减少幻听错误
- ✅ 提高文本可读性

## 🔍 输出文件

### 生成的文件

```
your_video.mp4                          # 原始视频
your_video.mp3                          # 提取的音频
your_video_voice_only.mp3               # 人声音频（预处理后）
your_video_transcript_enhanced.txt      # 增强版转录结果 ⭐
```

### 转录文件格式

```text
=== 完整转录文本（已过滤音乐）===

今天我们要学习的课文我的白鸽 在阅读文章之前...

=== 分段转录 ===

[20.32s - 21.92s] 今天我们要学习的课文 (置信度: -0.35, 无语音: 0.12)
[21.92s - 23.42s] 我的白鸽 (置信度: -0.28, 无语音: 0.08)
[24.94s - 26.54s] 在阅读文章之前 (置信度: -0.41, 无语音: 0.15)
...
```

**字段说明：**
- 时间戳：该段音频的起止时间
- 文本：识别的内容
- 置信度：越接近0越准确（-0.5以上表示高置信度）
- 无语音概率：越低越好（0.3以下表示确定是人声）

## 🛠️ 故障排除

### Q1: 提示缺少 ffmpeg

**症状：**
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**解决方案：**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# 验证安装
ffmpeg -version
```

### Q2: pydub 安装失败

**解决方案：**
```bash
pip3 install pydub

# 如果失败，使用国内镜像
pip3 install pydub -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 人声被过滤掉了

**原因：** 阈值设置太严格

**解决方案：**
```bash
# 降低静音阈值
python3 extract_audio_to_text_enhanced.py \
  --video video.mp4 \
  --silence-thresh -45  # 从-40降到-45

# 或禁用预处理
python3 extract_audio_to_text_enhanced.py \
  --video video.mp4 \
  --no-preprocess
```

### Q4: 还是识别到音乐

**原因：** 音乐和人声重叠太多

**解决方案：**
```bash
# 提高无语音阈值（修改代码）
# 在 transcribe_audio_with_vad 函数中修改：
no_speech_threshold=0.8  # 从0.6提高到0.8
```

### Q5: 处理速度太慢

**解决方案：**
```bash
# 1. 使用更小的模型
python3 extract_audio_to_text_enhanced.py --video video.mp4 --model tiny

# 2. 禁用预处理
python3 extract_audio_to_text_enhanced.py --video video.mp4 --no-preprocess

# 3. 使用GPU（如果有）
# 安装GPU版PyTorch：https://pytorch.org/
```

## 📚 集成到Pro版

### 更新 video_analyzer_pro.py

```python
# 替换音频转录部分
from extract_audio_to_text_enhanced import (
    extract_audio,
    detect_voice_segments,
    filter_voice_segments,
    transcribe_audio_with_vad,
    post_process_transcript
)

# 使用增强版转录
def _parse_transcript(self):
    # 提取音频
    audio_file = f"{self.video_id}.mp3"
    voice_audio = f"{self.video_id}_voice_only.mp3"
    
    # 人声检测
    voice_segments = detect_voice_segments(audio_file)
    filter_voice_segments(audio_file, voice_segments, voice_audio)
    
    # VAD转录
    result = transcribe_audio_with_vad(voice_audio, model_size="base")
    
    # 后处理
    filtered_result = post_process_transcript(result)
    
    return filtered_result["segments"]
```

## 🎓 最佳实践

### 1. 参数调优流程

```bash
# Step 1: 先用默认参数测试
python3 extract_audio_to_text_enhanced.py --video test.mp4

# Step 2: 如果过滤太多，降低阈值
python3 extract_audio_to_text_enhanced.py --video test.mp4 --silence-thresh -45

# Step 3: 如果过滤太少，提高阈值
python3 extract_audio_to_text_enhanced.py --video test.mp4 --silence-thresh -35

# Step 4: 找到最佳参数后固定使用
```

### 2. 模型选择策略

- **快速预览** → tiny模型
- **日常使用** → base模型（推荐）
- **准确度优先** → medium模型
- **专业用途** → large模型

### 3. 批量处理

```bash
# 批量处理多个视频
for video in *.mp4; do
    python3 extract_audio_to_text_enhanced.py --video "$video" --model base
done
```

## 📖 相关文档

- [README_PRO.md](README_PRO.md) - Pro版功能介绍
- [QUICK_START.md](QUICK_START.md) - 快速开始
- [Whisper文档](https://github.com/openai/whisper) - Whisper官方文档
- [pydub文档](https://github.com/jiaaro/pydub) - pydub使用指南

---

**版本**: v4.2  
**更新日期**: 2025-12-06  
**新功能**: 人声过滤、VAD检测、智能后处理
