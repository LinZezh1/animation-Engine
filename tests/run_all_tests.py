#!/usr/bin/env python3
"""
Run All Tests - 运行所有测试的脚本
"""
import sys
import os
import subprocess
import time

def run_test(test_name, test_file, timeout=10):
    """运行单个测试"""
    print(f"\n{'='*50}")
    print(f"运行测试: {test_name}")
    print(f"文件: {test_file}")
    print(f"{'='*50}")
    
    try:
        # 运行测试，设置超时
        result = subprocess.run(
            [sys.executable, test_file],
            timeout=timeout,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {test_name} - 测试通过")
            if result.stdout:
                print("输出:")
                print(result.stdout[:500])  # 限制输出长度
        else:
            print(f"❌ {test_name} - 测试失败")
            if result.stderr:
                print("错误:")
                print(result.stderr[:500])
                
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} - 测试超时 ({timeout}秒)")
        return False
    except Exception as e:
        print(f"💥 {test_name} - 运行异常: {e}")
        return False

def main():
    """主函数"""
    print("Mini Animation Engine - 自动化测试套件")
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    
    # 测试列表
    tests = [
        ("快速功能测试", "quick_test.py", 8),
        ("基础动画测试", "test_basic.py", 8),
        # 注意: 交互测试和完整动画测试需要人工交互，这里跳过
        # ("交互测试", "test_interactive.py", 15),
        # ("动画序列测试", "test_animation.py", 30),
    ]
    
    # 运行测试
    results = {}
    start_time = time.time()
    
    for test_name, test_file, timeout in tests:
        results[test_name] = run_test(test_name, test_file, timeout)
        time.sleep(1)  # 短暂休息
    
    # 总结
    total_time = time.time() - start_time
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    print(f"总计: {total} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {total - passed} 个")
    print(f"耗时: {total_time:.1f} 秒")
    print()
    
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {status} - {test_name}")
    
    print(f"\n{'='*60}")
    
    if passed == total:
        print("🎉 所有测试通过！Mini Animation Engine 工作正常！")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())