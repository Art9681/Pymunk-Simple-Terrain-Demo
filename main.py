import pyglet
from cocos.director import director
import scenes
import terrain_gen

def main():
    pyglet.font.add_directory('.')
    director.init(width=1024, height=768, do_not_scale=True, caption = "TerrainDemo", vsync = False, resizable = True)
    director.show_FPS = True
    my_scene = scenes.MyGame()

    #Tile Map tiles have to be either manually selected to display, or a scrolling manager is used. Below I use
    #set_view to manually since we are not scrolling yet.
    my_scene.resource.set_view(0, 0, 1024, 768)

    # run the scene
    director.run(my_scene)

if __name__ == '__main__':
    terrain_gen.Gen_XML()
    #Look for resources in the data directory.  If you modify the path, you must call reindex.
    pyglet.resource.path.append('data')
    pyglet.resource.reindex()
    main()