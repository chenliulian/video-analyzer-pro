# 视频分析器 Pro 版 🚀

> 智能视频关键帧提取 + OCR识别 + LLM文字精炼 + 人声过滤 + PDF生成

## ✨ 功能特性

### 核心功能
- ✅ **智能关键帧提取**：自动识别场景变化，去重保留重要画面
- ✅ **OCR文字识别**：识别课件/PPT中的文字内容（中文优化）
- ✅ **语音转文字**：Whisper高精度语音识别
- ✅ **人声过滤**：自动过滤音乐和噪音，只识别人声 ⭐ NEW
- ✅ **LLM智能精炼**：结合OCR和语音，自动纠错和段落整理
- ✅ **高质量PDF生成**：图片+精炼文字，专业排版

### 版本对比

| 功能 | 标准版 | Pro版 v4.1 | Pro版 v4.2 |
|------|--------|------------|------------|
| 关键帧提取 | ✅ | ✅ | ✅ |
| 语音转文字 | ✅ | ✅ | ✅ |
| 文字页生成 | ✅ | ✅ | ✅ |
| OCR识别 | ❌ | ✅ | ✅ |
| 中文OCR优化 | ❌ | ⚠️ | ✅ |
| 智能纠错 | ❌ | ✅ | ✅ |
| 段落整理 | ❌ | ✅ | ✅ |
| Markdown格式 | ❌ | ✅ | ✅ |
| **人声过滤** | ❌ | ❌ | ✅ ⭐ |
| **音乐去除** | ❌ | ❌ | ✅ ⭐ |
| **VAD检测** | ❌ | ❌ | ✅ ⭐ |

## 🎯 使用场景

- 📚 **在线课程记录**：自动提取课件+讲解整理
- 🎓 **学术讲座归档**：快速生成讲座笔记
- 💼 **会议记录**：PPT展示+讨论内容整理
- 🎬 **培训视频处理**：教学内容结构化提取

## 🚀 快速开始

### 1. 安装依赖

```bash
# 运行自动安装脚本
./setup_pro.sh

# 或手动安装
pip3 install -r requirements.txt
```

### 2. 配置LLM API（可选，使用智能精炼功能时必需）

**推荐方式：使用 .env 文件**

```bash
# 1. 复制配置模板
cp .env.example .env

# 2. 编辑 .env 文件，填入你的API配置
nano .env
```

`.env` 文件示例：
```env
# DeepSeek（推荐，性价比最高）
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

**或使用环境变量：**

```bash
# DeepSeek
export LLM_API_KEY="your-deepseek-api-key"
export LLM_BASE_URL="https://api.deepseek.com"
export LLM_MODEL="deepseek-chat"

# 智谱AI GLM-4
export LLM_API_KEY="your-zhipu-api-key"
export LLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export LLM_MODEL="glm-4"

# OpenAI GPT-4
export LLM_API_KEY="your-openai-api-key"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4"
```

### 3. 运行处理

```bash
# 完整流程（OCR + LLM）
python3 video_analyzer_pro.py --video your_video.mp4

# 仅OCR（不使用LLM）
python3 video_analyzer_pro.py --video your_video.mp4 --no-llm
```

## 📊 处理流程

```
视频文件 (MP4)
    ↓
提取关键帧 (智能去重)
    ↓
OCR识别课件文字
    ↓
语音转文字 (Whisper)
    ↓
LLM精炼整理 (纠错+段落化)
    ↓
生成PDF (图片+文字)
```

## 📁 输出文件

```
project/
├── your_video_frames_pro.pdf    # 最终PDF
├── your_video_ocr.txt           # OCR结果
├── your_video_refined.json      # 精炼后的文字
├── your_video_transcript.txt    # 原始转录
└── extracted_frames/            # 关键帧图片
    ├── frame_0000_0.00s.jpg
    ├── frame_0001_5.00s.jpg
    └── ...
```

## 💡 效果展示

### 原始转录（v3.0）
```
今天我们要学习的科目端de过的拜歌在閱读文章之前我们先一起来回顾以下词语的读音...
```
❌ 识别错误
❌ 缺乏结构
❌ 难以阅读

### Pro版精炼（v4.0）
```markdown
# 我的白鸽
## 作者：陈忠实

### 课文导读
今天我们要学习陈忠实的散文《我的白鸽》。

在阅读文章之前，我们先一起来回顾以下词语的读音：
- 借义
- 土批
- 烹然
...
```
✅ 自动纠错
✅ 层次分明
✅ 易于阅读

## 🔧 高级配置

### 自定义关键帧提取参数

编辑 `video_analyzer_pro.py`:

```python
image_files = extract_key_frames(
    video_file,
    frames_dir,
    check_interval=1.0,       # 检查间隔（秒）
    scene_threshold=30,       # 场景变化阈值
    min_interval=5.0,         # 最小保存间隔
    similarity_threshold=8,   # 相似度门槛
    max_skip_time=60,         # 强制检查时间
    force_save_threshold=3    # 强制保存阈值
)
```

### 切换OCR引擎

编辑 `ocr_module.py`:

```python
# 使用PaddleOCR（推荐）
ocr = OCRRecognizer(engine="paddleocr")

# 或使用Tesseract
ocr = OCRRecognizer(engine="tesseract")
```

### 调整LLM参数

编辑 `llm_agent.py`:

```python
response = self.client.chat.completions.create(
    model=self.model,
    temperature=0.3,    # 0-1，越低越保守
    max_tokens=2000     # 最大输出长度
)
```

## 💰 成本估算

以20分钟视频为例（134帧）：

### 使用DeepSeek
- Token消耗：~200K tokens
- 价格：¥1/百万tokens
- **总成本：¥0.2**

### 使用GPT-4
- Token消耗：~200K tokens
- 价格：$30/百万tokens
- **总成本：$6**

💡 **推荐**：日常使用DeepSeek，追求极致质量用GPT-4

## 📚 文档

- [完整使用指南](PRO_VERSION_GUIDE.md) - 详细的安装、配置和使用说明
- [文字布局优化](TEXT_LAYOUT_V3.md) - v3.0文字页布局优化说明
- [文字集成功能](TEXT_INTEGRATION_GUIDE.md) - 文字页功能演进历史

## 🐛 故障排除

### OCR识别失败
```bash
# 检查PaddleOCR安装
python3 -c "from paddleocr import PaddleOCR; print('OK')"

# 或切换到Tesseract
brew install tesseract tesseract-lang
```

### LLM调用失败
```bash
# 检查 .env 文件配置
cat .env

# 或检查环境变量
echo $LLM_API_KEY
echo $LLM_BASE_URL
echo $LLM_MODEL

# 测试API连接
python3 llm_agent.py
```

### 依赖版本冲突
```bash
# 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📝 更新日志

### v4.0 Pro (2025-12-06)
- ✨ 新增OCR识别模块（PaddleOCR）
- ✨ 新增LLM Agent模块（智能纠错+段落整理）
- ✨ 集成OCR和LLM到完整流程
- 📚 完善文档和使用指南

### v3.0 (2025-12-06)
- 🎨 双列文字布局
- 📝 时间范围合并显示
- ✅ 100%文字显示完整

### v2.0 (2025-12-06)
- 🎯 文字页紧跟图片
- 📏 尺寸自适应匹配
- ⏱️ 精确时间段匹配

### v1.0 (2025-12-05)
- 🎬 智能关键帧提取
- 🎤 语音转文字
- 📄 PDF生成

## 📄 许可证

MIT License

---

**作者**: AI Assistant  
**版本**: v4.0 Pro  
**更新**: 2025-12-06
