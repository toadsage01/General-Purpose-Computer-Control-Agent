# General Purpose Computer Control Agent (GPCCA)

A modular, autonomous agent framework designed to interact with GUI elements using Vision-Language Models (VLMs). The system utilizes a "See-Think-Act" loop to perceive screen state via OS-level accessibility trees and visual snapshots, then executes human-like input commands.

## 🚧 Project Status: Alpha Prototype

### Core Modules
- **Observer (Eyes):** Hybrid detection system using `uiautomation` for DOM/Accessibility tree parsing and `PIL` for visual verification. Includes custom DPI-aware coordinate mapping.
- **Intelligence (Brain):** Integrated with Groq (`llama-4-scout`) for high-speed, low-latency visual reasoning.
- **Executor (Hands):** Implements Bezier curve mouse movements to simulate human interaction patterns and evade bot-detection heuristics.

### Technical Challenges & Solutions
During the initial prototype phase, several architectural hurdles were addressed:

1.  **DPI Scaling Drift:** * *Challenge:* High-DPI Windows environments caused coordinate offsets between the accessibility tree and the physical cursor position.
    * *Solution:* Implemented `ctypes` DPI awareness to enforce 1:1 pixel mapping.
2.  **LLM Hallucinations:**
    * *Challenge:* Vision models occasionally return normalized (float) coordinates or sub-pixel values, causing executor crashes.
    * *Solution:* Built a robust clamping and type-enforcement layer in the Executor to handle non-deterministic outputs gracefully.
3.  **Inference Latency:**
    * *Challenge:* Initial tests with Gemini 2.0 Flash exhibited resource exhaustion limits during tight automation loops.
    * *Solution:* Migrated inference backend to Groq's LPU infrastructure, significantly reducing "Think" time.

## Roadmap
- [ ] Implement state management to handle multi-step workflows across applications.
- [ ] Integrate "Taggr" application wrapper for external task ingestion.
- [ ] Add visual feedback overlays for real-time debugging.

## Setup
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your `GROQ_API_KEY`.
4. Run the test agent: `python test_brain.py`
