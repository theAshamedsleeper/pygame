import pygame
import random
import pygame
from Components import Component
from GameObject import GameObject
from Components import SpriteRenderer
from Enemy import Enemy


class EnemyWell:
    def __init__(self, game_world, initial_size=10):
        self._game_world = game_world
        self._pool = []
        self._initialize_pool(initial_size)

    def _initialize_pool(self, initial_size):
        for _ in range(initial_size):
            enemy_go = GameObject(None)
            enemy_go.add_component(SpriteRenderer("enemy_01_00.png"))
            enemy_go.add_component(Enemy())
            enemy_go.active = False  # Set the active state using the active property
            self._pool.append(enemy_go)

    def get_enemy(self):
        for enemy_go in self._pool:
            if not enemy_go.active:
                enemy_go.active = True  # Set the active state using the active property
                return enemy_go
        enemy_go = GameObject(None)
        enemy_go.add_component(SpriteRenderer("enemy_01_00.png"))
        enemy_go.add_component(Enemy())
        enemy_go.active = True  # Set the active state using the active property
        self._pool.append(enemy_go)
        return enemy_go

    def return_enemy(self, enemy_go):
        enemy_go.active = False  # Set the active state using the active property