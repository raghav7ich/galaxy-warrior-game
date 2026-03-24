import math
import random
import pygame
from settings import *


class Star:
    def __init__(self):
        self.reset(initial=True)

    def reset(self, initial=False):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT) if initial else random.randint(-40, -10)
        self.speed = random.uniform(1, 4)
        self.size = random.randint(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset()

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)


class Bullet:
    def __init__(self, x, y, speed, owner='player', color=YELLOW, radius=4, dx=0):
        self.x = x
        self.y = y
        self.speed = speed
        self.owner = owner
        self.color = color
        self.radius = radius
        self.dx = dx
        self.rect = pygame.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)

    def update(self):
        self.y += self.speed
        self.x += self.dx
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), max(1, self.radius - 2), 1)

    def offscreen(self):
        return self.y < -20 or self.y > HEIGHT + 20 or self.x < -20 or self.x > WIDTH + 20


class Player:
    def __init__(self):
        self.width = 52
        self.height = 58
        self.x = WIDTH // 2
        self.y = HEIGHT - 90
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.lives = 3
        self.fire_delay = 260
        self.last_shot = 0
        self.power_timer = 0
        self.shield_timer = 0
        self.rapid_timer = 0
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.update_rect()

    def update_rect(self):
        self.rect.center = (self.x, self.y)

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(self.width // 2, min(WIDTH - self.width // 2, self.x))
        self.y = max(80, min(HEIGHT - self.height // 2, self.y))
        self.update_rect()

    def update_timers(self, dt):
        self.power_timer = max(0, self.power_timer - dt)
        self.shield_timer = max(0, self.shield_timer - dt)
        self.rapid_timer = max(0, self.rapid_timer - dt)

    def shoot(self):
        now = pygame.time.get_ticks()
        current_delay = 130 if self.rapid_timer > 0 else self.fire_delay
        if now - self.last_shot < current_delay:
            return []
        self.last_shot = now

        bullets = [Bullet(self.x, self.y - 28, -BULLET_SPEED, owner='player', color=YELLOW, radius=5)]
        if self.power_timer > 0:
            bullets.append(Bullet(self.x - 15, self.y - 20, -BULLET_SPEED, owner='player', color=CYAN, radius=4, dx=-1.2))
            bullets.append(Bullet(self.x + 15, self.y - 20, -BULLET_SPEED, owner='player', color=CYAN, radius=4, dx=1.2))
        return bullets

    def damage(self, amount):
        if self.shield_timer > 0:
            amount = max(0, amount // 3)
        self.health -= amount
        if self.health <= 0:
            self.lives -= 1
            self.health = self.max_health
            return True
        return False

    def draw(self, surface):
        points = [
            (self.x, self.y - 28),
            (self.x - 22, self.y + 18),
            (self.x - 10, self.y + 14),
            (self.x, self.y + 28),
            (self.x + 10, self.y + 14),
            (self.x + 22, self.y + 18),
        ]
        pygame.draw.polygon(surface, BLUE, points)
        pygame.draw.polygon(surface, WHITE, points, 2)
        pygame.draw.rect(surface, CYAN, (self.x - 5, self.y - 10, 10, 22))
        pygame.draw.circle(surface, ORANGE, (int(self.x), int(self.y + 26)), 5)
        if self.shield_timer > 0:
            pygame.draw.circle(surface, CYAN, (int(self.x), int(self.y)), 42, 2)


class Enemy:
    def __init__(self, level):
        self.level = level
        self.kind = random.choice(['scout', 'fighter', 'tank'])
        self.x = random.randint(60, WIDTH - 60)
        self.y = random.randint(-200, -60)
        self.base_x = self.x
        self.wave_phase = random.uniform(0, math.pi * 2)
        self.rect = pygame.Rect(0, 0, 42, 42)

        if self.kind == 'scout':
            self.health = 20 + level * 4
            self.speed = 2.5 + level * 0.3
            self.score = 12
            self.color = RED
        elif self.kind == 'fighter':
            self.health = 35 + level * 6
            self.speed = 1.8 + level * 0.25
            self.score = 20
            self.color = PURPLE
        else:
            self.health = 55 + level * 10
            self.speed = 1.2 + level * 0.2
            self.score = 35
            self.color = ORANGE

        self.fire_delay = random.randint(400, 800)
        self.last_shot = pygame.time.get_ticks()
        self.update_rect()

    def update_rect(self):
        self.rect.center = (self.x, self.y)

    def update(self):
        self.y += self.speed
        self.x = self.base_x + math.sin(pygame.time.get_ticks() * 0.003 + self.wave_phase) * 30
        self.update_rect()

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.fire_delay and self.y > 0:
            self.last_shot = now
            return True
        return False

    def shoot(self):
        return Bullet(self.x, self.y + 18, ENEMY_BULLET_SPEED, owner='enemy', color=RED, radius=4)

    def draw(self, surface):
        body = [(self.x, self.y + 18), (self.x - 20, self.y - 12), (self.x, self.y - 24), (self.x + 20, self.y - 12)]
        pygame.draw.polygon(surface, self.color, body)
        pygame.draw.polygon(surface, WHITE, body, 2)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y - 8)), 4)

    def offscreen(self):
        return self.y > HEIGHT + 50


class Boss:
    def __init__(self, level):
        self.level = level
        self.x = WIDTH // 2
        self.y = 120
        self.width = 220
        self.height = 120
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.max_health = 450 + level * 120
        self.health = self.max_health
        self.speed = 2.8
        self.direction = 1
        self.fire_delay = 800
        self.last_shot = 0
        self.entering = True
        self.arrive_y = 110
        self.angle = 0
        self.update_rect()

    def update_rect(self):
        self.rect.center = (self.x, self.y)

    def update(self):
        if self.entering:
            self.y += 1.5
            if self.y >= self.arrive_y:
                self.entering = False
        else:
            self.x += self.speed * self.direction
            if self.x < 140 or self.x > WIDTH - 140:
                self.direction *= -1
            self.angle += 0.04
        self.update_rect()

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.fire_delay and not self.entering:
            self.last_shot = now
            return True
        return False

    def shoot(self):
        bullets = []
        for dx in (-3.0, -1.5, 0, 1.5, 3.0):
            bullets.append(Bullet(self.x, self.y + 30, ENEMY_BULLET_SPEED + 1, owner='enemy', color=ORANGE, radius=6, dx=dx))
        return bullets

    def draw(self, surface):
        x, y = self.x, self.y
        pygame.draw.rect(surface, PURPLE, (x - 95, y - 30, 190, 60), border_radius=18)
        pygame.draw.rect(surface, RED, (x - 50, y - 55, 100, 110), border_radius=24)
        pygame.draw.circle(surface, YELLOW, (int(x), int(y - 5)), 18)
        pygame.draw.polygon(surface, ORANGE, [(x - 100, y + 20), (x - 140, y + 55), (x - 85, y + 42)])
        pygame.draw.polygon(surface, ORANGE, [(x + 100, y + 20), (x + 140, y + 55), (x + 85, y + 42)])
        pygame.draw.rect(surface, WHITE, (x - 95, y - 30, 190, 60), 2, border_radius=18)
        pygame.draw.rect(surface, WHITE, (x - 50, y - 55, 100, 110), 2, border_radius=24)
        pygame.draw.circle(surface, BLACK, (int(x), int(y - 5)), 8)

    def damage(self, amount):
        self.health -= amount
        return self.health <= 0


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 4
        self.max_radius = 30
        self.alive = True

    def update(self):
        self.radius += 2.8
        if self.radius >= self.max_radius:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, ORANGE, (int(self.x), int(self.y)), int(self.radius), 3)
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), max(1, int(self.radius * 0.55)), 2)


class PowerUp:
    TYPES = ['triple', 'shield', 'rapid', 'heal']

    def __init__(self, x, y):
        self.kind = random.choice(self.TYPES)
        self.x = x
        self.y = y
        self.speed = 2.5
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.update_rect()

    def update_rect(self):
        self.rect.center = (self.x, self.y)

    def update(self):
        self.y += self.speed
        self.update_rect()

    def draw(self, surface):
        color_map = {
            'triple': CYAN,
            'shield': BLUE,
            'rapid': YELLOW,
            'heal': GREEN,
        }
        color = color_map[self.kind]
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 12)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 12, 2)
        label = self.kind[0].upper()
        font = pygame.font.SysFont('arial', 16, bold=True)
        text = font.render(label, True, BLACK)
        surface.blit(text, text.get_rect(center=(self.x, self.y)))

    def offscreen(self):
        return self.y > HEIGHT + 30
