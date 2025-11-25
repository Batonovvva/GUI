import pygame
import sys
from logic import settings
from classes.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Spiral Marble Shooter")
    clock = pygame.time.Clock()

    game = Game(screen)

    game.state = "menu"

    running = True
    while running:
        dt = clock.tick(settings.FPS) / 1000.0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(settings.FPS) / 1000.0

        game.handle_events(events)
        game.update(dt)
        game.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
