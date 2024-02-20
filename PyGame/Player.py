from Components import Component
import pygame
from pygame import mixer
from GameObject import GameObject
from Components import Laser
from Components import SpriteRenderer


class Player(Component):

    def __init__(self):
        self.shoot_delay = 0.15
        self.shoot_timer = 0
        self.shoot_sound = mixer.Sound("Assets\\Audio\\Pew1.mp3")

        #property
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
        pass

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        speed = 650
        movement = pygame.math.Vector2(0,0)

        
        self.shoot_timer +=delta_time

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement.y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement.y += speed

        bottom_limit = self._screen_size.y - self._sprite_size.y

        #Player boundries for top and bottom of screen
        if self._gameObject.transform.position.y > bottom_limit:
            self._gameObject.transform.position.y = bottom_limit
        elif self._gameObject.transform.position.y < 20:
            self._gameObject.transform.position.y = 20
     
        if keys[pygame.K_SPACE] and self.shoot_timer >= self.shoot_delay:
            
            self.shoot()
            self.shoot_timer = 0 #resets cooldown after shoot()
 
        self._gameObject.transform.translate(movement*delta_time)

    def shoot(self):
        self.shoot_sound.play()
        projectile = GameObject(None)
        sr = projectile.add_component(SpriteRenderer("tile001.png"))
        projectile.add_component(Laser())

        projectile_position = pygame.math.Vector2(self._gameObject.transform.position.x+(self._sprite_size.x-10)-sr.sprite_image.get_width()/2
                                                 ,self._gameObject.transform.position.y)

        projectile.transform.position = projectile_position


        self._game_world.current_State.instantiate(projectile)

class Thruster(Component):

    def __init__(self) -> None:
        super().__init__()

    def draw_flame(self, surface, ship_position):
        flame_image = pygame.Surface((10, 20))
        flame_image.fill((255, 69, 0))  # Orange color flame
        flame_rect = flame_image.get_rect(midbottom=ship_position)
        surface.blit(flame_image, flame_rect)

    def awake(self, game_world):
        return super().awake(game_world)
    
    def start(self):
        return super().start()

    def update(self, delta_time):
        ship_position = self._gameObject.transform.position
        ship_movement = self._gameObject.get_component("Player").movement
        
        if ship_movement.y < 0:  # Moving up
            self.draw_flame(self._game_world.screen, ship_position - pygame.math.Vector2(0, 10))
        elif ship_movement.y > 0:  # Moving down
            self.draw_flame(self._game_world.screen, ship_position + pygame.math.Vector2(0, 10))

    
    