# Mini Animation Engine

一个轻量级动画引擎，类似ManimGL但更简洁。从零构建，展示动画引擎的核心架构。

## 🚀 快速开始

### 安装依赖
```bash
pip install moderngl pygame numpy
```

### 运行演示
```bash
python main.py
```
选择不同的演示和测试程序。

## 📁 项目结构

```
mini_anim_engine/
├── main.py                 # 主入口程序
├── __init__.py            # 包初始化
│
├── core/                  # 核心模块
│   ├── __init__.py       # 核心模块初始化
│   ├── renderer.py       # OpenGL渲染器
│   ├── geometry.py       # 几何对象系统
│   ├── animation.py      # 动画和时间管理
│   └── scene.py          # 场景管理
│
├── tests/                # 测试程序
│   ├── __init__.py      # 测试模块初始化
│   ├── quick_test.py    # 快速验证测试
│   ├── test_basic.py    # 基础功能测试
│   ├── test_interactive.py  # 交互测试
│   └── test_animation.py    # 动画序列测试
│
├── demos/               # 演示程序
│   ├── __init__.py     # 演示模块初始化
│   ├── demo_simple.py  # 简化演示
│   └── demo_final.py   # 完整演示
│
└── docs/               # 文档
    ├── README.md       # 详细说明文档
    └── DEVELOPMENT_SUMMARY.md  # 开发总结
```

## 🎯 核心功能

- ✅ **OpenGL渲染** - 基于ModernGL的高性能渲染
- ✅ **几何对象** - Triangle + Transform系统
- ✅ **动画插值** - 位置、旋转、缩放、颜色动画
- ✅ **时间管理** - 精确的动画时序控制
- ✅ **场景管理** - 多对象场景系统
- ✅ **类ManimGL API** - 熟悉的使用体验

## 📖 使用示例

```python
from core import MiniAnimationEngine, move_to, rotate_to

# 创建引擎
engine = MiniAnimationEngine(1200, 800, "My Animation")

# 创建三角形
triangle = engine.create_equilateral_triangle(2.0, (1.0, 0.0, 0.0))
triangle.move_to(-2, 0)

# 添加到场景
engine.add(triangle)

# 播放动画
engine.play(
    move_to(triangle, (2, 0), 2.0),
    rotate_to(triangle, 3.14, 2.0)
)

# 等待和清理
engine.wait(1.0)
engine.cleanup()
```

## 🎮 运行方式

### 方式1: 主菜单
```bash
python main.py
```
通过交互菜单选择程序。

### 方式2: 直接运行
```bash
# 快速测试
python tests/quick_test.py

# 简化演示
python demos/demo_simple.py

# 交互测试 (WASD移动，QE旋转，RF缩放)
python tests/test_interactive.py
```

## 📊 技术参数

| 指标 | 数值 |
|------|------|
| 代码量 | ~800行 |
| 开发时间 | ~2小时 |
| 渲染性能 | 60 FPS |
| 支持平台 | Windows/Linux/macOS |
| Python版本 | 3.8+ |

## 🏗️ 架构设计

### 核心模块
- **Renderer** - OpenGL渲染和着色器管理
- **Geometry** - 几何对象和变换系统  
- **Animation** - 动画插值和时间控制
- **Scene** - 场景管理和主API

### 技术栈
- **ModernGL** - 现代OpenGL绑定
- **Pygame** - 窗口和事件处理
- **NumPy** - 数值计算和矩阵运算

## 🔧 扩展方向

- [ ] 更多几何形状 (矩形、圆形、多边形)
- [ ] 文本渲染支持
- [ ] 3D渲染能力
- [ ] 视频导出功能
- [ ] 可视化编辑器

## 📄 开源协议

MIT License

---

**🎉 从零到一，构建动画引擎！**