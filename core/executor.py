# The Hands : Human-like mouse control

import ctypes
try:
    # This tells Windows: "I know what I'm doing, give me real pixels."
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass # Not on Windows 8+ or already set

import pyautogui
import time
import random
import math

# Safety: Fail-safe feature. Slam mouse to corner to kill script.
pyautogui.FAILSAFE = True 

class Executor:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def _human_curve(self, start_x, start_y, end_x, end_y):
        """
        Generates a random Bezier curve path to look human.
        """
        # Control point for the curve (random offset)
        control_x = random.randint(min(start_x, end_x), max(start_x, end_x))
        control_y = random.randint(min(start_y, end_y), max(start_y, end_y))
        
        # Add some chaos
        control_x += random.randint(-100, 100)
        control_y += random.randint(-100, 100)

        path = []
        steps = 20 # Number of tiny movements
        for t in range(steps + 1):
            t /= steps
            # Quadratic Bezier Formula
            x = (1 - t)**2 * start_x + 2 * (1 - t) * t * control_x + t**2 * end_x
            y = (1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * end_y
            path.append((x, y))
        return path

    def move_to(self, x, y, duration=None):
        """
        Moves mouse to (x, y) using a human-like curve.
        """
        # SAFETY FIX: Force coordinates to be integers
        x = int(x)
        y = int(y)
        
        start_x, start_y = pyautogui.position()
        
        # If duration is not set, calculate based on distance (farther = slower)
        if duration is None:
            dist = math.hypot(x - start_x, y - start_y)
            duration = random.uniform(0.5, 1.0) + (dist / 2000)

        path = self._human_curve(start_x, start_y, x, y)
        
        # Execute the move in small chunks
        step_duration = duration / len(path)
        for point in path:
            pyautogui.moveTo(point[0], point[1], duration=step_duration, tween=pyautogui.easeOutQuad)

    def click(self, x, y):
        self.move_to(x, y)
        time.sleep(random.uniform(0.1, 0.3)) # Micro-pause before clicking
        pyautogui.click()
        print(f"[Executor] Clicked at ({x}, {y})")

    def type_text(self, text):
        """
        Types text with random delays between keystrokes.
        """
        for char in text:
            pyautogui.typewrite(char)
            # Random typing speed (average human: 0.05 - 0.15s per key)
            time.sleep(random.uniform(0.05, 0.15))
        print(f"[Executor] Typed: {text}")

# --- Simple Test Block ---
if __name__ == "__main__":
    bot = Executor()
    # Test: Move mouse to center of screen
    bot.move_to(500, 500)