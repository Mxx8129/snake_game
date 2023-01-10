import random
from os import path
import pygame

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (35, 171, 250)
FPS = 60
snake_block = 20
snake_step = 2
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")

image_dir = path.join(path.dirname(__file__), "img")
music_dir = path.join(path.dirname(__file__), "music")

head_snake = [
    pygame.image.load(path.join(image_dir, "HeadB.png")).convert(),
    pygame.image.load(path.join(image_dir, "HeadT.png")).convert(),
    pygame.image.load(path.join(image_dir, "HeadR.png")).convert(),
    pygame.image.load(path.join(image_dir, "HeadL.png")).convert(),

]


def draw_head(i, snake_list):
    snake_head_image = head_snake[i]
    snake_head = pygame.transform.scale(snake_head_image, (snake_block, snake_block)).convert()
    snake_head.set_colorkey(BLACK)
    snake_head_rect = snake_head.get_rect(x=snake_list[-1][0], y=snake_list[-1][-1])
    screen.blit(snake_head, snake_head_rect)


def eating_check(xcor, ycor, foodx, foody):
    if foodx - snake_block <= xcor <= foodx + snake_block:
        if foody - snake_block <= ycor <= foody + snake_block:
            return True
        else:
            return False


def create_message(msg, color, x, y, font_name, size):
    style = pygame.font.SysFont(font_name, size)
    message = style.render(msg, True, color)
    screen.blit(message, (x, y))


def game_loop():
    snake_list = []
    food_images = [
        pygame.image.load(path.join(image_dir, "f_1.png")).convert(),
        pygame.image.load(path.join(image_dir, "f_2.png")).convert(),
        pygame.image.load(path.join(image_dir, "f_3.png")).convert(),
        pygame.image.load(path.join(image_dir, "f_4.png")).convert(),
        pygame.image.load(path.join(image_dir, "f_5.png")).convert(),
        pygame.image.load(path.join(image_dir, "f_6.png")).convert(),
        pygame.image.load(path.join(image_dir, "f_7.png")).convert()
    ]
    food = pygame.transform.scale(random.choice(food_images), (snake_block, snake_block))
    food.set_colorkey(WHITE)
    i = 0
    xCOR = WIDTH / 2
    yCOR = HEIGHT / 2
    x_change = 0
    y_change = 0
    length = 1
    score = 0
    foodX = random.randrange(snake_block, WIDTH - snake_block)
    foodY = random.randrange(snake_block, HEIGHT - snake_block)
    bg = pygame.image.load(path.join(image_dir, "Fon_grass4_1.jpg"))
    food_rect = food.get_rect(x=foodX, y=foodY)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_rect = bg.get_rect()
    pygame.mixer.music.load(path.join(music_dir, "Intense.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    am = pygame.mixer.Sound(path.join(music_dir, "apple_bite.ogg"))
    am.set_volume(0.1)

    run = True
    game_close = False
    while run:
        clock.tick(FPS)
        screen.fill(BLUE)
        screen.blit(bg, bg_rect)
        create_message(f'Ваш счёт равен: {score}', RED, 10, 10, "comicsans", 18)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    i = 1
                    x_change = 0
                    y_change -= snake_step
                elif event.key == pygame.K_s:
                    i = 0
                    x_change = 0
                    y_change += snake_step
                elif event.key == pygame.K_a:
                    i = 3
                    y_change = 0
                    x_change -= snake_step
                elif event.key == pygame.K_d:
                    i = 2
                    y_change = 0
                    x_change += snake_step
        xCOR += x_change
        yCOR += y_change
        if xCOR >= WIDTH or xCOR <= 0 or yCOR >= HEIGHT or yCOR <= 0:
            run = False
            game_close = True
            pygame.mixer.music.load(path.join(music_dir, "hit_wall.mp3"))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.load(path.join(music_dir, "lose_game.mp3"))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.1)

        snake_head = [xCOR, yCOR]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        for x in snake_list[1:]:
            snake_image = pygame.image.load(path.join(image_dir, "body3.png")).convert()
            snake = pygame.transform.scale(snake_image, (snake_block, snake_block))
            snake.set_colorkey(WHITE)
            screen.blit(snake, (x[0], x[1]))

        for body in snake_list[1:-1]:
            if body == snake_head:
                run = False
                game_close = True
                pygame.mixer.music.load(path.join(music_dir, "lose_game.mp3"))
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.1)

        screen.blit(food, food_rect)
        draw_head(i, snake_list)
        if eating_check(xCOR, yCOR, foodX, foodY):
            score += 1
            length += 6
            foodX = random.randrange(snake_block, WIDTH - snake_block)
            foodY = random.randrange(snake_block, HEIGHT - snake_block)
            food_images = [
                pygame.image.load(path.join(image_dir, "f_1.png")).convert(),
                pygame.image.load(path.join(image_dir, "f_2.png")).convert(),
                pygame.image.load(path.join(image_dir, "f_3.png")).convert(),
                pygame.image.load(path.join(image_dir, "f_4.png")).convert(),
                pygame.image.load(path.join(image_dir, "f_5.png")).convert(),
                pygame.image.load(path.join(image_dir, "f_6.png")).convert(),
                pygame.image.load(path.join(image_dir, "f_7.png")).convert()
            ]
            food = pygame.transform.scale(random.choice(food_images), (snake_block, snake_block))
            food.set_colorkey(WHITE)
            food_rect = food.get_rect(x=foodX, y=foodY)
            am.play()

        while game_close:
            screen.fill(BLACK)
            create_message("Вы проиграли", RED, 250, 150, "comicsans", 50)
            create_message("Для выхода нажмите - \'q\'", WHITE, 50, 220, "comicsans", 25)
            create_message("Для перезагрузки нажмите - \'r\'", WHITE, 385, 220, "comicsans", 25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        game_close = False
                    elif event.key == pygame.K_r:
                        game_loop()
            pygame.display.update()

        pygame.display.flip()


game_loop()
pygame.quit()