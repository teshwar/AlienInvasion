import pygame.font
from pygame.sprite import Group

from Ship import Ship

"""
A class to report scoring information
"""
class Scoreboard:

    def __init__(self, alienInvasion):
        """"
        Initialize scoring attributes
        """
        self.alienInvasion = alienInvasion
        self.screen = alienInvasion.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = alienInvasion.settings
        self.stats =  alienInvasion.stats
        

        # Font settings for scoring information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()

        # Display levels & ships
        self.prep_level()
        self.prep_ships()

    
    def prep_score(self):
        """
        Turn the scoreboard into a rendered image
        """
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)

        # Display the score at the top right of the screen. 
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 
        self.score_rect.top = 20
    
    def prep_high_score(self):
        """
        Turns the highscore into a rendered image
        """
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,self.settings.bg_color)

        # Center highscore at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """
        Turn the level into a rendered image
        """
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.text_color, self.settings.bg_color)

        # Position level below score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        """
        Show how many ships are left
        """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.alienInvasion)
            ship.rect.x = 10 +  ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """
        Draw scores, level & ships to the screen
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    
    def check_high_score(self):
        """
        Check to see if there is a new highscore
        """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    