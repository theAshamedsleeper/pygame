import pygame
from Components import Component
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator
from Components import Collider
from pygame import mixer

class TurretLaser(Component):
    spawn_delay = 0.15


    def __init__(self, position, target_pos, direction, sound) -> None:
        super().__init__()
        self._position_to_set = position
        self._target_pos = target_pos
        self._direction = direction
        self.target_x, self.target_y = self._target_pos
        self._animation = {}
        self.spawn_time = 0
        self.spawned = False
        self._sound = sound
        

    def awake(self, game_world):
        self._gameObject.transform.position = self._position_to_set
        self._game_world = game_world
        self._sr = self._gameObject.get_component("SpriteRenderer")

    def start(self):
        self._animator = self._gameObject.get_component("Animator")
        self._animator.frame_duration = 0.05
        self._animation = self._animator.animations["Effect"]
        self._plas_anim = self._animator.animations["Plasma"]
        self._image =self._sr.sprite_image
            


    def update(self, delta_time):
        
        self.spawn_time += delta_time

        if not (self.target_x - 10 <= self._gameObject.transform.position[0] <= self.target_x + 10 and
                self.target_y - 10 <= self._gameObject.transform.position[1] <= self.target_y + 10):
            if self.spawn_time >= self.spawn_delay or self.spawn_time <= self.spawn_delay:
                if self.spawned == False:
                    self.create_child()
                    self.spawned = True
        elif (self.target_x - 10 <= self._gameObject.transform.position[0] <= self.target_x + 10 and
                self.target_y - 10 <= self._gameObject.transform.position[1] <= self.target_y + 10):
            self.create_explosion(self._sound)

        if self._animator.is_on_final_frame():
            self._gameObject.destroy()

    def create_child(self):
        new_object = GameObject(None)
        position = self._gameObject.transform.position + self._direction

        for i in range(20):
            position += (self._direction)

        new_object.add_component(TurretLaser(position, self._target_pos, self._direction, self._sound))
        new_object.add_component(SpriteRenderer(sprite_image=self._image))
        animator = new_object.add_component(Animator())

        animator.add_loaded_animation("Effect", self._animation)
        animator.add_loaded_animation("Plasma", self._plas_anim)
        
        animator.play_animation("Effect")

        self._game_world.current_State.instantiate(new_object)

    def create_explosion(self, sound):
        sprite_path = "NicoEffects\\Effect_TheVortex\\30fps\\Frames\\Effect_TheVortex_1\\"
        new_object = GameObject(None)
        position = self._gameObject.transform.position + self._direction

        new_object.add_component(PlamsaExplosion(position, sound))
        new_object.add_component(SpriteRenderer(f"{sprite_path}Effect_TheVortex_1_000.png"))
        new_object.add_component(Collider())
        animator = new_object.add_component(Animator())
        

        
        animator.add_loaded_animation("Plasma", self._plas_anim)
        
        animator.play_animation("Plasma")

        self._game_world.current_State.instantiate(new_object)

class PlamsaExplosion(Component):

    def __init__(self, position, sound) -> None:
        self._position_to_set = position
        self._sound = sound
        self._damage = 1000

    def awake(self, game_world):
        self._gameObject.transform.position = self._position_to_set
        self._game_world = game_world
        self._sound.set_volume(self._game_world.SFX_volume/200)
        collider = self._gameObject.get_component("Collider")
        collider.subscribe("collision_enter",self.on_collision_enter)
        collider.subscribe("collision_exit", self.on_collision_exit)
        collider.subscribe("pixel_collision_enter", self.on_pixel_collision_enter)
        collider.subscribe("pixel_collision_exit", self.on_pixel_collision_exit)
    
    def start(self):
        self._animator = self._gameObject.get_component("Animator")
        self._animator.frame_duration = 0.05
        self._sound.play()
    
    def update(self, delta_time):
        if self._animator.is_on_final_frame():
            self._gameObject.destroy()

    def on_collision_enter(self, other):
        if other.gameObject.has_component("Enemy"):
            enemy = other.gameObject.get_component("Enemy")
            enemy.health -= self._damage
            self._gameObject.destroy()
            self._game_world.current_State.give_score(10)
        
        if other.gameObject.has_component("EnemyLvl2"):
            enemy = other.gameObject.get_component("EnemyLvl2")
            enemy.health -= self._damage
            self._gameObject.destroy()
            self._game_world.current_State.give_score(20)

        if other.gameObject.has_component("EnemyLaser"):
            laser = other.gameObject.get_component("EnemyLaser")
            laser.gameObject.destroy()
            self._game_world.current_State.give_score(1)

            

    def on_collision_exit(self, other):
        print("collision exit")

    def on_pixel_collision_enter(self, other):
        print("pixel collision enter")

    def on_pixel_collision_exit(self, other):
        print("pixel collision exit")