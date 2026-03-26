# 视频分析器Pro版 使用说明

## 概述

`video_analyzer_pro.py` 是针对教育讲课视频的**一站式自动化处理脚本**,完整流程包括:

1. **提取视频关键帧** - 智能识别关键帧,自动去重
2. **提取音频数据** - 自动从视频提取音频
3. **OCR识别文字** - 使用通义千问识别课件文字
4. **语音转文字** - 使用Whisper自动转录
5. **LLM精炼整合** - 结合OCR和转录,智能整理(可选)
6. **生成PDF文档** - 图片+文字交替排列,完整记录

## 🎉 最新更新 (2025-12-07 v3.0)

## 🎉 最新更新 (2025-12-07 v3.0)

### 重大改进 🚀

1. **完全自动化流程**
   - ✅ 集成音频提取 - 无需手动提取音频
   - ✅ 集成语音转录 - 自动调用Whisper进行转录
   - ✅ 一键完成所有步骤 - 从视频到PDF全自动

2. **智能断点续传**
   - ✅ 自动检测已完成的步骤
   - ✅ 跳过已存在的文件,节省时间
   - ✅ 支持强制重新处理(`--no-skip`)

3. **通义千问OCR**
   - ✅ 更准确的中文识别
   - ✅ 支持复杂场景和手写体
   - ✅ 多模型选择

4. **增强的用户体验**
   - ✅ 详细的进度显示
   - ✅ 完整的处理统计
   - ✅ 更好的错误提示
   - ✅ 彩色输出界面

5. **结果文件管理**
   - ✅ 统一保存到 `results/` 目录
   - ✅ 清晰的文件组织结构
   - ✅ 自动创建必要目录

## 环境配置

### 1. API密钥配置

在项目根目录的 `.env` 文件中配置:

```bash
# 通义千问OCR API密钥 (必需)
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx

# LLM API密钥 (可选,用于文字精炼)
LLM_API_KEY=your-openai-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
```

### 2. 获取通义千问API密钥

访问: https://help.aliyun.com/zh/model-studio/get-api-key

## 使用方法

### 🚀 快速开始(一键处理)

```bash
# 最简单的用法 - 只需指定视频文件!
python3 video_analyzer_pro.py --video your_lecture.mp4

# 脚本会自动完成:
# ✓ 提取关键帧
# ✓ 提取音频
# ✓ 语音转文字
# ✓ OCR识别
# ✓ LLM精炼(如果配置)
# ✓ 生成PDF
```

### 常用命令

```bash
# 使用小型Whisper模型(更快)
python3 video_analyzer_pro.py --video lecture.mp4 --whisper-model small

# 不使用LLM精炼(仅OCR和转录)
python3 video_analyzer_pro.py --video lecture.mp4 --no-llm

# 强制重新处理所有步骤
python3 video_analyzer_pro.py --video lecture.mp4 --no-skip

# 指定OCR模型
python3 video_analyzer_pro.py --video lecture.mp4 --ocr-model qwen-vl-plus
```

### 完整参数示例

```bash
python3 video_analyzer_pro.py \
  --video lecture.mp4 \
  --whisper-model base \
  --ocr-model qwen-vl-max \
  --ocr-api-key sk-xxxxx \
  --api-key your-openai-key \
  --model gpt-4 \
  --no-skip
```

### 命令行参数说明

| 参数 | 说明 | 默认值 | 必需 |
|------|------|--------|------|
| `--video` | 视频文件路径 | 无 | ✅ 是 |
| `--whisper-model` | Whisper模型大小 | `base` | 否 |
| `--ocr-model` | OCR模型 | `qwen-vl-max` | 否 |
| `--ocr-api-key` | 通义千问API密钥 | 环境变量 | 否 |
| `--api-key` | LLM API密钥 | 环境变量 | 否 |
| `--base-url` | LLM API地址 | 环境变量 | 否 |
| `--model` | LLM模型名称 | `gpt-4` | 否 |
| `--no-llm` | 禁用LLM精炼 | False | 否 |
| `--no-skip` | 不跳过已存在文件 | False | 否 |

#### Whisper模型选择

| 模型 | 大小 | 速度 | 准确度 | 推荐场景 |
|------|------|------|--------|----------|
| `tiny` | ~1GB | 最快 | 一般 | 快速测试 |
| `base` | ~1GB | 快 | 良好 | **推荐默认** |
| `small` | ~2GB | 中等 | 很好 | 平衡选择 |
| `medium` | ~5GB | 慢 | 优秀 | 高质量需求 |
| `large` | ~10GB | 最慢 | 最佳 | 专业场景 |

## OCR模型选择

通义千问提供三种OCR模型:

1. **qwen-vl-max** (推荐)
   - 最强识别能力
   - 适合复杂场景、手写体、模糊图片
   - 成本较高

2. **qwen-vl-plus**
   - 平衡性能和成本
   - 适合大多数常规场景

3. **qwen3-vl-plus**
   - 最新版本
   - 优化的性能和识别准确度

## 输出文件

所有输出文件保存在 `results/` 目录:

```
results/
├── extracted_frames/           # 提取的关键帧图片
│   ├── frame_0000_0.00s.jpg
│   ├── frame_0001_5.50s.jpg
│   └── ...
├── {video_id}_transcript.txt   # 语音转录文本
├── {video_id}_ocr_qwen.txt    # OCR识别结果
├── {video_id}_refined.json    # LLM精炼结果
└── {video_id}_frames_pro.pdf  # 最终生成的PDF
```

## 处理流程详解

### 完整6步流程

#### 步骤1: 提取视频关键帧 🖼️
- 智能场景检测算法
- 自动去除重复帧
- 保留关键教学画面
- 输出: `results/extracted_frames/*.jpg`

**特点:**
- 场景变化阈值: 30
- 最小间隔: 5秒
- 相似度过滤: 智能去重

#### 步骤2: 提取音频数据 🎵
- 自动从视频提取音频
- 转换为MP3格式
- 输出: `results/{video_id}.mp3`

**断点续传:** 如果音频文件已存在,自动跳过此步骤

#### 步骤3: 语音转文字 🎤
- 使用OpenAI Whisper模型
- 支持中文识别
- 生成分段时间戳
- 输出: `results/{video_id}_transcript.txt`

**特点:**
- 自动加载模型
- 支持多种模型大小
- 生成时间戳对齐

#### 步骤4: OCR识别课件文字 🔍
- 使用通义千问多模态API
- 识别每帧图片中的文字
- 支持复杂场景和手写体
- 输出: `results/{video_id}_ocr_qwen.txt`

**优势:**
- 高准确度中文识别
- 保持文本结构
- 批量处理优化

#### 步骤5: LLM精炼整合 🤖 (可选)
- 结合OCR和语音转录
- 纠正识别错误
- 整理成结构化内容
- 输出: `results/{video_id}_refined.json`

**功能:**
- 智能纠错
- 内容整理
- Markdown格式

#### 步骤6: 生成PDF文档 📄
- 图片页 + 文字页交替排列
- 时间戳标注
- 支持Markdown格式
- 输出: `results/{video_id}_frames_pro.pdf`

**布局:**
```
[图片页] 课件截图
[文字页] 对应讲解文字 + 时间段
[图片页] 下一张课件
[文字页] 对应讲解文字 + 时间段
...
```

## 常见问题

### Q: 必须要配置API密钥吗?

**A:** 取决于你的需求:
- **必需**: `DASHSCOPE_API_KEY` (用于OCR识别)
- **可选**: `LLM_API_KEY` (用于文字精炼,可用 `--no-llm` 跳过)

### Q: 可以只处理部分步骤吗?

**A:** 可以!利用断点续传功能:
1. 运行一次后,已完成的步骤会自动跳过
2. 删除特定结果文件,可重新处理该步骤
3. 使用 `--no-skip` 强制重新处理所有步骤

### Q: 语音转录需要很长时间吗?

**A:** 时间取决于:
- 视频长度
- Whisper模型大小
- CPU/GPU性能

**建议:**
- 10分钟视频 + base模型 ≈ 2-5分钟
- 使用 `--whisper-model small` 可加快速度
- 首次运行需下载模型(~1-2GB)

### Q: OCR识别失败怎么办?

**A:** 检查以下事项:
1. ✅ 确认 `DASHSCOPE_API_KEY` 已正确配置
2. ✅ 检查API密钥是否有效
3. ✅ 确认网络连接正常
4. ✅ 查看是否有API配额限制
5. ✅ 尝试切换到 `--ocr-model qwen-vl-plus` (成本更低)

### Q: 生成的PDF太大怎么办?

**A:** 优化建议:
- 帧数较多时PDF会较大
- 可以调整 `extract_frames_to_pdf.py` 中的图片分辨率
- 使用PDF压缩工具进一步压缩

### Q: 断点续传如何工作?

**A:** 脚本会检查以下文件是否存在:
- `results/extracted_frames/` - 跳过帧提取
- `results/{video_id}.mp3` - 跳过音频提取
- `results/{video_id}_transcript.txt` - 跳过语音转录
- `results/{video_id}_ocr_qwen.txt` - 跳过OCR识别
- `results/{video_id}_refined.json` - 跳过LLM精炼

**强制重新处理:** 使用 `--no-skip` 参数

### Q: 如何选择合适的Whisper模型?

**A:** 根据需求选择:
| 需求 | 推荐模型 | 理由 |
|------|----------|------|
| 快速测试 | `tiny` | 最快,准确度够用 |
| 日常使用 | `base` | **推荐**,平衡速度和质量 |
| 高质量 | `small`/`medium` | 更准确,稍慢 |
| 专业用途 | `large` | 最佳质量,需要好硬件 |

## 性能优化建议

### 1. 硬件配置

**推荐配置:**
- CPU: 4核以上
- 内存: 8GB以上
- 硬盘: 预留视频大小的3-5倍空间
- GPU: 可选,但能加速Whisper转录

### 2. 参数优化

```bash
# 快速模式 - 牺牲少量质量,大幅提升速度
python3 video_analyzer_pro.py \
  --video lecture.mp4 \
  --whisper-model tiny \
  --ocr-model qwen-vl-plus \
  --no-llm

# 高质量模式 - 最佳效果
python3 video_analyzer_pro.py \
  --video lecture.mp4 \
  --whisper-model medium \
  --ocr-model qwen-vl-max
```

### 3. 成本控制

**API调用成本:**
- OCR: 每张图片约 ¥0.01-0.05 (取决于模型)
- LLM: 每次精炼约 ¥0.1-0.5 (取决于模型和长度)

**节省成本的方法:**
1. 使用 `--no-llm` 跳过LLM精炼
2. 选择 `qwen-vl-plus` 而不是 `qwen-vl-max`
3. 减少提取的关键帧数量

### 4. 批量处理优化

```bash
# 使用 GNU Parallel 并行处理多个视频
ls *.mp4 | parallel -j 2 \
  'python3 video_analyzer_pro.py --video {} --no-llm'

# -j 2 表示同时处理2个视频
```

### 5. 处理时间估算

| 视频长度 | Whisper模型 | 预计时间 | 说明 |
|----------|-------------|----------|------|
| 10分钟 | tiny | 3-5分钟 | 快速 |
| 10分钟 | base | 5-8分钟 | 推荐 |
| 10分钟 | small | 8-12分钟 | 平衡 |
| 30分钟 | base | 15-25分钟 | 常规 |
| 60分钟 | base | 30-50分钟 | 长视频 |

*注: 时间包含所有步骤,实际时间受硬件影响*

## 示例工作流

### 场景1: 完整自动化处理

```bash
# 一键处理整个视频
python3 video_analyzer_pro.py --video lecture.mp4

# 输出:
# ✓ 提取 45 个关键帧
# ✓ 提取音频 (20.5 MB)
# ✓ 语音转录 (128 个段落)
# ✓ OCR识别 (42/45 成功)
# ✓ LLM精炼完成
# ✓ 生成PDF (90页, 15.2 MB)
```

### 场景2: 快速处理(不使用LLM)

```bash
# 跳过LLM精炼,加快处理速度
python3 video_analyzer_pro.py \
  --video lecture.mp4 \
  --whisper-model small \
  --no-llm

# 处理时间: ~10分钟 (原本可能需要30分钟)
```

### 场景3: 断点续传

```bash
# 第一次运行 - 处理到步骤3后中断
python3 video_analyzer_pro.py --video lecture.mp4
# Ctrl+C 中断

# 第二次运行 - 自动从步骤4继续
python3 video_analyzer_pro.py --video lecture.mp4
# ✓ 发现已提取的帧: 45 张 (跳过)
# ✓ 发现已提取的音频 (跳过)
# ✓ 发现已有转录文件 (跳过)
# ⏳ 正在识别 45 张图片... (继续)
```

### 场景4: 重新处理特定步骤

```bash
# 删除OCR结果,重新识别
rm results/*_ocr_qwen.txt

# 再次运行,只重新做OCR
python3 video_analyzer_pro.py --video lecture.mp4
```

### 场景5: 批量处理多个视频

```bash
# 创建批处理脚本
cat > process_all.sh << 'EOF'
#!/bin/bash
for video in *.mp4; do
    echo "处理: $video"
    python3 video_analyzer_pro.py --video "$video" --no-llm
done
EOF

chmod +x process_all.sh
./process_all.sh
```

## 技术支持

遇到问题请检查:
1. 所有依赖包是否已安装 (`requirements.txt`)
2. API密钥是否正确配置
3. 视频文件路径是否正确
4. 查看终端输出的详细错误信息

## 更新日志

### v3.0 (2025-12-07) - 完全自动化版本 🚀
- ✨ **新功能**: 集成音频提取,无需手动操作
- ✨ **新功能**: 集成语音转录(Whisper),一键完成
- ✨ **新功能**: 智能断点续传,自动跳过已完成步骤
- ✨ **新功能**: 详细的进度显示和处理统计
- ✨ **新功能**: 完整的错误处理和恢复机制
- 🎨 **改进**: 全新的命令行界面,更直观
- 🎨 **改进**: 彩色输出,清晰的步骤标识
- 📝 **改进**: 更详细的日志和提示信息
- 🐛 **修复**: 多个稳定性问题
- 📚 **文档**: 全面更新使用文档

### v2.0 (2025-12-07) - OCR升级版本
- ✨ 升级到通义千问OCR
- 📁 结果文件自动保存到 `results/` 目录
- ⚙️ 增强配置管理
- 📊 改进识别统计信息

### v1.0 - 初始版本
- 基础功能实现
- PaddleOCR支持
- LLM文字精炼
