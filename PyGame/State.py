from abc import ABC, abstractmethod
import pygame
from Player import Player
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator
import pygame.locals
import threading
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
        self._dis = pygame.display.set_mode((3440, 1000))
        
        #uses the system font
        self._text_font = pygame.font.SysFont(None, 30, bold = False)
        self._text_font_sel = pygame.font.SysFont(None, 30, bold = True)
        self._menu_sele = 0
        self._opt_menu_sel = 1 #0 for down, for mid, 2 for up
        self._options_sele = False  
        self._graphics_opt = int(1)      


        
    def hande_input(self):
        global _menu_sele
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self._options_sele == False:
                        self.do_menu_input()
                    elif self._options_sele == True:
                        self._options_sele = False
                elif event.key == pygame.K_UP:
                    self._menu_sele -= 1
                elif event.key == pygame.K_DOWN:
                    self._menu_sele += 1
                if self._options_sele == True:
                    if event.key == pygame.K_LEFT:
                        self.do_options_input(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.do_options_input(1)


        # Clamp menu selection within range
        self._menu_sele = max(0, min(2, self._menu_sele))
    def do_menu_input(self):
        match self._menu_sele:
            case 0:#new game
                level = FirstLevelState(self._game_world)
                self._game_world.ChangeToNewState(level)
            case 1:#Options
                self._options_sele = True
                pass
            case 2:
                pygame.quit()
                quit()
    
    tmp = 1
    def do_options_input(self, value):
        self._opt_menu_sel += value
        self._opt_menu_sel = max(0, min(2, self._opt_menu_sel))
        self.tmp += value
        self.tmp = max(0, min(2, self.tmp))

        #Which option the player is on
        match self._menu_sele:
            case 0: #Music Volumen
                if self._opt_menu_sel == 2:
                    self._game_world.music_volume += 10     
                    if self._game_world.music_volume > 100:
                        self._game_world.music_volume = 100     
                elif self._opt_menu_sel == 0:
                    self._game_world.music_volume -= 10
                    if self._game_world.music_volume < 0:
                        self._game_world.music_volume = 0     
            case 1: #sfx Volumen
                if self._opt_menu_sel == 2:
                    self._game_world.SFX_volume += 10     
                    if self._game_world.SFX_volume > 100:
                        self._game_world.SFX_volume = 100     
                elif self._opt_menu_sel == 0:
                    self._game_world.SFX_volume -= 10     
                    if self._game_world.SFX_volume < 0:
                        self._game_world.SFX_volume = 0     
            case 2:#Grapchis options
                self._graphics_opt = self.tmp
        #Resets the pos to 1
        self._opt_menu_sel = 1
    
    def draw_text(self,text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self._dis.blit(img,(x,y))

    def awake(self, game_world):
        super().awake(game_world)
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self._game_world)     
#        self._game_world.Graphics = 1
        #self._graphics_optr = 1
        #input_thread = threading.Thread(target=self.hande_input,args=())
        #input_thread.start()

    def start(self):
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self, delta_time):        
        # fill the screen with a color to wipe away anything from last frame
        self._game_world.screen.fill("cornflowerblue")
        #drawing the game
        self.drawing_menu()
        self.hande_input()

        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)
        
    def drawing_menu(self):
        self.draw_text(f"{self._menu_sele}", self._text_font_sel, (0,0,0), 1000, 0)
        self.draw_text(f"{self._opt_menu_sel}", self._text_font_sel, (0,0,0), 1000, 50)
        if self._options_sele == False:
            match self._menu_sele:
                case 0:
                    self.draw_text("New Game", self._text_font_sel, (0,0,0), 600, 360)
                    self.draw_text("   Option", self._text_font, (0,0,0), 600, 410)
                    self.draw_text("     Quit", self._text_font, (0,0,0), 600, 460)
                case 1:
                    self.draw_text("New Game", self._text_font, (0,0,0), 600, 360)
                    self.draw_text("   Option", self._text_font_sel, (0,0,0), 600, 410)
                    self.draw_text("     Quit", self._text_font, (0,0,0), 600, 460)
                case 2:
                    self.draw_text("New Game", self._text_font, (0,0,0), 600, 360)
                    self.draw_text("   Option", self._text_font, (0,0,0), 600, 410)
                    self.draw_text("     Quit", self._text_font_sel, (0,0,0), 600, 460)
        #Options
        elif self._options_sele == True:
            match self._menu_sele:
                case 0:
                    self.draw_text("Music", self._text_font_sel, (0,0,0), 600, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font_sel, (0,0,0), 700, 360)
                    self.draw_text("SFX", self._text_font, (0,0,0), 600, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (0,0,0), 700, 410)
                    self.draw_text("Graphics", self._text_font, (0,0,0), 600, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (0,0,0), 700, 460)
                case 1:
                    self.draw_text("Music", self._text_font, (0,0,0), 600, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (0,0,0), 700, 360)
                    self.draw_text("SFX", self._text_font_sel, (0,0,0), 600, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font_sel, (0,0,0), 700, 410)
                    self.draw_text("Graphics", self._text_font, (0,0,0), 600, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (0,0,0), 700, 460)
                case 2:
                    self.draw_text("Music", self._text_font, (0,0,0), 600, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (0,0,0), 700, 360)
                    self.draw_text("SFX", self._text_font, (0,0,0), 600, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (0,0,0), 700, 410)
                    self.draw_text("Graphics", self._text_font_sel, (0,0,0), 600, 460)    
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font_sel, (0,0,0), 700, 460)




class FirstLevelState(State):

    def __init__(self, game_world) -> None:
        super().__init__(game_world)
        
        self._background_image_path ="SimpleBackgroundClear.png"
        self._scroll_speed = 300
        self._background_go = GameObject(position=(0, 0))
        self._background_go.add_component(Background(game_world, image_path=self._background_image_path, scroll_speed=self._scroll_speed))

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
        #self._gameObjects.append(self._background_go)

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

        
            