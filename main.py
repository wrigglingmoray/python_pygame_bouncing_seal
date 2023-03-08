#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This is a game resembling "Flappy Bird" where you control seal trying to avoid icebergs
Created by Konstantin Kuklin for Technische Hochschule Brandenburg (konstantin.kuklin@th-brandenburg.de)
Version 1.0
Sprites: Konstantin Kuklin
Audio: soundbible.com
"""

__author__ = "konstantin kuklin"

import sys

import pygame
from pygame.locals import *
import random


# Display
window_width = 640
window_height = 480
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Bouncing Seal")
#Pre-load sprites and optimize via alpha conversion
background = pygame.image.load("sprites/ice_bg.png").convert_alpha()
background = pygame.transform.scale(background, (window_width, window_height))
player = pygame.image.load("sprites/seal_idle.png").convert_alpha()
playerBounce = pygame.image.load("sprites/seal_bounce.png").convert_alpha()
playerHit = pygame.image.load("sprites/seal_sad.png").convert_alpha()
playerCurrentSprite = pygame.image.load("sprites/seal_idle.png").convert_alpha()
obstacleA = pygame.image.load("sprites/iceberg1.png").convert_alpha()
obstacleA = pygame.transform.scale(obstacleA, (obstacleA.get_width() / 2, obstacleA.get_height() / 2))
obstacleB = pygame.image.load("sprites/iceberg2.png").convert_alpha()
obstacleB = pygame.transform.scale(obstacleB, (obstacleB.get_width() / 2, obstacleB.get_height() / 2))

#Console game tutorial
print("WELCOME TO THE BOUNCING SEAL GAME")
print(
    "Press space or enter to start the game."
    "\nDon't hit ground or icebergs by bouncing seal with SPACE or UP."
    "\nQuit game with ESCAPE.")


def game():
    playerCurrentSprite = player
    playerSound = pygame.mixer.Sound("sounds/jump.wav")
    hitSound = pygame.mixer.Sound("sounds/hit.wav")

    score = 0
    x_axis = int(window_width / 5)
    y_axis = int(window_height / 2)
    startHeight = 100

    # Generate obstacles
    iceberg_a = createObstacle()
    iceberg_b = createObstacle()

    # Save obstacles in a list
    bottom_icebergs = [
        {"x": window_width + 300 - startHeight,
         "y": iceberg_a[1]["y"]},
        {"x": window_width + 300 - startHeight + window_width / 2,
         "y": iceberg_b[1]["y"]}
    ]
    top_icebergs = [
        {"x": window_width + 300 - startHeight,
         "y": iceberg_a[0]["y"]
         },
        {"x": window_width + 300 - startHeight + window_width / 2,
         "y": iceberg_b[0]["y"]
         }
    ]

    # obstacle velocity on x_axis
    iceberg_vel_x = -4

    # player velocity
    player_vel_y = -9
    player_max_vel_y = 10
    player_acc_y = 1

    player_bounce_vel = -8
    player_bounce = False

    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if y_axis > 0:
                    playerSound.play()
                    player_vel_y = player_bounce_vel
                    player_bounce = True
        # End game if player collides with x=0 or iceberg
        game_over = gameOver(x_axis, y_axis, top_icebergs, bottom_icebergs, playerCurrentSprite)
        if game_over:
            hitSound.play()
            return

        if player_vel_y < player_max_vel_y and not player_bounce:
            player_vel_y += player_acc_y

        if player_bounce:
            playerCurrentSprite = playerBounce
            player_bounce = False
        else:
            playerCurrentSprite = player

        player_height = player.get_height()
        y_axis = y_axis + player_vel_y
        # vertical
        for iceberg in top_icebergs:
            iceberg['x'] += iceberg_vel_x

        for iceberg in bottom_icebergs:
            iceberg['x'] += iceberg_vel_x

        # Create new obstacle once previous one reaches end of screen
        if 0 < top_icebergs[0]['x'] < 5:
            newIceberg = createObstacle()
            top_icebergs.append(newIceberg[0])
            bottom_icebergs.append(newIceberg[1])

        if top_icebergs[0]['x'] < -window_width/5:
            top_icebergs.pop(0)
            bottom_icebergs.pop(0)
            score += 1

        screen.blit(background, (0, 0))

        for iceberg in top_icebergs:
            screen.blit(obstacleB, (iceberg['x'], iceberg['y']))
        for iceberg in bottom_icebergs:
            screen.blit(obstacleA, (iceberg['x'], iceberg['y']))
        playerCurrentSprite = pygame.transform.scale(playerCurrentSprite, (
            playerCurrentSprite.get_width() / 6, playerCurrentSprite.get_height() / 6))

        screen.blit(playerCurrentSprite, (x_axis, y_axis))
        scoring = font.render(f'Your score is: {score}', True, Color("White"))
        screen.blit(scoring, (50, window_height - 50))
        pygame.display.update()
        fps.tick(30)


def createObstacle():
    offset = window_height / 3
    obstacle_height = obstacleA.get_height()

    # generate random height
    y2 = offset + random.randrange(0, int(window_height - 1.2 * offset))
    obstacle_x = window_width + 10
    y1 = obstacle_height - y2 + offset
    obstacle = [
        # Top iceberg
        {"x": obstacle_x, "y": -y1},
        # Bottom iceberg
        {"x": obstacle_x, "y": y2}
    ]
    return obstacle


def gameOver(x_axis, y_axis, top_obstacles, bottom_obstacles, playerCurrentSprite):
    if y_axis >= window_height:
        return True

    # Collision detection with top icebergs
    for obstacle in top_obstacles:
        if(y_axis + playerCurrentSprite.get_height()/2 < obstacle["y"] + obstacleA.get_height()
                and abs((x_axis + playerCurrentSprite.get_width()/2) - (obstacle["x"] + obstacleA.get_width()/2)) < 50):
            return True

    # Collision detection with bottom icebergs
    for obstacle in bottom_obstacles:
        if(y_axis + playerCurrentSprite.get_height()/2 > obstacle["y"]
                and abs((x_axis + playerCurrentSprite.get_width()/2) - (obstacle["x"] + obstacleA.get_width()/2)) < 50):
            return True

    return False


# Load objects
if __name__ == "__main__":
    pygame.init()

    font = pygame.font.Font(None, int(window_height * 0.1))

    fps = pygame.time.Clock()

    x_axis = int(window_width / 5)
    y_axis = int((window_height - player.get_height()) / 2)
    ground = 0

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                game()
            else:
                screen.blit(background, (0, 0))
                text1 = font.render("BOUNCING SEAL", True, Color("White"))
                screen.blit(text1, (int(window_width / 4), int(window_height / 2)))
                text2 = font.render("PRESS SPACE OR UP", True, Color("White"))
                screen.blit(text2, (int(window_width / 4), int(window_height / 2) + 100))
                pygame.display.update()
                fps.tick(30)
