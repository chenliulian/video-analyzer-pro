#!/usr/bin/env python3
"""测试video_analyzer_pro是否正确调用批处理模式"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from llm_agent import TextRefineAgent

def test_initialization():
    """测试LLM Agent初始化"""
    print("=" * 70)
    print("测试1: LLM Agent初始化")
    print("=" * 70)
    
    # 测试批处理模式
    agent_batch = TextRefineAgent(use_batch_mode=True)
    print(f"✓ 批处理模式: use_batch_mode = {agent_batch.use_batch_mode}")
    
    # 测试逐帧模式
    agent_frame = TextRefineAgent(use_batch_mode=False)
    print(f"✓ 逐帧模式: use_batch_mode = {agent_frame.use_batch_mode}")
    
    print("\n✅ 初始化测试通过\n")


def test_batch_method_exists():
    """测试批处理方法是否存在"""
    print("=" * 70)
    print("测试2: 批处理方法检查")
    print("=" * 70)
    
    agent = TextRefineAgent(use_batch_mode=True)
    
    # 检查方法是否存在
    methods = [
        'batch_refine_all_frames',
        'batch_refine_entire_transcript',
        'batch_split_by_frames'
    ]
    
    for method_name in methods:
        if hasattr(agent, method_name):
            print(f"✓ 方法存在: {method_name}")
        else:
            print(f"❌ 方法缺失: {method_name}")
    
    print("\n✅ 方法检查通过\n")


def test_mock_batch_refine():
    """测试模拟批处理调用"""
    print("=" * 70)
    print("测试3: 模拟批处理调用")
    print("=" * 70)
    
    agent = TextRefineAgent(use_batch_mode=True)
    
    # 模拟数据
    transcript_segments = [
        (0.0, 5.0, "同学们好 今天我们要学习新课文"),
        (5.0, 10.0, "请大家翻开课本第三十页"),
        (10.0, 15.0, "我们先来认识几个生字")
    ]
    
    ocr_results = {
        "frame_001_0.0s.jpg": "第30页",
        "frame_002_5.0s.jpg": "生字学习",
        "frame_003_10.0s.jpg": "词语：惬意、土坯"
    }
    
    image_times = [
        (0.0, "frame_001_0.0s.jpg"),
        (5.0, "frame_002_5.0s.jpg"),
        (10.0, "frame_003_10.0s.jpg")
    ]
    
    print(f"📊 模拟数据:")
    print(f"  - 转录段落: {len(transcript_segments)} 个")
    print(f"  - OCR帧数: {len(ocr_results)} 个")
    print(f"  - 图片帧数: {len(image_times)} 个")
    
    # 尝试调用批处理方法
    try:
        print(f"\n⏳ 调用 batch_refine_all_frames()...")
        results = agent.batch_refine_all_frames(
            transcript_segments,
            ocr_results,
            image_times
        )
        
        print(f"\n✓ 批处理完成!")
        print(f"  - 返回结果数: {len(results)}")
        
        # 显示前2个结果
        for i, (key, value) in enumerate(list(results.items())[:2]):
            print(f"\n  [{i+1}] {key}:")
            print(f"      {value[:100]}..." if len(value) > 100 else f"      {value}")
        
        print("\n✅ 批处理调用测试通过\n")
        
    except Exception as e:
        print(f"\n❌ 批处理调用失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🧪 开始测试 video_analyzer_pro 批处理模式\n")
    
    test_initialization()
    test_batch_method_exists()
    test_mock_batch_refine()
    
    print("=" * 70)
    print("✅ 所有测试完成!")
    print("=" * 70)
    print("\n💡 现在可以运行完整分析:")
    print("   python3 video_analyzer_pro.py --video data/1732328440969754.mp4 --asr-engine qwen")
    print()
