from core.observer import Observer
from core.executor import Executor
import time

def run_test():
    print("--- GHOST OPERATOR V1 TEST ---")
    
    obs = Observer()
    bot = Executor()

    # 1. Give user time to open Calculator
    print("Please open the CALCULATOR app. You have 5 seconds.")
    time.sleep(5)

    # 2. Observe
    window_info = obs.get_active_window_info()
    print(f"Detected Window: {window_info['name']}")

    # 3. Scan for buttons
    elements = obs.scan_ui_elements(depth=15)
    
    # 4. Find the "5" button (Logic usually handled by AI, hardcoded here for test)
    target_button = None
    for el in elements:
        if el['name'] == "Five" or el['name'] == "5":
            target_button = el
            break
    
    if target_button:
        print(f"Target found: {target_button['name']} at ({target_button['x']}, {target_button['y']})")
        
        # 5. Execute Action
        bot.click(target_button['x'], target_button['y'])
        print("Test Passed: Clicked button 5.")
    else:
        print("Test Failed: Could not find button '5'.")
        # Print what we found to debug
        print([e['name'] for e in elements])

if __name__ == "__main__":
    run_test()