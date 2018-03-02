from kivy.app import App
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector
from random import randint
from kivy.uix.boxlayout import BoxLayout
import random
from main import run_en_csv
from threading import Thread

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]




class SimulatorUI(BoxLayout):
    
    def run_simulation(self):
        print "Simulation Running!"
        self.set_status("Simulation Running")
        t = Thread(target=run_en_csv, args=('output', {'battery_capacity':0.001}, self.set_status))
        t.start()
        # t.join()
        # self.set_status("Simulation Finished")
    
    def set_status(self, message):
        self.ids.status.text = message
    


class SimulatorApp(App):
    def build(self):
        sim = SimulatorUI()

        # return Button(text='Hello World')
        return sim

SimulatorApp().run()