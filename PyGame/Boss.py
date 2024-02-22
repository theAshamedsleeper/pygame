from Components import Component
from Components import SpriteRenderer
from Components import Animator
from GameObject import GameObject
from Components import EnemyLaser
from Components import Collider
import pygame
import math
from pygame import mixer

class Boss(Component):
    def __init__(self, scale_factor= 0.5) -> None:
        super().__init__()
        self.shoot_sound = mixer.Sound("Assets\\Audio\\scificannon.mp3")
        self.scale_factor = scale_factor
        self._health = 60
        self._shoot_delay = 4.878
        self._shoot_timer = 0
        self._spawn_timer = 0
        self._spawn_delay =4.878
    
    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self.shoot_sound.set_volume(self._game_world.SFX_volume/300)
        sr.scale(self.scale_factor)
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        collider = self._gameObject.get_component("Collider")
        collider.subscribe("collision_enter",self.on_collision_enter)
        collider.subscribe("collision_exit", self.on_collision_exit)
        collider.subscribe("pixel_collision_enter", self.on_pixel_collision_enter)
        collider.subscribe("pixel_collision_exit", self.on_pixel_collision_exit)

    def start(self):
        pass
        self.direction = 1
        
    def update(self, delta_time):
        self._shoot_timer += delta_time
        self._spawn_timer += delta_time
        y_move = 50
        #Move down
        if self.direction == 1:
            self._gameObject.transform.position.y += y_move * delta_time
            if self._gameObject.transform.position.y >= 500:
                self.direction = -1  # Change direction to up
        #Move up
        else:
            self._gameObject.transform.position.y -= y_move * delta_time
            if self._gameObject.transform.position.y <= 300:
                self.direction = 1  # Change direction to down
            
        if self._shoot_timer >= self._shoot_delay:
            self.shoot()
            self._shoot_timer = 0 
        if self._spawn_timer >= self._spawn_delay:
            self.spawn_minnions()
            self._spawn_timer = 0 
        
    def lose_health(self, damage):
        self._health -= damage
        if self._health <= 0:
            self._gameObject.destroy()
            self._game_world.current_State.give_score(100)
            self._game_world.current_State.move_to_endscreen(True)
    
    def spawn_minnions(self):
        self._game_world.current_State.spawn_enemy()
    
    def shoot(self):
        self.shoot_sound.play()
        projectile = GameObject(None)
        sr = projectile.add_component(SpriteRenderer("EnemyLaser.png"))
        projectile.add_component(Collider())
        scale_factor = 7  # You can adjust this value as needed
        sr.scale(scale_factor)
        el = projectile.add_component(EnemyLaser())
        el.damage = 10


        projectile_position = pygame.math.Vector2( self._gameObject.transform.position.x+(self._sprite_size.x-200)-sr.sprite_image.get_width()/2
                                                 , self._gameObject.transform.position.y)

        projectile.transform.position = projectile_position
        self._game_world.current_State.instantiate(projectile)
        
    def on_collision_enter(self, other):
        if other.gameObject.has_component("TurretLaser"):   
            self.lose_health(15)
                       

            

    def on_collision_exit(self, other):
        print("collision exit")

    def on_pixel_collision_enter(self, other):
        print("pixel collision enter")

    def on_pixel_collision_exit(self, other):
        print("pixel collision exit")

