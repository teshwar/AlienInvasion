import logging

import sys
from time import sleep

import pygame

from Settings import Settings
from Ship import Ship
from Bullet import Bullet
from Alien import Alien
from GameStats import GameStats

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

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        #Ship and Bullets Group
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Aliens group + create alien
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = True

        
    def run_game(self):
        """Start the main loop to run the game"""
        while True:

            # Check for any events
            self._check_events()


            # Parts that should be checked only when game is active
            if self.game_active:
                # Update ship
                self.ship.update()

                # UPdate bullets & delete bullets if they went out of range
                self._update_bullets()

                # Update aliens 
                self._update_aliens()

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
        """
        Update position of bullets and get rid of old bullets
        """
        # Update bullets
        self.bullets.update()

        # Check if bullets went out of screen
        # If so delete it
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """"
        Respond to bullet-alien collisions
        """
        # Check if any bullets have hit the aliens
        # If so, get ridd of bullet and alien
        # The 2 true arguments tell pygame to delete the bullets and aliens that have collided
        # To make an opp bullet destroying all alien, set first Boolean to False, and second boolean to True
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True )

        # If there is no alients create new ones &
        # Replenish bullets
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _ship_hit(self):
        """
        Respond to the ship being hit by an alien
        """

        # Decrement ships_left
        self.stats.ships_left -= 1


        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and cneter the ship
        self._create_fleet()
        self.ship.center_ship()

        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
        
            # Pause 
            sleep(0.5)

        else:
            self.game_active = False

    def _create_fleet(self):
        """"
        Create the fleet of aliens.
        """

        # Create an alien and keep adding aliens until
        # there is no room left

        # Spacing between aliens is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width , alien_height

        # Make aliens rows until there is 3 alien space
        while current_y < (self.settings.screen_height - 3 * alien_height):

            # Make sure there is space enough for 2 aliens before
            while current_x < (self.settings.screen_width -2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        """
        Create an alien and place it in the row
        """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """
        Update the positions of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for any alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
           self._ship_hit()
        
        # Look for any alien hitting the bottom screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """
        Respond appropriately if any aliens have reached an edge
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """
        Drop the entire fleet and change the fleet's direction
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """
        Check if any aliens have reached the bottom of the screen
        """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship ogt hit
                self._ship_hit()
                break


    def _update_screen(self):
        """"
        Update game frame
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        
        #aleins
        self.aliens.draw(self.screen)

        # bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Update game frame
        pygame.display.flip()


# Make game instance, and run it
if __name__ == '__main__':
    alienInvasion = AlienInvasion()
    alienInvasion.run_game()