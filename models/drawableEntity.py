from pygame import image, transform

class DrawableEntity:
    def __init__(self, x, y, size, media_path):
        self.x = x
        self.y = y
        self.size = size
        self.media_path = media_path
        self.__init_sprites()
        self.refresh()

    def __init_sprites(self):
        if (self.media_path):
            self.image = image.load(self.media_path)
            self.image = transform.scale(self.image, (self.size, self.size))
        else:
            pass
            # self.rect = self.image.get_rect()

    def refresh(self):
        pass
        # self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)