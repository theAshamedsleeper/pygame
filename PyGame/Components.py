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
        self._sprite_mask = pygame.mask.from_surface(self.sprite_image)
        
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
    def sprite_mask(self):
        return self._sprite_mask    
    
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

       # pygame.draw.rect(self._game_world.screen, (255, 0, 0), self._sprite.rect, 1)

    def scale(self, scale_factor):
        if scale_factor <=0:
            raise ValueError("Scale factor must be greater than zero")
        
        self.sprite_image = pygame.transform.scale(self._og_sprite_image,
                                                   (int(self.og_sprite_image.get_width() * scale_factor),
                                                   int(self._og_sprite_image.get_height() * scale_factor)))
        
        # Scale the rectangle
        original_center = self._sprite.rect.center
        self._sprite.rect.size = self.sprite_image.get_size()
        self._sprite.rect.center = original_center
        
        
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
        self._damage = 2
        collider = self._gameObject.get_component("Collider")
        collider.subscribe("collision_enter",self.on_collision_enter)
        collider.subscribe("collision_exit", self.on_collision_exit)
        collider.subscribe("pixel_collision_enter", self.on_pixel_collision_enter)
        collider.subscribe("pixel_collision_exit", self.on_pixel_collision_exit)
    def start(self):
        pass
    def update(self, delta_time):

        speed = 17
        direction = pygame.math.Vector2(speed,0)
        self._gameObject.transform.translate(direction)
        
        if self._gameObject.transform.position.x > self._screen_size.x:
            self._gameObject.destroy()
        #   print("Remove_check :-)")
            
    def on_collision_enter(self, other):
        if other.gameObject.has_component("EnemyLaser"):
            laser = other.gameObject.get_component("EnemyLaser")
            laser.gameObject.destroy()

    def on_collision_exit(self, other):
        print("collision exit")

    def on_pixel_collision_enter(self, other):
        if other.gameObject.has_component("Enemy"):
            enemy = other.gameObject.get_component("Enemy")
            enemy.health -= self._damage
            self._gameObject.destroy()

        if other.gameObject.has_component("EnemyLvl2"):
            enemy = other.gameObject.get_component("EnemyLvl2")
            enemy.health -= self._damage
            self._gameObject.destroy()
            
        if other.gameObject.has_component("Boss"):
            enemy = other.gameObject.get_component("Boss")
            enemy.lose_health(self._damage)
            self._gameObject.destroy()


    def on_pixel_collision_exit(self, other):
        print("pixel collision exit")
            

class Collider():
    def __init__(self) -> None:
        self._other_colliders = []
        self._other_masks = []
        self._listeners = {}

    def awake(self, game_world):
        self.sr = self.gameObject.get_component("SpriteRenderer")
        self._collision_box = self.sr.sprite_rect
        self._sprite_mask = self.sr.sprite_mask
        game_world.current_State.colliders.append(self)

    @property
    def collision_box(self):
        return self._collision_box
    
    @property
    def sprite_mask(self):
        return self._sprite_mask
    
    def subscribe(self, service, method):
        self._listeners[service] = method
    
    def collision_check(self, other):
        self._collision_box = self.sr.sprite_rect
        is_rect_colliding = self._collision_box.colliderect(other.collision_box)
        is_already_colliding = other in self._other_colliders

        if is_rect_colliding:
            if not is_already_colliding:
                self.collision_enter(other)
                other.collision_enter(self)
            if self.check_pixel_collision(self._collision_box, other.collision_box,self._sprite_mask, other.sprite_mask):
                if other not in self._other_masks:
                    self.pixel_collision_enter(other)
                    other.pixel_collision_enter(self)
               
            else:
                if other in self._other_masks:
                    self.pixel_collision_exit(other)
                    other.pixel_collision_exit(self)
        else:
            if is_already_colliding:
                self.collision_exit(other)
                other.collision_exit(self)

    def check_pixel_collision(self, collision_box1, collision_box2, mask1, mask2):
        offset_x = collision_box2.x - collision_box1.x
        offset_y = collision_box2.y - collision_box1.y

        return mask1.overlap(mask2, (offset_x,offset_y)) is not None

    def start(self):
        pass

    def update(self, delta_time):
        pass

    def collision_enter(self, other):
        self._other_colliders.append(other)
        if "collision_enter" in self._listeners:
            self._listeners["collision_enter"](other)

    def collision_exit(self, other):
         self._other_colliders.remove(other)
         if "collision_exit" in self._listeners:
            self._listeners["collision_exit"](other)

    def pixel_collision_enter(self,other):
        self._other_masks.append(other)
        if "pixel_collision_enter" in self._listeners:
            self._listeners["pixel_collision_enter"](other)

    def pixel_collision_exit(self,other):
         self._other_masks.remove(other)
         if "pixel_collision_exit" in self._listeners:
            self._listeners["pixel_collision_exit"](other)
         
class EnemyLaser(Component):

    def __init__(self) -> None:
        super().__init__()
        self._damage = 2
        
    def awake(self, game_world):
        self._game_world = game_world
        self._screen_size = pygame.math.Vector2(game_world.screen.get_width(),game_world.screen.get_height())
        collider = self._gameObject.get_component("Collider")
        collider.subscribe("collision_enter",self.on_collision_enter)
        collider.subscribe("collision_exit", self.on_collision_exit)
        collider.subscribe("pixel_collision_enter", self.on_pixel_collision_enter)
        collider.subscribe("pixel_collision_exit", self.on_pixel_collision_exit)

    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, value):
        self._damage = value
        
    def start(self):
        pass
    def update(self, delta_time):

        speed = -10
        direction = pygame.math.Vector2(speed,0)
        self._gameObject.transform.translate(direction)
        
        if self._gameObject.transform.position.x > self._screen_size.x:
            self._gameObject.destroy()

    def on_collision_enter(self, other):
        if other.gameObject.has_component("MotherShip"):
            mother_ship = self._game_world.current_State.get_mothership()
            mother_ship.take_damage(self._damage)
            self._gameObject.destroy()

        if other.gameObject.has_component("MShipPart"):
            mother_ship = self._game_world.current_State.get_mothership()
            mother_ship.take_damage(self._damage)
            self._gameObject.destroy()


    def on_collision_exit(self, other):
        print("collision exit")

    def on_pixel_collision_enter(self, other):
        print("pixel collision enter")

    def on_pixel_collision_exit(self, other):
        print("pixel collision exit")

    
