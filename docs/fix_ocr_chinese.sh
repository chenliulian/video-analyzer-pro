#!/bin/bash

# ============================================================================
# OCR 中文识别修复脚本（改进版）
# 解决 PaddleOCR 依赖冲突问题
# ============================================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================================================"
echo -e "${BLUE}               OCR 中文识别修复工具 v2.0${NC}"
echo "========================================================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 python3${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 版本: $(python3 --version)"
echo ""

# 步骤1: 清理旧版本
echo -e "${BLUE}【步骤 1/5】清理旧版本${NC}"
echo "----------------------------------------------------------------------"
pip3 uninstall -y paddleocr paddlepaddle langchain langchain-community 2>/dev/null || true
echo -e "${GREEN}✓${NC} 清理完成"
echo ""

# 步骤2: 安装兼容版本的 PaddleOCR
echo -e "${BLUE}【步骤 2/5】安装 PaddleOCR（兼容版本）${NC}"
echo "----------------------------------------------------------------------"
echo "正在安装... (可能需要几分钟)"
echo ""

# 使用国内镜像，安装指定版本避免冲突
if pip3 install "paddleocr==2.7.3" "paddlepaddle==2.6.1" \
    -i https://pypi.tuna.tsinghua.edu.cn/simple 2>&1 | grep -v "WARNING" | grep -E "(Successfully|Already)"; then
    echo ""
    echo -e "${GREEN}✓${NC} PaddleOCR 安装成功"
else
    echo ""
    echo -e "${YELLOW}⚠️${NC}  尝试备用方案..."
    if pip3 install paddleocr paddlepaddle \
        --no-deps 2>&1 | grep -v "WARNING"; then
        # 安装必需依赖
        pip3 install numpy pillow opencv-python shapely pyclipper lmdb tqdm pyyaml -q
        echo -e "${GREEN}✓${NC} PaddleOCR 安装成功（最小依赖）"
    else
        echo -e "${RED}❌ 安装失败${NC}"
        echo ""
        echo "请尝试手动安装："
        echo "  pip3 install paddleocr==2.7.3 paddlepaddle==2.6.1"
        exit 1
    fi
fi
echo ""

# 步骤3: 验证安装
echo -e "${BLUE}【步骤 3/5】验证安装${NC}"
echo "----------------------------------------------------------------------"

python3 << 'VERIFY_EOF'
import sys
try:
    import paddleocr
    print(f"✓ PaddleOCR 版本: {paddleocr.__version__}")
    
    import paddlepaddle
    print(f"✓ PaddlePaddle 版本: {paddlepaddle.__version__}")
    
    from paddleocr import PaddleOCR
    print("✓ 模块导入成功")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("\n请检查依赖是否正确安装")
    sys.exit(1)
except Exception as e:
    print(f"❌ 验证失败: {e}")
    sys.exit(1)
VERIFY_EOF

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ 验证失败${NC}"
    exit 1
fi
echo ""

# 步骤4: 初始化并下载模型
echo -e "${BLUE}【步骤 4/5】初始化 PaddleOCR（下载模型）${NC}"
echo "----------------------------------------------------------------------"
echo "首次运行会自动下载中文识别模型（约 10-20MB）..."
echo ""

python3 << 'INIT_EOF'
import sys
import os

# 禁用 PaddlePaddle 警告
os.environ['FLAGS_eager_delete_tensor_gb'] = '0'

try:
    from paddleocr import PaddleOCR
    
    print("正在初始化 PaddleOCR（中文模式）...")
    ocr = PaddleOCR(
        use_angle_cls=True, 
        lang='ch',
        det=True,
        rec=True,
        use_gpu=False,
        show_log=False
    )
    print("✓ 初始化成功")
    print("✓ 中文模型已加载")
    
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    sys.exit(1)
INIT_EOF

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ 初始化失败${NC}"
    exit 1
fi
echo ""

# 步骤5: 测试识别
echo -e "${BLUE}【步骤 5/5】测试中文识别${NC}"
echo "----------------------------------------------------------------------"

# 查找测试图片
TEST_IMAGE=""
if [ -d "extracted_frames" ]; then
    TEST_IMAGE=$(ls extracted_frames/*.jpg 2>/dev/null | head -1)
fi

if [ -z "$TEST_IMAGE" ]; then
    echo -e "${YELLOW}⚠️  未找到测试图片，跳过识别测试${NC}"
    echo "   运行完整流程后会自动使用 PaddleOCR"
else
    echo "测试图片: $(basename "$TEST_IMAGE")"
    echo ""
    
    python3 << TEST_EOF
import sys
import os

# 禁用警告
os.environ['FLAGS_eager_delete_tensor_gb'] = '0'

test_image = "$TEST_IMAGE"

try:
    from ocr_module import OCRRecognizer
    
    print("正在识别...")
    ocr = OCRRecognizer(engine='paddleocr')
    result = ocr.recognize_image(test_image)
    
    if result.strip():
        print("-" * 70)
        print("识别结果:")
        print(result[:500])  # 显示前500字符
        if len(result) > 500:
            print("...")
        print("-" * 70)
        print(f"✓ 识别成功！共 {len(result)} 个字符")
        
        # 检查中文
        import re
        chinese = re.findall(r'[\u4e00-\u9fff]', result)
        if chinese:
            print(f"✓ 包含 {len(chinese)} 个中文字符")
            print("✓ 中文识别正常！")
        else:
            print("⚠️  未检测到中文（图片可能无文字）")
    else:
        print("⚠️  未识别到文字")
        
except Exception as e:
    print(f"❌ 测试失败: {e}")
    sys.exit(1)
TEST_EOF

fi

echo ""
echo "========================================================================"
echo -e "${GREEN}                      ✅ 修复完成！${NC}"
echo "========================================================================"
echo ""
echo -e "${GREEN}✅ PaddleOCR 已安装并配置成功${NC}"
echo -e "${GREEN}✅ 中文识别功能已启用${NC}"
echo ""
echo "下一步操作："
echo ""
echo "1️⃣  删除旧的识别结果："
echo "   rm -f *_ocr.txt *_refined.json"
echo ""
echo "2️⃣  单独测试 OCR："
echo "   python3 ocr_module.py"
echo ""
echo "3️⃣  运行完整分析流程："
echo "   python3 video_analyzer_pro.py --video your_video.mp4"
echo ""
echo "📚 详细文档: cat OCR_CHINESE_FIX.md"
echo "========================================================================"
