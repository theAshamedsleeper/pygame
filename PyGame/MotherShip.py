from Components import Component
from Components import SpriteRenderer
from Components import Animator
from TurretLaser import TurretLaser
from GameObject import GameObject
import pygame
import math
from pygame import mixer

class MotherShip(Component):
    CURRENT_MOUSE = None
    PREVIOUS_MOUSE = None
    shoot_delay = 3

    def __init__(self) -> None:
        super().__init__()
        self._ship_part_north = None
        self._ship_part_south = None
        self._turret_one = None
        self._turret_two = None
        self._turret_three = None
        self._turret_four = None
        self._shot_index = 0
        self._shoot_time = 0
        self._plasma_anim = []
        self._plasma_sound = None
        self._health = 200

    
    
    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = ((self._screen_size.x/7)) - 120 #Spwn Location
        self._gameObject.transform.position.y = (self._screen_size.y/2) #Spwn Location       
        self._plasma_anim = self.create_anim()
        self._plasma_sound = mixer.Sound("Assets\\Audio\\sinus-bomb.mp3")

    def start(self):
        self._ship_part_north.transform.position.y = ((self._screen_size.y/2) - 185) 
        self._ship_part_south.transform.position.y = ((self._screen_size.y/2) + 185) 
        self._turret_one.transform.position.y = ((self._screen_size.y/2) - 250)
        self._turret_two.transform.position.y = ((self._screen_size.y/2) - 185)
        self._turret_three.transform.position.y = ((self._screen_size.y/2) + 185)
        self._turret_four.transform.position.y = ((self._screen_size.y/2) + 250)
        

    def update(self, delta_time):
        
        self._shoot_time += delta_time
        
        if self._shoot_time >= self.shoot_delay:
            
            self.PREVIOUS_MOUSE = self.CURRENT_MOUSE
            self.CURRENT_MOUSE = pygame.mouse.get_pressed()
            
            if self.CURRENT_MOUSE[2] and not self.PREVIOUS_MOUSE[2]:  # Index 2 corresponds to the right mouse button
                match self._shot_index:
                    case 0:
                        turret = self._turret_one.get_component("Turret")
                        turret.shoot(self._plasma_anim, self._plasma_sound)
                        self._shot_index = 3
                        self._shoot_time = 0
                    case 1:
                        turret = self._turret_two.get_component("Turret")
                        turret.shoot(self._plasma_anim, self._plasma_sound)
                        self._shot_index = 2
                        self._shoot_time = 0
                    case 2:
                        turret = self._turret_three.get_component("Turret")
                        turret.shoot(self._plasma_anim, self._plasma_sound)
                        self._shot_index = 0
                        self._shoot_time = 0
                    case 3:
                        turret = self._turret_four.get_component("Turret")
                        turret.shoot(self._plasma_anim, self._plasma_sound)
                        self._shot_index = 1
                        self._shoot_time = 0

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
    
    def create_anim(self):
        plasma_sprite_path = "Assets\\NicoEffects\\Effect_TheVortex\\30fps\\"
        sprite = (f"{plasma_sprite_path}Frames\\Effect_TheVortex_1\\")
        sprite_sheet = pygame.image.load(f"{plasma_sprite_path}Spritesheets\\Effect_TheVortex_1_427x431.png").convert_alpha()      
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_width, frame_height = (427, 431) 
        for i in range(24):
            x = i * frame_width % sheet_width
            y = (i * frame_width // sheet_width) * frame_height
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frames.append(frame)
        
        return frames

        

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
        self._ammo = 1
        self._sound = mixer.Sound("Assets\\Audio\\plasmacannon.mp3")


    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = ((self._screen_size.x/7)) - 120 #Spwn Location
        self._gameObject.transform.position.y = (self._screen_size.y/2) #Spwn Location 
        self._sound.set_volume(self._game_world.SFX_volume/200)     
    
    def start(self):
        return super().start()
    
    def update(self, delta_time):
        sr = self._gameObject.get_component("SpriteRenderer")
        if self._ammo >= 1:
            mouse_pos = pygame.mouse.get_pos()
            
            dx = mouse_pos[0] - sr.sprite_rect.centerx
            dy = mouse_pos[1] - sr.sprite_rect.centery
            self._rotation = math.degrees(math.atan2(-dy, dx)) - 90
            
            # Rotate the original sprite image once and store the rotated image
            rotated_image = pygame.transform.rotate(sr.og_sprite_image, self._rotation)
            sr.sprite_image = rotated_image
            sr.sprite_rect = sr.sprite_image.get_rect(center=sr.sprite_rect.center)
        elif self._ammo <= 0:
            pass
        
    def shoot(self, animation, sound):
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
        go.add_component(TurretLaser(b_position, mouse_pos, direction, sound))
        go.add_component(SpriteRenderer(f"{sprite_path}tile000.png"))
        animator = go.add_component(Animator())

        animator.add_animation("Effect", f"{sprite_path}tile001.png",
                                    f"{sprite_path}tile002.png",
                                    f"{sprite_path}tile003.png",
                                    f"{sprite_path}tile004.png",
                                    f"{sprite_path}tile005.png",
                                    f"{sprite_path}tile006.png",)
        animator.add_loaded_animation("Plasma", animation)
        
        animator.play_animation("Effect")

        self._game_world.current_State.instantiate(go)
        self._sound.play()
        
        self._ammo -= 1
        if len(self._game_world.STT_ammo) > 0:
            self._game_world.STT_ammo = self._game_world.STT_ammo[:-1]
            self._game_world.current_State.instantiate(go)
            
        
        