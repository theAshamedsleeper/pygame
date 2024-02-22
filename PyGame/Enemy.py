import pygame
import random
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Component
from Components import EnemyLaser
from pygame import mixer


class Enemy(Component):
    def __init__(self, scale_factor=0.3) -> None:
        super().__init__()
        self._speed_x = 201
        self._speed_y = 50
        self._scale_factor = scale_factor
        self._stop_x_position = 1100 #X position where the enemies stop
        self._direction = 1  # Initial direction: 1 for down, -1 for up
        self._shoot_delay = 4.15
        self._shoot_timer = 0
        self._shoot_sound = mixer.Sound("Assets\\Audio\\Pew1.mp3")
    
    def awake(self, game_world):
        self._game_world = game_world
        self._shoot_sound.set_volume(self._game_world.SFX_volume/1000)

        sr = self._gameObject.get_component("SpriteRenderer")
        sr.scale(self._scale_factor)
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = (self._screen_size.x) + (self._sprite_size.x)  #enemy spawn location x
        self._gameObject.transform.position.y = random.randint(180, int(self._screen_size.y)) + (self._sprite_size.y) #enemy spawn location y

    def start(self):
        pass

    def update(self, delta_time):
        self._shoot_timer +=delta_time

        self._gameObject.transform.position.x -= self._speed_x * delta_time

        if self._gameObject.transform.position.x <= self._stop_x_position:
            self._speed_x = 0

        if self._shoot_timer >= self._shoot_delay:
            self.shoot()
            self._shoot_timer = 0 
        
        if self._direction == 1:
            self._gameObject.transform.position.y += self._speed_y * delta_time
            if self._gameObject.transform.position.y >= 720:
                self._direction = -1  # Change direction to up
                if self._stop_x_position >800:
                    self._stop_x_position-=100
                self._speed_x = 200
        else:
            self._gameObject.transform.position.y -= self._speed_y * delta_time
            if self._gameObject.transform.position.y <= 180:
                self._direction = 1  # Change direction to down
                if self._stop_x_position >800:
                    self._stop_x_position-=100
                self._speed_x = 200

    def shoot(self):
        self._shoot_sound.play()
        projectile = GameObject(None)
        sr = projectile.add_component(SpriteRenderer("EnemyLaser.png"))
        scale_factor = 3  # You can adjust this value as needed
        sr.scale(scale_factor)
        projectile.add_component(EnemyLaser())


        projectile_position = pygame.math.Vector2(self._gameObject.transform.position.x+(self._sprite_size.x-250)-sr.sprite_image.get_width()/2
                                                 ,self._gameObject.transform.position.y-85)

        projectile.transform.position = projectile_position
        self._game_world.current_State.instantiate(projectile)


