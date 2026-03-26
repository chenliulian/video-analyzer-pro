#!/usr/bin/env python3
"""
测试V7改进: 时间范围修复 + 全局上下文
"""

import json
from llm_agent import TextRefineAgent

# 读取数据
with open("results/1732328440969754_transcript.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 解析转录段落
transcript_segments = []
for line in lines:
    if line.startswith("[") and " - " in line:
        try:
            time_part = line.split("]")[0].strip("[")
            start_str, end_str = time_part.split(" - ")
            start = float(start_str.replace("s", ""))
            end = float(end_str.replace("s", ""))
            text = line.split("] ", 1)[1].strip()
            transcript_segments.append((start, end, text))
        except:
            pass

print(f"✅ 读取转录段落: {len(transcript_segments)} 个")
print(f"   时间范围: {transcript_segments[0][0]:.1f}s - {transcript_segments[-1][1]:.1f}s")

# 模拟图片时间列表
image_times = [
    (0.0, "frame_0000_0.00s.jpg"),
    (5.0, "frame_0001_5.00s.jpg"),
    (10.0, "frame_0002_10.00s.jpg"),
    (15.0, "frame_0003_15.00s.jpg"),
    (25.0, "frame_0004_25.00s.jpg"),
]

print(f"\n✅ 模拟图片列表: {len(image_times)} 张")

# 测试1: 检查时间范围分配
print("\n" + "=" * 70)
print("测试1: 时间范围分配")
print("=" * 70)

for i in range(len(image_times)):
    img_time, img_path = image_times[i]
    
    # 计算时间范围
    if i < len(image_times) - 1:
        end_time = image_times[i+1][0]
    else:
        end_time = img_time + 60
    
    # 匹配转录段落 - 使用中点法
    matching_segments = []
    for seg_start, seg_end, seg_text in transcript_segments:
        seg_mid = (seg_start + seg_end) / 2
        if img_time <= seg_mid < end_time:
            matching_segments.append((seg_start, seg_end, seg_text))
    
    print(f"图片 {i+1}: {img_path}")
    print(f"  时间范围: [{img_time:.1f}s - {end_time:.1f}s)")
    print(f"  匹配段落: {len(matching_segments)} 个")
    if matching_segments:
        print(f"  第一段: {matching_segments[0][2][:50]}...")
        print(f"  最后一段: {matching_segments[-1][2][:50]}...")
    print()

# 测试2: 全局上下文生成
print("=" * 70)
print("测试2: 全局上下文生成")
print("=" * 70)

try:
    agent = TextRefineAgent()
    global_context = agent.generate_global_context(transcript_segments[:50])  # 使用前50段
    print(f"✅ 生成成功!")
    print(f"   上下文内容: {global_context}")
except Exception as e:
    print(f"❌ 生成失败: {e}")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
