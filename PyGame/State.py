from abc import ABC, abstractmethod
import pygame
import sys
from Player import Player
from Player import Thruster
from MotherShip import MotherShip
from MotherShip import MShipPart
from MotherShip import Turret
from Boss import Boss
from GameObject import GameObject
from Components import SpriteRenderer
from Components import Animator
from Components import Laser
from Components import Collider
import pygame.locals
import threading
from pygame import mixer
from Background import Background
from MenuBackground import MenuBackground
from SavingScoreJson import SavingScore
#from Enemy import EnemySpawner
from Enemy import Enemy




class State(ABC):

    def __init__(self, game_world) -> None:
        super().__init__()
        self._gameObjects = []
        self._colliders = []
        self._game_world = game_world

    @property
    def colliders(self):
        return self._colliders

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
        self._background_image_path ="MenuBackground.png"
        self._background_go = GameObject(position=(0, 0))
        self._background_go.add_component(MenuBackground(game_world, image_path=self._background_image_path))
        self._menu_sound = mixer.Sound("Assets\\Audio\\click.wav")
        self._started_on_level = False
        #not selected
        self._text_font = pygame.font.Font("Assets\\Font\\ARCADE_R.TTF", 30)
        #Selected
        self._text_font_sel = pygame.font.Font("Assets\\Font\\ARCADE_I.TTF", 30)
        
        self._menu_sele = 0
        self._graphics_opt = 1      
        self._opt_menu_sel = 1 #0 for down, 1 for mid, 2 for up
        self._options_sele = False  


        
    def hande_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self._options_sele == False:
                        self._menu_sound.play()
                        self._menu_sound.set_volume(self._game_world.SFX_volume/1000)
                        self.do_menu_input()
                    elif self._options_sele == True:
                        self._options_sele = False
                elif event.key == pygame.K_UP:
                    self._menu_sele -= 1
                    self._menu_sound.play()
                    self._menu_sound.set_volume(self._game_world.SFX_volume/1000)
                elif event.key == pygame.K_DOWN:
                    self._menu_sele += 1
                    self._menu_sound.play()
                    self._menu_sound.set_volume(self._game_world.SFX_volume/1000)
                if self._options_sele == True:
                    if event.key == pygame.K_LEFT:
                        self._menu_sound.play()
                        self.do_options_input(-1)
                        self._menu_sound.set_volume(self._game_world.SFX_volume/1000)
                    elif event.key == pygame.K_RIGHT:
                        self._menu_sound.play()
                        self.do_options_input(1)
                        self._menu_sound.set_volume(self._game_world.SFX_volume/1000)


        # Clamp menu selection within range
        self._menu_sele = max(0, min(3, self._menu_sele))
        
    def do_menu_input(self):
        match self._menu_sele:
            case 0:#new game
                self._game_world.start_game  = True
                level = FirstLevelState(self._game_world)
                self._game_world.ChangeToNewState(level)
            case 1:
                if self._game_world.start_game == True:
                    self._game_world.ChangeState(FirstLevelState(self._game_world))
            case 2:#Options
                self._options_sele = True
            case 3:
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
        self._game_world.screen.blit(img,(x,y))

    def awake(self, game_world):
        super().awake(game_world)
        
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self._game_world)     

    def start(self):
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self, delta_time):        
        #drawing the game
        self._background_go.update(delta_time)

        self.drawing_menu()
        self.hande_input()


        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)
        
    def drawing_menu(self):
        #self.draw_text(f"{self._menu_sele}", self._text_font_sel, (0,0,0), 1000, 0)
        #self.draw_text(f"{self._opt_menu_sel}", self._text_font_sel, (0,0,0), 1000, 50)
        if self._options_sele == False:
            match self._menu_sele:
                case 0:
                    self.draw_text("New Game", self._text_font_sel, (0,0,0), 600, 360)
                    self.draw_text("  Continue", self._text_font, (0,0,0), 600, 410)
                    self.draw_text("    Option", self._text_font, (0,0,0), 600, 460)
                    self.draw_text("      Quit", self._text_font, (0,0,0), 600, 510)
                case 1:
                    self.draw_text("New Game", self._text_font, (0,0,0), 600, 360)
                    self.draw_text("  Continue", self._text_font_sel, (0,0,0), 600, 410)
                    self.draw_text("    Option", self._text_font, (0,0,0), 600, 460)
                    self.draw_text("      Quit", self._text_font, (0,0,0), 600, 510)
                case 2:
                    self.draw_text("New Game", self._text_font, (0,0,0), 600, 360)
                    self.draw_text("  Continue", self._text_font, (0,0,0), 600, 410)
                    self.draw_text("    Option", self._text_font_sel, (0,0,0), 600, 460)
                    self.draw_text("      Quit", self._text_font, (0,0,0), 600, 510)
                case 3:
                    self.draw_text("New Game", self._text_font, (0,0,0), 600, 360)
                    self.draw_text("  Continue", self._text_font, (0,0,0), 600, 410)
                    self.draw_text("    Option", self._text_font, (0,0,0), 600, 460)
                    self.draw_text("      Quit", self._text_font_sel, (0,0,0), 600, 510)
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
        self.clock = pygame.time.Clock()


        self._player_score = 0
        self._menu_sele = 0
        self._options_sele = False  
        self._opt_menu_sel = 1 #0 for down, 1 for mid, 2 for up
        self._graphics_opt = 1      
        #So its reset from the start
        self._game_world.STT_ammo = "||||"
        
        #not selected
        self._text_font = pygame.font.Font("Assets\\Font\\ARCADE_R.TTF", 25)
        #Selected
        self._text_font_sel = pygame.font.Font("Assets\\Font\\ARCADE_I.TTF", 25)
        
        self._background_image_path ="SimpleBackgroundClear.png"
        self._scroll_speed = 50
        self._background_go = GameObject(position=(0, 0))
        self._background_go.add_component(Background(game_world, image_path=self._background_image_path, scroll_speed=self._scroll_speed))

        self._middle_ground_image_path = "GravelTransEkstra.png"
        self._middle_ground_scroll_speed = 130
        self._middle_ground_go = GameObject(position=(0, 0))
        self._middle_ground_go.add_component(Background(game_world, image_path=self._middle_ground_image_path, scroll_speed=self._middle_ground_scroll_speed))

        self._fore_ground_image_path = "SandTransNeutral.png"
        self._fore_ground_scroll_speed = 100
        self._fore_ground_go = GameObject(position=(0, 0))
        self._fore_ground_go.add_component(Background(game_world, image_path=self._fore_ground_image_path, scroll_speed=self._fore_ground_scroll_speed))

        self._effect_ground_image_path = "DustClear.png"
        self._effect_ground_scroll_speed = 250
        self._effect_ground_go = GameObject(position=(0, 0))
        self._effect_ground_go.add_component(Background(game_world, image_path=self._effect_ground_image_path, scroll_speed=self._effect_ground_scroll_speed))

        self.enemy_delay = 5 #Sekunder mellem enemies
        self.enemy_timer = 0

        # background_music = mixer
        self._music = mixer.music.load("Assets\\Audio\\Background.mp3")

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
        
        go_thruster = GameObject(pygame.math.Vector2(0,0))
        go_thruster.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png"))
        go_thruster.add_component(Thruster())
        thrust_anim = go_thruster.add_component(Animator())
        
        thrust_anim.add_animation("Dead", -90, "space_breaker_asset\\Ships\\Small\\Exhaust\\Dead.png",
                                  )
        thrust_anim.add_animation("Top", -135, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01d.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01f.png",)
        thrust_anim.add_animation("Bottom", -45, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01d.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01f.png",)
        thrust_anim.play_animation("Dead")

        go_thruster_main = GameObject(pygame.math.Vector2(0,0))
        go_thruster_main.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png"))
        go_thruster_main.add_component(Thruster())
        thrust_main_anim = go_thruster_main.add_component(Animator())
        thrust_main_anim.add_animation("Mid", -90, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01b.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",)
        thrust_main_anim.play_animation("Mid")

        go_player = GameObject(pygame.math.Vector2(0,0))
        go_player.add_component(SpriteRenderer("player_ship.png"))
        go_player.add_component(Player())
        go_player.get_component("Player").add_thruster(go_thruster, go_thruster_main)
        

        
        self._gameObjects.append(go_southship)
        self._gameObjects.append(go_northship)
        self._gameObjects.append(go_thruster)
        self._gameObjects.append(go_thruster_main)
        self._gameObjects.append(go_player)
        self._gameObjects.append(go_mothership)
        self._gameObjects.append(go_turret_one)
        self._gameObjects.append(go_turret_two)
        self._gameObjects.append(go_turret_three)
        self._gameObjects.append(go_turret_four)
        
    def draw_text(self,text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self._game_world.screen.blit(img,(x,y))

    def spawn_enemy(self):
        go_enemy = GameObject(pygame.math.Vector2(0,0))
        go_enemy.add_component(SpriteRenderer("Spaceships\\Enemy_ship_01.png"))
        go_enemy.add_component(Enemy())
        go_enemy.add_component(Collider())

        self.instantiate(go_enemy)

    def instantiate(self, gameObject):
        gameObject.awake(self._game_world)
        gameObject.start()
        self._gameObjects.append(gameObject)

    def awake(self, game_world):
        super().awake(game_world)
        self._music = mixer.music.play(-1)
        self._music= mixer.music.set_volume(self._game_world.music_volume/1000)
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self._game_world)        

    def start(self):
        self.drawen_start_level = False
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def move_to_endscreen(self, Win):#Win is bool
        self._music = mixer.music.pause()
        self._game_world.score = self._player_score
        self._game_world.ChangeToNewState(loosOrVicState(self._game_world, Win))

    def drawing_UI(self):
        self.draw_text(f"Ammo: {self._game_world.STT_ammo}",self._text_font,(255, 255, 255), 50, 25)
        self.draw_text(f"Score: {self._player_score}",self._text_font,(255, 255, 255), 500, 25)
        self.draw_text(f"Lives",self._text_font,(255, 255, 255), 950, 25)
        
        self.draw_text(f"{self._menu_sele}", self._text_font_sel,(255, 255, 255), 400, 100)
        
        if self._game_world.worldPause == True and self._options_sele == False:
            match self._menu_sele:
                case 0: #back but
                    self.draw_text("Back", self._text_font_sel,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font,(255, 255, 255), 500, 460)
                case 1: #Options but
                    self.draw_text("Back",self._text_font,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font_sel,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font,(255, 255, 255), 500, 460)
                case 2: #Menu but
                    self.draw_text("Back",self._text_font,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font_sel,(255, 255, 255), 500, 460)
        elif self._game_world.worldPause == True and self._options_sele == True:
            match self._menu_sele:
                case 0:
                    self.draw_text("Music", self._text_font_sel, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font_sel, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font, (255, 255, 255), 500, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (255, 255, 255), 750, 460)
                case 1:
                    self.draw_text("Music", self._text_font, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font_sel, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font_sel, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font, (255, 255, 255), 500, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (255, 255, 255), 750, 460)
                case 2:
                    self.draw_text("Music", self._text_font, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font_sel, (255, 255, 255), 500, 460)    
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font_sel, (255, 255, 255), 750, 460)

    def update(self, delta_time):
        #Game not paused
        self.enemy_timer +=delta_time
        

        self._background_go.update(delta_time)
        self._fore_ground_go.update(delta_time)
        self._middle_ground_go.update(delta_time)
        
        self.fps_counter(self.clock, self._game_world.screen)
        delta_time = self.clock.tick(60) / 1000.0 # limits FPS to 60
            
        if self._game_world.worldPause == False:
            #Makes a copy om _gameObjects and runs through that instead of the orginal
            for gamObjects in self._gameObjects[:]:
                gamObjects.update(delta_time)

            for i, collider1 in enumerate(self._colliders):
                for j in range(i + 1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    collider1.collision_check(collider2)
            self._colliders = [obj for obj in self._colliders if not obj.gameObject._is_destroyed]
            self._gameObjects = [obj for obj in self._gameObjects if not obj._is_destroyed]
            
        
        # self._effect_ground_go.update(delta_time)
        
        if self.enemy_timer >= self.enemy_delay:
            #self.spawn_enemy()
            self.enemy_timer = 0 #resets cooldown after shoot()

        if self.drawen_start_level == False:
            if self.enemy_timer <= 2:
                self.draw_text("First level started",self._text_font,(255, 255, 255), 750, 450)
            if self.enemy_timer >= 2:
                self.drawen_start_level = True
                
        self.drawing_UI()
        self.handle_input()
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self._game_world.worldPause == False:
                    self._game_world.worldPause = True
                    #self.pause_game()
                elif self._game_world.worldPause == True and event.key == pygame.K_p:
                    self._game_world.worldPause = False
                    self._options_sele = False
                elif event.key == pygame.K_COMMA:
                    self._game_world.score = self._player_score
                    self._game_world.ChangeToNewState(SecondLevelState(self._game_world))
    
                if self._game_world.worldPause == True:
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
                            #self._menu_sound.play()
                            self.do_options_input(-1)
                        elif event.key == pygame.K_RIGHT:
                            #self._menu_sound.play()
                            self.do_options_input(1)
                self._menu_sele = max(0, min(2, self._menu_sele))
                
    def do_menu_input(self):
        match self._menu_sele:
            case 0:#new game
                self._game_world.worldPause = False
            case 1:#Options
                    self._options_sele = True
            case 2:# back to menu
                self._options_sele == False
                self._game_world.worldPause = False
                self._music = mixer.music.pause()   
                level = MenuState(self._game_world)
                self._game_world.ChangeToNewState(level)
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
                self._music= mixer.music.set_volume(self._game_world.music_volume/1000)
            case 1: #sfx Volumen
                if self._opt_menu_sel == 2:
                    self._game_world.SFX_volume += 10     
                    if self._game_world.SFX_volume > 100:
                        self._game_world.SFX_volume = 100     
                elif self._opt_menu_sel == 0:
                    self._game_world.SFX_volume -= 10     
                    if self._game_world.SFX_volume < 0:
                        self._game_world.SFX_volume = 0     
                self._music= mixer.music.set_volume(self._game_world.SFX_volume/1000)
            case 2:#Grapchis options
                self._graphics_opt = self.tmp
        #Resets the pos to 1
        self._opt_menu_sel = 1
    
    def makeTurret(self, string):
        turret = GameObject(pygame.math.Vector2(0,0))
        turret.add_component(SpriteRenderer(string))
        turret.add_component(Turret())
        return turret 
    
    def fps_counter(self, clock, screen):
        BLACK = (255, 255, 255)
        WHITE= (0, 0, 0)
        fps = int(clock.get_fps())
        fps_text = f"FPS: {fps}"
        font = pygame.font.SysFont("Verdana", 15)
        text_surface = font.render(fps_text, True, BLACK)
        screen.blit(text_surface,(10, 10))  
    

    
class SecondLevelState(State):  

    def __init__(self, game_world) -> None:
        super().__init__(game_world)
        self.clock = pygame.time.Clock()

        self._player_score = 0
        self._menu_sele = 0
        self._options_sele = False  
        self._opt_menu_sel = 1 #0 for down, 1 for mid, 2 for up
        self._graphics_opt = 1      
        #So its reset from the start
        self._game_world.STT_ammo = "||||"
        
        #not selected
        self._text_font = pygame.font.Font("Assets\\Font\\ARCADE_R.TTF", 25)
        #Selected
        self._text_font_sel = pygame.font.Font("Assets\\Font\\ARCADE_I.TTF", 25)
        
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
        
        self.enemy_delay = 4 #Sekunder mellem enemies
        self.enemy_timer = 0

        # background_music = mixer
        mixer.music.load("Assets\\Audio\\Background.mp3")

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
        
        go_thruster = GameObject(pygame.math.Vector2(0,0))
        go_thruster.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png"))
        go_thruster.add_component(Thruster())
        thrust_anim = go_thruster.add_component(Animator())
        
        thrust_anim.add_animation("Dead", -90, "space_breaker_asset\\Ships\\Small\\Exhaust\\Dead.png",
                                  )
        thrust_anim.add_animation("Top", -135, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01d.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01f.png",)
        thrust_anim.add_animation("Bottom", -45, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01d.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01f.png",)
        thrust_anim.play_animation("Dead")

        go_thruster_main = GameObject(pygame.math.Vector2(0,0))
        go_thruster_main.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png"))
        go_thruster_main.add_component(Thruster())
        thrust_main_anim = go_thruster_main.add_component(Animator())
        thrust_main_anim.add_animation("Mid", -90, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01b.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",)
        thrust_main_anim.play_animation("Mid")

        go_player = GameObject(pygame.math.Vector2(0,0))
        go_player.add_component(SpriteRenderer("player_ship.png"))
        go_player.add_component(Player())
        go_player.get_component("Player").add_thruster(go_thruster, go_thruster_main)
        
        
        
        
        self._gameObjects.append(go_southship)
        self._gameObjects.append(go_northship)
        self._gameObjects.append(go_thruster)
        self._gameObjects.append(go_thruster_main)
        self._gameObjects.append(go_player)
        self._gameObjects.append(go_mothership)
        self._gameObjects.append(go_turret_one)
        self._gameObjects.append(go_turret_two)
        self._gameObjects.append(go_turret_three)
        self._gameObjects.append(go_turret_four)
    
    def draw_text(self,text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self._game_world.screen.blit(img,(x,y))
        
    def spawn_enemy(self):
        go_enemy = GameObject(pygame.math.Vector2(0,0))
        go_enemy.add_component(SpriteRenderer("Spaceships\\Enemy_ship_01.png"))
        go_enemy.add_component(Enemy())
        go_enemy.add_component(Collider())

        self.instantiate(go_enemy)


    def instantiate(self, gameObject):
        gameObject.awake(self._game_world)
        gameObject.start()
        self._gameObjects.append(gameObject)

    def awake(self, game_world):
        super().awake(game_world)
        self.drawen_start_level = False
        self._music = mixer.music.play(-1)
        self._music= mixer.music.set_volume(self._game_world.music_volume/1000)        
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self._game_world)        

    def start(self):
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def move_to_endscreen(self, Win):#Win is bool
        self._music = mixer.music.pause()
        self._game_world.score = self._player_score
        self._game_world.ChangeToNewState(loosOrVicState(self._game_world, Win))
    
    def drawing_UI(self):
        self.draw_text(f"Ammo: {self._game_world.STT_ammo}",self._text_font,(255, 255, 255), 50, 25)
        self.draw_text(f"Score: {self._player_score}",self._text_font,(255, 255, 255), 500, 25)
        self.draw_text(f"Lives",self._text_font,(255, 255, 255), 950, 25)
        
        self.draw_text(f"{self._menu_sele}", self._text_font_sel,(255, 255, 255), 400, 100)
        
        if self._game_world.worldPause == True and self._options_sele == False:
            match self._menu_sele:
                case 0: #back but
                    self.draw_text("Back", self._text_font_sel,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font,(255, 255, 255), 500, 460)
                case 1: #Options but
                    self.draw_text("Back",self._text_font,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font_sel,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font,(255, 255, 255), 500, 460)
                case 2: #Menu but
                    self.draw_text("Back",self._text_font,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font_sel,(255, 255, 255), 500, 460)
        elif self._game_world.worldPause == True and self._options_sele == True:
            match self._menu_sele:
                case 0:
                    self.draw_text("Music", self._text_font_sel, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font_sel, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font, (255, 255, 255), 500, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (255, 255, 255), 750, 460)
                case 1:
                    self.draw_text("Music", self._text_font, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font_sel, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font_sel, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font, (255, 255, 255), 500, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (255, 255, 255), 750, 460)
                case 2:
                    self.draw_text("Music", self._text_font, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font_sel, (255, 255, 255), 500, 460)    
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font_sel, (255, 255, 255), 750, 460)

    def update(self, delta_time):
        # fill the screen with a color to wipe away anything from last frame
        self.enemy_timer +=delta_time

        self._backgroundV2_go.update(delta_time)
        self._middle_groundV2_go.update(delta_time)
        

        self.fps_counter(self.clock, self._game_world.screen)
        delta_time = self.clock.tick(60) / 1000.0 # limits FPS to 60
        
        if self._game_world.worldPause == False:
            #Makes a copy om _gameObjects and runs through that instead of the orginal
            for gamObjects in self._gameObjects[:]:
                gamObjects.update(delta_time)

            for i, collider1 in enumerate(self._colliders):
                for j in range(i + 1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    collider1.collision_check(collider2)
            self._gameObjects = [obj for obj in self._gameObjects if not obj._is_destroyed]
        self._fore_groundV2_go.update(delta_time)  
        self._effect_groundV2_go.update(delta_time)
        
        if self.enemy_timer >= self.enemy_delay:
            self.spawn_enemy()
            self.enemy_timer = 0 #resets cooldown after shoot()

        if self.drawen_start_level == False:
            if self.enemy_timer <= 2:
                self.draw_text("Second level started",self._text_font,(255, 255, 255), 750, 450)
            if self.enemy_timer >= 2:
                self.drawen_start_level = True
        
        self.drawing_UI()
        self.handle_input()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self._game_world.worldPause == False:
                    self._game_world.worldPause = True
                    #self.pause_game()
                elif self._game_world.worldPause == True and event.key == pygame.K_p:
                    self._game_world.worldPause = False
                    self._options_sele = False
                elif event.key == pygame.K_COMMA:
                    self._game_world.score = self._player_score
                    self._game_world.ChangeToNewState(ThirdLevelState(self._game_world))
                if self._game_world.worldPause == True:
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
                            #self._menu_sound.play()
                            self.do_options_input(-1)
                            #self._menu_sound.set_volume(self._game_world.SFX_volume/1000)
                        elif event.key == pygame.K_RIGHT:
                            #self._menu_sound.play()
                            self.do_options_input(1)
                            #self._menu_sound.set_volume(self._game_world.SFX_volume/1000)
                self._menu_sele = max(0, min(2, self._menu_sele))
                        
    def do_menu_input(self):
        match self._menu_sele:
            case 0:#new game
                self._game_world.worldPause = False
            case 1:#Options
                    self._options_sele = True
            case 2:# back to menu
                self._options_sele == False
                self._game_world.worldPause = False
                self._music = mixer.music.pause()   
                level = MenuState(self._game_world)
                self._game_world.ChangeToNewState(level)
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
                self._music= mixer.music.set_volume(self._game_world.music_volume/1000)
            case 1: #sfx Volumen
                if self._opt_menu_sel == 2:
                    self._game_world.SFX_volume += 10     
                    if self._game_world.SFX_volume > 100:
                        self._game_world.SFX_volume = 100     
                elif self._opt_menu_sel == 0:
                    self._game_world.SFX_volume -= 10     
                    if self._game_world.SFX_volume < 0:
                        self._game_world.SFX_volume = 0     
                self._music= mixer.music.set_volume(self._game_world.SFX_Volume/1000)
            case 2:#Grapchis options
                self._graphics_opt = self.tmp
        #Resets the pos to 1
        self._opt_menu_sel = 1
        
    def makeTurret(self, string):
        turret = GameObject(pygame.math.Vector2(0,0))
        turret.add_component(SpriteRenderer(string))
        turret.add_component(Turret())
        return turret   
    
    def fps_counter(self, clock, screen):
        BLACK = (255, 255, 255)
        WHITE= (0, 0, 0)
        fps = int(clock.get_fps())
        fps_text = f"FPS: {fps}"
        font = pygame.font.SysFont("Verdana", 15)
        text_surface = font.render(fps_text, True, BLACK)
        screen.blit(text_surface,(10, 10))

        


class ThirdLevelState(State): #Boss level

    def __init__(self, game_world) -> None:
        super().__init__(game_world)
        self.clock = pygame.time.Clock()

        self._player_score = 0
        self._menu_sele = 0
        self._options_sele = False  
        self._opt_menu_sel = 1 #0 for down, 1 for mid, 2 for up
        self._graphics_opt = 1      
        #So its reset from the start
        self._game_world.STT_ammo = "||||"
        
        self.should_boss_spawn = True
        
        #not selected
        self._text_font = pygame.font.Font("Assets\\Font\\ARCADE_R.TTF", 25)
        #Selected
        self._text_font_sel = pygame.font.Font("Assets\\Font\\ARCADE_I.TTF", 25)

        self._backgroundv3_image_path ="BackgroundV4.4.png"
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
        
        self.enemy_delay = 3 #Sekunder mellem enemies
        self.enemy_timer = 0    

        # background_music = mixer
        mixer.music.load("Assets\\Audio\\Background.mp3")


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
        
        go_thruster = GameObject(pygame.math.Vector2(0,0))
        go_thruster.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png"))
        go_thruster.add_component(Thruster())
        thrust_anim = go_thruster.add_component(Animator())
        
        thrust_anim.add_animation("Dead", -90, "space_breaker_asset\\Ships\\Small\\Exhaust\\Dead.png",
                                  )
        thrust_anim.add_animation("Top", -135, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01d.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01f.png",)
        thrust_anim.add_animation("Bottom", -45, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01d.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01f.png",)
        thrust_anim.play_animation("Dead")

        go_thruster_main = GameObject(pygame.math.Vector2(0,0))
        go_thruster_main.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png"))
        go_thruster_main.add_component(Thruster())
        thrust_main_anim = go_thruster_main.add_component(Animator())
        thrust_main_anim.add_animation("Mid", -90, "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01a.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01b.png",
                                  "space_breaker_asset\\Ships\\Small\\Exhaust\\exhaust_01c.png",)
        thrust_main_anim.play_animation("Mid")

        go_player = GameObject(pygame.math.Vector2(0,0))
        go_player.add_component(SpriteRenderer("space_breaker_asset\\Ships\\Small\\body_01.png"))
        go_player.add_component(Player())
        go_player.get_component("Player").add_thruster(go_thruster, go_thruster_main)
        
        
        
        self._gameObjects.append(go_southship)
        self._gameObjects.append(go_northship)
        self._gameObjects.append(go_thruster)
        self._gameObjects.append(go_thruster_main)
        self._gameObjects.append(go_player)
        self._gameObjects.append(go_mothership)
        self._gameObjects.append(go_turret_one)
        self._gameObjects.append(go_turret_two)
        self._gameObjects.append(go_turret_three)
        self._gameObjects.append(go_turret_four)

    def draw_text(self,text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self._game_world.screen.blit(img,(x,y))
    
    def spawn_enemy(self):
        go_enemy = GameObject(pygame.math.Vector2(0,0))
        go_enemy.add_component(SpriteRenderer("ship_1782.png"))
        go_enemy.add_component(Enemy())
        go_enemy.add_component(Collider())
        self.instantiate(go_enemy)

    def spawn_boss(self):  
        go_boss = GameObject(pygame.math.Vector2(1150,400))
        go_boss.add_component(SpriteRenderer("Spaceships\\ship_41.png"))
        go_boss.add_component(Boss())
        go_boss.add_component(Collider())
        self.instantiate(go_boss)


    def instantiate(self, gameObject):
        gameObject.awake(self._game_world)
        gameObject.start()
        self._gameObjects.append(gameObject)

    def awake(self, game_world):
        super().awake(game_world)
        self.drawen_start_level = False
        self._music = mixer.music.play(-1)
        self._music= mixer.music.set_volume(self._game_world.music_volume/1000)
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self._game_world)        

    def start(self):
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def move_to_endscreen(self, Win):#Win is bool
        self._music = mixer.music.pause()
        self._game_world.score = self._player_score
        self._game_world.ChangeToNewState(loosOrVicState(self._game_world, Win))

    def drawing_UI(self):
        self.draw_text(f"Ammo: {self._game_world.STT_ammo}",self._text_font,(255, 255, 255), 50, 25)
        self.draw_text(f"Score: {self._player_score}",self._text_font,(255, 255, 255), 500, 25)
        self.draw_text(f"Lives",self._text_font,(255, 255, 255), 950, 25)
        
        self.draw_text(f"{self._menu_sele}", self._text_font_sel,(255, 255, 255), 400, 100)
        
        if self._game_world.worldPause == True and self._options_sele == False:
            match self._menu_sele:
                case 0: #back but
                    self.draw_text("Back", self._text_font_sel,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font,(255, 255, 255), 500, 460)
                case 1: #Options but
                    self.draw_text("Back",self._text_font,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font_sel,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font,(255, 255, 255), 500, 460)
                case 2: #Menu but
                    self.draw_text("Back",self._text_font,(255, 255, 255), 500, 360)
                    self.draw_text("Options",self._text_font,(255, 255, 255), 500, 410)
                    self.draw_text("Menu",self._text_font_sel,(255, 255, 255), 500, 460)
        elif self._game_world.worldPause == True and self._options_sele == True:
            match self._menu_sele:
                case 0:
                    self.draw_text("Music", self._text_font_sel, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font_sel, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font, (255, 255, 255), 500, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (255, 255, 255), 750, 460)
                case 1:
                    self.draw_text("Music", self._text_font, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font_sel, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font_sel, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font, (255, 255, 255), 500, 460)
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font, (255, 255, 255), 750, 460)
                case 2:
                    self.draw_text("Music", self._text_font, (255, 255, 255), 500, 360)
                    self.draw_text(f"{self._game_world.music_volume}", self._text_font, (255, 255, 255), 700, 360)
                    self.draw_text("SFX", self._text_font, (255, 255, 255), 500, 410)
                    self.draw_text(f"{self._game_world.SFX_volume}", self._text_font, (255, 255, 255), 700, 410)
                    self.draw_text("Graphics", self._text_font_sel, (255, 255, 255), 500, 460)    
                    self.draw_text(f"{self._game_world.Graphics[self._graphics_opt]}", self._text_font_sel, (255, 255, 255), 750, 460)

    def update(self, delta_time):
        
        self.enemy_timer +=delta_time
        
        self._backgroundv3_go.update(delta_time)
        self._middle_groundV3_go.update(delta_time)

        self.fps_counter(self.clock, self._game_world.screen)
        delta_time = self.clock.tick(60) / 1000.0 # limits FPS to 60
        
        if self._game_world.worldPause == False:
            #Makes a copy om _gameObjects and runs through that instead of the orginal
            for gamObjects in self._gameObjects[:]:
                gamObjects.update(delta_time)

            for i, collider1 in enumerate(self._colliders):
                for j in range(i + 1, len(self._colliders)):
                    collider2 = self._colliders[j]
                    collider1.collision_check(collider2)
            self._gameObjects = [obj for obj in self._gameObjects if not obj._is_destroyed]
        self._fore_groundV3_go.update(delta_time)
        self._effect_groundv3_go.update(delta_time)

        if self.enemy_timer >= self.enemy_delay:
            self.spawn_enemy()
            self.enemy_timer = 0 #resets cooldown after shoot()
        
        if self.should_boss_spawn == True:
            self.spawn_boss()
            self.should_boss_spawn = False
        
        if self.drawen_start_level == False:
            if self.enemy_timer <= 2:
                self.draw_text("Final level started",self._text_font,(255, 255, 255), 750, 450)
            if self.enemy_timer >= 2:
                self.drawen_start_level = True
        
        self.drawing_UI()
        self.handle_input()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self._game_world.worldPause == False:
                    self._game_world.worldPause = True
                    #self.pause_game()
                elif self._game_world.worldPause == True and event.key == pygame.K_p:
                    self._game_world.worldPause = False
                    self._options_sele = False
                elif event.key == pygame.K_COMMA:
                    self.move_to_endscreen(True)
                if self._game_world.worldPause == True:
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
                            #self._menu_sound.play()
                            self.do_options_input(-1)
                            #self._menu_sound.set_volume(self._game_world.SFX_volume/1000)
                        elif event.key == pygame.K_RIGHT:
                            #self._menu_sound.play()
                            self.do_options_input(1)
                            #self._menu_sound.set_volume(self._game_world.SFX_volume/1000)
                self._menu_sele = max(0, min(2, self._menu_sele))
                
    def do_menu_input(self):
        match self._menu_sele:
            case 0:#new game
                self._game_world.worldPause = False
            case 1:#Options
                    self._options_sele = True
            case 2:# back to menu
                self._options_sele == False
                self._game_world.worldPause = False
                self._music = mixer.music.pause()   
                level = MenuState(self._game_world)
                self._game_world.ChangeToNewState(level)
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
                self._music= mixer.music.set_volume(self._game_world.music_volume/1000)
            case 1: #sfx Volumen
                if self._opt_menu_sel == 2:
                    self._game_world.SFX_volume += 10     
                    if self._game_world.SFX_volume > 100:
                        self._game_world.SFX_volume = 100     
                elif self._opt_menu_sel == 0:
                    self._game_world.SFX_volume -= 10     
                    if self._game_world.SFX_volume < 0:
                        self._game_world.SFX_volume = 0     
                self._music= mixer.music.set_volume(self._game_world.SFX_Volume/1000)
            case 2:#Grapchis options
                self._graphics_opt = self.tmp
        #Resets the pos to 1
        self._opt_menu_sel = 1
    def makeTurret(self, string):
        turret = GameObject(pygame.math.Vector2(0,0))
        turret.add_component(SpriteRenderer(string))
        turret.add_component(Turret())
        return turret 
    
    def fps_counter(self, clock, screen):
        BLACK = (255, 255, 255)
        WHITE= (0, 0, 0)
        fps = int(clock.get_fps())
        fps_text = f"FPS: {fps}"
        font = pygame.font.SysFont("Verdana", 15)
        text_surface = font.render(fps_text, True, BLACK)
        screen.blit(text_surface,(10, 10))  

    
class loosOrVicState(State):
    def __init__(self, game_world, win) -> None:
        super().__init__(game_world)             
        #not selected
        self._text_font = pygame.font.Font("Assets\\Font\\ARCADE_R.TTF", 30)
        #Selected
        self._text_font_sel = pygame.font.Font("Assets\\Font\\ARCADE_I.TTF", 30)

        if win == True:
            self._background_image_path ="WonGame.png"
            self._background_go = GameObject(position=(0, 0))
            self._background_go.add_component(MenuBackground(game_world, image_path=self._background_image_path))
        else:
            self._background_image_path ="LostGame.png"
            self._background_go = GameObject(position=(0, 0))
            self._background_go.add_component(MenuBackground(game_world, image_path=self._background_image_path))

        self._text_font_write_name = pygame.font.Font("Assets\\Font\\ARCADE_N.TTF", 30)
        self._player_name = ""
        self._writen_name = False
        self._read_Json = False
        self._sorting = None
        
        self._score_holder = SavingScore
        self._menu_sele = 0
    
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self._game_world.screen.blit(img,(x,y))

    def write_player_name(self):
        self.draw_text("Your score:", self._text_font, (255,255,255), 300, 30)
        self.draw_text(f"{self._game_world.Score}", self._text_font, (255,255,255), 650, 30)
        self.draw_text("Write your desired name", self._text_font, (255,255,255), 300, 80)
        self.draw_text(f"{self._player_name}", self._text_font_write_name, (255,255,255), 350, 180)
        self.draw_text("Press       to continue", self._text_font, (255,255,255), 300, 280)
        self.draw_text("      enter            ", self._text_font_sel, (139,0,139), 300, 280)
        
    def drawing_endscreen(self):
        self.draw_text("Score:", self._text_font, (255,255,255), 500, 20)
        #displaying the player score
        self.draw_text(f"{self._game_world.Score}", self._text_font, (255,255,255), 700, 20)
        self.draw_text("Name:        Score:", self._text_font, (255,255,255), 400, 65)
        if self._menu_sele == 0:
            self.draw_text("Restart", self._text_font, (255,255,255), 300, 600)        
            self.draw_text("Main Menu", self._text_font, (255,255,255), 700, 600)        
        match self._menu_sele:
            case -1:#Restart the game
                self.draw_text("Restart", self._text_font_sel, (255,255,255), 300, 600)        
                self.draw_text("Main Menu", self._text_font, (255,255,255), 700, 600)        
            case 2:#Head to main menu
                self.draw_text("Main Menu", self._text_font_sel, (255,255,255), 700, 600)        
                self.draw_text("Restart", self._text_font, (255,255,255), 300, 600)        
                
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
                
            self.draw_text(f"{name}", self._text_font, (255,255,255), 400, y)
            self.draw_text(f"{score}", self._text_font, (255,255,255), 825, y)
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
        
        self._background_go.update(delta_time)
        
        if self._writen_name == False:
            self.write_player_name()
        else:
            self.drawing_endscreen()
        self.handle_input()
        
        #Makes a copy om _gameObjects and runs through that instead of the orginal
        for gamObjects in self._gameObjects[:]:
            gamObjects.update(delta_time)
