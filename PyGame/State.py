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
        #not selected
        self._text_font = pygame.font.Font("Assets\\Font\\ARCADE_R.TTF", 30)
        #Selected
        self._text_font_sel = pygame.font.Font("Assets\\Font\\ARCADE_I.TTF", 30)
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
                    self.draw_text("Music", self._text_font_sel, (0,0,0), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font_sel, (0, 0,0), 700, 360)
                    self.draw_text("SFX", self._text_font, (0,0,0), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (0,0,0), 700, 410)
                    self.draw_text("Graphics", self._text_font, (0,0,0), 500, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (0,0,0), 750, 460)
                case 1:
                    self.draw_text("Music", self._text_font, (0,0,0), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (0,0,0), 700, 360)
                    self.draw_text("SFX", self._text_font_sel, (0,0,0), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font_sel, (0,0,0), 700, 410)
                    self.draw_text("Graphics", self._text_font, (0,0,0), 500, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (0,0,0), 750, 460)
                case 2:
                    self.draw_text("Music", self._text_font, (0,0,0), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (0,0,0), 700, 360)
                    self.draw_text("SFX", self._text_font, (0,0,0), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (0,0,0), 700, 410)
                    self.draw_text("Graphics", self._text_font_sel, (0,0,0), 500, 460)    
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font_sel, (0,0,0), 750, 460)

class FirstLevelState(State):

    def __init__(self, game_world) -> None:
        super().__init__(game_world)
        self._player_score = 0
        
        self._background_image_path ="SimpleBackgroundClear.png"
        self._scroll_speed = 50
        self._background_go = GameObject(position=(0, 0))
        self._background_go.add_component(Background(game_world, image_path=self._background_image_path, scroll_speed=self._scroll_speed))

        self._middle_ground_image_path = "GravelTransEkstra.png"
        self._middle_ground_scroll_speed = 150
        self._middle_ground_go = GameObject(position=(0, 0))
        self._middle_ground_go.add_component(Background(game_world, image_path=self._middle_ground_image_path, scroll_speed=self._middle_ground_scroll_speed))

        self._fore_ground_image_path = "SandTransNeutral.png"
        self._fore_ground_scroll_speed = 100
        self._fore_ground_go = GameObject(position=(0, 0))
        self._fore_ground_go.add_component(Background(game_world, image_path=self._fore_ground_image_path, scroll_speed=self._fore_ground_scroll_speed))

        self._effect_ground_image_path = "DustClear.png"
        self._effect_ground_scroll_speed = 2500
        self._effect_ground_go = GameObject(position=(0, 0))
        self._effect_ground_go.add_component(Background(game_world, image_path=self._effect_ground_image_path, scroll_speed=self._effect_ground_scroll_speed))


        # background_music = mixer
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

    def move_to_endscreen(self):
        self._game_world.score = self._player_score
        self._game_world.ChangeToNewState(loosOrVicState(self._game_world))
    

    def update(self, delta_time):
        # fill the screen with a color to wipe away anything from last frame
        self._game_world.screen.fill("lightcoral")

        self._background_go.update(delta_time)
        
        self._fore_ground_go.update(delta_time)
        self._middle_ground_go.update(delta_time)
        self._effect_ground_go.update(delta_time)
        
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)

        self._gameObjects = [obj for obj in self._gameObjects if not obj._is_destroyed]

    def makeTurret(self, string):
        turret = GameObject(pygame.math.Vector2(0,0))
        turret.add_component(SpriteRenderer(string))
        turret.add_component(Turret())
        return turret   
    



    
class SecondLevelState(State):  

    def __init__(self, game_world) -> None:
        super().__init__(game_world)
        
        self._backgroundV2_image_path ="BackgroundV3.0.png"
        self._scroll_speed = 50
        self._backgroundV2_go = GameObject(position=(0, 0))
        self._backgroundV2_go.add_component(Background(game_world, image_path=self._backgroundV2_image_path, scroll_speed=self._scroll_speed))

        self._middle_groundV2_image_path = "MiddlegroundCloudsV3.0.png"
        self._middle_groundV2_scroll_speed = 150
        self._middle_groundV2_go = GameObject(position=(0, 0))
        self._middle_groundV2_go.add_component(Background(game_world, image_path=self._middle_groundV2_image_path, scroll_speed=self._middle_groundV2_scroll_speed))

        self._fore_groundV2_image_path = "ForegroundCloudsV3.0.png"
        self._fore_groundV2_scroll_speed = 100
        self._fore_groundV2_go = GameObject(position=(0, 0))
        self._fore_groundV2_go.add_component(Background(game_world, image_path=self._fore_groundV2_image_path, scroll_speed=self._fore_groundV2_scroll_speed))

        self._effect_groundV2_image_path = "DustClear.png"
        self._effect_groundV2_scroll_speed = 2500
        self._effect_groundV2_go = GameObject(position=(0, 0))
        self._effect_groundV2_go.add_component(Background(game_world, image_path=self._effect_groundV2_image_path, scroll_speed=self._effect_groundV2_scroll_speed))


        # background_music = mixer
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

        self._backgroundV2_go.update(delta_time)
        
        self._fore_groundV2_go.update(delta_time)
        self._middle_groundV2_go.update(delta_time)
        self._effect_groundV2_go.update(delta_time)

        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)

        self._gameObjects = [obj for obj in self._gameObjects if not obj._is_destroyed]

    def makeTurret(self, string):
        turret = GameObject(pygame.math.Vector2(0,0))
        turret.add_component(SpriteRenderer(string))
        turret.add_component(Turret())
        return turret   

        


class ThirdLevelState(State): #Boss level

    def __init__(self, game_world) -> None:
        super().__init__(game_world)
        
        self._backgroundv3_image_path ="BackgroundV4.1.png"
        self._scroll_speed = 50
        self._backgroundv3_go = GameObject(position=(0, 0))
        self._backgroundv3_go.add_component(Background(game_world, image_path=self._backgroundv3_image_path, scroll_speed=self._scroll_speed))

        self._middle_groundV3_image_path = "SandBlackDensest.png"
        self._middle_groundV3_scroll_speed = 150
        self._middle_groundV3_go = GameObject(position=(0, 0))
        self._middle_groundV3_go.add_component(Background(game_world, image_path=self._middle_groundV3_image_path, scroll_speed=self._middle_groundV3_scroll_speed))

        self._fore_groundV3_image_path = "ForegroundBlackCloudDense.png"
        self._fore_groundV3_scroll_speed = 100
        self._fore_groundV3_go = GameObject(position=(0, 0))
        self._fore_groundV3_go.add_component(Background(game_world, image_path=self._fore_groundV3_image_path, scroll_speed=self._fore_groundV3_scroll_speed))


        self._effect_groundv3_image_path = "DustBlack.png"
        self._effect_groundv3_scroll_speed = 2500
        self._effect_groundv3_go = GameObject(position=(0, 0))
        self._effect_groundv3_go.add_component(Background(game_world, image_path=self._effect_groundv3_image_path, scroll_speed=self._effect_groundv3_scroll_speed))


        # background_music = mixer
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

        self._backgroundv3_go.update(delta_time)
        
        self._fore_groundV3_go.update(delta_time)
        self._middle_groundV3_go.update(delta_time)
        self._effect_groundv3_go.update(delta_time)

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
        
                #not selected
        self._text_font = pygame.font.Font("Assets\\Font\\ARCADE_R.TTF", 30)
        #Selected
        self._text_font_sel = pygame.font.Font("Assets\\Font\\ARCADE_I.TTF", 30)

        self._text_font_write_name = pygame.font.Font("Assets\\Font\\ARCADE_N.TTF", 30)
        self._player_name = ""
        self._writen_name = False
        self._read_Json = False
        self._sorting = None
        
        self._score_holder = SavingScore
        self._menu_sele = 0
    
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self._dis.blit(img,(x,y))

    def write_player_name(self):
        self.draw_text("Your score:", self._text_font, (0,0,0), 300, 30)
        self.draw_text(f"{self._game_world.Score}", self._text_font, (0,0,0), 650, 30)
        self.draw_text("Write your desired name", self._text_font, (0,0,0), 300, 80)
        self.draw_text(f"{self._player_name}", self._text_font_write_name, (0,0,0), 350, 180)
        self.draw_text("Press       to continue", self._text_font, (0,0,0), 300, 280)
        self.draw_text("      enter            ", self._text_font_sel, (139,0,139), 300, 280)
        
    def drawing_endscreen(self):
        self.draw_text("Score:", self._text_font, (0,0,0), 500, 20)
        #displaying the player score
        self.draw_text(f"{self._game_world.Score}", self._text_font, (0,0,0), 700, 20)
        self.draw_text("Name:        Score:", self._text_font, (0,0,0), 400, 65)
        if self._menu_sele == 0:
            self.draw_text("Restart", self._text_font, (0,0,0), 300, 600)        
            self.draw_text("Main Menu", self._text_font, (0,0,0), 700, 600)        
        match self._menu_sele:
            case -1:#Restart the game
                self.draw_text("Restart", self._text_font_sel, (0,0,0), 300, 600)        
                self.draw_text("Main Menu", self._text_font, (0,0,0), 700, 600)        
            case 2:#Head to main menu
                self.draw_text("Main Menu", self._text_font_sel, (0,0,0), 700, 600)        
                self.draw_text("Restart", self._text_font, (0,0,0), 300, 600)        
                
        y = 125 #Initial y-coordinate for drawing
        if self._read_Json == False:
            # Get the player data and sort based on scores
            self._sorting = sorted(self._score_holder.print_score().items(), key=lambda x: int(x[1]["score"]), reverse=True)
            self._read_Json = True
        i = 0
        for name, player_data in self._sorting:
            if i >= 8:
                break
            score = player_data["score"]
                
            self.draw_text(f"{name}", self._text_font, (0,0,0), 400, y)
            self.draw_text(f"{score}", self._text_font, (0,0,0), 825, y)
            y += 50
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
