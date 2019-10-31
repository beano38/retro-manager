import logging
import time
import os
import sys
import shutil
import configparser
import xml.etree.cElementTree as ET
import concurrent.futures

from utilities import Databases, HyperList
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

# logger.addHandler(file_handler)
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
        self.controller_path = os.path.join(self.media_path, "Controller", self.system)
        self.fade_path = os.path.join(self.media_path, "Fade", self.system)
        self.guides_path = os.path.join(self.media_path, "Guides", self.system)
        self.logos_path = os.path.join(self.media_path, "Logos", self.system)
        self.manuals_path = os.path.join(self.media_path, "Manuals", self.system)
        self.multi_path = os.path.join(self.media_path, "MultiGame", self.system)
        self.music_path = os.path.join(self.media_path, "Music", self.system)
        self.video_path = os.path.join(self.media_path, "Videos", self.system)

        self.media_paths = [self.artwork_path, self.backgrounds_path, self.bezels_path, self.controller_path,
                            self.fade_path, self.guides_path, self.logos_path, self.manuals_path, self.multi_path,
                            self.music_path, self.video_path]

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

    def global_emulators_add_ext(self):
        """
        "global_emulators_add_ext" is a method that will add extension parameters in the
        Global Emulators.ini file

        Args:
            self

        Returns:
            None

        Raises:
            None
        """

        # Read/Create the config file
        ini = os.path.join(self.rl_path, "Settings", "Global Emulators.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        compressed_exts = ["7z", "zip", "rar"]
        if config.get(self.emulator, "Rom_Extension") != "":
            extensions = "|".join(
                sorted(set(config.get(self.emulator, "Rom_Extension").split("|") + compressed_exts + self.extensions)))
        else:
            extensions = "|".join(sorted(set(compressed_exts + self.extensions)))
        config.set(self.emulator, "Rom_Extension", extensions)

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

        pretty = self.prettify(root)
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
        msg = "Launch RocketLauncherUI and perform an update!!!!!!!!!!!!!"
        logger.info(msg)

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
            remove = [self.db_path, self.settings_path] + self.media_paths + [os.path.join(self.rom_path, self.system)]
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
        response = self._download_db()
        if response:
            # self.update_db()  # Method from utilities.py, HyperList Class
            self.write_emulator_ini()
            try:
                systems = self.read_menu()
            except:
                systems = []
            syss = [sys["name"] for sys in systems]
            if self.system in syss:
                msg = "{} is already in RocketLauncher Menu and will not be added".format(self.system)
                logger.info(msg)
            else:
                systems.append(self.full_sys)
            self.write_menu(systems)
        else:
            msg = "No database found from HyperList for {}, consider building one".format(self.system)
            logging.debug(msg)
            sys.exit(msg)

    # RocketLauncher Media
    def set_up_media(self, action="copy"):
        """
        "set_up_media" copies any EmuMovies content into the appropriate folders
        in RocketLauncher, for Pause, Fade and etc.

        Args:
            "action" (optional, default=copy): Sets the action to take, [copy, move, link]

        Returns:
            None

        Raises:
            None
        """
        xml = os.path.join(self.rl_path, "RocketLauncherUI", "Databases", self.system, self.system + ".xml")
        src_path = os.path.join(self.emu_movies_path, self.emu_movies_name)
        hs = Databases(system=self.system)
        header, db = hs.read_system_xml(db=xml)

        media_paths = os.listdir(src_path)

        # If Linking files, remove the old file before appending the new symlinks
        links = []
        batch_file = os.path.join(self.temp_path, "{}_RL_Media_Links_run_as_Admin.bat".format(self.system))
        if os.path.isfile(batch_file):
            os.remove(batch_file)

        for path in media_paths:
            src_dir = os.path.join(src_path, path)
            if action == "copy":
                msg = "Copying files from {}".format(src_dir)
            elif action == "move":
                msg = "Moving files from {}".format(src_dir)
            elif action == "link":
                msg = "Creating symbolic link from {}".format(src_dir)
            else:
                msg = "Action {} not permitted".format(action)
            logger.info(msg)
            files = os.listdir(src_dir)

            final_files = []

            for rom in db:
                for file in files:
                    if rom["name"] == os.path.basename(os.path.splitext(file)[0]):
                        final_files.append(file)

            for file in final_files:
                file = os.path.splitext(file)

                if path == "Advert":
                    dst = os.path.join(self.artwork_path, file[0], "Advertisement" + file[1])
                elif path == "Artwork Preview":
                    dst = os.path.join(self.artwork_path, file[0], "Preview" + file[1])
                elif path == "Background":
                    dst = os.path.join(self.backgrounds_path, file[0], "Background" + file[1])
                elif path == "Banner":
                    dst = os.path.join(self.artwork_path, file[0], "Banner" + file[1])
                elif path == "Box":
                    dst = os.path.join(self.artwork_path, file[0], "Box", "Box Art Front" + file[1])
                elif path == "Box_3D":
                    dst = os.path.join(self.artwork_path, file[0], "Box", "Box Art 3D" + file[1])
                elif path == "Box_Full":
                    dst = os.path.join(self.artwork_path, file[0], "Box", "Box Art Full" + file[1])
                elif path == "Box_Spine":
                    dst = os.path.join(self.artwork_path, file[0], "Box", "Box Art Spine" + file[1])
                elif path == "BoxBack":
                    dst = os.path.join(self.artwork_path, file[0], "Box", "Box Art Back" + file[1])
                elif path == "Cart":
                    dst = os.path.join(self.artwork_path, file[0], "Cartridge", "Cartridge" + file[1])
                elif path == "Cart_3D":
                    dst = os.path.join(self.artwork_path, file[0], "Cartridge", "Cartridge 3D" + file[1])
                elif path == "CartTop":
                    dst = os.path.join(self.artwork_path, file[0], "Cartridge", "Cartridge Top" + file[1])
                elif path == "Cabinet":
                    dst = os.path.join(self.artwork_path, file[0], "Cabinet" + file[1])
                elif path == "CD":
                    dst = os.path.join(self.artwork_path, file[0], "Media" + file[1])
                elif path == "Controls":
                    dst = os.path.join(self.controller_path, file[0], "Controls" + file[1])
                elif path == "CP":
                    dst = os.path.join(self.controller_path, file[0], "Control Panel" + file[1])
                elif path == "Disc":
                    dst = os.path.join(self.artwork_path, file[0], "Disc" + file[1])
                elif path == "GameOver":
                    dst = os.path.join(self.artwork_path, file[0], "Game Over" + file[1])
                elif path == "Icon":
                    dst = os.path.join(self.artwork_path, file[0], "Icon" + file[1])
                elif path == "Logos":
                    dst = os.path.join(self.logos_path, file[0], "Logo" + file[1])
                elif path == "Map":
                    dst = os.path.join(self.guides_path, file[0], "Map" + file[1])
                elif path == "Marquee":
                    dst = os.path.join(self.artwork_path, file[0], "Marquee" + file[1])
                elif path == "Overlay":
                    dst = os.path.join(self.artwork_path, file[0], "Overlay" + file[1])
                elif path == "PCB":
                    dst = os.path.join(self.artwork_path, file[0], "PCB" + file[1])
                elif path == "Score":
                    dst = os.path.join(self.artwork_path, file[0], "Score" + file[1])
                elif path == "Select":
                    dst = os.path.join(self.artwork_path, file[0], "Select" + file[1])
                elif path == "Snap":
                    dst = os.path.join(self.artwork_path, file[0], "Snapshot" + file[1])
                elif path == "Title":
                    dst = os.path.join(self.artwork_path, file[0], "Title Screen" + file[1])
                elif path == "Manual":
                    dst = os.path.join(self.manuals_path, file[0], "Game Manual" + file[1])
                elif path == "Music":
                    dst = os.path.join(self.music_path, file[0], file[0] + file[1])
                elif path == "Video_Advert_MP4":
                    dst = os.path.join(self.video_path, file[0], "Commercial" + file[1])
                elif path == "Video_Review_MP4":
                    dst = os.path.join(self.video_path, file[0], "Review" + file[1])

                else:
                    dst = ""

                src = os.path.join(src_dir, file[0] + file[1])

                # Check if the file is the same by validating the CRC
                src_c = Compressor(src)
                src_crc = src_c.get_crc()
                try:
                    dst_c = Compressor(dst)
                    dst_crc = dst_c.get_crc()
                except FileNotFoundError:
                    dst_crc = None

                try:
                    if action == "copy":
                        if dst_crc and src_crc[0]["crc"] != dst_crc[0]["crc"]:  # Check if CRCs Match
                            if not os.path.exists(os.path.dirname(dst)):
                                os.makedirs(os.path.dirname(dst))  # Create directory path if it doesn't exist
                            shutil.copy(src, dst)
                        elif not dst_crc:
                            if not os.path.exists(os.path.dirname(dst)):
                                os.makedirs(os.path.dirname(dst))  # Create directory path if it doesn't exist
                            shutil.copy(src, dst)
                        else:
                            msg = "RL: {} CRCs match".format(os.path.basename(src))
                            logger.debug(msg)
                    elif action == "move":
                        if dst_crc and src_crc[0]["crc"] != dst_crc[0]["crc"]:  # Check if CRCs Match
                            if not os.path.exists(os.path.dirname(dst)):
                                os.makedirs(os.path.dirname(dst))  # Create directory path if it doesn't exist
                            shutil.copy(src, dst)
                        elif dst_crc is None:
                            if not os.path.exists(os.path.dirname(dst)):
                                os.makedirs(os.path.dirname(dst))  # Create directory path if it doesn't exist
                            shutil.move(src, dst)
                        else:
                            msg = "RL: {} CRCs match".format(os.path.basename(src))
                            logger.debug(msg)
                    elif action == "link":
                        if not os.path.exists(os.path.dirname(dst)):
                            os.makedirs(os.path.dirname(dst))  # Create directory path if it doesn't exist
                        links.append('mklink "{}" "{}"\n'.format(dst, src))
                    else:
                        print("Action: {} not permitted".format(action))
                except FileNotFoundError as e:
                    msg = "RL: {} will not be moved: {}".format(file[0] + file[1], e)
                    logger.info(msg)

        if len(links) > 0:
            with open(batch_file, mode="a") as f:
                for link in links:
                    f.write(link)


if __name__ == "__main__":
    nes = "Nintendo Entertainment System"
    snes = "Super Nintendo Entertainment System"
    atari = "Atari Jaguar"
    sega = "Sega Genesis"
    rl = RocketLauncher(atari)
    rl.move_emu_movies(action="link")
