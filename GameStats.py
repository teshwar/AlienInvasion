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

        # High score never to be reset
        self.high_score = 0

    def reset_stats(self):
        """
        Initiazlize stastistics that can change during the game
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
