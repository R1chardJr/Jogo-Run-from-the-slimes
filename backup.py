# main.py
WIDTH = 800
HEIGHT = 600
TITLE = "Run from the Slimes"

import math
import random
from pygame import Rect


# Estado do jogo
game_state = "menu"
music_on = True
sound_on = True

# Música
music.play("musica_fundo")
music.set_volume(0.5)

# Botões do menu
button_width = 250
button_height = 60
button_x = (WIDTH - button_width) // 2

buttons = {
    "start": Rect(button_x, 200, button_width, button_height),
    "toggle_sound": Rect(button_x, 300, button_width, button_height),
    "quit": Rect(button_x, 400, button_width, button_height)
}

# Plataforma simples
floor_y = HEIGHT - 210

# --- CLASSES ---

class Player:
    def __init__(self):
        self.actor = Actor("hero_idle1", (WIDTH // 2, floor_y))
        self.vel_y = 0
        self.on_ground = True
        self.idle_frames = ["hero_idle1", "hero_idle2"]
        self.walk_frames = ["hero_walk1", "hero_walk2", "hero_walk3"]
        self.jump_frame = "hero_idle1"
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 0.2
        self.moving = False

    def update(self, dt):
        self.moving = False

        # Movimento lateral
        if keyboard.left:
            if self.actor.x > 0:
                self.actor.x -= 4
                self.actor.angle = 0
            self.moving = True
        elif keyboard.right:
            if self.actor.x < WIDTH:
                self.actor.x += 4
                self.actor.angle = 0
            self.moving = True

        # Pulo
        if keyboard.up and self.on_ground:
            self.vel_y = -10
            self.on_ground = False
            if sound_on:
                sounds.jump.play()

        # Gravidade
        self.vel_y += 0.5
        self.actor.y += self.vel_y

        # Verifica colisão com plataformas
        self.on_ground = False
        player_rect = Rect(
            self.actor.x - self.actor.width // 2,
            self.actor.y - self.actor.height // 2,
            self.actor.width,
            self.actor.height
        )

        for plat in platforms:
            plat_rect = plat.get_rect()
            if player_rect.colliderect(plat_rect) and self.vel_y >= 0:
                if player_rect.bottom - self.vel_y <= plat_rect.top:
                    # Está em cima da plataforma
                    self.actor.y = plat_rect.top - self.actor.height // 2
                    self.vel_y = 0
                    self.on_ground = True
                    break

        # Animação
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % (len(self.walk_frames) if self.moving else len(self.idle_frames))
            if not self.on_ground:
                self.actor.image = self.jump_frame
            else:
                self.actor.image = self.walk_frames[self.frame_index] if self.moving else self.idle_frames[self.frame_index]


    def draw(self):
        self.actor.draw()

    def collides_with(self, enemy):
        return self.actor.colliderect(enemy.actor)


class Enemy:
    def __init__(self, x, y, patrol_width=150):
        self.actor = Actor("vilain_iddle1", (x, y))
        self.idle_frames = [f"vilain_iddle{i}" for i in range(1, 11)]
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 0.15
        self.start_x = x
        self.patrol_width = patrol_width
        self.direction = 1

    def update(self, dt):
        self.actor.x += self.direction * 2
        if self.actor.x > self.start_x + self.patrol_width or self.actor.x < self.start_x - self.patrol_width:
            self.direction *= -1

        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
            self.actor.image = self.idle_frames[self.frame_index]

    def draw(self):
        self.actor.draw()

class Platform:
    def __init__(self, x, y, image="platform_grass", base=False):
        self.base = base
        if not base:
            self.actor = Actor(image, (x, y))
        self.x = x
        self.y = y

    def draw(self):
        if not self.base:
            self.actor.draw()

    def get_rect(self):
        if self.base:
            return Rect(0, self.y - 16, WIDTH, 32)
        else:
            padding = 20  # reduz a largura da colisão em 20px de cada lado
            return Rect(
                self.actor.x - self.actor.width // 2 + padding,
                self.actor.y - self.actor.height // 2,
                self.actor.width - 2 * padding,
                self.actor.height
            )


# --- Instâncias ---

player = Player()
enemies = []
score = 0
enemy_spawn_timer = 0
enemy_spawn_interval = 3
enemy_removal_timer = 10  
MAX_ENEMIES = 8

platforms = [
    Platform(x, HEIGHT - 250) 
    for x in [120, 140, 160, 180, 300, 320, 340, 360, 480, 500, 520, 540, 660, 680, 700, 720]
] + [Platform(WIDTH // 2, floor_y + 32, base=True)]  # Chão fixo
# --- FUNÇÕES DE JOGO ---

def draw():
    screen.clear()

    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        screen.blit("bg", (0, 0))
        screen.draw.text(f"Pontos: {int(score)}", topleft=(10, 10), fontsize=40, color="white")
        for plat in platforms[:-1]:
            plat.draw()
        player.draw()
        for e in enemies:
            e.draw()
    elif game_state == "gameover":
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        screen.draw.text("Pressione ESC para voltar ao menu", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="white")

def draw_menu():
    screen.blit("imagem_fundo", (0, 0))
    screen.draw.text("Run from the Slimes", center=(WIDTH // 2, 100), fontsize=100,color = "green")

    screen.draw.filled_rect(buttons["start"], "orange")
    screen.draw.text("Comecar o jogo", center=buttons["start"].center, fontsize=30, color="black")

    screen.draw.filled_rect(buttons["toggle_sound"], "orange")
    status = "Ligado" if music_on else "Desligado"
    screen.draw.text(f"Musica/Sons: {status}", center=buttons["toggle_sound"].center, fontsize=30, color="black")

    screen.draw.filled_rect(buttons["quit"], "orange")
    screen.draw.text("Saida", center=buttons["quit"].center, fontsize=30, color="black")

def update(dt):
    global game_state, enemy_spawn_timer, enemy_removal_timer, score

    if game_state == "playing":
        player.update(dt)
        score += dt * 10

        # Atualiza inimigos
        new_enemies = []
        for e in enemies:
            e.update(dt)
            if player.collides_with(e):
                game_state = "gameover"
                if sound_on:
                    sounds.game_over.play()
            else:
                new_enemies.append(e)
        enemies[:] = new_enemies

        # Remove inimigo mais antigo a cada 10s
        enemy_removal_timer += dt
        if enemy_removal_timer >= 10 and len(enemies) > 1:
            enemies.pop(0)
            enemy_removal_timer = 0

        # Spawn de novos inimigos
        enemy_spawn_timer += dt
        if enemy_spawn_timer >= enemy_spawn_interval and len(enemies) < MAX_ENEMIES:
            enemy_spawn_timer = 0
            spawnable_platforms = [p for p in platforms if not p.base]
            if spawnable_platforms:
                plat = random.choice(spawnable_platforms)
                while True:
                    spawn_x = random.randint(0, WIDTH-20)
                    if abs(spawn_x - player.actor.x) >= 10:
                        break  # Aceita se distância no eixo X for maior ou igual a 10

                spawn_y = plat.actor.y + 50
                enemies.append(Enemy(spawn_x, spawn_y))


def reset_game():
    global player, enemies, enemy_spawn_timer,score

    player = Player()
    enemies = []
    enemy_spawn_timer = 0
    score = 0

def on_mouse_down(pos):
    global game_state, music_on, sound_on

    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            reset_game()
            game_state = "playing"
        elif buttons["toggle_sound"].collidepoint(pos):
            music_on = not music_on
            sound_on = not sound_on
            if music_on:
                music.play("musica_fundo")
            else:
                music.stop()
        elif buttons["quit"].collidepoint(pos):
            exit()

def on_key_down(key):
    global game_state
    if key == keys.ESCAPE and (game_state == "playing" or game_state == "gameover"):
        game_state = "menu"
        reset_game()
