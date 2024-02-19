import pygame
import random
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Component


class Enemy(Component):
    def __init__(self, scale_factor=0.3) -> None:
        super().__init__()
        self.speed_x = 201
        self.speed_y = 50
        self.scale_factor = scale_factor
        self.stop_x_position = 1100 #X position where the enemies stop
        self.direction = 1  # Initial direction: 1 for down, -1 for up
        


    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        sr.scale(self.scale_factor)
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = (self._screen_size.x) + (self._sprite_size.x)  #enemy spawn location x

        min_y = 80  # Minimum y-coordinate for enemy spawn
        max_y = max(min_y, self._screen_size.y)  # Ensure max_y is at least min_y
        self._gameObject.transform.position.y = random.randint(180, int(self._screen_size.y)) + (self._sprite_size.y)
        #self._gameObject.transform.position.y = (self._screen_size.y) + (self._sprite_size.y)  



    def start(self):
        pass

    def update(self, delta_time):

        self._gameObject.transform.position.x -= self.speed_x * delta_time

        if self._gameObject.transform.position.x <= self.stop_x_position:
            self.speed_x = 0
        # if    self._gameObject.transform.position.x <= self.stop_x_position-100 and self.speed_x==200:
        #     self.speed_x = 0
        # if    self._gameObject.transform.position.x <= self.stop_x_position-200 and self.speed_x==199:
        #     self.speed_x = 0
        # if    self._gameObject.transform.position.x <= self.stop_x_position-300 and self.speed_x>=51:
        #     self.speed_x = 0


        if self.direction == 1:
            self._gameObject.transform.position.y += self.speed_y * delta_time
            if self._gameObject.transform.position.y >= 720:
                self.direction = -1  # Change direction to up
                self.stop_x_position-=100
                self.speed_x = 200

        else:
            self._gameObject.transform.position.y -= self.speed_y * delta_time
            if self._gameObject.transform.position.y <= 180:
                self.direction = 1  # Change direction to down
                self.stop_x_position-=100
                self.speed_x = 200


