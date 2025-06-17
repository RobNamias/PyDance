import pygame
import random

class DialogBox:

    # X_POSITION = 100
    # Y_POSITION = 635

    def __init__(self, x, y, width, height, reading):
        self.width=width
        self.height=height
        self.box = pygame.image.load('./dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (self.width, self.height))
        self.X_POSITION=x
        self.Y_POSITION=y
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("./dialogs/dialog_font.ttf", 20)
        self.reading = reading

    def execute(self, dialog=[]):
        pygame.mixer.Sound(f"./sound/dialog_effect_{random.randint(1, 3)}.ogg").play()
        if self.reading==False:
            self.reading=  True
            self.text_index= 0
            self.texts = dialog
            

    def render(self,screen):
        if self.reading :

            self.letter_index += 1

            #pour ne pas dépasser le nombre de caractères prévus
            if self.letter_index <= len(self.texts[self.text_index]):
                self.letter_index= self.letter_index
            
            screen.blit(self.box,(self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0 ,0)) #(texte à afficher), (faut il utiliser des alias ???) ,(r,g,b,)
            screen.blit(text, (self.X_POSITION + 100,self.Y_POSITION + 25)) #On margin

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            #close dialog
            self.reading = False

class Dialog(DialogBox):
    def __init__(self):
        super().__init__(100, 635, 824, 118, True)
        self.texts = ["ESP : Action", "I : Inventaire", "E : Equipement"]


class Menu_Inventaire(DialogBox):
    def __init__(self):
        super().__init__(112, 0, 800, 400, False)
        self.blockTab = []

    def execute(self, liste_item):
        pygame.mixer.Sound(f"./sound/dialog_effect_{random.randint(1, 3)}.ogg").play()
        if self.reading==False:
            self.reading=  True
            self.item_index= 0
            
            self.liste_item = liste_item
            self.blockTab=[]
    
    def render(self,screen):

        if self.reading :
            screen.blit(self.box,(self.X_POSITION, self.Y_POSITION))
            for item_index in range (0, len(self.liste_item)):
                self.letter_index += 1
                #pour ne pas dépasser le nombre de caractères prévus
                if self.letter_index <= len(self.liste_item[item_index].name):
                    self.letter_index= self.letter_index          
                
                text = self.font.render(self.liste_item[item_index].name, False, (1, 0 ,0))#(texte à afficher), (faut il utiliser des alias ???) ,(r,g,b,)
                text_and_miniature = pygame.Surface([200, 40])
                text_and_miniature.set_colorkey((0,0,0))
                                                    
                text_and_miniature.blit(text, [20, 0])
                text_and_miniature.blit(self.liste_item[item_index].get_image([16,16]), [0, 5])
                self.blockTab.append(text_and_miniature)
                # text_index+=1

            for j in range(0, len(self.blockTab)):
                if (j<10):
                    screen.blit(self.blockTab[j], (self.X_POSITION + 80,self.Y_POSITION +40 + j*30))
                elif (j>=10 and j<20):
                    screen.blit(self.blockTab[j], (self.X_POSITION + 280,self.Y_POSITION +40 + j*30-300))
                elif (j>=20 and j<30):
                    screen.blit(self.blockTab[j], (self.X_POSITION + 480,self.Y_POSITION +40 + j*30-600))

            self.blockTab=[]

class Menu_Equipement(DialogBox):
    def __init__(self):
        super().__init__(724, 0, 300, 280, False)
        self.blockTab = []

    def execute(self, liste_item):
        pygame.mixer.Sound(f"./sound/dialog_effect_{random.randint(1, 3)}.ogg").play()
        if self.reading==False:
            self.reading=  True
            self.item_index= 0
            self.liste_item = liste_item
            self.blockTab=[]
    
    def render(self,screen):

        if self.reading :
            screen.blit(self.box,(self.X_POSITION, self.Y_POSITION))
            for item_index in range (0, len(self.liste_item)):
                self.letter_index += 1
                #pour ne pas dépasser le nombre de caractères prévus
                if self.letter_index <= len(self.liste_item[item_index].name):
                    self.letter_index= self.letter_index          
                
                text = self.font.render(self.liste_item[item_index].name, False, (1, 0 ,0))#(texte à afficher), (faut il utiliser des alias ???) ,(r,g,b,)
                text_and_miniature = pygame.Surface([250, 40])
                text_and_miniature.set_colorkey((0,0,0))
                                                    
                text_and_miniature.blit(text, [20, 0])
                text_and_miniature.blit(self.liste_item[item_index].get_image([16,16]), [0, 5])
                self.blockTab.append(text_and_miniature)


            print(self.blockTab)
            for j in range(0, len(self.blockTab)):
                screen.blit(self.blockTab[j], (self.X_POSITION + 15,self.Y_POSITION +50 + j*30))
            self.blockTab=[]