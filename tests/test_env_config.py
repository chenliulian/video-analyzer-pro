#!/usr/bin/env python3
"""
测试 .env 配置是否正确加载
"""
import os
from dotenv import load_dotenv

print("=" * 70)
print("测试 .env 配置加载")
print("=" * 70)

# 加载 .env 文件
print("\n1. 尝试加载 .env 文件...")
if os.path.exists('.env'):
    print("   ✓ .env 文件存在")
    load_dotenv()
    print("   ✓ .env 文件已加载")
else:
    print("   ✗ .env 文件不存在")
    print("   提示: 运行 'cp .env.example .env' 创建配置文件")

# 检查配置项
print("\n2. 检查配置项...")
configs = {
    'LLM_API_KEY': os.getenv('LLM_API_KEY'),
    'LLM_BASE_URL': os.getenv('LLM_BASE_URL'),
    'LLM_MODEL': os.getenv('LLM_MODEL'),
}

all_ok = True
for key, value in configs.items():
    if value:
        # 隐藏API密钥的大部分内容
        if 'KEY' in key and len(value) > 10:
            display_value = value[:10] + '...'
        else:
            display_value = value
        print(f"   ✓ {key}: {display_value}")
    else:
        print(f"   ✗ {key}: 未设置")
        all_ok = False

# 测试LLM Agent初始化
print("\n3. 测试LLM Agent初始化...")
try:
    from llm_agent import TextRefineAgent
    agent = TextRefineAgent()
    
    if agent.client:
        print("   ✓ LLM Agent初始化成功")
        print(f"   ✓ 使用模型: {agent.model}")
        if agent.base_url:
            print(f"   ✓ API地址: {agent.base_url}")
    else:
        print("   ✗ LLM Agent初始化失败（未设置API密钥）")
        all_ok = False
except Exception as e:
    print(f"   ✗ 初始化出错: {e}")
    all_ok = False

# 总结
print("\n" + "=" * 70)
if all_ok:
    print("✅ 配置测试通过！可以正常使用Pro版功能")
else:
    print("❌ 配置不完整，请检查 .env 文件")
    print("\n解决方案:")
    print("1. 运行: cp .env.example .env")
    print("2. 编辑 .env 文件，填入你的API配置")
    print("3. 参考 CONFIG_GUIDE.md 获取详细帮助")
print("=" * 70)
