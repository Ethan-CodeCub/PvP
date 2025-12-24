# Deploy PvP Battle Arena to itch.io

## 🎯 What This Does

This guide helps YOU (the developer) deploy the game to itch.io using your DESKTOP/LAPTOP computer.

Once deployed, ANYONE (including mobile users) can play the game in their browser - no terminal or downloads needed!

---

## ⚠️ Important: You Need a Desktop/Laptop

Mobile users CANNOT follow this guide - they don't have terminals!

**This is for the game DEVELOPER (you) to:**
1. Build the game on your Mac/PC
2. Upload it to itch.io
3. Then mobile users can play it on itch.io without any setup!

---

## Step 1: Build with Pygbag (Desktop Only)

**On your Mac/Windows/Linux computer**, open Terminal and run:

```bash
cd "/Users/mac/Desktop/Ethan/Projects/PvP game"
python3 -m pygbag --build .
```

This will create a `build/web` folder with all the files needed for itch.io.

**Note:** The build might take 2-5 minutes. Wait for it to complete!

## Step 2: Create itch.io Account

1. Go to https://itch.io/register
2. Create a free account
3. Verify your email

## Step 3: Create New Project

1. Go to https://itch.io/game/new
2. Fill in the details:
   - **Title:** PvP Battle Arena
   - **Project URL:** `pvp-battle-arena` (or your choice)
   - **Short description:** "A fast-paced 2D battle game with weapons, armor, and online multiplayer!"
   - **Classification:** Games
   - **Kind of project:** HTML

## Step 4: Upload Your Game

1. Scroll to "Uploads" section
2. Click "Upload files"
3. **ZIP the build/web folder first:**
   ```bash
   cd build
   zip -r pvp-battle-arena.zip web/
   ```
4. Upload `pvp-battle-arena.zip`
5. Check the box "This file will be played in the browser"
6. Set as the **Primary file**

## Step 5: Configure Settings

### Viewport dimensions:
- **Width:** 1280
- **Height:** 720

### Mobile-friendly:
- Check "Mobile friendly"
- Check "Automatically start on page load for HTML5 games"

### Embed options:
- Select "Click to launch in fullscreen"
- OR "Embed in page" (your choice)

## Step 6: Set Pricing & Visibility

1. **Pricing:** Free
2. **Visibility:** Public (or Draft if you want to test first)

## Step 7: Save & Publish

1. Click "Save & view page" at the bottom
2. Your game is now live! 🎉

## Your Game URL

After publishing, your game will be at:
`https://YOUR-USERNAME.itch.io/pvp-battle-arena`

Share this link and anyone can play on:
- 📱 Mobile phones (iOS, Android)
- 💻 Desktop browsers
- 📱 Tablets

## Touch Controls

Players should press **T** in-game to enable touch controls on mobile devices!

## Troubleshooting

### Game doesn't load:
- Make sure you uploaded the ZIP of the `build/web` folder, not individual files
- Check that "This file will be played in the browser" is checked
- Try refreshing the page

### Build failed:
- Make sure Pygbag is installed: `pip3 install pygbag`
- Check that `main.py` exists in your game folder
- Make sure all image files are in the `PvP images/` folder

### Touch controls not working:
- Press **T** key to toggle them on
- Make sure you selected "Mobile friendly" in itch.io settings

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
