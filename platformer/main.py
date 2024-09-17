import pygame
import sys
from random import randint
# Инициализация Pygame
pygame.init()


# Установка размеров окна и фоновой картинки
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.transform.scale(pygame.image.load('bg.jpg'), (1100,900))
bg_width, bg_height = bg.get_size()


# Установка заголовка окна
pygame.display.set_caption("Платформер")
# Загрузка музыки
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)


y_speed = 0
gravity = 0.5
jump_strength = -10
on_ground = True




platforms = [(0, bg_height, bg_width, 10),
             (600,700,100,10),
             (700, 800,100,10),
             (400,700,100,10),
             (300,600,100,10),
             (200, 500, 100, 10),
             (400, 400, 150, 10),
             (220, 300, 70,10),
             (370,200,100,10),
             (490,100,100,10)]
player = pygame.transform.scale(pygame.image.load('cat.png'), (70,70))
player_rect = player.get_rect()
player_rect.x = 100
player_rect.y = 150


pizza = pygame.transform.scale(pygame.image.load('pizza.png'), (70,70))
pizza_rect = pizza.get_rect()
pizza_rect.x = 530
pizza_rect.y = 30


mouse = pygame.transform.scale(pygame.image.load('mouse.png'), (50,50))
mouses = []
for _ in range(5):
    mouses_rect = mouse.get_rect()
    mouses_rect.x = randint(player_rect.x - 200, player_rect.x + 200)
    mouses_rect.y = randint(-300, 0)
    mouses.append(mouses_rect)


win = pygame.font.SysFont('Arial', 50).render("ММММ, ПИЦЦА", True, (0,255,0))
lose = pygame.font.SysFont('Arial', 50).render("АЙ, мышь!", True, (255,0,0))
# Определение камеры
camera = pygame.Rect(0, 0, screen_width, screen_height)


# Основной цикл игры
running = True
finish = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not finish:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player_rect.x += 5
        if keys[pygame.K_SPACE] and on_ground:
            y_speed = jump_strength
       
        y_speed += gravity
        player_rect.y += y_speed


        if y_speed != 0:
            on_ground = False
        # Обновление позиции камеры
        camera.x = player_rect.x - screen_width // 2
        camera.y = player_rect.y - screen_height // 2


        # Ограничение камеры границами фона
        camera.x = max(0, min(camera.x, bg_width - screen_width))
        camera.y = max(0, min(camera.y, bg_height - screen_height))
       
        screen.blit(bg, (-camera.x, -camera.y))
        screen.blit(player, (player_rect.x - camera.x, player_rect.y - camera.y))
        screen.blit(pizza, (pizza_rect.x - camera.x, pizza_rect.y - camera.y))
        # Проверка столкновений с платформами
        for platform in platforms:
            platform_rect = pygame.Rect(platform)
            if player_rect.colliderect(platform_rect) and y_speed > 0:
                player_rect.y = platform_rect.top - player_rect.height
                y_speed = 0
                on_ground = True
         # Рисование платформ
        for platform in platforms:
            pygame.draw.rect(screen, (0, 100, 200), (platform[0] - camera.x, platform[1] - camera.y, platform[2], platform[3]))


        if player_rect.colliderect(pizza_rect):
            screen.blit(win, (300,300))
            finish = True
        for mouses_rect in mouses:
            mouses_rect.y += 5  # Скорость падения мыши
            if mouses_rect.y > bg_height:
                mouses_rect.y = randint(-300, 0)
                mouses_rect.x = randint(player_rect.x - 200, player_rect.x + 200)
            screen.blit(mouse, (mouses_rect.x - camera.x, mouses_rect.y - camera.y))
            if player_rect.colliderect(mouses_rect):
                screen.blit(lose, (300,300))
                finish = True


    # Обновление экрана
    pygame.display.flip()
    pygame.time.delay(20)


# Завершение работы Pygame
pygame.quit()
sys.exit()