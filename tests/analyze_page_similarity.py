#!/usr/bin/env python3
"""
分析PDF特定页面对应图片的相似度
"""
import os
import cv2
import numpy as np

def calculate_frame_similarity_detailed(frame1, frame2):
    """
    计算相似度 - 返回详细的子项数值
    """
    # 1. 直方图相似度 - 检测颜色和亮度变化
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2HSV)
    
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    hist_diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA) * 100
    
    # 2. 边缘检测相似度 - 检测结构变化
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    small_edges1 = cv2.resize(edges1, (64, 64))
    small_edges2 = cv2.resize(edges2, (64, 64))
    edge_diff = np.abs(small_edges1.astype(np.float32) - small_edges2.astype(np.float32)).mean() / 2.55
    
    # 3. 亮度差异
    brightness_diff = abs(gray1.mean() - gray2.mean()) / 2.55
    
    # 加权组合
    combined = hist_diff * 0.5 + edge_diff * 0.3 + brightness_diff * 0.2
    
    return {
        'hist_diff': hist_diff,
        'edge_diff': edge_diff,
        'brightness_diff': brightness_diff,
        'combined': combined
    }


def find_image_by_pdf_page(pdf_page_num, extracted_frames_dir="extracted_frames"):
    """
    根据PDF页码找到对应的图片
    
    PDF页面结构: 图片1 -> 文字页1 -> 图片2 -> 文字页2 -> ...
    所以: PDF页码 = 图片序号 * 2 - 1 (奇数页是图片)
    或者: 图片序号 = (PDF页码 + 1) // 2
    """
    # 计算图片序号
    # 如果PDF页码是奇数，说明是图片页
    # 如果是偶数，说明是文字页
    
    if pdf_page_num % 2 == 0:
        print(f"警告: PDF第{pdf_page_num}页是文字页，不是图片页")
        return None
    
    # 图片序号（从0开始）
    image_index = (pdf_page_num - 1) // 2
    
    # 获取所有图片文件
    image_files = sorted([f for f in os.listdir(extracted_frames_dir) if f.endswith('.jpg')])
    
    if image_index >= len(image_files):
        print(f"错误: 图片序号{image_index}超出范围（共{len(image_files)}张图片）")
        return None
    
    image_file = image_files[image_index]
    image_path = os.path.join(extracted_frames_dir, image_file)
    
    return image_path


def main():
    # PDF页码
    page1 = 183
    page2 = 185
    
    print("=" * 70)
    print(f"分析PDF第{page1}页和第{page2}页对应图片的相似度")
    print("=" * 70)
    
    # 找到对应的图片文件
    img_path1 = find_image_by_pdf_page(page1)
    img_path2 = find_image_by_pdf_page(page2)
    
    if not img_path1 or not img_path2:
        print("错误: 无法找到对应的图片文件")
        return
    
    print(f"\nPDF第{page1}页对应图片: {os.path.basename(img_path1)}")
    print(f"PDF第{page2}页对应图片: {os.path.basename(img_path2)}")
    
    # 读取图片
    if not os.path.exists(img_path1):
        print(f"错误: 图片不存在: {img_path1}")
        return
    
    if not os.path.exists(img_path2):
        print(f"错误: 图片不存在: {img_path2}")
        return
    
    img1_bgr = cv2.imread(img_path1)
    img2_bgr = cv2.imread(img_path2)
    
    img1 = cv2.cvtColor(img1_bgr, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2_bgr, cv2.COLOR_BGR2RGB)
    
    print(f"\n图片1尺寸: {img1.shape}")
    print(f"图片2尺寸: {img2.shape}")
    
    # 计算相似度
    print("\n" + "=" * 70)
    print("相似度分析结果:")
    print("=" * 70)
    
    result = calculate_frame_similarity_detailed(img1, img2)
    
    print(f"\n1. 直方图差异 (hist_diff):      {result['hist_diff']:.2f}")
    print(f"   - 检测颜色和亮度变化")
    print(f"   - 权重: 50%")
    
    print(f"\n2. 边缘检测差异 (edge_diff):     {result['edge_diff']:.2f}")
    print(f"   - 检测结构变化")
    print(f"   - 权重: 30%")
    
    print(f"\n3. 亮度差异 (brightness_diff):  {result['brightness_diff']:.2f}")
    print(f"   - 检测整体亮度变化")
    print(f"   - 权重: 20%")
    
    print(f"\n" + "-" * 70)
    print(f"综合差异度 (combined):          {result['combined']:.2f}")
    print("-" * 70)
    
    # 判断相似度
    print("\n" + "=" * 70)
    print("相似度评估:")
    print("=" * 70)
    
    combined = result['combined']
    
    if combined < 3:
        similarity_level = "极度相似（几乎完全一样）"
    elif combined < 8:
        similarity_level = "非常相似（细微差异）"
    elif combined < 15:
        similarity_level = "相似（有一定差异）"
    elif combined < 30:
        similarity_level = "有差异（场景变化不大）"
    else:
        similarity_level = "差异较大（场景明显变化）"
    
    print(f"\n综合差异度: {combined:.2f}")
    print(f"相似度等级: {similarity_level}")
    
    # 参考阈值说明
    print("\n" + "-" * 70)
    print("参考阈值说明:")
    print("-" * 70)
    print("  scene_threshold = 30          (场景变化阈值)")
    print("  similarity_threshold = 8      (定时保存相似度门槛)")
    print("  force_save_threshold = 3      (强制保存差异门槛)")
    print("\n当前配置下:")
    if combined >= 30:
        print("  ✓ 会被识别为【场景变化】，立即保存")
    elif combined >= 8:
        print("  ✓ 会被识别为【定时保存】，达到间隔时保存")
    elif combined >= 3:
        print("  ✓ 会被识别为【强制保存】，超过60秒时保存")
    else:
        print("  ✗ 会被识别为【重复帧】，跳过不保存")
    
    print("\n" + "=" * 70)
    
    # 分析为什么会保存这两张图片
    print("\n为什么会同时保存这两张图片？")
    print("-" * 70)
    
    # 获取时间信息
    import re
    match1 = re.search(r'_(\d+\.?\d*)s\.jpg', os.path.basename(img_path1))
    match2 = re.search(r'_(\d+\.?\d*)s\.jpg', os.path.basename(img_path2))
    
    if match1 and match2:
        time1 = float(match1.group(1))
        time2 = float(match2.group(1))
        time_diff = time2 - time1
        
        print(f"\n图片1时间: {time1:.2f}s")
        print(f"图片2时间: {time2:.2f}s")
        print(f"时间间隔: {time_diff:.2f}s")
        
        if time_diff >= 60:
            print(f"\n可能原因: 时间间隔 {time_diff:.2f}s ≥ 60s")
            print(f"         触发了【强制保存】机制（max_skip_time=60）")
            print(f"         虽然差异度只有 {combined:.2f}，但因为超过60秒未保存")
            print(f"         且差异 {combined:.2f} ≥ force_save_threshold(3)")
            print(f"         所以仍然保存了")
        elif combined >= 8:
            print(f"\n可能原因: 差异度 {combined:.2f} ≥ similarity_threshold(8)")
            print(f"         且时间间隔 {time_diff:.2f}s ≥ min_interval(5s)")
            print(f"         触发了【定时保存】机制")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
