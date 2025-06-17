from dataclasses import dataclass
import pygame
import sys
sys.path.append('./src')
from components.item import *


class Inventory:

    def __init__(self, capacity):
        self.liste_item=[]
        self.capacity=capacity


    def add_prebuild_item(self,dialog_box, item):
        if self.check_item(item.name):
            self.check_item(item.name)[1]
            self.liste_item[self.check_item(item.name)[1]].nb_item+=1
        elif (len(self.liste_item)<self.capacity):
            self.liste_item.append(item)
        else:
            dialog_box.execute(["Plus de place dans l'inventaire"])
        dialog_box.execute([f"Ajouté à l'inventaire :  {self.liste_item[len(self.liste_item) - 1].name}", self.liste_item[len(self.liste_item) - 1].dialog[0]])

    def create_item(self, dialog_box, name_item, dialog_item, typeOf, typeOfRenderedItem):
        new_item=Item(name = name_item, dialog= dialog_item, typeOf = typeOf, typeofRenderedItem=typeOfRenderedItem)
        self.add_prebuild_item(dialog_box, new_item)
        
    
    def remove_item(self, name_item):
        # if self.check_item(name_item):
        #     print("Je l'ai déjà")    # self.liste_item[self.liste_item.name.index(name_item)].nb_item+=1
        # else :
            self.liste_item.remove(name_item)

    def check_item(self, name):
        object_own = False
        for i in range(len(self.liste_item)):
            if name==self.liste_item[i].name:
                object_own = True
                index_own_objet = i
        if object_own:
            return (object_own, index_own_objet)
        else:
            return (object_own) 

    def get_listeItem(self):      
        return self.liste_item
    
    def getKeys(self):
        keys=[]
        for i in range (len(self.liste_item)):
            if self.liste_item[i].typeOfItem =="key":
                keys.append(self.liste_item[i])
        return keys

class Equipment(Inventory):
    def __init__(self):
        super().__init__(6)

    def add_item(self, dialog_box, name_item, dialog_item, type, stats, typeOfRenderedItem):
        if (len(self.liste_item)<self.capacity):
            new_item=Equipement(name_item, dialog_item, type, stats, typeOfRenderedItem)
            self.liste_item.append(new_item)
            # print(new_item.name)
        else:
            dialog_box.execute(["Plus de place dans l'inventaire"])
        dialog_box.execute([f"Ajouté à l'inventaire :  {self.liste_item[len(self.liste_item) - 1].name}", self.liste_item[len(self.liste_item) - 1].dialog[0]])
    
    def add_prebuild_equipment(self, dialog_box, equipment):
        if (len(self.liste_item)<self.capacity):
            self.liste_item.append(equipment)
        else:
            dialog_box.execute(["Plus de place dans l'inventaire"])
        dialog_box.execute([f"Ajouté à l'inventaire :  {self.liste_item[len(self.liste_item) - 1].name}", self.liste_item[len(self.liste_item) - 1].dialog[0]])

        
class ChestInventory(Inventory):
    def __init__(self, capacity):
        super().__init__(capacity)
