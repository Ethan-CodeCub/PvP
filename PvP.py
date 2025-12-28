import pygame
import math
import random
import socket
import threading
import json
import time
import os

pygame.init()

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
GREEN = (50, 255, 50)
PURPLE = (200, 50, 255)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# Weapons
WEAPONS = {
    'sword': {'name': 'Sword', 'damage': 25, 'range': 150, 'cooldown': 15, 'color': (192, 192, 192), 'image': 'PvP images/PvP sword.png'},
    'bow': {'name': 'Bow', 'damage': 20, 'range': 500, 'cooldown': 25, 'color': (139, 69, 19), 'projectile': True, 'image': 'PvP images/PvP bow.png'},
    'axe': {'name': 'Axe', 'damage': 40, 'range': 120, 'cooldown': 35, 'color': (100, 100, 100), 'image': 'PvP images/PvP axe.png'},
    'magic': {'name': 'Magic', 'damage': 30, 'range': 400, 'cooldown': 20, 'color': (138, 43, 226), 'projectile': True, 'image': 'PvP images/PvP magic wand.png'},
    'gun': {'name': 'Gun', 'damage': 35, 'range': 600, 'cooldown': 18, 'color': (50, 50, 50), 'projectile': True, 'image': 'PvP images/PvP gun.png'}
}

# Load weapon images
WEAPON_IMAGES = {}
for weapon_key, weapon_data in WEAPONS.items():
    try:
        image_path = os.path.join(SCRIPT_DIR, weapon_data['image'])
        img = pygame.image.load(image_path)
        WEAPON_IMAGES[weapon_key] = pygame.transform.scale(img, (35, 35))
    except Exception as e:
        print(f"Could not load weapon image: {weapon_data['image']} - {e}")
        WEAPON_IMAGES[weapon_key] = None

# Armor
ARMOR_TYPES = {
    'light': {'name': 'Light Armor', 'defense': 0.8, 'speed_mult': 1.0, 'color': (200, 200, 150)},
    'medium': {'name': 'Medium Armor', 'defense': 0.6, 'speed_mult': 0.9, 'color': (150, 150, 150)},
    'heavy': {'name': 'Heavy Armor', 'defense': 0.4, 'speed_mult': 0.7, 'color': (80, 80, 80)}
}

class Projectile:
    def __init__(self, x, y, target_x, target_y, damage, color, owner=None):
        self.x = x
        self.y = y
        self.damage = damage
        self.color = color
        self.radius = 10
        self.owner = owner  # Track who fired this projectile

        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx**2 + dy**2)

        speed = 15
        if dist > 0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0
            self.vy = 0

        self.alive = True
        self.lifetime = 100

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

        if self.lifetime <= 0 or self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius + 3, 2)

class HealingGem:
    # Load gem images once for all instances
    gem_images = []
    images_loaded = False

    @classmethod
    def load_images(cls):
        if not cls.images_loaded:
            gem_paths = [
                'PvP images/PvP gem red.png',
                'PvP images/PvP gem green.png',
                'PvP images/PvP gem blue.png'
            ]
            for path in gem_paths:
                try:
                    image_path = os.path.join(SCRIPT_DIR, path)
                    img = pygame.image.load(image_path)
                    # Scale gem to appropriate size
                    img = pygame.transform.scale(img, (40, 40))
                    cls.gem_images.append(img)
                except Exception as e:
                    print(f"Could not load gem image: {path} - {e}")
            cls.images_loaded = True

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20  # Increased for image size
        self.heal_amount = 30
        self.collected = False
        self.pulse = 0
        self.respawn_timer = 0  # Timer for respawning after collection
        self.respawn_time = random.randint(120, 300)  # 2-5 seconds at 60 FPS

        # Load images if not already loaded
        HealingGem.load_images()

        # Randomly select a gem image
        if HealingGem.gem_images:
            self.image = random.choice(HealingGem.gem_images)
        else:
            self.image = None

    def update(self):
        self.pulse += 0.1

        # Handle respawn timer
        if self.collected:
            self.respawn_timer += 1
            if self.respawn_timer >= self.respawn_time:
                # Respawn the gem
                self.collected = False
                self.respawn_timer = 0
                self.respawn_time = random.randint(120, 300)  # New random respawn time
                # Pick a new random gem image
                if HealingGem.gem_images:
                    self.image = random.choice(HealingGem.gem_images)

    def draw(self, screen):
        if not self.collected:
            if self.image:
                # Draw the gem image with pulsing effect
                pulse_offset = int(math.sin(self.pulse) * 3)
                draw_x = int(self.x - 20)  # Center the 40x40 image
                draw_y = int(self.y - 20 + pulse_offset)
                screen.blit(self.image, (draw_x, draw_y))

                # Add sparkle effect around the gem
                for i in range(4):
                    angle = i * math.pi / 2 + self.pulse
                    sx = self.x + math.cos(angle) * 25
                    sy = self.y + math.sin(angle) * 25 + pulse_offset
                    pygame.draw.circle(screen, YELLOW, (int(sx), int(sy)), 3)
            else:
                # Fallback to original drawing if images didn't load
                pulse_size = int(self.radius + math.sin(self.pulse) * 5)
                pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), pulse_size)
                pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), pulse_size + 2, 2)
                # Sparkle
                for i in range(4):
                    angle = i * math.pi / 2 + self.pulse
                    sx = self.x + math.cos(angle) * 20
                    sy = self.y + math.sin(angle) * 20
                    pygame.draw.circle(screen, YELLOW, (int(sx), int(sy)), 3)

class Cave:
    # Load cave image once for all instances
    cave_image = None

    @classmethod
    def load_image(cls):
        if cls.cave_image is None:
            try:
                image_path = os.path.join(SCRIPT_DIR, 'PvP images/PvP cave.png')
                cls.cave_image = pygame.image.load(image_path)
            except Exception as e:
                print(f"Could not load cave image: PvP images/PvP cave.png - {e}")

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = DARK_GRAY
        self.gems = []

        # Load image if not already loaded
        Cave.load_image()

        # Scale cave image to size
        if Cave.cave_image:
            self.scaled_image = pygame.transform.scale(Cave.cave_image, (width, height))
        else:
            self.scaled_image = None

        # Add healing gems inside
        for i in range(random.randint(2, 4)):
            gx = x + random.randint(30, width - 30)
            gy = y + random.randint(30, height - 30)
            self.gems.append(HealingGem(gx, gy))

    def draw(self, screen):
        # Draw cave image or fallback to ellipse
        if self.scaled_image:
            screen.blit(self.scaled_image, (self.x, self.y))
        else:
            # Fallback to original ellipse drawing
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.ellipse(screen, BLACK, (self.x, self.y, self.width, self.height), 3)

            # Cave text
            font = pygame.font.Font(None, 24)
            text = font.render("CAVE", True, YELLOW)
            screen.blit(text, (self.x + self.width // 2 - 25, self.y + self.height // 2 - 10))

        # Draw gems
        for gem in self.gems:
            gem.draw(screen)

class Player:
    def __init__(self, x, y, color, controls, name, is_ai=False, ai_difficulty='medium', image_path=None):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 70
        self.color = color
        self.name = name
        self.is_ai = is_ai
        self.ai_difficulty = ai_difficulty

        # Load player image if provided
        self.image = None
        if image_path:
            try:
                full_path = os.path.join(SCRIPT_DIR, image_path)
                self.image = pygame.image.load(full_path)
                # Scale image to player size
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except Exception as e:
                print(f"Could not load image: {image_path} - {e}")

        # Stats
        self.health = 100
        self.max_health = 100
        self.base_speed = 6
        self.speed = self.base_speed

        # Equipment
        self.weapon = 'sword'
        self.armor = 'light'
        self.attack_cooldown = 0

        # State
        self.facing_right = True
        self.alive = True
        self.controls = controls

        # AI variables
        self.ai_timer = 0
        self.ai_action = 'idle'
        self.ai_target_x = x
        self.ai_target_y = y
        self.ai_reaction_time = 0  # Delay for AI attacks

    def update(self, keys, caves, opponent=None):
        if not self.alive:
            return

        # Apply armor speed modifier
        armor = ARMOR_TYPES[self.armor]
        self.speed = self.base_speed * armor['speed_mult']

        # AI behavior
        if self.is_ai and opponent:
            self.ai_update(opponent, caves)
            return

        # Movement
        if keys[self.controls['left']]:
            self.x -= self.speed
            self.facing_right = False
        if keys[self.controls['right']]:
            self.x += self.speed
            self.facing_right = True
        if keys[self.controls['up']]:
            self.y -= self.speed
        if keys[self.controls['down']]:
            self.y += self.speed

        # Boundaries
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

        # Cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Check cave for healing gems
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for cave in caves:
            cave_rect = pygame.Rect(cave.x, cave.y, cave.width, cave.height)
            if player_rect.colliderect(cave_rect):
                for gem in cave.gems:
                    if not gem.collected:
                        gem_rect = pygame.Rect(gem.x - gem.radius, gem.y - gem.radius,
                                             gem.radius * 2, gem.radius * 2)
                        if player_rect.colliderect(gem_rect):
                            gem.collected = True
                            self.health = min(self.max_health, self.health + gem.heal_amount)

        # Death check
        if self.health <= 0:
            self.alive = False

    def ai_update(self, opponent, caves):
        """AI behavior - attacks and seeks healing"""
        self.ai_timer += 1

        # Difficulty settings
        if self.ai_difficulty == 'easy':
            decision_delay = 60  # Slower decisions
            health_threshold = 30  # Seeks healing earlier
            accuracy = 0.6  # 60% chance to make optimal move
        elif self.ai_difficulty == 'medium':
            decision_delay = 30
            health_threshold = 50
            accuracy = 0.8
        else:  # hard
            decision_delay = 15  # Fast decisions
            health_threshold = 70  # Aggressive, rarely heals
            accuracy = 1.0  # Always optimal

        # Decide action based on difficulty
        if self.ai_timer % decision_delay == 0:
            # Check if need healing (based on difficulty threshold)
            if self.health < health_threshold:
                # Find nearest cave with gems
                nearest_cave = None
                min_dist = float('inf')
                for cave in caves:
                    for gem in cave.gems:
                        if not gem.collected:
                            dist = math.sqrt((self.x - gem.x)**2 + (self.y - gem.y)**2)
                            if dist < min_dist:
                                min_dist = dist
                                nearest_cave = gem

                if nearest_cave:
                    self.ai_action = 'heal'
                    self.ai_target_x = nearest_cave.x
                    self.ai_target_y = nearest_cave.y
                else:
                    self.ai_action = 'attack'
            else:
                self.ai_action = 'attack'

        # Execute action
        if self.ai_action == 'heal':
            # Move towards healing target
            dx = self.ai_target_x - self.x
            dy = self.ai_target_y - self.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist > 10:
                # Slower movement on easy
                move_speed = self.speed * (0.7 if self.ai_difficulty == 'easy' else 1.0)
                if abs(dx) > 5:
                    self.x += move_speed if dx > 0 else -move_speed
                if abs(dy) > 5:
                    self.y += move_speed if dy > 0 else -move_speed
            else:
                self.ai_action = 'attack'

        elif self.ai_action == 'attack':
            # Calculate distance to opponent
            dx = opponent.x - self.x
            dy = opponent.y - self.y
            dist = math.sqrt(dx**2 + dy**2)

            weapon = WEAPONS[self.weapon]
            optimal_range = weapon['range'] * 0.8

            # Apply accuracy - sometimes make mistakes on easy/medium
            if random.random() > accuracy:
                # Make a mistake - move in random direction
                dx = random.choice([-1, 1]) * 50
                dy = random.choice([-1, 1]) * 50

            # Slower movement on easy
            move_speed = self.speed * (0.7 if self.ai_difficulty == 'easy' else 1.0)

            # Move towards or away to maintain optimal range
            if dist > optimal_range + 50:
                # Too far, move closer
                if abs(dx) > 10:
                    self.x += move_speed if dx > 0 else -move_speed
                if abs(dy) > 10:
                    self.y += move_speed if dy > 0 else -move_speed
            elif dist < optimal_range - 50 and not weapon.get('projectile', False):
                # Too close for melee, back up
                if abs(dx) > 10:
                    self.x -= move_speed if dx > 0 else -move_speed
                if abs(dy) > 10:
                    self.y -= move_speed if dy > 0 else -move_speed

            # Face opponent
            self.facing_right = dx > 0

        # Boundaries
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

        # Cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Check cave for healing gems
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for cave in caves:
            cave_rect = pygame.Rect(cave.x, cave.y, cave.width, cave.height)
            if player_rect.colliderect(cave_rect):
                for gem in cave.gems:
                    if not gem.collected:
                        gem_rect = pygame.Rect(gem.x - gem.radius, gem.y - gem.radius,
                                             gem.radius * 2, gem.radius * 2)
                        if player_rect.colliderect(gem_rect):
                            gem.collected = True
                            self.health = min(self.max_health, self.health + gem.heal_amount)

        # Death check for AI
        if self.health <= 0:
            self.alive = False

    def attack(self, target_x, target_y):
        if self.attack_cooldown > 0 or not self.alive:
            return None

        weapon = WEAPONS[self.weapon]
        self.attack_cooldown = weapon['cooldown']

        if weapon.get('projectile', False):
            return Projectile(
                self.x + self.width // 2,
                self.y + self.height // 2,
                target_x, target_y,
                weapon['damage'],
                weapon['color'],
                owner=self  # Pass owner when creating projectile
            )
        else:
            # Melee range check
            dx = target_x - (self.x + self.width // 2)
            dy = target_y - (self.y + self.height // 2)
            dist = math.sqrt(dx**2 + dy**2)
            if dist <= weapon['range']:
                return 'melee_hit'
        return None

    def take_damage(self, damage):
        # Apply armor defense
        armor = ARMOR_TYPES[self.armor]
        actual_damage = int(damage * armor['defense'])
        self.health -= actual_damage

    def draw(self, screen):
        if not self.alive:
            pygame.draw.rect(screen, GRAY, (self.x, self.y + 50, self.width, 20))
            font = pygame.font.Font(None, 24)
            text = font.render("DEAD", True, RED)
            screen.blit(text, (self.x, self.y + 25))
            return

        # Draw player image or fallback to rectangle
        if self.image:
            # Flip image if facing left
            image_to_draw = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
            screen.blit(image_to_draw, (self.x, self.y))
        else:
            # Fallback to original rectangle drawing
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 3)

            # Armor overlay
            armor = ARMOR_TYPES[self.armor]
            pygame.draw.rect(screen, armor['color'], (self.x + 5, self.y + 5, self.width - 10, 20))

            # Face
            eye_x = self.x + (35 if self.facing_right else 15)
            pygame.draw.circle(screen, WHITE, (eye_x, int(self.y + 20)), 5)

        # Weapon
        weapon = WEAPONS[self.weapon]
        weapon_img = WEAPON_IMAGES.get(self.weapon)

        if weapon_img:
            # Position weapon to the side of the player
            weapon_x = self.x + (self.width - 5) if self.facing_right else self.x - 30
            weapon_y = self.y + 20

            # Flip weapon if facing left
            weapon_to_draw = weapon_img if self.facing_right else pygame.transform.flip(weapon_img, True, False)
            screen.blit(weapon_to_draw, (weapon_x, weapon_y))
        else:
            # Fallback to rectangle
            weapon_x = self.x + (self.width if self.facing_right else -35)
            weapon_y = self.y + 30
            if weapon.get('projectile', False):
                pygame.draw.rect(screen, weapon['color'], (weapon_x, weapon_y, 30, 8))
            else:
                pygame.draw.rect(screen, weapon['color'], (weapon_x, weapon_y, 28, 10))

        # Health bar
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 5, self.y - 25, self.width + 10, 12))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 23, int(self.width * health_percent), 8))

        # Cooldown bar
        if self.attack_cooldown > 0:
            cooldown_percent = self.attack_cooldown / WEAPONS[self.weapon]['cooldown']
            pygame.draw.rect(screen, YELLOW, (self.x, self.y - 15, int(self.width * (1 - cooldown_percent)), 4))

        # Name
        font = pygame.font.Font(None, 22)
        name_text = font.render(self.name, True, WHITE)
        screen.blit(name_text, (self.x, self.y - 45))

class TouchButton:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.pressed = False

    def draw(self, screen, font):
        # Draw button with transparency and better visual feedback
        s = pygame.Surface((self.rect.width, self.rect.height))
        if self.pressed:
            s.set_alpha(220)  # More opaque when pressed
            s.fill((255, 255, 100))  # Bright yellow when pressed
        else:
            s.set_alpha(150)
            s.fill(self.color)
        screen.blit(s, (self.rect.x, self.rect.y))

        # Draw border - thicker when pressed
        border_width = 3 if self.pressed else 2
        pygame.draw.rect(screen, WHITE, self.rect, border_width)

        # Draw text
        text_surf = font.render(self.text, True, BLACK if self.pressed else WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)

class PvPGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PvP Battle Arena - With Armor & Healing!")
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = 'menu'
        self.player1 = None
        self.player2 = None
        self.projectiles = []
        self.caves = []

        # Touch controls
        self.show_touch_controls = False
        self.touch_buttons = {
            'p1_left': TouchButton(20, SCREEN_HEIGHT - 180, 60, 60, '←', BLUE),
            'p1_right': TouchButton(90, SCREEN_HEIGHT - 180, 60, 60, '→', BLUE),
            'p1_up': TouchButton(55, SCREEN_HEIGHT - 250, 60, 60, '↑', BLUE),
            'p1_down': TouchButton(55, SCREEN_HEIGHT - 110, 60, 60, '↓', BLUE),
            'p1_attack': TouchButton(20, SCREEN_HEIGHT - 330, 130, 60, 'ATTACK', RED),

            'p2_left': TouchButton(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 180, 60, 60, '←', BLUE),
            'p2_right': TouchButton(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 180, 60, 60, '→', BLUE),
            'p2_up': TouchButton(SCREEN_WIDTH - 115, SCREEN_HEIGHT - 250, 60, 60, '↑', BLUE),
            'p2_down': TouchButton(SCREEN_WIDTH - 115, SCREEN_HEIGHT - 110, 60, 60, '↓', BLUE),
            'p2_attack': TouchButton(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 330, 130, 60, 'ATTACK', RED),
        }

        # Toggle button for touch controls (always visible)
        self.touch_toggle_button = TouchButton(SCREEN_WIDTH // 2 - 75, 10, 150, 40, 'TOUCH ON/OFF', PURPLE)

        # On-screen keyboard for IP entry
        self.keyboard_buttons = []
        self.create_keyboard()

        # Menu touch buttons
        self.menu_buttons = []
        self.create_menu_buttons()

        # Setup touch buttons (for weapon mode, weapons, armor, etc.)
        self.setup_buttons = []
        self.last_setup_phase = None  # Track which phase buttons were created for

        self.font = pygame.font.Font(None, 56)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)

        # Selections
        self.game_mode = '2p'  # '2p', 'ai', or 'online'
        self.weapon_mode = 'any'  # 'melee_only', 'ranged_only', 'any'
        self.ai_difficulty = 'medium'  # 'easy', 'medium', 'hard'
        self.p1_weapon = 'sword'
        self.p1_armor = 'light'
        self.p2_weapon = 'sword'
        self.p2_armor = 'light'
        self.select_phase = 'mode'

        # Online multiplayer
        self.online_mode = None  # 'host' or 'join'
        self.connection = None
        self.socket = None
        self.connected = False
        self.host_ip = ''
        self.network_thread = None
        self.received_data = None

        # Player 2 aiming system
        self.p2_aiming = False
        self.p2_aim_x = SCREEN_WIDTH // 2
        self.p2_aim_y = SCREEN_HEIGHT // 2

    def create_keyboard(self):
        """Create on-screen keyboard for IP entry"""
        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
        button_width = 80
        button_height = 60
        spacing = 10
        start_x = SCREEN_WIDTH // 2 - (len(keys) // 2) * (button_width + spacing) // 2
        start_y = 500

        for i, key in enumerate(keys):
            x = start_x + i * (button_width + spacing)
            btn = TouchButton(x, start_y, button_width, button_height, key, DARK_GRAY)
            self.keyboard_buttons.append(btn)

        # Add special buttons
        backspace_btn = TouchButton(start_x, start_y + 80, 120, button_height, 'BACK', RED)
        self.keyboard_buttons.append(backspace_btn)

        connect_btn = TouchButton(start_x + 140, start_y + 80, 200, button_height, 'CONNECT', GREEN)
        self.keyboard_buttons.append(connect_btn)

        cancel_btn = TouchButton(start_x + 360, start_y + 80, 120, button_height, 'CANCEL', GRAY)
        self.keyboard_buttons.append(cancel_btn)

    def create_menu_buttons(self):
        """Create touch buttons for main menu"""
        button_width = 400
        button_height = 70
        start_x = SCREEN_WIDTH // 2 - button_width // 2

        # VS Player button (Local)
        vs_player_btn = TouchButton(start_x, 450, button_width, button_height, 'VS PLAYER (Local)', RED)
        self.menu_buttons.append(vs_player_btn)

        # VS AI button
        vs_ai_btn = TouchButton(start_x, 540, button_width, button_height, 'VS AI', BLUE)
        self.menu_buttons.append(vs_ai_btn)

        # Around the World button (Online)
        online_btn = TouchButton(start_x, 630, button_width, button_height, 'AROUND THE WORLD (Online)', GREEN)
        self.menu_buttons.append(online_btn)

    def create_setup_buttons(self, phase, count, colors=None):
        """Create touch buttons for setup screens dynamically"""
        self.setup_buttons = []
        button_width = 500
        button_height = 70
        start_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = 250

        if colors is None:
            colors = [BLUE] * count

        for i in range(count):
            y = start_y + i * 150
            btn = TouchButton(start_x, y, button_width, button_height, f"Option {i+1}", colors[i])
            self.setup_buttons.append(btn)

    def create_world(self):
        # Create caves with healing gems
        self.caves = [
            Cave(100, 100, 200, 150),
            Cave(SCREEN_WIDTH - 300, 100, 200, 150),
            Cave(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 200, 200, 150),
            Cave(50, SCREEN_HEIGHT // 2 - 75, 180, 150),
            Cave(SCREEN_WIDTH - 230, SCREEN_HEIGHT // 2 - 75, 180, 150)
        ]

    def reset_game(self):
        self.player1 = Player(200, SCREEN_HEIGHT // 2, RED,
                            {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w,
                             'down': pygame.K_s, 'attack': pygame.K_SPACE}, "Player 1",
                            image_path="PvP images/PvP red.png")
        self.player1.weapon = self.p1_weapon
        self.player1.armor = self.p1_armor

        # Create Player 2 (either human or AI)
        is_ai = (self.game_mode == 'ai')
        player2_name = "AI Opponent" if is_ai else "Player 2"

        self.player2 = Player(SCREEN_WIDTH - 250, SCREEN_HEIGHT // 2, BLUE,
                            {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP,
                             'down': pygame.K_DOWN, 'attack': pygame.K_RETURN}, player2_name,
                            is_ai=is_ai, ai_difficulty=self.ai_difficulty,
                            image_path="PvP images/PvP blue.png")
        self.player2.weapon = self.p2_weapon
        self.player2.armor = self.p2_armor

        self.projectiles = []
        self.create_world()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Touch/Mouse controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # Handle menu buttons
                if self.state == 'menu':
                    for i, button in enumerate(self.menu_buttons):
                        if button.is_pressed(pos):
                            button.pressed = True
                            # Handle menu selection
                            if i == 0:  # VS Player (Local)
                                self.game_mode = '2p'
                                self.state = 'setup'
                                self.select_phase = 'weapon_mode'
                            elif i == 1:  # VS AI
                                self.game_mode = 'ai'
                                self.state = 'setup'
                                self.select_phase = 'weapon_mode'
                            elif i == 2:  # Around the World (Online)
                                self.game_mode = 'online'
                                self.state = 'setup'
                                self.select_phase = 'online_mode'

                # Handle setup buttons (weapon mode, difficulty, online mode, etc.)
                if self.state == 'setup' and self.select_phase not in ['enter_ip', 'waiting_for_player']:
                    for i, button in enumerate(self.setup_buttons):
                        if button.is_pressed(pos):
                            button.pressed = True
                            # Handle selection based on how many options
                            self.handle_selection(i)

                # Handle keyboard buttons for IP entry
                if self.state == 'setup' and self.select_phase == 'enter_ip':
                    for i, button in enumerate(self.keyboard_buttons):
                        if button.is_pressed(pos):
                            button.pressed = True
                            # Handle different button types
                            if button.text in '0123456789.':
                                if len(self.host_ip) < 15:
                                    self.host_ip += button.text
                            elif button.text == 'BACK':
                                self.host_ip = self.host_ip[:-1]
                            elif button.text == 'CONNECT':
                                if self.connect_to_host(self.host_ip):
                                    self.select_phase = 'weapon_mode'
                            elif button.text == 'CANCEL':
                                self.state = 'menu'
                                self.host_ip = ''

                # Check toggle button (always available during playing)
                if self.state == 'playing' and self.touch_toggle_button.is_pressed(pos):
                    self.show_touch_controls = not self.show_touch_controls
                    self.touch_toggle_button.pressed = True

                if self.state == 'playing' and self.show_touch_controls:
                    # Check touch button presses
                    for key, button in self.touch_buttons.items():
                        if button.is_pressed(pos):
                            button.pressed = True

                            # Handle attack buttons immediately on press
                            if key == 'p1_attack' and self.player1 and self.player1.alive:
                                weapon = WEAPONS[self.player1.weapon]

                                if weapon.get('projectile', False):
                                    # Projectile weapons aim at opponent
                                    target_x = self.player2.x + self.player2.width // 2
                                    target_y = self.player2.y + self.player2.height // 2
                                    result = self.player1.attack(target_x, target_y)
                                    if isinstance(result, Projectile):
                                        self.projectiles.append(result)
                                else:
                                    # Melee weapons - check if opponent is in range
                                    if self.player1.attack_cooldown == 0:
                                        dx = self.player2.x - self.player1.x
                                        dy = self.player2.y - self.player1.y
                                        dist = math.sqrt(dx**2 + dy**2)

                                        if dist <= weapon['range']:
                                            self.player2.take_damage(weapon['damage'])
                                            self.player1.attack_cooldown = weapon['cooldown']

                            elif key == 'p2_attack' and self.player2 and not self.player2.is_ai and self.player2.alive:
                                weapon = WEAPONS[self.player2.weapon]

                                if weapon.get('projectile', False):
                                    # Projectile weapons aim at opponent
                                    target_x = self.player1.x + self.player1.width // 2
                                    target_y = self.player1.y + self.player1.height // 2
                                    result = self.player2.attack(target_x, target_y)
                                    if isinstance(result, Projectile):
                                        self.projectiles.append(result)
                                else:
                                    # Melee weapons - check if opponent is in range
                                    if self.player2.attack_cooldown == 0:
                                        dx = self.player1.x - self.player2.x
                                        dy = self.player1.y - self.player2.y
                                        dist = math.sqrt(dx**2 + dy**2)

                                        if dist <= weapon['range']:
                                            self.player1.take_damage(weapon['damage'])
                                            self.player2.attack_cooldown = weapon['cooldown']

            if event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos

                # Release menu buttons
                if self.state == 'menu':
                    for button in self.menu_buttons:
                        if button.pressed:
                            button.pressed = False

                # Release setup buttons
                if self.state == 'setup':
                    for button in self.setup_buttons:
                        if button.pressed:
                            button.pressed = False

                # Release keyboard buttons
                if self.state == 'setup' and self.select_phase == 'enter_ip':
                    for button in self.keyboard_buttons:
                        if button.pressed:
                            button.pressed = False

                if self.state == 'playing':
                    # Release toggle button
                    if self.touch_toggle_button.pressed:
                        self.touch_toggle_button.pressed = False

                    if self.show_touch_controls:
                        # Release buttons when touch is lifted
                        for key, button in self.touch_buttons.items():
                            if button.pressed and button.is_pressed(pos):
                                button.pressed = False

            # Handle MOUSEMOTION for detecting when finger moves off button
            if event.type == pygame.MOUSEMOTION:
                if self.state == 'playing' and self.show_touch_controls:
                    # Check if mouse button is still down
                    if pygame.mouse.get_pressed()[0]:
                        pos = event.pos
                        # Release buttons if finger moved away
                        for key, button in self.touch_buttons.items():
                            if button.pressed and not button.is_pressed(pos):
                                button.pressed = False

            if event.type == pygame.KEYDOWN:
                # Toggle touch controls with T key
                if event.key == pygame.K_t:
                    self.show_touch_controls = not self.show_touch_controls
                if self.state == 'menu':
                    if event.key == pygame.K_1:
                        self.game_mode = '2p'
                        self.state = 'setup'
                        self.select_phase = 'weapon_mode'
                    elif event.key == pygame.K_2:
                        self.game_mode = 'ai'
                        self.state = 'setup'
                        self.select_phase = 'weapon_mode'
                    elif event.key == pygame.K_3:
                        self.game_mode = 'online'
                        self.state = 'setup'
                        self.select_phase = 'online_mode'

                elif self.state == 'setup':
                    # ESC key always goes back to menu
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
                        self.host_ip = ''
                        # Clean up any network connections
                        if self.socket:
                            try:
                                self.socket.close()
                            except:
                                pass
                            self.socket = None
                        self.connection = None
                        self.connected = False
                    # IP entry mode
                    elif self.select_phase == 'enter_ip':
                        if event.key == pygame.K_RETURN:
                            # Try to connect
                            if self.connect_to_host(self.host_ip):
                                self.select_phase = 'weapon_mode'
                        elif event.key == pygame.K_BACKSPACE:
                            self.host_ip = self.host_ip[:-1]
                        elif len(self.host_ip) < 15:
                            # Only allow IP-valid characters
                            if event.unicode in '0123456789.':
                                self.host_ip += event.unicode
                    else:
                        # Normal selection handling
                        if event.key == pygame.K_1:
                            self.handle_selection(0)
                        elif event.key == pygame.K_2:
                            self.handle_selection(1)
                        elif event.key == pygame.K_3:
                            self.handle_selection(2)
                        elif event.key == pygame.K_4 and self.select_phase in ['p1_weapon', 'p2_weapon']:
                            self.handle_selection(3)
                        elif event.key == pygame.K_5 and self.select_phase in ['p1_weapon', 'p2_weapon']:
                            self.handle_selection(4)

                elif self.state == 'playing':
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
                        # Clean up any network connections
                        if self.socket:
                            try:
                                self.socket.close()
                            except:
                                pass
                            self.socket = None
                        self.connection = None
                        self.connected = False

                    # Player 1 attack
                    if self.player1 and self.player2 and event.key == self.player1.controls['attack'] and self.player1.alive:
                        weapon = WEAPONS[self.player1.weapon]

                        if weapon.get('projectile', False):
                            # Projectile weapons use mouse for aiming
                            mx, my = pygame.mouse.get_pos()
                            result = self.player1.attack(mx, my)
                            if isinstance(result, Projectile):
                                self.projectiles.append(result)
                        else:
                            # Melee weapons - check if opponent is in range
                            if self.player1.attack_cooldown == 0 and self.player2.alive:
                                dx = self.player2.x - self.player1.x
                                dy = self.player2.y - self.player1.y
                                dist = math.sqrt(dx**2 + dy**2)

                                if dist <= weapon['range']:
                                    self.player2.take_damage(weapon['damage'])
                                    self.player1.attack_cooldown = weapon['cooldown']

                    # Player 2 melee attack (ENTER key for melee weapons only)
                    if self.player1 and self.player2 and not self.player2.is_ai and event.key == self.player2.controls['attack'] and self.player2.alive:
                        weapon = WEAPONS[self.player2.weapon]

                        if not weapon.get('projectile', False):
                            # Melee weapons - check if opponent is in range
                            if self.player2.attack_cooldown == 0 and self.player1.alive:
                                dx = self.player1.x - self.player2.x
                                dy = self.player1.y - self.player2.y
                                dist = math.sqrt(dx**2 + dy**2)

                                if dist <= weapon['range']:
                                    self.player1.take_damage(weapon['damage'])
                                    self.player2.attack_cooldown = weapon['cooldown']

                    # Player 2 shoot (SHIFT key for ranged weapons - always ready)
                    if self.player2 and not self.player2.is_ai and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT) and self.player2.alive:
                        weapon = WEAPONS[self.player2.weapon]
                        if weapon.get('projectile', False):
                            # Ranged weapons shoot at crosshair position
                            result = self.player2.attack(self.p2_aim_x, self.p2_aim_y)
                            if isinstance(result, Projectile):
                                self.projectiles.append(result)

                elif self.state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = 'playing'
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.state = 'menu'

    def handle_selection(self, choice):
        if self.select_phase == 'online_mode':
            modes = ['host', 'join']
            self.online_mode = modes[choice]
            if self.online_mode == 'host':
                self.start_host()
            else:
                self.select_phase = 'enter_ip'
            return
        elif self.select_phase == 'weapon_mode':
            modes = ['melee_only', 'ranged_only', 'any']
            self.weapon_mode = modes[choice]
            # Go to AI difficulty if AI mode, otherwise go to weapon selection
            if self.game_mode == 'ai':
                self.select_phase = 'ai_difficulty'
            else:
                self.select_phase = 'p1_weapon'
        elif self.select_phase == 'ai_difficulty':
            difficulties = ['easy', 'medium', 'hard']
            self.ai_difficulty = difficulties[choice]
            self.select_phase = 'p1_weapon'
        elif self.select_phase == 'p1_weapon':
            # Filter weapons based on weapon mode
            available_weapons = self.get_available_weapons()
            self.p1_weapon = available_weapons[choice]
            self.select_phase = 'p1_armor'
        elif self.select_phase == 'p1_armor':
            self.p1_armor = list(ARMOR_TYPES.keys())[choice]
            # If AI mode, skip to game start
            if self.game_mode == 'ai':
                # Auto-select AI loadout based on weapon mode
                available_weapons = self.get_available_weapons()
                self.p2_weapon = random.choice(available_weapons)
                self.p2_armor = random.choice(list(ARMOR_TYPES.keys()))
                self.reset_game()
                self.state = 'playing'
            else:
                self.select_phase = 'p2_weapon'
        elif self.select_phase == 'p2_weapon':
            # Filter weapons based on weapon mode
            available_weapons = self.get_available_weapons()
            self.p2_weapon = available_weapons[choice]
            self.select_phase = 'p2_armor'
        elif self.select_phase == 'p2_armor':
            self.p2_armor = list(ARMOR_TYPES.keys())[choice]
            self.reset_game()
            self.state = 'playing'

    def get_available_weapons(self):
        """Get list of weapons based on current weapon mode"""
        if self.weapon_mode == 'melee_only':
            return [w for w in WEAPONS.keys() if not WEAPONS[w].get('projectile', False)]
        elif self.weapon_mode == 'ranged_only':
            return [w for w in WEAPONS.keys() if WEAPONS[w].get('projectile', False)]
        else:  # 'any'
            return list(WEAPONS.keys())

    def start_host(self):
        """Start hosting a game"""
        try:
            # Clean up any existing socket first
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
                time.sleep(0.5)  # Give OS time to release the port

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Also set SO_REUSEPORT on macOS for better port reuse
            try:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except AttributeError:
                pass  # Not available on all platforms

            self.socket.bind(('0.0.0.0', 5555))
            self.socket.listen(1)

            # Get local IP address (better method)
            try:
                # Create a temporary socket to find the local IP
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                temp_socket.connect(('8.8.8.8', 80))  # Connect to Google DNS
                self.host_ip = temp_socket.getsockname()[0]
                temp_socket.close()
            except:
                # Fallback to hostname method
                hostname = socket.gethostname()
                self.host_ip = socket.gethostbyname(hostname)

            self.select_phase = 'waiting_for_player'

            # Start accepting connections in background
            self.network_thread = threading.Thread(target=self.accept_connection, daemon=True)
            self.network_thread.start()
        except Exception as e:
            print(f"Error starting host: {e}")
            import traceback
            traceback.print_exc()
            self.state = 'menu'

    def accept_connection(self):
        """Accept incoming connection"""
        try:
            # Set timeout so we can check if socket was closed
            self.socket.settimeout(1.0)
            while self.socket:
                try:
                    self.connection, addr = self.socket.accept()
                    self.connected = True
                    print(f"Connected to {addr}")
                    break
                except socket.timeout:
                    # Check if socket still exists
                    if not self.socket:
                        break
                    continue
        except Exception as e:
            if self.socket:  # Only print if socket wasn't intentionally closed
                print(f"Error accepting connection: {e}")

    def connect_to_host(self, ip):
        """Connect to a host"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, 5555))
            self.connection = self.socket
            self.connected = True
            print(f"Connected to {ip}")
        except Exception as e:
            print(f"Error connecting: {e}")
            return False
        return True

    def send_data(self, data):
        """Send data over network"""
        if self.connection:
            try:
                message = json.dumps(data) + '\n'
                self.connection.sendall(message.encode())
            except Exception as e:
                print(f"Error sending data: {e}")
                self.connected = False

    def receive_data(self):
        """Receive data from network (non-blocking)"""
        if self.connection:
            try:
                self.connection.setblocking(0)
                data = self.connection.recv(4096).decode()
                if data:
                    # Handle multiple messages
                    for line in data.strip().split('\n'):
                        if line:
                            return json.loads(line)
            except BlockingIOError:
                pass
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.connected = False
        return None

    def update(self):
        if self.state != 'playing':
            return

        # Safety check - make sure players exist
        if not self.player1 or not self.player2:
            return

        # Get keyboard state
        keys = pygame.key.get_pressed()

        # Handle touch controls for movement - use a wrapper class to handle large key codes
        if self.show_touch_controls:
            # Create a wrapper that can handle any key code safely
            class KeyWrapper:
                def __init__(self, original_keys):
                    self.keys = original_keys
                    self.overrides = {}

                def __getitem__(self, key):
                    if key in self.overrides:
                        return self.overrides[key]
                    if key < len(self.keys):
                        return self.keys[key]
                    return 0

            key_wrapper = KeyWrapper(keys)

            # Player 1 controls
            if self.touch_buttons['p1_left'].pressed:
                key_wrapper.overrides[pygame.K_a] = 1
            if self.touch_buttons['p1_right'].pressed:
                key_wrapper.overrides[pygame.K_d] = 1
            if self.touch_buttons['p1_up'].pressed:
                key_wrapper.overrides[pygame.K_w] = 1
            if self.touch_buttons['p1_down'].pressed:
                key_wrapper.overrides[pygame.K_s] = 1

            # Player 2 controls
            if self.player2 and not self.player2.is_ai:
                if self.touch_buttons['p2_left'].pressed:
                    key_wrapper.overrides[pygame.K_LEFT] = 1
                if self.touch_buttons['p2_right'].pressed:
                    key_wrapper.overrides[pygame.K_RIGHT] = 1
                if self.touch_buttons['p2_up'].pressed:
                    key_wrapper.overrides[pygame.K_UP] = 1
                if self.touch_buttons['p2_down'].pressed:
                    key_wrapper.overrides[pygame.K_DOWN] = 1

            keys = key_wrapper

        # Player 2 crosshair control - use IJKL to move crosshair (always active)
        if self.player2 and not self.player2.is_ai:
            aim_speed = 8
            if keys[pygame.K_j]:  # J = Left
                self.p2_aim_x -= aim_speed
            if keys[pygame.K_l]:  # L = Right
                self.p2_aim_x += aim_speed
            if keys[pygame.K_i]:  # I = Up
                self.p2_aim_y -= aim_speed
            if keys[pygame.K_k]:  # K = Down
                self.p2_aim_y += aim_speed

            # Keep crosshair on screen
            self.p2_aim_x = max(0, min(self.p2_aim_x, SCREEN_WIDTH))
            self.p2_aim_y = max(0, min(self.p2_aim_y, SCREEN_HEIGHT))

        # Normal movement for both players
        self.player1.update(keys, self.caves, self.player2)
        self.player2.update(keys, self.caves, self.player1)

        # AI auto-attack with reaction time based on difficulty
        if self.player2.is_ai and self.player2.alive and self.player1.alive:
            # Reaction time delays
            if self.ai_difficulty == 'easy':
                attack_delay = 45  # Slow attacks
            elif self.ai_difficulty == 'medium':
                attack_delay = 25
            else:  # hard
                attack_delay = 10  # Very fast attacks

            self.player2.ai_reaction_time += 1

            if self.player2.attack_cooldown == 0 and self.player2.ai_reaction_time >= attack_delay:
                # Calculate distance to player
                dx = self.player1.x - self.player2.x
                dy = self.player1.y - self.player2.y
                dist = math.sqrt(dx**2 + dy**2)

                weapon = WEAPONS[self.player2.weapon]
                # Attack if in range
                if dist <= weapon['range']:
                    result = self.player2.attack(self.player1.x + 25, self.player1.y + 35)
                    if isinstance(result, Projectile):
                        self.projectiles.append(result)
                    elif result == 'melee_hit':
                        self.player1.take_damage(weapon['damage'])
                    self.player2.ai_reaction_time = 0  # Reset reaction timer

        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update()
            if not proj.alive:
                self.projectiles.remove(proj)
                continue

            p1_rect = pygame.Rect(self.player1.x, self.player1.y, self.player1.width, self.player1.height)
            p2_rect = pygame.Rect(self.player2.x, self.player2.y, self.player2.width, self.player2.height)
            proj_rect = pygame.Rect(proj.x - proj.radius, proj.y - proj.radius, proj.radius * 2, proj.radius * 2)

            # Only hit opponent, not the player who fired it
            if p1_rect.colliderect(proj_rect) and proj.owner != self.player1:
                self.player1.take_damage(proj.damage)
                proj.alive = False
            elif p2_rect.colliderect(proj_rect) and proj.owner != self.player2:
                self.player2.take_damage(proj.damage)
                proj.alive = False

        # Update gems
        for cave in self.caves:
            for gem in cave.gems:
                gem.update()

        # Check game over
        if not self.player1.alive or not self.player2.alive:
            self.state = 'game_over'

    def draw(self):
        self.screen.fill((30, 30, 50))

        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'setup':
            self.draw_setup()
        elif self.state == 'playing':
            self.draw_game()
        elif self.state == 'game_over':
            self.draw_game()
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        title = self.font.render("PvP BATTLE ARENA", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 250, 150))

        subtitle = self.small_font.render("With Weapons, Armor & Healing Gems!", True, WHITE)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 300, 230))

        # Mode selection
        mode_title = self.small_font.render("Choose Game Mode:", True, WHITE)
        self.screen.blit(mode_title, (SCREEN_WIDTH // 2 - 160, 320))

        # Draw touch buttons for menu
        for button in self.menu_buttons:
            button.draw(self.screen, self.small_font)

        # Also show keyboard shortcuts on the side
        mode_1 = self.tiny_font.render("Press 1", True, GRAY)
        self.screen.blit(mode_1, (SCREEN_WIDTH // 2 + 230, 470))

        mode_2 = self.tiny_font.render("Press 2", True, GRAY)
        self.screen.blit(mode_2, (SCREEN_WIDTH // 2 + 230, 560))

        mode_3 = self.tiny_font.render("Press 3", True, GRAY)
        self.screen.blit(mode_3, (SCREEN_WIDTH // 2 + 230, 650))

        info = [
            "",
            "Player 1: WASD (move) + SPACE (attack/aim with mouse)",
            "Player 2: Arrow Keys (move) + IJKL (aim) + SHIFT (shoot) + ENTER (melee)",
            "",
            "Mobile: Tap 'TOUCH ON/OFF' button at top for controls",
            "",
            "Find healing gems hidden in caves!",
            "Choose your weapon and armor wisely!"
        ]

        y = 720
        for line in info:
            text = self.tiny_font.render(line, True, GRAY)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 250, y))
            y += 25

    def draw_setup(self):
        # Online mode selection
        if self.select_phase == 'online_mode':
            title = self.font.render("Around The World Mode", True, GREEN)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 300, 50))

            subtitle = self.small_font.render("Choose how to connect:", True, WHITE)
            self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 180, 150))

            # Create buttons if not already created for this phase
            if self.last_setup_phase != 'online_mode':
                self.create_setup_buttons('online_mode', 2, [YELLOW, BLUE])
                self.setup_buttons[0].text = "HOST GAME"
                self.setup_buttons[1].text = "JOIN GAME"
                self.last_setup_phase = 'online_mode'

            # Draw buttons
            for button in self.setup_buttons:
                button.draw(self.screen, self.small_font)

            # Draw descriptions below buttons
            host_desc = self.tiny_font.render("Create a game and share your IP with a friend", True, GRAY)
            self.screen.blit(host_desc, (SCREEN_WIDTH // 2 - 250, 330))

            join_desc = self.tiny_font.render("Enter your friend's IP address to join their game", True, GRAY)
            self.screen.blit(join_desc, (SCREEN_WIDTH // 2 - 250, 480))

            # Show keyboard hints
            hint1 = self.tiny_font.render("Press 1", True, GRAY)
            self.screen.blit(hint1, (SCREEN_WIDTH // 2 + 270, 270))
            hint2 = self.tiny_font.render("Press 2", True, GRAY)
            self.screen.blit(hint2, (SCREEN_WIDTH // 2 + 270, 420))
            return

        # Waiting for player
        if self.select_phase == 'waiting_for_player':
            title = self.font.render("Waiting for Player...", True, YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 280, 150))

            ip_text = self.small_font.render(f"Your IP Address: {self.host_ip}", True, GREEN)
            self.screen.blit(ip_text, (SCREEN_WIDTH // 2 - 200, 300))

            instruction = self.small_font.render("Share this IP with your friend!", True, WHITE)
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - 250, 380))

            waiting = self.tiny_font.render("Waiting for connection...", True, GRAY)
            self.screen.blit(waiting, (SCREEN_WIDTH // 2 - 120, 460))

            # Add ESC hint
            esc_hint = self.tiny_font.render("Press ESC to cancel and return to menu", True, RED)
            self.screen.blit(esc_hint, (SCREEN_WIDTH // 2 - 180, 520))

            # Check if connected
            if self.connected:
                self.select_phase = 'weapon_mode'
            return

        # Enter IP screen
        if self.select_phase == 'enter_ip':
            title = self.font.render("Join Game", True, BLUE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 150, 100))

            instruction = self.small_font.render("Enter Host IP Address:", True, WHITE)
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - 200, 250))

            # Draw input box
            input_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 50)
            pygame.draw.rect(self.screen, WHITE, input_box, 3)

            ip_display = self.font.render(self.host_ip if self.host_ip else '___.___.___', True, YELLOW if self.host_ip else GRAY)
            self.screen.blit(ip_display, (SCREEN_WIDTH // 2 - 190, 330))

            hint = self.tiny_font.render("Use keyboard below or type with keyboard", True, GRAY)
            self.screen.blit(hint, (SCREEN_WIDTH // 2 - 180, 400))

            # Draw on-screen keyboard
            for button in self.keyboard_buttons:
                button.draw(self.screen, self.tiny_font)

            return

        # Weapon mode selection
        if self.select_phase == 'weapon_mode':
            title = self.font.render("Choose Weapon Type", True, YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 250, 50))

            modes = [
                ('Melee Only', 'Sword & Axe - Close combat only', RED),
                ('Ranged Only', 'Bow, Magic & Gun - Distance attacks', BLUE),
                ('Any Weapon', 'All weapons available - Mixed combat', GREEN)
            ]

            # Create buttons if not already created for this phase
            if self.last_setup_phase != 'weapon_mode':
                self.create_setup_buttons('weapon_mode', 3, [RED, BLUE, GREEN])
                self.setup_buttons[0].text = "Melee Only"
                self.setup_buttons[1].text = "Ranged Only"
                self.setup_buttons[2].text = "Any Weapon"
                self.last_setup_phase = 'weapon_mode'

            # Draw buttons and descriptions
            y = 250
            for i, button in enumerate(self.setup_buttons):
                button.rect.y = y
                button.draw(self.screen, self.small_font)

                # Draw description below button
                name, desc, color = modes[i]
                desc_text = self.tiny_font.render(desc, True, GRAY)
                self.screen.blit(desc_text, (SCREEN_WIDTH // 2 - 250, y + 85))

                # Keyboard hint
                hint = self.tiny_font.render(f"Press {i+1}", True, GRAY)
                self.screen.blit(hint, (SCREEN_WIDTH // 2 + 270, y + 25))
                y += 150
            return

        # Difficulty selection
        if self.select_phase == 'ai_difficulty':
            title = self.font.render("Choose AI Difficulty", True, YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 250, 50))

            difficulties = [
                ('Easy', 'Slower, makes mistakes, heals early', GREEN),
                ('Medium', 'Balanced AI opponent', YELLOW),
                ('Hard', 'Fast, aggressive, rarely heals', RED)
            ]

            # Create buttons if not already created for this phase
            if self.last_setup_phase != 'ai_difficulty':
                self.create_setup_buttons('ai_difficulty', 3, [GREEN, YELLOW, RED])
                self.setup_buttons[0].text = "Easy"
                self.setup_buttons[1].text = "Medium"
                self.setup_buttons[2].text = "Hard"
                self.last_setup_phase = 'ai_difficulty'

            # Draw buttons and descriptions
            y = 250
            for i, button in enumerate(self.setup_buttons):
                button.rect.y = y
                button.draw(self.screen, self.small_font)

                # Draw description below button
                name, desc, color = difficulties[i]
                desc_text = self.tiny_font.render(desc, True, GRAY)
                self.screen.blit(desc_text, (SCREEN_WIDTH // 2 - 200, y + 85))

                # Keyboard hint
                hint = self.tiny_font.render(f"Press {i+1}", True, GRAY)
                self.screen.blit(hint, (SCREEN_WIDTH // 2 + 270, y + 25))
                y += 150
            return

        if 'p1' in self.select_phase:
            title = self.font.render("Player 1 Setup", True, RED)
            player_color = RED
        else:
            title = self.font.render("Player 2 Setup", True, BLUE)
            player_color = BLUE

        self.screen.blit(title, (SCREEN_WIDTH // 2 - 200, 50))

        if 'weapon' in self.select_phase:
            subtitle = self.small_font.render("Choose Your Weapon:", True, WHITE)
            self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 180, 150))

            # Get available weapons based on mode
            available_weapons = self.get_available_weapons()

            # Create buttons for weapons
            if self.last_setup_phase != self.select_phase:
                weapon_colors = [WEAPONS[w]['color'] for w in available_weapons]
                self.create_setup_buttons('weapon', len(available_weapons), weapon_colors)
                for i, weapon_key in enumerate(available_weapons):
                    weapon = WEAPONS[weapon_key]
                    self.setup_buttons[i].text = weapon['name']
                self.last_setup_phase = self.select_phase

            # Draw buttons
            y = 250
            for i, button in enumerate(self.setup_buttons):
                button.rect.y = y
                button.draw(self.screen, self.small_font)

                # Draw weapon details below button
                weapon_key = available_weapons[i]
                weapon = WEAPONS[weapon_key]
                weapon_type = "Ranged" if weapon.get('projectile', False) else "Melee"
                desc = f"({weapon_type}, DMG: {weapon['damage']}, Range: {weapon['range']})"
                desc_text = self.tiny_font.render(desc, True, GRAY)
                self.screen.blit(desc_text, (SCREEN_WIDTH // 2 - 220, y + 85))

                # Keyboard hint
                hint = self.tiny_font.render(f"Press {i+1}", True, GRAY)
                self.screen.blit(hint, (SCREEN_WIDTH // 2 + 270, y + 25))
                y += 130

        else:  # armor
            subtitle = self.small_font.render("Choose Your Armor:", True, WHITE)
            self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 180, 150))

            # Create buttons for armor
            armor_list = list(ARMOR_TYPES.items())
            if self.last_setup_phase != self.select_phase:
                armor_colors = [armor['color'] for key, armor in armor_list]
                self.create_setup_buttons('armor', len(armor_list), armor_colors)
                for i, (key, armor) in enumerate(armor_list):
                    self.setup_buttons[i].text = armor['name']
                self.last_setup_phase = self.select_phase

            # Draw buttons
            y = 250
            for i, button in enumerate(self.setup_buttons):
                button.rect.y = y
                button.draw(self.screen, self.small_font)

                # Draw armor details below button
                key, armor = armor_list[i]
                desc = f"(DMG Reduction: {int((1-armor['defense'])*100)}%, Speed: {int(armor['speed_mult']*100)}%)"
                desc_text = self.tiny_font.render(desc, True, GRAY)
                self.screen.blit(desc_text, (SCREEN_WIDTH // 2 - 220, y + 85))

                # Keyboard hint
                hint = self.tiny_font.render(f"Press {i+1}", True, GRAY)
                self.screen.blit(hint, (SCREEN_WIDTH // 2 + 270, y + 25))
                y += 130

    def draw_game(self):
        # Grid
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, (40, 40, 60), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, (40, 40, 60), (0, y), (SCREEN_WIDTH, y), 1)

        # Caves
        for cave in self.caves:
            cave.draw(self.screen)

        # Projectiles
        for proj in self.projectiles:
            proj.draw(self.screen)

        # Players
        if self.player1:
            self.player1.draw(self.screen)
        if self.player2:
            self.player2.draw(self.screen)

        # Player 2 aiming crosshair - always visible and active for Player 2
        if self.player2 and not self.player2.is_ai:
            # Draw crosshair - always bright since it's always ready
            crosshair_size = 20
            outer_color = BLUE
            inner_color = RED
            line_width = 3

            # Outer circle
            pygame.draw.circle(self.screen, outer_color, (int(self.p2_aim_x), int(self.p2_aim_y)), crosshair_size, line_width)
            # Inner dot
            pygame.draw.circle(self.screen, inner_color, (int(self.p2_aim_x), int(self.p2_aim_y)), 3)
            # Cross lines
            pygame.draw.line(self.screen, outer_color, (self.p2_aim_x - crosshair_size - 5, self.p2_aim_y),
                           (self.p2_aim_x - crosshair_size, self.p2_aim_y), line_width)
            pygame.draw.line(self.screen, outer_color, (self.p2_aim_x + crosshair_size, self.p2_aim_y),
                           (self.p2_aim_x + crosshair_size + 5, self.p2_aim_y), line_width)
            pygame.draw.line(self.screen, outer_color, (self.p2_aim_x, self.p2_aim_y - crosshair_size - 5),
                           (self.p2_aim_x, self.p2_aim_y - crosshair_size), line_width)
            pygame.draw.line(self.screen, outer_color, (self.p2_aim_x, self.p2_aim_y + crosshair_size),
                           (self.p2_aim_x, self.p2_aim_y + crosshair_size + 5), line_width)

        # Always draw the toggle button
        self.touch_toggle_button.draw(self.screen, self.tiny_font)

        # Touch controls
        if self.show_touch_controls:
            # Draw Player 1 controls
            for key in ['p1_left', 'p1_right', 'p1_up', 'p1_down', 'p1_attack']:
                self.touch_buttons[key].draw(self.screen, self.tiny_font)

            # Only draw Player 2 controls if not playing against AI (check game mode)
            if self.game_mode != 'ai':
                for key in ['p2_left', 'p2_right', 'p2_up', 'p2_down', 'p2_attack']:
                    self.touch_buttons[key].draw(self.screen, self.tiny_font)

        # HUD
        hint_text = "Find healing gems in caves! ESC: Menu"
        hint = self.tiny_font.render(hint_text, True, GRAY)
        self.screen.blit(hint, (10, SCREEN_HEIGHT - 30))

        if self.show_touch_controls:
            touch_status = self.tiny_font.render("Touch Controls: ON", True, GREEN)
            self.screen.blit(touch_status, (SCREEN_WIDTH // 2 - 80, 55))
        else:
            touch_status = self.tiny_font.render("Touch Controls: OFF", True, RED)
            self.screen.blit(touch_status, (SCREEN_WIDTH // 2 - 85, 55))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        if self.player1.alive:
            if self.game_mode == 'ai':
                winner = self.font.render("YOU WIN!", True, RED)
            else:
                winner = self.font.render("PLAYER 1 WINS!", True, RED)
        else:
            if self.game_mode == 'ai':
                winner = self.font.render("AI WINS!", True, BLUE)
            else:
                winner = self.font.render("PLAYER 2 WINS!", True, BLUE)

        self.screen.blit(winner, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 50))

        restart = self.small_font.render("SPACE: Rematch  |  ENTER: Menu", True, WHITE)
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 + 50))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

def main():
    game = PvPGame()
    game.run()

if __name__ == '__main__':
    main()
