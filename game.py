import random
import sys
import pygame
from settings import *
from entities import Player, Enemy, Boss, Bullet, Star, Explosion, PowerUp


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont('arial', 22)
        self.font_medium = pygame.font.SysFont('arial', 32, bold=True)
        self.font_large = pygame.font.SysFont('arial', 58, bold=True)
        self.reset()

    def reset(self):
        self.state = 'menu'
        self.player = Player()
        self.level = 1
        self.level_enemy_target = 20
        self.enemies_spawned = 0
        self.enemies_destroyed = 0
        self.spawn_delay = 400
        self.last_spawn = 0
        self.boss = None
        self.message = 'Press ENTER to Start'
        self.message_timer = 0

        self.stars = [Star() for _ in range(STAR_COUNT)]
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.explosions = []
        self.powerups = []

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.state == 'menu' and event.key == pygame.K_RETURN:
                    self.start_game()
                elif self.state in ('game_over', 'victory') and event.key == pygame.K_r:
                    self.reset()
                elif self.state == 'playing' and event.key == pygame.K_SPACE:
                    self.bullets.extend(self.player.shoot())

    def start_game(self):
        self.reset()
        self.state = 'playing'
        self.message = 'Level 1'
        self.message_timer = pygame.time.get_ticks()

    def spawn_enemy(self):
        if self.boss is not None:
            return
        if self.enemies_spawned < self.level_enemy_target:
            self.enemies.append(Enemy(self.level))
            self.enemies_spawned += 1

    def maybe_start_boss(self):
        if self.enemies_destroyed >= self.level_enemy_target and not self.enemies and self.boss is None:
            self.boss = Boss(self.level)
            self.message = f'Boss Fight - Level {self.level}'
            self.message_timer = pygame.time.get_ticks()

    def next_level(self):
        self.level += 1
        if self.level > MAX_LEVEL:
            self.state = 'victory'
            return
        self.enemies_spawned = 0
        self.enemies_destroyed = 0
        self.level_enemy_target += 6
        self.spawn_delay = max(350, self.spawn_delay - 120)
        self.message = f'Level {self.level}'
        self.message_timer = pygame.time.get_ticks()

    def apply_powerup(self, kind):
        if kind == 'triple':
            self.player.power_timer = 8000
        elif kind == 'shield':
            self.player.shield_timer = 7000
        elif kind == 'rapid':
            self.player.rapid_timer = 7000
        elif kind == 'heal':
            self.player.health = min(self.player.max_health, self.player.health + 30)

    def update(self, dt):
        for star in self.stars:
            star.update()

        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.alive:
                self.explosions.remove(explosion)

        if self.state != 'playing':
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.update_timers(dt)

        now = pygame.time.get_ticks()
        if now - self.last_spawn >= self.spawn_delay and self.enemies_spawned < self.level_enemy_target:
            self.spawn_enemy()
            self.last_spawn = now

        self.maybe_start_boss()

        for enemy in self.enemies[:]:
            enemy.update()

            if enemy.can_shoot():
                self.enemy_bullets.append(enemy.shoot())

            if enemy.offscreen():
                self.enemies.remove(enemy)
                self.enemies_destroyed += 1

            elif enemy.rect.colliderect(self.player.rect):
                self.explosions.append(Explosion(enemy.x, enemy.y))
                self.enemies.remove(enemy)
                self.enemies_destroyed += 1
                dead = self.player.damage(25)
                if dead and self.player.lives < 0:
                    self.state = 'game_over'

        if self.boss:
            self.boss.update()
            if self.boss.can_shoot():
                self.enemy_bullets.extend(self.boss.shoot())
            if self.boss.rect.colliderect(self.player.rect):
                dead = self.player.damage(50)
                if dead and self.player.lives < 0:
                    self.state = 'game_over'

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.offscreen():
                self.bullets.remove(bullet)
                continue

            hit_something = False

            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= 20
                    hit_something = True
                    self.explosions.append(Explosion(bullet.x, bullet.y))

                    if enemy.health <= 0:
                        self.player.score += enemy.score
                        self.explosions.append(Explosion(enemy.x, enemy.y))
                        if random.random() < 0.18:
                            self.powerups.append(PowerUp(enemy.x, enemy.y))
                        self.enemies.remove(enemy)
                        self.enemies_destroyed += 1
                    break

            if not hit_something and self.boss and bullet.rect.colliderect(self.boss.rect):
                hit_something = True
                self.explosions.append(Explosion(bullet.x, bullet.y))
                if self.boss.damage(18):
                    self.player.score += 250
                    self.explosions.append(Explosion(self.boss.x, self.boss.y))
                    self.boss = None
                    self.next_level()

            if hit_something and bullet in self.bullets:
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.offscreen():
                self.enemy_bullets.remove(bullet)
                continue

            if bullet.rect.colliderect(self.player.rect):
                self.enemy_bullets.remove(bullet)
                self.explosions.append(Explosion(bullet.x, bullet.y))
                dead = self.player.damage(12)
                if dead and self.player.lives < 0:
                    self.state = 'game_over'

        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.offscreen():
                self.powerups.remove(powerup)
            elif powerup.rect.colliderect(self.player.rect):
                self.apply_powerup(powerup.kind)
                self.powerups.remove(powerup)

        if self.player.lives < 0:
            self.state = 'game_over'

    def draw_background(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, NAVY, (0, 0, WIDTH, HEIGHT))
        for star in self.stars:
            star.draw(self.screen)

    def draw_hud(self):
        score_text = self.font_small.render(f'Score: {self.player.score}', True, WHITE)
        level_text = self.font_small.render(f'Level: {self.level}', True, WHITE)
        lives_text = self.font_small.render(f'Lives: {max(0, self.player.lives)}', True, WHITE)

        self.screen.blit(score_text, (20, 16))
        self.screen.blit(level_text, (20, 46))
        self.screen.blit(lives_text, (20, 76))

        pygame.draw.rect(self.screen, GRAY, (WIDTH - 250, 18, 210, 22), border_radius=8)
        current_hp = max(0, self.player.health) / self.player.max_health
        pygame.draw.rect(self.screen, GREEN, (WIDTH - 250, 18, int(210 * current_hp), 22), border_radius=8)

        hp_text = self.font_small.render('Health', True, BLACK)
        self.screen.blit(hp_text, (WIDTH - 180, 17))

        powers = []
        if self.player.power_timer > 0:
            powers.append('Triple Shot')
        if self.player.shield_timer > 0:
            powers.append('Shield')
        if self.player.rapid_timer > 0:
            powers.append('Rapid Fire')

        if powers:
            power_text = self.font_small.render(' | '.join(powers), True, CYAN)
            self.screen.blit(power_text, (WIDTH // 2 - power_text.get_width() // 2, 18))

        if self.boss:
            pygame.draw.rect(self.screen, GRAY, (WIDTH // 2 - 220, 55, 440, 22), border_radius=8)
            ratio = max(0, self.boss.health) / self.boss.max_health
            pygame.draw.rect(self.screen, RED, (WIDTH // 2 - 220, 55, int(440 * ratio), 22), border_radius=8)
            text = self.font_small.render('Boss Health', True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 54))

    def draw_center_message(self, title, subtitle):
        title_surf = self.font_large.render(title, True, WHITE)
        sub_surf = self.font_medium.render(subtitle, True, CYAN)
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    def draw(self):
        self.draw_background()

        for powerup in self.powerups:
            powerup.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        if self.boss:
            self.boss.draw(self.screen)
        for explosion in self.explosions:
            explosion.draw(self.screen)

        self.player.draw(self.screen)
        self.draw_hud()

        if self.state == 'menu':
            self.draw_center_message('GALAXY WARRIOR', 'Press ENTER to Start')
            tips = [
                'Move: Arrow Keys or W A S D',
                'Shoot: SPACE',
                'Power-ups: T = Triple, S = Shield, R = Rapid, H = Heal',
            ]
            for i, line in enumerate(tips):
                surf = self.font_small.render(line, True, WHITE)
                self.screen.blit(surf, surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90 + i * 32)))

        elif self.state == 'game_over':
            self.draw_center_message('GAME OVER', 'Press R to Restart')

        elif self.state == 'victory':
            self.draw_center_message('YOU WIN!', 'Press R to Play Again')

        if self.message and pygame.time.get_ticks() - self.message_timer < 2000 and self.state == 'playing':
            msg = self.font_medium.render(self.message, True, YELLOW)
            self.screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()