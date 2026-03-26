# Qwen ASR 集成完成 ✅

## 📋 完成内容

根据您提供的阿里云 Qwen ASR 示例代码,我已经完成了以下工作:

### 1️⃣ 创建 `audio_qwen.py` 脚本 ✅

**功能**:
- ✅ 封装了阿里云 Qwen3-ASR-Flash 模型
- ✅ 提供 `QwenASR` 类和便捷函数
- ✅ 支持命令行独立使用
- ✅ 支持被 `video_analyzer_pro.py` 调用

**核心类和方法**:
```python
class QwenASR:
    def __init__(self, api_key=None, region="intl")
    def transcribe_audio(self, audio_file_path, language=None, enable_itn=False)
    def transcribe_audio_with_timestamps(self, audio_file_path, ...)
    
# 便捷函数
def transcribe_audio_file(audio_file_path, api_key=None, language="zh", ...)
```

---

### 2️⃣ 集成到 `video_analyzer_pro.py` ✅

**修改内容**:

#### 1. 导入模块
```python
# 尝试导入 Qwen ASR (可选)
try:
    from audio_qwen import QwenASR
    HAS_QWEN_ASR = True
except ImportError:
    HAS_QWEN_ASR = False
```

#### 2. 新增初始化参数
```python
def __init__(self, 
             ...
             asr_engine: str = "whisper",      # 新增
             asr_config: Optional[Dict] = None, # 新增
             ...):
```

#### 3. 重构语音转录逻辑
```python
def _step3_audio_to_text(self):
    """根据 asr_engine 选择不同引擎"""
    if self.asr_engine == "qwen":
        return self._transcribe_with_qwen()  # 新增
    else:
        return self._transcribe_with_whisper()  # 重构

def _transcribe_with_qwen(self):
    """使用 Qwen ASR"""
    asr = QwenASR(...)
    result = asr.transcribe_audio(...)
    # 保存结果并返回

def _transcribe_with_whisper(self):
    """使用 Whisper (原有逻辑)"""
    model = whisper.load_model(...)
    result = model.transcribe(...)
    # 保存结果并返回
```

---

### 3️⃣ 更新依赖和文档 ✅

**更新的文件**:
- ✅ `requirements.txt` - 添加 dashscope 注释
- ✅ `docs/QWEN_ASR_USAGE.md` - 完整使用文档
- ✅ `QUICKSTART_QWEN_ASR.md` - 快速开始指南
- ✅ `QWEN_ASR_集成说明.md` - 本文档

---

## 🚀 使用方式

### 方式1: 命令行 (video_analyzer_pro.py)

```bash
# 使用 Qwen ASR (需要 DASHSCOPE_API_KEY)
python3 video_analyzer_pro.py --video data/video.mp4 --asr-engine qwen

# 使用 Whisper (默认,无需配置)
python3 video_analyzer_pro.py --video data/video.mp4 --asr-engine whisper
```

### 方式2: 命令行 (audio_qwen.py 单独使用)

```bash
# 测试单个音频文件
python3 audio_qwen.py --audio results/audio.mp3 --language zh

# 查看帮助
python3 audio_qwen.py --help
```

### 方式3: Python 代码

#### 独立使用
```python
from audio_qwen import transcribe_audio_file

text = transcribe_audio_file(
    audio_file_path="path/to/audio.mp3",
    language="zh",
    enable_itn=False
)
print(text)
```

#### 集成使用
```python
from video_analyzer_pro import VideoAnalyzerPro

analyzer = VideoAnalyzerPro(
    video_file="data/video.mp4",
    asr_engine="qwen",  # 选择 Qwen ASR
    asr_config={
        "api_key": "sk-xxx",  # 可选
        "region": "intl",
        "language": "zh",
        "enable_itn": False
    }
)
analyzer.run()
```

---

## 📝 配置说明

### 1. API Key 配置

在项目根目录创建 `.env` 文件:
```bash
# 阿里云 API Key (Qwen ASR 使用)
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx

# 其他配置 (可选)
LLM_API_KEY=xxx
LLM_BASE_URL=xxx
LLM_MODEL=xxx
```

### 2. 获取 API Key

访问: https://help.aliyun.com/zh/model-studio/get-api-key

---

## 🔧 参数详解

### asr_engine 参数
- `"whisper"` (默认): 使用 OpenAI Whisper 模型
- `"qwen"`: 使用阿里云 Qwen ASR 模型

### asr_config 参数 (仅 Qwen ASR 使用)
```python
asr_config = {
    "api_key": "sk-xxx",      # API Key (可选,默认从环境变量读取)
    "region": "intl",         # 地域: "intl"(新加坡) 或 "cn"(北京)
    "language": "zh",         # 语言: "zh"(中文) 或 "en"(英文)
    "enable_itn": False       # 反向文本规范化 (数字、日期格式化)
}
```

---

## 📊 两种引擎对比

| 特性 | Qwen ASR | Whisper |
|-----|----------|---------|
| **中文准确率** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **速度** | ⭐⭐⭐⭐⭐ (云端) | ⭐⭐⭐ (本地) |
| **资源消耗** | ⭐⭐⭐⭐⭐ (无) | ⭐⭐ (CPU密集) |
| **时间戳** | ❌ 无段落时间戳 | ✅ 精确时间戳 |
| **离线使用** | ❌ 需要联网 | ✅ 可离线 |
| **成本** | 💰 收费 (有免费额度) | 🆓 完全免费 |

### 选择建议

**使用 Qwen ASR** 适合:
- ✅ 主要处理中文语音
- ✅ 对速度要求高
- ✅ 本地资源有限
- ⚠️ 不严格依赖时间戳

**使用 Whisper** 适合:
- ✅ 需要精确的段落时间戳
- ✅ 需要离线使用
- ✅ 多语言混合内容
- ✅ 对成本敏感

---

## ⚠️ 重要注意事项

### 1. 时间戳限制
Qwen ASR **不返回段落级时间戳**,只返回完整文本。

**当前处理方式**:
- 将整段文本保存为一个段落: `[0.00s - 0.00s] 完整文本`
- 在 PDF 生成中可能影响图文对应精度

**解决方案**:
- 如需精确时间戳,请使用 Whisper
- 或手动添加 VAD 进行分段 (需额外开发)

### 2. 向后兼容
- ✅ 默认继续使用 Whisper
- ✅ 现有代码无需修改
- ✅ 只有显式指定 `asr_engine="qwen"` 才切换

### 3. 依赖安装
```bash
# Qwen ASR 依赖
pip3 install dashscope

# 如果未安装,会自动回退到 Whisper
```

---

## 🧪 测试步骤

### 1. 测试 audio_qwen.py
```bash
# 编译检查
python3 -m py_compile audio_qwen.py

# 功能测试 (需要配置 API Key)
python3 audio_qwen.py --audio results/1732328440969754.mp3
```

### 2. 测试 video_analyzer_pro.py 集成
```bash
# 测试 Qwen ASR
python3 video_analyzer_pro.py --video data/1732328440969754.mp4 --asr-engine qwen

# 测试 Whisper (确保向后兼容)
python3 video_analyzer_pro.py --video data/1732328440969754.mp4 --asr-engine whisper
```

---

## 📁 文件清单

```
VedioAnalyzer/
├── audio_qwen.py                    # 新增: Qwen ASR 核心模块
├── video_analyzer_pro.py            # 修改: 集成 Qwen ASR
├── requirements.txt                 # 修改: 添加 dashscope 说明
├── QUICKSTART_QWEN_ASR.md          # 新增: 快速开始指南
├── QWEN_ASR_集成说明.md            # 新增: 本文档
└── docs/
    └── QWEN_ASR_USAGE.md           # 新增: 完整使用文档
```

---

## 🎯 核心特性

### 1. 灵活切换
- 通过 `--asr-engine` 参数轻松切换
- 无需修改代码

### 2. 向后兼容
- 默认使用 Whisper
- 现有代码和脚本无需修改

### 3. 配置简单
- 只需在 `.env` 添加 `DASHSCOPE_API_KEY`
- 支持命令行参数覆盖

### 4. 错误容错
- 如果 dashscope 未安装,自动回退到 Whisper
- API 调用失败时有详细错误信息

---

## 💡 使用建议

### 场景1: 教学视频分析 (推荐 Whisper)
```bash
python3 video_analyzer_pro.py --video lecture.mp4 --asr-engine whisper
```
**原因**: 需要精确的时间戳来对应图片和文字

### 场景2: 快速文本提取 (推荐 Qwen ASR)
```bash
python3 video_analyzer_pro.py --video interview.mp4 --asr-engine qwen
```
**原因**: 只需要完整文本,不需要时间对应

### 场景3: 批量处理 (根据资源选择)
- **本地资源充足**: Whisper (免费)
- **云端服务器**: Qwen ASR (速度快,低资源)

---

## 🔗 相关链接

- **阿里云模型工作室**: https://help.aliyun.com/zh/model-studio/
- **API Key 获取**: https://help.aliyun.com/zh/model-studio/get-api-key
- **Qwen ASR 文档**: https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-audio-models
- **Whisper 项目**: https://github.com/openai/whisper

---

## 🎉 总结

✅ **已完成**:
1. 创建了 `audio_qwen.py` 模块
2. 集成到 `video_analyzer_pro.py`
3. 支持命令行和代码两种调用方式
4. 完全向后兼容
5. 提供完整文档

✅ **可以立即使用**:
- 配置 API Key 后即可使用 Qwen ASR
- 未配置则继续使用 Whisper (默认)

✅ **灵活可扩展**:
- 易于切换引擎
- 保留添加其他 ASR 引擎的可能性

---

**祝使用愉快！** 🚀
