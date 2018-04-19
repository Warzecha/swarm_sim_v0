from Settings import *
import pygame
import math
class Robot:

    size = 20
    max_dis = 100
    max_vel = 2
    max_force = 0.1
    desiredSeparation = 50
    slow_down_distance = 50


    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)

        self.v = pygame.math.Vector2(0, self.max_vel)
        self.vel = 1

        self.f_distance = 0

        self.size = 20
        self.max_dis = 100
        self.max_vel = 2
        self.max_force = 0.1
        self.desiredSeparation = 50
        self.slow_down_distance = 50

        


    def show(self, display):
        vel, angle = self.v.as_polar()
        angle = angle * math.pi / 180

        pygame.draw.polygon(display, (255,0,0), ((self.pos.x + self.size * 2 * math.cos(angle), self.pos.y + self.size * 2 * math.sin(angle)), (self.pos.x + self.size * math.sin(angle), self.pos.y - self.size * math.cos(angle)), (self.pos.x - self.size * math.sin(angle), self.pos.y + self.size * math.cos(angle))))
        #pygame.draw.circle(display,(50,50,50), (int(self.pos.x),int(self.pos.y)), 10)


    def move(self):
        self.pos = self.pos + self.v

    def check_if_dead(self, obstacles):

        if self.pos.x < 0 or self.pos.x > displayWidth or self.pos.y < 0 or self.pos.y > displayHeight:
            return True

        for i in range(len(obstacles)):
            if distance(self.pos.x, self.pos.y, obstacles[i].x, obstacles[i].y) <= obstacles[i].radius:
                return True

        return False




    def get_distance(self, obstacles):


        vel, angle = self.v.as_polar()


        #print(angle)
        distances = []
        if -180 < angle < 0:
            distances.append(math.fabs(self.pos.y/math.sin(math.pi - angle)))

        if 0 < angle < 180:
            distances.append(math.fabs((displayHeight - self.pos.y)/math.sin(angle)))
        distances.append(self.max_dis)


        if -90 < angle < 90:
            distances.append(math.fabs((displayWidth - self.pos.x)/math.cos(angle)))


        if -180 < angle < -90 or 90 < angle < 180:
            distances.append(math.fabs(self.pos.x / math.cos(math.pi - angle)))
        distances.append(self.max_dis)


        return min(distances)


    def seek(self, target):



        desired = pygame.math.Vector2(target)
        desired -= self.pos
        d = desired.length()
        if d == 0:
            return pygame.math.Vector2()
        desired = desired.normalize()
        if d > self.slow_down_distance:
            desired *= self.max_vel
        else:
            desired *= self.max_vel * d / self.slow_down_distance
        steering = pygame.math.Vector2()
        steering = desired - self.v

        steering.scale_to_length(self.max_force)


        return steering

    def separate(self, others):

        sum = pygame.math.Vector2()
        count = 0

        for i in range(len(others)):
            d = self.pos.distance_to(others[i].pos)

            if (d > 0) and d < self.desiredSeparation:
                difference = pygame.math.Vector2
                difference = self.pos - others[i].pos
                difference.normalize()
                difference /= d
                sum += difference
                count += 1

        if count > 0 and sum.length() > 0:
            sum /= count
            sum.normalize()
            sum *= self.max_vel

            steering = pygame.math.Vector2()
            steering = sum - self.v
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)


            return steering

        return pygame.math.Vector2()


    def obstaclesAvoidance(self, obstacles):
        count = 0
        sum = pygame.math.Vector2()
        for i in range(len(obstacles)):
            d = self.pos.distance_to(obstacles[i].pos)

            if d < obstacles[i].radius + 10:
                difference = pygame.math.Vector2
                difference = self.pos - obstacles[i].pos
                difference.normalize()
                difference /= d
                sum += difference
                count += 1

        if count > 0 and sum.length() > 0:
            sum /= count
            sum.normalize()
            sum *= self.max_vel

            steering = pygame.math.Vector2()
            steering = sum - self.v
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)

            return steering

        return pygame.math.Vector2()



    def applyBehaviour(self,others, target, obstacles):

        separationForce = self.separate(others)
        seekForce = self.seek(target)
        avoidanceForce = self.obstaclesAvoidance(obstacles)
        separationForce *= 1.8
        seekForce *= 1
        avoidanceForce *= 1.5

        self.v += separationForce
        self.v += seekForce
        self.v += avoidanceForce