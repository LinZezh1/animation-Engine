"""
Mini Animation Engine - Core Module
核心模块，包含所有基础功能
"""

from .renderer import Renderer
from .geometry import Triangle, Transform
from .animation import (
    Animation, TransformAnimation, ColorAnimation, TimeManager,
    EaseFunction, move_to, rotate_to, scale_to, color_to, lerp
)
from .scene import Scene, MiniAnimationEngine

__all__ = [
    # 渲染器
    'Renderer',
    
    # 几何对象
    'Triangle', 'Transform',
    
    # 动画系统
    'Animation', 'TransformAnimation', 'ColorAnimation', 'TimeManager',
    'EaseFunction', 'move_to', 'rotate_to', 'scale_to', 'color_to', 'lerp',
    
    # 场景管理
    'Scene', 'MiniAnimationEngine'
]

__version__ = '1.0.0'
__author__ = 'Mini Animation Engine Team'
__description__ = 'A lightweight animation engine inspired by ManimGL'