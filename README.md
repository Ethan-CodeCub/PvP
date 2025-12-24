---
title: PvP Battle Arena
emoji: 🎮
colorFrom: red
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# PvP Battle Arena

A fast-paced 2D battle arena game with weapons, armor, healing gems, and online multiplayer support!

## Features

### Game Modes
- **VS Player (Local)** - Two players on the same computer
- **VS AI** - Battle against AI with 3 difficulty levels (Easy, Medium, Hard)
- **Around The World (Online)** - Play with friends across the internet

### Weapon System
Choose from 5 unique weapons:
- **Sword** - Melee, 25 DMG, 150 range
- **Axe** - Melee, 40 DMG, 120 range (slower but powerful)
- **Bow** - Ranged, 20 DMG, 500 range
- **Magic Wand** - Ranged, 30 DMG, 400 range
- **Gun** - Ranged, 35 DMG, 600 range

### Armor Types
- **Light Armor** - 20% damage reduction, 100% speed (agile)
- **Medium Armor** - 40% damage reduction, 90% speed (balanced)
- **Heavy Armor** - 60% damage reduction, 70% speed (tank)

### Weapon Modes
- **Melee Only** - Sword & Axe only for fair close-combat
- **Ranged Only** - Bow, Magic & Gun for distance battles
- **Any Weapon** - All weapons available for mixed combat

### Healing System
Find healing gems hidden in caves around the map! Gems restore health and come in 3 colors (red, green, blue).

### Touch Controls
Full mobile support with on-screen controls! Toggle with the "TOUCH ON/OFF" button at the top.

## Controls

### Player 1
- **WASD** - Move (W=Up, S=Down, A=Left, D=Right)
- **SPACE** - Attack (ranged weapons aim with mouse)

### Player 2
- **Arrow Keys** - Move (↑↓←→)
- **ENTER** - Toggle aim mode (for ranged weapons) / Melee attack
- **I, J, K, L** - Aim crosshair (I=Up, K=Down, J=Left, L=Right)
- **SHIFT** - Shoot (while in aim mode)

### General
- **T** - Toggle touch controls on/off
- **ESC** - Return to main menu from anywhere

## Online Multiplayer

### Host a Game
1. Select "AROUND THE WORLD (Online)"
2. Choose "HOST GAME"
3. Share your IP address with your friend
4. Wait for them to connect

### Join a Game
1. Select "AROUND THE WORLD (Online)"
2. Choose "JOIN GAME"
3. Enter your friend's IP address using the on-screen keyboard or physical keyboard
4. Press CONNECT

**Note:** Both players must be on the same network or use port forwarding for internet play.

## Installation

### Requirements
- Python 3.7+
- Pygame

### Setup
```bash
# Clone or download the repository
cd "PvP game"

# Install dependencies
pip install pygame

# Run the game
python3 PvP.py
```

## Game Assets

The game includes custom images for:
- Player characters (red and blue)
- Weapons (sword, bow, axe, magic wand, gun)
- Healing gems (red, green, blue)
- Cave backgrounds

All assets are located in the `PvP images/` directory.

## Tips & Strategies

- **Melee weapons** deal more damage but require you to get close
- **Ranged weapons** are safer but deal less damage
- **Heavy armor** protects you but makes you slower - harder to dodge!
- **Light armor** keeps you fast but more vulnerable
- Healing gems respawn after being collected - remember their locations!
- Use caves as cover and strategic positions
- In melee-only mode, armor choice is critical since you can't keep distance

## Technical Details

- Built with Python & Pygame
- Online multiplayer uses TCP sockets (port 5555)
- JSON serialization for network data
- Event-driven architecture
- Supports both keyboard and touch input

## Credits

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Developed with assistance from Claude Sonnet 4.5
