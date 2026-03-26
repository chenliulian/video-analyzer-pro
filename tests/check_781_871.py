#!/usr/bin/env python3
import cv2
import numpy as np
from moviepy import VideoFileClip

def calc_diff(f1, f2):
    hsv1 = cv2.cvtColor(f1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(f2, cv2.COLOR_BGR2HSV)
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    hist_diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA) * 100
    gray1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    small_edges1 = cv2.resize(edges1, (64, 64))
    small_edges2 = cv2.resize(edges2, (64, 64))
    edge_diff = np.abs(small_edges1.astype(np.float32) - small_edges2.astype(np.float32)).mean() / 2.55
    brightness_diff = abs(gray1.mean() - gray2.mean()) / 2.55
    return hist_diff * 0.5 + edge_diff * 0.3 + brightness_diff * 0.2

video = VideoFileClip('1732328440969754.mp4')

frame_781 = video.get_frame(781)
frame_871 = video.get_frame(871)

# 保存并加载(模拟实际保存过程)
cv2.imwrite('temp_781.jpg', cv2.cvtColor(frame_781, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
saved_781 = cv2.imread('temp_781.jpg')
saved_781_rgb = cv2.cvtColor(saved_781, cv2.COLOR_BGR2RGB)

# 871直接用原始帧比较
diff = calc_diff(saved_781_rgb, frame_871)
print(f'13:01 (781s保存的) <-> 14:31 (871s原始) 差异: {diff:.2f}')
print(f'判断: {"✓ 会保存(≥8)" if diff >= 8 else ("⚠️ 强制保存(5-8)" if diff >= 5 else "❌ 跳过(<5)")}')

video.close()
