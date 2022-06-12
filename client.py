import pygame
from network import Network
from player import Player

width = 500
height = 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Player")


def redrawWindow(window, player, enemy1, enemy2, enemy3, enemy4):
    window.fill((255, 255, 255))
    player.draw(window)
    enemy1.draw(window)
    enemy2.draw(window)
    enemy3.draw(window)
    enemy4.draw(window)
    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.getPlayer()
    clock = pygame.time.Clock()

    while run:
        pygame.init()
        clock.tick(60)
        # Send this player's details(this client) and receive other player's details through the server
        e1, e2, e3, e4 = n.send(p)
        # print("ClientSide:", e1, e2, e3, e4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        p.move()
        redrawWindow(window, p, e1, e2, e3, e4)

    pygame.quit()


main()