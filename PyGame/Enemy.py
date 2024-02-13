import pygame
import random
import pygame
from Components import Component
from GameObject import GameObject

# Define the Enemy class
class Enemy(Component):
    def __init__(self):
        super().__init__()

    def awake(self, game_world):
        sr = self.gameObject.get_component("SpriteRenderer")
        random_x = random.randint(0, game_world.screen.get_width() - sr.sprite_image.get_width())
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(), game_world.screen.get_height())
        self.gameObject.transform.position = pygame.math.Vector2(random_x, 0)

    def start(self):
        pass

    def update(self, delta_time):
        speed = 100
        movement = pygame.math.Vector2(0, speed)
        if self.active:
            self.gameObject.transform.translate(movement * delta_time)
            bottom_limit = self._screen_size.y

            # Check for collisions with bullets
            for bullet in self._game_world.current_State._gameObjects:
                if bullet.name == "Bullet":
                    if self.gameObject.transform.position.distance_to(bullet.transform.position) < 20:
                        self.gameObject.destroy()
                        bullet.destroy()
                        return

            # Destroy the enemy if it reaches the bottom of the screen
            if self.gameObject.transform.position.y > bottom_limit:
                self.gameObject.destroy()

    def set_active(self, active):
        super().set_active(active)
        # Additional logic to handle activation/deactivation if needed
