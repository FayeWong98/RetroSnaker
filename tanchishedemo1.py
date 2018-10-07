#!usr/bin/python
# -*- coding:utf-8 -*-
import pygame
import random
import sys
import time
from pygame.locals import *
snake_speed=15  #速度
windows_width=800
windows_height=600  #窗口大小
cell_size=20  #蛇大小
map_width=int(windows_width / cell_size)
map_height=int(windows_height / cell_size)  #地图相对于蛇的大小
white=(255,255,255)
black=(0,0,0)
gray=(230,230,230)
dark_gray=(40,40,40)
DARKGreen=(0,155,0)
Green=(0,255,0)
Red=(255,0,0)
blue=(0,0,255)
dark_blue=(0,0,139)
BG_COLOR=black
#定义方向
UP=1
DOWN=2
LEFT=3
RIGHT=4
HEAD=0  #蛇头部下标
pause = False
screen=pygame.display.set_mode((windows_width,windows_height))
snake_speed_clock=pygame.time.Clock()
pygame.display.set_caption("Python 贪吃蛇小游戏")
def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play(-1)

    #snake_speed_clock=pygame.time.Clock()  #创建时钟对象，fps
    #screen=pygame.display.set_mode((windows_width,windows_height)) #生成indows窗口,返回surface对象
    screen.fill(white)
    #pygame.display.set_caption("Python 贪吃蛇小游戏")
    draw_grid(screen)
    pause = False
    show_start_info(screen)
    while True:
        running_game(screen,snake_speed_clock)
        show_gameover_info(screen)
        paused(screen)

def show_start_info(screen):
    font=pygame.font.Font('myfont.ttf',40)
    tip=font.render("按任意键继续游戏....",True,(65,105,225))
    gamestart=pygame.image.load('gamestart.png')
    screen.blit(gamestart,(140,30))
    screen.blit(tip,(240,550))
    pygame.display.update()
    while True: #键盘监听事件
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==KEYDOWN:
                if(event.key==K_ESCAPE):
                    terminate()
                else:
                    return

def show_gameover_info(screen):
    font=pygame.font.Font('myfont.ttf',40)
    tip=font.render('按Q或和EXC退出游戏，按任意键继续游戏',True,(65,105,255))
    gamestart=pygame.image.load('gameover.png')
    screen.blit(gamestart,(60,0))
    screen.blit(tip,(80,300))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE or event.key==K_q:
                    terminate()
                else:
                    return
'''
def paused(screen):
    font = pygame.font.Font('myfont.ttf', 40)
    tip = font.render('暂停游戏，按q继续', True, (65, 105, 255))
    screen.blit(tip, (80, 300))
    pygame.display.update()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    unpause()
                elif event.key==K_l:
                    quitgame()
'''
def paused(screen):
    largeText = pygame.font.SysFont('comicsansms', 30)
    TextSurf, TextRect = text_objects('Paused', largeText)
    TextRect.center = ((windows_width / 2), (windows_height / 2))
    screen.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        ##        gameDisplay.fill(white)
        button("Continue", 150, 450, 100, 50, Green, Red, unpause)
        button("Quit", 550, 450, 100, 50, Red, Green, quitgame)
        pygame.display.update()
        snake_speed_clock.tick(snake_speed)

def running_game(screen,snake_speed_clock):
    global pause
    startx=random.randint(3,map_width-8) #开始位置
    starty=random.randint(3,map_height-8)
    snake_coords=[{'x':startx,'y':starty},  #初始贪吃蛇
                  {'x':startx-1,'y':starty},
                  {'x':startx-2,'y':starty}]
    direction=RIGHT #开始向右移动
    food=get_random_location()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type==KEYDOWN:
                if(event.key==K_LEFT or event.key==K_a) and direction!=RIGHT:
                    direction=LEFT
                elif(event.key==K_RIGHT or event.key==K_d) and direction!=LEFT:
                    direction=RIGHT
                elif(event.key==K_UP or event.key==K_w) and direction!=DOWN:
                    direction=UP
                elif(event.key==K_DOWN or event.key==K_s) and direction!=UP:
                    direction=DOWN
                elif event.key == pygame.K_p:
                    pause = True
                    paused(screen)
                    '''
                    font = pygame.font.Font('myfont.ttf', 40)
                    tip = font.render('waiting 10s', True, (65, 105, 255))
                    screen.blit(tip, (80, 300))
                    pygame.display.update()
                    pygame.time.wait(10000)#暂停十秒
                '''
                elif event.key==K_ESCAPE:
                    terminate()
        move_snake(direction,snake_coords) #移动贪吃蛇
        ret=snake_is_alive(snake_coords)
        if not ret:
            break
        snake_is_eat_food(snake_coords,food)
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_snake(screen,snake_coords)
        draw_food(screen,food)
        draw_score(screen,len(snake_coords)-3)
        pygame.display.update()
        snake_speed_clock.tick(snake_speed)

def move_snake(direction,snake_coords):
    if direction==UP:
        newHead={'x':snake_coords[HEAD]['x'],'y':snake_coords[HEAD]['y']-1}
    elif direction==DOWN:
        newHead={'x':snake_coords[HEAD]['x'],'y':snake_coords[HEAD]['y']+1}
    elif direction==LEFT:
        newHead={'x':snake_coords[HEAD]['x']-1,'y':snake_coords[HEAD]['y']}
    elif direction==RIGHT:
        newHead={'x':snake_coords[HEAD]['x']+1,'y':snake_coords[HEAD]['y']}
    snake_coords.insert(0,newHead)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
def quitgame():
    pygame.quit()
    quit()
def unpause():
    global pause
    pause = False

def button (msg, x, y, w, h, ic, ac, action=None):
    mouse =pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
##                if action == "play":
##                    action()
##                if action == "quit":
##                    pygame.quit()
##                    quit()
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
    smallText = pygame.font.SysFont('comicsansms', 30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

def snake_is_alive(snake_coords):
    tag=True
    if snake_coords[HEAD]['x']==-1 or snake_coords[HEAD]['x']==map_width or snake_coords[HEAD]['y']==-1 or \
            snake_coords[HEAD]['y']==map_height:
        tag = False
    for snake_body in snake_coords[1:]:
        if snake_body['x']==snake_coords[HEAD]['x'] and snake_body['y']==snake_coords[HEAD]['y']:
            tag=False
    return tag

def snake_is_eat_food(snake_coords,food):
    if snake_coords[HEAD]['x']==food['x'] and snake_coords[HEAD]['y']==food['y']:
        food['x']=random.randint(0,map_width-1)
        food['y']=random.randint(0,map_height-1)
    else:
        del snake_coords[-1]

def draw_snake(screen,snake_coords):
    for coord in snake_coords:
        x=coord['x']*cell_size
        y=coord['y']*cell_size
        wormSegmentRect=pygame.Rect(x,y,cell_size,cell_size)
        pygame.draw.rect(screen,dark_blue,wormSegmentRect)
        wormInnerSementRect=pygame.Rect(   #贪吃蛇身体里的第二层绿色
            x+4,y+4,cell_size-8,cell_size-8
        )
        pygame.draw.rect(screen,blue,wormInnerSementRect)

def draw_food(screen,food):
    x=food['x']*cell_size
    y=food['y']*cell_size
    appleRect=pygame.Rect(x,y,cell_size,cell_size)
    pygame.draw.rect(screen,Red,appleRect)

def draw_grid(screen):
    for x in range(0,windows_width,cell_size):
        pygame.draw.line(screen,dark_gray,(x,0),(x,windows_height))
    for y in range(0,windows_height,cell_size):
        pygame.draw.line(screen,dark_gray,(0,y),(windows_width,y))
def get_random_location():
    return {'x':random.randint(0,map_width-1),'y':random.randint(0,map_height-1)}

def draw_score(screen,score):
    font=pygame.font.Font('myfont.ttf',30)
    scoreSurf=font.render('得分:%s'% score,True,Green)
    scoreRect=scoreSurf.get_rect()
    scoreRect.topleft=(windows_width-120,10)
    screen.blit(scoreSurf,scoreRect)

def terminate():
    pygame.quit()
    sys.exit()
main()





