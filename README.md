# VideoAnalyzer Pro - 智能视频分析工具

VideoAnalyzer Pro 是一个功能强大的视频内容分析工具，能够自动提取视频中的关键帧、音频转录、OCR文字识别，并通过大语言模型整合生成结构化的PDF和Word文档。

## 核心功能

- **智能关键帧提取**: 基于场景变化检测自动提取视频关键帧
- **语音识别转录**: 支持 Whisper 和 阿里云 Qwen ASR 双引擎
- **OCR文字识别**: 基于通义千问多模态API，精准识别课件文字
- **LLM智能精炼**: 整合语音转录和OCR结果，纠错并优化排版
- **文档生成**: 自动生成包含图片和文字的PDF和Word文档

## 项目结构

```
video-analyzer-pro/
├── src/
│   └── video_analyzer/           # 主包
│       ├── __init__.py
│       ├── core/                 # 核心模块
│       │   ├── __init__.py
│       │   └── analyzer.py       # 视频分析主流程
│       ├── ocr/                  # OCR模块
│       │   ├── __init__.py
│       │   └── qwen_ocr.py       # 通义千问OCR
│       ├── asr/                  # ASR模块
│       │   ├── __init__.py
│       │   └── qwen_asr.py       # Qwen语音识别
│       ├── llm/                  # LLM模块
│       │   ├── __init__.py
│       │   └── refine_agent.py   # 文本精炼Agent
│       └── utils/                # 工具模块
│           ├── __init__.py
│           ├── config.py         # 配置管理
│           └── file_utils.py     # 文件工具
├── tests/                        # 测试目录
│   ├── unit/                     # 单元测试
│   └── integration/              # 集成测试
├── examples/                     # 使用示例
│   ├── basic_usage.py            # 基础使用示例
│   └── api_usage.py              # API使用示例
├── docs/                         # 文档目录
├── data/                         # 视频文件存放目录
├── results/                      # 输出结果目录
├── config/                       # 配置文件
├── scripts/                      # 辅助脚本
├── main.py                       # 主入口文件
├── pyproject.toml                # 项目配置
├── setup.py                      # 安装脚本
├── Makefile                      # 常用命令
├── requirements.txt              # 依赖列表
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git忽略规则
└── README.md                     # 项目说明
```

## 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd video-analyzer-pro
```

### 2. 安装系统依赖

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install ffmpeg
```

### 3. 安装Python依赖

```bash
# 方式1: 使用 pip
pip install -e .

# 方式2: 使用 Makefile
make install

# 开发模式 (包含测试工具)
pip install -e ".[dev]"
# 或
make install-dev
```

### 4. 配置API密钥

复制环境变量示例文件并配置你的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥：

```env
# LLM 配置（用于文本精炼）
LLM_API_KEY=your-llm-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4

# OCR 配置（通义千问多模态）
DASHSCOPE_API_KEY=your-dashscope-api-key
QWEN_OCR_MODEL=qwen-vl-max
```

## 使用方法

### 方式1: 使用主入口 (推荐)

```bash
# 基础用法 - 使用Whisper进行语音识别
python main.py --video data/lecture.mp4

# 使用Qwen ASR（中文识别效果更好）
python main.py --video data/lecture.mp4 --asr-engine qwen

# 不使用LLM精炼（快速模式）
python main.py --video data/lecture.mp4 --no-llm

# 强制重新处理（不跳过已存在的文件）
python main.py --video data/lecture.mp4 --no-skip
```

### 方式2: 作为Python模块运行

```bash
python -m video_analyzer.core.analyzer --video data/lecture.mp4
```

### 方式3: 在代码中使用

```python
from video_analyzer import VideoAnalyzerPro

# 创建分析器
analyzer = VideoAnalyzerPro(
    video_file="data/lecture.mp4",
    use_llm=True,
    asr_engine="qwen"
)

# 运行完整流程
analyzer.run_full_pipeline()
```

更多示例请查看 [examples/](examples/) 目录。

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--video` | 视频文件路径（必填） | - |
| `--asr-engine` | 语音识别引擎：`whisper` 或 `qwen` | whisper |
| `--asr-api-key` | Qwen ASR API密钥 | 从.env读取 |
| `--asr-region` | Qwen ASR区域：`intl`(国际) 或 `cn`(国内) | intl |
| `--ocr-api-key` | 通义千问OCR API密钥 | 从.env读取 |
| `--ocr-model` | OCR模型：`qwen-vl-max`/`qwen-vl-plus`/`qwen3-vl-plus` | qwen-vl-max |
| `--api-key` | LLM API密钥 | 从.env读取 |
| `--base-url` | LLM API基础URL | 从.env读取 |
| `--model` | LLM模型名称 | 从.env读取 |
| `--whisper-model` | Whisper模型大小：`tiny`/`base`/`small`/`medium`/`large` | base |
| `--no-llm` | 禁用LLM精炼 | False |
| `--no-skip` | 不跳过已存在的文件 | False |

## 处理流程

```
视频输入
    ↓
[步骤1] 提取关键帧（场景变化检测）
    ↓
[步骤2] 提取音频
    ↓
[步骤3] 语音转文字（Whisper/Qwen ASR）
    ↓
[步骤4] OCR识别课件文字（通义千问）
    ↓
[步骤5] LLM精炼整合（纠错、排版优化）
    ↓
[步骤6] 生成PDF和Word文档
    ↓
输出结果
```

## 输出文件说明

| 文件类型 | 说明 |
|----------|------|
| `*_frames_pro.pdf` | 包含关键帧图片和精炼文字的PDF文档 |
| `*_frames_pro.docx` | Word格式文档，便于编辑 |
| `*_transcript.txt` | 语音转录的原始文本 |
| `*_ocr_qwen.txt` | OCR识别的课件文字 |
| `*_refined.json` | LLM精炼后的结构化数据 |
| `extracted_frames/*.jpg` | 提取的关键帧图片 |

## API密钥获取

### 1. 通义千问（DashScope）- 用于OCR和ASR

1. 访问 [阿里云百炼平台](https://help.aliyun.com/zh/model-studio/get-api-key)
2. 注册/登录阿里云账号
3. 创建API Key
4. 将Key填入 `.env` 文件的 `DASHSCOPE_API_KEY`

### 2. LLM API（可选）- 用于文本精炼

**DeepSeek（推荐，性价比高）:**
- 访问 [DeepSeek开放平台](https://platform.deepseek.com/)
- 注册并获取API Key

**OpenAI:**
- 访问 [OpenAI Platform](https://platform.openai.com/)
- 创建API Key

**智谱AI:**
- 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
- 注册并获取API Key

## 推荐配置

### 方案1：DeepSeek + 通义千问（性价比最高）

```env
LLM_API_KEY=sk-your-deepseek-key
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
DASHSCOPE_API_KEY=sk-your-dashscope-key
```

### 方案2：智谱AI + 通义千问（国内访问快）

```env
LLM_API_KEY=your-zhipu-key
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
LLM_MODEL=glm-4
DASHSCOPE_API_KEY=sk-your-dashscope-key
```

## 开发

### 常用命令

```bash
# 运行测试
make test

# 代码格式化
make format

# 代码检查
make lint

# 清理临时文件
make clean
```

### 项目结构说明

- `src/video_analyzer/core/` - 核心分析流程
- `src/video_analyzer/ocr/` - OCR文字识别
- `src/video_analyzer/asr/` - 语音识别
- `src/video_analyzer/llm/` - 大模型文本精炼
- `src/video_analyzer/utils/` - 工具函数
- `tests/` - 测试代码
- `examples/` - 使用示例

## 性能优化建议

1. **语音识别引擎选择**
   - 中文视频：推荐使用 `--asr-engine qwen`
   - 英文视频：Whisper效果也很好

2. **Whisper模型选择**
   - `tiny`: 最快，准确度较低
   - `base`: 平衡选择（默认）
   - `small`: 更准确，速度稍慢
   - `medium`/`large`: 最高准确度，较慢

3. **OCR模型选择**
   - `qwen-vl-max`: 最强识别能力（推荐）
   - `qwen-vl-plus`: 平衡性能和成本
   - `qwen3-vl-plus`: 最新版本

## 常见问题

### Q: 如何处理大视频文件？

A: Qwen ASR支持大文件自动切分，无需额外配置。对于超长视频，建议分段处理。

### Q: 为什么OCR识别效果不理想？

A: 请确保：
1. 视频画质清晰
2. 文字区域不要太小
3. 使用 `qwen-vl-max` 模型

### Q: LLM精炼失败怎么办？

A: 可以使用 `--no-llm` 参数跳过LLM精炼，系统会使用简单的合并策略。

### Q: 如何调整关键帧提取参数？

A: 编辑 `src/video_analyzer/core/analyzer.py` 中的 `_extract_key_frames` 方法：
- `scene_threshold`: 场景变化阈值（默认30）
- `min_interval`: 最小提取间隔秒数（默认5.0）

## 技术栈

- **视频处理**: MoviePy, OpenCV
- **语音识别**: OpenAI Whisper, 阿里云 Qwen ASR
- **OCR识别**: 通义千问多模态API
- **文本精炼**: OpenAI API兼容的各种大模型
- **文档生成**: ReportLab (PDF), python-docx (Word)

## 许可证

MIT License

## 更新日志

详见 [docs/CHANGELOG.md](docs/CHANGELOG.md)

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- 邮箱: support@videoanalyzer.com
- GitHub Issues: [提交问题](https://github.com/yourusername/video-analyzer-pro/issues)
