import random
from noise import snoise2, pnoise1
import xml.etree.cElementTree as ET

class Gen_XML(object):
    def __init__(self):
        #The map variables.
        self.map_size = (5056, 5056) #Map size in pixels.
        self.tile_size = 32 #Tiles are 32x32
        #Divide map size by tile size to produce columns and rows.
        self.columns = self.map_size[0]/self.tile_size
        self.rows = self.map_size[1]/self.tile_size

        #This list holds all integers representing 2D simplex noise data.
        self.noise_data = []

        #This counter is incremented every time the terrain gen loops through inserting a cell into a row.
        #Used to keep track of the last item in nData we accessed.
        self.noise_counter = 0

        #The texture source variables.
        self.source_size = (96, 64)

        #Begin noise code
        self.octaves = random.randint(3, 6)
        print "Octaves: %s" %self.octaves
        self.freq = random.uniform(1.0, 10.0) * self.octaves
        #self.freq = 8.0 * self.octaves
        print "Noise Frequency: %s" %self.freq

        for y in range(self.columns):
            for x in range (self.rows):
                self.noise_data.append(int(snoise2(x / self.freq, y / self.freq, self.octaves) * 127.0 + 128.0 ))
        #End noise code

        self.xml_tilemap()

    def xml_tilemap(self):
        self.resource = ET.Element("resource")
        self.requires = ET.SubElement(self.resource, "requires")
        self.requires.set("file", "blocks.xml")
        self.rectmap = ET.SubElement(self.resource, "rectmap")
        self.rectmap.set("id", "map0")
        self.rectmap.set("tile_size", "32x32")
        self.col_height = 80

        for col in range(self.columns):
            self.column = ET.SubElement(self.rectmap, "column")

            #Changes the column height to a value within a given range from the previous value.
            #Bigger range means more drastic changes in column height, lower range means flatter terrain.
            self.col_height = random.randint(self.col_height - 3, self.col_height + 3)

            for row in range(self.rows):
                self.cell = ET.SubElement(self.column, "cell")
                self.cell.set("tile", "air" if row > self.col_height else ("rock" if self.noise_data[self.noise_counter] <= 64 else ("air" if self.noise_data[self.noise_counter] <= 128 else ("dirt" if self.noise_data[self.noise_counter] <= 192 else "sand"))))

                self.noise_counter += 1

        self.tree = ET.ElementTree(self.resource)
        self.tree.write("test.xml")


