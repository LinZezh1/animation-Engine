#!/usr/bin/env python3
"""
Mini Animation Engine - 主入口
选择运行不同的演示和测试
"""

import sys
import os

def main():
    print("=== Mini Animation Engine ===")
    print("选择要运行的程序:")
    print()
    print("演示程序 (Demos):")
    print("  1. 简化演示    - demos/demo_simple.py")
    print("  2. 完整演示    - demos/demo_final.py")
    print()
    print("测试程序 (Tests):")
    print("  3. 快速测试    - tests/quick_test.py")  
    print("  4. 基础测试    - tests/test_basic.py")
    print("  5. 交互测试    - tests/test_interactive.py")
    print("  6. 动画测试    - tests/test_animation.py")
    print()
    print("  0. 退出")
    print()
    
    while True:
        try:
            choice = input("请选择 (0-6): ").strip()
            
            if choice == '0':
                print("退出程序")
                break
            elif choice == '1':
                print("启动简化演示...")
                os.system(f"{sys.executable} demos/demo_simple.py")
            elif choice == '2':
                print("启动完整演示...")
                os.system(f"{sys.executable} demos/demo_final.py")
            elif choice == '3':
                print("启动快速测试...")
                os.system(f"{sys.executable} tests/quick_test.py")
            elif choice == '4':
                print("启动基础测试...")
                os.system(f"{sys.executable} tests/test_basic.py")
            elif choice == '5':
                print("启动交互测试...")
                print("提示: 使用WASD移动，QE旋转，RF缩放，123切换颜色，ESC退出")
                os.system(f"{sys.executable} tests/test_interactive.py")
            elif choice == '6':
                print("启动动画测试...")
                os.system(f"{sys.executable} tests/test_animation.py")
            else:
                print("无效选择，请输入0-6之间的数字")
                continue
                
            print("\n程序运行完成\n")
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"运行出错: {e}")


if __name__ == "__main__":
    main()