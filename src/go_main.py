# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 22:51:51 2021

@author: LIN03
"""

import pygame
from go_class import *
from random import randint
pygame.init()
sz = (700,700)
screen = pygame.display.set_mode(size=sz)
pygame.display.set_caption('Go')

def import_pic(filename, x, y):
    pic = pygame.image.load(filename)
    pic.convert_alpha()
    #pic = pygame.transform.scale(pic, (300,300))
    rec = pic.get_rect()
    rec.center = x,y
    return [pic, rec]

def show_board():
    board_img = {0 : import_pic('img_corner1.png',71,71),
                 8 : import_pic('img_corner2.png',631,71),
                 72 : import_pic('img_corner3.png',71,631),
                 80 : import_pic('img_corner4.png',631,631),
                 1 : import_pic('img_side1.png',1500,1500),
                 2 : import_pic('img_side2.png',1500,1500),
                 3 : import_pic('img_side3.png',1500,1500),
                 4 : import_pic('img_side4.png',1500,1500),
                 -1 : import_pic('img_center.png',1500,1500),
                 -2 : import_pic('img_star.png',1500,1500)}
    for i in range(9):
        for j in range(9):
            if i*9+j in [0,8,72,80]:
                [pic,rec] = board_img.get(i*9+j)
            elif i == 0:
                [pic,rec] = board_img.get(4)
                rec.center = 71,71+70*j
            elif i == 8:
                [pic,rec] = board_img.get(2)
                rec.center = 631,71+70*j
            elif j == 0:
                [pic,rec] = board_img.get(1)
                rec.center = 71+70*i,71
            elif j == 8:
                [pic,rec] = board_img.get(3)
                rec.center = 71+70*i,631
            elif (i in [2,6] and j in [2,6]) or [i,j] == [4,4]:
                [pic,rec] = board_img.get(-2)
                rec.center = 71+70*i,71+70*j
            else:
                [pic,rec] = board_img.get(-1)
                rec.center = 71+70*i,71+70*j
            screen.blit(pic,rec)

def show_stones(board):
    for i in range(9):
        for j in range(9):
            board_stone = board[i][j]
            if board_stone in [0,3]:
                continue
            if board_stone == 1:
                [pic,rec] = import_pic('img_black.png',71+70*i,71+70*j)
            elif board_stone == 2:
                [pic,rec] = import_pic('img_white.png',71+70*i,71+70*j)
            screen.blit(pic,rec)

gamemode = 0
''' gamemode: 
        0 = menu, 
        1 = start game
        2 = end, restart?
'''

g = go(9)


done = False
moving = False
bg_pic,bg_rec = import_pic('img_wood2.png', sz[0] // 2, sz[1] // 2)
while not done: # EVENT LOOP
    screen.fill((255,192,203))
    screen.blit(bg_pic,bg_rec)
    show_board()

    show_stones(g.board)


    pygame.display.update()
    if gamemode == 0:
        for event in pygame.event.get():
            t = event.type
            if t == pygame.QUIT:
                pygame.quit()
                done = True
                break
            if t == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click, place a stone
                    x,y = event.pos
                    x,y  = (x-36) // 70, (y-36) // 70
                    if x in range(g.size) and y in range(g.size):
                        g.ordered_move(x, y)
                    
                elif event.button == 3: # right click, remove the last placed
                    g.ordered_undo_move()
            '''
            elif t == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    moving = True
            elif t == pygame.MOUSEBUTTONUP:
                moving = False
            elif t == pygame.MOUSEMOTION and moving:
                rect.move_ip(event.rel)
            elif t == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
            '''
    elif gamemode == 1:
        pass
    elif gamemode == 2:
        screen.fill((255,255,255))