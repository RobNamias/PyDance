import pygame
import sys
sys.path.append('./src')
from utilities.renderItem import renderedItem

class Item(renderedItem):
    def __init__(self, name, dialog, typeOf, typeofRenderedItem):
        super().__init__(typeofRenderedItem)
        self.name = name
        self.dialog=dialog
        self.nb_item = 1
        self.typeOfItem = typeOf
        #On récupère lk'image à partir d'un point
        # self.image.set_colorkey([0, 0, 0])
        self.rect = self.get_image(self.get_dimension()).get_rect()
        self.feet = self.rect

class Key(Item):
    def __init__(self, name, typeofRenderedItem, dialog,  related_gate, position):
        super().__init__(name, dialog, "key", typeofRenderedItem)
        self.related_gate = related_gate
        self.position=position
        self.visible=True

class Chest(Item):
    def __init__(self, name, dialog, typeOf, typeofRenderedItem):
        super().__init__(name, dialog, "chest", typeofRenderedItem)
        self.is_empty=False
        self.visible=True
        self.inventory=[Equipement("Bottes gonflables", ["Permet de marcher sur l'eau"], "Chaussures", [0,0,0], "bottes gonflables")]


class Equipement(Item):
    def __init__(self, name, dialog, type, stats, typeofRenderedItem):
        # stats : un tableau [atk, def, vie]
        super().__init__(name, dialog, "equipment", typeofRenderedItem)
        self.type = type
        # type est armure/collier/arme2/chaussures/Gant/Coiffe/
        self.stats = stats