import pygame
from Components import Component

class Background(Component):
    def __init__(self, image_path, scroll_speed) -> None:
        super().__init__()
        self._background_image = pygame.image.load(image_path)
        self._scroll_speed = scroll_speed
        self._x_position = 0

    def start(self):
        pass

    def update(self, delta_time):
        screen_width = self._game_world.screen.get_width()
        self._x_position -= self._scroll_speed * delta_time

        # If the background has scrolled past its width, reset its position
        if self._x_position <= -self._background_image.get_width():
            self._x_position = 0

        # Draw the background image twice to cover the entire screen
        self._game_world.screen.blit(self._background_image, (self._x_position, 0))
        self._game_world.screen.blit(self._background_image, (self._x_position + self._background_image.get_width(), 0))