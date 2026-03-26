#!/usr/bin/env python3
"""测试OCR结果加载"""

from pathlib import Path

ocr_file = Path('results/1732328440969754_ocr_qwen.txt')

results = {}
current_file = None
current_text = []

with open(ocr_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        
        # 新格式(Qwen OCR): 【frame_xxx】
        if line.startswith('【') and line.endswith('】'):
            # 保存上一个文件的结果
            if current_file and current_text:
                results[current_file] = '\n'.join(current_text)
            
            # 开始新文件
            current_file = line[1:-1]  # 去掉【】
            current_text = []
        
        # 跳过分隔线和空行
        elif line and not line.startswith('=') and not line.startswith('-') and line != '(无法识别)' and line != '通义千问 OCR 识别结果':
            current_text.append(line)

# 保存最后一个文件
if current_file and current_text:
    results[current_file] = '\n'.join(current_text)

print('=' * 70)
print('测试OCR结果加载')
print('=' * 70)
print(f'加载的OCR结果数量: {len(results)} 个帧\n')

# 显示前5个结果
for i, (frame_name, text) in enumerate(list(results.items())[:5]):
    print(f'[{i+1}] {frame_name}:')
    text_preview = text[:80] + '...' if len(text) > 80 else text
    print(f'    {text_preview}\n')

# 统计有内容的帧
non_empty = sum(1 for text in results.values() if text.strip())
print(f'✓ 有内容的帧: {non_empty}/{len(results)}')
