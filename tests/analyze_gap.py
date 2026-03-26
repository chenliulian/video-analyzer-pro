#!/usr/bin/env python3
"""
分析13:01到15:04之间为什么跳过了
"""
import cv2
import numpy as np
from moviepy import VideoFileClip

def calc_diff(f1, f2):
    hsv1 = cv2.cvtColor(f1, cv2.COLOR_RGB2HSV if len(f1.shape) == 3 else cv2.COLOR_GRAY2RGB)
    hsv2 = cv2.cvtColor(f2, cv2.COLOR_RGB2HSV if len(f2.shape) == 3 else cv2.COLOR_GRAY2RGB)
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    hist_diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA) * 100
    
    gray1 = cv2.cvtColor(f1, cv2.COLOR_RGB2GRAY) if len(f1.shape) == 3 else f1
    gray2 = cv2.cvtColor(f2, cv2.COLOR_RGB2GRAY) if len(f2.shape) == 3 else f2
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    small_edges1 = cv2.resize(edges1, (64, 64))
    small_edges2 = cv2.resize(edges2, (64, 64))
    edge_diff = np.abs(small_edges1.astype(np.float32) - small_edges2.astype(np.float32)).mean() / 2.55
    brightness_diff = abs(gray1.mean() - gray2.mean()) / 2.55
    return hist_diff * 0.5 + edge_diff * 0.3 + brightness_diff * 0.2

print("=" * 80)
print("分析 13:01 (781s) 到 15:04 (904s) 之间")
print("=" * 80)

video = VideoFileClip('1732328440969754.mp4')

# 加载13:01的保存帧
saved_781 = cv2.imread('extracted_frames/frame_0019_781.00s.jpg')
saved_781_rgb = cv2.cvtColor(saved_781, cv2.COLOR_BGR2RGB)

# 检查每隔5秒的关键时间点(min_interval=5)
check_times = list(range(786, 905, 5))  # 从781+5开始,每5秒一个检查点

print("\n检查点分析 (min_interval=5秒):")
print("-" * 80)

for t in check_times:
    frame = video.get_frame(t)
    diff = calc_diff(saved_781_rgb, frame)
    
    time_since = t - 781
    minutes = int(t // 60)
    seconds = int(t % 60)
    
    status = ""
    if diff >= 30:
        status = "✓ 场景变化 (≥30)"
    elif diff >= 8:
        status = "✓ 定时保存 (≥8)"
    elif diff >= 5 and time_since >= 90:
        status = "⚠️  强制保存 (≥5 且 ≥90s)"
    elif diff < 5:
        status = f"❌ 跳过 (<5, 真重复)"
    else:
        status = f"❌ 跳过 (差异{diff:.1f}, 时间{time_since}s)"
    
    if diff < 10 or t in [871, 904]:  # 只打印差异<10或关键点
        print(f"{minutes:2d}:{seconds:02d} (+{time_since:3d}s) - 差异:{diff:5.2f} - {status}")

video.close()

print("\n" * 1 + "=" * 80)
print("结论:")
print("=" * 80)
print("如果大部分时间点差异<5, 说明这段确实是重复/静态画面")
print("如果有差异≥5但<8的点且时间≥90秒, 应该触发强制保存")
print("=" * 80)
