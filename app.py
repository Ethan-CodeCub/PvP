import gradio as gr
import subprocess
import os

def launch_game():
    """Launch the PvP game"""
    return """
    # PvP Battle Arena Game

    To play the game, please run it locally on your computer:

    1. Clone this repository
    2. Install dependencies: `pip install pygame`
    3. Run the game: `python3 PvP.py`

    ## Game Features
    - **VS Player (Local)** - Two players on the same computer
    - **VS AI** - Battle against AI (Easy, Medium, Hard)
    - **Around The World (Online)** - Play with friends across the internet

    ## Controls
    **Player 1:** WASD to move, SPACE to attack
    **Player 2:** Arrow keys to move, IJKL to aim, SHIFT to shoot, ENTER for melee

    Press **T** to toggle touch controls
    Press **ESC** to return to menu

    ## Weapons
    Choose from Sword, Axe, Bow, Magic Wand, or Gun!

    ## Armor Types
    Light (fast), Medium (balanced), or Heavy (tank)

    ---

    **Note:** This is a Pygame application that requires a local display.
    Hugging Face Spaces doesn't support interactive Pygame applications in the browser.
    Please download and run locally for the best experience!

    ### Download Instructions
    ```bash
    git clone https://huggingface.co/spaces/ethan-codecub/PvP-Battle
    cd PvP-Battle
    pip install pygame
    python3 PvP.py
    ```
    """

# Create Gradio interface
with gr.Blocks(title="PvP Battle Arena") as demo:
    gr.Markdown("# 🎮 PvP Battle Arena")
    gr.Markdown("### A fast-paced 2D battle game with weapons, armor, and online multiplayer!")

    game_info = gr.Markdown(launch_game())

    gr.Markdown("---")
    gr.Markdown("🤖 Built with [Claude Code](https://claude.com/claude-code)")

if __name__ == "__main__":
    demo.launch()
