import pyglet
import cocos
import layers

class MyGame(cocos.scene.Scene):
    def __init__(self):
        super(MyGame, self).__init__()


        #Create the clock and delta time variables.
        #The clock ticks 60 times a second.
        self.clock = pyglet.clock

        #The layers this scene has.
        self.mainLayer = layers.MainLayer()


        #Add the layers to the scene.
        self.add(self.mainLayer, z=0)

        #self.clock.schedule(self.levelMain.update)
