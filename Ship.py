import pygame

""""
A class to manage the ship
"""

class Ship:
    def __init__(self,alienInvasion):
        """
        Initialsie the ship and set its starting position
        """
        self.screen = alienInvasion.screen
        self.screen_rect = alienInvasion.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """
        Draw the ship at it's current location
        """
        self.screen.blit(self.image, self.rect)