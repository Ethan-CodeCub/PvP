import gradio as gr

def get_game_info():
    return """# 🎮 PvP Battle Arena Game

This is a Pygame application that requires a local display. Hugging Face Spaces doesn't support interactive Pygame applications in the browser.

## 📥 Download and Play Locally

```bash
git clone https://huggingface.co/spaces/ethan-codecub/PvP-Battle
cd PvP-Battle
pip install pygame
python3 PvP.py
```

## 🎯 Game Features
- **VS Player (Local)** - Two players on the same computer
- **VS AI** - Battle against AI (Easy, Medium, Hard)
- **Around The World (Online)** - Play with friends across the internet

## 🎮 Controls

### Player 1
- **WASD** - Move (W=Up, S=Down, A=Left, D=Right)
- **SPACE** - Attack

### Player 2
- **Arrow Keys** - Move (↑↓←→)
- **IJKL** - Aim crosshair (I=Up, K=Down, J=Left, L=Right)
- **SHIFT** - Shoot
- **ENTER** - Melee attack

### General
- **T** - Toggle touch controls on/off
- **ESC** - Return to main menu

## ⚔️ Weapons
- **Sword** - Melee, 25 DMG, 150 range
- **Axe** - Melee, 40 DMG, 120 range (slower but powerful)
- **Bow** - Ranged, 20 DMG, 500 range
- **Magic Wand** - Ranged, 30 DMG, 400 range
- **Gun** - Ranged, 35 DMG, 600 range

## 🛡️ Armor Types
- **Light Armor** - 20% damage reduction, 100% speed (agile)
- **Medium Armor** - 40% damage reduction, 90% speed (balanced)
- **Heavy Armor** - 60% damage reduction, 70% speed (tank)

## 💡 Tips
- Melee weapons deal more damage but require you to get close
- Ranged weapons are safer but deal less damage
- Heavy armor protects you but makes you slower
- Healing gems respawn after being collected!

---

🤖 Built with [Claude Code](https://claude.com/claude-code)"""

with gr.Blocks() as demo:
    gr.Markdown("# 🎮 PvP Battle Arena")
    gr.Markdown("A fast-paced 2D battle game with weapons, armor, and online multiplayer!")
    gr.Markdown(get_game_info())

demo.launch()
