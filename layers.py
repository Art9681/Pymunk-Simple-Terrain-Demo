import cocos
from cocos import layer, tiles, actions
import pyglet
from pyglet.window import key, mouse
import pymunk
import pymunk.pyglet_util
import player

class PhysicsLayer(cocos.layer.ScrollableLayer):
    is_event_handler = True
    def __init__(self, clock):
        super( PhysicsLayer, self ).__init__()

        self.space = pymunk.Space()
        self.space.gravity = (0,-700)

        self.player = player.Player(pos=(150, 50))

        self.add(self.player.sprite)

        #If true, draws pymunk bodies using opengl. False = no drawing.
        self.bodies_visible = False

        self.space.add(self.player.body,
                       self.player.shape)

    def create_segment(self, start, end):
        self.segment = pymunk.Segment(self.space.static_body, start, end, 1)
        self.space.add(self.segment)


    def draw(self):
        if self.bodies_visible == True:
            pymunk.pyglet_util.draw(self.space)
        else:
            pass

    def update(self, dt):
        self.player.update()
        self.space.step(dt)

#Contains scrolling manager, tilemap and player layers.
class Scroller(object):
    def __init__(self, director, clock):
        super(Scroller, self).__init__()
        global scroller, terrain_layer, keyboard

        #Initialize some stuff.
        self.air_sprite = pyglet.image.load('air.png')

        self.clock = clock
        #Begin Scrolling Manager.
        self.scroller = cocos.layer.ScrollingManager()

        #Grab physics layer.
        self.physics_layer = PhysicsLayer(clock)

        #The camera layer. Our target is the sprite.
        self.cam_target = cocos.sprite.Sprite("player.png")

        #Begin terrain map layer.
        self.terrain_layer = cocos.tiles.load('test.xml')['map0']

        self.scroller.add(self.terrain_layer, z=0)
        self.scroller.add(self.physics_layer, z=1)

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
        director.window.push_handlers(self.on_key_press, self.on_key_release, self.on_mouse_scroll, self.on_mouse_press)

    def update(self, dt):
        self.physics_layer.update(dt)
        #Forces focus and allows to go out of map bounds. There is a different function to keep it in bounds.
        self.scroller.set_focus(*self.physics_layer.player.sprite.position)

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
            if self.physics_layer.bodies_visible == False:
                self.physics_layer.bodies_visible = True
            else:
                self.physics_layer.bodies_visible = False
        if symbol == key.W:
            print "W key pressed"
            self.physics_layer.player.body.velocity.y = 200
        if symbol == key.S:
            print "S key pressed"
            self.physics_layer.player.body.velocity.y = -200
        if symbol == key.A:
            print "A key pressed"
            self.physics_layer.player.body.velocity.x = -200
        if symbol == key.D:
            print "D key pressed"
            self.physics_layer.player.body.velocity.x = 200
        if symbol == key.SPACE:
            self.physics_layer.player.body.apply_impulse(pymunk.Vec2d(0, 500), (0, 0))
        if symbol == key.I:
            print len(self.physics_layer.space.shapes)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            print "stopped"
            self.physics_layer.player.body.velocity.y = 0
            #self.clock.unschedule(self.move_cam_up)
        if symbol == key.S:
            print "stopped"
            #self.clock.unschedule(self.move_cam_down)
            self.physics_layer.player.body.velocity.y = 0
        if symbol == key.A:
            print "stopped"
            self.physics_layer.player.body.velocity.x = 0
            #self.clock.unschedule(self.move_cam_left)
        if symbol == key.D:
            print "stopped"
            self.physics_layer.player.body.velocity.x = 0
            #self.clock.unschedule(self.move_cam_right)
        if symbol == key.SPACE:
            self.physics_layer.player.body.apply_impulse(pymunk.Vec2d(0, -200), (0, 0))

    def on_mouse_press (self, x, y, buttons, modifiers):
        #Gets the cell's location from the scrolling manager world coordinates.
        self.cell = self.terrain_layer.get_at_pixel(*self.scroller.pixel_from_screen(x, y))
        #Gets the clicked cell's neighbors.
        self.neighbors = self.terrain_layer.get_neighbors(self.cell)
        top = self.neighbors[(0, 1)]
        bottom = self.neighbors[(0, -1)]
        right = self.neighbors[(1, 0)]
        left = self.neighbors[(-1, 0)]

        #Changes clicked tile to air tile.
        self.cell.tile = cocos.tiles.Tile(id= 'air', properties= {'btype': 'air'}, image= self.air_sprite)
        #Redraws the map. Need to create function that redraws the tile only.
        self.terrain_layer.set_dirty()

        #Gets a list of pymunk objects within 16 pixels of tile center. Since tile size is 32 pixels, this will always find pymunk objects at the border of the tile, hence, the pymunk segments around it if any.
        self.near_shapes =  self.physics_layer.space.nearest_point_query((self.cell.position[0] + 16, self.cell.position[1] + 16), 16, -1, 0)

        #Check to see if pymunk object is the player, if True, ignore this object.
        for i in self.near_shapes:
            if i['shape'] == self.physics_layer.player.shape:
                pass
            else:
                #Deletes all pymunk objects from space, except the player object.
                self.physics_layer.space._remove_shape(i['shape'])

        #The following conditionals determine where to generate segments when a tile is changed to an air tile.
        if top.tile.properties['btype'] != 'air':
                    self.physics_layer.create_segment(start=(self.cell.position[0], self.cell.position[1]+32), end=((self.cell.position[0]+32),self.cell.position[1]+32))

        if bottom.tile.properties['btype'] != 'air':
            self.physics_layer.create_segment(start=(self.cell.position[0], self.cell.position[1]), end=((self.cell.position[0]+32),self.cell.position[1]))

        if right.tile.properties['btype'] != 'air':
                    self.physics_layer.create_segment(start=(self.cell.position[0]+32, self.cell.position[1]), end=((self.cell.position[0]+32),self.cell.position[1]+32))

        if left.tile.properties['btype'] != 'air':
                    self.physics_layer.create_segment(start=(self.cell.position[0], self.cell.position[1]), end=((self.cell.position[0]),self.cell.position[1]+32))

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
            self._desired_scale = 0
        if dy:
            self.scroller.do(cocos.actions.ScaleTo(self._desired_scale, .1))
            return True