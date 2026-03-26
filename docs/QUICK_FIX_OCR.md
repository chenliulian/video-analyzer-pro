# OCR 中文识别快速修复指南 🚀

## ❌ 你遇到的问题

运行 `fix_ocr_chinese.sh` 时出现错误：
```
❌ 导入失败: No module named 'langchain.docstore'
```

## 🎯 问题原因

PaddleOCR 的某些版本依赖了 `langchain`，但版本不兼容导致导入失败。

## ✅ 解决方案

### 方案一：使用新版修复脚本（推荐）

```bash
# 直接运行改进版脚本
./fix_ocr_chinese.sh
```

**新脚本的改进：**
- ✅ 自动清理冲突的依赖
- ✅ 安装指定的兼容版本
- ✅ 避免 langchain 依赖问题
- ✅ 更好的错误处理

### 方案二：手动修复

```bash
# 1. 清理旧版本
pip3 uninstall -y paddleocr paddlepaddle langchain langchain-community

# 2. 安装指定版本（兼容性最好）
pip3 install paddleocr==2.7.3 paddlepaddle==2.6.1 \
  -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 验证安装
python3 -c "from paddleocr import PaddleOCR; print('✓ 安装成功')"

# 4. 测试识别
python3 ocr_module.py
```

### 方案三：最小依赖安装

如果上面的方法还有问题，尝试最小依赖安装：

```bash
# 1. 清理
pip3 uninstall -y paddleocr paddlepaddle

# 2. 安装核心包（不安装额外依赖）
pip3 install paddleocr paddlepaddle --no-deps

# 3. 手动安装必需依赖
pip3 install numpy pillow opencv-python shapely pyclipper \
  lmdb tqdm pyyaml

# 4. 验证
python3 -c "from paddleocr import PaddleOCR; print('✓ 成功')"
```

## 🧪 验证是否修复成功

运行测试命令：

```bash
python3 << 'EOF'
import os
os.environ['FLAGS_eager_delete_tensor_gb'] = '0'

from paddleocr import PaddleOCR
import paddleocr

print(f"✓ PaddleOCR 版本: {paddleocr.__version__}")

ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
print("✓ 初始化成功")
print("✓ 中文模型已加载")
EOF
```

**预期输出：**
```
✓ PaddleOCR 版本: 2.7.3
下载中文模型...
✓ 初始化成功
✓ 中文模型已加载
```

## 🚀 修复后的使用

### 1. 删除旧的识别结果

```bash
rm -f *_ocr.txt *_refined.json
```

### 2. 单独测试 OCR

```bash
python3 ocr_module.py
```

### 3. 运行完整流程

```bash
python3 video_analyzer_pro.py --video 1732328440969754.mp4
```

## 📊 效果对比

### 修复前（Tesseract 错误识别）
```
❌ FAIA aS RE KR # A
❌ bBSSA BE UR 4X
```

### 修复后（PaddleOCR 中文识别）
```
✅ 我的白鸽
✅ 作者：陈忠实
✅ 在阅读文章之前，请同学们...
```

## 🔍 常见问题

### Q1: 安装太慢怎么办？

使用国内镜像：
```bash
pip3 install paddleocr==2.7.3 paddlepaddle==2.6.1 \
  -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 提示 "No module named xxx"？

逐个安装缺失的依赖：
```bash
pip3 install numpy pillow opencv-python shapely \
  pyclipper lmdb tqdm pyyaml
```

### Q3: Mac M1/M2 芯片安装失败？

```bash
# 使用 CPU 版本
pip3 install paddlepaddle==2.6.1
pip3 install paddleocr==2.7.3

# 如果还有问题，使用 Rosetta
arch -x86_64 pip3 install paddleocr paddlepaddle
```

### Q4: 识别结果还是乱码？

检查是否正确使用了中文模式：
```bash
python3 -c "
from ocr_module import OCRRecognizer
ocr = OCRRecognizer(engine='paddleocr')
print(ocr.engine)  # 应该是 'paddleocr'
"
```

## 💡 最佳实践

1. **安装固定版本** - 避免最新版的兼容性问题
   ```bash
   paddleocr==2.7.3
   paddlepaddle==2.6.1
   ```

2. **使用国内镜像** - 加速下载
   ```bash
   -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. **清理旧版本** - 避免冲突
   ```bash
   pip3 uninstall -y paddleocr paddlepaddle
   ```

4. **禁用警告** - 让输出更清晰
   ```python
   import os
   os.environ['FLAGS_eager_delete_tensor_gb'] = '0'
   ```

## 📚 更多资源

- **[OCR_CHINESE_FIX.md](OCR_CHINESE_FIX.md)** - 完整的 OCR 修复指南
- **[README_PRO.md](README_PRO.md)** - Pro 版功能介绍
- **[PRO_VERSION_GUIDE.md](PRO_VERSION_GUIDE.md)** - 详细使用说明

---

**需要帮助？** 

1. 查看错误日志：`cat error.log`
2. 运行诊断：`python3 -m pip check`
3. 重新安装：`./fix_ocr_chinese.sh`
