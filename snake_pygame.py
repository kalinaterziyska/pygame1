import random
import pygame

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (102, 0, 0)
red2 = (153, 0, 76)
green = (0, 255, 0)
blue = (65, 242, 242)

dis_width = 700
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Kalina's Snake Game")

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 13

font_style = pygame.font.SysFont("spendthrift", 25)
score_font = pygame.font.SysFont("cosmeticians", 35)


def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], block, block])


def message(msg, color):
    my_message = font_style.render(msg, True, color)
    dis.blit(my_message, [dis_width / 6, dis_height / 3])


def game_loop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    current_direction_x = 0
    current_direction_y = 0

    snake_list = []
    length_of_snake = 1

    foods = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    fody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    if current_direction_x != snake_block:
                        current_direction_x = -snake_block
                        current_direction_y = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if current_direction_x != -snake_block:
                        current_direction_x = snake_block
                        current_direction_y = 0
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if current_direction_y != snake_block:
                        current_direction_x = 0
                        current_direction_y = -snake_block
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if current_direction_y != -snake_block:
                        current_direction_x = 0
                        current_direction_y = snake_block

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += current_direction_x
        y1 += current_direction_y

        dis.fill(blue)
        pygame.draw.rect(dis, red2, [foods, fody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foods and y1 == fody:
            foods = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            fody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_loop()
