import pygame
import math
import random

pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
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
    'sword': {'name': 'Sword', 'damage': 25, 'range': 70, 'cooldown': 15, 'color': (192, 192, 192)},
    'bow': {'name': 'Bow', 'damage': 20, 'range': 500, 'cooldown': 25, 'color': (139, 69, 19), 'projectile': True},
    'axe': {'name': 'Axe', 'damage': 40, 'range': 60, 'cooldown': 35, 'color': (100, 100, 100)},
    'magic': {'name': 'Magic', 'damage': 30, 'range': 400, 'cooldown': 20, 'color': (138, 43, 226), 'projectile': True}
}

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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.heal_amount = 30
        self.collected = False
        self.pulse = 0

    def update(self):
        self.pulse += 0.1

    def draw(self, screen):
        if not self.collected:
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
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = DARK_GRAY
        self.gems = []

        # Add healing gems inside
        for i in range(random.randint(2, 4)):
            gx = x + random.randint(30, width - 30)
            gy = y + random.randint(30, height - 30)
            self.gems.append(HealingGem(gx, gy))

    def draw(self, screen):
        # Cave entrance
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
    def __init__(self, x, y, color, controls, name, is_ai=False, ai_difficulty='medium'):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 70
        self.color = color
        self.name = name
        self.is_ai = is_ai
        self.ai_difficulty = ai_difficulty

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

        # Body
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

        self.font = pygame.font.Font(None, 56)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)

        # Selections
        self.game_mode = '2p'  # '2p' or 'ai'
        self.ai_difficulty = 'medium'  # 'easy', 'medium', 'hard'
        self.p1_weapon = 'sword'
        self.p1_armor = 'light'
        self.p2_weapon = 'sword'
        self.p2_armor = 'light'
        self.select_phase = 'mode'

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
                             'down': pygame.K_s, 'attack': pygame.K_SPACE}, "Player 1")
        self.player1.weapon = self.p1_weapon
        self.player1.armor = self.p1_armor

        # Create Player 2 (either human or AI)
        is_ai = (self.game_mode == 'ai')
        player2_name = "AI Opponent" if is_ai else "Player 2"

        self.player2 = Player(SCREEN_WIDTH - 250, SCREEN_HEIGHT // 2, BLUE,
                            {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP,
                             'down': pygame.K_DOWN, 'attack': pygame.K_RSHIFT}, player2_name,
                            is_ai=is_ai, ai_difficulty=self.ai_difficulty)
        self.player2.weapon = self.p2_weapon
        self.player2.armor = self.p2_armor

        self.projectiles = []
        self.create_world()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == 'menu':
                    if event.key == pygame.K_1:
                        self.game_mode = '2p'
                        self.state = 'setup'
                        self.select_phase = 'p1_weapon'
                    elif event.key == pygame.K_2:
                        self.game_mode = 'ai'
                        self.state = 'setup'
                        self.select_phase = 'ai_difficulty'

                elif self.state == 'setup':
                    if event.key == pygame.K_1:
                        self.handle_selection(0)
                    elif event.key == pygame.K_2:
                        self.handle_selection(1)
                    elif event.key == pygame.K_3:
                        self.handle_selection(2)
                    elif event.key == pygame.K_4 and self.select_phase in ['p1_weapon', 'p2_weapon']:
                        self.handle_selection(3)

                elif self.state == 'playing':
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'

                    if event.key == self.player1.controls['attack']:
                        mx, my = pygame.mouse.get_pos()
                        result = self.player1.attack(mx, my)
                        if isinstance(result, Projectile):
                            self.projectiles.append(result)
                        elif result == 'melee_hit':
                            dist = math.sqrt((self.player2.x - self.player1.x)**2 +
                                           (self.player2.y - self.player1.y)**2)
                            if dist <= WEAPONS[self.player1.weapon]['range']:
                                self.player2.take_damage(WEAPONS[self.player1.weapon]['damage'])

                    if event.key == self.player2.controls['attack']:
                        result = self.player2.attack(self.player1.x + 25, self.player1.y + 35)
                        if isinstance(result, Projectile):
                            self.projectiles.append(result)
                        elif result == 'melee_hit':
                            self.player1.take_damage(WEAPONS[self.player2.weapon]['damage'])

                elif self.state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = 'playing'
                    elif event.key == pygame.K_RETURN:
                        self.state = 'menu'

    def handle_selection(self, choice):
        if self.select_phase == 'ai_difficulty':
            difficulties = ['easy', 'medium', 'hard']
            self.ai_difficulty = difficulties[choice]
            self.select_phase = 'p1_weapon'
        elif self.select_phase == 'p1_weapon':
            self.p1_weapon = list(WEAPONS.keys())[choice]
            self.select_phase = 'p1_armor'
        elif self.select_phase == 'p1_armor':
            self.p1_armor = list(ARMOR_TYPES.keys())[choice]
            # If AI mode, skip to game start
            if self.game_mode == 'ai':
                # Auto-select AI loadout
                self.p2_weapon = random.choice(list(WEAPONS.keys()))
                self.p2_armor = random.choice(list(ARMOR_TYPES.keys()))
                self.reset_game()
                self.state = 'playing'
            else:
                self.select_phase = 'p2_weapon'
        elif self.select_phase == 'p2_weapon':
            self.p2_weapon = list(WEAPONS.keys())[choice]
            self.select_phase = 'p2_armor'
        elif self.select_phase == 'p2_armor':
            self.p2_armor = list(ARMOR_TYPES.keys())[choice]
            self.reset_game()
            self.state = 'playing'

    def update(self):
        if self.state != 'playing':
            return

        keys = pygame.key.get_pressed()
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

        mode_1 = self.small_font.render("1 - VS PLAYER", True, RED)
        self.screen.blit(mode_1, (SCREEN_WIDTH // 2 - 250, 380))

        mode_2 = self.small_font.render("2 - VS AI", True, BLUE)
        self.screen.blit(mode_2, (SCREEN_WIDTH // 2 + 50, 380))

        info = [
            "",
            "Player 1: WASD + SPACE (aim with mouse)",
            "Player 2: Arrow Keys + Right SHIFT (auto-aim)",
            "",
            "Find healing gems hidden in caves!",
            "Choose your weapon and armor wisely!"
        ]

        y = 480
        for line in info:
            text = self.tiny_font.render(line, True, GRAY)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 250, y))
            y += 30

    def draw_setup(self):
        # Difficulty selection
        if self.select_phase == 'ai_difficulty':
            title = self.font.render("Choose AI Difficulty", True, YELLOW)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - 250, 50))

            difficulties = [
                ('Easy', 'Slower, makes mistakes, heals early', GREEN),
                ('Medium', 'Balanced AI opponent', YELLOW),
                ('Hard', 'Fast, aggressive, rarely heals', RED)
            ]

            y = 200
            for i, (name, desc, color) in enumerate(difficulties, 1):
                text = f"{i} - {name}"
                rendered = self.font.render(text, True, color)
                self.screen.blit(rendered, (SCREEN_WIDTH // 2 - 150, y))

                desc_text = self.tiny_font.render(desc, True, GRAY)
                self.screen.blit(desc_text, (SCREEN_WIDTH // 2 - 200, y + 50))
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

            y = 250
            for i, (key, weapon) in enumerate(WEAPONS.items(), 1):
                text = f"{i} - {weapon['name']} (DMG: {weapon['damage']}, Range: {weapon['range']})"
                color = player_color if i <= len(WEAPONS) else GRAY
                rendered = self.small_font.render(text, True, color)
                self.screen.blit(rendered, (400, y))
                pygame.draw.rect(self.screen, weapon['color'], (350, y + 5, 30, 20))
                y += 80

        else:  # armor
            subtitle = self.small_font.render("Choose Your Armor:", True, WHITE)
            self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 180, 150))

            y = 250
            for i, (key, armor) in enumerate(ARMOR_TYPES.items(), 1):
                text = f"{i} - {armor['name']} (DMG Reduction: {int((1-armor['defense'])*100)}%, Speed: {int(armor['speed_mult']*100)}%)"
                rendered = self.small_font.render(text, True, player_color)
                self.screen.blit(rendered, (300, y))
                pygame.draw.rect(self.screen, armor['color'], (250, y + 5, 30, 20))
                y += 80

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
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        # HUD
        hint = self.tiny_font.render("Find healing gems in caves! ESC: Menu", True, GRAY)
        self.screen.blit(hint, (10, 10))

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
