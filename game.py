import random #for making pipes randomly appear
import sys #to exit the game
import pygame
from pygame.locals import * #baisc pygame imports


#Game variables
FPS=30
WIDTH=289
HEIGHT=511
SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
GROUNDY=HEIGHT*0.01
IMAGES={}
SOUNDS={}
PLAYER='gallery/images/bird.png'
PIPE='gallery/images/pipe.png'
BACKGROUND='gallery/images/background.png'

def welcomescreen():
    player_x=-50
    player_y=150
    message_x=-105
    message_y=-150
    base_x=0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_w):
                return
            
            else:
                SCREEN.blit(IMAGES['background'], (0,0))
                SCREEN.blit(IMAGES['player'], (player_x,player_y))
                SCREEN.blit(IMAGES['message'], (message_x,message_y))
                SCREEN.blit(IMAGES['base'], (base_x,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def maingame():
    score=0
    playerx=-50
    playery=150
    basex=0

    newPipe1=getrandomPipe()
    newPipe2=getrandomPipe()

    upperPipes=[
        {'x':WIDTH+200, 'y':newPipe1[0]['y']},
        {'x':WIDTH+200+(WIDTH/2), 'y':newPipe2[1]['y']}
    ]
    lowerPipes=[
        {'x':WIDTH+200, 'y':newPipe1[0]['y']},
        {'x':WIDTH+200+(WIDTH/2), 'y':newPipe2[1]['y']}
    ]

    pipevelx=-4
    playermaxvel_y=10
    playervel_y=-9
    playerminvel_y=-8
    playeracc_y=1

    playerflapaccv=-8 #velocity while flapping
    playerFlapped=False

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervel_y=playerflapaccv
                    playerFlapped=True
                    SOUNDS['flap'].play()
        
        crash_test=isCollide(playerx,playery,upperPipes,lowerPipes)#returns true when player crashes
        if crash_test:
            return

        #score check
        playerMidPos=100
        for pipe in upperPipes:
            pipeMidPos=pipe['x']+IMAGES['pipe'][0].get_width()/2
            if pipeMidPos<=playerMidPos+4:
                score+=1
                print(f"SCORE={score}")
            SOUNDS['point'].play()
        
        if playervel_y<playermaxvel_y and not playerFlapped:
            playervel_y+=playeracc_y

        if playerFlapped:
            playerFlapped=False
        playerHeight=IMAGES['player'].get_height()
        playery=playery+min(playervel_y, GROUNDY-playery-playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x']+=pipevelx
            lowerPipe['x']+=pipevelx
        
        #adding new pipes
        if 0<upperPipes[0]['x']<5:
            newpipe=getrandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x']<-IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        SCREEN.blit(IMAGES['background'], (0,0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (upperPipe['x'],upperPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lowerPipe['x'],lowerPipe['y']))


        SCREEN.blit(IMAGES['base'], (basex,GROUNDY))
        SCREEN.blit(IMAGES['player'], (playerx,playery))
        mydigits=[int(x) for x in list(str(score))]
        wdth=0
        for digit in mydigits:
            wdth+=IMAGES['numbers'][digit].get_width()
        Xoffset=(WIDTH-wdth)/2

        for digit in mydigits:
            SCREEN.blit(IMAGES['numbers'][digit],(Xoffset, HEIGHT*0.12))
            Xoffset+=IMAGES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx,playery,upperPipes,lowerPipes):
    return False
        

def getrandomPipe():
    pipeheight=IMAGES['pipe'][0].get_height()
    offset=HEIGHT/3
    y2=offset+random.randrange(0, (int(HEIGHT+IMAGES['base'].get_height()-(1.2)*(offset))))
    pipex=WIDTH+10
    y1=pipeheight-y2+offset
    pipe=[
        {'x':pipex, 'y': -y1},
        {'x':pipex, 'y': y2}
    ]

    return pipe


if __name__ == "__main__":
    #the point from where the game will start
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    IMAGES['numbers']=(
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
    
    IMAGES['message']=pygame.image.load('gallery/images/message.png').convert_alpha()
    IMAGES['base']=pygame.image.load('gallery/images/base.png')
    IMAGES['pipe']=(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    #SOUNDS
    SOUNDS['die']=pygame.mixer.Sound('gallery/audio/die.wav')
    SOUNDS['flap']=pygame.mixer.Sound('gallery/audio/flap.wav')
    SOUNDS['hit']=pygame.mixer.Sound('gallery/audio/hit.wav')
    SOUNDS['point']=pygame.mixer.Sound('gallery/audio/point.wav')
    SOUNDS['swoosh']=pygame.mixer.Sound('gallery/audio/swoosh.wav')

    IMAGES['background']=pygame.image.load(BACKGROUND).convert()
    IMAGES['player']=pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomescreen()
        maingame()