import cocos
from cocos import layer
from pyglet.window import key


class MainLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super( MainLayer, self ).__init__()

        #Detects key presses and releases and fires events accordingly.
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            print "Input SPACE"