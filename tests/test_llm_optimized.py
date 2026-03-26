#!/usr/bin/env python3
"""
测试优化后的LLM Agent性能
"""
import time
from llm_agent import TextRefineAgent

def test_optimized_agent():
    """测试优化后的Agent"""
    print("=" * 80)
    print("优化后的LLM Agent测试")
    print("=" * 80)
    
    # 初始化Agent
    agent = TextRefineAgent()
    
    if not agent.client:
        print("❌ LLM未配置,无法测试")
        return
    
    # 测试数据 (模拟实际场景)
    test_cases = [
        {
            "name": "简短文字(典型场景)",
            "transcript": [
                (0.0, 5.0, "同学们好"),
                (5.0, 10.0, "今天我们要学习的课文是 过的白割")
            ],
            "ocr": "《我的白鸽》",
            "time": 5.0
        },
        {
            "name": "中等长度文字",
            "transcript": [
                (10.0, 15.0, "在阅读文章之前"),
                (15.0, 20.0, "我们先一起来回顾 以下词语的读音"),
                (20.0, 25.0, "同学们可以跟著一起 读读写写")
            ],
            "ocr": "词语学习",
            "time": 15.0
        },
        {
            "name": "长文字(压力测试)",
            "transcript": [
                (i, i+5, f"这是第{i//5 + 1}段测试文字 包含一些内容")
                for i in range(0, 100, 5)
            ],
            "ocr": "测试课件标题",
            "time": 50.0
        }
    ]
    
    total_time = 0
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n{'-' * 80}")
        print(f"测试 {idx}: {test_case['name']}")
        print(f"{'-' * 80}")
        
        start_time = time.time()
        
        result = agent.refine_transcript_with_ocr(
            test_case["transcript"],
            test_case["ocr"],
            test_case["time"]
        )
        
        elapsed = time.time() - start_time
        total_time += elapsed
        
        print(f"✓ 完成 (耗时: {elapsed:.2f}秒)")
        print(f"  输入段落数: {len(test_case['transcript'])}")
        print(f"  OCR文字: {test_case['ocr']}")
        print(f"  输出结果: {result[:100]}..." if len(result) > 100 else f"  输出结果: {result}")
    
    # 总结
    print(f"\n{'=' * 80}")
    print(f"测试总结")
    print(f"{'=' * 80}")
    print(f"总测试用例: {len(test_cases)}")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"平均耗时: {total_time / len(test_cases):.2f}秒/次")
    print(f"\n预估36帧处理时间: {(total_time / len(test_cases)) * 36:.1f}秒 (约{((total_time / len(test_cases)) * 36) / 60:.1f}分钟)")
    
    # 评估
    avg_time = total_time / len(test_cases)
    if avg_time < 2:
        print(f"\n✅ 性能优秀: 平均{avg_time:.2f}秒/次")
    elif avg_time < 3:
        print(f"\n✓ 性能良好: 平均{avg_time:.2f}秒/次")
    elif avg_time < 5:
        print(f"\n⚠️  性能一般: 平均{avg_time:.2f}秒/次")
    else:
        print(f"\n❌ 性能较慢: 平均{avg_time:.2f}秒/次")
        print("   建议:")
        print("   1. 检查网络连接")
        print("   2. 更换更快的模型(如qwen-turbo)")
        print("   3. 减少max_tokens")


if __name__ == "__main__":
    test_optimized_agent()
