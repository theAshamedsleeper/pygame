import pygame
from State import MenuState
from State import FirstLevelState
from State import SecondLevelState
from State import ThirdLevelState
from State import loosOrVicState
from GameObject import GameObject

class GameWorld:
    
    def __init__(self) -> None:
        pygame.init()  

        self._gameObjects = []
        self._screen = pygame.display.set_mode((1280, 750))
        self._running = True
        self._clock = pygame.time.Clock()
        self._clock.tick(60)
        self._nextState = None
        self._newState = None
        self._music_vol = 100
        self._SFX_vol = 100
        self._started_on_level = False
        self._graphics = ["Low", "Medium", "High"]
        self._STT_ammo_count = "|||||"
        self._score = 0
        self._game_paused = False
        menu = MenuState(self)
        self._currentState = menu
        

    @property
    def screen(self):
        return self._screen
    
    @property 
    def current_State(self):
        return self._currentState
    
    @property
    def music_volume(self):
        return self._music_vol
    
    @property 
    def SFX_volume(self):
        return self._SFX_vol
    
    @property 
    def Graphics(self):
        return self._graphics
    
    @property 
    def Score(self):
        return self._score
    
    @property
    def start_game(self):
        return self._started_on_level
    
    @property
    def STT_ammo(self):
        return self._STT_ammo_count
    
    @property
    def worldPause(self):
        return self._game_paused
    
    @worldPause.setter
    def worldPause(self, value):
        self._game_paused = value
    
    @STT_ammo.setter
    def STT_ammo(self, value):
        self._STT_ammo_count = value
    
    @start_game.setter
    def start_game(self,value):
        self._started_on_level = value
        
    @Score.setter
    def Score(self,value):
        self._score = value
        
    @music_volume.setter
    def music_volume(self,value):
        self._music_vol = value
        
    @SFX_volume.setter
    def SFX_volume(self,value):
        self._SFX_vol = value
        
    @Graphics.setter
    def Graphics(self,value):
        self._graphics = value

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
            delta_time = self._clock.tick(60) / 1000.0 # limits FPS to 60

            #drawing the game
            if self._nextState is not None:
                self._currentState = self._nextState
                self.Awake()
                self.Start()
                self._nextState = None
            self._currentState.update(delta_time)
            

            pygame.display.flip()
            

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