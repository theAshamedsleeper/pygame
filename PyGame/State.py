from abc import ABC, abstractmethod
import pygame
from Player import Player
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator

class State(ABC):

    def __init__(self, game_world) -> None:
        super().__init__()
        self._gameObjects = []
        self._game_world = game_world

    @abstractmethod
    def awake(self, game_world):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass



class MenuState(State):

    def __init__(self, game_world) -> None:
        super().__init__(game_world)

    def awake(self, game_world):
        super().awake(game_world)
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self._game_world)        

    def start(self):
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self, delta_time):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level = FirstLevelState(self._game_world)
                    self._game_world.ChangeToNewState(level)
        # fill the screen with a color to wipe away anything from last frame
        self._game_world.screen.fill("cornflowerblue")
        #drawing the game

        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)



class FirstLevelState(State):

    def __init__(self, game_world) -> None:
        super().__init__(game_world)
        go = GameObject(pygame.math.Vector2(0,0))
        go.add_component(SpriteRenderer("player_ship.png"))
        go.add_component(Player())
        animator = go.add_component(Animator())

        animator.add_animation("Idle","player_ship.png",
                                # "player03.png",
                                # "player04.png",
                                # "player05.png",
                                # "player06.png",
                                # "player07.png",
                                # "player08.png",
                                # "player07.png",
                                # "player06.png",
                                # "player05.png",
                                # "player04.png",
                                # "player03.png"
                               )
        
        animator.play_animation("Idle")
        self._gameObjects.append(go)

    def instantiate(self, gameObject):
        gameObject.awake(self._game_world)
        gameObject.start()
        self._gameObjects.append(gameObject)

    def awake(self, game_world):
        super().awake(game_world)
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self._game_world)        

    def start(self):
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self, delta_time):
        # fill the screen with a color to wipe away anything from last frame
        self._game_world.screen.fill("lightcoral")

        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)

        
            