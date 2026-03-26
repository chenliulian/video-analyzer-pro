#!/usr/bin/env python3
"""
测试实际场景:直接对refined.json进行标点符号恢复
"""
import json
import time
from pathlib import Path
from llm_agent import TextRefineAgent

def load_refined_json():
    """加载refined JSON"""
    refined_file = Path("results/1732328440969754_refined.json")
    
    if not refined_file.exists():
        print(f"❌ 找不到refined文件: {refined_file}")
        return None
    
    with open(refined_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_ocr_results():
    """加载OCR结果"""
    ocr_results = {}
    ocr_file = Path("results/1732328440969754_ocr_qwen.txt")
    
    if not ocr_file.exists():
        return ocr_results
    
    with open(ocr_file, 'r', encoding='utf-8') as f:
        current_frame = None
        current_text = []
        
        for line in f:
            line = line.strip()
            
            if line.startswith("【") and line.endswith("】"):
                # 保存上一帧
                if current_frame and current_text:
                    ocr_results[current_frame] = "\n".join(current_text)
                
                # 新帧
                current_frame = line[1:-1]
                current_text = []
            elif line and line != "-"*70:
                current_text.append(line)
        
        # 保存最后一帧
        if current_frame and current_text:
            ocr_results[current_frame] = "\n".join(current_text)
    
    return ocr_results


def main():
    print("=" * 80)
    print("对refined.json进行标点符号恢复")
    print("=" * 80)
    
    # 加载数据
    refined_data = load_refined_json()
    if not refined_data:
        return
    
    ocr_results = load_ocr_results()
    
    print(f"\n📊 数据统计:")
    print(f"  - refined帧数: {len(refined_data)}")
    print(f"  - OCR帧数: {len(ocr_results)}")
    
    # 合并所有转录文字
    all_text = " ".join([text for text in refined_data.values() if text.strip()])
    print(f"  - 总文字: {len(all_text)} 字符")
    
    # 显示前200字
    print(f"\n原始文字(无标点,前200字):")
    print(f"{all_text[:200]}...")
    
    # 初始化Agent
    print(f"\n{'='*80}")
    agent = TextRefineAgent(use_batch_mode=True)
    
    if not agent.client:
        print("❌ LLM未配置")
        return
    
    # 批处理精炼
    print(f"\n{'='*80}")
    start_time = time.time()
    
    refined_text = agent.batch_refine_entire_transcript(
        all_text,
        ocr_results
    )
    
    elapsed = time.time() - start_time
    
    # 显示结果
    print(f"\n{'='*80}")
    print(f"处理完成")
    print(f"{'='*80}")
    print(f"✓ 耗时: {elapsed:.1f}秒")
    print(f"  输入: {len(all_text)} 字符")
    print(f"  输出: {len(refined_text)} 字符")
    
    print(f"\n精炼后文字(有标点,前500字):")
    print(f"{refined_text[:500]}...")
    
    # 保存结果
    output_file = Path("results/1732328440969754_refined_with_punctuation.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(refined_text)
    
    print(f"\n✓ 已保存到: {output_file}")
    
    # 性能评估
    print(f"\n{'='*80}")
    print(f"性能对比")
    print(f"{'='*80}")
    frame_count = len(refined_data)
    old_time = frame_count * 4.0  # 逐帧模式
    
    print(f"逐帧模式: {frame_count}帧 × 4秒 = {old_time}秒 ({old_time/60:.1f}分钟)")
    print(f"批处理模式: 1次调用 = {elapsed:.1f}秒")
    print(f"✅ 速度提升: {old_time / elapsed:.1f}倍!")


if __name__ == "__main__":
    main()
