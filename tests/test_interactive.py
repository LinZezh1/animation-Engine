"""
Mini Animation Engine MVP - 交互测试
测试几何对象与渲染器的结合，支持键盘交互
"""
import pygame as pg
import numpy as np
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.renderer import Renderer
from core.geometry import Triangle


def main():
    """交互式几何对象测试"""
    print("=== Mini Animation Engine 交互测试 ===")
    print("控制说明:")
    print("  WASD     - 移动三角形")
    print("  QE       - 旋转三角形")
    print("  RF       - 缩放三角形")
    print("  123      - 切换颜色 (红/绿/蓝)")
    print("  SPACE    - 重置三角形")
    print("  ESC      - 退出")
    print()
    
    # 创建渲染器
    renderer = Renderer(1200, 800, "Mini Animation Engine - 交互测试")
    
    # 创建三角形对象
    triangle = Triangle.create_equilateral(side_length=1.5, color=(1.0, 0.0, 0.0))
    
    # 设置状态变量
    clock = pg.time.Clock()
    move_speed = 0.1
    rotation_speed = 0.05
    scale_speed = 0.02
    
    # 主循环
    running = True
    while running:
        # 处理事件
        keys = pg.key.get_pressed()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_1:
                    triangle.set_color((1.0, 0.0, 0.0))  # 红色
                    print("颜色: 红色")
                elif event.key == pg.K_2:
                    triangle.set_color((0.0, 1.0, 0.0))  # 绿色
                    print("颜色: 绿色")
                elif event.key == pg.K_3:
                    triangle.set_color((0.0, 0.0, 1.0))  # 蓝色
                    print("颜色: 蓝色")
                elif event.key == pg.K_SPACE:
                    # 重置三角形
                    triangle = Triangle.create_equilateral(side_length=1.5, color=(1.0, 0.0, 0.0))
                    print("三角形已重置")
        
        # 处理连续按键输入
        if keys[pg.K_w]:
            triangle.shift(0, move_speed)
        if keys[pg.K_s]:
            triangle.shift(0, -move_speed)
        if keys[pg.K_a]:
            triangle.shift(-move_speed, 0)
        if keys[pg.K_d]:
            triangle.shift(move_speed, 0)
        if keys[pg.K_q]:
            triangle.rotate(-rotation_speed)
        if keys[pg.K_e]:
            triangle.rotate(rotation_speed)
        if keys[pg.K_r]:
            triangle.scale(1 + scale_speed)
        if keys[pg.K_f]:
            triangle.scale(1 - scale_speed)
        
        # 渲染
        renderer.clear_screen()
        
        # 获取变换后的顶点和变换矩阵
        vertices = triangle.get_vertices()
        
        # 渲染三角形
        renderer.draw_triangle(vertices, triangle.color)
        
        # 显示
        renderer.present()
        clock.tick(60)
    
    # 清理
    renderer.cleanup()
    print("交互测试完成")


if __name__ == "__main__":
    main()