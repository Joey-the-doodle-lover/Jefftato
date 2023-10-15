import pygame
from Game import Game


def create_pygame_screen():
    pygame.init()
    return pygame.display.set_mode((1920, 1080))


def main():
    screen = create_pygame_screen()
    game = Game(screen)

    # Create Game()
    game.run()


if __name__ == '__main__':
    main()
