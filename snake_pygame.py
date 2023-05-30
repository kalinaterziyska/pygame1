import random
import pygame
import pygame.mixer

pygame.init()

white = (255, 255, 255)
purple = (153, 0, 153)
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
apple_img = pygame.transform.scale(apple_img, (int(snake_block * 1.5), int(snake_block * 1.5)))

eat_sound = pygame.mixer.Sound("eat_sound.mp3")
death_sound = pygame.mixer.Sound("game_over_sound.wav")


def show_menu():
    menu_running = True
    option = 1

    while menu_running:
        dis.fill(blue)
        message("Snake Game Menu", black, y_offset=-50)
        message("Choose an option:", black, y_offset=50)
        message("1. Play with Walls", black, y_offset=100)
        message("2. Play without Obstacles", black, y_offset=150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    option = 1
                    menu_running = False
                elif event.key == pygame.K_2:
                    option = 2
                    menu_running = False

        pygame.display.update()

    return option


def your_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    dis.blit(value, [10, 770])


def our_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], block, block])

    if len(snake_list) > 0:
        x1, y1 = snake_list[-1]
        left_eye = (x1 + block // 3, y1 + block // 3)
        right_eye = (x1 + 2 * block // 3, y1 + block // 3)
        pygame.draw.circle(dis, white, left_eye, block // 10)
        pygame.draw.circle(dis, white, right_eye, block // 10)


def message(msg, color, y_offset=0):
    text = font_style.render(msg, True, color)
    text_rect = text.get_rect(center=(dis_width / 2, dis_height / 2 + y_offset))
    dis.blit(text, text_rect)


def is_collision(x1, y1, x2, y2, collision_range):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    if distance < collision_range:
        pygame.mixer.Sound.play(eat_sound)
        return True
    return False


def game_loop(option):
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

    if option == 1:
        obstacle_positions = []
        num_obstacles = 10

        for _ in range(num_obstacles):
            while True:
                obstacle_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                obstacle_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                obstacle_pos = (obstacle_x, obstacle_y)

                if (
                    obstacle_pos not in obstacle_positions
                    and (obstacle_x, obstacle_y) != (food_x, food_y)
                    and (obstacle_x, obstacle_y) != (food_x - snake_block, food_y)
                    and (obstacle_x, obstacle_y) != (food_x - 2 * snake_block, food_y)
                ):
                    obstacle_positions.append(obstacle_pos)
                    break

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.mixer.Sound.play(death_sound)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop(option)

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

        if option == 1:
            for obstacle_pos in obstacle_positions:
                if x1 == obstacle_pos[0] and y1 == obstacle_pos[1]:
                    game_close = True
                    pygame.mixer.Sound.play(death_sound)
        else:
            if x1 >= dis_width:
                x1 = 0
            elif x1 < 0:
                x1 = dis_width - snake_block
            elif y1 >= dis_height:
                y1 = 0
            elif y1 < 0:
                y1 = dis_height - snake_block

        x1 += current_direction_x
        y1 += current_direction_y

        dis.fill(blue)
        dis.blit(apple_img, (food_x, food_y))

        if option == 1:
            for obstacle_pos in obstacle_positions:
                pygame.draw.rect(dis, purple, [obstacle_pos[0], obstacle_pos[1], snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
                pygame.mixer.Sound.play(death_sound)

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


selected_option = show_menu()
game_loop(selected_option)
