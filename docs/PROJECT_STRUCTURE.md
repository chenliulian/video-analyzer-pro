# 项目结构说明

> 最后更新：2025-12-06 (v4.1)

## 📁 目录结构

```
VedioAnalyzer/
├── 📝 配置文件
│   ├── .env                          # 本地配置（不提交到Git）⚠️
│   ├── .env.example                  # 配置模板
│   ├── .gitignore                    # Git忽略规则
│   ├── requirements.txt              # Python依赖
│   └── setup_pro.sh                  # 自动安装脚本
│
├── 🎬 核心功能模块
│   ├── video_analyzer.py             # 标准版（v1.0-v3.0）
│   ├── video_analyzer_pro.py         # Pro版主程序（v4.0+）
│   ├── extract_frames_to_pdf.py      # 关键帧提取+PDF生成
│   ├── extract_audio_to_text.py      # 音频转文字
│   ├── ocr_module.py                 # OCR识别模块
│   └── llm_agent.py                  # LLM智能精炼模块
│
├── 📚 文档
│   ├── README.md                     # 项目主README
│   ├── README_PRO.md                 # Pro版功能介绍
│   ├── QUICK_START.md                # 5分钟快速上手 ⭐
│   ├── CONFIG_GUIDE.md               # 配置详细指南 ⭐
│   ├── PRO_VERSION_GUIDE.md          # Pro版完整指南
│   ├── CHANGELOG.md                  # 更新日志
│   ├── PROJECT_STRUCTURE.md          # 本文件
│   ├── TEXT_INTEGRATION_GUIDE.md     # 文字集成功能文档
│   ├── TEXT_LAYOUT_V3.md             # v3.0布局优化文档
│   ├── OPTIMIZATION_REPORT.md        # 性能优化报告
│   └── FINAL_SUMMARY.md              # 项目总结
│
├── 🧪 测试文件（tests/）
│   ├── test_env_config.py            # 配置测试脚本 ⭐
│   ├── analyze_gap.py                # 时间间隔分析
│   ├── analyze_page_similarity.py    # 页面相似度分析
│   ├── check_*.py                    # 各种检查脚本
│   ├── debug_*.py                    # 调试脚本
│   ├── diagnose_*.py                 # 诊断脚本
│   ├── test_*.py                     # 测试脚本
│   ├── verify_*.py                   # 验证脚本
│   ├── output.log                    # 测试日志
│   ├── similarity_*.txt              # 相似度分析结果
│   └── temp_*.jpg                    # 临时测试图片
│
├── 📂 输出目录
│   ├── extracted_frames/             # 提取的关键帧图片
│   ├── *_frames.pdf                  # 生成的PDF（标准版）
│   ├── *_frames_pro.pdf              # 生成的PDF（Pro版）
│   ├── *_transcript.txt              # 语音转录文字
│   ├── *_ocr.txt                     # OCR识别结果
│   └── *_refined.json                # LLM精炼结果
│
└── 🎥 示例文件
    ├── 1732328440969754.mp4          # 示例视频
    ├── 1732328440969754.mp3          # 提取的音频
    ├── 1732328440969754_transcript.txt # 示例转录
    └── 1732328440969754_frames.pdf   # 示例PDF
```

## 📖 文件说明

### 核心模块

#### `video_analyzer.py` - 标准版分析器
- **功能**：基础的关键帧提取 + 语音转文字 + PDF生成
- **版本**：v1.0 - v3.0
- **适用场景**：简单记录，不需要智能优化
- **使用**：`python3 video_analyzer.py video.mp4`

#### `video_analyzer_pro.py` - Pro版分析器
- **功能**：完整流程（关键帧 + OCR + LLM精炼 + PDF）
- **版本**：v4.0+
- **适用场景**：需要高质量文字整理
- **使用**：`python3 video_analyzer_pro.py --video video.mp4`

#### `extract_frames_to_pdf.py` - 核心处理模块
- **功能**：
  - 智能关键帧提取（场景检测、相似度去重）
  - 语音转录解析
  - PDF生成（图片+文字页）
- **被调用**：`video_analyzer.py` 和 `video_analyzer_pro.py`

#### `ocr_module.py` - OCR识别模块
- **功能**：识别视频帧中的文字（课件、PPT等）
- **引擎**：PaddleOCR（主） / Tesseract（备）
- **输出**：每张图片的文字内容

#### `llm_agent.py` - LLM智能代理
- **功能**：
  - 结合OCR和语音转录
  - 自动纠错（如"拜歌" → "白鸽"）
  - 段落整理（层次分明）
  - Markdown格式输出
- **支持**：OpenAI API兼容服务（DeepSeek、智谱、GPT-4等）

### 配置文件

#### `.env` ⚠️ 重要
- **内容**：LLM API密钥和配置
- **安全**：已添加到`.gitignore`，不会被提交
- **创建**：`cp .env.example .env`
- **示例**：
  ```env
  LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
  LLM_BASE_URL=https://api.deepseek.com
  LLM_MODEL=deepseek-chat
  ```

#### `.env.example`
- **内容**：配置模板，包含所有支持的服务商示例
- **用途**：复制为`.env`后填入真实配置

#### `requirements.txt`
- **内容**：所有Python依赖包
- **安装**：`pip3 install -r requirements.txt`

### 文档导航

#### 新手必看 ⭐
1. **[QUICK_START.md](QUICK_START.md)** - 5分钟快速上手
2. **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - 详细配置教程（含API密钥获取）

#### Pro版用户
1. **[README_PRO.md](README_PRO.md)** - 功能概览
2. **[PRO_VERSION_GUIDE.md](PRO_VERSION_GUIDE.md)** - 完整使用指南

#### 开发者
1. **[CHANGELOG.md](CHANGELOG.md)** - 版本更新记录
2. **[TEXT_INTEGRATION_GUIDE.md](TEXT_INTEGRATION_GUIDE.md)** - 文字功能演进
3. **[OPTIMIZATION_REPORT.md](OPTIMIZATION_REPORT.md)** - 性能优化分析

### 测试工具

#### `tests/test_env_config.py` ⭐
- **功能**：测试`.env`配置是否正确
- **使用**：`python3 tests/test_env_config.py`
- **输出**：配置状态检查报告

#### 其他测试脚本
- `test_similarity.py` - 相似度算法测试
- `analyze_page_similarity.py` - 页面重复分析
- `check_*.py` - 各种检查工具
- `debug_*.py` - 调试工具

## 🚀 快速导航

### 我想...

#### 快速开始使用
👉 查看 **[QUICK_START.md](QUICK_START.md)**

#### 配置LLM API
👉 查看 **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)**

#### 了解Pro版功能
👉 查看 **[README_PRO.md](README_PRO.md)**

#### 解决配置问题
👉 运行 `python3 tests/test_env_config.py`  
👉 查看 **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)** 中的"常见问题"

#### 了解版本更新
👉 查看 **[CHANGELOG.md](CHANGELOG.md)**

#### 调整关键帧提取参数
👉 编辑 `extract_frames_to_pdf.py` 中的 `extract_key_frames()` 函数

#### 切换OCR引擎
👉 编辑 `ocr_module.py`，修改 `OCRRecognizer(engine="paddleocr")` 参数

## 📊 文件统计

```
总文件：    ~27个主文件 + 20个测试文件
代码文件：  ~10个 Python模块
文档文件：  ~12个 Markdown文档
配置文件：  4个
测试文件：  20个（已整理到tests/）
```

## 🔄 版本历史

| 版本 | 日期 | 主要更新 |
|------|------|----------|
| **v4.1** | 2025-12-06 | .env配置支持、文档完善、测试整理 |
| v4.0 | 2025-12-06 | OCR模块、LLM Agent、Pro版 |
| v3.0 | 2025-12-06 | 双列布局、文字显示优化 |
| v2.0 | 2025-12-06 | 文字页紧跟图片、精确匹配 |
| v1.0 | 2025-12-05 | 初始版本：关键帧提取、语音转文字 |

## 🔗 相关链接

- 主README: [README.md](README.md)
- Pro版README: [README_PRO.md](README_PRO.md)
- 快速开始: [QUICK_START.md](QUICK_START.md)
- 配置指南: [CONFIG_GUIDE.md](CONFIG_GUIDE.md)
- 更新日志: [CHANGELOG.md](CHANGELOG.md)

---

**维护者**: AI Assistant  
**版本**: v4.1  
**最后更新**: 2025-12-06
