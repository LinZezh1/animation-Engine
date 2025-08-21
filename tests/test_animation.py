"""
Mini Animation Engine MVP - Animation Test
测试三角形的位置、旋转、缩放、颜色动画
"""
import pygame as pg
import numpy as np
import math
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.renderer import Renderer
from core.geometry import Triangle
from core.animation import TimeManager, move_to, rotate_to, scale_to, color_to, EaseFunction


def main():
    """动画测试程序"""
    print("=== Mini Animation Engine 动画测试 ===")
    print("即将展示以下动画序列:")
    print("  1. 位置移动动画")
    print("  2. 旋转动画")
    print("  3. 缩放动画")
    print("  4. 颜色渐变动画")
    print("  5. 复合动画（同时进行多种变换）")
    print("按任意键开始...")
    
    # 等待用户输入
    input()
    
    # 创建渲染器
    renderer = Renderer(1200, 800, "Mini Animation Engine - 动画测试")
    
    # 创建时间管理器
    time_manager = TimeManager()
    
    # 创建三角形
    triangle = Triangle.create_equilateral(side_length=1.0, color=(1.0, 0.0, 0.0))
    
    clock = pg.time.Clock()
    
    # 动画序列 1: 位置移动
    print("\n1. 位置移动动画 (3秒)")
    triangle.move_to(-3, 0)  # 起始位置
    time_manager.add_animation(move_to(triangle, (3, 0), 3.0, EaseFunction.ease_in_out))
    
    run_animation_sequence(renderer, time_manager, triangle, clock, "位置移动")
    
    # 等待用户
    print("按任意键继续...")
    input()
    
    # 动画序列 2: 旋转动画
    print("\n2. 旋转动画 (2秒)")
    triangle.move_to(0, 0)  # 重置位置
    triangle.transform.set_rotation(0)  # 重置旋转
    time_manager.add_animation(rotate_to(triangle, 2 * math.pi, 2.0, EaseFunction.ease_in_out))
    
    run_animation_sequence(renderer, time_manager, triangle, clock, "旋转")
    
    # 等待用户
    print("按任意键继续...")
    input()
    
    # 动画序列 3: 缩放动画
    print("\n3. 缩放动画 (2秒)")
    triangle.transform.set_scale(1.0)  # 重置缩放
    triangle.transform.set_rotation(0)  # 重置旋转
    time_manager.add_animation(scale_to(triangle, 3.0, 2.0, EaseFunction.ease_in_out_quad))
    
    run_animation_sequence(renderer, time_manager, triangle, clock, "缩放")
    
    # 等待用户
    print("按任意键继续...")
    input()
    
    # 动画序列 4: 颜色渐变
    print("\n4. 颜色渐变动画 (2秒)")
    triangle.transform.set_scale(1.5)  # 保持适中大小
    triangle.set_color((1.0, 0.0, 0.0))  # 重置为红色
    time_manager.add_animation(color_to(triangle, (0.0, 1.0, 1.0), 2.0, EaseFunction.linear))
    
    run_animation_sequence(renderer, time_manager, triangle, clock, "颜色渐变")
    
    # 等待用户
    print("按任意键继续...")
    input()
    
    # 动画序列 5: 复合动画
    print("\n5. 复合动画 (4秒)")
    triangle.move_to(-2, -2)
    triangle.transform.set_rotation(0)
    triangle.transform.set_scale(0.5)
    triangle.set_color((1.0, 0.0, 0.0))
    
    # 同时执行多个动画
    time_manager.add_animation(move_to(triangle, (2, 2), 4.0, EaseFunction.ease_in_out))
    time_manager.add_animation(rotate_to(triangle, 4 * math.pi, 4.0, EaseFunction.linear))
    time_manager.add_animation(scale_to(triangle, 2.0, 4.0, EaseFunction.ease_out_quad))
    time_manager.add_animation(color_to(triangle, (0.2, 0.8, 1.0), 4.0, EaseFunction.ease_in_quad))
    
    run_animation_sequence(renderer, time_manager, triangle, clock, "复合动画")
    
    # 最终展示
    print("\n动画序列完成！最终状态展示 3 秒...")
    final_display_time = time.time()
    while time.time() - final_display_time < 3.0:
        if renderer.should_quit():
            break
            
        renderer.clear_screen()
        vertices = triangle.get_vertices()
        renderer.draw_triangle(vertices, triangle.color)
        renderer.present()
        clock.tick(60)
    
    renderer.cleanup()
    print("动画测试完成！")


def run_animation_sequence(renderer, time_manager, triangle, clock, description):
    """运行一个动画序列"""
    start_time = time.time()
    
    while not time_manager.is_all_finished():
        if renderer.should_quit():
            break
            
        # 更新动画
        time_manager.update()
        
        # 渲染
        renderer.clear_screen()
        vertices = triangle.get_vertices()
        renderer.draw_triangle(vertices, triangle.color)
        renderer.present()
        
        clock.tick(60)
    
    elapsed = time.time() - start_time
    print(f"{description}动画完成，耗时: {elapsed:.2f} 秒")
    
    # 清空动画管理器
    time_manager.clear()


if __name__ == "__main__":
    main()