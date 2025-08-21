"""
Quick test to verify the engine works
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import math
from core.scene import MiniAnimationEngine
from core.animation import move_to, rotate_to, scale_to, color_to, EaseFunction

def main():
    print("Mini Animation Engine - Quick Test")
    print("Testing basic functionality...")
    
    # Create engine
    engine = MiniAnimationEngine(800, 600, "Quick Test")
    
    # Create triangle
    triangle = engine.create_equilateral_triangle(1.5, (1.0, 0.0, 0.0))
    triangle.move_to(-2, 0)
    
    engine.add(triangle)
    
    print("Playing simple animations...")
    
    # Test move animation
    engine.play(move_to(triangle, (2, 0), 1.0))
    print("Move animation completed")
    
    # Test rotation animation
    engine.play(rotate_to(triangle, math.pi, 1.0))
    print("Rotation animation completed")
    
    # Test scale animation
    engine.play(scale_to(triangle, 2.0, 1.0))
    print("Scale animation completed")
    
    # Test color animation
    engine.play(color_to(triangle, (0.0, 1.0, 0.0), 1.0))
    print("Color animation completed")
    
    # Show final result
    engine.wait(1.0)
    
    engine.cleanup()
    print("Quick test completed successfully!")

if __name__ == "__main__":
    main()