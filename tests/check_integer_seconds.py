#!/usr/bin/env python3
import cv2
import numpy as np
from moviepy import VideoFileClip

def calc_diff(f1, f2):
    hsv1 = cv2.cvtColor(f1, cv2.COLOR_RGB2HSV)
    hsv2 = cv2.cvtColor(f2, cv2.COLOR_RGB2HSV)
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    hist_diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA) * 100
    gray1 = cv2.cvtColor(f1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(f2, cv2.COLOR_RGB2GRAY)
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    small_edges1 = cv2.resize(edges1, (64, 64))
    small_edges2 = cv2.resize(edges2, (64, 64))
    edge_diff = np.abs(small_edges1.astype(np.float32) - small_edges2.astype(np.float32)).mean() / 2.55
    brightness_diff = abs(gray1.mean() - gray2.mean()) / 2.55
    return hist_diff * 0.5 + edge_diff * 0.3 + brightness_diff * 0.2

video = VideoFileClip('1732328440969754.mp4')
saved_781 = cv2.imread('extracted_frames/frame_0019_781.00s.jpg')
saved_781_rgb = cv2.cvtColor(saved_781, cv2.COLOR_BGR2RGB)

print("检查整数秒时刻 (实际检查点):")
print("=" * 80)

# 从786秒开始 (781+5), 每5秒检查一次看是否应该保存
for t in [831, 841, 851, 861, 871, 881, 891]:  # 关键的10秒间隔点
    frame = video.get_frame(float(t))
    diff = calc_diff(saved_781_rgb, frame)
    time_since = t - 781
    
    status = ""
    if diff >= 8:
        status = "✓ 应保存"
    elif diff >= 5 and time_since >= 90:
        status = "⚠️  强制保存"
    else:
        status = "❌ 跳过"
    
    print(f"{t}s (+{time_since:3d}s) - 差异:{diff:5.2f} - {status}")

video.close()
