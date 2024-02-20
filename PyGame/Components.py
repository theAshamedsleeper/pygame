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
    
    def __init__(self, sprite_name=None, sprite_image=None, game_world=None) -> None:
        super().__init__()
        
        self._game_world = game_world

        if sprite_image is None:
            self._sprite_image = pygame.image.load(f"Assets\\{sprite_name}").convert_alpha()
        else:
            self._sprite_image = sprite_image
        
        self._sprite = pygame.sprite.Sprite()
        image_width, image_height = self._sprite_image.get_size()
        self._sprite.rect = pygame.Rect(0,0, image_width, image_height)
        self._sprite.rect.center = (self._sprite.rect.width // 2, self._sprite.rect.height // 2)
        
        if sprite_name is not None:
            self._og_sprite_image = pygame.image.load(f"Assets\\{sprite_name}").convert_alpha()
        else:
            self._og_sprite_image = sprite_image

    @property
    def og_sprite_image(self):
        return self._og_sprite_image    
    
    @og_sprite_image.setter
    def og_sprite_image(self, value):
        self._og_sprite_image = value 

    @property
    def sprite_image(self):
        return self._sprite_image    
    
    @sprite_image.setter
    def sprite_image(self, value):
        self._sprite_image = value      
    
    @property
    def sprite_rect(self):
        return self._sprite.rect
    
    @sprite_rect.setter
    def sprite_rect(self, value):
        self._sprite.rect = value

    def awake(self, game_world):
        self._game_world = game_world
        self._sprite.rect.center = self.gameObject.transform.position
        

    def start(self):
        pass

    def update(self, delta_time):
        self._sprite.rect.center = self.gameObject.transform.position
        self._game_world.screen.blit(self._sprite_image, self._sprite.rect)

    def scale(self, scale_factor):
        if scale_factor <=0:
            raise ValueError("Scale factor must be greater than zero")
        
        self.sprite_image = pygame.transform.scale(self._og_sprite_image,
                                                   (int(self.og_sprite_image.get_width() * scale_factor),
                                                   int(self._og_sprite_image.get_height() * scale_factor)))
        
        
class Animator(Component):

    def __init__(self) -> None:
        super().__init__()
        self._animations = {}
        self._current_animation = None
        self._animation_time = 0
        self._current_frame_index = 0
        self._frame_duration = 0.05

    @property
    def animations(self):
        return self._animations
    
    @property
    def frame_duration(self):
        return self._frame_duration
    
    @frame_duration.setter
    def frame_duration(self, value):
        self._frame_duration = value


    def add_animation(self, name, rotation, *args):
        frames =[]
        for arg in args:
            sprite_image = pygame.image.load(f"Assets\\{arg}").convert_alpha()
            sprite_image = pygame.transform.rotate(sprite_image, rotation)
            frames.append(sprite_image)

        self._animations[name] = frames


    def add_animation_sheet(self, name, sprite_sheet_path, frame_size, num_frames):
        sprite_sheet = pygame.image.load(f"Assets\\{sprite_sheet_path}").convert_alpha()
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_width, frame_height = frame_size
        for i in range(num_frames):
            x = i * frame_width % sheet_width
            y = (i * frame_width // sheet_width) * frame_height
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frames.append(frame)
        self.animations[name] = frames

    def add_loaded_animation(self, name, animation):
        self._animations[name] = animation

    def play_animation(self, animation):
        self._current_animation = animation

    def awake(self, game_world):
        self._sprite_renderer = self._gameObject.get_component("SpriteRenderer")

    def start(self):
        pass

    def update(self, delta_time):

        # Update the time accumulator
        self._animation_time += delta_time

        # Check if it's time to update the frame
        if self._animation_time >= self._frame_duration:
            # Reset the time accumulator
            self._animation_time = 0

            # Update the frame index
            self._current_frame_index += 1

            # Get the current animation sequence
            animation_sequence = self._animations[self._current_animation]

            # Loop the animation
            if self._current_frame_index >= len(animation_sequence):
                self.is_on_final_frame()


            # Update the sprite image
            self._sprite_renderer.sprite_image = animation_sequence[self._current_frame_index]

    def is_on_second_frame(self):
        return self._current_frame_index == 1

    def is_on_final_frame(self):
        # Get the current animation sequence
        animation_sequence = self._animations[self._current_animation]
        # Check if the current frame index is at the last frame
        is_final_frame = self._current_frame_index >= len(animation_sequence) - 1
        if is_final_frame:
            # Reset the frame index to loop the animation
            self._current_frame_index = 0
        return is_final_frame
    

class Laser(Component):
    def awake(self, game_world):
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
    def start(self):
        pass
    def update(self, delta_time):

        speed = 17
        direction = pygame.math.Vector2(speed,0)
        self._gameObject.transform.translate(direction)
        
        if self._gameObject.transform.position.x > self._screen_size.x:
            self._gameObject.destroy()
        #   print("Remove_check :-)")
            

class Collider():
    def __init__(self) -> None:
        self._other_colliders = []

    def awake(self, game_world):
        sr = self.gameObject.get_component("SpriteRenderer")
        self._collision_box = sr.sprite.rect
        game_world.colliders.append(self)

    @property
    def collision_box(self):
        return self._collision_box
    
    def collision_check(self, other):
        is_rect_colliding = self._collision_box.colliderect(other.collision_box)
        is_already_colliding = other in self._other_colliders

        if is_rect_colliding:
            if not is_already_colliding:
                self.collision_enter(other)
                other.collision_enter(self)
        else:
            if is_already_colliding:
                self.collision_exit(other)
                other.collision_exit(self)

    def start(self):
        pass

    def update(self, delta_time):
        pass

    def collision_enter(self, other):
        self._other_colliders.append(other)
        print("Collision enter")

    def collision_exit(self, other):
         self._other_colliders.remove(other)
         print("Collision exit")
         
class EnemyLaser(Component):
    def awake(self, game_world):
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
    def start(self):
        pass
    def update(self, delta_time):

        speed = -10
        direction = pygame.math.Vector2(speed,0)
        self._gameObject.transform.translate(direction)
        
        if self._gameObject.transform.position.x > self._screen_size.x:
            self._gameObject.destroy()
