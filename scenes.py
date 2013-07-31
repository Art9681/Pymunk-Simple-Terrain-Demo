import pyglet
import cocos
from pyglet.window import key, mouse
import layers

class DevScene(cocos.scene.Scene):
    def __init__(self):
        super(DevScene, self).__init__()



class MyGame(cocos.scene.Scene):
    def __init__(self, director):
        super(MyGame, self).__init__()

        #Create the clock and delta time variables.
        #The clock ticks 60 times a second.
        self.clock = pyglet.clock
        self.dt = 1/60

        #The layers this scene has.
        self.bg_color = cocos.layer.ColorLayer(100, 120, 150, 255)
        self.scroller = layers.Scroller(director, self.clock)
        self.add(self.bg_color, z=0)
        self.add(self.scroller.scroller, z=1)


        #Begin clock tick.
        #self.clock.schedule(self.scroller.update)

