#!/usr/bin/env python3
"""
检查第21-23页的相似度
"""
import cv2
import numpy as np

def calculate_frame_similarity(frame1, frame2):
    """当前使用的相似度算法"""
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    hist_diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA) * 100
    
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    small_edges1 = cv2.resize(edges1, (64, 64))
    small_edges2 = cv2.resize(edges2, (64, 64))
    edge_diff = np.abs(small_edges1.astype(np.float32) - small_edges2.astype(np.float32)).mean() / 2.55
    
    brightness_diff = abs(gray1.mean() - gray2.mean()) / 2.55
    
    combined = hist_diff * 0.5 + edge_diff * 0.3 + brightness_diff * 0.2
    return combined, hist_diff, edge_diff, brightness_diff

frames_folder = "extracted_frames"
problem_frames = [
    f"{frames_folder}/frame_0020_559.00s.jpg",
    f"{frames_folder}/frame_0021_619.00s.jpg",
    f"{frames_folder}/frame_0022_679.00s.jpg",
]

print("=" * 80)
print("检查第21-23页的相似度")
print("=" * 80)

images = []
for frame_path in problem_frames:
    img = cv2.imread(frame_path)
    if img is not None:
        images.append((frame_path, img))
        print(f"✓ 加载: {frame_path}")
    else:
        print(f"✗ 无法加载: {frame_path}")

print("\n" + "=" * 80)
print("相邻帧之间的相似度分析")
print("=" * 80)

for i in range(len(images) - 1):
    path1, img1 = images[i]
    path2, img2 = images[i + 1]
    
    combined, hist_diff, edge_diff, brightness_diff = calculate_frame_similarity(img1, img2)
    
    print(f"\n{path1.split('/')[-1]} <-> {path2.split('/')[-1]}")
    print(f"  综合差异: {combined:.2f}")
    print(f"  直方图:   {hist_diff:.2f} (权重50%)")
    print(f"  边缘:     {edge_diff:.2f} (权重30%)")
    print(f"  亮度:     {brightness_diff:.2f} (权重20%)")
    print(f"  判断: {'不同场景' if combined >= 30 else ('应保留' if combined >= 8 else '重复/相似')}")

print("\n" + "=" * 80)
print("第一帧和最后一帧对比")
print("=" * 80)

if len(images) >= 2:
    path1, img1 = images[0]
    path2, img2 = images[-1]
    
    combined, hist_diff, edge_diff, brightness_diff = calculate_frame_similarity(img1, img2)
    
    print(f"\n{path1.split('/')[-1]} <-> {path2.split('/')[-1]}")
    print(f"  综合差异: {combined:.2f}")
    print(f"  直方图:   {hist_diff:.2f}")
    print(f"  边缘:     {edge_diff:.2f}")
    print(f"  亮度:     {brightness_diff:.2f}")
    print(f"  判断: {'不同场景' if combined >= 30 else ('应保留' if combined >= 8 else '重复/相似')}")

print("\n" + "=" * 80)
print("建议:")
print("=" * 80)
print("如果综合差异 < 8, 说明这些帧确实是重复的")
print("需要调整 max_skip_time 参数来避免强制保存重复帧")
print("=" * 80)
