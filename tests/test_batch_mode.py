#!/usr/bin/env python3
"""
测试批处理模式 - 一次性处理整个转录文件
"""
import time
from pathlib import Path
from llm_agent import TextRefineAgent

def test_batch_mode():
    """测试批处理模式"""
    print("=" * 80)
    print("批处理模式测试 - 处理实际转录文件")
    print("=" * 80)
    
    # 读取实际的转录文件
    transcript_file = Path("results/1732328440969754_transcript.txt")
    ocr_file = Path("results/1732328440969754_ocr_qwen.txt")
    
    if not transcript_file.exists():
        print(f"❌ 找不到转录文件: {transcript_file}")
        return
    
    if not ocr_file.exists():
        print(f"❌ 找不到OCR文件: {ocr_file}")
        return
    
    # 读取转录文本(只取前2000字符用于测试)
    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # 提取完整转录文本部分
        if "完整转录文本" in content:
            full_text = content.split("完整转录文本")[1].split("分段转录")[0]
            full_text = full_text.replace("="*70, "").strip()
            # 测试用前2000字符
            test_text = full_text[:2000]
        else:
            print("❌ 无法解析转录文件格式")
            return
    
    # 读取OCR结果(模拟)
    ocr_results = {
        "frame_0001_5.00s.jpg": "《大学教学教》",
        "frame_0003_15.00s.jpg": "我的白鸽",
        "frame_0006_34.00s.jpg": "惬意、土坯、怦然、蜕变",
    }
    
    print(f"\n📊 测试数据:")
    print(f"  - 转录文字: {len(test_text)} 字符")
    print(f"  - OCR参考: {len(ocr_results)} 个帧")
    print(f"\n原始文字(前200字):")
    print(f"{test_text[:200]}...")
    
    # 初始化Agent (批处理模式)
    print(f"\n{'='*80}")
    agent = TextRefineAgent(use_batch_mode=True)
    
    if not agent.client:
        print("❌ LLM未配置,无法测试")
        return
    
    # 测试批处理
    print(f"\n{'='*80}")
    start_time = time.time()
    
    refined_text = agent.batch_refine_entire_transcript(
        test_text,
        ocr_results
    )
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*80}")
    print(f"测试结果")
    print(f"{'='*80}")
    print(f"✓ 处理完成!")
    print(f"  - 耗时: {elapsed:.1f}秒")
    print(f"  - 输入: {len(test_text)} 字符")
    print(f"  - 输出: {len(refined_text)} 字符")
    print(f"\n精炼后的文字(前500字):")
    print(f"{refined_text[:500]}...")
    
    print(f"\n{'='*80}")
    print(f"性能评估")
    print(f"{'='*80}")
    print(f"批处理模式: 1次API调用 = {elapsed:.1f}秒")
    print(f"预估完整文件({len(content)} 字符): 约 {elapsed * (len(content) / len(test_text)):.1f}秒")
    
    # 对比逐帧模式
    frame_count = 36
    time_per_frame = 4.0  # 逐帧模式平均耗时
    old_total_time = frame_count * time_per_frame
    
    print(f"\n对比逐帧模式:")
    print(f"  - 逐帧模式: {frame_count}次API调用 = {old_total_time:.1f}秒")
    print(f"  - 批处理模式: 1次API调用 ≈ {elapsed:.1f}秒")
    print(f"  - ✅ 速度提升: {old_total_time / elapsed:.1f}倍!")


if __name__ == "__main__":
    test_batch_mode()
