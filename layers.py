import cocos
from cocos import layer, tiles, actions
from pyglet.window import key, mouse

#Handles the scrolling manager. Physics layers get added to this and this class gets added to the scene.
class MapCollider(actions.Action, tiles.RectMapCollider):
    global scroller, terrain_layer, keyboard
    on_ground = True
    MOVE_SPEED = 200
    JUMP_SPEED = 500
    GRAVITY = -1500

    def start(self):
        # initial velocity
        self.target.velocity = (0, 0)

    def step(self, dt):
        dx, dy = self.target.velocity
        # using the player controls, gravity and other acceleration influences
        # update the velocity
        dx = (keyboard[key.D] - keyboard[key.A]) * self.MOVE_SPEED *dt
        dy = dy + self.GRAVITY * dt
        if self.on_ground and keyboard[key.SPACE]:
            dy = self.JUMP_SPEED

        # get the player's current bounding rectangle
        last = self.target.get_rect()
        new = last.copy()
        new.x += dx
        new.y += dy * dt

        # run the collider
        dx, dy = self.target.velocity = self.collide_map(terrain_layer, last, new, dy, dx)
        self.on_ground = bool(new.y == last.y)

        # player position is anchored in the center of the image rect
        self.target.position = new.center

        #Forces focus and allows to go out of map bounds. There is a different function to keep it in bounds.
        scroller.force_focus(*new.center)


class Scroller(object):
    def __init__(self, director, clock):
        super(Scroller, self).__init__()
        global scroller, terrain_layer, keyboard
        self.clock = clock

        #The camera layer. Our target is the sprite.
        self.cam_layer = cocos.layer.ScrollableLayer()
        self.cam_target = cocos.sprite.Sprite("player.png")
        self.cam_target.do(MapCollider())

        #Spawn the camera target object at the viewport length/2 and terrain map height/2. Need to automate this.
        self.cam_target.position = (1024/2, 5012/2)
        self.cam_layer.add(self.cam_target)

        #Begin terrain map layer.
        terrain_layer = cocos.tiles.load('test.xml')['map0']
        #Begin Scrolling Manager.
        scroller = cocos.layer.ScrollingManager()
        self.scroller = scroller
        scroller.add(terrain_layer)
        scroller.add(self.cam_layer)

        #Begin Keyboard code.
        keyboard = key.KeyStateHandler()
        director.window.push_handlers(keyboard)
        director.window.push_handlers(self.on_mouse_scroll, self.on_mouse_press)
        #director.window.push_handlers(self.on_key_press, self.on_key_release)

    def move_cam_up(self, dt):
        self.cam_target.y = self.cam_target.y + 1
    def move_cam_down(self, dt):
        self.cam_target.y = self.cam_target.y - 1
    def move_cam_left(self, dt):
        self.cam_target.x = self.cam_target.x - 1
    def move_cam_right(self, dt):
        self.cam_target.x = self.cam_target.x + 1

    #Begin input code.
    '''def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            print "W key pressed"
            self.clock.schedule(self.move_cam_up)
        if symbol == key.S:
            print "S key pressed"
            self.clock.schedule(self.move_cam_down)
        if symbol == key.A:
            print "A key pressed"
            self.clock.schedule(self.move_cam_left)
        if symbol == key.D:
            print "D key pressed"
            self.clock.schedule(self.move_cam_right)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            print "stopped"
            self.clock.unschedule(self.move_cam_up)
        if symbol == key.S:
            print "stopped"
            self.clock.unschedule(self.move_cam_down)
        if symbol == key.A:
            print "stopped"
            self.clock.unschedule(self.move_cam_left)
        if symbol == key.D:
            print "stopped"
            self.clock.unschedule(self.move_cam_right)'''

    def on_mouse_press (self, x, y, buttons, modifiers):
        #Gets the cell's location from the scrolling manager world coordinates.
        self.cell = terrain_layer.get_at_pixel(*scroller.pixel_from_screen(x, y))
        #Removes the tile, effectively deleting it from the map.
        self.cell.tile = None
        #Redraws the map. Need to create function that redraws the tile only.
        terrain_layer.set_dirty()

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    _desired_scale = 1
    def on_mouse_scroll(self, x, y, dx, dy):
        #Zooms the map.
        if dy < 0:
            if self._desired_scale < .2: return True
            self._desired_scale -= .1
        elif dy > 0:
            if self._desired_scale > 2: return True
            self._desired_scale += .1
        if dy:
            scroller.do(cocos.actions.ScaleTo(self._desired_scale, .1))
            return True

