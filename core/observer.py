import os
import time
import pyautogui
import uiautomation as auto
import ctypes
from datetime import datetime
from PIL import Image, ImageDraw

import ctypes
try:
    # This tells Windows: "I know what I'm doing, give me real pixels."
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass # Not on Windows 8+ or already set

class Observer:
    def __init__(self, output_dir="logs/screenshots"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def capture_screen(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screen_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return filepath

    def scan_ui_elements(self, depth=3):
        window = auto.GetForegroundControl()
        elements = []
        
        def walk(control, current_depth):
            if current_depth > depth: return
            if control.Name and not control.IsOffscreen:
                rect = control.BoundingRectangle
                # Calculate center
                x = (rect.left + rect.right) // 2
                y = (rect.top + rect.bottom) // 2
                
                elements.append({
                    "name": control.Name,
                    "type": control.ControlTypeName,
                    "x": x,
                    "y": y,
                    "rect": [rect.left, rect.top, rect.right, rect.bottom] # Save rect for drawing
                })
            for child in control.GetChildren():
                walk(child, current_depth + 1)

        walk(window, 0)
        return elements

    def draw_debug_boxes(self, screenshot_path, elements):
        """
        Draws red boxes around detected elements to verify accuracy.
        """
        try:
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)
            
            for el in elements:
                # Draw box: [left, top, right, bottom]
                r = el['rect']
                draw.rectangle([r[0], r[1], r[2], r[3]], outline="red", width=2)
                # Draw center point
                draw.ellipse([el['x']-3, el['y']-3, el['x']+3, el['y']+3], fill="blue")

            # Save as a debug file
            debug_path = screenshot_path.replace(".png", "_debug.png")
            image.save(debug_path)
            print(f"[Observer] Debug map saved: {debug_path}")
        except Exception as e:
            print(f"[Observer] Failed to draw debug boxes: {e}")