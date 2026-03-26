#!/usr/bin/env python3
"""
测试LLM Agent的速度和性能
"""
import os
import sys
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    print("错误: 未安装openai库")
    print("安装: pip3 install openai")
    sys.exit(1)


def test_llm_connection():
    """测试LLM连接和响应速度"""
    print("=" * 80)
    print("LLM 连接和速度测试")
    print("=" * 80)
    
    # 读取配置
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")
    
    print(f"\n配置信息:")
    print(f"  API Key: {api_key[:20]}...{api_key[-10:] if api_key else 'None'}")
    print(f"  Base URL: {base_url}")
    print(f"  Model: {model}")
    
    if not api_key:
        print("\n❌ 错误: LLM_API_KEY 未配置")
        return
    
    # 初始化客户端
    try:
        if base_url:
            client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            client = OpenAI(api_key=api_key)
        print("\n✓ 客户端初始化成功")
    except Exception as e:
        print(f"\n❌ 客户端初始化失败: {e}")
        return
    
    # 测试1: 简单请求
    print("\n" + "-" * 80)
    print("测试1: 简单请求 (Hello World)")
    print("-" * 80)
    
    try:
        start_time = time.time()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个测试助手。"},
                {"role": "user", "content": "请说'你好'"}
            ],
            temperature=0.3,
            max_tokens=50
        )
        
        elapsed = time.time() - start_time
        
        if response and hasattr(response, 'choices') and response.choices:
            result = response.choices[0].message.content
            print(f"✓ 响应成功 (耗时: {elapsed:.2f}秒)")
            print(f"  响应内容: {result}")
        else:
            print(f"⚠️  响应结构异常")
            print(f"  响应: {response}")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试2: 标点符号恢复 (模拟实际场景)
    print("\n" + "-" * 80)
    print("测试2: 标点符号恢复 (实际场景)")
    print("-" * 80)
    
    test_text = "同学们好 今天我们要学习的课文是 过的白割 在阅读文章之前 我们先一起来回顾 以下词语的读音"
    
    try:
        start_time = time.time()
        
        prompt = f"""请为以下文字添加标点符号，不要改变内容。

文字：
{test_text}

要求：
1. 只添加标点符号
2. 不要改变原文
3. 直接输出结果，不要添加说明"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是文字编辑助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        elapsed = time.time() - start_time
        
        if response and hasattr(response, 'choices') and response.choices:
            result = response.choices[0].message.content
            print(f"✓ 响应成功 (耗时: {elapsed:.2f}秒)")
            print(f"  原文: {test_text}")
            print(f"  结果: {result}")
        else:
            print(f"⚠️  响应结构异常")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试3: 复杂提示词 (模拟当前llm_agent的prompt)
    print("\n" + "-" * 80)
    print("测试3: 复杂提示词 (当前llm_agent的prompt)")
    print("-" * 80)
    
    ocr_text = "《大学教学教》"
    transcript_text = "同学们好 今天我们要学习的课文是 过的白割"
    
    try:
        start_time = time.time()
        
        prompt = f"""请整理以下课堂讲座的文字内容。

**任务要求：**
1. **纠错**: 结合OCR识别的课件文字纠正语音转录中的错误
2. **标点**: 添加准确的中文标点符号(。,、;:?!)
3. **分段**: 将内容整理成层次分明、逻辑清晰的段落
4. **忠实原文**: 不要改变原意,不要添加额外内容
5. **格式化**: 使用Markdown格式

**时间点：** 0分5秒

**OCR识别的课件文字(作为参考)：**
```
{ocr_text}
```

**语音转录文字(需要纠错和格式化)：**
```
{transcript_text}
```

**输出格式：**
- 直接输出整理好的文字内容
- 使用清晰的段落结构
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的文字编辑助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        elapsed = time.time() - start_time
        
        if response and hasattr(response, 'choices') and response.choices:
            result = response.choices[0].message.content
            print(f"✓ 响应成功 (耗时: {elapsed:.2f}秒)")
            print(f"  结果: {result}")
        else:
            print(f"⚠️  响应结构异常")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试4: 全局上下文生成 (5000字符)
    print("\n" + "-" * 80)
    print("测试4: 全局上下文生成 (模拟完整转录)")
    print("-" * 80)
    
    full_text = "同学们好 " * 500  # 模拟大量文本
    
    try:
        start_time = time.time()
        
        prompt = f"""请分析以下完整的课堂讲座转录文字,提供一个简洁的总结性描述。

**任务要求：**
1. 识别讲座的主题
2. 提取关键的专业术语
3. 概括讲座的主要内容结构
4. 输出格式要简洁,100字以内

**完整转录文字：**
```
{full_text[:5000]}...(后续省略)
```

**输出要求：**
- 直接输出总结
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的文本分析助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        elapsed = time.time() - start_time
        
        if response and hasattr(response, 'choices') and response.choices:
            result = response.choices[0].message.content
            print(f"✓ 响应成功 (耗时: {elapsed:.2f}秒)")
            print(f"  结果: {result}")
        else:
            print(f"⚠️  响应结构异常")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print("\n如果单次请求超过5秒，说明:")
    print("  1. 模型响应慢 - 可能需要更换更快的模型")
    print("  2. Prompt太复杂 - 需要简化提示词")
    print("  3. max_tokens太大 - 可以减小到500-1000")
    print("\n如果36帧每帧需要5秒，总计需要3分钟")
    print("如果加上全局上下文生成(1次)，总计约3-4分钟")


if __name__ == "__main__":
    test_llm_connection()
