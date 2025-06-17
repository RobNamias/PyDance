from dataclasses import dataclass

#cajouter le répertoire parents pour importer une classe d'un autre dossier
import sys

# from utilities.fx_particule import Particule

sys.path.append('./src')
sys.path.append('./sound')

import pygame, pytmx, pyscroll

from components.player import *
from utilities.dialog import *
from components.item import *

@dataclass
class Sign:
    rect : pygame.Rect
    dialog : list[str]


@dataclass
class Portal:
    from_world : str
    origin_point : str
    target_world : str
    teleport_point : str
    is_opened : bool


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    waters: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    groupItem:pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals : list[Portal]
    npcs: list[NPC]
    signs: list[Sign]
    deathzones : list[pygame.Rect]
    bpm : int
    sound : pygame.mixer.Sound
    items : list[Item]

class MapManager:
    def __init__(self, screen, player):
        self.maps = dict() #exemple : clé 'house' -> Map('house', walls, group)
        self.screen= screen
        self.player = player
        self.currentMap = "world"
        self.dialog_box = Dialog()
        self.house_music = pygame.mixer.Sound("./sound/house_theme_150.ogg")
        self.synchronisator = 0
        self.is_half_time = True

        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house", target_world="house", teleport_point="spawn_house", is_opened=True),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house2", is_opened=False)
        ],
        npcs=[
            NPC("jack", nb_points=6, dialog=["Hey !", "J'entends du bruit venant de la maison un peu loin"], bpm = 120), 
            NPC("robin", nb_points=2, dialog=["Venez !", "Venez !!!", "Y'a un tintamarre d'enfer qui s'échappe", "du deuxième étage de cette maison !"], bpm = 120),
            Boss("boss", nb_points=4, dialog=["Le méchant", "C'est le méchant !", "Je suis méchant !"], bpm = 120 )],
        bpm = 120,
        sound=pygame.mixer.Sound("./sound/world_theme_120.ogg"))
        
        self.register_map("house", 
            portals=[
                Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="spawn_exit_house", is_opened=True)
            ],
            bpm = 150,
            sound= self.house_music)

        self.register_map("house2", 
            portals=[
                Portal(from_world="house2", origin_point="exit_house2", target_world="world", teleport_point="spawn_exit_house2",is_opened=True),
                Portal(from_world="house2", origin_point="enter_house2_2", target_world="house2_2", teleport_point="spawn_house2_2",is_opened=True)
            ],
            bpm = 150,
            sound=self.house_music)

        self.register_map("house2_2", 
            portals=[
                Portal(from_world="house2_2", origin_point="exit_house2_2", target_world="house2", teleport_point="spawn_exit_house2_2", is_opened=True),
                Portal(from_world="house2_2", origin_point="enter_dungeon", target_world="dungeon", teleport_point="spawn_dungeon", is_opened=True)
            ],
            bpm = 150,
            sound=self.house_music)

        self.register_map("dungeon", 
            portals=[
                Portal(from_world="dungeon", origin_point="exit_dungeon", target_world="house2_2", teleport_point="spawn_exit_dungeon", is_opened=True),
                Portal(from_world="dungeon", origin_point="backto_world", target_world="world", teleport_point="spawn_exit_dungeon", is_opened=False),
                ],
            npcs=[NPC("boss", nb_points=8, dialog=["Le méchant", "C'est le méchant !", "Je suis méchant !"], bpm = 180 )],
            bpm = 180,
            sound=pygame.mixer.Sound("./sound/dungeon_theme_180.ogg")            
        )

        self.teleport_player("player")
        self.teleport_npcs()

    def stop_music(self):
        self.get_sound().stop()

    def lecture_music(self):
        self.get_sound().set_volume(0.5)
        self.get_sound().play(-1) 
      
    def check_object_collision(self, dialog_box):
        for item in self.get_items():
            if item.visible is True:
                if self.player.feet.colliderect(item.rect):
                    print(item.name)
                    # self.player.inventory.add_item(dialog_box, self.get_items()[i].name,self.get_items()[i].dialog, self.get_items()[i].typeOfItem)
                    if item.typeOfItem=="key":
                        self.player.inventory.add_prebuild_item(dialog_box, item)
                        item.visible=False
                        item.set_image(False)
                    elif item.typeOfItem=="chest":
                        print(item.inventory)
                        for itemChest in item.inventory:
                            print(itemChest)
                            self.player.equipment.add_prebuild_equipment(dialog_box, itemChest)
                            item.inventory.remove(itemChest)
                            # if itemChest. == "equipment":
                            #     print(itemChest.name)
                            #     self.player.equipment.add_prebuild_item(self,dialog_box, itemChest)
                        item.is_opened = True
                        item.set_image(False)
                        # dialog_box.execute([f"Ajouté à l'inventaire :  {self.player.inventory.liste_item[len(self.player.inventory.liste_item) - 1].name}"])

    def check_dz_collision(self):
         if self.synchronisator==0:
            if self.is_half_time==False:
                for i in range(len(self.get_map().deathzones)):

                    for sprite in self.get_group().sprites():
                        if sprite.feet.colliderect(self.get_map().deathzones[i]):
                            sprite.change_life(-5)
                            damage_sound = pygame.mixer.Sound("./sound/damage_sound.ogg")
                            damage_sound.set_volume(0.2)
                            damage_sound.play()
                            print(f"Vie du {sprite.name} : {sprite.life}")
                            sprite.update_health_bar(sprite.life, sprite.direction)

                    # if self.player.feet.colliderect(self.get_map().deathzones[i]):
                    #     self.player.change_life(-5)
                    #     #ajout de l'effet de particules à voir
                    #     # particules = [Particule(self.player.position[0], self.player.position[1]) for _ in range(30)]
                    #     damage_sound = pygame.mixer.Sound("./sound/damage_sound.ogg")
                    #     damage_sound.set_volume(0.2)
                    #     damage_sound.play()
                    #     print(f"Vie du joueur : {self.player.life}")
                    #     self.player.update_health_bar(self.player.life, self.player.direction)


    def check_synchronisator(self):
        self.synchronisator+=self.get_bpm()/120
        if self.synchronisator>=60:
            if self.is_half_time:
                self.is_half_time = False
            else:
                self.is_half_time = True
            self.synchronisator=0

                    
    def check_npc_collision(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) == NPC:
              dialog_box.execute(sprite.dialog)  

    def check_sign_collision(self, dialog_box):
        #panneaux
        for i in range(len(self.get_map().signs)):
            if self.player.feet.colliderect(self.get_map().signs[i].rect):
                    dialog = self.get_map().signs[i].dialog
                    # print(dialog)
                    dialog_box.execute(dialog)

    def check_water_collision(self):
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_waters()) > -1:
                if type(sprite) is Player:
                    if self.player.equipment.check_item("Bottes gonflables") is False:
                        sprite.move_back()
                else:sprite.move_back()


    def check_closedDoor_collision(self, dialog_box):
        for portal in self.get_map().portals:
            if portal.from_world == self.currentMap:
                if portal.is_opened is False:
                    point = self.get_object(portal.origin_point)
                    rect = pygame.Rect(point.x, point.y, point.width, point.height)
                    if dialog_box.reading is False:  
                        if self.player.feet.colliderect(rect):
                            for key in self.player.inventory.getKeys():
                                if key.related_gate==portal.origin_point:
                                    dialog_box.execute(["Vous utilisez la clé."])
                                    portal.is_opened=True
                            if portal.is_opened is False:
                                dialog_box.execute(["Il te faut une clé pour entrer."])




    def check_collisions(self):

        #portails
        for portal in self.get_map().portals:
            if portal.from_world == self.currentMap:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    if self.synchronisator%60==0:
                        if portal.is_opened is True :
                            # print(portal.origin_point)
                            is_meme_music = True
                                    #changement de map ici !
                                    
                                    #si on va jouer le même thème, on n'arrête pas le lecteur.
                            current_theme = self.get_sound()
                            if self.maps[portal.target_world].sound != current_theme:
                                is_meme_music = False
                                self.stop_music()

                            copy_portal = portal
                            self.currentMap=portal.target_world
                            self.player.speed = self.get_bpm()/60
                            self.synchronisator=0
                            # print(f"La vitesse du joueur est de {self.player.speed}" )
                            self.teleport_player(copy_portal.teleport_point)

                            #on ne relance la musique que si on l'a arrêté
                            if is_meme_music == False:
                                self.lecture_music()
        

        #collision
        for sprite in self.get_group().sprites(): 
            if type(sprite) is NPC or type(sprite) is Boss :
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed=0
                else:
                    sprite.speed= self.get_bpm()/120
            if type(sprite) is NPC or type(sprite) is Player:
                if sprite.feet.collidelist(self.get_walls()) > -1:
                    sprite.move_back()


    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()


    def register_map(self, name, portals=[], npcs=[], signs=[], bpm=int, sound=pygame.mixer.Sound): #=[] : argument optionnel
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f"./maps/{name}.tmx")#charge le fichier
        map_data = pyscroll.data.TiledMapData(tmx_data)#map en fonction du fichier
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        item_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        #  gérer les collisions
            #appeler une liste
        waters = []
        walls = []
        signs = []
        deathzones = []
        items = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type =="riviere":
                waters.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "sign":
                Sign.rect=pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                Sign.dialog = obj.dialog.split("+")
                signs.append(Sign(Sign.rect,Sign.dialog))          
                # print(signs)
            elif obj.type == "keys":
                key = Key(name = obj.name, typeofRenderedItem="goldenKey", dialog=[obj.dialog], related_gate=obj.related_gate, position=[obj.x, obj.y])
                # print(key.related_gate)
                key.rect=pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                key.deja_pris= obj.deja_pris
                items.append(key)
            elif obj.type == "chests":
                chest = Chest(name=obj.name, typeOf="Chest", typeofRenderedItem="brownChest", dialog=[""])
                chest.rect=pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                items.append(chest)
            elif obj.type == "deathzone":
                deathzones.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        

                    # After this, use event.y == 1 for upward scroll, while event.y == -1 for downward scroll

        #dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5) #default_layer : positionnement du layer
        groupItem = pyscroll.PyscrollGroup(map_layer=item_layer, default_layer=6) #default_layer : positionnement du layer

        

 


        #recupérer les npcs pour les ajouter aux groupes
        for npc in npcs:
            group.add(npc)

        for item in items:
            groupItem.add(item)
        group.add(groupItem)
        
            #on ajoute le joueur
        group.add(self.player)
        general_overlay=group
        # general_overlay.add(groupItem)
        #Enregistrer la nouvelle carte chargée
        self.maps[name]= Map(name, walls, waters, group, groupItem, tmx_data, portals, npcs, signs, deathzones, bpm, sound, items) 
    
    def get_map(self): return self.maps[self.currentMap]

    def get_bpm(self): return self.get_map().bpm

    def get_group(self): return self.get_map().group

    def get_groupItem(self): return self.get_map().groupItem
        
        # self.getgroupItem.remove(item)

    def get_walls(self): return self.get_map().walls
    
    def get_waters(self): return self.get_map().waters

    def get_signs(self): return self.get_map().signs

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def get_sound(self): return self.get_map().sound

    def get_items(self): return self.get_map().items
    def set_items(self, item):
        if (item in self.get_items()):
            self.get_map().items.remove(item)

    def get_is_half_time(self): return self.is_half_time
    def get_synchronisator(self): return self.synchronisator

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)#Charger les points du NPC par à son monde à lui et pas à la current Map
                npc.teleport_spawn()
  

    def draw(self):   
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.get_groupItem().update()
        self.check_collisions()
        self.check_water_collision()
        self.check_dz_collision()
        self.check_synchronisator()

        for npc in self.get_map().npcs:
            if self.is_half_time==False:
                if type(npc)==Boss:
                    Boss.move_boss(npc, self.player)
                else:
                    npc.move_npc()
                # print(npc.life)
        
        # print(self.get_groupItem())

        