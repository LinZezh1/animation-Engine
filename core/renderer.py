"""
Mini Animation Engine MVP - Renderer Module
基础渲染器，负责创建OpenGL窗口和基础渲染功能
"""
import moderngl as mgl
import pygame as pg
import numpy as np
from typing import Tuple


class Renderer:
    """基础渲染器类 - 管理OpenGL上下文和基础渲染操作"""
    
    def __init__(self, width: int = 1200, height: int = 800, title: str = "Mini Animation Engine"):
        self.width = width
        self.height = height
        self.title = title
        
        # 初始化pygame和OpenGL
        pg.init()
        pg.display.set_mode((width, height), pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption(title)
        
        # 创建ModernGL上下文
        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.BLEND)
        self.ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA
        
        # 设置清屏颜色（深灰色背景）
        self.clear_color = (0.2, 0.2, 0.2, 1.0)
        
        # 基础着色器程序（用于渲染三角形）
        self.vertex_shader = """
        #version 330 core
        
        layout(location = 0) in vec3 position;
        
        uniform mat4 transform_matrix;
        uniform mat4 projection_matrix;
        
        void main() {
            gl_Position = projection_matrix * transform_matrix * vec4(position, 1.0);
        }
        """
        
        self.fragment_shader = """
        #version 330 core
        
        uniform vec3 color;
        out vec4 fragColor;
        
        void main() {
            fragColor = vec4(color, 1.0);
        }
        """
        
        # 编译着色器程序
        self.program = self.ctx.program(
            vertex_shader=self.vertex_shader,
            fragment_shader=self.fragment_shader
        )
        
        # 设置投影矩阵（正交投影，类似ManimGL的坐标系统）
        self.setup_projection()
        
    def setup_projection(self):
        """设置投影矩阵 - 使用类似ManimGL的坐标系统"""
        # 类似ManimGL：屏幕高度为8个单位，中心为原点
        frame_height = 8.0
        aspect_ratio = self.width / self.height
        frame_width = frame_height * aspect_ratio
        
        # 正交投影矩阵
        left = -frame_width / 2
        right = frame_width / 2
        bottom = -frame_height / 2
        top = frame_height / 2
        near = -10.0
        far = 10.0
        
        projection_matrix = np.array([
            [2/(right-left), 0, 0, -(right+left)/(right-left)],
            [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
            [0, 0, -2/(far-near), -(far+near)/(far-near)],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        self.program['projection_matrix'] = projection_matrix.flatten()
        
    def clear_screen(self):
        """清空屏幕"""
        self.ctx.clear(*self.clear_color)
        
    def draw_triangle(self, vertices: np.ndarray, color: Tuple[float, float, float] = (1.0, 0.0, 0.0), transform_matrix: np.ndarray = None):
        """绘制三角形
        
        Args:
            vertices: 3x3的顶点数组 [[x1,y1,z1], [x2,y2,z2], [x3,y3,z3]]
            color: RGB颜色值
            transform_matrix: 4x4变换矩阵，如果为None则使用单位矩阵
        """
        # 确保顶点数据是正确的格式
        vertices = np.array(vertices, dtype=np.float32).flatten()
        
        # 创建顶点缓冲对象
        vbo = self.ctx.buffer(vertices)
        vao = self.ctx.vertex_array(self.program, [(vbo, '3f', 'position')])
        
        # 设置变换矩阵
        if transform_matrix is None:
            transform_matrix = np.eye(4, dtype=np.float32)
        
        self.program['transform_matrix'] = transform_matrix.flatten()
        self.program['color'] = color
        
        # 渲染三角形
        vao.render()
        
        # 清理资源
        vbo.release()
        vao.release()
        
    def present(self):
        """将渲染结果显示到屏幕"""
        pg.display.flip()
        
    def should_quit(self) -> bool:
        """检查是否应该退出程序"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return True
        return False
        
    def cleanup(self):
        """清理资源"""
        pg.quit()


if __name__ == "__main__":
    # 测试代码：渲染一个红色三角形
    renderer = Renderer()
    
    # 定义三角形顶点（在屏幕中心的小三角形）
    triangle_vertices = np.array([
        [0.0,  1.0, 0.0],   # 顶点
        [-1.0, -1.0, 0.0],  # 左下
        [1.0, -1.0, 0.0]    # 右下
    ], dtype=np.float32)
    
    print("渲染测试：显示红色三角形")
    print("按ESC或关闭窗口退出")
    
    # 主渲染循环
    clock = pg.time.Clock()
    while not renderer.should_quit():
        renderer.clear_screen()
        renderer.draw_triangle(triangle_vertices, color=(1.0, 0.0, 0.0))
        renderer.present()
        clock.tick(60)  # 60 FPS
        
    renderer.cleanup()
    print("渲染测试完成")