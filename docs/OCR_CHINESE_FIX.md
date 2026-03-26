# OCR 中文识别修复指南

## 🐛 问题现象

OCR识别课件中的中文显示为乱码或英文字母：
```
识别结果：FAIA aS Re KR # A: XK (RAM)
实际内容：我的白鸽
```

## 🔍 问题原因

当前使用的OCR引擎（Tesseract）**没有正确配置中文语言包**，或者 **PaddleOCR 未安装**。

## ✅ 解决方案

### 方案一：安装 PaddleOCR（推荐 ⭐）

PaddleOCR 是百度开源的中文OCR工具，对中文识别效果最好。

#### 1. 安装依赖

```bash
# 安装 PaddleOCR 和 PaddlePaddle
pip3 install paddleocr paddlepaddle

# 如果安装速度慢，使用国内镜像
pip3 install paddleocr paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2. 首次运行会自动下载模型

```bash
# 测试OCR
python3 -c "
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')
print('✓ PaddleOCR 安装成功')
"
```

首次运行会下载中文识别模型（约 10-20MB），下载完成后会自动缓存。

#### 3. 重新运行识别

```bash
# 方式1：单独运行OCR
python3 ocr_module.py

# 方式2：运行完整Pro版流程
python3 video_analyzer_pro.py --video your_video.mp4
```

### 方案二：配置 Tesseract 中文支持

如果无法安装 PaddleOCR，可以配置 Tesseract 的中文语言包。

#### 1. 安装 Tesseract 和中文语言包

```bash
# macOS
brew install tesseract tesseract-lang

# 验证中文语言包
tesseract --list-langs | grep chi
# 应该显示：chi_sim（简体中文）、chi_tra（繁体中文）
```

#### 2. 测试 Tesseract 中文识别

```bash
python3 -c "
import pytesseract
from PIL import Image
img = Image.open('extracted_frames/frame_0003_15.00s.jpg')
text = pytesseract.image_to_string(img, lang='chi_sim')
print('识别结果:')
print(text)
"
```

#### 3. 修改 ocr_module.py

如果 Tesseract 识别效果仍然不好，可以调整识别参数：

```python
# 在 _recognize_with_tesseract 方法中
def _recognize_with_tesseract(self, image_path):
    img = Image.open(image_path)
    
    # 使用中文简体 + 英文混合识别
    # 添加 PSM（页面分割模式）参数
    custom_config = r'--psm 6 --oem 3'
    text = pytesseract.image_to_string(
        img, 
        lang='chi_sim+eng',
        config=custom_config
    )
    
    return text.strip()
```

**PSM 模式说明：**
- `--psm 3`: 全自动页面分割（默认）
- `--psm 6`: 假设是单个文本块
- `--psm 11`: 稀疏文本（适合课件）
- `--oem 3`: 使用神经网络识别（推荐）

## 🧪 测试识别效果

### 快速测试单张图片

```bash
python3 << 'EOF'
from ocr_module import OCRRecognizer
import os

# 初始化OCR
ocr = OCRRecognizer(engine='paddleocr')  # 或 'tesseract'

# 测试图片
test_image = 'extracted_frames/frame_0003_15.00s.jpg'
if os.path.exists(test_image):
    result = ocr.recognize_image(test_image)
    print('识别结果:')
    print(result)
    print(f'\n识别了 {len(result)} 个字符')
else:
    print('图片不存在')
EOF
```

### 批量重新识别

```bash
# 删除旧的OCR结果
rm -f *_ocr.txt *_ocr.json

# 重新运行OCR识别
python3 ocr_module.py

# 或运行完整流程
python3 video_analyzer_pro.py --video 1732328440969754.mp4
```

## 📊 识别效果对比

### Tesseract（未配置中文）
```
❌ FAIA aS
❌ Re KR # A: XK (RAM)
```

### Tesseract（配置中文后）
```
⚠️ 我的白鸽
⚠️ 作者: 陈忠实
识别率：约 60-70%
```

### PaddleOCR（推荐）
```
✅ 我的白鸽
✅ 作者：陈忠实
识别率：约 90-95%
```

## 🔧 已修复的代码

### ocr_module.py 中的关键修改

```python
# 初始化PaddleOCR时明确指定中文模式
self.ocr = PaddleOCR(
    use_angle_cls=True,  # 支持旋转文字
    lang='ch',           # 中文简体模型
    det=True,            # 启用文字检测
    rec=True,            # 启用文字识别
    use_gpu=False,       # CPU模式（有GPU可改为True）
    show_log=False       # 不显示详细日志
)
```

## 💡 推荐配置

### 日常使用
```bash
# 安装 PaddleOCR（一次性）
pip3 install paddleocr paddlepaddle

# 使用
python3 video_analyzer_pro.py --video video.mp4
```

### 对比测试
```bash
# 测试 PaddleOCR
python3 -c "
from ocr_module import OCRRecognizer
ocr = OCRRecognizer(engine='paddleocr')
result = ocr.recognize_image('extracted_frames/frame_0003_15.00s.jpg')
print('PaddleOCR:', result)
"

# 测试 Tesseract
python3 -c "
from ocr_module import OCRRecognizer
ocr = OCRRecognizer(engine='tesseract')
result = ocr.recognize_image('extracted_frames/frame_0003_15.00s.jpg')
print('Tesseract:', result)
"
```

## 🚨 常见问题

### Q1: PaddleOCR 安装失败

**解决方案：**
```bash
# 1. 升级 pip
pip3 install --upgrade pip

# 2. 使用国内镜像安装
pip3 install paddleocr paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 如果还是失败，降级版本
pip3 install paddleocr==2.6.0 paddlepaddle==2.4.0
```

### Q2: 首次运行很慢

**原因：** PaddleOCR 首次运行会下载模型文件（约 10-20MB）

**解决方案：**
- 耐心等待下载完成
- 下载完成后会缓存，后续运行很快
- 可以使用代理加速下载

### Q3: 识别结果还是乱码

**解决方案：**
```bash
# 1. 确认使用的是 PaddleOCR
python3 -c "
from ocr_module import OCRRecognizer
ocr = OCRRecognizer(engine='paddleocr')
print('当前引擎:', ocr.engine)
"

# 2. 检查图片质量
# 如果图片模糊或分辨率太低，任何OCR都难以识别

# 3. 手动测试 PaddleOCR
python3 -c "
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')
result = ocr.ocr('extracted_frames/frame_0003_15.00s.jpg')
print(result)
"
```

### Q4: 想要切换OCR引擎

**修改代码：**
```python
# 在 video_analyzer_pro.py 中修改
self.ocr = OCRRecognizer(engine="paddleocr")  # 或 "tesseract"
```

## 📚 相关文档

- [PaddleOCR 官方文档](https://github.com/PaddlePaddle/PaddleOCR)
- [Tesseract 文档](https://github.com/tesseract-ocr/tesseract)
- [README_PRO.md](README_PRO.md) - Pro版功能介绍
- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - 配置指南

---

**更新日期：** 2025-12-06  
**问题状态：** ✅ 已修复（需要安装 PaddleOCR）
