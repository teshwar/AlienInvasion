import sys
import pygame

from Settings import Settings
from Ship import Ship

"""Overall class to manage different class + logic"""
class AlienInvasion:

    def __init__(self):
        """Initialise the game and create the game resources"""
        pygame.init()

        # Settings and clock
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Initialise the screen
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #Ship and Alien
        self.ship = Ship(self)


    def run_game(self):
        """Start the main loop to run the game"""
        while True:
            # Watch keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw screen everytime through the loop
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            
            # Update game frame
            pygame.display.flip()
            self.clock.tick(60)

# Make game instance, and run it
if __name__ == '__main__':
    alienInvasion = AlienInvasion()
    alienInvasion.run_game()