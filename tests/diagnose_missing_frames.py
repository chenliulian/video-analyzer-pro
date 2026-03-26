#!/usr/bin/env python3
"""
诊断工具 - 分析14:05-14:54时间段为何没有提取帧
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

# 分析目标时间段
video_file = "1732328440969754.mp4"
target_start = 845  # 14:05
target_end = 894    # 14:54

print("=" * 80)
print(f"诊断工具: 分析 {target_start}s-{target_end}s (14:05-14:54) 时间段")
print("=" * 80)

video = VideoFileClip(video_file)
fps = video.fps

# 采样这个时间段的关键时间点
sample_times = [
    target_start,      # 14:05 开始
    target_start + 10, # 14:15
    target_start + 25, # 14:30
    target_end - 10,   # 14:44
    target_end         # 14:54 结束
]

print("\n提取样本帧...")
frames = []
for t in sample_times:
    if t <= video.duration:
        frame = video.get_frame(t)
        frames.append((t, frame))
        print(f"  ✓ {t}s ({int(t//60)}:{int(t%60):02d})")

# 检查这些帧之间的相似度
print("\n" + "=" * 80)
print("帧之间的相似度:")
print("=" * 80)
for i in range(len(frames) - 1):
    t1, frame1 = frames[i]
    t2, frame2 = frames[i + 1]
    diff = calculate_frame_similarity(frame1, frame2)
    print(f"{int(t1//60)}:{int(t1%60):02d} <-> {int(t2//60)}:{int(t2%60):02d} : 差异 = {diff:.2f}")
    if diff < 30:
        print(f"  ⚠️  差异 < 30 (场景变化阈值), 不会触发场景变化保存")

# 查找最近保存的帧
import os
frames_folder = "extracted_frames"
saved_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])

print("\n" + "=" * 80)
print(f"目标时间段 {target_start}-{target_end}s 前后已保存的帧:")
print("=" * 80)

before_frame = None
after_frame = None

for file in saved_files:
    time_str = file.split('_')[-1].replace('s.jpg', '')
    time = float(time_str)
    if time < target_start:
        before_frame = (time, file)
    elif time > target_end and after_frame is None:
        after_frame = (time, file)
        break

if before_frame:
    t, f = before_frame
    print(f"之前: {f} - {int(t//60)}:{int(t%60):02d}")
else:
    print("之前: 无")

if after_frame:
    t, f = after_frame
    print(f"之后: {f} - {int(t//60)}:{int(t%60):02d}")
else:
    print("之后: 无")

# 测试: 如果14:30的帧与最近保存帧的相似度
if before_frame and len(frames) >= 3:
    print("\n" + "=" * 80)
    print("测试: 14:30帧 与 最近保存帧的相似度")
    print("=" * 80)
    
    before_time, before_file = before_frame
    before_img_path = os.path.join(frames_folder, before_file)
    before_img = cv2.imread(before_img_path)
    before_img = cv2.cvtColor(before_img, cv2.COLOR_BGR2RGB)
    
    middle_time, middle_frame = frames[2]  # 14:30左右
    
    diff = calculate_frame_similarity(before_img, middle_frame)
    print(f"差异 = {diff:.2f}")
    
    if diff < 10:
        print(f"  ⚠️  差异 < 10 (定时保存相似度门槛), 会被跳过!")
        print(f"  这就是为什么14:05-14:54没有保存帧")
    else:
        print(f"  ✓ 差异 >= 10, 应该会保存")

video.close()

print("\n" + "=" * 80)
print("建议:")
print("=" * 80)
print("1. 如果14:05-14:54确实只有一张图片,且与前一帧相似度很低")
print("   需要降低 similarity_threshold (当前=10)")
print("2. 或者减小 min_interval (当前=5秒)")
print("3. 或者降低 scene_threshold (当前=30)")
print("=" * 80)
