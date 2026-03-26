# 快速开始指南 v5.0

## 🎯 两个问题,两个解决方案

### 问题1: 语音识别输出繁体字 ❌
**解决:** ✅ 自动转换为简体  
**无需配置,自动执行!**

### 问题2: 识别有错误,无标点,无段落 ❌
**解决:** ✅ LLM智能纠错+标点+分段  
**需要配置API,可选使用!**

---

## 🚀 方案一: 基础版(免费)

### 安装依赖
```bash
pip3 install opencc-python-reimplemented
```

### 运行命令
```bash
python3 video_analyzer_pro.py --video your_video.mp4 --no-llm
```

### 你会得到
✅ 简体中文转录  
❌ 无标点符号  
❌ 无段落结构  
❌ 有识别错误  

### 适用场景
- 快速预览
- 成本敏感
- 不要求高质量

---

## ⭐ 方案二: 完整版(推荐)

### 1. 安装依赖
```bash
pip3 install opencc-python-reimplemented openai python-dotenv
```

### 2. 配置API

创建 `.env` 文件(在项目根目录):
```bash
# LLM配置(用于纠错)
LLM_API_KEY=sk-xxxxxxxxxxxxx
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

# OCR配置(用于识别课件)
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxx
```

### 3. 运行命令
```bash
python3 video_analyzer_pro.py --video your_video.mp4
```

### 你会得到
✅ 简体中文转录  
✅ 准确的标点符号  
✅ 层次分明的段落  
✅ 纠正识别错误  

### 成本估算
- 10分钟视频: ~$0.10
- 30分钟视频: ~$0.30
- 60分钟视频: ~$0.60

### 适用场景
- 正式课程整理
- 需要高质量输出
- 有API预算

---

## 📋 效果对比

### 原始输出(繁体+无标点)
```
同學們好今天我們要學習的客文是過的白歌在閱讀文章之前我們先一起來回顧以下詞語的讀音
```

### 方案一输出(简体+无标点)
```
同学们好今天我们要学习的客文是过的白歌在阅读文章之前我们先一起来回顾以下词语的读音
```

### 方案二输出(简体+标点+纠错)
```
同学们好!今天我们要学习的课文是《我的白鸽》。

在阅读文章之前,我们先一起来回顾以下词语的读音。
```

---

## 🔍 如何选择?

| 需求 | 推荐方案 |
|------|---------|
| 快速测试 | 方案一 |
| 正式使用 | 方案二 |
| 预算有限 | 方案一 |
| 要求质量 | 方案二 |
| 内部使用 | 方案一 |
| 对外发布 | 方案二 |

---

## ⚙️ 常用命令

### 基础使用
```bash
# 简体转录(免费)
python3 video_analyzer_pro.py --video lecture.mp4 --no-llm

# 完整处理(需API)
python3 video_analyzer_pro.py --video lecture.mp4
```

### 自定义选项
```bash
# 使用小型Whisper模型(更快)
python3 video_analyzer_pro.py --video lecture.mp4 --whisper-model tiny

# 强制重新处理
python3 video_analyzer_pro.py --video lecture.mp4 --no-skip

# 指定OCR模型
python3 video_analyzer_pro.py --video lecture.mp4 --ocr-model qwen-vl-plus
```

---

## 🆘 遇到问题?

### 问题: "未安装 opencc"
```bash
pip3 install opencc-python-reimplemented
```

### 问题: "LLM未配置"
检查 `.env` 文件:
```bash
cat .env
```

确保包含:
```
LLM_API_KEY=sk-xxxxx
```

### 问题: "API调用失败"
1. 检查API余额
2. 检查网络连接
3. 检查API密钥是否正确

---

## 📚 更多信息

- 详细文档: `docs/TRADITIONAL_TO_SIMPLIFIED.md`
- 更新说明: `docs/V5_UPDATE_SUMMARY.md`
- PDF修复: `docs/PDF_TEXT_FIX.md`

---

## 🎉 开始使用!

```bash
# 1. 克隆或下载项目
cd /path/to/VedioAnalyzer

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 配置API(可选)
nano .env

# 4. 运行
python3 video_analyzer_pro.py --video your_video.mp4
```

就这么简单! 🚀
