import random
import pygame
from Circle import *
from Robot import *

robots = []
#rob = Robot(100,100)
obstacles = []

pygame.init()

display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Swarm Sim')
clock = pygame.time.Clock()

want_to_exit = False

for i in range(4):
    obstacles.append(Circle(random.randrange(800), random.randrange(600),random.randrange(40,120)))



while not want_to_exit:
    display.fill((255, 255, 255))


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            want_to_exit = True

        if event.type == pygame.MOUSEBUTTONUP:

            robots.append(Robot((random.randrange(0,displayWidth),random.randrange(0,displayHeight))))





    for i in range(len(robots)):
        robots[i].move()
        robots[i].show(display)
        robots[i].applyBehaviour(robots, pygame.mouse.get_pos(), obstacles)

    #print(rob.v.as_polar())


    #print(rob.get_distance(obstacles))

    for i in range (len(obstacles)):
        obstacles[i].show(display)


    pygame.display.update()
    clock.tick(60)

pygame.quit()