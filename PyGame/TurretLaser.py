import pygame
from Components import Component
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator

class TurretLaser(Component):
    spawn_delay = 0.15


    def __init__(self, position, target_pos, direction) -> None:
        super().__init__()
        self._position_to_set = position
        self._target_pos = target_pos
        self._direction = direction
        self.target_x, self.target_y = self._target_pos
        self._animation = {}
        self.spawn_time = 0
        self.spawned = False
        

    def awake(self, game_world):
        self._gameObject.transform.position = self._position_to_set
        self._game_world = game_world
        self._sr = self._gameObject.get_component("SpriteRenderer")

    def start(self):
        self._animator = self._gameObject.get_component("Animator")
        self._animator.frame_duration = 0.05
        self._animation = self._animator.animations["Effect"]
        self._image =self._sr.sprite_image
            


    def update(self, delta_time):
        
        self.spawn_time += delta_time

        if not (self.target_x - 10 <= self._gameObject.transform.position[0] <= self.target_x + 10 and
                self.target_y - 10 <= self._gameObject.transform.position[1] <= self.target_y + 10):
            if self.spawn_time >= self.spawn_delay or self.spawn_time <= self.spawn_delay:
                if self.spawned == False:
                    self.create_child()
                    self.spawned = True

        if self._animator.is_on_final_frame():
            self._gameObject.destroy()

    def create_child(self):
        new_object = GameObject(None)
        position = self._gameObject.transform.position + self._direction

        for i in range(20):
            position += (self._direction)

        new_object.add_component(TurretLaser(position, self._target_pos, self._direction))
        new_object.add_component(SpriteRenderer(sprite_image=self._image))
        animator = new_object.add_component(Animator())

        animator.add_loaded_animation("Effect", self._animation)
        
        animator.play_animation("Effect")

        self._game_world.current_State.instantiate(new_object)