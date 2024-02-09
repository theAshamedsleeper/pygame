from abc import ABC, abstractmethod
import pygame
from Player import Player
from MotherShip import MotherShip
from MotherShip import MShipPart
from MotherShip import Turret
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator
from Background import Background

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
        
        self._background_image_path ="photo2pixel_download (7).png"
        self._scroll_speed = 300
        self._background_go = GameObject(position=(0, 0))
        self._background_go.add_component(Background(game_world, image_path=self._background_image_path, scroll_speed=self._scroll_speed))

        go_mothership = GameObject(pygame.math.Vector2(0,0))
        go_mothership.add_component(SpriteRenderer("space_breaker_asset\\Others\\Stations\\station.png"))
        go_mothership.add_component(MotherShip())
        go_northship = GameObject(pygame.math.Vector2(0,0))
        go_northship.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Big\\body_02.png"))
        go_northship.add_component(MShipPart(0, 0))
        go_mothership.get_component("MotherShip").add_ship_part(go_northship, 0)


        go_player = GameObject(pygame.math.Vector2(0,0))
        go_player.add_component(SpriteRenderer("player_ship.png"))
        go_player.add_component(Player())
        
        self._gameObjects.append(go_northship)
        self._gameObjects.append(go_player)
        self._gameObjects.append(go_mothership)


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

        self._background_go.update(delta_time)

        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)

        self._gameObjects = [obj for obj in self._gameObjects if not obj._is_destroyed]

        
            