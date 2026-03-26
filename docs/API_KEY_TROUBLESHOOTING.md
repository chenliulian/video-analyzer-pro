# API Key 问题排查和解决方案 🔧

## 🔍 当前问题

```
错误: InvalidApiKey - Invalid API-key provided.
API Key: sk-f35aed46f12a4f5fb9f023b70ab5e093
```

## 📊 诊断结果

✅ **格式正确** - API Key 格式符合标准（sk-开头）  
✅ **配置正确** - .env 文件配置无误  
❌ **认证失败** - API 服务器拒绝此 Key

## 🎯 可能的原因

### 1. API Key 已过期或被删除
- 阿里云控制台中删除了此 Key
- Key 有效期已到

### 2. API Key 权限不足
- Key 没有启用"通义千问多模态"服务权限
- 账户未开通相关服务

### 3. 账户问题
- 账户欠费
- 账户被限制
- 免费额度用完且未充值

### 4. 地域/环境问题
- Key 是新加坡地域的，但代码连接的是国内地域
- 需要设置 `dashscope.base_http_api_url`

## ✅ 解决方案

### 方案1: 重新创建 API Key（推荐）

**步骤：**

1. **登录阿里云百炼控制台**
   ```
   https://bailian.console.aliyun.com/
   ```

2. **进入 API Key 管理**
   - 点击右上角头像
   - 选择 "API-KEY 管理"

3. **检查现有 Key**
   - 查看 `sk-f35aed46f12a4f5fb9f023b70ab5e093` 的状态
   - 如果显示"已失效"或找不到，说明已被删除

4. **创建新的 API Key**
   - 点击 "创建新的API-KEY"
   - **立即复制并保存**（只显示一次！）
   - 更新 .env 文件

5. **更新配置**
   ```bash
   nano .env
   ```
   
   修改为新的 Key：
   ```env
   DASHSCOPE_API_KEY=sk-新的API-Key
   ```

### 方案2: 检查服务权限

1. **访问模型广场**
   ```
   https://bailian.console.aliyun.com/#/model-market
   ```

2. **确认已开通**
   - 搜索 "通义千问VL"
   - 确保状态为"已开通"
   - 如未开通，点击"免费开通"

3. **检查额度**
   - 进入"用量中心"
   - 查看剩余调用次数
   - 如已用完，需要充值

### 方案3: 检查地域设置

如果你的 Key 是新加坡地域的，需要修改代码：

**修改 `ocr_qwen.py`：**

```python
# 在 QwenOCR 类的 __init__ 方法中添加
import dashscope

# 如果是新加坡地域
dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
```

或在调用前设置：

```python
import dashscope
dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

from ocr_qwen import QwenOCR
ocr = QwenOCR()
```

### 方案4: 使用 PaddleOCR（免费替代方案）

如果暂时无法解决 API Key 问题，可以使用 PaddleOCR：

```bash
# 修复并安装 PaddleOCR
./fix_ocr_chinese.sh

# 使用 PaddleOCR 识别
python3 ocr_module.py

# 或识别单张图片
python3 -c "
from ocr_module import OCRRecognizer
ocr = OCRRecognizer(engine='paddleocr')
text = ocr.recognize_image('extracted_frames/frame_0012_290.00s.jpg')
print(text)
"
```

## 🧪 验证步骤

### 测试1: 验证新 API Key

```bash
python3 << 'EOF'
import os
from dashscope import MultiModalConversation

api_key = "sk-你的新API-Key"  # 替换为新Key

messages = [{'role': 'user', 'content': [{'text': '你好'}]}]

try:
    response = MultiModalConversation.call(
        api_key=api_key,
        model='qwen-vl-max',
        messages=messages
    )
    
    if response.status_code == 200:
        print("✅ API Key 有效！")
        print(f"响应: {response.output.choices[0].message.content[0]['text']}")
    else:
        print(f"❌ 错误: {response.code} - {response.message}")
except Exception as e:
    print(f"❌ 异常: {e}")
EOF
```

### 测试2: 测试 OCR 识别

```bash
# 更新 .env 后重新测试
python3 ocr_qwen.py --image extracted_frames/frame_0012_290.00s.jpg
```

**预期输出：**
```
✓ Qwen OCR 初始化成功
  模型: qwen-vl-max

识别结果:
----------------------------------------------------------------------
(图片中的文字内容)
----------------------------------------------------------------------
```

## 📞 获取帮助

### 阿里云官方支持

- **控制台**: https://bailian.console.aliyun.com/
- **文档**: https://help.aliyun.com/zh/model-studio/
- **工单**: 在控制台右上角提交工单

### 常见问题

**Q: 新创建的 Key 还是无效？**
A: 等待1-2分钟让系统同步，或者退出浏览器重新登录

**Q: 提示账户欠费？**
A: 进入"费用中心"充值，通常充值10元就够用很长时间

**Q: 找不到创建 Key 的入口？**
A: 确保已登录，并在右上角头像菜单中查找

**Q: 想使用免费额度？**
A: 新用户通常有免费试用额度，在"用量中心"查看

## 💡 重要提示

1. **API Key 安全**
   - 不要分享你的 API Key
   - 不要提交到 Git 仓库
   - 定期更换 Key

2. **成本控制**
   - 设置用量告警
   - 监控调用次数
   - 及时充值避免服务中断

3. **备用方案**
   - PaddleOCR（免费，离线）
   - 其他云服务商（百度、腾讯等）

## 🚀 推荐流程

**最快解决方案（5分钟）：**

```bash
# 1. 重新创建 API Key
# 访问: https://bailian.console.aliyun.com/
# 创建新的 API Key 并复制

# 2. 更新配置
nano .env
# 修改: DASHSCOPE_API_KEY=sk-新的Key

# 3. 测试
python3 ocr_qwen.py --image extracted_frames/frame_0012_290.00s.jpg

# 4. 如果还是失败，使用 PaddleOCR
./fix_ocr_chinese.sh
python3 ocr_module.py
```

---

**需要进一步帮助？**  
请提供更多信息：
- 控制台中 Key 的状态截图
- 账户余额/额度信息
- 是否为新注册用户
