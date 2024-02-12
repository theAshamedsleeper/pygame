from Components import Component
import pygame
import math

class MotherShip(Component):

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
        pass

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
        
