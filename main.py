import pyglet
from cocos.director import director
import scenes
import terrain_gen

# Disable error checking for increased performance
pyglet.options['debug_gl'] = False

def main():
    pyglet.font.add_directory('.')
    director.init(width=1024, height=768, do_not_scale=True, caption = "TerrainDemo", vsync = False, resizable = True)
    director.show_FPS = True
    my_scene = scenes.MyGame(director)

    # run the scene
    director.run(my_scene)

if __name__ == '__main__':
    terrain_gen.Gen_XML()
    #Look for resources in the data directory.  If you modify the path, you must call reindex.
    pyglet.resource.path.append('data')
    pyglet.resource.reindex()
    main()