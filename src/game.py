import random
import pygame
import pytmx #module pour gérer la map
import pyscroll
import sys
import time
sys.path.append('./src')
from components.player import Player
from utilities.map import MapManager
from utilities.dialog import *

class Game : #reprensete le concept du jeu

    def __init__(self): #fonction au chargement du jeu
        
        #définir la police générale
        self.font = pygame.font.Font("./dialogs/dialog_font.ttf", 40)

        self.menu_theme = pygame.mixer.Sound("./sound/menu_theme_128.ogg")
        self.menu_theme.set_volume(0.4)
        self.menu_theme.play()
        self.menu_compteur = 0

        #créer la fenetre du jeu
        self.screen = pygame.display.set_mode((1024, 768)) #taille de la fenetre

        pygame.display.set_caption("PyDance") #Nom de la fenêtre

    
        self.is_game_started = False
        self.is_game_paused = False

        #charger les bouton de lancement et d'arrêt :

        self.cassette_img = pygame.image.load("maps/cassette.png")
        self.cassette_img = pygame.transform.scale(self.cassette_img, (self.screen.get_width() ,self.screen.get_height()))
        
        self.start_button = pygame.image.load("icon/start_icon.png")
        self.start_button = pygame.transform.scale(self.start_button, (45, 45))
            
        self.quit_button = pygame.image.load("icon/stop_icon.png")
        self.quit_button = pygame.transform.scale(self.quit_button, (45, 45))

        self.start_button_rect=self.start_button.get_rect()
        self.start_button_rect.x = 680
        self.start_button_rect.y = 225

        self.quit_button_rect=self.quit_button.get_rect()
        self.quit_button_rect.x = 315
        self.quit_button_rect.y = 223
        
        if self.is_game_started == False :
            self.display_start_menu()
        
            #generer les boites de dialogue
        self.dialog_box = Dialog()
        self.inventaire_dialog = Menu_Inventaire()
        self.equip_dialog = Menu_Equipement()

            #générer un joueur
        self.player = Player()

        

        for j in range (8):
            self.player.inventory.create_item(self.dialog_box, f"Caillou",["Il prend d'la place pour pas grand chose."], "Ressources", "littleRock")
        self.player.equipment.add_item(self.dialog_box,"Epee du Gueux",["Hmm, c'est un simple bâton"], "Arme", [5, 0, 0], "goldenKey")
        self.player.equipment.add_item(self.dialog_box,"Chaussons", ["Juste un lacet autour de la cheville"], "Chaussures", [0, 1, 0], "bottes gonflables")
        self.player.equipment.add_item(self.dialog_box,"Vieille blouse", ["Qui donne le Blues"], "Armure", [0, 3, 0], "goldenKey")

        self.map_manager = MapManager(self.screen, self.player)

    def clean_game(self):
        self.is_game_started=False
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player) 

    def display_start_menu(self):
        self.screen.fill((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
        self.screen.blit(self.cassette_img, (0,0))
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.quit_button, self.quit_button_rect)
        # pygame.display.flip()        

    
    #récupérer les input du clavier et définir les actions    
    def handle_input(self):
        pressed = pygame.key.get_pressed() #quelle touche a été pressée

        if pressed[pygame.K_UP]:
            self.player.move("up")
        elif pressed[pygame.K_DOWN]: 
            self.player.move("down")
        elif pressed[pygame.K_LEFT]: 
            self.player.move("left")
        elif pressed[pygame.K_RIGHT]: 
            self.player.move("right")

    def change_layer(self, is_half_time):
        s = pygame.Surface((1024,768))  # the size of your rect              
        s.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        if is_half_time:
            s.set_alpha(random.randint(20,60))
        else:
            s.set_alpha(0)
        return(s)
    

    def update(self):
        self.map_manager.update()

    def startgame(self):
        pygame.mixer.Sound(f"./sound/cassette_start.ogg").play()
        time.sleep(1.5)
        self.is_game_started=True
        self.menu_theme.stop()
        self.map_manager.lecture_music()

    def run(self):
        clock = pygame.time.Clock() 
        #boucle du jeu pour maintenir la fenetre ouverte
        running = True

        while running:
            for event in pygame.event.get():
                if self.is_game_started==False:
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_RETURN:
                            self.startgame()
                        elif event.key==pygame.K_ESCAPE:
                            running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.start_button_rect.collidepoint(event.pos):
                            self.startgame()
                        elif self.quit_button_rect.collidepoint(event.pos):
                            running = False
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.dialog_box.reading:
                                self.dialog_box.next_text()
                            else:
                                self.inventaire_dialog.reading=False
                                self.equip_dialog.reading=False
                                self.map_manager.check_npc_collision(self.dialog_box, )
                                self.map_manager.check_sign_collision(self.dialog_box, )
                                self.map_manager.check_object_collision(self.dialog_box,)
                                self.map_manager.check_closedDoor_collision(self.dialog_box,)
                    # elif event.key == pygame.K_RETURN:
                        elif event.key == pygame.K_i:
                            if self.dialog_box.reading==False:
                                if self.inventaire_dialog.reading:
                                    self.inventaire_dialog.reading=False
                                else:
                                    self.equip_dialog.reading=False
                                    self.inventaire_dialog.execute(self.player.inventory.get_listeItem())
                        elif event.key == pygame.K_e:
                            if self.dialog_box.reading==False:
                                if self.equip_dialog.reading:
                                    self.equip_dialog.reading=False
                                else:
                                    self.inventaire_dialog.reading=False
                                    self.equip_dialog.execute(self.player.equipment.get_listeItem())
                if event.type == pygame.QUIT : #si la personne clique sur fermer :
                    running = False

            if self.is_game_started==True:
                self.menu_button = pygame.image.load("icon/stop_icon.png")
                self.menu_button = pygame.transform.scale(self.menu_button, (45, 45))
                self.menu_button_rect=self.menu_button.get_rect()

                self.synchronisator= self.map_manager.get_synchronisator()
                self.is_half_time = self.map_manager.get_is_half_time()
                self.player.save_location()
                self.handle_input()
                self.update()
                self.map_manager.draw()
                self.dialog_box.render(self.screen)
                self.inventaire_dialog.render(self.screen)
                self.equip_dialog.render(self.screen)
                if self.synchronisator==0:
                        s = self.change_layer(self.is_half_time)
                self.screen.blit(s, (0, 0))
                self.screen.blit(self.menu_button, (1200, 40))
                    
                if self.player.life==0:
                    pygame.mixer.Sound(f"./sound/cassette_stop.ogg").play()
                    self.screen.fill((0,0,0))
                    image_texte = self.font.render( "Vous êtes morts !", 1 , (255,0,0) )
                    self.screen.blit(image_texte, (300, 320))
                    time.sleep(1.3)
                    pygame.display.flip()
                    self.map_manager.stop_music()
                    time.sleep(2)
                    self.clean_game() 
                    self.is_game_started=False
                    self.menu_theme.play()
            else:
                self.menu_compteur+=128/60/4
                if self.menu_compteur >= 60:
                    self.display_start_menu()
                    self.menu_compteur=0
                                                    
            pygame.display.flip() #recharger l'affichage
            clock.tick(60) #60 image/sec
        pygame.quit()
        