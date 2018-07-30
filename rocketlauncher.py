import logging
import time
import os

from hyperspin import Databases, HyperList

LOG_FILE = "arcade.log"
LOG_STAMP = time.strftime("%Y-%m-%d %H:%M:%S")
LOG_FORMAT = logging.Formatter("[{}] [%(levelname)s] [%(name)s] : %(message)s".format(LOG_STAMP))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(LOG_FORMAT)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(LOG_FORMAT)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class RocketLauncher(Databases, HyperList):

    def __init__(self, system):
        Databases.__init__(self, system)
        HyperList.__init__(self, system)

        self.system = system
        self.rl_ui_path = os.path.join(self.rl_path, "RocketLauncherUI")
        self.settings_path = os.path.join(self.rl_path, "Settings")
        self.modules_path = os.path.join(self.rl_path, "Modules")

        # Media
        self.media_path = os.path.join(self.rl_path, "Media")
        self.artwork_path = os.path.join(self.media_path, "Artwork")
        self.backgrounds_path = os.path.join(self.media_path, "Backgrounds")
        self.bezels_path = os.path.join(self.media_path, "Bezels")
        self.fade_path = os.path.join(self.media_path, "Fade")
        self.logos_path = os.path.join(self.media_path, "Logos")
        self.music_path = os.path.join(self.media_path, "Music")
        self.video_path = os.path.join(self.media_path, "Videos")

        # UI
        self.db_path = os.path.join(self.rl_ui_path, "Databases", self.system)
        self.icon_path = os.path.join(self.rl_ui_path, "Media", "Icons")
        self.ui_logo_path = os.path.join(self.rl_ui_path, "Media", "Logos")


if __name__ == "__main__":
    platform = "Nintendo Entertainment System"
    rl = RocketLauncher(platform)
