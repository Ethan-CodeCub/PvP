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
    return """## 📱 Mobile Users - Play on itch.io!

Good news! This game CAN run on mobile devices through **itch.io**!

### 🎮 How Mobile Users Can Play:

**Option 1: Wait for itch.io deployment** (Coming Soon!)
- The developer will upload the web version to itch.io
- You can then play directly in your mobile browser
- No downloads, no terminal, no setup needed!
- Touch controls built-in (press T in-game)

**Option 2: Download on Desktop** (Available Now)
- If you have access to a desktop/laptop computer
- Use the Mac/Linux or Windows buttons above
- Install and play with full features

### Why Can't Mobile Users Download Directly?

Mobile devices (phones/tablets) don't have:
- ❌ Command-line terminals for installation
- ❌ Support for running Python/Pygame natively
- ❌ Keyboard for game controls

### ✅ The Solution: itch.io Web Version

The game will be converted to WebAssembly and hosted on **itch.io**, where:
- ✅ Runs in ANY browser (mobile or desktop)
- ✅ Touch controls already built-in
- ✅ No downloads or setup required
- ✅ Works on iOS, Android, tablets, everything!

---

**Stay tuned! Web version coming to itch.io soon!** 🎮📱

*Developer: See ITCH_IO_DEPLOY.md for deployment instructions*"""

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
