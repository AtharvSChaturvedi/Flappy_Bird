import random
import sys
import pygame
from pygame.locals import *

# Game variables
FPS = 30
WIDTH = 289
HEIGHT = 511
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
GROUNDY = HEIGHT - 100  # Adjusted for base height
IMAGES = {}
SOUNDS = {}
PLAYER = 'gallery/images/bird.png'
PIPE = 'gallery/images/pipe.png'
BACKGROUND = 'gallery/images/background.png'

def welcomescreen():
    player_x = int(WIDTH / 5)
    player_y = int((HEIGHT - IMAGES['player'].get_height()) / 2)
    message_x = int((WIDTH - IMAGES['message'].get_width()) / 2)
    message_y = int(HEIGHT * 0.12)
    base_x = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_w):
                return

        SCREEN.blit(IMAGES['background'], (0, 0))
        SCREEN.blit(IMAGES['player'], (player_x, player_y))
        SCREEN.blit(IMAGES['message'], (message_x, message_y))
        SCREEN.blit(IMAGES['base'], (base_x, GROUNDY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def maingame():
    score = 0
    playerx = int(WIDTH / 5)
    playery = int(HEIGHT / 2)
    basex = 0

    newPipe1 = getrandomPipe()
    newPipe2 = getrandomPipe()

    upperPipes = [
        {'x': WIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': WIDTH + 200 + (WIDTH / 2), 'y': newPipe2[0]['y']}
    ]
    lowerPipes = [
        {'x': WIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': WIDTH + 200 + (WIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccV = -8  # velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccV
                    playerFlapped = True
                    SOUNDS['flap'].play()

        crash_test = isCollide(playerx, playery, upperPipes, lowerPipes)  # Check for collisions
        if crash_test:
            return

        # Score check
        playerMidPos = playerx + IMAGES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"SCORE = {score}")
                SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = IMAGES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # Move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add new pipes
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getrandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # Remove pipes that are out of screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Draw everything
        SCREEN.blit(IMAGES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, GROUNDY))
        SCREEN.blit(IMAGES['player'], (playerx, playery))

        # Display score
        mydigits = [int(x) for x in list(str(score))]
        wdth = sum(IMAGES['numbers'][digit].get_width() for digit in mydigits)
        Xoffset = (WIDTH - wdth) / 2

        for digit in mydigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, HEIGHT * 0.12))
            Xoffset += IMAGES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - IMAGES['player'].get_height() or playery < 0:
        SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = IMAGES['pipe'][0].get_height()
        if (playery < pipe['y'] + pipeHeight and
            playerx + IMAGES['player'].get_width() > pipe['x'] and
            playerx < pipe['x'] + IMAGES['pipe'][0].get_width()):
            SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + IMAGES['player'].get_height() > pipe['y'] and
            playerx + IMAGES['player'].get_width() > pipe['x'] and
            playerx < pipe['x'] + IMAGES['pipe'][0].get_width()):
            SOUNDS['hit'].play()
            return True

    return False

def getrandomPipe():
    pipeHeight = IMAGES['pipe'][0].get_height()
    baseHeight = IMAGES['base'].get_height()
    offset = HEIGHT / 3

    # Ensure y2 has a valid range
    maxPipeY = HEIGHT - baseHeight - int(1.2 * offset)
    if maxPipeY <= offset:  # Avoid invalid range
        maxPipeY = int(offset + 10)  # Set a minimum valid range

    y2 = offset + random.randrange(0, maxPipeY - int(offset))
    pipeX = WIDTH + 10
    y1 = pipeHeight - y2 + offset

    pipe = [
        {'x': pipeX, 'y': -y1},  # Upper pipe
        {'x': pipeX, 'y': y2}    # Lower pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")

    # Load images
    IMAGES['numbers'] = (
        pygame.image.load('gallery/images/0.png').convert_alpha(),
        pygame.image.load('gallery/images/1.png').convert_alpha(),
        pygame.image.load('gallery/images/2.png').convert_alpha(),
        pygame.image.load('gallery/images/3.png').convert_alpha(),
        pygame.image.load('gallery/images/4.png').convert_alpha(),
        pygame.image.load('gallery/images/5.png').convert_alpha(),
        pygame.image.load('gallery/images/6.png').convert_alpha(),
        pygame.image.load('gallery/images/7.png').convert_alpha(),
        pygame.image.load('gallery/images/8.png').convert_alpha(),
        pygame.image.load('gallery/images/9.png').convert_alpha()
    )

    IMAGES['message'] = pygame.image.load('gallery/images/message.png').convert_alpha()
    IMAGES['base'] = pygame.image.load('gallery/images/base.png').convert_alpha()
    IMAGES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    IMAGES['background'] = pygame.image.load(BACKGROUND).convert()
    IMAGES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Load sounds
    SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    SOUNDS['flap'] = pygame.mixer.Sound('gallery/audio/flap.wav')
    SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')

    while True:
        welcomescreen()
        maingame()
