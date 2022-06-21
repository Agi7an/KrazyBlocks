import pygame


class Player():

    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = (x, y, width, height)
        self.vel = 10

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        self.update()