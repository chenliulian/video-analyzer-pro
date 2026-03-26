#!/usr/bin/env python3
"""
测试JPEG压缩后的差异
"""
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

# 获取781秒的原始帧
frame_781_orig = video.get_frame(781)

# 保存并重新加载(模拟实际保存)
cv2.imwrite('temp_save.jpg', cv2.cvtColor(frame_781_orig, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
frame_781_saved_bgr = cv2.imread('temp_save.jpg')
frame_781_saved = cv2.cvtColor(frame_781_saved_bgr, cv2.COLOR_BGR2RGB)

# 获取871秒的原始帧
frame_871_orig = video.get_frame(871)

print("=" * 80)
print("JPEG压缩对相似度的影响")
print("=" * 80)

# 情况1: 原始帧 vs 原始帧
diff1 = calc_diff(frame_781_orig, frame_871_orig)
print(f"1. 原始781 vs 原始871: {diff1:.2f}")

# 情况2: 保存的781 vs 原始871 (实际代码的比较方式 - 错误!)
diff2 = calc_diff(frame_781_saved, frame_871_orig)
print(f"2. 保存781 vs 原始871: {diff2:.2f} (实际代码中的情况)")

# 情况3: 原始781 vs 原始781保存后加载 (自身压缩损失)
diff3 = calc_diff(frame_781_orig, frame_781_saved)
print(f"3. 原始781 vs 保存781: {diff3:.2f} (JPEG压缩误差)")

# 情况4: 保存后的781 vs 保存后的781 (应该是0)
cv2.imwrite('temp_save2.jpg', cv2.cvtColor(frame_781_orig, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
frame_781_saved2 = cv2.cvtColor(cv2.imread('temp_save2.jpg'), cv2.COLOR_BGR2RGB)
diff4 = calc_diff(frame_781_saved, frame_781_saved2)
print(f"4. 保存781 vs 保存781(第二次): {diff4:.2f}")

video.close()

print("\n" + "=" * 80)
print("问题分析:")
print("=" * 80)
print("代码中用 frame.copy() 保存到 prev_saved_frame")
print("这是原始RGB帧, 但文件保存的是JPEG压缩后的")
print("两者比较会有6-7的JPEG压缩误差")
print("导致8.5的实际差异变成了~2的比较差异")
print("=" * 80)
