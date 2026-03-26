#!/usr/bin/env python3
import os

frames_folder = 'extracted_frames'
files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.jpg')])

print('=' * 80)
print('所有提取的帧:')
print('=' * 80)
for i, file in enumerate(files, 1):
    time_str = file.split('_')[-1].replace('s.jpg', '')
    time = float(time_str)
    size = os.path.getsize(os.path.join(frames_folder, file))
    minutes = int(time // 60)
    seconds = int(time % 60)
    print(f'{i:3d}. {minutes:2d}:{seconds:02d} ({time:7.1f}s) - {file:40s} ({size/1024:6.1f}KB)')

print('\n' + '=' * 80)
print('重点检查 14:05-14:54 (845-894秒):')
print('=' * 80)
found = []
for file in files:
    time_str = file.split('_')[-1].replace('s.jpg', '')
    time = float(time_str)
    if 845 <= time <= 894:
        found.append(file)
        size = os.path.getsize(os.path.join(frames_folder, file))
        minutes = int(time // 60)
        seconds = int(time % 60)
        print(f'  ✓ {minutes:2d}:{seconds:02d} - {file} ({size/1024:.1f}KB)')

if not found:
    print('  ✗ 该时间段没有帧')
else:
    print(f'\n  共找到 {len(found)} 帧')

# 检查34-50秒
print('\n' + '=' * 80)
print('复查 34-50秒 (之前的重复区域):')
print('=' * 80)
found2 = []
for file in files:
    time_str = file.split('_')[-1].replace('s.jpg', '')
    time = float(time_str)
    if 34 <= time <= 50:
        found2.append(file)
        size = os.path.getsize(os.path.join(frames_folder, file))
        print(f'  {file} ({size/1024:.1f}KB)')

print(f'\n  共 {len(found2)} 帧 (之前有6帧重复)')
