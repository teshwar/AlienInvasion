import pygame

from pygame.sprite import Sprite

"""
A class used to manage bullets fired from the ship
"""
class Bullet(Sprite):

    def __init__(self,alienInvasion):
        """
        Create a bullet object at ship current position
        """
        super().__init__()
        self.screen = alienInvasion.screen
        self.settings = alienInvasion.settings
        self.color = self.settings.bullet_color

        # Create a bullet at object (0,0) then correct its position relative to the ship
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = alienInvasion.ship.rect.midtop

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """
        Move the bullet up the screen.
        """

        # Update the position of the bullet
        self.y -= self.settings.bullet_speed

        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """
        Draw the bullet to the screen
        """
        pygame.draw.rect(self.screen, self.color, self.rect)

    def blitme(self):
        """
        Draw the bullet on the screen
        """
        pygame.draw.rect(self.screen, self.color, self.rect)