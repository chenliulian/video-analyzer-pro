#!/usr/bin/env python3
"""
调试: 为什么14:05-14:54缺失了
"""
import cv2
import numpy as np
from moviepy import VideoFileClip

def calculate_frame_similarity(frame1, frame2):
    """当前使用的相似度算法"""
    if frame1.shape != frame2.shape:
        frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))
    
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
print("调试: 14:05-14:54为什么缺失")
print("=" * 80)

video_file = "1732328440969754.mp4"
video = VideoFileClip(video_file)

# 上一个保存的帧是11:31 (691s)
saved_frame_path = "extracted_frames/frame_0018_691.00s.jpg"
saved_frame = cv2.imread(saved_frame_path)
saved_frame = cv2.cvtColor(saved_frame, cv2.COLOR_BGR2RGB)

print(f"上一个保存帧: 11:31 (691s)")

# 检查从691s到900s之间每隔90秒的检查点
check_times = [691 + 90, 691 + 180]  # 781s, 871s

for check_time in check_times:
    if check_time <= video.duration:
        frame = video.get_frame(check_time)
        diff = calculate_frame_similarity(saved_frame, frame)
        
        minutes = int(check_time // 60)
        seconds = int(check_time % 60)
        
        print(f"\n检查点 {minutes:2d}:{seconds:02d} ({check_time}s):")
        print(f"  与11:31的差异: {diff:.2f}")
        print(f"  ≥8 (正常保存): {'✓' if diff >= 8 else '✗'}")
        print(f"  ≥5 且距离≥90秒 (强制保存): {'✓' if diff >= 5 else '✗'}")
        print(f"  结论: {'应该保存' if diff >= 5 else '会被跳过(差异<5)'}")

# 特别检查14:31 (871s)
print("\n" + "=" * 80)
print("特别检查 14:31 (871s):")
print("=" * 80)

frame_871 = video.get_frame(871)
diff_871 = calculate_frame_similarity(saved_frame, frame_871)
print(f"14:31 与 11:31 的差异: {diff_871:.2f}")

if diff_871 < 5:
    print(f"❌ 差异 {diff_871:.2f} < 5, 会被force_save_threshold过滤掉")
    print(f"即使距离上次保存已经 {871-691} 秒")
elif diff_871 < 8:
    print(f"⚠️  差异 {diff_871:.2f} 在 [5, 8) 之间")
    print(f"需要触发强制保存: 距离上次 {871-691} 秒 >= 90秒")
else:
    print(f"✓ 差异 {diff_871:.2f} >= 8, 应该正常保存")

video.close()
