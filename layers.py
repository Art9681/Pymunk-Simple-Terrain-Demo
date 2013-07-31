import cocos
from cocos import layer, tiles, actions
from pyglet.window import key, mouse
import pymunk
import pymunk.pyglet_util

class PhysicsLayer(cocos.layer.ScrollableLayer):
    def __init__(self, clock):
        super( PhysicsLayer, self ).__init__()

        self.space = pymunk.Space()
        self.space.collision_slop = 0.3
        self.space.gravity = (0,-700)

    def create_segment(self, start, end):
        segment = pymunk.Segment(self.space.static_body, start, end, 1)
        self.space.add(segment)

    def draw(self):
        pymunk.pyglet_util.draw(self.space)


#Contains scrolling manager, tilemap and player layers.
class Scroller(object):
    def __init__(self, director, clock):
        super(Scroller, self).__init__()
        global scroller, terrain_layer, keyboard

        self.clock = clock

        #Grab physics layer.
        self.physics_layer = PhysicsLayer(clock)

        #The camera layer. Our target is the sprite.
        self.cam_layer = cocos.layer.ScrollableLayer()
        self.cam_target = cocos.sprite.Sprite("player.png")
        #self.cam_target.do(MapCollider())

        #Spawn the camera target object at the viewport length/2 and terrain map height/2. Need to automate this.
        self.cam_target.position = (1024/2, 5012/2)
        self.cam_layer.add(self.cam_target)

        #Begin terrain map layer.
        self.terrain_layer = cocos.tiles.load('test.xml')['map0']
        terrain_layer = self.terrain_layer
        #Begin Scrolling Manager.
        scroller = cocos.layer.ScrollingManager()
        self.scroller = scroller
        scroller.add(self.physics_layer)
        scroller.add(self.terrain_layer)
        scroller.add(self.cam_layer)

        #Begin physics segment collider generation. (This is crazy!)
        self.air_cells = []
        #Get each air cell in the map and append to air_cell list.
        for air_cell in self.terrain_layer.find_cells(btype="air"):
            self.air_cells.append(air_cell)

        #Get the neighbor for each air cell. For each neighbor, determine its block type.
        for air_cell in self.air_cells:
            cell_neighbors = self.terrain_layer.get_neighbors(air_cell)

            top = cell_neighbors[(0, 1)]
            if top:
                if top.tile.properties['btype'] != 'air':
                    self.physics_layer.create_segment(start=(air_cell.position[0], air_cell.position[1]+32), end=((air_cell.position[0]+32),air_cell.position[1]+32))
                    #print top.tile.properties['btype']

            bottom = cell_neighbors[(0, -1)]
            if bottom:
                if bottom.tile.properties['btype'] != 'air':
                    self.physics_layer.create_segment(start=(air_cell.position[0], air_cell.position[1]), end=((air_cell.position[0]+32),air_cell.position[1]))

            right = cell_neighbors[(1, 0)]
            if right:
                if right.tile.properties['btype'] != 'air':
                    self.physics_layer.create_segment(start=(air_cell.position[0]+32, air_cell.position[1]), end=((air_cell.position[0]+32),air_cell.position[1]+32))


            left = cell_neighbors[(-1, 0)]
            if left:
                if left.tile.properties['btype'] != 'air':
                    self.physics_layer.create_segment(start=(air_cell.position[0], air_cell.position[1]), end=((air_cell.position[0]),air_cell.position[1]+32))

        #Begin Keyboard code.
        keyboard = key.KeyStateHandler()
        director.window.push_handlers(keyboard)
        director.window.push_handlers(self.on_key_press, self.on_mouse_scroll, self.on_mouse_press)

    def move_cam_up(self, dt):
        self.cam_target.y = self.cam_target.y + 1
    def move_cam_down(self, dt):
        self.cam_target.y = self.cam_target.y - 1
    def move_cam_left(self, dt):
        self.cam_target.x = self.cam_target.x - 1
    def move_cam_right(self, dt):
        self.cam_target.x = self.cam_target.x + 1

    #Begin input code.
    def on_key_press(self, symbol, modifiers):
        if symbol == key.V:
            if self.terrain_layer.visible == True:
                self.terrain_layer.visible = False
                print "Terrain layer Off"
            else:
                self.terrain_layer.visible = True
                print "Terrain layer On"


        '''if symbol == key.W:
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
            self.clock.schedule(self.move_cam_right)'''


    '''def on_key_release(self, symbol, modifiers):
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
        self.cell = self.terrain_layer.get_at_pixel(*scroller.pixel_from_screen(x, y))
        #Removes the tile, effectively deleting it from the map.
        self.cell.tile = None
        #Redraws the map. Need to create function that redraws the tile only.
        self.terrain_layer.set_dirty()

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