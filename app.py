import gradio as gr

def show_mac_instructions():
    return """## 📥 Installation Instructions for Mac/Linux

1. Open Terminal
2. Run these commands:

```bash
git clone https://huggingface.co/spaces/ethan-codecub/PvP-Battle
cd PvP-Battle
pip3 install pygame
python3 PvP.py
```

That's it! The game will launch. Enjoy! 🎮"""

def show_windows_instructions():
    return """## 📥 Installation Instructions for Windows

1. Open Command Prompt or PowerShell
2. Run these commands:

```bash
git clone https://huggingface.co/spaces/ethan-codecub/PvP-Battle
cd PvP-Battle
pip install pygame
python PvP.py
```

That's it! The game will launch. Enjoy! 🎮"""

game_info = """## 🎯 Game Features
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

def show_mobile_notice():
    return """## 📱 Mobile Version Coming Soon!

This game is currently **desktop-only**, but we're working on a mobile-friendly web version!

### Why Desktop-Only Right Now?

This game uses **Pygame**, which is designed for desktop computers. However, the game includes touch controls (press T in-game), showing it was built with mobile in mind!

### 🚀 Future Mobile Support

We plan to convert this to a **web-based version** that will work on:
- ✅ **Mobile phones** (iOS & Android)
- ✅ **Tablets** (iPad, Android tablets)
- ✅ **Any device with a web browser**

The touch controls are already built-in and ready to go!

### 💡 Want to Play Now?

For now, you'll need a **desktop computer** (Windows, Mac, or Linux) to download and play. Check out the Mac/Linux or Windows buttons above for instructions!

---

**Stay tuned for the mobile web version!** 🎮📱"""

with gr.Blocks() as demo:
    gr.Markdown("# 🎮 PvP Battle Arena")
    gr.Markdown("### A fast-paced 2D battle game with weapons, armor, and online multiplayer!")
    gr.Markdown("*This is a Pygame application that requires a desktop computer. Choose your platform below:*")

    gr.Markdown("## 📥 Choose Your Platform:")

    with gr.Row():
        mac_btn = gr.Button("🍎 Mac/Linux", variant="primary", size="lg")
        windows_btn = gr.Button("🪟 Windows", variant="primary", size="lg")
        mobile_btn = gr.Button("📱 Mobile Device", variant="secondary", size="lg")

    instructions_output = gr.Markdown("")

    mac_btn.click(fn=show_mac_instructions, outputs=instructions_output)
    windows_btn.click(fn=show_windows_instructions, outputs=instructions_output)
    mobile_btn.click(fn=show_mobile_notice, outputs=instructions_output)

    gr.Markdown("---")
    gr.Markdown(game_info)

demo.launch()
