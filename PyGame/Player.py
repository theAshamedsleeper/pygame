from Components import Component
import pygame
from pygame import mixer
from GameObject import GameObject
from Components import Laser
from Components import SpriteRenderer
from Components import Collider


class Player(Component):

    def __init__(self):
        self.shoot_delay = 0.15
        self.shoot_timer = 0
        self.shoot_sound = mixer.Sound("Assets\\Audio\\Pew1.mp3")
        self._thruster = None
        self._thrusterMain = None
        self._movement = pygame.math.Vector2(0,0)

    @property
    def movement(self):
        return self._movement
        
    def awake(self, game_world):
        self._game_world = game_world
        self.shoot_sound.set_volume(self._game_world.SFX_volume/1000)
        sr = self._gameObject.get_component("SpriteRenderer")
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = (self._screen_size.x/4) - (self._sprite_size.x/2) #player spawn location x
        self._gameObject.transform.position.y = (self._screen_size.y/2) - (self._sprite_size.y/2) #player spawn location y

    def start(self):
        self._thruster.transform.position.y = (self._screen_size.y/2) - (self._sprite_size.y/2)
        self._thrusterMain.transform.position.y = (self._screen_size.y/2) - (self._sprite_size.y/2)

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        speed = 650
        self._movement = pygame.math.Vector2(0,0)

        
        self.shoot_timer +=delta_time

        #MainThruster
        #animationMain = self._thrusterMain.get_component("Animator")
        #animationMain.play_animation("Mid")
        #self._thrusterMain.transform.position.y = self._gameObject.transform.position.y +10 


        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self._movement.y -= speed
            animation = self._thruster.get_component("Animator")
            animation.play_animation("Bottom")
            self._thruster.transform.position.y = self._gameObject.transform.position.y +2
            self._thruster.transform.position.x = ((self._screen_size.x/4) - (self._sprite_size.x/2)) - 34 #player spawn location x  

            #Main
            self._thrusterMain.transform.position.y = self._gameObject.transform.position.y -10
            self._thrusterMain.transform.position.x = ((self._screen_size.x/4) - (self._sprite_size.x/2)) - 30 #player spawn location x
            animationMain = self._thrusterMain.get_component("Animator")
            animationMain.play_animation("Mid")      
            

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self._movement.y += speed
            animation = self._thruster.get_component("Animator")
            animation.play_animation("Top")
            self._thruster.transform.position.y = self._gameObject.transform.position.y -14
            self._thruster.transform.position.x = ((self._screen_size.x/4) - (self._sprite_size.x/2)) - 34 #player spawn location x

            #Main
            self._thrusterMain.transform.position.y = self._gameObject.transform.position.y +10
            self._thrusterMain.transform.position.x = ((self._screen_size.x/4) - (self._sprite_size.x/2)) - 30 #player spawn location x
            animationMain = self._thrusterMain.get_component("Animator")
            animationMain.play_animation("Mid")


        else:
            
            animation = self._thruster.get_component("Animator")
            animation.play_animation("Dead")
            self._thruster.transform.position.y = self._gameObject.transform.position.y -4
            self._thruster.transform.position.x = ((self._screen_size.x/4) - (self._sprite_size.x/2)) - 25 #player spawn location x


            #Main
            self._thrusterMain.transform.position.y = self._gameObject.transform.position.y
            self._thrusterMain.transform.position.x = ((self._screen_size.x/4) - (self._sprite_size.x/2)) - 34 #player spawn location x
            animationMain = self._thrusterMain.get_component("Animator")
            animationMain.play_animation("Mid")

        
        
        bottom_limit = self._screen_size.y - self._sprite_size.y

        #Player boundries for top and bottom of screen
        if self._gameObject.transform.position.y > bottom_limit:
            self._gameObject.transform.position.y = bottom_limit
        elif self._gameObject.transform.position.y < 20:
            self._gameObject.transform.position.y = 20
     
        if keys[pygame.K_SPACE] and self.shoot_timer >= self.shoot_delay:
            
            self.shoot()
            self.shoot_timer = 0 #resets cooldown after shoot()
 
        self._gameObject.transform.translate(self._movement*delta_time)

    def shoot(self):
        self.shoot_sound.play()
        projectile = GameObject(None)
        sr = projectile.add_component(SpriteRenderer("tile001.png"))
        projectile.add_component(Collider())
        
        projectile.add_component(Laser())

        projectile_position = pygame.math.Vector2(self._gameObject.transform.position.x+(self._sprite_size.x-10)-sr.sprite_image.get_width()/2
                                                 ,self._gameObject.transform.position.y)

        projectile.transform.position = projectile_position


        self._game_world.current_State.instantiate(projectile)

    def add_thruster(self, go, go2):
        self._thruster = go
        self._thrusterMain = go2

class Thruster(Component):
    def __init__(self) -> None:
        super().__init__()
        self._ship_movement = pygame.math.Vector2(0,0)
        self._rotation = -90

    def draw_flame(self, surface, ship_position):
        flame_image = pygame.Surface((10, 20))
        flame_image.fill((255, 0, 0))  
        flame_rect = flame_image.get_rect(midbottom=ship_position) # tegnet ved skibets bund hopefully?
        surface.blit(flame_image, flame_rect)

    @property
    def ship_movement(self):
        return self._ship_movement
    
    @ship_movement.setter
    def ship_movement(self, value):
        self._ship_movement = value

    def awake(self, game_world):
        self._game_world = game_world
        sr = self._gameObject.get_component("SpriteRenderer")
        sr.sprite_image = pygame.transform.rotate(sr.sprite_image, self._rotation)
        sr.sprite_rect = sr.sprite_image.get_rect(center=sr.sprite_rect.center)
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        self._sprite_size = pygame.math.Vector2(sr.sprite_image.get_width(),sr.sprite_image.get_height())
        self._gameObject.transform.position.x = ((self._screen_size.x/4) - (self._sprite_size.x/2)) - 50 #player spawn location x
    
    def start(self):
        return super().start()

    def update(self, delta_time):
        return super().update(delta_time)
       

    
    