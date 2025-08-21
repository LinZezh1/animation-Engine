"""
Mini Animation Engine MVP - Scene Module
场景管理系统，管理多个几何对象和动画
"""
from typing import List, Optional
import time
from .renderer import Renderer
from .geometry import Triangle
from .animation import TimeManager, Animation


class Scene:
    """场景类 - 管理多个几何对象和动画播放"""
    
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.objects: List[Triangle] = []
        self.time_manager = TimeManager()
        self.background_color = (0.2, 0.2, 0.2, 1.0)
        
    def add(self, *objects):
        """添加对象到场景"""
        for obj in objects:
            if obj not in self.objects:
                self.objects.append(obj)
        return self
        
    def remove(self, *objects):
        """从场景中移除对象"""
        for obj in objects:
            if obj in self.objects:
                self.objects.remove(obj)
        return self
        
    def clear(self):
        """清空场景中的所有对象"""
        self.objects.clear()
        self.time_manager.clear()
        
    def play(self, *animations: Animation, run_time: Optional[float] = None):
        """播放动画序列"""
        # 添加动画到时间管理器
        for animation in animations:
            self.time_manager.add_animation(animation)
        
        # 如果指定了运行时间，等待指定时间
        if run_time is not None:
            start_time = time.time()
            while time.time() - start_time < run_time:
                if self.renderer.should_quit():
                    break
                self._update_and_render()
        else:
            # 等待所有动画完成
            while not self.time_manager.is_all_finished():
                if self.renderer.should_quit():
                    break
                self._update_and_render()
                
        # 清空动画队列
        self.time_manager.clear()
        
    def wait(self, duration: float = 1.0):
        """等待指定时间（类似ManimGL的wait）"""
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.renderer.should_quit():
                break
            self._update_and_render()
            
    def render_static(self, duration: float = float('inf')):
        """静态渲染场景（不播放动画）"""
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.renderer.should_quit():
                break
            self._render_frame()
            
    def _update_and_render(self):
        """更新动画并渲染一帧"""
        self.time_manager.update()
        self._render_frame()
        
    def _render_frame(self):
        """渲染一帧"""
        # 清空屏幕
        self.renderer.clear_screen()
        
        # 渲染所有对象
        for obj in self.objects:
            vertices = obj.get_vertices()
            self.renderer.draw_triangle(vertices, obj.color)
            
        # 显示到屏幕
        self.renderer.present()
        
        # 控制帧率
        import pygame as pg
        pg.time.Clock().tick(60)
        
    def set_background_color(self, color):
        """设置背景颜色"""
        self.background_color = color
        self.renderer.clear_color = color
        return self
        
    def get_objects(self) -> List[Triangle]:
        """获取场景中的所有对象"""
        return self.objects.copy()
        
    def get_object_count(self) -> int:
        """获取对象数量"""
        return len(self.objects)
        
    def is_empty(self) -> bool:
        """检查场景是否为空"""
        return len(self.objects) == 0


class MiniAnimationEngine:
    """Mini Animation Engine 主类 - 类似ManimGL的Scene基类"""
    
    def __init__(self, width: int = 1200, height: int = 800, title: str = "Mini Animation Engine"):
        self.renderer = Renderer(width, height, title)
        self.scene = Scene(self.renderer)
        
    def add(self, *objects):
        """添加对象到场景"""
        return self.scene.add(*objects)
        
    def remove(self, *objects):
        """从场景移除对象"""
        return self.scene.remove(*objects)
        
    def play(self, *animations, run_time: Optional[float] = None):
        """播放动画"""
        return self.scene.play(*animations, run_time=run_time)
        
    def wait(self, duration: float = 1.0):
        """等待"""
        return self.scene.wait(duration)
        
    def clear(self):
        """清空场景"""
        return self.scene.clear()
        
    def show(self, duration: float = 5.0):
        """显示静态场景"""
        self.scene.render_static(duration)
        
    def cleanup(self):
        """清理资源"""
        self.renderer.cleanup()
        
    def set_background_color(self, color):
        """设置背景颜色"""
        return self.scene.set_background_color(color)
        
    # 便捷的几何对象创建方法
    @staticmethod
    def create_triangle(vertices=None, color=(1.0, 0.0, 0.0)):
        """创建三角形"""
        return Triangle(vertices, color)
        
    @staticmethod
    def create_equilateral_triangle(side_length=2.0, color=(1.0, 0.0, 0.0)):
        """创建等边三角形"""
        return Triangle.create_equilateral(side_length, color)
        
    @staticmethod
    def create_right_triangle(width=2.0, height=2.0, color=(0.0, 1.0, 0.0)):
        """创建直角三角形"""
        return Triangle.create_right_triangle(width, height, color)


if __name__ == "__main__":
    # 测试代码
    print("场景管理系统测试:")
    
    # 创建引擎
    engine = MiniAnimationEngine(title="Scene Test")
    
    # 创建几何对象
    triangle1 = engine.create_equilateral_triangle(1.5, (1.0, 0.0, 0.0))
    triangle2 = engine.create_equilateral_triangle(1.0, (0.0, 1.0, 0.0))
    triangle3 = engine.create_right_triangle(1.5, 1.8, (0.0, 0.0, 1.0))
    
    # 设置位置
    triangle1.move_to(-2, 0)
    triangle2.move_to(0, 0) 
    triangle3.move_to(2, 0)
    
    # 添加到场景
    engine.add(triangle1, triangle2, triangle3)
    
    print(f"场景中对象数量: {engine.scene.get_object_count()}")
    print("显示静态场景 3 秒...")
    
    # 显示场景
    engine.show(3.0)
    
    # 清理
    engine.cleanup()
    print("场景管理系统测试完成!")