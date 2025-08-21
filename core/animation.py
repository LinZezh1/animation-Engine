"""
Mini Animation Engine MVP - Animation Module
动画系统，包括Animation类和时间管理
"""
import time
import math
from typing import Callable, Any, List, Optional
from dataclasses import dataclass
import numpy as np


class EaseFunction:
    """缓动函数集合"""
    
    @staticmethod
    def linear(t: float) -> float:
        """线性插值"""
        return t
        
    @staticmethod
    def ease_in_out(t: float) -> float:
        """缓入缓出（类似ManimGL的smooth函数）"""
        return 3 * t**2 - 2 * t**3
        
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """二次缓入"""
        return t * t
        
    @staticmethod
    def ease_out_quad(t: float) -> float:
        """二次缓出"""
        return 1 - (1 - t) * (1 - t)
        
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """二次缓入缓出"""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - 2 * (1 - t) * (1 - t)


def lerp(start: Any, end: Any, t: float) -> Any:
    """线性插值函数，支持数值、向量、颜色等"""
    if isinstance(start, (int, float)):
        return start + (end - start) * t
    elif isinstance(start, np.ndarray):
        return start + (end - start) * t
    elif isinstance(start, (tuple, list)):
        return type(start)(lerp(s, e, t) for s, e in zip(start, end))
    else:
        # 对于其他类型，尝试直接相加
        try:
            return start + (end - start) * t
        except:
            # 如果无法插值，返回起始值或结束值
            return end if t >= 1.0 else start


class Animation:
    """基础动画类"""
    
    def __init__(
        self,
        target,  # 目标对象
        attribute: str,  # 要改变的属性名
        start_value: Any,  # 起始值
        end_value: Any,  # 结束值
        duration: float,  # 持续时间（秒）
        ease_func: Callable[[float], float] = EaseFunction.ease_in_out
    ):
        self.target = target
        self.attribute = attribute
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.ease_func = ease_func
        
        # 动画状态
        self.start_time = None
        self.is_finished = False
        self.is_started = False
        
    def start(self):
        """开始动画"""
        if not self.is_started:
            self.start_time = time.time()
            self.is_started = True
            # 如果起始值为None，则获取当前值
            if self.start_value is None:
                self.start_value = getattr(self.target, self.attribute)
                # 对于numpy数组，创建副本
                if hasattr(self.start_value, 'copy'):
                    self.start_value = self.start_value.copy()
            
    def update(self) -> bool:
        """更新动画，返回是否完成"""
        if not self.is_started or self.is_finished:
            return self.is_finished
            
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # 计算进度
        if elapsed_time >= self.duration:
            # 动画完成
            progress = 1.0
            self.is_finished = True
        else:
            progress = elapsed_time / self.duration
            
        # 应用缓动函数
        eased_progress = self.ease_func(progress)
        
        # 插值并设置值
        current_value = lerp(self.start_value, self.end_value, eased_progress)
        setattr(self.target, self.attribute, current_value)
        
        return self.is_finished
        
    def reset(self):
        """重置动画"""
        self.start_time = None
        self.is_finished = False
        self.is_started = False


class TransformAnimation(Animation):
    """变换动画类 - 专门用于Transform对象的动画"""
    
    def __init__(
        self,
        target_object,  # 具有transform属性的对象
        transform_type: str,  # 'position', 'rotation', 'scale'
        start_value: Any,
        end_value: Any,
        duration: float,
        ease_func: Callable[[float], float] = EaseFunction.ease_in_out
    ):
        self.target_object = target_object
        self.transform_type = transform_type
        super().__init__(target_object.transform, transform_type, start_value, end_value, duration, ease_func)
        
    def start(self):
        """开始动画 - 重写以确保正确获取起始值"""
        if not self.is_started:
            self.start_time = time.time()
            self.is_started = True
            # 确保起始值类型正确
            current_value = getattr(self.target, self.attribute)
            if self.transform_type == 'rotation':
                # rotation是标量值
                self.start_value = float(current_value)
            else:
                # position和scale是向量
                self.start_value = current_value.copy() if hasattr(current_value, 'copy') else current_value


class ColorAnimation(Animation):
    """颜色动画类"""
    
    def __init__(
        self,
        target,
        start_color: tuple,
        end_color: tuple,
        duration: float,
        ease_func: Callable[[float], float] = EaseFunction.ease_in_out
    ):
        super().__init__(target, 'color', start_color, end_color, duration, ease_func)


class TimeManager:
    """时间管理器 - 管理所有动画的播放"""
    
    def __init__(self):
        self.animations: List[Animation] = []
        self.finished_animations: List[Animation] = []
        
    def add_animation(self, animation: Animation):
        """添加动画到队列"""
        self.animations.append(animation)
        
    def start_all(self):
        """启动所有动画"""
        for animation in self.animations:
            animation.start()
            
    def update(self):
        """更新所有动画"""
        active_animations = []
        
        for animation in self.animations:
            if not animation.is_started:
                animation.start()
                
            finished = animation.update()
            
            if finished:
                self.finished_animations.append(animation)
            else:
                active_animations.append(animation)
                
        self.animations = active_animations
        
    def is_all_finished(self) -> bool:
        """检查是否所有动画都完成了"""
        return len(self.animations) == 0
        
    def clear(self):
        """清空所有动画"""
        self.animations.clear()
        self.finished_animations.clear()
        
    def get_active_count(self) -> int:
        """获取活跃动画数量"""
        return len(self.animations)


# 便捷的动画创建函数

def move_to(target, end_pos: tuple, duration: float = 1.0, ease_func: Callable = EaseFunction.ease_in_out):
    """移动动画"""
    # 起始值将在动画开始时自动获取
    end_pos_array = np.array(list(end_pos) + [0.0] if len(end_pos) == 2 else end_pos, dtype=np.float32)
    return TransformAnimation(target, 'position', None, end_pos_array, duration, ease_func)


def rotate_to(target, end_rotation: float, duration: float = 1.0, ease_func: Callable = EaseFunction.ease_in_out):
    """旋转动画"""
    # 起始值将在动画开始时自动获取
    return TransformAnimation(target, 'rotation', None, float(end_rotation), duration, ease_func)


def scale_to(target, end_scale: float, duration: float = 1.0, ease_func: Callable = EaseFunction.ease_in_out):
    """缩放动画"""
    # 起始值将在动画开始时自动获取
    end_scale_array = np.array([end_scale, end_scale, end_scale], dtype=np.float32)
    return TransformAnimation(target, 'scale', None, end_scale_array, duration, ease_func)


def color_to(target, end_color: tuple, duration: float = 1.0, ease_func: Callable = EaseFunction.ease_in_out):
    """颜色渐变动画"""
    start_color = target.color
    return ColorAnimation(target, start_color, end_color, duration, ease_func)


if __name__ == "__main__":
    # 测试代码
    print("动画系统测试:")
    
    # 创建一个简单的测试对象
    class TestObject:
        def __init__(self):
            self.value = 0.0
            self.color = (1.0, 0.0, 0.0)
    
    test_obj = TestObject()
    
    # 创建动画
    value_animation = Animation(test_obj, 'value', 0.0, 10.0, 2.0)
    color_animation = ColorAnimation(test_obj, (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), 1.5)
    
    # 创建时间管理器
    time_manager = TimeManager()
    time_manager.add_animation(value_animation)
    time_manager.add_animation(color_animation)
    
    print(f"初始值: {test_obj.value}, 初始颜色: {test_obj.color}")
    
    # 模拟动画更新
    start_time = time.time()
    while not time_manager.is_all_finished():
        time_manager.update()
        elapsed = time.time() - start_time
        print(f"时间: {elapsed:.2f}s, 值: {test_obj.value:.2f}, 颜色: ({test_obj.color[0]:.2f}, {test_obj.color[1]:.2f}, {test_obj.color[2]:.2f})")
        time.sleep(0.1)
    
    print(f"最终值: {test_obj.value}, 最终颜色: {test_obj.color}")
    print("动画系统测试完成!")