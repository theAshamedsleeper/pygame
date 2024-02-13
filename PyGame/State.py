from abc import ABC, abstractmethod
import pygame
from Player import Player
from MotherShip import MotherShip
from MotherShip import MShipPart
from MotherShip import Turret
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator
import pygame.locals
import threading
from pygame import mixer
from Background import Background
from MenuBackground import MenuBackground
from SavingScoreJson import SavingScore


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
        self._dis = pygame.display.set_mode((1280, 720))
        
        self._background_image_path ="MenuBackground.png"
        self._background_go = GameObject(position=(0, 0))
        self._background_go.add_component(MenuBackground(game_world, image_path=self._background_image_path))

        #uses the system font
        self._text_font = pygame.font.SysFont(None, 30, bold = False)
        self._text_font_sel = pygame.font.SysFont(None, 30, bold = True)
        self._menu_sele = 0
        self._opt_menu_sel = 1 #0 for down, 1 for mid, 2 for up
        self._options_sele = False  
        self._graphics_opt = 1      


        
    def hande_input(self):
        #global _menu_sele
        
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
        self._background_go.update(delta_time)

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

      #  background_music = mixer
        mixer.music.load("Assets\\Audio\\Background.mp3")
        mixer.music.play(-1)
        mixer.music.set_volume(.03)

        go_mothership = GameObject(pygame.math.Vector2(0,0))
        go_mothership.add_component(SpriteRenderer("space_breaker_asset\\Others\\Stations\\station.png"))
        go_mothership.add_component(MotherShip())
        go_northship = GameObject(pygame.math.Vector2(0,0))
        go_northship.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Big\\body_02.png"))
        go_northship.add_component(MShipPart(0))
        go_southship = GameObject(pygame.math.Vector2(0,0))
        go_southship.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Big\\body_02.png"))
        go_southship.add_component(MShipPart(180))
        go_turret_one = self.makeTurret("space_breaker_asset\\Bonus\\turret_01c_mk3.png")
        go_turret_two = self.makeTurret("space_breaker_asset\\Bonus\\turret_01c_mk3.png")
        go_turret_three = self.makeTurret("space_breaker_asset\\Bonus\\turret_01c_mk3.png")
        go_turret_four = self.makeTurret("space_breaker_asset\\Bonus\\turret_01c_mk3.png")
        
        go_mothership.get_component("MotherShip").add_ship_part(go_northship, 0)
        go_mothership.get_component("MotherShip").add_ship_part(go_southship, 1)
        go_mothership.get_component("MotherShip").add_turret_part(go_turret_one, 0)
        go_mothership.get_component("MotherShip").add_turret_part(go_turret_two, 1)
        go_mothership.get_component("MotherShip").add_turret_part(go_turret_three, 2)
        go_mothership.get_component("MotherShip").add_turret_part(go_turret_four, 3)
        


        go_player = GameObject(pygame.math.Vector2(0,0))
        go_player.add_component(SpriteRenderer("player_ship.png"))
        go_player.add_component(Player())
        
        
        
        self._gameObjects.append(go_southship)
        self._gameObjects.append(go_northship)
        self._gameObjects.append(go_player)
        self._gameObjects.append(go_mothership)
        self._gameObjects.append(go_turret_one)
        self._gameObjects.append(go_turret_two)
        self._gameObjects.append(go_turret_three)
        self._gameObjects.append(go_turret_four)


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

    def makeTurret(self, string):
        turret = GameObject(pygame.math.Vector2(0,0))
        turret.add_component(SpriteRenderer(string))
        turret.add_component(Turret())
        return turret   
    
    
class loosOrVicState(State):
    def __init__(self, game_world) -> None:
        super().__init__(game_world)             
        self._dis = pygame.display.set_mode((1280, 720))
        
        #uses the system font
        self._text_font = pygame.font.SysFont(None, 30, bold = False)
        self._text_font_sel = pygame.font.SysFont(None, 30, bold = True)
        self._text_font_write_name = pygame.font.SysFont(None, 50, bold = False)
        self._player_name = ""
        self._writen_name = False
        self._read_Json = False
        self._sorting = None
        
        self._score_holder = SavingScore
        self._menu_sele = 0
    
    def draw_text(self,text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self._dis.blit(img,(x,y))

    def write_player_name(self):
        self.draw_text("Your score:", self._text_font, (0,0,0), 500, 20)
        self.draw_text(f"{self._game_world.Score}", self._text_font_sel, (0,0,0), 650, 20)
        self.draw_text("Write your desired name", self._text_font, (0,0,0), 500, 50)
        self.draw_text(f"{self._player_name}", self._text_font_write_name, (0,0,0), 500, 150)
        self.draw_text("Press enter when you're happy with your name", self._text_font, (0,0,0), 450, 250)
        
    def drawing_endscreen(self):
        self.draw_text("Score:", self._text_font, (0,0,0), 575, 20)
        #displaing the player score
        self.draw_text(f"{self._game_world.Score}", self._text_font_sel, (0,0,0), 650, 20)
        self.draw_text("Name     Score", self._text_font, (0,0,0), 575, 65)
        self.draw_text("Restart", self._text_font, (0,0,0), 500, 500)        
        self.draw_text("Main Menu", self._text_font, (0,0,0), 700, 500)        
        match self._menu_sele:
            case -1:#Restart the game
                self.draw_text("Restart", self._text_font_sel, (0,0,0), 500, 500)        
            case 2:#Head to main menu
                self.draw_text("Main Menu", self._text_font_sel, (0,0,0), 700, 500)        
                
        y = 100 #Initial y-coordinate for drawing
        if self._read_Json == False:
            # Get the player data and sort based on scores
            self._sorting = sorted(self._score_holder.print_score().items(), key=lambda x: int(x[1]["score"]), reverse=True)
            self._read_Json = True
        i = 0
        for name, player_data in self._sorting:
            if i >= 10:
                break
            score = player_data["score"]
                
            self.draw_text(f"{name}", self._text_font, (0,0,0), 580, y)
            self.draw_text(f"{score}", self._text_font, (0,0,0), 670, y)
            y += 35
            i +=1

    def handle_input(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if self._writen_name  == True: #only when the player has written their name
                        if event.key == pygame.K_LEFT:
                            self._menu_sele = -1
                        elif event.key == pygame.K_RIGHT:
                            self._menu_sele = 2
                        if event.key == pygame.K_SPACE:
                            match self._menu_sele:
                                case -1:#Restart the game
                                    restart = FirstLevelState(self._game_world)
                                    self._game_world.ChangeToNewState(restart)
                                case 2:#Head to main menu
                                    main_menu = MenuState(self._game_world)
                                    self._game_world.ChangeToNewState(main_menu)
                    else:
                        if event.key == pygame.K_RETURN:
                            self._score_holder.give_score(f"{self._player_name}", f"{self._game_world.Score}")
                            self._writen_name = True
                        elif event.key == pygame.K_BACKSPACE:
                            self._player_name = self._player_name[:-1]
                        else:
                            self._player_name += event.unicode               
            
        
        
    def awake(self, game_world):
        super().awake(game_world)
        
        #Testing score -TB
        #self._score_holder.give_score("TB","500")
        #self._score_holder.give_score("JK","700")
        
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self._game_world)   
            
            
            
    def start(self):
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gameObject in self._gameObjects[:]:
            gameObject.start()
            
    def update(self, delta_time):
        # fill the screen with a color to wipe away anything from last frame
        self._game_world.screen.fill("lightcoral")
        if self._writen_name == False:
            self.write_player_name()
        else:
            self.drawing_endscreen()
        self.handle_input()
        
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)
