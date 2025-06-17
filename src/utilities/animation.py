import pygame

#définir une classe Animation
class AnimateSprite(pygame.sprite.Sprite):

    #définir les choses à faire à la création de l'entité
    def __init__(self, name, life):
        super().__init__()
        self.name = name
        self.sprite_sheet = pygame.image.load(f"./sprites/Entities/{self.name}.png") #On charge le sprite
        self.animation_index = 0
        self.clock = 0
        self.images= {
            'down' : self.get_images(0), #clé du tableau, puis image
            'left' : self.get_images(32),
            'right' : self.get_images(64),
            'up' : self.get_images(96)
        }
        self.speed = 2 #initialisation pourle premier monde à 120bpm (speed = bpm/60)
        self.max_life=life
        self.life=self.max_life
    
    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0]) #Enlever le fond noir
                #dessiner la barre de vie (sur quoi, la couleur, la position relative au joueur)
        if self.life <=self.max_life/3 :
            color = (255, 0 ,0)
        elif self.life >self.max_life/3  and self.life<self.max_life*2/3 :
            color = (255, 255, 0)
        elif self.life >self.max_life*2/3:
            color = (0, 128, 0)
        pygame.draw.rect(self.image, (60, 60, 60), [0, 0, self.max_life/6, 5])
        pygame.draw.rect(self.image, color, [0, 0, self.life/6, 5]) 
        self.clock += self.speed*4

        if self.clock>=100:
            self.animation_index += 1 #Passer à l'image suivante
            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0
            self.clock=0

    def get_images(self, y):
        images = []
        for i in range(0, 3):
            x = i*32
            image = self.get_image(x, y)
            images.append(image)

        return images
    
    def update_health_bar(self, life, direction):
        self.life=life
        print(self.life)
        self.change_animation(direction)

    def get_image(self, x, y):

         #On découpe l'image de base pour en garder qu'un morceau selon loe mouvement
        image = pygame.Surface([32, 32]) #taille de l'image
        image.blit(self.sprite_sheet, (0,0),(x, y, 32, 32 ))

        return image

