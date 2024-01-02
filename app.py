import pygame
import random
import sys  # Import sys for sys.exit()
from pygame import mixer

# Inicialização do Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
METEOR_WIDTH = 50
METEOR_HEIGHT = 50
METEOR_COUNT_MIN = 5
METEOR_COUNT_MAX = 10

# Variável de saúde do jogador
player_health = 3

# Configurações da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space da Transformação")

# Outras configurações
clock = pygame.time.Clock()

# Imagem de fundo
background = pygame.image.load('images/background/img1.jpg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Configurações de fontes
font = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        screen.fill((0, 0, 0))  # Preenche a tela com a cor preta
        text_line1 = font.render("Space da Transformação !", True, (255, 255, 255))
        text_line2 = font.render("Pressione ESPAÇO para iniciar", True, (255, 255, 255))

        screen.blit(text_line1, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50))
        screen.blit(text_line2, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

        pygame.display.update()


# Chama a tela de introdução antes do loop principal
game_intro()

# Configurações de som
mixer.music.load('song/song1.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)
explosion_sound = mixer.Sound('song/explosion.mp3')


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, x_change, y_change):
        super().__init__()
        self.image = pygame.transform.scale(image, (METEOR_WIDTH, METEOR_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_change = x_change
        self.y_change = y_change


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Adjust size as needed
        self.image.fill((255, 255, 255))  # White color for the bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed


# Função para criar meteoros
def spawn_meteors():
    meteors = pygame.sprite.Group()
    for _ in range(random.randint(METEOR_COUNT_MIN, METEOR_COUNT_MAX)):
        meteor_image = pygame.image.load('images/vilain/img4.png')
        meteor = GameSprite(meteor_image, random.randint(100, SCREEN_WIDTH - 150),
                            random.randint(30, 180), random.uniform(-1.5, 1.5), random.uniform(1, 3))
        meteors.add(meteor)
    return meteors


# Inicialização do jogador
player_image = pygame.image.load('images/hero/hero1.png')
player_sprite = GameSprite(player_image, SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT, 0, 0)

# Inicialização dos meteoros
meteors = spawn_meteors()

# Initialize the bullet group
bullets = pygame.sprite.Group()

# Variável para controlar o tempo inicial
start_time = pygame.time.get_ticks()

# Função para mostrar a pontuação
def show_score(x, y, score):
    score_display = font.render("Points: " + str(score), True, (255, 255, 255))
    screen.blit(score_display, (x, y))


def is_collision(rect1, rect2):
    return rect1.colliderect(rect2)

class PlayerSprite(GameSprite):
    def __init__(self, image, x, y, x_change, y_change):
        super().__init__(image, x, y, x_change, y_change)

    def shoot(self):
        bullet = Bullet(self.rect.x + PLAYER_WIDTH // 2, self.rect.y, 5)  # Adjust speed as needed
        bullets.add(bullet)

# Inicialização do jogador
player_image = pygame.image.load('images/hero/hero1.png')
player_sprite = PlayerSprite(player_image, SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT, 0, 0)
# Variável para controlar o tempo inicial
start_time = pygame.time.get_ticks()

# Initialize score_val
score_val = 0

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_sprite.x_change = -3
            elif event.key == pygame.K_RIGHT:
                player_sprite.x_change = 3
            elif event.key == pygame.K_UP:
                player_sprite.y_change = -3
            elif event.key == pygame.K_DOWN:
                player_sprite.y_change = 3
            elif event.key == pygame.K_SPACE:
                player_sprite.shoot()  # Call the shoot method when space is pressed
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_sprite.x_change = 0
            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                player_sprite.y_change = 0
    screen.blit(background, (0, 0))


    # Calcular o tempo decorrido
    elapsed_time = pygame.time.get_ticks() - start_time

    # Aumentar a pontuação com o tempo
    score_val = int(elapsed_time / 1000)  # Aumenta 1 ponto a cada segundo

    # Atualização da posição do jogador
    player_sprite.rect.x += player_sprite.x_change
    player_sprite.rect.y += player_sprite.y_change

    screen.blit(player_sprite.image, (player_sprite.rect.x, player_sprite.rect.y))
    show_score(10, 10, score_val)
    # Atualização da posição dos meteoros
    for meteor in meteors:
        meteor.rect.x += meteor.x_change
        meteor.rect.y += meteor.y_change

        if meteor.rect.x >= SCREEN_WIDTH - METEOR_WIDTH or meteor.rect.x <= 0:
            meteor.x_change *= -1

        if meteor.rect.y >= SCREEN_HEIGHT:
            meteor.rect.y = -meteor.rect.height
            meteor.rect.x = random.randint(100, SCREEN_WIDTH - 150)

        if is_collision(player_sprite.rect, meteor.rect):
            player_health -= 1
            explosion_sound.play()
            meteor.rect.y = random.randint(-METEOR_HEIGHT, 0)
            meteor.rect.x = random.randint(100, SCREEN_WIDTH - 150)

    # Atualização da posição das balas
    bullets.update()

    # Verificar colisão entre jogador e meteoros
    collisions = pygame.sprite.spritecollide(player_sprite, meteors, False)
    if collisions:
        player_health -= 1
        explosion_sound.play()
        for meteor in collisions:
            meteor.rect.y = random.randint(-METEOR_HEIGHT, 0)
            meteor.rect.x = random.randint(100, SCREEN_WIDTH - 150)

    # Verificar colisão entre balas e meteoros
    bullet_meteor_collisions = pygame.sprite.groupcollide(bullets, meteors, True, True)

    # Calcular o tempo decorrido
    elapsed_time = pygame.time.get_ticks() - start_time

    # Aumentar a pontuação com o tempo
    score_val = int(elapsed_time / 1000)  # Aumenta 1 ponto a cada segundo

    if player_health <= 0:
        game_over()
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    if player_sprite.rect.x <= 0:
        player_sprite.rect.x = 0
    elif player_sprite.rect.x >= SCREEN_WIDTH - PLAYER_WIDTH:
        player_sprite.rect.x = SCREEN_WIDTH - PLAYER_WIDTH

    if player_sprite.rect.y <= 0:
        player_sprite.rect.y = 0
    elif player_sprite.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_sprite.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT

    screen.blit(player_sprite.image, (player_sprite.rect.x, player_sprite.rect.y))
    show_score(10, 10, score_val)

    for meteor in meteors:
        screen.blit(meteor.image, (meteor.rect.x, meteor.rect.y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
