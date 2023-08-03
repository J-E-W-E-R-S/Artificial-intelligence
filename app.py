# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading

import pygame
import tensorflow as tf
import numpy as np

pygame.init()

# Global Constants
color = 'white'

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Squirrel Run")

Ico = pygame.image.load("assets/Squirrel/SquirrelDead1.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelRun1.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelRun2.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelRun3.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelRun4.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelRun5.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelRun6.png")),

]
JUMPING = [
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelJump1.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelJump2.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelJump3.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelJump4.png"))
]
DUCKING = [
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelDuck1.png")),
    pygame.image.load(os.path.join("assets/Squirrel", "SquirrelDuck2.png")),
]
DEAD = pygame.image.load(os.path.join("assets/Squirrel/SquirrelDead1.png"))


ANT = [
    pygame.image.load(os.path.join("assets/Obstacles", "ant1.png")),
    pygame.image.load(os.path.join("assets/Obstacles", "ant2.png")),
    pygame.image.load(os.path.join("assets/Obstacles", "ant3.png")),
    pygame.image.load(os.path.join("assets/Obstacles", "ant4.png")),
    pygame.image.load(os.path.join("assets/Obstacles", "ant5.png")),
    pygame.image.load(os.path.join("assets/Obstacles", "ant6.png")),
    pygame.image.load(os.path.join("assets/Obstacles", "ant7.png")),
    pygame.image.load(os.path.join("assets/Obstacles", "ant8.png"))
]

BIRD1 = [
    pygame.image.load(os.path.join("assets/Birds/Bird1", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Birds/Bird1", "Bird2.png")),
    pygame.image.load(os.path.join("assets/Birds/Bird1", "Bird3.png")),
    pygame.image.load(os.path.join("assets/Birds/Bird1", "Bird4.png")),
    pygame.image.load(os.path.join("assets/Birds/Bird1", "Bird5.png")),
    pygame.image.load(os.path.join("assets/Birds/Bird1", "Bird6.png"))
]

BIRD2 = [
    pygame.image.load(os.path.join("assets/Birds/Bird2", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Birds/Bird2", "Bird2.png")),
    pygame.image.load(os.path.join("assets/Birds/Bird2", "Bird3.png")),
    pygame.image.load(os.path.join("assets/Birds/Bird2", "Bird4.png"))
]


CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))
MOUNTAINS = pygame.image.load(os.path.join("assets/Other", "mountains.png"))
TREES = pygame.image.load(os.path.join("assets/Other", "trees.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

OVER = pygame.image.load(os.path.join("UI/GameOverText.png"))
clock = pygame.time.Clock()
game_speed = 10
pred = False

FONT_COLOR=(0,0,0)

# Configuración de los objetos
global player_pos, player_rect, obstacle_pos, obstacle_rect

class Squirrel:

    X_POS = 80
    Y_POS = 350
    JUMP_VEL = 6.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DEAD

        self.squirrel_duck = False
        self.squirrel_run = True
        self.squirrel_jump = False
        self.squirrel_jump2 = False

        self.step_index = 1
        self.step_indexd = 0
        self.step_indexj = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.image = self.jump_img[0]
        self.squirrel_rect = self.image.get_rect()
        self.squirrel_rect.x = self.X_POS
        self.squirrel_rect.y = self.Y_POS

        global player_pos
        player_pos = self.X_POS

    def update(self, userInput, pred):
        if self.squirrel_duck:
            self.duck()
        if self.squirrel_run:
            self.run()
        if self.squirrel_jump:
            self.jump()
        if self.squirrel_jump2:
            self.jump2()

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE] or pred == True) and not self.squirrel_jump and self.Y_POS == 350:
            self.squirrel_duck = False
            self.squirrel_run = False
            self.squirrel_jump = True
        if pred == True:
            self.squirrel_duck = False
            self.squirrel_run = False
            self.squirrel_jump = True
        elif userInput[pygame.K_DOWN] and self.squirrel_jump:
            self.squirrel_jump = False
            self.squirrel_run = False
            self.squirrel_jump2 = True
            self.squirrel_duck = False
        elif userInput[pygame.K_DOWN] and not self.squirrel_jump:
            self.squirrel_duck = True
            self.squirrel_run = False
            self.squirrel_jump = False
        elif not (self.squirrel_jump or userInput[pygame.K_DOWN]):
            self.squirrel_duck = False
            self.squirrel_run = True
            self.squirrel_jump = False

##        if pred == True:
##            self.jump()
    
    def duck(self):
        self.image = self.duck_img[self.step_indexd]
        self.squirrel_rect = self.image.get_rect()
        self.squirrel_rect.width = 118
        self.squirrel_rect.height = 60
        self.squirrel_rect.x = self.X_POS
        self.squirrel_rect.y = self.Y_POS
        self.step_indexd += 1
        while self.step_indexd >= 2:
            self.step_indexd = 0

    def run(self):
        self.image = self.run_img[self.step_index]
        self.squirrel_rect = self.image.get_rect()
        self.squirrel_rect.width = 40
        self.squirrel_rect.height = 40
        self.squirrel_rect.x = self.X_POS
        self.squirrel_rect.y = self.Y_POS
        self.step_index += 1
        while self.step_index >= 6:
            self.step_index = 0

    def jump(self):
        self.image = self.jump_img[self.step_indexj]
        if self.squirrel_jump:
            self.squirrel_rect.y -= self.jump_vel * 4 # type: ignore
            self.jump_vel -= 0.6
        if self.jump_vel < -self.JUMP_VEL:
            self.squirrel_jump = False
            self.jump_vel = self.JUMP_VEL
        self.step_indexj += 1
        while self.step_indexj >= 3:
            self.step_indexj = 0

    def jump2(self):
        self.image = self.jump_img[self.step_indexj]
        if self.squirrel_jump2:
            self.squirrel_rect.y -= self.jump_vel * 3 # type: ignore
            self.jump_vel -= 2.6
        if self.jump_vel < -self.JUMP_VEL:
            self.squirrel_jump2 = False
            self.jump_vel = self.JUMP_VEL
        if self.squirrel_rect.y > 311:
            self.squirrel_rect.y = self.Y_POS
        for event in pygame.event.get():
            while event.type == pygame.KEYDOWN and not self.squirrel_jump2:
                if event.key == pygame.K_DOWN:
                    self.squirrel_duck = True
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.squirrel_rect.x, self.squirrel_rect.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

        global obstacle_pos, obstacle_rect
        obstacle_pos = self.rect.x

    def update(self):
        self.rect.x -= game_speed * 2
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Ant(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 370
        self.index = 0
        self.rect.height = 20

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.index], self.rect)
        self.rect.height = 30
        self.index += 1
        if self.index >= 8:
            self.index = 0

##class LargeCactus(Obstacle):
##    def __init__(self, image):
##        self.type = random.randint(0, 2)
##        super().__init__(image, self.type)
##        self.rect.y = 300
##        self.rect.height = 94
##        


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0
        self.rect.height = 30

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.index], self.rect)
        self.rect.height = 30
        self.index += 1
        if self.index >= 6:
            self.index = 0

class Bird2(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0
        self.rect.height = 30

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.index], self.rect)
        self.rect.height = 30
        self.index += 1
        if self.index >= 4:
            self.index = 0


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, cloudsx, cloudsy, mx, my, my2, ty2, my3, ty3, ty4, ty5, player_pos, obstacle_pos
    run = True
    player = Squirrel()
    mx = 0
    my = 30
    my2 = 90
    ty2 = 150
    my3 = 210
    ty3 = 260
    ty4 = 330
    ty5 = 400
    cloudsx = 0
    cloudsy = 27
    x_pos_bg = 0
    y_pos_bg = 400
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    # Función para calcular la distancia entre dos objetos
    def distance(obj1_pos, obj2_pos):
        x1 = obj1_pos.x
        x2 = obj2_pos.x
        return np.sqrt((x1 - x2) ** 2)
    
    def score():
        global points, game_speed
        points += 1
        if points != 10:
            if points % 100 == 0:
                game_speed += 1
        if game_speed == 10:
            game_speed = 10
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
        final = image_width + -(game_speed)

    def clouds():
        global cloudsx, cloudsy
        image_width = CLOUD.get_width()
        SCREEN.blit(CLOUD, (cloudsx, cloudsy))
        SCREEN.blit(CLOUD, (image_width + cloudsx, cloudsy))
        if cloudsx <= -image_width:
            SCREEN.blit(CLOUD, (image_width + cloudsx, cloudsy))
            cloudsx = 0
        cloudsx -= 0.5
        final = image_width + -(game_speed)


    def mountains():
        global mx, my
        image_width = MOUNTAINS.get_width()
        SCREEN.blit(MOUNTAINS, (mx, my))
        SCREEN.blit(MOUNTAINS, (image_width + mx, my))
        if mx <= -image_width:
            SCREEN.blit(MOUNTAINS, (image_width + mx, my))
            mx = 0
        mx -= game_speed // 4
        final = image_width + -(game_speed)

    def mountains2():
        global mx, my2
        image_width = MOUNTAINS.get_width()
        SCREEN.blit(MOUNTAINS, (mx, my2))
        SCREEN.blit(MOUNTAINS, (image_width + mx, my2))
        if mx <= -image_width:
            SCREEN.blit(MOUNTAINS, (image_width + mx, my2))
            mx = 0
        mx -= game_speed // 4
        final = image_width + -(game_speed)

    def trees2():
        global mx, ty2
        image_width = TREES.get_width()
        SCREEN.blit(TREES, (mx, ty2))
        SCREEN.blit(TREES, (image_width + mx, ty2))
        if mx <= -image_width:
            SCREEN.blit(TREES, (image_width + mx, ty2))
            mx = 0
        mx -= game_speed // 4
        final = image_width + -(game_speed)

    def mountains3():
        global mx, my3
        image_width = MOUNTAINS.get_width()
        SCREEN.blit(MOUNTAINS, (mx, my3))
        SCREEN.blit(MOUNTAINS, (image_width + mx, my3))
        if mx <= -image_width:
            SCREEN.blit(MOUNTAINS, (image_width + mx, my3))
            mx = 0
        mx -= game_speed // 4
        final = image_width + -(game_speed)

    def trees3():
        global mx, ty3
        image_width = TREES.get_width()
        SCREEN.blit(TREES, (mx, ty3))
        SCREEN.blit(TREES, (image_width + mx, ty3))
        if mx <= -image_width:
            SCREEN.blit(TREES, (image_width + mx, ty3))
            mx = 0
        mx -= game_speed // 4
        final = image_width + -(game_speed)

    def trees4():
        global mx, ty4
        image_width = TREES.get_width()
        SCREEN.blit(TREES, (mx, ty4))
        SCREEN.blit(TREES, (image_width + mx, ty4))
        if mx <= -image_width:
            SCREEN.blit(TREES, (image_width + mx, ty4))
            mx = 0
        mx -= game_speed // 4
        final = image_width + -(game_speed)

    def trees5():
        global mx, ty5
        image_width = TREES.get_width()
        SCREEN.blit(TREES, (mx, ty5))
        SCREEN.blit(TREES, (image_width + mx, ty5))
        if mx <= -image_width:
            SCREEN.blit(TREES, (image_width + mx, ty5))
            mx = 0
        mx -= game_speed // 4
        final = image_width + -(game_speed)

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()
    
    # Configuración del modelo de TensorFlow
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(1, activation='relu')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()
    
        current_time = datetime.datetime.now().hour
        SCREEN.fill((208, 244, 247))

        userInput = pygame.key.get_pressed()
        
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Ant(ANT))
            elif random.randint(0, 2) == 1:
                  obstacles.append(Bird2(BIRD2))
            elif random.randint(0, 2) == 1:
                obstacles.append(Bird(BIRD1))

        clouds()
        mountains()
        mountains2()
        trees2()
        mountains3()
        trees3()
        trees4()
        trees5()
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            player.draw(SCREEN)
            global player_pos, player_rect, obstacle_pos, obstacle_rect
            player_rect = player.squirrel_rect
            obstacle_rect = obstacle.rect

            # Actualización del modelo y comprobación de colisiones
            distance_to_obstacle = distance(player_rect, obstacle_rect)
            input_data = np.array([player_pos, 1100, obstacle_pos, -1100])
            input_data = np.reshape(input_data, (1, 4))
            prediction = model.predict(input_data)[0][0]
            print(prediction)
            if distance_to_obstacle < 90 and prediction > 0.1:
                player.update(userInput, True)
                print("saltar")
            else:
                player.update(userInput, False)
            if player.squirrel_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
        
        background()

        score()
        
        clock.tick(999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
        pygame.display.update()


def menu(death_count):
    global points
    global FONT_COLOR
    run = True
    while run:
        
        font = pygame.font.Font("freesansbold.ttf", 30)
        if death_count == 0:
            SCREEN.fill((208, 244, 247))
            def background():
                image_width = BG.get_width()
                SCREEN.blit(BG, (0, 400))
                SCREEN.blit(BG, (image_width + 0, 400))
            def clouds():
                image_width = CLOUD.get_width()
                SCREEN.blit(CLOUD, (0, 27))
                SCREEN.blit(CLOUD, (image_width + 0, 27))
            def mountains():
                image_width = MOUNTAINS.get_width()
                SCREEN.blit(MOUNTAINS, (0, 30))
                SCREEN.blit(MOUNTAINS, (image_width + 0, 30))
            def mountains2():
                image_width = MOUNTAINS.get_width()
                SCREEN.blit(MOUNTAINS, (0, 90))
                SCREEN.blit(MOUNTAINS, (image_width + 0, 90))
            def trees2():
                image_width = TREES.get_width()
                SCREEN.blit(TREES, (0, 150))
                SCREEN.blit(TREES, (image_width + 0, 150))
            def mountains3():
                image_width = MOUNTAINS.get_width()
                SCREEN.blit(MOUNTAINS, (0, 210))
                SCREEN.blit(MOUNTAINS, (image_width + 0, 210))
            def trees():
                image_width = TREES.get_width()
                SCREEN.blit(TREES, (0, 260))
                SCREEN.blit(TREES, (image_width + 0, 260))
            def trees3():
                image_width = TREES.get_width()
                SCREEN.blit(TREES, (0, 330))
                SCREEN.blit(TREES, (image_width + 0, 330))
            def trees4():
                image_width = TREES.get_width()
                SCREEN.blit(TREES, (0, 400))
                SCREEN.blit(TREES, (image_width + 0, 400))
            text = font.render("Press any Key to Start", True, FONT_COLOR)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            clouds()
            mountains()
            mountains2()
            trees2()
            mountains3()
            trees()
            trees3()
            trees4()
            
            background()
            SCREEN.blit(text, textRect)
            
        elif death_count > 0:
            OverRect = OVER.get_rect()
            OverRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(OVER, OverRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()

t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
