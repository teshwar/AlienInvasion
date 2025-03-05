import pygame
import logging

""""
A class to manage the ship
"""

class Ship:
    def __init__(self,alienInvasion):
        """
        Initialsie the ship and set its starting position
        """
        #logging setup
        logging.basicConfig(level=logging.DEBUG)

        self.screen = alienInvasion.screen
        self.screen_rect = alienInvasion.screen.get_rect()
        self.settings = alienInvasion.settings


        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Get a float for ship exact horizontal coordinate (The x coordinate)
        self.x = float(self.rect.x)

        # Movement Flag
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """
        Center the ship on the screen
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """
        Update the ship position based on the flags
        """  

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # New x position of ship
        self.rect.x = self.x


    def blitme(self):
        """
        Draw the ship at it's current location
        """
        self.screen.blit(self.image, self.rect)

