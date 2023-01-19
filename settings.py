
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.game_active = False
        self.highscore_active = False

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.bg_on = False

        self.laser_width = 5
        self.laser_height = 30
        self.laser_color = 255, 0, 0
        self.lasers_every = 10

        self.aliens_shoot_every = 300

        # Alien points, does not include UFO
        self.alien_points = {
            0: 10,
            1: 20,
            2: 40,
        }

        self.ship_limit = 3  # Total ships allowed in game before game over

        self.fleet_drop_speed = 3
        self.fleet_direction = 1
        self.fleet_direction_ufo = 1
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        self.ufo_speed_factor = 1
        self.alien_speed_factor = 1
        self.ship_speed_factor = 3
        self.alien_laser_speed_factor = 1
        self.ship_laser_speed_factor = 5
