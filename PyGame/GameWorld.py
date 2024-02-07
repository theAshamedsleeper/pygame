import pygame
from State import MenuState
from State import FirstLevelState
from GameObject import GameObject

class GameWorld:
    
    def __init__(self) -> None:
        pygame.init()  

        self._gameObjects = []
        self._screen = pygame.display.set_mode((1280, 720))
        self._running = True
        self._clock = pygame.time.Clock()
        menu = MenuState(self)
        self._currentState = menu
        self._nextState = None
        self._newState = None

    @property
    def screen(self):
        return self._screen
    
    @property
    def current_State(self):
        return self._currentState

    def Awake(self):
        self._currentState.awake(self)
        
    def Start(self):      
        self._currentState.start()  

    def StateStartUp(self):
        if self._newState is not None:
            self._currentState = self._newState
            self._newState = None  
            self.Awake()
            self.Start()            
        
    def Update(self):
        while self._running:
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            delta_time = self._clock.tick(60) / 1000.0

            #drawing the game
            if self._nextState is not None:
                self._currentState = self._nextState
                self._nextState = None
            self._currentState.update(delta_time)

            pygame.display.flip()
            self._clock.tick(60) # limits FPS to 60

        pygame.quit()

    def ChangeToNewState(self, newState):
        self._newState = newState
        self.StateStartUp()

    def ChangeState(self, nextState):
        self._nextState = nextState


gw = GameWorld()

gw.Awake()
gw.Start()
gw.Update()