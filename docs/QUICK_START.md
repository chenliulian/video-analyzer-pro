# 快速开始指南

## 🎯 5分钟快速上手

### 第一步：安装依赖

```bash
# 安装基础依赖
pip3 install -r requirements.txt
```

### 第二步：配置LLM API（使用Pro版智能精炼功能时需要）

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件（使用你喜欢的编辑器）
nano .env
```

在 `.env` 文件中填入你的API配置（以DeepSeek为例）：

```env
LLM_API_KEY=sk-your-api-key-here
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

> 💡 **没有API密钥？** 访问 [CONFIG_GUIDE.md](CONFIG_GUIDE.md) 查看如何获取

### 第三步：测试配置

```bash
# 测试配置是否正确
python3 tests/test_env_config.py
```

预期输出：
```
======================================================================
测试 .env 配置加载
======================================================================

1. 尝试加载 .env 文件...
   ✓ .env 文件存在
   ✓ .env 文件已加载

2. 检查配置项...
   ✓ LLM_API_KEY: sk-xxxxxxxx...
   ✓ LLM_BASE_URL: https://api.deepseek.com
   ✓ LLM_MODEL: deepseek-chat

3. 测试LLM Agent初始化...
   ✓ LLM Agent初始化成功
   ✓ 使用模型: deepseek-chat
   ✓ API地址: https://api.deepseek.com

======================================================================
✅ 配置测试通过！可以正常使用Pro版功能
======================================================================
```

### 第四步：运行视频分析

#### 选项A：完整流程（OCR + LLM智能精炼）

```bash
python3 video_analyzer_pro.py --video your_video.mp4
```

#### 选项B：仅OCR识别（不使用LLM）

```bash
python3 video_analyzer_pro.py --video your_video.mp4 --no-llm
```

#### 选项C：使用标准版（无OCR，无LLM）

```bash
python3 video_analyzer.py your_video.mp4
```

### 第五步：查看结果

```bash
# 生成的文件
ls -lh *_frames*.pdf        # PDF文件
ls -lh *_ocr.txt           # OCR识别结果
ls -lh *_refined.json      # LLM精炼结果
ls -lh extracted_frames/   # 提取的关键帧
```

## 📊 版本选择建议

| 版本 | 适用场景 | 成本 | 效果 |
|------|----------|------|------|
| **标准版** | 简单记录，不需要文字优化 | 免费 | ⭐⭐⭐ |
| **Pro版 (no-llm)** | 需要识别课件文字 | 免费 | ⭐⭐⭐⭐ |
| **Pro版 (完整)** | 需要智能纠错和段落整理 | ~¥0.2/20分钟 | ⭐⭐⭐⭐⭐ |

## 🔧 常见问题

### Q: 提示 "未设置API密钥"

**解决：**
```bash
# 1. 检查 .env 文件是否存在
ls -la .env

# 2. 如果不存在，创建它
cp .env.example .env

# 3. 编辑并填入你的API密钥
nano .env
```

### Q: 想要不使用LLM

**解决：** 添加 `--no-llm` 参数
```bash
python3 video_analyzer_pro.py --video test.mp4 --no-llm
```

### Q: 想要临时使用不同的API配置

**解决：** 使用命令行参数覆盖
```bash
python3 video_analyzer_pro.py \
  --video test.mp4 \
  --api-key "sk-different-key" \
  --model "gpt-4"
```

### Q: 如何获取API密钥？

**解决：** 查看详细教程
```bash
# 查看配置指南（推荐）
cat CONFIG_GUIDE.md

# 或访问服务商官网
# DeepSeek: https://platform.deepseek.com/
# 智谱AI: https://open.bigmodel.cn/
# OpenAI: https://platform.openai.com/
```

## 📚 进阶阅读

- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - 详细的配置指南
- [README_PRO.md](README_PRO.md) - Pro版功能介绍
- [PRO_VERSION_GUIDE.md](PRO_VERSION_GUIDE.md) - 完整使用指南

## 💬 需要帮助？

1. 查看配置指南：[CONFIG_GUIDE.md](CONFIG_GUIDE.md)
2. 查看故障排除：[README_PRO.md](README_PRO.md) 中的"🐛 故障排除"部分
3. 提交Issue到项目仓库

---

**最后更新：** 2025-12-06
