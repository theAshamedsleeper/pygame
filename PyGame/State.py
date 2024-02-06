from abc import ABC, abstractmethod
import pygame

class State(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def awake(self, game_world):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass