#!/usr/bin/env python3
"""测试LLM批处理中OCR的使用"""

import sys
import json
from pathlib import Path

# 模拟video_analyzer_pro加载OCR的过程
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
print('模拟批处理模式中的OCR使用')
print('=' * 70)

# 合并所有OCR文字作为参考
all_ocr_text = "\n".join([
    f"[{name}] {text}" 
    for name, text in results.items() 
    if text.strip()
])

ocr_count = sum(1 for text in results.values() if text.strip())

print(f'📊 输入数据:')
print(f'  - OCR总数: {len(results)} 个帧')
print(f'  - OCR有内容: {ocr_count} 个帧')
print(f'  - OCR文本长度: {len(all_ocr_text)} 字符')
print()

# 显示合并后的OCR文本预览
print('OCR合并文本预览 (前500字符):')
print('-' * 70)
print(all_ocr_text[:500])
print('...')
print()

# 显示哪些帧有有用的内容(排除数学公式)
useful_frames = []
for name, text in results.items():
    # 过滤掉只有数学公式的帧
    if text.strip() and not all(c in '=+-×÷()[]{}0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz|²³⁴πMJKCSVhbDIFN  \n' for c in text):
        useful_frames.append((name, text[:50]))

print(f'有有用内容的帧 (共{len(useful_frames)}个):')
print('-' * 70)
for name, preview in useful_frames[:10]:
    print(f'{name}: {preview}...')
