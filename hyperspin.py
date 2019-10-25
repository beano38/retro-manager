import os
import shutil
import logging
import configparser
import time
import xml.etree.cElementTree as ET

from general import Arcade, Compressor
from utilities import Databases
from rocketlauncher import RocketLauncher
from models.system import System

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

# logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class HyperSpin(Arcade):

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

        self.default_systems = ["Atari 5200",
                                "Atari Lynx",
                                "Daphne",
                                "NEC TurboGrafx-16",
                                "Nintendo 64",
                                "Nintendo Entertainment System",
                                "Nintendo Game Boy Advance",
                                "Panasonic 3DO",
                                "Sega 32X",
                                "Sega CD",
                                "Sega Dreamcast",
                                "Sega Game Gear",
                                "Sega Genesis",
                                "Sega Master System",
                                "Sega Model 2",
                                "SNK Neo Geo",
                                "SNK Neo Geo Pocket Color",
                                "Sony PlayStation",
                                "Super Nintendo Entertainment System"]

    # Install helper methods

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
        self._remove_junk()

    # New System helper methods

    def _media_directories(self):
        images = ["Artwork1", "Artwork2", "Artwork3", "Artwork4", "Backgrounds", "Genre", "Letters", "Other",
                  "Particle", "Special", "Wheel"]

        for image in images:
            path = os.path.join(self.hs_path, "Media", self.system, "Images", image)
            if not os.path.exists(path):
                os.makedirs(path)

    def _system_ini(self):
        platform = System(system=self.system)
        if type(platform.extensions) == list:
            extension = "zip, 7z, {}".format(platform.extensions[0])
        elif type(platform.extensions) == str:
            extension = "zip, 7z, {}".format(platform.extensions)
        else:
            extension = "zip, 7z"
        msg = "HS: Setting {} Defaults".format(self.system)
        logger.info(msg)
        ini = os.path.join(self.hs_path, "Settings", self.system + ".ini")
        if os.path.isfile(ini):
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read(ini)
        else:
            src_ini = os.path.join(self.hs_path, "Settings", "MAME.ini")
            shutil.copy(src_ini, ini)
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read(ini)

        config.set("exe info", "rompath", os.path.relpath(os.path.join(self.rom_path, self.system), self.hs_path))
        config.set("exe info", "romextension", extension)
        config.set("wheel", "alpha", "0")
        config.set("wheel", "style", "vertical")
        config.set("sounds", "game_sounds", "false")
        config.set("sounds", "wheel_click", "false")

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    def _copy_genre_art(self, link):

        # If Linking files, remove the old file before appending the new symlinks
        links = []
        batch_file = os.path.join(self.root_path, "{} Genre Links run as Admin.bat".format(self.system))
        if os.path.isfile(batch_file):
            os.remove(batch_file)

        if link:
            msg = "Linking Genre Art for {}".format(self.system)
            logger.info(msg)
        else:
            msg = "Copying Genre Art for {}".format(self.system)
            logger.info(msg)

        if not self.system == "MAME":
            src_dir = os.path.join(self.hs_path, "Media", "MAME", "Images", "Genre")
            dst_dir = os.path.join(self.hs_path, "Media", self.system, "Images", "Genre")

            wheel_dir = os.path.join(dst_dir, "Wheel")
            background_dir = os.path.join(dst_dir, "Backgrounds")
            create_dirs = [wheel_dir, background_dir]

            for directory in create_dirs:
                if not os.path.exists(directory):
                    os.makedirs(directory)

            wheels = os.listdir(os.path.join(src_dir, "Wheel"))
            for wheel in wheels:
                src = os.path.join(src_dir, "Wheel", wheel)
                dst = os.path.join(wheel_dir, wheel)
                if link:
                    links.append('mklink "{}" "{}"\n'.format(dst, src))
                else:
                    if not os.path.exists(dst):
                        shutil.copy(src, dst)

            backgrounds = os.listdir(os.path.join(src_dir, "Backgrounds"))
            for background in backgrounds:
                src = os.path.join(src_dir, "Backgrounds", background)
                dst = os.path.join(background_dir, background)
                if link:
                    links.append('mklink "{}" "{}"\n'.format(dst, src))
                else:
                    if not os.path.exists(dst):
                        shutil.copy(src, dst)

            src_dir = os.path.join(self.hs_path, "Media", "MAME", "Images", "Special")
            dst_dir = os.path.join(self.hs_path, "Media", self.system, "Images", "Special")

            specials = os.listdir(src_dir)
            for special in specials:
                src = os.path.join(src_dir, special)
                dst = os.path.join(dst_dir, special)
                if link:
                    links.append('mklink "{}" "{}"\n'.format(dst, src))
                else:
                    if not os.path.exists(dst):
                        shutil.copy(src, dst)
        else:
            msg = "MAME is base Genre Art and will not be copied"
            logger.debug(msg)

        if len(links) > 0:
            with open(batch_file, mode="a") as f:
                for link in links:
                    f.write(link)

    def _read_hs_menu(self):
        """
        "read_hs_menu" is a method that reads the Main Menu.xml database, a.k.a. the Main Menu

        Args:
            self

        Returns:
            a list of Systems

        Raises:
            None
        """
        msg = "Reading HyperSpin Main Menu XML database ..."
        logger.info(msg)
        xml = os.path.join(self.hs_path, "Databases", "Main Menu", "Main Menu.xml")
        tree = ET.parse(xml)
        doc = tree.getroot()
        systems = []
        for child in doc:
            system = child.get("name")
            systems.append(system)
        return systems

    def _write_hs_menu(self, sort=False, remove=False):
        """
        "write_hs_menu" is a method that adds a system to the Main Menu.xml database, a.k.a. the Main Menu

        Args:
            sort (required): If true, sorts by Manufacturer, Platform Type and Year
            remove (optional): If tru, removes the system from the Menu

        Returns:
            None

        Raises:
            None
        """
        systems = self._read_hs_menu()

        if remove:
            systems.remove(self.system)
        else:
            systems.append(self.system)

        platform = {}
        platforms = []

        for system in systems:
            plat = System(system)
            platform["name"] = plat.system
            platform["manufacturer"] = plat.manufacturer.lower()
            platform["type"] = plat.platform_type.lower()
            platform["year"] = plat.year
            platforms.append(dict(platform))

        if sort:
            final_systems = sorted(platforms, key=lambda platform: (
                platform["manufacturer"],
                platform["type"],
                platform["year"]))
        else:
            final_systems = platforms
        xml = os.path.join(self.hs_path, "Databases", "Main Menu", "Main Menu.xml")
        try:
            shutil.copy(xml, "{}_backup_{}.xml".format(xml, time.strftime("%Y%m%d")))
            root = ET.Element("menu")
            for name in final_systems:
                ET.SubElement(root, "game", name=name["name"])
        except FileNotFoundError:
            msg = "System Menu does not exist"
            logger.info(msg)
            root = ET.Element("menu")
            for name in final_systems:
                ET.SubElement(root, "game", name=name["name"])

        pretty = self.prettify(root)
        with open(xml, mode="w") as xml:
            xml.write(pretty)

    def _create_hs_database(self):
        msg = "Creating database of found ROMs for {}".format(self.system)
        logger.info(msg)
        src_db = os.path.join(self.rl_path, "RocketLauncherUI", "Databases", self.system, "{}.xml".format(self.system))
        hs_db = Databases(system=self.system)
        db = hs_db.audit(files_to_audit=os.path.join(self.rom_path, self.system), db=src_db, audit_type="rom")
        have = [rom for rom in db if rom["rom"]]
        dst_db = os.path.join(self.db_path, "{}.xml".format(self.system))
        if not os.path.isdir(os.path.dirname(dst_db)):
            os.makedirs(os.path.dirname(dst_db))
        msg = "Creating database of found ROMs for {}".format(self.system)
        logger.info(msg)
        hs_db.write_rom_xml(games=have, xml=dst_db)

    def _write_genre_xml(self, genre):
        # Audit the ROMS and only include the ones we have
        src_db = os.path.join(self.rl_path, "RocketLauncherUI", "Databases", self.system, "{}.xml".format(self.system))
        hs_db = Databases(system=self.system)
        db = hs_db.audit(files_to_audit=os.path.join(self.rom_path, self.system), db=src_db, audit_type="rom")
        have = [rom for rom in db if rom["rom"]]

        # Format the naming of the Genres
        if genre == "Mini-":
            xml = os.path.join(self.hs_path, "Databases", self.system, "Mini-Games.xml")
            genre_name = "Mini-Games"
        else:
            xml = os.path.join(self.hs_path, "Databases", self.system, genre + " Games.xml")
            genre_name = "{} Games".format(genre)
        output = []

        # Cycle thru the ROMs and match the Genre to current
        for rom in have:
            if not rom["genre"]:
                msg = "{} does not have a Genre assigned".format(rom["name"])
                logger.debug(msg)
            else:
                if genre == rom["genre"]:
                    output.append(rom)
        if not output:
            msg = "No ROMS match {} genre".format(genre)
            logger.debug(msg)
            return genre
        else:
            hs_db.write_rom_xml(games=output, xml=xml, listname="{} {}".format(self.system, genre_name))
            return ""

    def _create_genres(self):

        categories = ("Action", "Adventure", "Ball & Paddle", "Beat-'Em-Up",
                      "Biking", "Board", "Breakout", "Card Battle", "Casino", "Climbing",
                      "Compilation", "Driving", "Educational", "Favorites", "Fighter",
                      "Flying", "Game Show", "Gun", "Mahjong", "Mature", "Maze",
                      "Mini-", "Miscellaneous", "Motorcycle", "Multimedia", "Party", "Pinball",
                      "Platform", "Puzzle", "Quiz", "Rhythm", "Role-Playing",
                      "Shoot-'Em-Up", "Shooter", "Simulation", "Spinner", "Strategy", "Surfing",
                      "Tabletop", "Trackball", "Utility", "Virtual Life", "Wakeboarding", "Water",
                      "Sports",
                      "Baseball", "Basketball", "Bowling", "Boxing", "Cricket", "Fishing", "Football",
                      "Futuristic", "Golf", "Handball", "Hockey", "Horse Racing", "Hunting", "Olympic",
                      "Pool and Dart", "Rugby", "Skateboarding", "Skating", "Skiing",
                      "Snowboarding", "Soccer", "Surfing", "Tennis", "Track & Field", "Volleyball",
                      "Wrestling")
        non_matches = []  # Holder for any Genre that doesn't match in the ROM set
        for i in categories:
            no_match = self._write_genre_xml(i)
            msg = "Creating Genre XML for {} genre".format(i)
            logger.info(msg)
            non_matches.append(no_match)

        # Build the genre.xml menu list
        root = ET.Element("menu")
        ET.SubElement(root, "game", name="All Games")
        for genre in categories:
            if genre not in non_matches:
                if genre == "Mini-":
                    ET.SubElement(root, "game", name=genre + "Games")
                else:
                    ET.SubElement(root, "game", name=genre + " Games")
        xml = os.path.join(self.hs_path, "Databases", self.system, "genre.xml")
        pretty = self.prettify(root)
        with open(xml, mode="w") as xml:
            xml.write(pretty)

    def new_system(self, link=False):
        self._media_directories()
        self._system_ini()
        self._write_hs_menu(sort=True)
        self._create_hs_database()
        self._create_genres()
        self._copy_genre_art(link)

    # Remove System

    def remove_system(self, remove_media=False):
        """
        "remove_system" removes the system from HyperSpin, it's database, default
        settings and optionally it's media

        Args:
            "remove_media" (optional, default=False): Removes associated media from RocketLauncher's Media directory

        Returns:
            None

        Raises:
            None
        """
        msg = "Removing {} from Main Menu".format(self.system)
        logger.info(msg)
        settings_ini = os.path.join(self.hs_path, "Settings", self.system + ".ini")
        if os.path.isfile(settings_ini):
            os.remove(settings_ini)
        if remove_media:
            msg = "Removing Media files from {}".format(self.system)
            logger.info(msg)
            remove = [self.db_path, self.media_path]
        else:
            remove = [self.db_path]
        for i in remove:
            if os.path.exists(i):
                msg = "Removing {} and all items".format(i)
                logger.debug(msg)
                shutil.rmtree(i)
        self._write_hs_menu(remove=True)

    # Get rid of un-necessary HyperSpin Stuff

    def _remove_junk(self):
        for system in self.default_systems:
            hs = HyperSpin(system=system)
            hs.remove_system(remove_media=True)

        dirs = [os.path.join(self.hs_path, "Emulators"), os.path.join(self.hs_path, "Modules")]
        for i in dirs:
            if os.path.exists(i):
                msg = "Removing {} and all items".format(i)
                logger.debug(msg)
                shutil.rmtree(i)

    # Update systems from RocketLauncher

    def build_systems_from_rl(self):
        rl = RocketLauncher(self.system)
        systems = rl.read_menu()
        for system in systems:
            hs = HyperSpin(system["name"])
            hs.new_system(link=True)


if __name__ == "__main__":
    nes = "Nintendo Entertainment System"
    atari = "Atari Jaguar"
    hs = HyperSpin(atari)
    # hs.new_system(link=True)
    # hs.build_systems_from_rl()
