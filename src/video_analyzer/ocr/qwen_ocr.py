#!/usr/bin/env python3
"""
基于通义千问多模态API的OCR识别模块
支持更准确的中文识别，尤其适合复杂场景
"""
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict

try:
    from dashscope import MultiModalConversation
    import dashscope
except ImportError:
    print("请安装 dashscope SDK:")
    print("pip3 install dashscope")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"


class QwenOCR:
    """通义千问多模态OCR识别器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "qwen-vl-max"):
        """
        初始化OCR识别器
        
        参数:
            api_key: 阿里云API密钥（从.env或环境变量读取 DASHSCOPE_API_KEY）
            model: 模型名称，可选:
                   - qwen-vl-max (推荐，最强识别能力)
                   - qwen-vl-plus (平衡性能和成本)
                   - qwen3-vl-plus (最新版本)
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.model = model
        
        if not self.api_key:
            print("❌ 错误: 未设置 DASHSCOPE_API_KEY")
            print("\n请在 .env 文件中配置:")
            print("  DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx")
            print("\n或使用环境变量:")
            print("  export DASHSCOPE_API_KEY='sk-xxxxxxxxxxxxxxxx'")
            print("\n获取API Key: https://help.aliyun.com/zh/model-studio/get-api-key")
            raise ValueError("未设置 API 密钥")
        
        print(f"✓ Qwen OCR 初始化成功")
        print(f"  模型: {self.model}")
    
    def recognize_image(self, image_path: str, prompt: Optional[str] = None) -> str:
        """
        识别单张图片中的文字
        
        参数:
            image_path: 图片路径（支持本地路径和URL）
            prompt: 自定义提示词（默认为OCR提示）
            
        返回:
            识别到的文字内容
        """
        # 处理图片路径
        if image_path.startswith("http://") or image_path.startswith("https://"):
            # 网络图片
            formatted_path = image_path
        else:
            # 本地图片
            abs_path = os.path.abspath(image_path)
            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"图片不存在: {abs_path}")
            formatted_path = f"file://{abs_path}"
        
        # 默认OCR提示词（优化过的）
        if prompt is None:
            prompt = """请识别图片中的所有文字内容。
要求:
1. 按从上到下、从左到右的顺序识别
2. 保持原文的段落结构和换行
3. 忽略水印、logo等非正文内容
4. 如果有表格，请尽量保持表格结构
5. 只输出识别的文字，不要添加任何解释"""
        
        # 构建消息
        messages = [
            {
                'role': 'user',
                'content': [
                    {'image': formatted_path},
                    {'text': prompt}
                ]
            }
        ]
        
        try:
            # 调用API
            response = MultiModalConversation.call(
                api_key=self.api_key,
                model=self.model,
                messages=messages
            )
            
            # 提取文字
            if response.status_code == 200:
                text = response.output.choices[0].message.content[0]["text"]
                return text.strip()
            else:
                error_msg = f"API调用失败: {response.code} - {response.message}"
                print(f"❌ {error_msg}")
                return ""
                
        except Exception as e:
            print(f"❌ 识别失败: {e}")
            return ""
    
    def recognize_images_batch(self, image_paths: List[str], 
                              prompt: Optional[str] = None,
                              show_progress: bool = True) -> Dict[str, str]:
        """
        批量识别多张图片
        
        参数:
            image_paths: 图片路径列表
            prompt: 自定义提示词
            show_progress: 是否显示进度
            
        返回:
            {图片路径: 识别文字} 的字典
        """
        results = {}
        total = len(image_paths)
        
        for i, image_path in enumerate(image_paths, 1):
            if show_progress:
                print(f"\r识别进度: {i}/{total} - {os.path.basename(image_path)}", end="")
            
            text = self.recognize_image(image_path, prompt)
            results[image_path] = text
        
        if show_progress:
            print()  # 换行
        
        return results


def extract_ocr_for_frames(frames_dir: str = "extracted_frames",
                          output_file: str = None,
                          api_key: Optional[str] = None,
                          model: str = "qwen-vl-max") -> str:
    """
    提取视频帧的OCR文字（使用通义千问）
    
    参数:
        frames_dir: 视频帧目录
        output_file: 输出文件路径
        api_key: API密钥
        model: 模型名称
        
    返回:
        输出文件路径
    """
    print("=" * 70)
    print("通义千问 OCR 识别")
    print("=" * 70)
    print()
    
    # 查找图片文件
    frames_dir = Path(frames_dir)
    if not frames_dir.exists():
        print(f"❌ 错误: 目录不存在 {frames_dir}")
        return None
    
    image_files = sorted(frames_dir.glob("*.jpg"))
    if not image_files:
        print(f"❌ 错误: 目录中没有图片文件")
        return None
    
    print(f"找到 {len(image_files)} 张图片")
    print()
    
    # 初始化OCR
    ocr = QwenOCR(api_key=api_key, model=model)
    
    # 批量识别
    print("开始识别...")
    results = ocr.recognize_images_batch([str(f) for f in image_files])
    
    # 生成输出文件名
    if output_file is None:
        # 从frames_dir名称推导基础名称
        if "frames" in frames_dir.name:
            base_name = frames_dir.name.replace("_frames", "").replace("frames_", "")
        else:
            base_name = "output"
        output_file = f"{base_name}_ocr_qwen.txt"
    
    # 保存结果
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("通义千问 OCR 识别结果\n")
        f.write("=" * 70 + "\n\n")
        
        for image_path, text in results.items():
            image_name = os.path.basename(image_path)
            f.write(f"【{image_name}】\n")
            f.write("-" * 70 + "\n")
            if text:
                f.write(text + "\n")
            else:
                f.write("(未识别到文字)\n")
            f.write("\n")
    
    print()
    print("=" * 70)
    print(f"✓ OCR识别完成")
    print(f"  输出文件: {output_file}")
    print(f"  识别图片: {len(image_files)} 张")
    print(f"  成功识别: {sum(1 for t in results.values() if t)} 张")
    print("=" * 70)
    
    return output_file


def main():
    """主函数 - 用于测试"""
    import argparse
    
    parser = argparse.ArgumentParser(description='通义千问 OCR 识别')
    parser.add_argument('--image', help='单张图片路径')
    parser.add_argument('--frames-dir', default='extracted_frames', help='视频帧目录')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--model', default='qwen-vl-max', 
                       choices=['qwen-vl-max', 'qwen-vl-plus', 'qwen3-vl-plus'],
                       help='模型名称')
    parser.add_argument('--prompt', help='自定义OCR提示词')
    
    args = parser.parse_args()
    
    if args.image:
        # 识别单张图片
        print("=" * 70)
        print("通义千问 OCR - 单图识别")
        print("=" * 70)
        print(f"图片: {args.image}")
        print()
        
        ocr = QwenOCR(model=args.model)
        text = ocr.recognize_image(args.image, prompt=args.prompt)
        
        print("\n识别结果:")
        print("-" * 70)
        print(text)
        print("-" * 70)
        
    else:
        # 批量识别视频帧
        extract_ocr_for_frames(
            frames_dir=args.frames_dir,
            output_file=args.output,
            model=args.model
        )


if __name__ == "__main__":
    main()
