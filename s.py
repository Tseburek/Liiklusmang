#github: https://github.com/Tseburek/Liiklusmang
import pygame
import random

pygame.init()

# Ekraani suurus
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Liiklusmäng')

# Värvid
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (200, 50, 50)

# Skoor
score = 0

# Mängu kiirus (muutub vastavalt raskusastmele)
difficulty = "Lihtne"
enemy_speed = 5  # Vaikeväärtus (muutub)

# Piltide laadimine
background_image = pygame.image.load('bg_rally.jpg')
red_car_image = pygame.image.load('f1_red.png')
blue_car_image = pygame.image.load('f1_blue.png')

# Piltide suuruse muutmine
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
red_car_image = pygame.transform.scale(red_car_image, (50, 100))
blue_car_image = pygame.transform.scale(blue_car_image, (50, 100))

#rotate neid õigeit pidi
blue_car_image = pygame.transform.rotate(blue_car_image,180)
red_car_image = pygame.transform.rotate(red_car_image,360)

# Punase auto algasukoht (mängija)
red_car = red_car_image.get_rect(center=(WIDTH // 2, HEIGHT - 60))

# **Tee piirid**
LEFT_BORDER = 150
RIGHT_BORDER = WIDTH - 100 - red_car.width

# Mängu kell
clock = pygame.time.Clock()

# **Menu funktsioon**
def main_menu():
    global difficulty, enemy_speed, score

    running = True
    while running:
        screen.fill(GRAY)

        #Pealkiri
        font = pygame.font.Font(None, 50)
        title_text = font.render("Liiklusmäng", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Mängi
        play_rect = pygame.Rect(WIDTH // 2 - 100, 150, 200, 50)
        pygame.draw.rect(screen, WHITE, play_rect)
        play_text = font.render("Mängi", True, BLACK)
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 160))

        # Raskuse nupu valik
        diff_rect = pygame.Rect(WIDTH // 2 - 200, 250, 400, 50)
        pygame.draw.rect(screen, WHITE, diff_rect)
        diff_text = font.render(f"Raskus: {difficulty}", True, BLACK)
        screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):  # If "Play" is clicked
                    score = 0  # Reset score before starting
                    return  # Exit menu and start game
                if diff_rect.collidepoint(event.pos):  #kui vajutatud "difficulty peale"
                    if difficulty == "Lihtne":
                        difficulty = "Keskmine"
                        enemy_speed = 5
                    elif difficulty == "Keskmine":
                        difficulty = "Raske"
                        enemy_speed = 8
                    else:
                        difficulty = "Lihtne"
                        enemy_speed = 3
                        # description

# Mäng läbi funktsioon
def game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("Mäng läbi! Su skoor: " + str(score), True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

    pygame.display.flip()
    pygame.time.delay(3000)  # Oota 3 sek

    main_menu()  #mine menüsse tagasi

# Põhi funktsioon

screenX = WIDTH
screenY = HEIGHT

coords = []
for i in range (10):
    posX = random.randint(1,screenX)
    posY = random.randint(1,screenY)
    speed = random.randint(10,20)
    coords.append([posX, posY, speed])


def game_loop():
    global score

    #Genereeri siniseid autosi
    blue_cars = [
        pygame.Rect(random.randint(LEFT_BORDER, RIGHT_BORDER), random.randint(-300, -8), 50, 100)
        for _ in range(3)
    ]

    red_car.x = WIDTH // 2.2  # Punased autod #pythonile ei meeldi see aga see töötab
    red_car.y = HEIGHT - 120

    vel = 10  # Mänguja kiirus


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # AUTO LIIKUMINE KLAVATUURILT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and red_car.left > LEFT_BORDER:
            red_car.x -= vel
        if keys[pygame.K_RIGHT] and red_car.right < RIGHT_BORDER:
            red_car.x += vel
        if keys[pygame.K_UP] and red_car.top > 0:
            red_car.y -= vel
        if keys[pygame.K_DOWN] and red_car.bottom < HEIGHT:
            red_car.y += vel

        # Liiguta siniseid autosid alla
        for car in blue_cars:
            car.y += enemy_speed  # Muudab kiirust raskusastme järgi
            if car.y > HEIGHT:
                car.y = random.randint(-300, -100)
                car.x = random.randint(LEFT_BORDER, RIGHT_BORDER)
                score += 10

            # **Collision Detection**
            if red_car.colliderect(car):
              #  explosion = pygame.image.load('explode.jpg')
                #explodee = pygame.transform.scale(explosion, (50, 100))


                game_over()
                return  # Exit game loop and return to menu

        # Joonista mänguekraan
        screen.blit(background_image, (0, 0))
        for car in blue_cars:
            screen.blit(blue_car_image, car)

        # Kuva skoor
        font = pygame.font.Font(None, 36)
        score_text = font.render('Skoor: ' + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))

        # Joonista punane auto
        screen.blit(red_car_image, red_car)
        if difficulty== "Raske":
            for i in range(len(coords)):
                pygame.draw.rect(screen, (0,0,255), [coords[i][0], coords[i][1], 20,20])
                coords[i][1] +=  coords[i][2]
                #kui jõuab alla, siis muudame ruduu alguspunkti
                if coords[i][1] > WIDTH:
                    coords[i][1] = random.randint(-40,-10)
                    coords[i][0] = random.randint(0,HEIGHT)
        pygame.display.flip()
        clock.tick(60)

# **Start Menu**

while True:
    main_menu()
    game_loop ()