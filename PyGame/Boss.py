from Components import Component
from Components import SpriteRenderer
from Components import Animator
from GameObject import GameObject
from Components import EnemyLaser
import pygame
import math
from pygame import mixer

class Boss(Component):
    def __init__(self, scale_factor= 0.5) -> None:
        super().__init__()
        self.scale_factor = scale_factor
        self._health = 10
        self.shoot_delay = 4
        self.shoot_timer = 0
        
    
    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        sr.scale(self.scale_factor)
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())

    def start(self):
        pass
        self.direction = 1
        
    def update(self, delta_time):
        self.shoot_timer += delta_time
        y_move = 50
        #Move down
        if self.direction == 1:
            self._gameObject.transform.position.y += y_move * delta_time
            if self._gameObject.transform.position.y >= 600:
                self.direction = -1  # Change direction to up
        #Move up
        else:
            self._gameObject.transform.position.y -= y_move * delta_time
            if self._gameObject.transform.position.y <= 400:
                self.direction = 1  # Change direction to down
            
        if self.shoot_timer >= self.shoot_delay:
            self.shoot()
            self.shoot_timer = 0 
    
    def shoot(self):
        #self.shoot_sound.play()
        projectile = GameObject(None)
        sr = projectile.add_component(SpriteRenderer("EnemyLaser.png"))
        scale_factor = 5  # You can adjust this value as needed
        sr.scale(scale_factor)
        projectile.add_component(EnemyLaser())


        projectile_position = pygame.math.Vector2( 1200
                                                 , 400)

        projectile.transform.position = projectile_position
        self._game_world.current_State.instantiate(projectile)
        
