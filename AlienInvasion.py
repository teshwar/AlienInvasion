import logging

import sys
import pygame

from Settings import Settings
from Ship import Ship
from Bullet import Bullet

"""Overall class to manage different class + logic"""
class AlienInvasion:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

        """Initialise the game and create the game resources"""
        pygame.init()

        # Settings and clock
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Initialise the screen
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        
        # Full Screen mode
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        #Ship and Bullets Group
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()


    def run_game(self):
        """Start the main loop to run the game"""
        while True:

            # Check for any events
            self._check_events()

            # Update ship
            self.ship.update()

            # UPdate bullets & delete bullets if they went out of range
            self._update_bullets()

            # Redraw screen everytime through the loop
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """
        Helper function to check if there was any keypresses and mouse events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # See if key was press down
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            # See if key is no more press
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """
        Respond to keypressed 
        """
        if event.key == pygame.K_RIGHT:
            # Move the ship to right
            self.ship.moving_right = True

        if event.key == pygame.K_LEFT:
            # Move the ship to right
            self.ship.moving_left = True
        
        # Qutting game with q
        if event.key == pygame.K_q:
            sys.exit()
        
        # Bullets spacebar
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

        

    def _check_keyup_events(self, event):
        """
        Respond to key releases.
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """
        Create new bullet and add it to bullet group
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Update bullets
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

           
    def _update_screen(self):
        """"
        Update game frame
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        
        # bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Update game frame
        pygame.display.flip()


# Make game instance, and run it
if __name__ == '__main__':
    alienInvasion = AlienInvasion()
    alienInvasion.run_game()