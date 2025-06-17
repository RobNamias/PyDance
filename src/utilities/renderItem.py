import pygame

#définir une classe Animation
class renderedItem(pygame.sprite.Sprite):
    def __init__(self, typeofRenderedItem):
        super().__init__()
        # print(typeofRenderedItem)
        self.sprite_sheet = pygame.image.load(f"./sprites/Items/{typeofRenderedItem}.png")
        self.height = self.sprite_sheet.get_height()
        self.width = self.sprite_sheet.get_width()
        self.size=[self.width, self.height]
        self.proportion = self.width/self.height
        self.image = pygame.Surface(self.size)
        self.image.blit(self.sprite_sheet, (0,0),(0, 0, self.width/2,self.height))
        self.image.set_colorkey([0, 0, 0])

    def get_dimension(self): return (self.size)
        
    def set_image(self, statut=True):
        x=0
        image = pygame.Surface(self.size)
        if statut is False:
            x=self.size[1]
           
        image.blit(self.sprite_sheet, (0,0),(x, 0, self.width, self.height))
        image.set_colorkey([0, 0, 0])
        self.image=image



    def get_image(self, size, x=0):
        image = pygame.Surface(size)
        image.blit(pygame.transform.scale(self.sprite_sheet, [size[0]*self.proportion,size[1]]), (0,0),(0, 0, size[0]*self.proportion,size[1]))
        image.set_colorkey([0,0,0])
        return image