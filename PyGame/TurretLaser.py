import pygame
from Components import Component
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator

class TurretLaser(Component):

    def __init__(self, position, target_pos, direction) -> None:
        super().__init__()
        self._position_to_set = position
        self._target_pos = target_pos
        self._direction = direction

    def awake(self, game_world):
        self._gameObject.transform.position = self._position_to_set
        self._game_world = game_world

    def start(self):
        self._animator = self._gameObject.get_component("Animator")


    def update(self, delta_time):
        
        if self._animator.is_on_final_frame():
            self._gameObject.destroy()

    def create_child(self):
        sprite_path = "space_breaker_asset\\Weapons\\Small\\Laser\\turretlaserAnim\\"
        new_object = GameObject(None)
        position = self._gameObject.transform.position

        for i in range(30):
            position += (self._direction)

        new_object.add_component(TurretLaser(position, self._target_pos, self._direction))
        new_object.add_component(SpriteRenderer(f"{sprite_path}tile000.png"))
        animator = new_object.add_component(Animator())

        self._game_world.current_State.instantiate(new_object)

        animator.add_animation("Effect", f"{sprite_path}tile001.png",
                                    f"{sprite_path}tile002.png",
                                    f"{sprite_path}tile003.png",
                                    f"{sprite_path}tile004.png",
                                    f"{sprite_path}tile005.png",
                                    f"{sprite_path}tile006.png",)
        
        animator.play_animation("Effect")