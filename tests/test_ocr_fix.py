#!/usr/bin/env python3
"""
测试OCR修复 - 验证OCR结果是否正确传递给LLM
"""
import os
import json

# 测试读取OCR文件
ocr_file = "results/1732328440969754_ocr_qwen.txt"
print("=" * 70)
print("测试1: 读取并解析OCR文件")
print("=" * 70)

if os.path.exists(ocr_file):
    with open(ocr_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 模拟image_files
    image_files = [
        "results/extracted_frames/frame_0000_0.00s.jpg",
        "results/extracted_frames/frame_0001_5.00s.jpg",
        "results/extracted_frames/frame_0002_10.00s.jpg",
        "results/extracted_frames/frame_0003_15.00s.jpg",
        "results/extracted_frames/frame_0004_20.00s.jpg",
        "results/extracted_frames/frame_0005_25.00s.jpg",
        "results/extracted_frames/frame_0006_34.00s.jpg",
        "results/extracted_frames/frame_0007_50.00s.jpg",
    ]
    
    ocr_results = {}
    current_img = None
    current_text = []
    
    for line in content.split('\n'):
        # 匹配图片文件名标记
        if line.startswith('【') and line.endswith('】'):
            # 保存上一张图片的结果
            if current_img:
                img_full_path = None
                for img_path in image_files:
                    if os.path.basename(img_path) == current_img:
                        img_full_path = img_path
                        break
                if img_full_path:
                    ocr_results[img_full_path] = '\n'.join(current_text).strip()
            # 开始新图片
            current_img = line.strip('【】')
            current_text = []
        elif line.startswith('------'):
            # 分隔线，跳过
            continue
        else:
            # OCR文本内容
            if current_img and line.strip():
                current_text.append(line)
    
    # 保存最后一张图片
    if current_img:
        img_full_path = None
        for img_path in image_files:
            if os.path.basename(img_path) == current_img:
                img_full_path = img_path
                break
        if img_full_path:
            ocr_results[img_full_path] = '\n'.join(current_text).strip()
    
    print(f"✓ 成功解析OCR文件")
    print(f"  图片总数: {len(image_files)}")
    print(f"  有OCR的图片: {len(ocr_results)}")
    print(f"  有内容的图片: {sum(1 for text in ocr_results.values() if text.strip())}")
    
    print("\n" + "=" * 70)
    print("测试2: 检查关键图片的OCR内容")
    print("=" * 70)
    
    # 检查frame_0003 (课文标题)
    key_frame = "results/extracted_frames/frame_0003_15.00s.jpg"
    if key_frame in ocr_results:
        ocr_text = ocr_results[key_frame]
        print(f"\n[frame_0003_15.00s.jpg] OCR内容:")
        print(f"  字符数: {len(ocr_text)}")
        print(f"  内容预览:")
        print(f"  {ocr_text[:200]}")
        if "我的白鸽" in ocr_text:
            print(f"  ✓ 包含课文名称: 我的白鸽")
        else:
            print(f"  ✗ 未找到课文名称")
    else:
        print(f"  ✗ 未找到该图片的OCR结果")
    
    # 检查frame_0006 (词语列表)
    key_frame2 = "results/extracted_frames/frame_0006_34.00s.jpg"
    if key_frame2 in ocr_results:
        ocr_text = ocr_results[key_frame2]
        print(f"\n[frame_0006_34.00s.jpg] OCR内容:")
        print(f"  字符数: {len(ocr_text)}")
        print(f"  内容预览:")
        print(f"  {ocr_text[:200]}")
        if "惬意" in ocr_text or "土坯" in ocr_text:
            print(f"  ✓ 包含正确词语: 惬意、土坯")
        else:
            print(f"  ✗ 未找到正确词语")
    else:
        print(f"  ✗ 未找到该图片的OCR结果")
    
else:
    print(f"✗ OCR文件不存在: {ocr_file}")

# 测试读取转录文件
print("\n" + "=" * 70)
print("测试3: 检查转录文件的时间段")
print("=" * 70)

transcript_file = "results/1732328440969754_transcript.txt"
if os.path.exists(transcript_file):
    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查24-45秒范围的内容
    import re
    pattern = r'\[(\d+\.?\d*)s\s*-\s*(\d+\.?\d*)s\]\s*(.+)'
    matches = re.findall(pattern, content, re.MULTILINE)
    
    segments_24_45 = []
    for match in matches:
        start_time = float(match[0])
        end_time = float(match[1])
        text = match[2].strip()
        
        # 检查是否在24-45秒范围内
        if not (end_time < 24 or start_time > 45):
            segments_24_45.append((start_time, end_time, text))
    
    print(f"✓ 24-45秒范围内的转录段落: {len(segments_24_45)} 个")
    if segments_24_45:
        print(f"  第一段: [{segments_24_45[0][0]:.2f}s - {segments_24_45[0][1]:.2f}s] {segments_24_45[0][2][:50]}...")
        print(f"  最后一段: [{segments_24_45[-1][0]:.2f}s - {segments_24_45[-1][1]:.2f}s] {segments_24_45[-1][2][:50]}...")
else:
    print(f"✗ 转录文件不存在: {transcript_file}")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
