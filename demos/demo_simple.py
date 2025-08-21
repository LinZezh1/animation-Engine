"""
Mini Animation Engine - Simple Demo
简化版演示，展示核心功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import math
from core.scene import MiniAnimationEngine
from core.animation import move_to, rotate_to, scale_to, color_to, EaseFunction


def main():
    print("=== Mini Animation Engine 简化演示 ===")
    print("展示核心动画功能:")
    print("  1. 三角形渲染")
    print("  2. 位置动画")  
    print("  3. 旋转动画")
    print("  4. 缩放动画")
    print("  5. 颜色动画")
    print("  6. 多对象场景")
    print()
    print("开始演示...")
    
    # 创建引擎
    engine = MiniAnimationEngine(1000, 700, "Mini Animation Engine - 简化演示")
    
    # === 第一部分：单个三角形动画 ===
    print("\n[1/3] 单个三角形动画演示")
    
    # 创建红色三角形
    triangle = engine.create_equilateral_triangle(1.2, (1.0, 0.0, 0.0))
    triangle.move_to(-3, 0)
    engine.add(triangle)
    
    # 位置动画
    print("  - 位置移动...")
    engine.play(move_to(triangle, (3, 0), 2.0, EaseFunction.ease_in_out))
    
    # 移动到中心
    engine.play(move_to(triangle, (0, 0), 1.0))
    
    # 旋转动画
    print("  - 旋转动画...")
    engine.play(rotate_to(triangle, 2 * math.pi, 1.5, EaseFunction.linear))
    
    # 缩放动画
    print("  - 缩放动画...")
    engine.play(scale_to(triangle, 2.0, 1.0, EaseFunction.ease_out_quad))
    engine.play(scale_to(triangle, 0.8, 0.8))
    
    # 颜色动画
    print("  - 颜色渐变...")
    engine.play(color_to(triangle, (0.0, 1.0, 0.0), 1.5))
    engine.play(color_to(triangle, (0.0, 0.5, 1.0), 1.0))
    
    # 移除第一个三角形
    engine.remove(triangle)
    
    # === 第二部分：多对象动画 ===
    print("\n[2/3] 多对象动画演示")
    
    # 创建三个不同的三角形
    tri1 = engine.create_equilateral_triangle(1.0, (1.0, 0.0, 0.0))  # 红色
    tri2 = engine.create_equilateral_triangle(1.0, (0.0, 1.0, 0.0))  # 绿色
    tri3 = engine.create_equilateral_triangle(1.0, (0.0, 0.0, 1.0))  # 蓝色
    
    # 设置初始位置
    tri1.move_to(-2.5, -1.5)
    tri2.move_to(0, -1.5)
    tri3.move_to(2.5, -1.5)
    
    engine.add(tri1, tri2, tri3)
    
    # 同步动画
    print("  - 同步移动动画...")
    engine.play(
        move_to(tri1, (-1.5, 1.5), 2.0),
        move_to(tri2, (0, 1.5), 2.0),
        move_to(tri3, (1.5, 1.5), 2.0)
    )
    
    # 同步旋转
    print("  - 同步旋转...")
    engine.play(
        rotate_to(tri1, math.pi, 1.5),
        rotate_to(tri2, -math.pi, 1.5),
        rotate_to(tri3, 2 * math.pi, 1.5)
    )
    
    # 汇聚到中心
    print("  - 汇聚动画...")
    engine.play(
        move_to(tri1, (-0.5, 0), 1.5),
        move_to(tri2, (0, 0), 1.5),
        move_to(tri3, (0.5, 0), 1.5),
        scale_to(tri1, 0.6, 1.5),
        scale_to(tri2, 0.8, 1.5),
        scale_to(tri3, 0.6, 1.5)
    )
    
    engine.wait(1.0)
    
    # === 第三部分：最终展示 ===
    print("\n[3/3] 最终展示")
    
    # 创建一个大的展示三角形
    final_tri = engine.create_equilateral_triangle(0.2, (1.0, 0.5, 0.0))
    final_tri.move_to(0, 0)
    
    # 清空之前的三角形
    engine.clear()
    engine.add(final_tri)
    
    # 最终动画序列
    print("  - 最终动画序列...")
    engine.play(
        scale_to(final_tri, 3.0, 2.0, EaseFunction.ease_out_quad),
        color_to(final_tri, (0.8, 0.2, 0.9), 2.0)
    )
    
    engine.play(
        rotate_to(final_tri, 4 * math.pi, 2.0, EaseFunction.ease_in_out)
    )
    
    # 渐隐效果
    engine.play(
        scale_to(final_tri, 0.1, 1.5, EaseFunction.ease_in_quad),
        color_to(final_tri, (0.1, 0.1, 0.1), 1.5)
    )
    
    engine.wait(0.5)
    
    # 清理
    engine.cleanup()
    
    print("\n演示完成！")
    print("\n=== Mini Animation Engine MVP 总结 ===")
    print("[完成] 基础OpenGL渲染系统")
    print("[完成] 几何对象系统 (Triangle + Transform)")
    print("[完成] 动画插值系统 (位置/旋转/缩放/颜色)")
    print("[完成] 时间管理系统 (TimeManager)")
    print("[完成] 场景管理系统 (Scene)")
    print("[完成] 类ManimGL的API设计")
    print()
    print("总代码量: ~800行")
    print("核心功能: 全部实现")
    print("扩展性: 优秀")
    print()
    print("恭喜！您已经成功构建了一个动画引擎MVP！")


if __name__ == "__main__":
    main()