"""
Mini Animation Engine MVP - Geometry Module
几何对象类，包括Triangle和Transform系统
"""
import numpy as np
import math
from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class Transform:
    """变换类 - 管理位置、旋转、缩放"""
    position: np.ndarray = None
    rotation: float = 0.0  # Z轴旋转角度（弧度）
    scale: np.ndarray = None
    
    def __post_init__(self):
        if self.position is None:
            self.position = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        if self.scale is None:
            self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)
            
    def get_matrix(self) -> np.ndarray:
        """获取4x4变换矩阵"""
        # 平移矩阵
        translation = np.eye(4, dtype=np.float32)
        translation[:3, 3] = self.position
        
        # 旋转矩阵（绕Z轴）
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)
        rotation = np.array([
            [cos_r, -sin_r, 0, 0],
            [sin_r, cos_r, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        # 缩放矩阵
        scale_matrix = np.eye(4, dtype=np.float32)
        scale_matrix[0, 0] = self.scale[0]
        scale_matrix[1, 1] = self.scale[1]
        scale_matrix[2, 2] = self.scale[2]
        
        # 组合变换：先缩放，再旋转，最后平移
        return translation @ rotation @ scale_matrix
        
    def translate(self, dx: float, dy: float, dz: float = 0.0):
        """平移变换"""
        self.position += np.array([dx, dy, dz], dtype=np.float32)
        return self
        
    def rotate(self, angle: float):
        """旋转变换（弧度）"""
        self.rotation += angle
        return self
        
    def scale_by(self, sx: float, sy: float = None, sz: float = None):
        """缩放变换"""
        if sy is None:
            sy = sx
        if sz is None:
            sz = sx
        self.scale *= np.array([sx, sy, sz], dtype=np.float32)
        return self
        
    def set_position(self, x: float, y: float, z: float = 0.0):
        """设置位置"""
        self.position = np.array([x, y, z], dtype=np.float32)
        return self
        
    def set_rotation(self, angle: float):
        """设置旋转角度（弧度）"""
        self.rotation = angle
        return self
        
    def set_scale(self, sx: float, sy: float = None, sz: float = None):
        """设置缩放"""
        if sy is None:
            sy = sx
        if sz is None:
            sz = sx
        self.scale = np.array([sx, sy, sz], dtype=np.float32)
        return self


class Triangle:
    """三角形几何对象"""
    
    def __init__(self, vertices: List[List[float]] = None, color: Tuple[float, float, float] = (1.0, 0.0, 0.0)):
        """初始化三角形
        
        Args:
            vertices: 3x3顶点列表 [[x1,y1,z1], [x2,y2,z2], [x3,y3,z3]]
            color: RGB颜色值
        """
        if vertices is None:
            # 默认单位三角形（指向上方）
            vertices = [
                [0.0,  1.0, 0.0],   # 顶点
                [-1.0, -1.0, 0.0],  # 左下
                [1.0, -1.0, 0.0]    # 右下
            ]
            
        self.original_vertices = np.array(vertices, dtype=np.float32)
        self.color = color
        self.transform = Transform()
        
        # 用于动画的目标值
        self._target_color = None
        self._target_transform = None
        
    def get_vertices(self) -> np.ndarray:
        """获取经过变换的顶点数据"""
        # 将3D顶点转换为齐次坐标
        homogeneous_vertices = np.column_stack([
            self.original_vertices, 
            np.ones(len(self.original_vertices))
        ])
        
        # 应用变换矩阵
        transform_matrix = self.transform.get_matrix()
        transformed = homogeneous_vertices @ transform_matrix.T
        
        # 返回3D坐标
        return transformed[:, :3]
        
    def set_vertices(self, vertices: List[List[float]]):
        """设置新的顶点"""
        self.original_vertices = np.array(vertices, dtype=np.float32)
        return self
        
    def set_color(self, color: Tuple[float, float, float]):
        """设置颜色"""
        self.color = color
        return self
        
    def move_to(self, x: float, y: float, z: float = 0.0):
        """移动到指定位置"""
        self.transform.set_position(x, y, z)
        return self
        
    def shift(self, dx: float, dy: float, dz: float = 0.0):
        """相对移动"""
        self.transform.translate(dx, dy, dz)
        return self
        
    def rotate(self, angle: float):
        """旋转（弧度）"""
        self.transform.rotate(angle)
        return self
        
    def scale(self, factor: float):
        """缩放"""
        self.transform.scale_by(factor)
        return self
        
    def copy(self):
        """创建副本"""
        new_triangle = Triangle(self.original_vertices.tolist(), self.color)
        new_triangle.transform = Transform(
            position=self.transform.position.copy(),
            rotation=self.transform.rotation,
            scale=self.transform.scale.copy()
        )
        return new_triangle
        
    @staticmethod
    def create_equilateral(side_length: float = 2.0, color: Tuple[float, float, float] = (1.0, 0.0, 0.0)):
        """创建等边三角形"""
        height = side_length * math.sqrt(3) / 2
        vertices = [
            [0.0, height * 2/3, 0.0],                    # 顶点
            [-side_length/2, -height * 1/3, 0.0],       # 左下
            [side_length/2, -height * 1/3, 0.0]         # 右下
        ]
        return Triangle(vertices, color)
        
    @staticmethod
    def create_right_triangle(width: float = 2.0, height: float = 2.0, color: Tuple[float, float, float] = (0.0, 1.0, 0.0)):
        """创建直角三角形"""
        vertices = [
            [0.0, height/2, 0.0],        # 顶点
            [-width/2, -height/2, 0.0],  # 左下（直角点）
            [width/2, -height/2, 0.0]    # 右下
        ]
        return Triangle(vertices, color)


if __name__ == "__main__":
    # 测试代码
    print("几何系统测试:")
    
    # 创建基础三角形
    triangle = Triangle()
    print(f"默认三角形顶点: {triangle.original_vertices}")
    print(f"默认颜色: {triangle.color}")
    
    # 测试变换
    triangle.move_to(1.0, 0.5).rotate(math.pi / 4).scale(1.5)
    transformed_vertices = triangle.get_vertices()
    print(f"变换后顶点: {transformed_vertices}")
    
    # 测试等边三角形
    equilateral = Triangle.create_equilateral(side_length=3.0, color=(0.0, 1.0, 0.0))
    print(f"等边三角形顶点: {equilateral.original_vertices}")
    
    # 测试直角三角形
    right_triangle = Triangle.create_right_triangle(width=2.0, height=3.0, color=(0.0, 0.0, 1.0))
    print(f"直角三角形顶点: {right_triangle.original_vertices}")
    
    print("几何系统测试完成!")