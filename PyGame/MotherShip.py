from Components import Component
import pygame

class MotherShip(Component):

    def __init__(self) -> None:
        super().__init__()
        self._ship_part_north = None
        self._ship_part_south = None
        self._turret_one = None
        self._turret_two = None

    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = ((self._screen_size.x/8) - 50) - ((self._sprite_size.x/8)*7) #Spwn Location
        self._gameObject.transform.position.y = (self._screen_size.y/2) - (self._sprite_size.y/2) #Spwn Location       

    def start(self):
        self._ship_part_north.transform.position.y = ((self._screen_size.y/2) - 250) - (self._sprite_size.y/2)

    def update(self, delta_time):
        pass

    def add_ship_part(self, go, choice):
        if choice == 0:
            self._ship_part_north = go
        if choice == 1:
            self._ship_part_south = go
        

class MShipPart(Component):
    
    def __init__(self, rotation, position) -> None:
        super().__init__()
        self._rotation = rotation
        self._position = position


    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        sr.sprite_image = pygame.transform.rotate(sr.sprite_image, self._rotation)
        sr.sprite_rect = sr.sprite_image.get_rect(center=sr.sprite_rect.center)
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = ((self._screen_size.x/8) - 50) - ((self._sprite_size.x/8)*7) #Spwn Location
        self._gameObject.transform.position.y = (self._screen_size.y/2) - (self._sprite_size.y/2) #Spwn Location         
    
    def start(self):
        return super().start()
    
    def update(self, delta_time):
        return super().update(delta_time)


class Turret(Component):

    def __init__(self) -> None:
        super().__init__()

    def awake(self, game_world):
        return super().awake(game_world)
    
    def start(self):
        return super().start()
    
    def update(self, delta_time):
        return super().update(delta_time)
