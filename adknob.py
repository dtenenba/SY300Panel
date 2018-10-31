from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty


kv = '''
<ADKnob>
    orientation: 'vertical'
    BoxLayout:
        Label:
            id:pad_left
            text:'L'
            size_hint_x:.001
        Label:
            id:sq_pad
            text: '-50'
            font_size: 15
            size_hint_x: None
            width: self.size[1]
            canvas.before:
                Color:
                    rgba: [.4, .4 , .4, .5 ]
                Line:  # Middle Bar
                    width:4
                    cap: 'none'
                    points:[(sq_pad.center_x,sq_pad.pos[1]), (sq_pad.center_x, sq_pad.top)]
                Color:
                    rgba: [0, 0 , 1, .9]
                Line: # Attack Line
                    width: 2
                    cap: 'none'
                    points: [sq_pad.center_x - 6,sq_pad.pos[1], sq_pad.center_x - 6, sq_pad.top] #offset from center
                Line: # Decay Line
                    width: 2
                    cap: 'none'   
                    points: [sq_pad.center_x + 6 ,sq_pad.pos[1], sq_pad.center_x + 6, sq_pad.top] #offset from center
            
                Color:
                    rgba:[1,1,1,1]
                Line:
                    width:2
                    rectangle: (*self.pos,self.width,self.height)

                
        Label:
            id:pad_right
            text: 'R'
            size_hint_x: .001 
    #Label:
    #    text: 'Y-Axis Label'
    #    size_hint_y: None
    #    height: self.texture_size[1]
    Label:
        text: 'AMP ENV'
        font_size: 15
        size_hint_y: None
        height: self.texture_size[1]
    
    Label:
        text: 'Test pos:' # + str()
        size_hint: (None, None)
        color:[1,1,1,1]
        size: self.texture_size
        pos: (sq_pad.pos[0] + 20,sq_pad.pos[1] + 20) 
'''


class ADKnob(BoxLayout):
    adknob_decay_value = NumericProperty(0)
    adknob_attack_value = NumericProperty(0)
    adknob_ndx = NumericProperty(0)

    def on_touch_down(self, touch):
        if self.ids.sq_pad.collide_point(*touch.pos):
            sq_xy = self.ids.sq_pad.to_widget(*touch.pos, True)
            scale_xy = [int(sq_xy[0] * 100/(self.ids.sq_pad.width - 1)), int(sq_xy[1] * 100/(self.ids.sq_pad.height - 1))]
            print('Self transformed pos:', sq_xy)
            print('Transformed and scaled', scale_xy)
            print('pos', touch.pos)
            print('to local', self.ids.sq_pad.to_widget(*touch.pos, True))

        return super().on_touch_down(touch)


if __name__ == '__main__':
    kv_test = '''
GridLayout:
    rows: 3
    cols: 3
    ADKnob:
    ADKnob:
    ADKnob:
    ADKnob:       
    ADKnob:
    ADKnob:
    ADKnob:
    ADKnob:       
    ADKnob:       

    '''


class ADKnobApp(App):


    def build(self):
        return Builder.load_string(kv + kv_test)

ADKnobApp().run()

