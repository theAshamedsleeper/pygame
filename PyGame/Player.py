from Components import Component
import pygame
from GameObject import GameObject
from Components import Laser
from Components import SpriteRenderer


class Player(Component):
    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = (self._screen_size.x/10) - (self._sprite_size.x/2)
        self._gameObject.transform.position.y = (self._screen_size.y/2) - (self._sprite_size.y/2)

    def start(self):
        pass

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        speed = 500
        movement = pygame.math.Vector2(0,0)

        if keys[pygame.K_w]:
            movement.y -= speed
        if keys[pygame.K_s]:
            movement.y += speed
        if keys[pygame.K_a]:
            movement.x -= speed
        if keys[pygame.K_d]:
            movement.x += speed
        if keys[pygame.K_COMMA]:
            self.shoot()
            
        self._gameObject.transform.translate(movement*delta_time)

        

    def shoot(self):
        projectile = GameObject(None)
        sr = projectile.add_component(SpriteRenderer("tile001.png"))
        projectile.add_component(Laser())

        projectile_position = pygame.math.Vector2(self._gameObject.transform.position.x+(self._sprite_size.x/2)-sr.sprite_image.get_width()/2
                                                 ,self._gameObject.transform.position.y-40)

        projectile.transform.position = projectile_position


        self._game_world.current_State.instantiate(projectile)