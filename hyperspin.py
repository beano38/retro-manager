import os
import shutil
import logging
import configparser
import time
import math
import xml.etree.cElementTree as ET

from PIL import Image

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


class HyperSpin(Arcade, System):

    def __init__(self, system=None):
        Arcade.__init__(self)
        System.__init__(self, system)

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
        """
        "_settings_ini" sets default values for the global settings config file for
        HyperSpin - Settings.ini

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        msg = "HS: Setting Settings.ini Defaults"
        logger.info(msg)
        ini = os.path.join(self.hs_path, "Settings", "Settings.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        # Set RocketLauncher as the main launcher for HyperSpin
        config.set("Main", "Hyperlaunch_Path", os.path.join(self.rl_path, "RocketLauncher.exe"))

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    def _main_menu_ini(self):
        """
        "_main_menu_ini" sets default values for the way the main menu looks in HyperSpin

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        msg = "HS: Setting Main Menu Defaults"
        logger.info(msg)
        ini = os.path.join(self.hs_path, "Settings", "Main Menu.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        config.set("wheel", "alpha", "1")
        config.set("wheel", "style", "horizontal")
        config.set("wheel", "vert_wheel_position", "center")

        config.set("wheel", "norm_large", "256")
        config.set("wheel", "norm_small", "200")
        config.set("wheel", "horz_large", "250")
        config.set("wheel", "horz_small", "125")

        config.set("wheel", "horz_wheel_y", "575")

        config.set("sounds", "game_sounds", "false")
        config.set("sounds", "wheel_click", "false")

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    def _rename_genre_art(self):
        """
        "_rename_genre_art" renames some of the artwork to be consistent with the Genre labels,
        uses MAME as it's default source of genre art

        Args:
            "action" (optional, default=copy): Sets the action to take, (copy, move, link)

        Returns:
            None

        Raises:
            None
        """

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
        "extract_archive" is a method that unzips the install archives for HyperSpin

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
        rl = RocketLauncher(system="Nintendo Entertainment System")
        exe = os.path.join(self.hs_path, "HyperSpin.exe")
        rl.write_frontends_ini(fe_name="HyperSpin", executable=exe)
        self._remove_junk()

    # New System helper methods

    def _media_directories(self):
        """
        "_media_directories" creates the media directories for the HyperSpin system

        Args:
            self

        Returns:
            None

        Raises:
            None
        """

        sound_path = os.path.join(self.media_path, "Sound")
        theme_path = os.path.join(self.media_path, "Themes")
        video_path = os.path.join(self.media_path, "Video")

        dirs = [self.artwork1_path, self.artwork2_path, self.artwork3_path, self.artwork4_path, self. backgrounds_path,
                self.genre_wheel_path, self.genre_backgrounds_path, self.letters_path, self.other_path,
                self.particle_path, self.special_path, self.wheel_path, sound_path, theme_path, video_path]

        for path in dirs:
            if not os.path.exists(path):
                os.makedirs(path)

    def _system_ini(self):
        """
        "_system_ini" sets default values for the way the System menu looks in HyperSpin and sets the
        ROM path and extensions

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
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
        config.set("wheel", "alpha", "1")
        config.set("wheel", "style", "vertical")

        config.set("wheel", "y_rotation", "center")

        config.set("wheel", "norm_large", "256")
        config.set("wheel", "norm_small", "200")
        config.set("wheel", "vert_large", "300")
        config.set("wheel", "vert_small", "150")

        config.set("wheel", "horz_wheel_y", "575")

        config.set("video defaults", "path", os.path.join(self.media_path, "Video"))

        config.set("sounds", "game_sounds", "false")
        config.set("sounds", "wheel_click", "false")

        config.set("navigation", "remove_info_wheel", "true")
        config.set("navigation", "remove_info_text", "true")

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    def _copy_genre_art(self, action):
        """
        "_copy_genre_art" copies default Genre art, backgrounds and wheels to the new system

        Args:
            self
            action (required): Sets the action to take, (copy, link)

        Returns:
            None

        Raises:
            None
        """
        # If Linking files, remove the old file before appending the new symlinks
        links = []
        batch_file = os.path.join(self.temp_path, "{} Genre Links run as Admin.bat".format(self.system))
        if os.path.isfile(batch_file):
            os.remove(batch_file)

        # Set paths
        src_path = os.path.join(self.hs_path, "Media", "MAME", "Images", "Genre")
        src_logos = os.listdir(os.path.join(src_path, "Wheel"))
        src_bgs = os.listdir(os.path.join(src_path, "Backgrounds"))

        dirs = [self.genre_backgrounds_path, self.genre_wheel_path]

        wheels = []
        backgrounds = []
        output = {}

        # We will use the MAME assets as our base
        if not self.system == "MAME":
            for directory in dirs:
                msg = "Setting Paths for {} directory".format(directory)
                logger.info(msg)
                if directory == self.genre_backgrounds_path:
                    for fname in src_bgs:
                        output["src"] = os.path.join(src_path, "Backgrounds", fname)
                        output["dst"] = os.path.join(self.genre_backgrounds_path, fname)
                        backgrounds.append(dict(output))
                elif directory == self.genre_wheel_path:
                    for fname in src_logos:
                        output["src"] = os.path.join(src_path, "Wheel", fname)
                        output["dst"] = os.path.join(self.genre_wheel_path, fname)
                        wheels.append(dict(output))
        else:
            msg = "{} is not a valid system".format(self.system)
            logger.debug(msg)

        if action == "link" or action == "copy":
            self._do_media(wheels, action=action, batch_file=batch_file)
            self._do_media(backgrounds, action=action, batch_file=batch_file)
        elif action == "move":
            self._do_media(wheels, action="copy", batch_file=batch_file)
            self._do_media(backgrounds, action="copy", batch_file=batch_file)
        else:
            msg = "{} action is not permitted for Genre Art"
            logger.debug(msg)

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
            self
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
        elif self.system not in systems:
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

        # Sort by Manufacturer, then by Platform type, then by Year
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
        """
        "_create_hs_database" creates the database of ROMs for the system in HyperSpin.
        Filters the RocketLauncher Database for available ROMs.  RocketLauncher Database is the master
        database

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        msg = "Creating database of found ROMs for {}".format(self.system)
        logger.info(msg)
        # Get the database from RocketLauncher
        src_db = os.path.join(self.rl_path, "RocketLauncherUI", "Databases", self.system, "{}.xml".format(self.system))
        hs_db = Databases(system=self.system)
        db = hs_db.audit(files_to_audit=os.path.join(self.rom_path, self.system), db=src_db, audit_type="rom")

        # Audit for available ROMs
        have = [rom for rom in db if rom["rom"]]
        dst_db = os.path.join(self.db_path, "{}.xml".format(self.system))
        if not os.path.isdir(os.path.dirname(dst_db)):
            os.makedirs(os.path.dirname(dst_db))
        msg = "Creating database of found ROMs for {}".format(self.system)
        logger.info(msg)

        # Write the database to the system
        hs_db.write_rom_xml(games=have, xml=dst_db)

    def _write_genre_xml(self, genre):
        """
        "_write_genre_xml" writes genre databases for available genres

        Args:
            self
            genre: name of genre to create the database for

        Returns:
            genre

        Raises:
            None
        """
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
        """
        "_create_genres" creates genre databases for ROMs matching the genre label in the database

        Args:
            self

        Returns:
            None

        Raises:
            None
        """

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
            # Write the specific genre database
            no_match = self._write_genre_xml(i)
            msg = "Creating Genre XML for {} genre".format(i)
            logger.info(msg)
            # if the genre exists, add to the list to build the genre.xml
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

    def resize_width(self, src, dst, width):
        img = Image.open(src)
        width_percent = width / img.size[0]
        height = math.ceil(img.size[1] * width_percent)
        new = img.resize((width, height), Image.ANTIALIAS)
        new.save(dst)

    def resize_width(self, src, dst, width):
        img = Image.open(src)
        width_percent = width / img.size[0]
        height = math.ceil(img.size[1] * width_percent)
        new = img.resize((width, height), Image.ANTIALIAS)
        new.save(dst)

    def _do_media(self, files, action, batch_file):
        """
        "_main_menu_ini" sets default values for the way the main menu looks in HyperSpin

        Args:
            self
            files (required): dictionary of file with source and destination
            action (required): Sets the action to take, (copy, move, link)

        Returns:
            None

        Raises:
            None
        """

        links = []
        for f in files:
            if action == "copy":
                if not os.path.isfile(f["dst"]):
                    shutil.copy(src=f["src"], dst=f["dst"])
            elif action == "move":
                if not os.path.isfile(f["dst"]):
                    shutil.copy(src=f["src"], dst=f["dst"])
            elif action == "link":
                if not os.path.isfile(f["dst"]):
                    link = 'mklink "{}" "{}"\n'.format(f["dst"], f["src"])
                    links.append(link)
            elif action == "resize":
                if not os.path.isfile(f["dst"]):
                    try:
                        self.resize_width(src=f["src"], dst=f["dst"], width=180)
                    except OSError:
                        msg = "Error with file {}".format(f["src"])
                        logger.debug(msg)
            else:
                msg = "{} action is not permitted".format(action)
                logger.debug(msg)

        if len(links) > 0:
            with open(batch_file, mode="a") as f:
                for link in links:
                    f.write(link)

    def _set_up_media(self, action="copy", three_d=False):
        """
        "set_up_media" copies any EmuMovies content into the appropriate folders
        in HyperSpin

        Args:
            action (optional, default=copy): Sets the action to take, (copy, move, link)
            three_d (optional, default=False): If 3D art is required, set to True

        Returns:
            None

        Raises:
            None
        """
        xml = os.path.join(self.db_path, self.system + ".xml")

        hs = Databases(system=self.system)
        header, db = hs.read_system_xml(db=xml)

        # Just worried about the ROM name in the database
        names = [name["name"] for name in db]

        batch_file = os.path.join(self.temp_path, "{} HS Media Links run as Admin.bat".format(self.system))
        if os.path.isfile(batch_file):
            os.remove(batch_file)

        # Set Paths
        src_path = os.path.join(self.emu_movies_path, self.emu_movies_name)
        cart = os.path.join(src_path, "Cart")
        box = os.path.join(src_path, "Box")
        three_d_cart = os.path.join(src_path, "Cart_3D")
        three_d_box = os.path.join(src_path, "Box_3D")
        wheel = os.path.join(src_path, "Logos")
        video1 = os.path.join(src_path, "Video_MP4_HI_QUAL")
        video2 = os.path.join(src_path, "Video_MP4")
        theme = os.path.join(src_path, "Video_Themes_MP4")
        sys_intro = os.path.join(src_path, "Video_System_Intro_MP4")

        dirs = [three_d_cart, three_d_box, cart, box, wheel, video1, video2, theme]

        # Holders for adding the media content to
        artwork3 = []
        artwork4 = []
        wheels = []
        videos = []

        themes = []
        output = {}

        for directory in dirs:
            if os.path.exists(directory):
                msg = "Setting Paths for {} directory".format(directory)
                logger.info(msg)
                media = os.listdir(directory)
                for fname in media:
                    f, ext = os.path.splitext(fname)
                    if f in names and directory == three_d_cart and three_d:
                        output["src"] = os.path.join(directory, fname)
                        output["dst"] = os.path.join(self.artwork4_path, fname)
                        artwork4.append(dict(output))
                    elif f in names and directory == three_d_box and three_d:
                        output["src"] = os.path.join(directory, fname)
                        output["dst"] = os.path.join(self.artwork3_path, fname)
                        artwork3.append(dict(output))
                    elif f in names and directory == cart and not three_d:
                        output["src"] = os.path.join(directory, fname)
                        output["dst"] = os.path.join(self.artwork4_path, fname)
                        artwork4.append(dict(output))
                    elif f in names and directory == box and not three_d:
                        output["src"] = os.path.join(directory, fname)
                        output["dst"] = os.path.join(self.artwork3_path, fname)
                        artwork3.append(dict(output))
                    elif f in names and directory == wheel:
                        output["src"] = os.path.join(directory, fname)
                        output["dst"] = os.path.join(self.wheel_path, fname)
                        wheels.append(dict(output))
                    elif f in names and directory == video1 or directory == video2:
                        output["src"] = os.path.join(directory, fname)
                        output["dst"] = os.path.join(self.video_path, fname)
                        videos.append(dict(output))
                    elif f in names and directory == theme:
                        output["src"] = os.path.join(directory, fname)
                        output["dst"] = os.path.join(self.themes_path, fname)
                        themes.append(dict(output))
                    else:
                        output["src"] = ""
                        output["dst"] = ""
            else:
                msg = "{} is not a directory for {}".format(directory, self.system)
                logger.debug(msg)

        intro_src = os.path.join(src_path, "Video_System_Intro_MP4", "system_intro.mp4")
        logo_src = os.path.join(src_path, "System_Logo", "system_logo.png")
        intro_dst = os.path.join(self.hs_path, "Media", "Main Menu", "Video", "{}.mp4".format(self.system))
        logo_dst = os.path.join(self.hs_path, "Media", "Main Menu", "Images", "Wheel", "{}.png".format(self.system))
        rl_logo_src = os.path.join(self.rl_path, "Media", "Logos", self.system, "_default", "{}.png".format(self.system))

        sys_medias = []
        sys_media = {}
        if os.path.isfile(intro_src):
            sys_media["src"] = intro_src
            sys_media["dst"] = intro_dst
            sys_medias.append(dict(sys_media))
        if os.path.isfile(logo_src):
            sys_media["src"] = logo_src
            sys_media["dst"] = logo_dst
            sys_medias.append(dict(sys_media))
        elif os.path.isfile(rl_logo_src):
            sys_media["src"] = rl_logo_src
            sys_media["dst"] = logo_dst
            sys_medias.append(dict(sys_media))
        if len(sys_medias) > 0:
            self._do_media(sys_medias, action=action, batch_file=batch_file)

        msg = "Re-sizing {}'s Box Art".format(self.system)
        logger.info(msg)
        self._do_media(artwork3, action="resize", batch_file=batch_file)
        msg = "Re-sizing {}'s Game Media".format(self.system)
        logger.info(msg)
        self._do_media(artwork4, action="resize", batch_file=batch_file)
        self._do_media(wheels, action=action, batch_file=batch_file)
        self._do_media(videos, action=action, batch_file=batch_file)
        # self._do_media(themes, action=action, batch_file=batch_file)

    def _build_theme(self):
        msg = "Building Main Menu Theme for {}".format(self.system)
        logger.info(msg)
        main_bg = os.path.join("assets", "background.png")
        main_theme = os.path.join("assets", "main theme.xml")
        main_console = os.path.join("assets", "consoles", "{}.png".format(self.system))
        main_theme_dst = os.path.join(self.hs_path, "Media", "Main Menu", "Themes")

        temp_dir = os.path.join(main_theme_dst, self.system)

        if not os.path.isdir(temp_dir):
            os.makedirs(os.path.join(temp_dir))
        if os.path.isfile(main_bg):
            shutil.copy(main_bg, os.path.join(temp_dir, "Background.png"))
        if os.path.isfile(main_theme):
            shutil.copy(main_theme, os.path.join(temp_dir, "Theme.xml"))
        if os.path.isfile(main_console):
            shutil.copy(main_console, os.path.join(temp_dir, "Artwork2.png"))
        if os.path.isfile(os.path.join(main_theme_dst, "{}.zip".format(self.system))):
            os.remove(os.path.join(main_theme_dst, "{}.zip".format(self.system)))

        c = Compressor(src_file=temp_dir)
        c.compress_dir(dst_file=os.path.join(main_theme_dst, "{}.zip".format(self.system)))

        msg = "Building System Theme for {}".format(self.system)
        logger.info(msg)

        system_bg = os.path.join("assets", "system background.png")
        system_theme = os.path.join("assets", "system theme.xml")
        system_logo = os.path.join(self.hs_path, "Media", "Main Menu", "Images", "Wheel", "{}.png".format(self.system))
        system_theme_dst = os.path.join(self.hs_path, "Media", self.system, "Themes")

        temp_sys_dir = os.path.join(system_theme_dst, "_Temp")

        if not os.path.isdir(temp_sys_dir):
            os.makedirs(os.path.join(temp_sys_dir))
        if os.path.isfile(system_bg):
            shutil.copy(system_bg, os.path.join(temp_sys_dir, "Background.png"))
        if os.path.isfile(system_theme):
            shutil.copy(system_theme, os.path.join(temp_sys_dir, "Theme.xml"))
        if os.path.isfile(system_logo):
            shutil.copy(system_logo, os.path.join(temp_sys_dir, "Artwork1.png"))
        if os.path.isfile(os.path.join(system_theme_dst, "default.zip".lower())):
            os.remove(os.path.join(system_theme_dst, "default.zip".lower()))

        c = Compressor(src_file=temp_sys_dir)
        c.compress_dir(dst_file=os.path.join(system_theme_dst, "Default.zip"))

    def new_system(self, action="copy", three_d=False):
        self._media_directories()
        self._system_ini()
        self._write_hs_menu(sort=True)
        self._create_hs_database()
        self._create_genres()
        self._copy_genre_art(action=action)
        self._set_up_media(action=action, three_d=three_d)
        self._build_theme()

    # Remove System

    def remove_system(self, remove_media=False):
        """
        "remove_system" removes the system from HyperSpin, it's database, default
        settings and optionally it's media

        Args:
            self
            remove_media (optional, default=False): Removes associated media from RocketLauncher's Media directory

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
        # Remove the system from the Main Menu
        self._write_hs_menu(remove=True)

    # Get rid of un-necessary HyperSpin Stuff

    def _remove_junk(self):
        """
        "_remove_junk" removes the extra items no longer needed since RocketLauncher is the
        launcher.  Also removes the default systems since they are outdated

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        # Remove the default systems
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

    def build_systems_from_rl(self, action="link", three_d=False):
        """
        "build_systems_from_rl" builds the systems that exist in RocketLauncher into HyperSpin

        Args:
            self
            link (optional, default=False): Link the genre artwork

        Returns:
            None

        Raises:
            None
        """
        rl = RocketLauncher(self.system)
        systems = rl.read_menu()
        hs_systems = self._read_hs_menu()

        for system in systems:
            if system["name"] not in hs_systems:
                hs = HyperSpin(system["name"])
                hs.new_system(action, three_d)
            else:
                msg = "System {} is in RocketLauncher and HyperSpin already".format(system["name"])
                logger.info(msg)

    # Update system
    def update_system(self, action="Copy", three_d=False):
        self._system_ini()
        self._create_hs_database()
        self._create_genres()
        self._set_up_media(action=action, three_d=three_d)
        self._build_theme()


if __name__ == "__main__":
    nes = "Nintendo 64"
    atari = "Atari 2600"
    hs = HyperSpin("Sega 32X")
    # hs.new_system(action="link", three_d=False)
    hs.remove_system(remove_media=True)
    # hs.build_systems_from_rl(action="link", three_d=False)

