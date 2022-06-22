import pygame

WIDTH = 500
HEIGHT = 500


class Player():

    def __init__(self, x, y, _width, _height, colour):
        self.x = x
        self.y = y
        self.width = _width
        self.height = _height
        self.colour = colour
        self.rect = (x, y, _width, _height)
        self.vel = 10
        self.alive = True

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.vel
            else:
                self.alive = False

        if keys[pygame.K_RIGHT]:
            if self.x + self.width < WIDTH:
                self.x += self.vel
            else:
                self.alive = False

        if keys[pygame.K_DOWN]:
            if self.y + self.height < HEIGHT:
                self.y += self.vel
            else:
                self.alive = False

        if keys[pygame.K_UP]:
            if self.y > 0:
                self.y -= self.vel
            else:
                self.alive = False

        self.update()