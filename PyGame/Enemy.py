import pygame
import random
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Component


class Enemy(Component):
    def __init__(self, scale_factor=0.3) -> None:
        super().__init__()
        self.speed = 200
        self.scale_factor = scale_factor
        


    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        sr.scale(self.scale_factor)
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = (self._screen_size.x) + (self._sprite_size.x)  #enemy spawn location x

        min_y = 50  # Minimum y-coordinate for enemy spawn
        max_y = max(min_y, self._screen_size.y)  # Ensure max_y is at least min_y
        self._gameObject.transform.position.y = random.randint(50, int(self._screen_size.y)) + (self._sprite_size.y)


    def start(self):
        pass

    def update(self, delta_time):
        
        self._gameObject.transform.position.x -= self.speed * delta_time

       # if self._gameObject.transform.position.x < -self._sprite_size:
      #      self._gameObject.destroy()
        
