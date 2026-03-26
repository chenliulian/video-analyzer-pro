# LLM API 配置指南

本文档详细说明如何配置和使用大语言模型API。

## 📋 配置方式优先级

当多个配置方式同时存在时，优先级如下：

1. **命令行参数** > 2. **环境变量** > 3. **.env 文件**

## 方式一：使用 .env 文件（推荐 ⭐）

### 为什么推荐？
- ✅ 配置持久化，不需要每次设置环境变量
- ✅ 配置集中管理，清晰明了
- ✅ 自动加载，使用便捷
- ✅ 不会被提交到Git仓库，安全可靠

### 操作步骤

**1. 复制配置模板**
```bash
cp .env.example .env
```

**2. 编辑 .env 文件**

选择你使用的服务商，取消对应配置的注释（删除行首的 `#`），并填入真实的API密钥。

#### DeepSeek 配置（推荐 ⭐）

```env
LLM_API_KEY=sk-your-actual-api-key-here
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

**获取API密钥：**
1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 进入"API Keys"页面
4. 创建新的API密钥
5. 复制密钥（格式：`sk-xxxxxxxxxxxxxxxx`）

**特点：**
- 💰 价格最低：¥1/百万tokens（GPT-4的1/180）
- 🚀 速度快：国内访问无需代理
- 🎯 中文优化：识别准确率高
- 💡 适合场景：日常使用、批量处理、成本敏感项目

#### 智谱AI GLM-4 配置

```env
LLM_API_KEY=your-zhipu-api-key.your-api-secret
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
LLM_MODEL=glm-4
```

**获取API密钥：**
1. 访问 https://open.bigmodel.cn/
2. 注册/登录账号
3. 进入"API Keys"页面
4. 创建新密钥
5. 复制完整的密钥（格式：`xxxxxxxx.xxxxxxxx`）

**特点：**
- 🇨🇳 国产模型：清华智谱出品
- 💰 价格适中：¥100/百万tokens
- 📚 中文理解好：适合中文内容处理
- 💡 适合场景：企业使用、国产化要求

#### OpenAI GPT-4 配置

```env
LLM_API_KEY=sk-your-openai-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
```

**获取API密钥：**
1. 访问 https://platform.openai.com/
2. 注册/登录账号（需要海外手机号）
3. 进入"API Keys"页面
4. 创建新密钥
5. 复制密钥（格式：`sk-xxxxxxxxxxxxxxxx`）

**特点：**
- 🏆 效果最好：理解能力和输出质量最优
- 💎 高级功能：支持最新特性
- 💰 价格最高：$30/百万tokens
- 🌍 需要代理：国内访问需要VPN
- 💡 适合场景：追求最佳效果、预算充足

**3. 验证配置**

```bash
# 测试 LLM Agent
python3 llm_agent.py

# 预期输出：
# ✓ LLM Agent初始化成功
#   模型: deepseek-chat
#   API地址: https://api.deepseek.com
```

**4. 使用**

配置完成后，直接运行即可：

```bash
# 自动从 .env 文件加载配置
python3 video_analyzer_pro.py --video your_video.mp4
```

## 方式二：使用环境变量

### 适用场景
- 临时测试不同配置
- CI/CD环境
- Docker容器部署

### 操作步骤

**1. 设置环境变量**

```bash
# DeepSeek
export LLM_API_KEY="sk-xxxxxxxxxxxxxxxx"
export LLM_BASE_URL="https://api.deepseek.com"
export LLM_MODEL="deepseek-chat"
```

**2. 验证设置**

```bash
echo $LLM_API_KEY
echo $LLM_BASE_URL
echo $LLM_MODEL
```

**3. 使用**

```bash
python3 video_analyzer_pro.py --video your_video.mp4
```

**注意：** 环境变量仅在当前终端会话有效，关闭终端后需要重新设置。

### 持久化环境变量（可选）

如果希望环境变量永久生效，可以添加到 shell 配置文件：

```bash
# bash 用户
echo 'export LLM_API_KEY="sk-xxxxxxxxxxxxxxxx"' >> ~/.bashrc
echo 'export LLM_BASE_URL="https://api.deepseek.com"' >> ~/.bashrc
echo 'export LLM_MODEL="deepseek-chat"' >> ~/.bashrc
source ~/.bashrc

# zsh 用户
echo 'export LLM_API_KEY="sk-xxxxxxxxxxxxxxxx"' >> ~/.zshrc
echo 'export LLM_BASE_URL="https://api.deepseek.com"' >> ~/.zshrc
echo 'export LLM_MODEL="deepseek-chat"' >> ~/.zshrc
source ~/.zshrc
```

## 方式三：使用命令行参数

### 适用场景
- 临时覆盖默认配置
- 脚本自动化
- 测试不同API

### 操作步骤

```bash
python3 video_analyzer_pro.py \
  --video your_video.mp4 \
  --api-key "sk-xxxxxxxxxxxxxxxx" \
  --base-url "https://api.deepseek.com" \
  --model "deepseek-chat"
```

### 查看所有参数

```bash
python3 video_analyzer_pro.py --help
```

## 🔒 安全建议

1. **不要提交 .env 文件到Git**
   ```bash
   # .env 已在 .gitignore 中，检查确认
   cat .gitignore | grep .env
   ```

2. **定期轮换API密钥**
   - 建议每3-6个月更换一次
   - 泄露后立即删除并重新生成

3. **限制API密钥权限**
   - 设置合理的使用额度
   - 启用IP白名单（如果支持）

4. **监控API使用量**
   - 定期检查服务商后台
   - 设置用量告警

## 🐛 常见问题

### Q1: 提示 "未设置API密钥"

**原因：** 配置未正确加载

**解决方案：**
```bash
# 1. 检查 .env 文件是否存在
ls -la .env

# 2. 检查 .env 文件内容
cat .env

# 3. 确认没有多余空格或换行
# 正确：LLM_API_KEY=sk-xxx
# 错误：LLM_API_KEY = sk-xxx（多了空格）

# 4. 确认安装了 python-dotenv
pip3 show python-dotenv
```

### Q2: 提示 "LLM调用出错"

**原因：** API密钥无效或网络问题

**解决方案：**
```bash
# 1. 验证API密钥（以DeepSeek为例）
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# 2. 检查网络连接
ping api.deepseek.com

# 3. 查看详细错误日志
python3 video_analyzer_pro.py --video test.mp4 2>&1 | tee debug.log
```

### Q3: 配置了但没有生效

**原因：** 配置优先级问题

**解决方案：**
```bash
# 1. 清除所有环境变量
unset LLM_API_KEY
unset LLM_BASE_URL
unset LLM_MODEL

# 2. 只使用 .env 文件
python3 video_analyzer_pro.py --video test.mp4

# 3. 在代码中打印实际使用的配置
# 编辑 llm_agent.py，在 __init__ 后添加：
print(f"Using API Key: {self.api_key[:10]}...")
print(f"Using Base URL: {self.base_url}")
print(f"Using Model: {self.model}")
```

### Q4: python-dotenv 未安装

**解决方案：**
```bash
pip3 install python-dotenv

# 或重新安装所有依赖
pip3 install -r requirements.txt
```

## 📊 成本对比

以处理20分钟视频（约134帧）为例：

| 服务商 | Token消耗 | 单价 | 总成本 | 耗时 |
|--------|-----------|------|--------|------|
| DeepSeek | ~200K | ¥1/百万 | **¥0.2** | ~2分钟 |
| 智谱GLM-4 | ~200K | ¥100/百万 | ¥20 | ~3分钟 |
| OpenAI GPT-4 | ~200K | $30/百万 | $6 (~¥42) | ~5分钟 |

💡 **建议策略：**
- **日常使用**：DeepSeek（极致性价比）
- **企业项目**：智谱GLM-4（国产化+性能平衡）
- **追求极致**：OpenAI GPT-4（最佳效果）

## 📚 相关文档

- [README_PRO.md](README_PRO.md) - Pro版功能介绍
- [PRO_VERSION_GUIDE.md](PRO_VERSION_GUIDE.md) - 完整使用指南
- [.env.example](.env.example) - 配置文件模板

## 💬 技术支持

遇到问题？
1. 查看本文档的"常见问题"部分
2. 检查 [PRO_VERSION_GUIDE.md](PRO_VERSION_GUIDE.md) 中的"故障排除"
3. 提交 Issue 到项目仓库

---

**更新日期：** 2025-12-06  
**文档版本：** v1.0
