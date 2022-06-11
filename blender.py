#!/usr/bin/env python3

"""
NOTE: It seems like comms from the SY300 are not reliable, so
we make some assumptions about the SY300's state, namely:

1) When the app starts, the blender is not in auto mode, and
2) History is at CUR (0).
TODO: Fix these issues.
"""

# std lib imports

import sys

# third party imports

import kivy
from kivy.app import App
# from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock


import mido

# local imports

# import sy300midi
from sy300midi import set_sy300, get_midi_ports, req_sy300


# Replace this with your
# current version
kivy.require('2.1.0')


# Defining a class
class Sy300Blender(App):

    def __init__(self, **kwargs):
        super(Sy300Blender, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)


    def on_start(self):
        self.oncet = True
        self.history = 0
        self.midi_ports = get_midi_ports()
        if not self.midi_ports:
            print("Connection Failure: SY300 not connected")
            sys.exit(1)
        self.from_sy300 = mido.open_input(self.midi_ports['in'])
        print(self.midi_ports['in'])
        self.to_sy300 = mido.open_output(self.midi_ports['out'])
        Clock.schedule_interval(self.callback_read_midi, .1)  # read the midi port at a regular interval

        self.to_sy300.send(set_sy300([0x7F, 0x00, 0x00, 0x01], [0x01]))  # set the SY300 into verbose or editor mode
        # find out if we are in auto mode:
        # self.to_sy300.send(req_sy300([0x30, 0x00, 0x8, 0xd], [1])) # 0 means yes, 1 means no
        # find out where history is
        self.to_sy300.send(req_sy300([0x30, 0x00, 0x08, 0x0C], [0x1]))



    def get_top_level(self, adr):
        f2 = adr[0:2]
        if f2 == ['0x0', '0x0']:
            return "SETUP"
        if  f2 == ['0x10', '0x0']:
            return "SYSTEM"
        if f2 == ['0x20', '0x0']:
            return "PATCH (Temporary)"
        if f2 == ['0x20', '0x04']:   
            return "PATCH (User 1)"
        if f2 == ['0x23', '0x0C']:
            return "PATCH (User 99)"
        if f2 == ['0x30', '0x0']:
            return "SYSTEMP"
        if f2 == ['0x7F', '0x0']:
            return "EDITOR/VERBOSE"
        return f"UNKNOWN {f2}"
    

    def callback_read_midi(self, dt):
        # print("in callback")
        # for msg in from_sy300:
        for msg in self.from_sy300.iter_pending():
            if self.oncet:
                print("in message iteration")
                self.oncet = False
            if msg.type != 'sysex':
                continue
            # print("got a sysex message")
            data = [hex(x) for x in msg.data]
            adr = data[7:11]
            top_level = self.get_top_level(adr)
            if top_level != "SYSTEMP":
                continue
            payload = data[11:]
            print(f"{top_level} {adr} {payload}")
            # history
            if adr == ['0x30', '0x0', '0x8', '0xc']:
                print(f"got history status, payload is {payload}")
                self.history = int(payload[0], 16)
                if self.history > 0:
                    # TODO left/right buttons should be disabled if blender (auto) is running
                    # regardless of history status
                    self.right_button.disabled = False


            if adr == ['0x30', '0x0', '0x8', '0xd']: # auto on/off
                print("got blender auto message")
                print(f"{payload[0]} {payload[0].__class__}")
                if payload[0] == '0x0': # on
                    print("auto is on")
                    # self.auto_button.text = "Stop"
                    # self.auto_button.background_color = ("mediumspringgreen")
                elif payload[0] == '0x1': # off
                    print("auto is off")
                    # self.auto_button.text = "Auto"
                    # self.auto_button.background_color = [1,1,1,1]

        # print("got midi")


    # Function that returns
    # the root widget
    def build(self):
        
        self.layout = BoxLayout(spacing=10)
        self.left_button = Button(text='<', size_hint=(.2, 1))
        self.left_button.bind(on_press=self.left_button_click)
        self.right_button = Button(text='>', size_hint=(.2, 1), disabled=True)
        self.right_button.bind(on_press=self.right_button_click)
        self.auto_button = Button(text='Auto', size_hint=(.6, 1))
        self.auto_button.bind(on_press=self.auto_button_click)
        self.layout.add_widget(self.left_button)
        self.layout.add_widget(self.right_button)
        self.layout.add_widget(self.auto_button)
        return self.layout

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        # print('The key', keycode, 'have been pressed')
        if keycode in [40, 44]: # space or enter toggles Auto
            self.auto_button_click(self.auto_button)
            return
        if keycode == 80: # left arrow goes left in history
            self.left_button_click(self.left_button)
            return
        if keycode == 79: # right arrow goes right in history
            self.right_button_click(self.right_button)
            return



    def left_button_click(self, instance):
        # TODO disable button if history + 1 == 99
        self.history += 1
        self.to_sy300.send(set_sy300([0x30, 0x00, 0x08, 0x0C], [self.history]))

    def right_button_click(self, instance):
        if instance.disabled:
            return
        if self.history - 2 < 0:
            instance.disabled = True
        self.history -= 1
        self.to_sy300.send(set_sy300([0x30, 0x00, 0x08, 0x0C], [self.history]))


    def auto_button_click(self, instance):
        print(f"{instance.text}")
        if instance.text == "Stop": # starting
        # 0 = auto, 1 = stop
            self.to_sy300.send(set_sy300([0x30, 0x00, 0x08, 0x0D], [0x00]))
            self.auto_button.text = "Auto"
            self.auto_button.background_color = [1,1,1,1]
            return
        if instance.text == "Auto": # starting
            self.to_sy300.send(set_sy300([0x30, 0x00, 0x08, 0x0D], [0x01]))
            self.auto_button.text = "Stop"
            self.auto_button.background_color = ("mediumspringgreen")

    def on_stop(self):
        if self.midi_ports:      # if the midi_ports were not opened, do not close at shutdown.
            # TODO uncomment this (it slows things down):
            self.to_sy300.send(set_sy300([0x7F, 0x00, 0x00, 0x01], [0x00]))  # set the SY300 to turn off verbose/editor mode
            self.to_sy300.close()
            self.from_sy300.close()
            print("Quitting")


if __name__ == '__main__':
    Sy300Blender().run()
    # Here our class is initialized
    # and its run() method is called.
    # This initializes and starts
    # our Kivy application.
