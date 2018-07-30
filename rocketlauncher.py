import logging
import time
import os
import shutil
import configparser
import xml.etree.cElementTree as ET

from hyperspin import Databases, HyperList
from general import Arcade, Compressor
from models.system import System

TIME_STAMP = time.strftime(" %Y%m%d")

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


class RocketLauncher(Databases, HyperList, System):

    def __init__(self, system):
        Databases.__init__(self, system)
        HyperList.__init__(self, system)
        System.__init__(self, system)

        self.system = system

        self.full_sys = {"name": self.system,
                         "type": self.platform_type,
                         "year": self.year,
                         "manufacturer": self.manufacturer,
                         "enabled": "true"}

        # Paths
        self.rl_ui_path = os.path.join(self.rl_path, "RocketLauncherUI")
        self.settings_path = os.path.join(self.rl_path, "Settings", self.system)
        self.modules_path = os.path.join(self.rl_path, "Modules")

        # Media
        self.media_path = os.path.join(self.rl_path, "Media")
        self.artwork_path = os.path.join(self.media_path, "Artwork", self.system)
        self.backgrounds_path = os.path.join(self.media_path, "Backgrounds", self.system)
        self.bezels_path = os.path.join(self.media_path, "Bezels", self.system)
        self.fade_path = os.path.join(self.media_path, "Fade", self.system)
        self.logos_path = os.path.join(self.media_path, "Logos", self.system)
        self.music_path = os.path.join(self.media_path, "Music", self.system)
        self.video_path = os.path.join(self.media_path, "Videos", self.system)
        self.media_paths = [self.artwork_path, self.backgrounds_path, self.bezels_path, self.fade_path,
                            self.logos_path, self.music_path, self.video_path]

        # UI
        self.db_path = os.path.join(self.rl_ui_path, "Databases", self.system)
        self.icon_path = os.path.join(self.rl_ui_path, "Media", "Icons")
        self.ui_logo_path = os.path.join(self.rl_ui_path, "Media", "Logos")
        self.ui_settings_path = os.path.join(self.rl_ui_path, "Settings")

    # System Level Methods
    def write_emulator_ini(self):
        """
        "write_emulator_ini" is a method that will set the emulator and relative path for
        RocketLauncher's Emulator config ini for the system

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        # Create Directory if it does not exist
        if not os.path.exists(self.settings_path):
            os.makedirs(self.settings_path)
        # Read/Create the config file
        ini = os.path.join(self.settings_path, "Emulators.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        if not config.has_section("ROMS"):
            msg = "Setting the {}'s Emulator and Paths".format(self.system)
            logger.info(msg)
            config.add_section("ROMS")
        else:
            msg = "Updating the {}'s Emulator and Paths".format(self.system)
            logger.info(msg)
        # Set values for emulator and ROM path
        config.set("ROMS", "Default_Emulator", self.emulator)
        config.set("ROMS", "Rom_Path", os.path.relpath(os.path.join(self.rom_path, self.system), self.rl_path))

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)
        # Create ROM path if it does not exist
        if not os.path.exists(os.path.join(self.rom_path, self.system)):
            os.makedirs(os.path.join(self.rom_path, self.system))

    # Global Level Methods
    def _set_defaults(self):
        """
        "set_defaults" is a method that will set some of the default extraction paths
        and enable Pause globally
        potentially could be used to set other values in Global RocketLauncher.ini configuration
        file

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        msg = "Setting Defaults"
        logger.info(msg)
        # Read/Create the config file
        ini = os.path.join(self.rl_path, "Settings", "Global RocketLauncher.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        if not config.has_section("7z"):
            config.add_section("7z")

        if not config.has_section("Pause"):
            config.add_section("Pause")
        # Set values for extract path and Pause
        config.set("7z", "7z_Extract_Path", os.path.relpath(self.temp_path, self.rl_path))
        config.set("7z", "7z_Attach_System_Name", "true")
        config.set("7z", "7z_Delete_Temp", "false")
        config.set("Pause", "Pause_Enabled", "true")

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    # RocketLauncher UI Methods
    def _set_rocket_launcher_ui_ini(self):
        """
        "set_rocket_launcher_ui_ini" is a method that will set the Notepad++ path
        potentially could be used to set other values in RocketLauncherUI.ini configuration
        file

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        msg = "Setting Notepad++ location"
        logger.info(msg)
        # Read/Create the config file
        ini = os.path.join(self.ui_settings_path, "RocketLauncherUI.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)
        if not config.has_section("Paths"):
            config.add_section("Paths")
        # Set path for the Notepad++ executable
        config.set("Paths", "Module_Editor_Path", self.notepad)

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    def write_frontends_ini(self, fe_name, executable, default=False):
        """
        "write_frontends_ini" is a method that will add/modify a Front End configuration
        in the Frontends.ini config file

        Args:
            fe_name (required): Front End Name
            executable (required): full path and Executable of the Front End
            default (optional, default=False): Set as the Default Front End in RocketLauncher

        Returns:
            None

        Raises:
            None
        """
        def_ini = os.path.join(self.ui_settings_path, "Frontends (Example).ini")
        ini = os.path.join(self.ui_settings_path, "Frontends.ini")
        # Copy the example config file if it does not exist
        if not os.path.exists(ini):
            shutil.copy(def_ini, ini)
        # Read/Create the config file
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)
        # Set the frontend as default if desired
        if default:
            msg = "Setting {} as Default Frontend".format(fe_name)
            logger.info(msg)
            config.set("Settings", "Default_Frontend", fe_name)

        if not config.has_section(fe_name):
            msg = "Adding {} Frontend".format(fe_name)
            logger.info(msg)
            config.add_section(fe_name)
        else:
            msg = "Updating {} Frontend".format(fe_name)
            logger.info(msg)
        # Set options
        config.set(fe_name, "Path", os.path.relpath(executable, self.rl_ui_path))
        config.set(fe_name, "RLUI_Plugin", "Auto")
        config.set(fe_name, "RL_Plugin", "Default")
        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=False)

    def read_menu(self):
        """
        "read_menu" is a method that reads the Systems.xml database, a.k.a. the Main Menu

        Args:
            self

        Returns:
            a list of dictionaries of Systems and system info

        Raises:
            None
        """
        msg = "Reading Rocket Launcher Systems XML database ..."
        logger.info(msg)
        xml = os.path.join(self.rl_ui_path, "Databases", "Systems.xml")
        tree = ET.parse(xml)
        doc = tree.getroot()
        system = {}
        systems = []
        for child in doc:
            system["name"] = child.get("name")
            system["type"] = child.get("type")
            system["year"] = child.get("year")
            system["manufacturer"] = child.get("manufacturer")
            system["enabled"] = child.get("enabled")
            systems.append(dict(system))
        return systems

    def write_menu(self, systems):
        """
        "write_menu" is a method that adds a system to the Systems.xml database, a.k.a. the Main Menu

        Args:
            systems (required): List of Dictionaries for the Menu

        Returns:
            None

        Raises:
            None
        """
        xml = os.path.join(self.rl_ui_path, "Databases", "Systems.xml")
        try:
            shutil.copy(xml, "{}_backup_{}.xml".format(xml, TIME_STAMP))
            root = ET.Element("systems")
            for name in systems:
                ET.SubElement(root, "system",
                              name=name["name"],
                              type=name["type"],
                              year=name["year"],
                              manufacturer=name["manufacturer"],
                              enabled=name["enabled"])
        except FileNotFoundError:
            msg = "System Menu does not exist"
            logger.info(msg)
            root = ET.Element("systems")
            ET.SubElement(root, "system",
                          name=self.full_sys["name"],
                          type=self.full_sys["type"],
                          year=self.full_sys["year"],
                          manufacturer=self.full_sys["manufacturer"],
                          enabled=self.full_sys["enabled"])

        fe = Arcade()
        pretty = fe.prettify(root)
        with open(xml, mode="w") as xml:
            xml.write(pretty)

    # Helper Methods
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
        cf = Compressor(self.rocket_launcher_archive)
        cf.extract_all(self.rl_path, password="www.rlauncher.com")

        cf = Compressor(self.rocket_launcher_media_archive)
        cf.extract_all(self.rl_path)

    def _copy_default_settings(self):
        """
        "copy_default_settings" is a method that copies some of the sample configuration
        files from RocketLauncher to their respective configuration file.

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        msg = "Copying Default Settings"
        logger.info(msg)
        src = os.path.join(self.rl_path, "Settings", "Global Emulators (Example).ini")
        dst = os.path.join(self.rl_path, "Settings", "Global Emulators.ini")
        shutil.copy(src, dst)

        src = os.path.join(self.rl_path, "RocketLauncherUI", "Settings", "RocketLauncherUI (Example).ini")
        dst = os.path.join(self.rl_path, "RocketLauncherUI", "Settings", "RocketLauncherUI.ini")
        shutil.copy(src, dst)

        src = os.path.join("settings", "Global RocketLauncher.ini")
        dst = os.path.join(self.rl_path, "Settings", "Global RocketLauncher.ini")
        shutil.copy(src, dst)

    # Install RocketLauncher from archive
    def install(self):
        """
        "install" is a method that unzips the archives and sets some defaults

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        a = Arcade()
        a.create_arcade()
        self._extract_archive()
        self._copy_default_settings()
        self._set_defaults()
        self._set_rocket_launcher_ui_ini()
        msg = "Launch RocketLauncherUI and perfrom an update!!!!!!!!!!!!!"
        logger.info(msg)

    def new_system(self):
        """
        "new_system" that creates a new menu item in RocketLauncher, it's database and
        default settings

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        msg = "Adding {} to the RocketLauncher Menu".format(self.system)
        logger.info(msg)
        self.download_db()  # Method from hyperspin.py, HyperList Class
        self.write_emulator_ini()
        try:
            systems = self.read_menu()
        except:
            systems =[]
        syss = [sys["name"] for sys in systems]
        if self.system in syss:
            msg = "{} is already in RocketLauncher Menu and will not be added".format(self.system)
            logger.info(msg)
        else:
            systems.append(self.full_sys)
        self.write_menu(systems)

    def remove_system(self, remove_media=False):
        """
        "remove_system" removes the system from RocketLauncher, it's database, default
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
        if remove_media:
            msg = "Removing Media files from {}".format(self.system)
            logger.info(msg)
            remove = [self.db_path, self.settings_path] + self.media_paths
        else:
            remove = [self.db_path, self.settings_path]
        for i in remove:
            if os.path.exists(i):
                msg = "Removing {} and all items".format(i)
                logger.debug(msg)
                shutil.rmtree(i)
        systems = self.read_menu()
        systems = [d for d in systems if d.get('name') != self.system]
        self.write_menu(systems)


if __name__ == "__main__":
    nes = "Nintendo Entertainment System"
    snes = "Super Nintendo Entertainment System"
    atari = "Atari 2600"
    sega = "Sega Genesis"
    rl = RocketLauncher(snes)
    rl.install()
    systems = [nes, snes, atari, sega]
    for system in systems:
        rl = RocketLauncher(system)
        rl.new_system()
    # rl.remove_system(remove_media=False)

