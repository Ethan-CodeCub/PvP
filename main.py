# Pygbag/WebAssembly compatible version of PvP Battle Arena
# This is the entry point for the web version

import asyncio
import sys

# Import everything from the original game
from PvP import *

async def main():
    """Main async function for Pygbag/web compatibility"""
    game = PvPGame()

    # Async game loop - required for Pygbag
    while game.running:
        game.handle_events()
        game.update()
        game.draw()
        game.clock.tick(FPS)

        # CRITICAL: Yield control back to browser
        # This allows the browser to handle events and render
        await asyncio.sleep(0)

    pygame.quit()

# Auto-start when loaded in browser
asyncio.run(main())
