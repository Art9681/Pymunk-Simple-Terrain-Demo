import cocos
from cocos import layer, tiles
from pyglet.window import key

class MainLayer(cocos.tiles.RectMapLayer):
    def __init__(self):
        super( MainLayer, self ).__init__()

        self.resource = cocos.tiles.load('test.xml')['map0']
        self.add(self.resource)
