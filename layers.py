import cocos
from cocos import layer, tiles, actions
from pyglet.window import key, mouse


#Handles the scrolling manager. Physics layers get added to this and this class gets added to the scene.
class Scroller(object):
    def __init__(self, director, clock):
        super(Scroller, self).__init__()

        self.clock = clock

        #The camera layer. Our target is the sprite.
        self.cam_layer = cocos.layer.ScrollableLayer()
        self.cam_target = cocos.sprite.Sprite("sword.png")
        self.cam_target.position = (1024/2, 768/2)
        self.cam_layer.add(self.cam_target)

        #Begin Scrolling Manager.
        self.scroller = cocos.layer.ScrollingManager()
        self.terrain_layer = cocos.tiles.load('test.xml')['map0']
        self.terrain_layer.width = 1920
        self.terrain_layer.height = 1080
        self.scroller.add(self.terrain_layer)
        self.scroller.add(self.cam_layer)


        #Begin Keyboard code.
        self.keyboard = key.KeyStateHandler()
        director.window.push_handlers(self.keyboard)
        director.window.push_handlers(self.on_mouse_motion)
        director.window.push_handlers(self.on_key_press, self.on_key_release, self.on_mouse_press)

    def update(self, dt):
        self.scroller.force_focus(self.cam_target.x, self.cam_target.y)

    def move_cam_up(self, dt):
        self.cam_target.y = self.cam_target.y + 1
    def move_cam_down(self, dt):
        self.cam_target.y = self.cam_target.y - 1
    def move_cam_left(self, dt):
        self.cam_target.x = self.cam_target.x - 1
    def move_cam_right(self, dt):
        self.cam_target.x = self.cam_target.x + 1


    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            print "W key pressed"
            self.clock.schedule(self.move_cam_up)
        if symbol == key.S:
            print "W key pressed"
            self.clock.schedule(self.move_cam_down)
        if symbol == key.A:
            print "W key pressed"
            self.clock.schedule(self.move_cam_left)
        if symbol == key.D:
            print "W key pressed"
            self.clock.schedule(self.move_cam_right)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            print "stopped"
            self.clock.unschedule(self.move_cam_up)
        if symbol == key.S:
            print "W key pressed"
            self.clock.unschedule(self.move_cam_down)
        if symbol == key.A:
            print "W key pressed"
            self.clock.unschedule(self.move_cam_left)
        if symbol == key.D:
            print "W key pressed"
            self.clock.unschedule(self.move_cam_right)

    def on_mouse_press (self, x, y, buttons, modifiers):
        #print self.scroller.pixel_from_screen(x, y)
        self.cell = self.terrain_layer.get_at_pixel(x, y)
        print self.cell.tile.id







    def on_mouse_motion(self, x, y, dx, dy):
        print '%d, %d' % (x, y)