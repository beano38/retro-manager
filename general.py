import os
import shutil
import configparser
import time
import zipfile
import logging
import subprocess
import binascii
import xml.etree.cElementTree as ET
from xml.dom import minidom

import rarfile

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


class Paths:

    def __init__(self):
        # self.root_drive = None
        # self.root_path = None
        # self.emulator_path = None
        # self.rom_path = None
        # self.log_path = None
        # self.temp_path = None
        # self.utilities_path = None
        # self.frontends_path = None
        #
        # self.mstr_no_intro = None
        # self.mstr_mame = None
        # self.mstr_sl = None
        # self.mstr_good_set = None
        # self.mstr_non_good_set = None
        # self.mstr_redump = None
        # self.mstr_tosec = None
        #
        # self.emu_movies = None
        #
        # self.seven_zip_exe = None
        # self.rar_exe = None

        self._load_paths()

    def _load_paths(self):
        """
        "load_paths" is a method that will set all the paths for the system based on the
        settings/paths.ini file

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        ini = os.path.join(os.path.dirname(__file__), "Settings", "paths.ini")
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.optionxform = str
        config.read(ini)

        self.root_drive = config.get("Common", "root_drive")
        self.root_path = config.get("Common", "root_path")

        self.emulator_path = config.get("Arcade", "emulator_path")
        self.rom_path = config.get("Arcade", "roms_path")
        self.log_path = config.get("Arcade", "logs_path")
        self.temp_path = config.get("Arcade", "temp_path")
        self.utilities_path = config.get("Arcade", "utilities_path")
        self.frontends_path = config.get("Arcade", "frontends_path")

        self.mstr_no_intro = config.get("Master ROMs", "NoIntro")
        self.mstr_mame = config.get("Master ROMs", "MAME")
        self.mstr_sl = config.get("Master ROMs", "SoftwareList")
        self.mstr_good_set = config.get("Master ROMs", "GoodSet")
        self.mstr_non_good_set = config.get("Master ROMs", "NonGoodSet")
        self.mstr_redump = config.get("Master ROMs", "Redump")
        self.mstr_tosec = config.get("Master ROMs", "TOSEC")

        self.emu_movies = config.get("EmuMovies", "DownloadPath")

        self.seven_zip_exe = config.get("Compressor", "SevenZip")
        self.rar_exe = config.get("Compressor", "Rar")

        self.rl_path = config.get("RocketLauncher", "path")
        # Front Ends
        self.hs_path = config.get("FrontEnds", "HyperSpin")
        # Utilities
        self.notepad = config.get("Utilities", "Notepad++")
        # Archives
        self.rocket_launcher_archive = config.get("Installs", "RocketLauncher")
        self.rocket_launcher_media_archive = config.get("Installs", "RocketLauncher_Media")


class Compressor(Paths):

    def __init__(self, src_file):
        Paths.__init__(self)

        self.src_file = src_file
        self.dst_file = None

    def _backup_file(self):
        """
        "_backup_file" is a method that will create the backup directory and move the file there

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        backup_path = os.path.join(os.path.split(self.dst_file)[0], "_Backup")
        if not os.path.isdir(backup_path):
            os.makedirs(backup_path)
        msg = "{} exists, moving to backup".format(self.dst_file)
        logger.info(msg)
        shutil.move(self.dst_file, os.path.join(backup_path, os.path.basename(self.dst_file)))

    # Zip File Operations

    def _compress_zip(self):
        """
        "_compress_zip" Method compresses the source file

        Args:
            self

        Returns:
            None

        Raises:
            None
        """

        with zipfile.ZipFile(self.dst_file, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
            zf.write(self.src_file, os.path.basename(self.src_file))

    def _crc_from_zip(self):
        """
        "_crc_from_zip" Method returns all CRC-32 info from files in compressed file

        Args:
            self

        Returns:
            List of Dictionaries that have the filename and crc values

        Raises:
            None
        """
        cf = zipfile.ZipFile(self.src_file)
        crcs = []
        crc_info = {}
        for i in cf.infolist():
            crc_info["compress_name"] = i.filename
            crc_info["crc"] = str(hex(i.CRC)[2:].zfill(8)).upper()
            crcs.append(dict(crc_info))
        return crcs

    def _get_file_from_zip(self, compressed_name, dst_dir, password=None):
        """
        "_get_file_from_zip" Method extracts a single file from the source file

        Args:
            compressed_name(required): Name of file in zip
            dst_dir(required): destination directory to extract the file to
            password(optional, default = None): password for archive if needed

        Returns:
            None

        Raises:
            None
        """

        with zipfile.ZipFile(self.src_file) as zf:
            zf.extract(compressed_name, dst_dir, password)

    # 7zip File Operations

    def _compress_seven_zip(self, level=5, threads=4):
        """
        "_compress_seven_zip" Method compresses the source file

        Args:
            level(optional, default=5): Compression level
            threads(optional, default=4): Amount of processor threads to use

        Returns:
            None

        Raises:
            None
        """
        command = [self.seven_zip_exe, "a", self.dst_file,
                   self.src_file, "-mx{}".format(level), "-mmt{}".format(threads)]
        execute = subprocess.Popen(command)

    def _crc_from_seven_zip(self):
        """
        "_crc_from_zip" Method returns all CRC-32 info from files in compressed file

        Args:
            self

        Returns:
            List of Dictionaries that have the filename and crc values

        Raises:
            None
        """
        command = [self.seven_zip_exe, "l", "-slt", self.src_file]
        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        crcs = []
        crc_info = {}
        for line in execute.stdout:
            if "Path" in line.decode():
                fname = line.decode().split(" = ")[1].strip("\n\r")
                crc_info["compress_name"] = fname
            elif "CRC" in line.decode():
                crc = line.decode().split(" = ")[1].strip("\n\r")
                crc_info["crc"] = crc
                crcs.append(dict(crc_info))
        return crcs

    def _get_file_from_seven_zip(self, compressed_name, dst_dir, password=None):
        """
        "_get_file_from_seven_zip" Method extracts a single file from the source file

        Args:
            compressed_name(required): Name of file in archive
            dst_dir(required): destination directory to extract the file to
            password(optional, default = None): password for archive if needed

        Returns:
            None

        Raises:
            None
        """

        # e = extract, -p = password, -o = output dir, -r = recursive, -y = answer yes
        command = [self.seven_zip_exe, "e",
                   self.src_file, "-p{}".format(password),
                   "-o{}".format(dst_dir), compressed_name, "-r", "-y"]
        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        for line in execute.stdout:
            msg = line.decode().strip("\n\r")
            logger.debug(msg)

    # RAR File Operations

    def _compress_rar(self):
        """
        "_compress_rar" Method compresses the source file

        Args:
            self

        Returns:
            None

        Raises:
            None
        """

        # a = add to archive, -ep = adds the archive without the path
        command = [self.rar_exe, "a", "-ep", self.dst_file, self.src_file]
        execute = subprocess.Popen(command)

        # msg = "Not defined yet"
        # logger.critical(msg)

    def _crc_from_rar(self):
        """
        "_crc_from_rar" Method returns all CRC-32 info from files in compressed file

        Args:
            self

        Returns:
            List of Dictionaries that have the filename and crc values

        Raises:
            None
        """
        cf = rarfile.RarFile(self.src_file)
        crcs = []
        crc_info = {}
        for i in cf.infolist():
            crc_info["compress_name"] = i.filename
            crc_info["crc"] = str(hex(i.CRC)[2:].zfill(8)).upper()
            crcs.append(dict(crc_info))
        return crcs

    def _get_file_from_rar(self, compressed_name, dst_dir, password=None):
        """
        "_get_file_from_rar" Method extracts a single file from the source file

        Args:
            compressed_name(required): Name of file in archive
            dst_dir(required): destination directory to extract the file to
            password(optional, default = None): password for archive if needed

        Returns:
            None

        Raises:
            None
        """
        rarfile.UNRAR_TOOL = self.rar_exe
        with rarfile.RarFile(self.src_file) as rf:
            rf.extract(compressed_name, dst_dir, password)

    # Other File Operations

    def _crc_from_file(self):
        """
        "_crc_from_rar" Method returns all CRC-32 info from files in compressed file

        Args:
            self

        Returns:
            List of Dictionaries that have the filename and crc values

        Raises:
            None
        """

        buf = open(self.src_file, 'rb').read()
        buf = (binascii.crc32(buf) & 0xFFFFFFFF)
        return [{"compress_name": os.path.basename(self.src_file), "crc": "%08X" % buf}]

    # Public Methods

    def compress(self, ext="zip", remove_source=True):
        """
        "compress" Method compresses the source file using the appropriate internal method

        Args:
            ext(optional, default="zip"): Sets the compression method
            remove_source(optional, default=True): Will remove the source file

        Returns:
            None

        Raises:
            None
        """

        self.dst_file = os.path.splitext(self.src_file)[0] + ".{}".format(ext)

        # Check if the zipfile exists
        if os.path.isfile(self.dst_file):
            self._backup_file()

        # Compress the file after ensuring it is a file and not a directory
        if os.path.isfile(self.src_file):
            msg = "Compressing {}".format(os.path.basename(self.src_file))
            logger.info(msg)

            if ext == "zip":
                self._compress_zip()
            elif ext == "7z":
                self._compress_seven_zip()
            elif ext == "rar":
                self._compress_rar()
            else:
                msg = "{} is not a supported extension".format(ext)
                logger.debug(msg)

        elif os.path.isdir(self.src_file):
            msg = "{} is a directory".format(os.path.basename(self.src_file))
            logger.debug(msg)

        if remove_source:
            os.remove(self.src_file)

    def get_crc(self):
        """
        "get_crc" Calculates the CRC-32 using the appropriate internal method

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        if os.path.isfile(self.src_file):
            msg = "Gathering CRCs from {}".format(os.path.basename(self.src_file))
            logger.info(msg)

        ext = os.path.splitext(self.src_file)[1]

        if ext == ".zip":
            crcs = self._crc_from_zip()
        elif ext == ".7z":
            crcs = self._crc_from_seven_zip()
        elif ext == ".rar":
            crcs = self._crc_from_rar()
        else:
            crcs = self._crc_from_file()

        return crcs

    def extract(self, compressed_name, dst_dir, password=None):
        """
        "extract" extracts a specific file from an archive

        Args:
            compressed_name(required): Name of file in archive
            dst_dir(required): destination directory to extract the file to
            password(optional, default = None): password for archive if needed

        Returns:
            None

        Raises:
            None
        """
        if os.path.isfile(self.src_file):
            msg = "Extracting {} from {}".format(compressed_name, os.path.basename(self.src_file))
            logger.info(msg)

            ext = os.path.splitext(self.src_file)[1]

            if ext == ".zip":
                self._get_file_from_zip(compressed_name, dst_dir, password)
            elif ext == ".7z":
                self._get_file_from_seven_zip(compressed_name, dst_dir, password)
            elif ext == ".rar":
                self._get_file_from_rar(compressed_name, dst_dir, password)
            else:
                msg = "{} is not a valid archive".format(self.src_file)
                logger.info(msg)

    def extract_all(self, dst_dir, password=None):
        """
        "extract_all" extracts all contents of archive

        Args:
            compressed_name(required): Name of file in archive
            dst_dir(required): destination directory to extract the file to
            password(optional, default = None): password for archive if needed

        Returns:
            None

        Raises:
            None
        """

        # x = extract, -p = password, -o = output dir, -y = answer yes
        if password:
            msg = "Extracting {}".format(self.src_file)
            logger.info(msg)
            command = [self.seven_zip_exe, "x",
                       self.src_file, "-p{}".format(password),
                       "-o{}".format(dst_dir), "-y"]
        else:
            msg = "Extracting {}".format(self.src_file)
            logger.info(msg)
            command = [self.seven_zip_exe, "x",
                       self.src_file, "-o{}".format(dst_dir), "-y"]
        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        for line in execute.stdout:
            msg = line.decode().strip("\n\r")
            logger.debug(msg)


class Arcade(Paths):

    def __init__(self):
        Paths.__init__(self)

    def create_arcade(self):
        dirs = [self.root_path, self.emulator_path, self.rom_path, self.temp_path, self.frontends_path,
                self.log_path, self.utilities_path]
        for directory in dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)

    @staticmethod
    def prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")


if __name__ == "__main__":

    system = "Nintendo Entertainment System"
    rom = "3-D WorldRunner (USA).nes"

    p = Paths()
    source_file = os.path.join(p.rom_path, system, rom)

    c = Compressor(source_file)
    c.compress(remove_source=False)
