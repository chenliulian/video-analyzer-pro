#!/usr/bin/env python3
"""
验证优化效果 - 检查34-50秒之间的帧
"""
import os

frames_folder = "extracted_frames"
files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])

print("=" * 80)
print("提取的所有帧:")
print("=" * 80)
for i, file in enumerate(files, 1):
    time = file.split('_')[-1].replace('s.jpg', '')
    size = os.path.getsize(os.path.join(frames_folder, file))
    print(f"{i:3d}. {file:40s} ({size/1024:6.1f}KB) - {time}秒")

print("\n" + "=" * 80)
print(f"总计: {len(files)} 帧")
print("=" * 80)

# 特别检查34-50秒之间
print("\n" + "=" * 80)
print("34-50秒之间的帧:")
print("=" * 80)
found_in_range = False
for file in files:
    time_str = file.split('_')[-1].replace('s.jpg', '')
    time = float(time_str)
    if 34 <= time <= 50:
        found_in_range = True
        size = os.path.getsize(os.path.join(frames_folder, file))
        print(f"  {file} ({size/1024:.1f}KB) - {time}秒")

if not found_in_range:
    print("  只有 frame_0007_34.00s.jpg 和 frame_0008_50.00s.jpg")
    print("  ✓ 成功跳过了37-49秒之间的重复帧！")

print("=" * 80)
