from Components import Component
from Components import SpriteRenderer
from Components import Animator
from TurretLaser import TurretLaser
from GameObject import GameObject
import pygame
import math

class MotherShip(Component):
    CURRENT_MOUSE = None
    PREVIOUS_MOUSE = None

    def __init__(self) -> None:
        super().__init__()
        self._ship_part_north = None
        self._ship_part_south = None
        self._turret_one = None
        self._turret_two = None
        self._turret_three = None
        self._turret_four = None

    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = ((self._screen_size.x/7)) - 120 #Spwn Location
        self._gameObject.transform.position.y = (self._screen_size.y/2) #Spwn Location       

    def start(self):
        self._ship_part_north.transform.position.y = ((self._screen_size.y/2) - 185) 
        self._ship_part_south.transform.position.y = ((self._screen_size.y/2) + 185) 
        self._turret_one.transform.position.y = ((self._screen_size.y/2) - 250)
        self._turret_two.transform.position.y = ((self._screen_size.y/2) - 185)
        self._turret_three.transform.position.y = ((self._screen_size.y/2) + 185)
        self._turret_four.transform.position.y = ((self._screen_size.y/2) + 250)
        

    def update(self, delta_time):
        
        self.PREVIOUS_MOUSE = self.CURRENT_MOUSE
        self.CURRENT_MOUSE = pygame.mouse.get_pressed()
        
        if self.CURRENT_MOUSE[2] and not self.PREVIOUS_MOUSE[2]:  # Index 2 corresponds to the right mouse button
            turret = self._turret_one.get_component("Turret")
            turret.shoot()

    def add_ship_part(self, go, choice):
        if choice == 0:
            self._ship_part_north = go
        if choice == 1:
            self._ship_part_south = go
    
    def add_turret_part(self, go, choice):
        if choice == 0:
            self._turret_one = go
        if choice == 1:
            self._turret_two = go
        if choice == 2:
            self._turret_three = go
        if choice == 3:
            self._turret_four = go
        

class MShipPart(Component):
    
    def __init__(self, rotation) -> None:
        super().__init__()
        self._rotation = rotation
        

    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        sr.sprite_image = pygame.transform.rotate(sr.sprite_image, self._rotation)
        sr.sprite_rect = sr.sprite_image.get_rect(center=sr.sprite_rect.center)
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = ((self._screen_size.x/7)) - 120 #Spwn Location
        self._gameObject.transform.position.y = (self._screen_size.y/2) #Spwn Location        
    
    def start(self):
        return super().start()
    
    def update(self, delta_time):
        return super().update(delta_time)


class Turret(Component):

    def __init__(self) -> None:
        super().__init__()
        self._rotation = 0

    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = ((self._screen_size.x/7)) - 120 #Spwn Location
        self._gameObject.transform.position.y = (self._screen_size.y/2) #Spwn Location      
    
    def start(self):
        return super().start()
    
    def update(self, delta_time):
        sr = self._gameObject.get_component("SpriteRenderer")
        mouse_pos = pygame.mouse.get_pos()
        
        dx = mouse_pos[0] - sr.sprite_rect.centerx
        dy = mouse_pos[1] - sr.sprite_rect.centery
        self._rotation = math.degrees(math.atan2(-dy, dx)) - 90
        
        # Rotate the original sprite image once and store the rotated image
        rotated_image = pygame.transform.rotate(sr.og_sprite_image, self._rotation)
        sr.sprite_image = rotated_image
        sr.sprite_rect = sr.sprite_image.get_rect(center=sr.sprite_rect.center)
        
    def shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        sprite_path = "space_breaker_asset\\Weapons\\Small\\Laser\\turretlaserAnim\\"

        dx = mouse_pos[0] - self._gameObject.transform.position.x
        dy = mouse_pos[1] - self._gameObject.transform.position.y
        magnitude = math.sqrt(dx ** 2 + dy ** 2)

        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude

        direction = (dx, dy)
        b_position = self._gameObject.transform.position + (direction)

        for i in range(30):
            b_position += (dx, dy)


        go = GameObject(None)
        go.add_component(TurretLaser(b_position, mouse_pos, direction))
        go.add_component(SpriteRenderer(f"{sprite_path}tile000.png"))
        animator = go.add_component(Animator())

        self._game_world.current_State.instantiate(go)

        animator.add_animation("Effect", f"{sprite_path}tile001.png",
                                    f"{sprite_path}tile002.png",
                                    f"{sprite_path}tile003.png",
                                    f"{sprite_path}tile004.png",
                                    f"{sprite_path}tile005.png",
                                    f"{sprite_path}tile006.png",)
        
        animator.play_animation("Effect")
        
        