#!/usr/bin/env python3
"""
最终验证 - 检查14:31帧是否正确捕获了14:05-14:54的画面
"""
import cv2
import numpy as np
from moviepy import VideoFileClip

def calculate_frame_similarity(frame1, frame2):
    """当前使用的相似度算法"""
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2HSV)
    
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    hist_diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA) * 100
    
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    small_edges1 = cv2.resize(edges1, (64, 64))
    small_edges2 = cv2.resize(edges2, (64, 64))
    edge_diff = np.abs(small_edges1.astype(np.float32) - small_edges2.astype(np.float32)).mean() / 2.55
    
    brightness_diff = abs(gray1.mean() - gray2.mean()) / 2.55
    
    combined = hist_diff * 0.5 + edge_diff * 0.3 + brightness_diff * 0.2
    return combined

print("=" * 80)
print("最终验证: 14:31帧是否代表14:05-14:54时间段")
print("=" * 80)

video_file = "1732328440969754.mp4"
video = VideoFileClip(video_file)

# 提取关键时间点的帧
times = [845, 855, 871, 884, 894]  # 14:05, 14:15, 14:31(保存的), 14:44, 14:54
frames = {}

for t in times:
    frame = video.get_frame(t)
    frames[t] = frame
    print(f"✓ 提取 {int(t//60)}:{int(t%60):02d} ({t}s)")

# 加载保存的14:31帧
saved_frame_path = "extracted_frames/frame_0026_871.00s.jpg"
saved_frame = cv2.imread(saved_frame_path)
saved_frame = cv2.cvtColor(saved_frame, cv2.COLOR_BGR2RGB)

print("\n" + "=" * 80)
print("保存的14:31帧 与 该时间段各时间点的相似度:")
print("=" * 80)

for t in times:
    diff = calculate_frame_similarity(saved_frame, frames[t])
    status = "✓ 相同画面" if diff < 5 else "不同"
    print(f"{int(t//60)}:{int(t%60):02d} - 差异: {diff:.2f} - {status}")

video.close()

print("\n" + "=" * 80)
print("结论:")
print("=" * 80)
print("如果所有差异都<5, 说明14:31帧正确代表了整个14:05-14:54时间段")
print("=" * 80)
