import pygame
import random
import math
from pygame import mixer

# Initialization
pygame.init()

# Display creation
display = pygame.display.set_mode((1280, 720))

# background
background = pygame.image.load("background.png").convert()

# sound
mixer.music.load("backgroundsound.wav")
mixer.music.play(-1)

# Title
pygame.display.set_caption("Monsters on Space")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Spaceship
spaceshipImg = pygame.image.load('spaceship.png')
spaceshipX = 620
spaceshipY = 600
spaceshipX_move = 0

# Monster
monsterImg = []
monsterX = []
monsterY = []
monsterX_move = []
monsterY_move = []
number_of_monsters = 8

for i in range(number_of_monsters):
    monsterImg.append(pygame.image.load('monster.png'))
    monsterX.append(random.randint(0, 1215))
    monsterY.append(random.randint(50, 300))
    monsterX_move.append(1)
    monsterY_move.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 600
bulletX_move = 1
bulletY_move = 5
bullet_state = "not fired"

# Score
point = 0
font = pygame.font.Font('Windsong.ttf', 70)
textX = 10
textY = 10

# Game over text
gofont = pygame.font.Font('Windsong.ttf', 140)


def show_score(x, y):
    score = font.render("Score: " + str(point), True, (255, 255, 255))
    display.blit(score, (x, y))


def gameover_text():
    gotext = gofont.render("GAME OVER", True, (255, 255, 255))
    display.blit(gotext, (320, 180))


def spaceship(x, y):
    display.blit(spaceshipImg, (x, y))


def monster(x, y, i):
    display.blit(monsterImg[i], (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fired"
    display.blit(bulletImg, (x + 16, y + 10))


def isCollision(monsterX, monsterY, bulletX, bulletY):
    distance = math.sqrt((math.pow(monsterX - bulletX, 2)) + (math.pow(monsterY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Run Game
open = True
while open:
    display.fill((0, 0, 0))
    display.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            open = False
        if event.type == pygame.KEYDOWN:
            print("Pressed")
            if event.key == pygame.K_a:
                spaceshipX_move = -1.8
            if event.key == pygame.K_d:
                spaceshipX_move = 1.8
            if event.key == pygame.K_SPACE:
                if bullet_state is "not fired":
                    bullet_sound = mixer.Sound("firesound.wav")
                    bullet_sound.play()
                    bulletX = spaceshipX
                    firebullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                print("Released")
                spaceshipX_move = 0

    # Spaceship movement
    spaceshipX += spaceshipX_move
    if spaceshipX <= 0:
        spaceshipX = 0
    elif spaceshipX >= 1216:
        spaceshipX = 1216

    # Monster movement
    for i in range(number_of_monsters):
        # Game over
        if monsterY[i] > 528:
            for j in range(number_of_monsters):
                monsterY[j] = 2000
            gameover_text()
            break

        monsterX[i] += monsterX_move[i]
        if monsterX[i] <= 0:
            monsterX_move[i] = 1.0
            monsterY[i] += monsterY_move[i]
        elif monsterX[i] >= 1216:
            monsterX_move[i] = -1.0
            monsterY[i] += monsterY_move[i]

        # Collision
        collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            bulletY = 600
            bullet_state = "not fired"
            point += 1
            print(point)
            monsterX[i] = random.randint(0, 1215)
            monsterY[i] = random.randint(50, 300)

        monster(monsterX[i], monsterY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 600
        bullet_state = "not fired"
    if bullet_state is "fired":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_move

    spaceship(spaceshipX, spaceshipY)
    show_score(textX, textY)
    pygame.display.update()
