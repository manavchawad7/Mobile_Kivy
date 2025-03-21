from kivy.config import Config
Config.set('graphics','width','900')
Config.set('graphics','height','400')

import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty,ObjectProperty,StringProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line,Quad,Triangle
from kivy.properties import Clock
from kivy.core.window import Window
from kivy import platform
from kivy.lang.builder import Builder
from kivy.core.audio import SoundLoader

Builder.load_file('menu.kv')

class MainWidget(RelativeLayout):

    from transform import transform,transform_2D,transform_perspective
    from user_action import on_keyboard_down,on_keyboard_up,on_touch_down,on_touch_up,keyboard_closed

    menu_widget=ObjectProperty()
    perspective_point_x=NumericProperty(0)
    perspective_point_y=NumericProperty(0)

    V_NB_Lines=8
    V_Lines_Spacing=.4 #percent in width screen
    vertical_lines=[]

    H_NB_Lines=15
    H_Lines_Spacing=.1 #percent in width screen
    horizental_lines=[]

    Speed=.8
    current_offset_y=0
    current_y_loop=0

    Speed_x=3
    current_speed_x=0
    current_offset_x=0

    NB_Tiles=16
    tiles=[]
    tiles_coordinate =[]

    Ship_Width=.1
    Ship_Hight=0.035
    Ship_Base_Y=0.04
    ship=None
    ship_coordinates=[(0,0),(0,0),(0,0)]

    state_game_over = False
    state_game_has_started=False

    menu_button_title=StringProperty("START")
    menu_title=StringProperty("G   A   L   A   X   Y")

    score_txt= StringProperty()

    sound_begin=None
    sound_galaxy =None
    sound_gameover_impact =None
    sound_gameover_voice =None
    sound_music1 =None
    sound_restart =None

    def __init__(self, **kwargs):
        super(MainWidget,self).__init__(**kwargs)
        #print('INIT W:'+ str(self.width)+ 'H:'+ str(self.height))
        self.init_vertical_lines()
        self.init_horizental_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()
        

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update,1/60)

    def init_audio(self):
        self.sound_begin =SoundLoader.load('audio/begin.wav')
        self.sound_galaxy =SoundLoader.load('audio/galaxy.wav')
        self.sound_gameover_impact =SoundLoader.load('audio/gameover_impact.wav')
        self.sound_gameover_voice =SoundLoader.load('audio/gameover_voice.wav')
        self.sound_music1 =SoundLoader.load('audio/music1.wav')
        self.sound_restart =SoundLoader.load('audio/restart.wav')

        self.sound_music1.volume =1
        self.sound_begin.volume =0.25
        self.sound_galaxy.volume =0.25
        self.sound_gameover_impact.volume =0.6
        self.sound_gameover_voice.volume =0.25
        self.sound_restart.volume =0.25
        

    def reset_game(self):
        self.tiles_coordinate=[]
        self.current_offset_y=0
        self.current_y_loop=0
        self.current_speed_x=0
        self.current_offset_x=0
        self.score_txt = "SCORE: " + str(self.current_y_loop)

        self.pre_fill_tile_coordinate()
        self.generate_tiles_coordinate()
        self.state_game_over = False


    def is_desktop(self):
        if platform in ('linux','win','macosx'):
            return True
        return False
    
    def init_ship(self):
        with self.canvas:
            Color(0,0,0)
            self.ship=Triangle()

    def update_ship(self):
        center_x= self.width/2
        base_y= self.Ship_Base_Y* self.height
        ship_half_width=self.Ship_Width* self.width/2
        ship_height=self.Ship_Hight*self.height

        self.ship_coordinates[0]= (center_x-ship_half_width,base_y)
        self.ship_coordinates[1]= (center_x,base_y+ship_height)
        self.ship_coordinates[2]= (center_x+ship_half_width,base_y)

        x1,y1=self.transform(*self.ship_coordinates[0])
        x2,y2=self.transform(*self.ship_coordinates[1])
        x3,y3=self.transform(*self.ship_coordinates[2])

        self.ship.points=[x1,y1,x2,y2,x3,y3]

    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinate)):
            ti_x, ti_y = self.tiles_coordinate[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinate(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinate(ti_x + 1, ti_y + 1)
        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    
    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range (0,self.NB_Tiles):
                self.tiles.append(Quad())

    def pre_fill_tile_coordinate(self):
        for i in range (0,10):
            self.tiles_coordinate.append([0,i])
        

    def generate_tiles_coordinate(self):
        last_x=0
        last_y=0

        for i in range(len(self.tiles_coordinate)-1,-1,-1):
            if self.tiles_coordinate[i][1]< self.current_y_loop:
                del self.tiles_coordinate[i]

        if len(self.tiles_coordinate) > 0:
            last_coordinate=self.tiles_coordinate[-1]
            last_x=last_coordinate[0]
            last_y=last_coordinate[1] +1

        for i in range (len(self.tiles_coordinate),self.NB_Tiles):
            r= random.randint(0,2)
            start_index= -int(self.V_NB_Lines/2)+1
            end_index= start_index+self.V_NB_Lines-2
            if last_x <= start_index:
                r=1
            if last_x >= end_index:
                r= 2

            self.tiles_coordinate.append((last_x,last_y))
            if r==1:
                last_x+=1
                self.tiles_coordinate.append((last_x,last_y))
                last_y += 1
                self.tiles_coordinate.append((last_x,last_y))

            if r==2:
                last_x-=1
                self.tiles_coordinate.append((last_x,last_y))
                last_y += 1
                self.tiles_coordinate.append((last_x,last_y))


            last_y+= 1

        #print('R')

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            #self.line=Line(points=[100,0,100,100])
            for i in range(0,self.V_NB_Lines):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self,index):
        center_line_x=self.perspective_point_x
        spacing=self.V_Lines_Spacing*self.width
        offset= index - 0.5
        line_x=center_line_x + offset*spacing + self.current_offset_x
        return line_x
    
    def get_line_y_from_index(self,index):
        spacing_y=self.H_Lines_Spacing*self.height
        line_y=index*spacing_y-self.current_offset_y
        return line_y
    
    def get_tile_coordinate(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y
    
    def update_tiles(self):
        for i in range(0,self.NB_Tiles):
            tile=self.tiles[i]
            tile_cordinate=self.tiles_coordinate[i]
            xmin,ymin=self.get_tile_coordinate(tile_cordinate[0],tile_cordinate[1])
            xmax,ymax=self.get_tile_coordinate(tile_cordinate[0]+1,tile_cordinate[1]+1)

            x1,y1=self.transform(xmin,ymin)
            x2,y2=self.transform(xmin,ymax)
            x3,y3=self.transform(xmax,ymax)
            x4,y4=self.transform(xmax,ymin)

            tile.points=[x1,y1,x2,y2,x3,y3,x4,y4]


    def update_vertical_line(self):
        start_index= -int(self.V_NB_Lines/2)+1
        for i in range(start_index,start_index+self.V_NB_Lines):
            line_x= self.get_line_x_from_index(i)

            x1,y1 = self.transform(line_x,0)
            x2,y2 = self.transform(line_x,self.height)
            self.vertical_lines[i].points=[x1,y1,x2,y2]

    def init_horizental_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0,self.H_NB_Lines):
                self.horizental_lines.append(Line())

    def update_horizental_line(self):
        start_index= -int(self.V_NB_Lines/2)+1
        end_index= start_index+self.V_NB_Lines-1

        x_min=self.get_line_x_from_index(start_index)
        x_max=self.get_line_x_from_index(end_index)

        for i in range(0,self.H_NB_Lines):
            line_y=self.get_line_y_from_index(i)
            x1,y1 = self.transform(x_min,line_y)
            x2,y2 = self.transform(x_max,line_y)
            self.horizental_lines[i].points=[x1,y1,x2,y2]
    
    
    
    def update(self,dt):
        #print('dt:'+str(dt))
        time_factor=dt*60
        self.update_vertical_line()
        self.update_horizental_line()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            speed_y=self.Speed* self.height/100
            self.current_offset_y+= speed_y*time_factor

            spacing_y=self.H_Lines_Spacing*self.height
            while self.current_offset_y>= spacing_y:
                self.current_offset_y-=spacing_y
                self.current_y_loop+=1
                self.score_txt = "SCORE: " + str(self.current_y_loop)
                self.generate_tiles_coordinate()
                #print('loop'+ str(self.current_y_loop))

            speed_x=self.current_speed_x * self.width/100
            self.current_offset_x+=speed_x * time_factor

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_title="G  A  M  E    O  V  E  R"
            self.menu_button_title= "RESTART"
            self.menu_widget.opacity= 1
            print('Game over')

    def on_menu_button_pressed(self):
        #print('tree')
        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity= 0



class GalaxyApp(App):
    pass

GalaxyApp().run()