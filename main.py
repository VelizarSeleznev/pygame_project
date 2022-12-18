import pygame
import sys
import os
from player import Player
from spritesheet import Spritesheet

# 67, 88
# 133, 64

# 7, 8, 15


pygame.init()
DISPLAY_W, DISPLAY_H = 800, 800
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True
character = Player()
index = 0
clock = pygame.time.Clock()
fps = 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if character.atk_state == 0:
                    character.current_anim = 0
                character.atk_state += 1
                character.move = False
            if event.key == pygame.K_UP:
                character.move = True
                character.direction = 'up'
            elif event.key == pygame.K_DOWN:
                character.move = True
                character.direction = 'down'
            if event.key == pygame.K_RIGHT:
                character.move = True
                character.direction = 'right'
            elif event.key == pygame.K_LEFT:
                character.move = True
                character.direction = 'left'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                character.move = False
            elif event.key == pygame.K_DOWN:
                character.move = False
            if event.key == pygame.K_RIGHT:
                character.move = False
            elif event.key == pygame.K_LEFT:
                character.move = False
    character.animate()
    canvas.fill((255, 255, 255))
    canvas.blit(character.get_image(), (-40, -40))
    window.blit(canvas, (0, 0))
    pygame.display.update()
    clock.tick(fps)
