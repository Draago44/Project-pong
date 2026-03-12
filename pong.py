import pygame
import random
import sys

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
PADDLE_W, PADDLE_H = 20, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED_MIN, BALL_SPEED_MAX = 5, 9


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_W, PADDLE_H)
        self.speed = 0

    def move(self, direction):
        self.speed = direction * PADDLE_SPEED

    def stop(self):
        self.speed = 0

    def update(self):
        self.rect.y += self.speed
        self.rect.y = max(0, min(HEIGHT - PADDLE_H, self.rect.y))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_MIN
        self.speed_y = BALL_SPEED_MIN
        self.prev_rect = self.rect.copy()

    def update(self):
        self.prev_rect = self.rect.copy()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x = random.randint(BALL_SPEED_MIN, BALL_SPEED_MAX) * random.choice([-1, 1])
        self.speed_y = random.randint(BALL_SPEED_MIN, BALL_SPEED_MAX) * random.choice([-1, 1])
        self.prev_rect = self.rect.copy()

    def check_wall_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = abs(self.speed_y)
            return True
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = -abs(self.speed_y)
            return True
        return False

    def check_paddle_collision(self, paddle):
        if not self.rect.colliderect(paddle.rect):
            return False

        dx = self.rect.centerx - self.prev_rect.centerx
        dy = self.rect.centery - self.prev_rect.centery

        overlap_left = self.rect.right - paddle.rect.left
        overlap_right = paddle.rect.right - self.rect.left
        overlap_top = self.rect.bottom - paddle.rect.top
        overlap_bottom = paddle.rect.bottom - self.rect.top

        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left and dx > 0:
            self.rect.right = paddle.rect.left
            self.speed_x = -abs(self.speed_x)
            self._apply_angle_effect(paddle, 'x')
        elif min_overlap == overlap_right and dx < 0:
            self.rect.left = paddle.rect.right
            self.speed_x = abs(self.speed_x)
            self._apply_angle_effect(paddle, 'x')
        elif min_overlap == overlap_top and dy > 0:
            self.rect.bottom = paddle.rect.top
            self.speed_y = -abs(self.speed_y)
        elif min_overlap == overlap_bottom and dy < 0:
            self.rect.top = paddle.rect.bottom
            self.speed_y = abs(self.speed_y)
        else:
            if abs(dx) > abs(dy):
                self.speed_x *= -1
                self._apply_angle_effect(paddle, 'x')
            else:
                self.speed_y *= -1
        return True

    def _apply_angle_effect(self, paddle, axis):
        if axis == 'x':
            relative_intersect = (paddle.rect.centery - self.rect.centery) / (PADDLE_H / 2)
            self.speed_y = -relative_intersect * abs(self.speed_x) * 0.7
            self.speed_x *= 1.03

    def draw(self, surface):
        pygame.draw.ellipse(surface, WHITE, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("IgnaPong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)

        self.left_paddle = Paddle(20, HEIGHT//2 - PADDLE_H//2)
        self.right_paddle = Paddle(WIDTH - 40, HEIGHT//2 - PADDLE_H//2)
        self.ball = Ball()
        self.left_score = 0
        self.right_score = 0

        self.keys = {'w': False, 's': False, 'up': False, 'down': False}

        self.bounce_sound = self._load_sound("bounce.wav")
        self.score_sound = self._load_sound("score.wav")
        self.paddle_sound = self._load_sound("paddle.wav")

    def _load_sound(self, filename):
        try:
            return pygame.mixer.Sound(filename)
        except:
            return None

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.keys['w'] = True
                    self.left_paddle.move(-1)
                    if self.paddle_sound:
                        self.paddle_sound.play()
                elif event.key == pygame.K_s:
                    self.keys['s'] = True
                    self.left_paddle.move(1)
                    if self.paddle_sound:
                        self.paddle_sound.play()
                elif event.key == pygame.K_UP:
                    self.keys['up'] = True
                    self.right_paddle.move(-1)
                    if self.paddle_sound:
                        self.paddle_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.keys['down'] = True
                    self.right_paddle.move(1)
                    if self.paddle_sound:
                        self.paddle_sound.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.keys['w'] = False
                    if self.keys['s']:
                        self.left_paddle.move(1)
                    else:
                        self.left_paddle.stop()
                elif event.key == pygame.K_s:
                    self.keys['s'] = False
                    if self.keys['w']:
                        self.left_paddle.move(-1)
                    else:
                        self.left_paddle.stop()
                elif event.key == pygame.K_UP:
                    self.keys['up'] = False
                    if self.keys['down']:
                        self.right_paddle.move(1)
                    else:
                        self.right_paddle.stop()
                elif event.key == pygame.K_DOWN:
                    self.keys['down'] = False
                    if self.keys['up']:
                        self.right_paddle.move(-1)
                    else:
                        self.right_paddle.stop()
        return True

    def _check_scoring(self):
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.ball.reset()
            if self.score_sound:
                self.score_sound.play()
        elif self.ball.rect.right >= WIDTH:
            self.left_score += 1
            self.ball.reset()
            if self.score_sound:
                self.score_sound.play()

    def _draw_net(self):
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(self.screen, WHITE, (WIDTH//2 - 2, y, 4, 10))

    def _render(self):
        self.screen.fill(BLACK)
        self._draw_net()
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        left_text = self.font.render(str(self.left_score), True, WHITE)
        right_text = self.font.render(str(self.right_score), True, WHITE)
        self.screen.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
        self.screen.blit(right_text, (3*WIDTH//4 - right_text.get_width()//2, 20))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self._handle_input()
            self.left_paddle.update()
            self.right_paddle.update()
            self.ball.update()

            if self.ball.check_wall_collision():
                if self.bounce_sound:
                    self.bounce_sound.play()

            if self.ball.check_paddle_collision(self.left_paddle) or \
               self.ball.check_paddle_collision(self.right_paddle):
                if self.bounce_sound:
                    self.bounce_sound.play()

            self._check_scoring()
            self._render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()