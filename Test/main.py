from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty,BooleanProperty
from kivy.graphics.vertex_instructions import Line,Rectangle,Ellipse
from kivy.graphics.context_instructions import Color
from kivy.properties import Clock


class WeigetTest(GridLayout):
    count=1
    count_enabled=BooleanProperty(False)
    my_text= StringProperty("0")
    #slider_value_txt=StringProperty("50")
    text_input_str=StringProperty("Placeholder")


    def on_button_click(self):
        print("Button clicked")
        if self.count_enabled==True:
            self.my_text = str(self.count)
            self.count+=1

    def on_toggle_button_state(self,weiget):
        print("Toggle state:"+ weiget.state)
        if weiget.state== 'normal':
            weiget.text="Off"
            self.count_enabled=False
        else:
            weiget.text='On'
            self.count_enabled=True

    def on_switch_active(self,widget):
        print("Switch: " + str(widget.active))

    def on_slider_value(self,widget):
        print("Slider:"+ str(int(widget.value)))
        #self.slider_value_txt = str(int(widget.value))

    def on_text_validate(self,widget):
        self.text_input_str=widget.text

class StackLayoutTest(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range (0,100):
            #size=dp(100)+ i*10
            size=dp(100)
            b=Button(text=str(i+1) ,size_hint= (None  ,None),size=(size,size))
            self.add_widget(b)

#class GridLayoutTest(GridLayout):
#    pass

class AnchorLayoutTest(AnchorLayout):
    pass

class BoxLayoutTest(BoxLayout):
    pass
"""    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        b1=Button(text="A")
        b2=Button(text="B")
        self.add_widget(b1)
        self.add_widget(b2)"""

class TestWidget(Widget):
    pass

class TestApp(App):
    pass

class CanvasTest(Widget):
    pass

class CanvasTest1(Widget):
    pass

class CanvasTest2(Widget):
    pass

class CanvasTest3(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Line(points=(100,100,400,500),width= 2)
            Color(0,1,0)
            Line(circle=(400,200,80))
            Line(rectangle=(500,300,150,100))
            self.rect=Rectangle(pos=(500,450),size=(150,100))

    def on_button_a_click(self):
        x,y=self.rect.pos
        w,h=self.rect.size
        inc=dp(10)
        diff=self.width-(x+w)
        if diff<inc:
            inc=diff

        x+=inc
        self.rect.pos=(x,y)

class CanvasTest4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size=dp(50)
        self.vx=dp(3)
        self.vy=dp(4)
        with self.canvas:
            self.ball=Ellipse(pos=self.center,size=(self.ball_size,self.ball_size))
        Clock.schedule_interval(self.update,1/50)

    def on_size(self,*agrs):
        #print("on size"+ str(self.width)+","+str(self.height))
        self.ball.pos=(self.center_x-self.ball_size/2,self.center_y-self.ball_size/2)

    def update(self,dt):
        #print("update")
        x,y=self.ball.pos
        x+=self.vx
        y+=self.vy
        self.ball.pos=(x+4,y)
        if y+ self.ball_size > self.height:
            y = self.height - self.ball_size
            self.vy = -self.vy
        if x + self.ball_size > self.width:
            x = self.width - self.ball_size
            self.vx = -self.vx
        if y < 0:
            y=0
            self.vy = -self.vy
        if x < 0:
            x=0
            self.vx = -self.vx

        self.ball.pos=(x,y)
        
class CanvasTest5(Widget):
    pass

class CanvasTest6(BoxLayout):
    pass

TestApp().run()