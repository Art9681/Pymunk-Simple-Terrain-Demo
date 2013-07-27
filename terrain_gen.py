import random
from noise import snoise2, pnoise2
import xml.etree.cElementTree as ET



class Gen_XML(object):
    def __init__(self):

        #The map variables.
        self.map_size = (1024, 768)
        self.tile_size = 32
        self.columns = self.map_size[0]/self.tile_size
        self.rows = self.map_size[1]/self.tile_size

        #The texture source variables.
        self.source_size = (96, 64)

        #Begin noise code
        self.octaves = random.randint(16, 30)
        self.freq = random.uniform(16.0, 30.0) * self.octaves
        self.nData = []

        for y in range(32):
            for x in range (24):
                self.nData.append(int(snoise2(x / self.freq, y / self.freq, self.octaves) * 127.0 + 128.0 ))
        #End noise code



        self.xml_tilemap()

    def xml_tilemap(self):
        self.resource = ET.Element("resource")
        self.requires = ET.SubElement(self.resource, "requires")
        self.requires.set("file", "blocks.xml")
        self.rectmap = ET.SubElement(self.resource, "rectmap")
        self.rectmap.set("id", "map0")
        #self.rectmap.set("origin", "100,0,0")
        self.rectmap.set("tile_size", "32x32")

        self.counter = 0

        for col in range(self.columns):
            self.column = ET.SubElement(self.rectmap, "column")

            for row in range(self.rows):
                self.cell = ET.SubElement(self.column, "cell")
                self.cell.set("tile", "air" if self.nData[self.counter] <= 100 else "dirt")
                self.counter += 1
                print self.counter



        self.tree = ET.ElementTree(self.resource)
        self.tree.write("test.xml")


