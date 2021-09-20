import pygame
import random
import math
from pygame import mixer

pygame.init()

# Screen size
screen = pygame.display.set_mode((800, 600))

# changing title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Background image
background = pygame.image.load("background.png")

# player image
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy Image
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for x in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(40, 140))
    enemyX_change.append(5)
    enemyY_change.append(40)


# Bullet Image
bulletImg = pygame.image.load("Bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"  # Bullet state help us determine whether our bullet is at rest or in motion

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Display score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
change_speed = 5

textX = 10  # the score coordinate on the screen
textY = 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)

# High score
with open("HighScore.txt") as highscore_handle2:
    h = highscore_handle2.read()
    if h == "":
        h = "0"
    highscore_value = int(h)  # open the highscore file and load the previous high score into the high score variable

highscore_handle = open("HighScore.txt", "w")  # open the high score text file and get ready to erite to it

highscore_font = pygame.font.Font("freesansbold.ttf", 32)


def display_highscore():
    highscore_display = highscore_font.render("High Score: " + h, True, (255, 255, 255))
    screen.blit(highscore_display, (500, 10))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(textX, textY):
    # rendering the score
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (textX, textY))

# draw player


def player(x, y):
    screen.blit(playerImg, (x, y))

# draw enemy


def enemy(x, y, i):  # i used i here and used x when calling it, they are the same thing
    screen.blit(enemyImg[i], (x, y))

# fire bullet


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Check if bullet is touching enemy


def ifcollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt(math.pow(bulletX - enemyX, 2) + math.pow(bulletY - enemyY, 2))
    if distance <= 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    screen.fill((82, 0, 55))

    # BACKGROUND
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save high score before shut down
            highscore_string = str(highscore_value)
            highscore_handle.write(highscore_string)

            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 7
            if event.key == pygame.K_RIGHT:
                playerX_change += 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX  # Get X coordinate of Spaceship
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # setting boundaries for the player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for x in range(num_of_enemies):

        if enemyY[x] > 450:
            for i in range(num_of_enemies):
                enemyY[i] = 2000
            game_over_text()
            break

        # Increase the speed of the enemies as the game continues
        if score_value >= change_speed:
            enemyX_change[x] += 5
            change_speed += 5
            bulletY_change += 5

        enemyX[x] += enemyX_change[x]

        if enemyX[x] <= 0:
            enemyX_change[x] = 5
            enemyY[x] += enemyY_change[x]
        elif enemyX[x] >= 736:
            enemyX_change[x] = -5
            enemyY[x] += enemyY_change[x]

        # Check if bullet is touching enemy
        collision = ifcollision(bulletX, bulletY, enemyX[x], enemyY[x])
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[x] = random.randint(0, 736)
            enemyY[x] = random.randint(40, 140)
            if score_value > highscore_value:
                highscore_value = score_value  # Change highscore value if score is higher than highscore

        enemy(enemyX[x], enemyY[x], x)

    # Bullet movement
    if bulletY <= 0:  # make bullet ready for another fire when it touches the edge
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":  # fire the bullet
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    display_highscore()

    pygame.display.update()  # so the screen will keep updating as long as the program keeps running
