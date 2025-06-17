import pygame
import sys
sys.path.append('./src')
from utilities.animation import AnimateSprite
from components.inventory import Inventory, Equipment

class Entity(AnimateSprite):
    
    def __init__(self, name, x , y, max_life=int):
        super().__init__(name,max_life)
        self.image = self.get_image(0, 0) #On récupère lk'image à partir d'un point
        self.image.set_colorkey([0, 0, 0])
        #dessiner la barre de vie (sur quoi, la couleur, la position relative au joueur)
        pygame.draw.rect(self.image, (60, 63, 60), [0, 0, self.max_life/3, 5])
        pygame.draw.rect(self.image, (0, 128, 0), [0, 0, self.life/3, 5]) 
        self.rect = self.image.get_rect() #définir sa position
        self.position = [x , y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.direction = "down"

    def save_location(self):self.old_position = self.position.copy()

    #self.position[0] est la première valeur du tableau self.position, donc le x = abscisse
    def move(self, direction):
        match direction:
            case "right":
                self.direction="right"
                self.change_animation("right")
                self.position[0] += self.speed
            case "left":
                self.direction="left" 
                self.change_animation("left")
                self.position[0] -= self.speed
            # print(f"Le PNJ se déplace à {self.speed}") 
            case "up":
                self.direction="up" 
                self.change_animation("up") 
                self.position[1] -= self.speed
        # print(f"le pnj se déplace à {self.speed}") 
            case "down":
                self.direction="down" 
                self.change_animation("down")  
                self.position[1] += self.speed

    def update(self) :
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom #initier la position des pieds en bas au centre de la position du player

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def change_life(self, diff_life):
        self.life += diff_life
        



class Player(Entity):

    def __init__(self):
        super().__init__("player", 0 ,0, 100)
        self.inventory = Inventory(30)
        self.equipment = Equipment()
               

class NPC(Entity):
    
    def __init__(self, name, nb_points, dialog, bpm):
        super().__init__(name, 0,0, 200)
        self.nb_points = nb_points
        self.points=[] #On définit les points de passage
        self.name = name
        self.dialog = dialog
        self.speed = bpm/120
        self.current_point = 0

    def move_npc(self):
        current_point= self.current_point
        target_point=self.current_point+1

        #Quand on arrive au dernier element self.points, on repart du premier pour faire un mouvement cyclique
        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

               #comparer les points selon les directions pour définir le mouvement :
        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3: #ajoute une tolérance de 3 pixels au_ cas où les points ne sont pas parfaitement sur le même x
            self.move("down")
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3: #ajoute une tolérance de 3 pixels au_ cas où les points ne sont pas parfaitement sur le même x
            self.move("up")
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3: #ajoute une tolérance de 3 pixels au_ cas où les points ne sont pas parfaitement sur le même y
            self.move("right")
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3: #ajoute une tolérance de 3 pixels au_ cas où les points ne sont pas parfaitement sur le même y
            self.move("left")


        if self.rect.colliderect(target_rect):
            self.current_point=target_point
        

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range (1, self.nb_points+1):
            #on récupére les objets sur la map
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            #on récupère leur surface
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            #on les ajoute à la liste de points
            self.points.append(rect)

class Boss(NPC):
    def __init__(self, name, nb_points, dialog, bpm):
        super().__init__(name, nb_points, dialog, bpm)
        self.compteur_pas=0

    def move_boss(self, entity):            
        current_point= self.current_point
        target_point = current_point + 1
        if target_point >= self.nb_points:
            target_point = 0    
          
        if (abs(self.position[0]-entity.position[0])<100 and abs(self.position[1]-entity.position[1])<100) :
            target_rect=entity.rect
        else:
            target_rect = self.points[target_point]
        if self.rect.colliderect(target_rect):
            self.current_point=target_point
        current_rect = self.rect

        if abs(current_rect.x - target_rect.x) < abs(current_rect.y - target_rect.y):
            if current_rect.y < target_rect.y:
               self.move("down")
            else:
                self.move("up")
        else:
            if current_rect.x < target_rect.x:
                self.move("right")
            else:
                self.move("left")
        