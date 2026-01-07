# The Brain: Talks to LLM

import os
import json
import base64
from groq import Groq
from dotenv import load_dotenv

# Load API Key
load_dotenv()

class Brain:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
            
        # Initialize Groq Client
        self.client = Groq(api_key=self.api_key)
        
        # We use the 11B Vision model (Fast & Free Tier friendly)
        self.model_name = "meta-llama/llama-4-scout-17b-16e-instruct"

    def _encode_image(self, image_path):
        """Helper to convert image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_next_action(self, instruction, ui_elements, screenshot_path):
        """
        Decides the next action using Groq Vision.
        """
        
        # 1. Prepare Visuals (Base64)
        try:
            base64_image = self._encode_image(screenshot_path)
            img_url = f"data:image/png;base64,{base64_image}"
        except Exception as e:
            print(f"[Brain] Error processing screenshot: {e}")
            return None

        # 2. Prepare Context (Simplified UI Tree)
        # Llama 3.2 loves structured data
        simplified_ui = [
            {"name": el['name'], "x": el['x'], "y": el['y']} 
            for el in ui_elements if el['name']
        ]

        system_instruction = f"""
        You are a GUI Automation Agent.
        User Goal: "{instruction}"
        
        Visible UI Elements (Name: X, Y):
        {json.dumps(simplified_ui)}
        
        Analyze the screenshot and the UI list. Return the JSON for the next mouse action.
        
        RULES:
        1. Output ONLY JSON.
        2. Format: {{"action": "click", "x": 100, "y": 200, "reason": "..."}} or {{"action": "type", "text": "...", "reason": "..."}}
        3. If you can't see the element, check the UI Elements list for a match.
        """

        try:
            # 3. Call Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": system_instruction},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": img_url
                                }
                            }
                        ],
                    }
                ],
                model=self.model_name,
                temperature=0.1, # Low temperature for precision
                response_format={"type": "json_object"} # Force JSON mode
            )
            
            # 4. Parse Response
            response_content = chat_completion.choices[0].message.content
            return json.loads(response_content)

        except Exception as e:
            print(f"[Brain] Groq Error: {e}")
            return None