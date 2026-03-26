# 更新日志

## [v4.1] - 2025-12-06

### 新增功能
- ✨ 支持 `.env` 配置文件管理LLM API配置
- ✨ 新增配置优先级：命令行参数 > 环境变量 > .env文件
- 📝 新增详细的配置指南 `CONFIG_GUIDE.md`
- 📝 新增快速开始指南 `QUICK_START.md`
- 🧪 新增配置测试脚本 `tests/test_env_config.py`

### 改进
- 🔧 统一环境变量命名：`LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`
- 📦 更新依赖：新增 `python-dotenv>=1.0.0`
- 📁 创建 `.gitignore` 文件，保护敏感配置
- 📄 创建 `.env.example` 配置模板文件
- 🗂️ 移动所有测试文件到 `tests/` 文件夹（20个文件）

### 文档更新
- 📚 更新 `README_PRO.md` - 新增.env配置说明
- 📚 更新 `PRO_VERSION_GUIDE.md` - 详细的配置教程
- 📚 新增 `CONFIG_GUIDE.md` - 完整的配置指南（含获取API密钥教程）
- 📚 新增 `QUICK_START.md` - 5分钟快速上手指南

### 项目结构优化
```
VedioAnalyzer/
├── .env                          # [新增] 本地配置文件（不提交到Git）
├── .env.example                  # [新增] 配置模板
├── .gitignore                    # [新增] Git忽略规则
├── CONFIG_GUIDE.md              # [新增] 配置指南
├── QUICK_START.md               # [新增] 快速开始
├── CHANGELOG.md                 # [新增] 更新日志
├── tests/                       # [整理] 所有测试文件
│   ├── test_env_config.py      # [新增] 配置测试
│   ├── analyze_gap.py          # [移动] 
│   ├── test_similarity.py      # [移动]
│   └── ... (共20个测试文件)
├── llm_agent.py                 # [更新] 支持.env
├── video_analyzer_pro.py        # [更新] 支持.env
└── requirements.txt             # [更新] 新增python-dotenv
```

### 配置方式对比

#### 旧版（v4.0）
```bash
# 仅支持环境变量
export OPENAI_API_KEY="sk-xxx"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4"
```

#### 新版（v4.1）
```bash
# 方式1：.env文件（推荐）
cp .env.example .env
# 编辑.env文件即可

# 方式2：环境变量（兼容旧版）
export LLM_API_KEY="sk-xxx"

# 方式3：命令行参数
python3 video_analyzer_pro.py --api-key "sk-xxx"
```

### 向后兼容
- ✅ 完全兼容旧版环境变量（`OPENAI_API_KEY` 等）
- ✅ 支持新的环境变量命名（`LLM_API_KEY` 等）
- ✅ 自动优先使用新命名，回退到旧命名

### 安全性提升
- 🔒 `.env` 文件自动添加到 `.gitignore`
- 🔒 提供 `.env.example` 模板，不包含真实密钥
- 🔒 文档中强调API密钥安全管理

## [v4.0] - 2025-12-06

### 新增功能
- ✨ OCR识别模块（PaddleOCR）
- ✨ LLM Agent模块（智能纠错+段落整理）
- ✨ 完整Pro版流程集成

### 文档
- 📚 `PRO_VERSION_GUIDE.md` - Pro版使用指南
- 📚 `README_PRO.md` - Pro版README

## [v3.0] - 2025-12-06

### 改进
- 🎨 文字页双列布局
- 📝 时间范围合并显示
- ✅ 100%文字显示完整

### 文档
- 📚 `TEXT_LAYOUT_V3.md` - 布局优化文档

## [v2.0] - 2025-12-06

### 改进
- 🎯 文字页紧跟对应图片
- 📏 尺寸自适应匹配
- ⏱️ 精确时间段匹配

### 文档
- 📚 `TEXT_INTEGRATION_GUIDE.md` - 文字集成指南

## [v1.0] - 2025-12-05

### 初始版本
- 🎬 智能关键帧提取
- 🎤 语音转文字（Whisper）
- 📄 PDF生成

---

**维护者**: AI Assistant  
**项目**: VideoAnalyzer  
**仓库**: /Users/shmichenliulian/CodeBuddy/VedioAnalyzer
