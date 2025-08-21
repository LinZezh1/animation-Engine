"""
Basic functionality test
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.scene import MiniAnimationEngine
from core.animation import move_to

# Create engine
engine = MiniAnimationEngine(800, 600, "Basic Test")

# Create and add triangle
triangle = engine.create_equilateral_triangle(1.5, (1.0, 0.0, 0.0))
triangle.move_to(-2, 0)
engine.add(triangle)

print("Starting basic animation test...")

# Simple move animation
engine.play(move_to(triangle, (2, 0), 2.0))

print("Animation completed!")

# Show result for 2 seconds
engine.wait(2.0)

# Cleanup
engine.cleanup()

print("Test completed successfully!")