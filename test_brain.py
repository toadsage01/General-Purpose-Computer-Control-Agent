from core.observer import Observer
from core.executor import Executor
from core.brain import Brain
import time

def run_smart_test():
    print("--- GHOST OPERATOR: AI MODE ---")
    
    obs = Observer()
    bot = Executor()
    brain = Brain()

    # 1. Setup
    print("Open CALCULATOR. I will try to multiply 7 by 9.")
    time.sleep(5)

    # 2. Define the Goal
    # We will loop through a sequence of natural language instructions
    instructions = [
        "Click the number 7",
        "Click the multiply button",
        "Click the number 9",
        "Click the equals button"
    ]

    for step in instructions:
        print(f"\n[Goal] {step}")
        
        # A. See (Observer)
        screenshot = obs.capture_screen()
        elements = obs.scan_ui_elements(depth=10) # Scan deep!
        
        # B. Think (Brain)
        print("Thinking...")
        plan = brain.get_next_action(step, elements, screenshot)
        
        if plan:
            print(f"[Plan] AI decided to: {plan}")
            
            # C. Act (Executor)
            if plan['action'] == 'click':
                bot.click(plan['x'], plan['y'])
            elif plan['action'] == 'type':
                bot.type_text(plan['text'])
            
            # Wait for animation
            time.sleep(1.5)
        else:
            print("AI Failed to come up with a plan.")
            break

if __name__ == "__main__":
    run_smart_test()