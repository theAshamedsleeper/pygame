from Components import Component
import pygame

class MotherShip(Component):

    def __init__(self) -> None:
        super().__init__()

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass

class Turret(Component):

    def __init__(self) -> None:
        super().__init__()

    def awake(self, game_world):
        return super().awake(game_world)
    
    def start(self):
        return super().start()
    
    def update(self, delta_time):
        return super().update(delta_time)
