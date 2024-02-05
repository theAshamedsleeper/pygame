from Components import Component
import pygame

class Player(Component):
    def awake(self, game_world):
        pass
    def start(self):
        pass
    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        speed = 250
        movement = pygame.math.Vector2(0,0)

        if keys[pygame.K_w]:
            movement.y -= speed
        if keys[pygame.K_s]:
            movement.y += speed
        if keys[pygame.K_a]:
            movement.x -= speed
        if keys[pygame.K_d]:
            movement.x += speed
        self._gameObject.transform.translate(movement*delta_time)