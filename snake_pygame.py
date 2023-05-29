import random
import pygame
# import pygame.mixer

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (102, 0, 0)
red2 = (153, 0, 76)
green = (0, 255, 0)
blue = (164, 210, 245)

dis_width = 800
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Kalina's Snake Game")

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

font_style = pygame.font.SysFont("spendthrift", 25)
score_font = pygame.font.SysFont("cosmeticians", 35)

apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (int(snake_block * 1.3), int(snake_block * 1.3)))

eat_sound = pygame.mixer.Sound("eat_sound.mp3")


def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], block, block])

    if len(snake_list) > 0:
        x1, y1 = snake_list[-1]
        left_eye = (x1 + block // 3, y1 + block // 3)
        right_eye = (x1 + 2 * block // 3, y1 + block // 3)
        pygame.draw.circle(dis, white, left_eye, block // 10)
        pygame.draw.circle(dis, white, right_eye, block // 10)


def message(msg, color):
    my_message = font_style.render(msg, True, color)
    dis.blit(my_message, [dis_width / 6, dis_height / 5])


def is_collision(x1, y1, x2, y2, collision_range):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    if distance < collision_range:
        pygame.mixer.Sound.play(eat_sound)
        return True
    return False


def game_loop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    current_direction_x = 0
    current_direction_y = 0

    snake_list = []
    length_of_snake = 1

    food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

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
            # pygame.mixer.Sound.play(game_over_sound)

        x1 += current_direction_x
        y1 += current_direction_y

        dis.fill(blue)
        dis.blit(apple_img, (food_x, food_y))

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

        if is_collision(x1, y1, food_x, food_y, snake_block):
            food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

            if length_of_snake % 5 == 0 and length_of_snake <= 15:
                clock.tick(snake_speed + 3)
            elif length_of_snake % 5 == 0 and 30 >= length_of_snake > 15:
                clock.tick(snake_speed + 6)
            elif length_of_snake % 5 == 0 and 45 >= length_of_snake > 30:
                clock.tick(snake_speed + 10)

            while (
                food_x < 3 * snake_block
                or food_x > dis_width - 4 * snake_block
                or food_y < 3 * snake_block
                or food_y > dis_height - 4 * snake_block
            ):
                food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

            length_of_snake += 1

        clock.tick(snake_speed + 2)

    pygame.quit()
    quit()


game_loop()


# да добавя звук при умирането и да записвам всичките скорове от едно разиграване в масив
# и да ги ижвеждам като свърши един рунд преди  да е затворен прожореца с Q
