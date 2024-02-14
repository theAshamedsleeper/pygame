import pygame
import random
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Component


class Enemy(Component):
    def __init__(self) -> None:
        super().__init__()
    speed = 200
        

    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = (self._screen_size.x) - (self._sprite_size.x) #enemy spawn location x
        self._gameObject.transform.position.y = (self._screen_size.y/2) - (self._sprite_size.y/2) #player spawn location y

       # self._gameObject.transform.position.y = random.randint(0, self._screen_size.y) - (self._sprite_size.y) #enemy spawn location y

    def start(self):
        pass

    def update(self, delta_time):
        
        self._gameObject.transform.position.x -= self.speed * delta_time

        if self._gameObject.transform.position.x < -self._sprite_size.x:
            self._gameObject.destroy()
        
# class EnemySpawner(Component):
#     def __init__(self, game_world) -> None:
#         super().__init__()
#         self.enemy_prefab = None
#         self.spawn_delay = 2
#         self.spawn_timer = 0

#     def awake(self, game_world):
#         self._game_world = game_world

#     def start(self):
#         pass

#     def update(self, delta_time):
#         self.spawn_timer += delta_time

#         if self.spawn_timer >= self.spawn_delay:
#             self.spawn_enemy()
#             self.spawn_timer = 0

#     def spawn_enemy(self):
#         go_enemy = GameObject(None)
#         go_enemy.add_component(self.enemy_prefab)
#         self._game_world.current_State.instantiate(enemy_go)