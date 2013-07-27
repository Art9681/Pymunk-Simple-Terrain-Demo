import pyglet
import cocos
from pyglet.window import key, mouse
import layers

class MyGame(cocos.scene.Scene):
    def __init__(self, director):
        super(MyGame, self).__init__()

        #Create the clock and delta time variables.
        #The clock ticks 60 times a second.
        self.clock = pyglet.clock
        self.dt = 1/60

        #The layers this scene has.
        self.scroller = layers.Scroller(director, self.clock)
        self.add(self.scroller.scroller, z=0)

        #Begin clock tick.
        self.clock.schedule(self.scroller.update)

