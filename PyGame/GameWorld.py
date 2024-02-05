import pygame
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator
from Player import Player

class GameWorld:
    
    def __init__(self) -> None:
        pygame.init()
        
        self._gameObjects = []
        go = GameObject(pygame.math.Vector2(0,0))
        go.add_component(SpriteRenderer("player.png"))
        go.add_component(Player())
        animator = go.add_component(Animator())

        animator.add_animation("Idle","player02.png",
                                "player03.png",
                                "player04.png",
                                "player05.png",
                                "player06.png",
                                "player07.png",
                                "player08.png",
                                "player07.png",
                                "player06.png",
                                "player05.png",
                                "player04.png",
                                "player03.png",)
        
        animator.play_animation("Idle")
        self._gameObjects.append(go)

        self._screen = pygame.display.set_mode((1280, 720))
        self._running = True
        self._clock = pygame.time.Clock()

    @property
    def screen(self):
        return self._screen

    def Awake(self):
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)
    
    def Start(self):
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def Update(self):
        while self._running:
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            # fill the screen with a color to wipe away anything from last frame
            self._screen.fill("cornflowerblue")
            delta_time = self._clock.tick(60) / 1000.0

            #drawing the game
            #Makes a copy om _gameObjects and runs through that instead of the orginal
            for gamObjects in self._gameObjects[:]:
                gamObjects.update(delta_time)

            # flip() the display to put your work on screen
            pygame.display.flip()
            self._clock.tick(60) # limits FPS to 60

        pygame.quit()

gw = GameWorld()

gw.Awake()
gw.Start()
gw.Update()