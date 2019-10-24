import os
import shutil
import logging
import configparser
import time

from general import Arcade, Compressor
from rocketlauncher import RocketLauncher

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


class HyperSpin(Arcade):

    # install helper methods

    def __init__(self, system=None):
        Arcade.__init__(self)

        self.system = system

        # HyperSpin Paths
        self.db_path = os.path.join(self.hs_path, "Databases", self.system)
        self.media_path = os.path.join(self.hs_path, "Media", self.system)
        self.settings_path = os.path.join(self.hs_path, "Settings")
        # Images
        self.images_path = os.path.join(self.media_path, "Images")
        self.artwork1_path = os.path.join(self.images_path, "Artwork1")
        self.artwork2_path = os.path.join(self.images_path, "Artwork2")
        self.artwork3_path = os.path.join(self.images_path, "Artwork3")
        self.artwork4_path = os.path.join(self.images_path, "Artwork4")
        self.backgrounds_path = os.path.join(self.images_path, "Backgrounds")
        self.genre_backgrounds_path = os.path.join(self.images_path, "Genre", "Backgrounds")
        self.genre_wheel_path = os.path.join(self.images_path, "Genre", "Wheel")
        self.letters_path = os.path.join(self.images_path, "Letters")
        self.other_path = os.path.join(self.images_path, "Other")
        self.particle_path = os.path.join(self.images_path, "Particle")
        self.special_path = os.path.join(self.images_path, "Special")
        self.wheel_path = os.path.join(self.images_path, "Wheel")
        # Other Media
        self.themes_path = os.path.join(self.media_path, "Themes")
        self.video_path = os.path.join(self.media_path, "Video")

    def _settings_ini(self):
        msg = "HS: Setting Settings.ini Defaults"
        logger.info(msg)
        ini = os.path.join(self.hs_path, "Settings", "Settings.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        config.set("Main", "Hyperlaunch_Path", os.path.join(self.rl_path, "RocketLauncher.exe"))

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    def _main_menu_ini(self):
        msg = "HS: Setting Main Menu Defaults"
        logger.info(msg)
        ini = os.path.join(self.hs_path, "Settings", "Main Menu.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        config.set("wheel", "alpha", "0")
        config.set("wheel", "style", "vertical")
        config.set("sounds", "game_sounds", "false")
        config.set("sounds", "wheel_click", "false")

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    def _rename_genre_art(self):
        missing_wheel = "Favorites", "Educational"
        missing_background = "Flying"

        wheel_dir = os.path.join(self.hs_path, "Media", "MAME", "Images", "Genre", "Wheel")
        background_dir = os.path.join(self.hs_path, "Media", "MAME", "Images", "Genre", "Backgrounds")

        # ------ Backgrounds -----

        src = os.path.join(background_dir, "Board Games Games.png")
        dst = os.path.join(background_dir, "Board Games.png")
        shutil.move(src, dst)

        src = os.path.join(self.hs_path, "Media", "MAME", "Images", "Genre", "Genre Image Educational.png")
        dst = os.path.join(background_dir, "Educational Games.png")
        shutil.move(src, dst)

        src = os.path.join(background_dir, "Favorites.png")
        dst = os.path.join(background_dir, "Favorites Games.png")
        shutil.move(src, dst)

        src = os.path.join(background_dir, "Spinner Gamesjpg.png")
        dst = os.path.join(background_dir, "Spinner Games.png")
        shutil.move(src, dst)

        src = os.path.join(self.hs_path, "Media", "MAME", "Images", "Genre", "Utility1.png")
        dst = os.path.join(background_dir, "Utility Games.png")
        shutil.move(src, dst)

        # ------ Wheels -----

        src = os.path.join(wheel_dir, "Board Games Games.png")
        dst = os.path.join(wheel_dir, "Board Games.png")
        shutil.move(src, dst)

        src = os.path.join(wheel_dir, "Climbing.png")
        dst = os.path.join(wheel_dir, "Climbing Games.png")
        shutil.move(src, dst)

        src = os.path.join(wheel_dir, "Educational.png")
        dst = os.path.join(wheel_dir, "Educational Games.png")
        shutil.move(src, dst)

        src = os.path.join(wheel_dir, "Mini-Games Games.png")
        dst = os.path.join(wheel_dir, "Mini-Games.png")
        shutil.move(src, dst)

        src = os.path.join(wheel_dir, "Role-Playing.png")
        dst = os.path.join(wheel_dir, "Role-Playing Games.png")
        shutil.move(src, dst)

        src = os.path.join(wheel_dir, "Utility.png")
        dst = os.path.join(wheel_dir, "Utility Games.png")
        shutil.move(src, dst)

        src = os.path.join(wheel_dir, "Handball.png")
        dst = os.path.join(wheel_dir, "Handball Games.png")
        shutil.move(src, dst)

    def _extract_archive(self):
        """
        "extract_archive" is a method that unzips the archives

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        cf = Compressor(self.hyperspin_archive)
        cf.extract_all(self.hs_path)

        cf = Compressor(self.hyperspin_upgrade_archive)
        cf.extract_all(self.hs_path)

    def install(self):
        msg = "Installing HyperSpin"
        logger.info(msg)
        if not os.path.exists(self.hs_path):
            os.makedirs(self.hs_path)
        self._extract_archive()
        self._settings_ini()
        self._main_menu_ini()
        self._rename_genre_art()
        rl = RocketLauncher(system=None)
        exe = os.path.join(self.hs_path, "HyperSpin.exe")
        rl.write_frontends_ini(fe_name="HyperSpin", executable=exe)


if __name__ == "__main__":
    platform = "Nintendo Entertainment System"
    hs = HyperSpin(platform)
    # hs.install()
    rl = RocketLauncher(system=platform)
    exe = os.path.join(hs.hs_path, "HyperSpin.exe")
    rl.write_frontends_ini(fe_name="HyperSpin", executable=exe)
