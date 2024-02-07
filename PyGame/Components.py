from abc import ABC, abstractmethod
import pygame

class Component(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._gameObject = None
    
    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self, value):
        self._gameObject = value
        

    @abstractmethod
    def awake(self,game_world):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass    

class Transform(Component):

    def __init__(self, position) -> None:
        super().__init__()
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def translate(self, direction):
        self._position += direction

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass

class SpriteRenderer(Component):
    
    def __init__(self,sprite_name) -> None:
        super().__init__()
        
        self._sprite_image = pygame.image.load(f"Assets\\{sprite_name}")
        self._sprite = pygame.sprite.Sprite()
        self._sprite.rect = self._sprite_image.get_rect()

    @property
    def sprite_image(self):
        return self._sprite_image    
    
    @sprite_image.setter
    def sprite_image(self, value):
        self._sprite_image = value      
    
    

    def awake(self, game_world):
        self._game_world = game_world
        self._sprite.rect.topleft = self.gameObject.transform.position

    def start(self):
        pass

    def update(self, delta_time):
        self._sprite.rect.topleft = self.gameObject.transform.position
        self._game_world.screen.blit(self._sprite_image, self._sprite.rect)

class Animator(Component):

    def __init__(self) -> None:
        super().__init__()
        self._animations = {}
        self._current_animation = None
        self._animation_time = 0
        self._current_frame_index = 0


    def add_animation(self, name, *args):
        frames =[]
        for arg in args:
            sprite_image = pygame.image.load(f"Assets\\{arg}")
            frames.append(sprite_image)

        self._animations[name] = frames

    def play_animation(self, animation):
        self._current_animation = animation

    def awake(self, game_world):
         self._sprite_renderer = self._gameObject.get_component("SpriteRenderer")

    def start(self):
        pass

    def update(self, delta_time):
        # Time per frame in seconds (adjust as needed)
        frame_duration = 0.05

        # Update the time accumulator
        self._animation_time += delta_time

        # Check if it's time to update the frame
        if self._animation_time >= frame_duration:
            # Reset the time accumulator
            self._animation_time = 0

            # Update the frame index
            self._current_frame_index += 1

            # Get the current animation sequence
            animation_sequence = self._animations[self._current_animation]

            # Loop the animation
            if self._current_frame_index >= len(animation_sequence):
                self._current_frame_index = 0

            # Update the sprite image
            self._sprite_renderer.sprite_image = animation_sequence[self._current_frame_index]

class Laser(Component):
    def awake(self, game_world):
        pass
    def start(self):
        pass
    def update(self, delta_time):
        #speed = 500
        #movement = pygame.math.Vector2(0,-speed)
        pass