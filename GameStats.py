"""
Track statistics for Alien Invasion
"""
class GameStats:

    def __init__(self, alienInvasion):
        """
        Initialize stastistics
        """
        self.settings = alienInvasion.settings
        self.reset_stats()

    def reset_stats(self):
        """
        Initiazlize stastistics that can change during the game
        """
        self.ships_left = self.settings.ship_limit
