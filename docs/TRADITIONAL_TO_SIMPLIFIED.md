# 繁简转换和LLM纠错功能说明

## 功能概述

基于用户反馈,我们新增了两个重要功能:

### 1. 繁简转换 (自动)
- Whisper语音识别默认输出繁体中文
- 现在会自动转换为简体中文
- 使用 `opencc-python-reimplemented` 库

### 2. LLM智能纠错和格式化 (可选)
- 结合OCR识别结果纠正语音识别错误
- 添加标准中文标点符号
- 智能分段,层次分明
- 保持原意,只纠正明显错误

## 技术实现

### 繁简转换

**使用库:** `opencc-python-reimplemented`

**安装:**
```bash
pip3 install opencc-python-reimplemented
```

**实现位置:** `video_analyzer_pro.py` - `_step3_audio_to_text()` 方法

**转换时机:** 在Whisper转录完成后立即转换

```python
from opencc import OpenCC
cc = OpenCC('t2s')  # 繁体到简体

# Whisper转录后
result = whisper_model.transcribe(audio_file, language="zh")

# 自动转换
full_text = cc.convert(result["text"])
for segment in result["segments"]:
    segment["text"] = cc.convert(segment["text"])
```

**效果对比:**

| 转换前(繁体) | 转换后(简体) |
|-------------|-------------|
| 同學們好 | 同学们好 |
| 學習 | 学习 |
| 課文 | 课文 |
| 閱讀 | 阅读 |
| 內容 | 内容 |

### LLM纠错和格式化

**使用模块:** `llm_agent.py` - `TextRefineAgent`

**配置方法:**

1. **创建 `.env` 文件** (在项目根目录):
```bash
# LLM配置 (必需,用于纠错)
LLM_API_KEY=sk-xxxxxxxxxxxxx
LLM_BASE_URL=https://api.openai.com/v1  # 可选
LLM_MODEL=gpt-4o-mini  # 可选,默认gpt-4

# OCR配置 (必需,用于参考)
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxx
```

2. **运行命令** (不加 `--no-llm`):
```bash
# 完整流程: 转录(繁转简) + OCR + LLM纠错
python3 video_analyzer_pro.py --video your_video.mp4
```

**LLM提示词设计:**

```
**任务要求：**
1. **纠错**: 结合OCR识别的课件文字纠正语音转录中的错误(特别是专业术语、人名、地名)
2. **标点**: 添加准确的中文标点符号(。,、;:?!)
3. **分段**: 将内容整理成层次分明、逻辑清晰的段落
4. **忠实原文**: 不要改变原意,不要添加额外内容,只纠正明显错误
5. **格式化**: 使用Markdown格式,必要时可使用项目列表或小标题
```

**输入示例:**

- **OCR识别课件:** "我的白鸽 —— 陈忠实"
- **语音转录:** "同学们好今天我们要学习的课文是过的白歌"

**LLM输出:**

```markdown
同学们好!今天我们要学习的课文是《我的白鸽》。

本文选自陈忠实文集,原题为《告别白鸽》。
```

## 使用场景

### 场景1: 只需繁简转换 (快速)

```bash
# 不使用LLM,只进行繁简转换
python3 video_analyzer_pro.py --video lecture.mp4 --no-llm

# 优点: 速度快,无API成本
# 缺点: 不纠错,不加标点,不分段
```

### 场景2: 完整处理 (高质量)

```bash
# 使用LLM进行纠错和格式化
python3 video_analyzer_pro.py --video lecture.mp4

# 优点: 文字质量高,格式规范
# 缺点: 需要API配置,有一定成本
```

## 处理流程对比

### 旧版流程
```
视频 → 提取音频 → Whisper转录(繁体) → 保存
```

### 新版流程(v5.0)
```
视频 → 提取音频 → Whisper转录(繁体) → 繁简转换(简体) → 保存

如果启用LLM:
→ OCR识别课件 → LLM纠错+标点+分段 → 保存精炼结果 → 生成PDF
```

## 效果展示

### 1. 繁简转换效果

**转录原文(繁体):**
```
《小貴子女生》同學們好今天我們要學習的客文是過的白歌在閱讀文章之前
我們先一起來回顧以下詞語的讀音同學們可以跟著一起讀讀寫寫
```

**转换后(简体):**
```
《小贵子女生》同学们好今天我们要学习的客文是过的白歌在阅读文章之前
我们先一起来回顾以下词语的读音同学们可以跟着一起读读写写
```

### 2. LLM纠错+格式化效果

**输入(简体无标点):**
```
同学们好今天我们要学习的客文是过的白歌在阅读文章之前我们先一起来
回顾以下词语的读音同学们可以跟着一起读读写写
```

**参考OCR:**
```
我的白鸽
——陈忠实
```

**LLM输出:**
```markdown
同学们好!今天我们要学习的课文是《我的白鸽》。

在阅读文章之前,我们先一起来回顾以下词语的读音。
同学们可以跟着一起读读写写。

**作者:** 陈忠实
```

## 配置检查

### 检查繁简转换是否启用

```bash
python3 -c "from opencc import OpenCC; print('繁简转换: 可用')"
```

如果报错,安装:
```bash
pip3 install opencc-python-reimplemented
```

### 检查LLM配置

```bash
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
if os.getenv('LLM_API_KEY'):
    print('LLM配置: 已设置')
else:
    print('LLM配置: 未设置 (将跳过纠错)')
"
```

## 成本估算

### 繁简转换
- **成本:** 免费
- **速度:** 即时
- **质量:** 准确

### LLM纠错 (以36帧视频为例)

假设使用 `gpt-4o-mini`:

| 项目 | 数量 | 单价 | 总成本 |
|------|------|------|--------|
| 输入token | ~500/帧 | $0.15/1M | ~$0.003 |
| 输出token | ~300/帧 | $0.6/1M | ~$0.006 |
| **总计** | 36帧 | - | **~$0.32** |

**省钱技巧:**
1. 使用 `--no-llm` 跳过纠错(免费)
2. 使用更便宜的模型(如 `gpt-3.5-turbo`)
3. 减少提取的关键帧数量

## 常见问题

### Q: 为什么Whisper输出是繁体?
A: Whisper的中文模型默认输出繁体,这是模型训练数据的特点。我们通过后处理自动转换为简体。

### Q: 可以只用繁简转换,不用LLM吗?
A: 可以!使用 `--no-llm` 参数即可。

### Q: LLM纠错会改变原意吗?
A: 不会。提示词明确要求"忠实原文,只纠正明显错误",并提供OCR作为参考。

### Q: 纠错效果如何?
A: 主要纠正:
- 专业术语错误 (如"白歌"→"白鸽")
- 标点符号缺失
- 段落结构混乱
- 不会改变说话内容和逻辑

### Q: 必须配置LLM API吗?
A: 不是必须的。不配置API时:
- ✅ 繁简转换仍然工作
- ✅ PDF仍然生成
- ❌ 不会进行纠错和格式化
- ❌ 直接使用原始转录

## 更新日志

### v5.0 (2025-12-07)
- ✨ **新增**: 繁简自动转换 (opencc)
- ✨ **新增**: LLM智能纠错和格式化
- ✨ **改进**: LLM提示词优化
- ✨ **改进**: 时间匹配算法 (区间重叠)
- 📝 **文档**: 新增使用说明

## 相关文件

- 主脚本: `video_analyzer_pro.py`
- LLM模块: `llm_agent.py`
- 配置文件: `.env` (需自己创建)
- 依赖列表: `requirements.txt`

## 技术支持

如有问题,请检查:
1. ✅ opencc 是否安装
2. ✅ .env 文件是否正确配置
3. ✅ API密钥是否有效
4. ✅ 网络连接是否正常
