import pygame
import sys
import os

# Инициализация
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong с звуками")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ракетки и мяч
paddle_width, paddle_height = 20, 100
ball_size = 20
left_paddle = pygame.Rect(20, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH//2 - ball_size//2, HEIGHT//2 - ball_size//2, ball_size, ball_size)

# Скорости
left_speed, right_speed = 0, 0
ball_speed_x, ball_speed_y = 5, 5

# Счёт
left_score, right_score = 0, 0
font = pygame.font.Font(None, 74)

# Звуки 
try:
    bounce_sound = pygame.mixer.Sound("bounce.wav")  # Отскок мяча
    score_sound = pygame.mixer.Sound("score.wav")    # Очки
    paddle_sound = pygame.mixer.Sound("paddle.wav")  # Движение ракетки
except:
    # Если файлов нет - загружаем системные звуки pygame
    bounce_sound = None
    score_sound = None
    paddle_sound = None
    print("Звуковые файлы не найдены. Скачайте bounce.wav, score.wav, paddle.wav")

def draw_net():
    for i in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 2, i, 4, 10))

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: 
                left_speed = -7
                if paddle_sound: paddle_sound.play()
            if event.key == pygame.K_s: 
                left_speed = 7
                if paddle_sound: paddle_sound.play()
            if event.key == pygame.K_UP: 
                right_speed = -7
                if paddle_sound: paddle_sound.play()
            if event.key == pygame.K_DOWN: 
                right_speed = 7
                if paddle_sound: paddle_sound.play()
        elif event.type == pygame.KEYUP:
            left_speed = 0
            right_speed = 0

    # Движение ракеток (исправленная граница)
    left_paddle.y = max(0, min(HEIGHT - paddle_height, left_paddle.y + left_speed))
    right_paddle.y = max(0, min(HEIGHT - paddle_height, right_paddle.y + right_speed))

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Отскок от верха/низа
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        if bounce_sound: bounce_sound.play()

    # Отскок от ракеток
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        if bounce_sound: bounce_sound.play()

    # Очки
    if ball.left <= 0:
        right_score += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1
        if score_sound: score_sound.play()
    if ball.right >= WIDTH:
        left_score += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1
        if score_sound: score_sound.play()

    # Отрисовка
    screen.fill(BLACK)
    draw_net()
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH//4, 20))
    screen.blit(right_text, (3*WIDTH//4, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
