import logging
import time
import json
import os

from general import Paths, Compressor
from hyperspin import HyperSpin
from models.rom import Rom

LOG_FILE = "../../arcade.log"
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


class System(Paths):

    def __init__(self, system=None):
        Paths.__init__(self,)
        self.system = system

        # --- GamesDB Attributes ---
        self.games_db_name = None
        self.games_db_id = None
        self.overview = None
        self.developer = None
        self.manufacturer = None
        self.cpu = None
        self.memory = None
        self.graphics = None
        self.sound = None
        self.display = None
        self.media = None
        self.maxcontrollers = None
        self.rating = None
        self.banners = None
        self.fanarts = None
        self.consoleart = None
        self.controllerart = None

        # ----- Model Attributes -----
        self.emulator = None
        self.extensions = None
        self.year = None
        self.platform_type = None
        self.emu_movies_name = None

        self.tosec = None
        self.goodset = None
        self.nointro = None
        self.software_lists = None
        self.no_good_set = None

        try:
            self.read_model()
        except FileNotFoundError:
            msg = "SYS: Model for {} not defined".format(self.system)
            logger.info(msg)

        # ----- ROM Set Paths -----
        try:
            self.tosecs = self.tosec_dirs()
        except Exception as e:
            self.tosecs = None
            logger.debug(e)

    # ----- TOSEC -----

    def tosec_dirs(self):
        """
        "tosec_dirs" is a method that will recursively set all directories
        associated with the TOSEC Emulation databases

        Args:
            self

        Returns:
            list of directories

        Raises:
            None
        """
        path = os.path.join(self.mstr_tosec, self.manufacturer, self.tosec)
        dirs = [x[0] for x in os.walk(path)]

        return dirs

    # ----- Read System Model -----

    def read_model(self):
        """
        "read_model" is a method that will set attributes for variables related to the
        specified system

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        model = os.path.join(os.path.dirname(__file__), "systems", self.system + ".json")
        with open(model, mode="r") as f:
            data = json.load(f)

        if "emulator" in data:
            self.emulator = data["emulator"]
        if "extensions" in data:
            if type(data["extensions"]) is str:
                self.extensions = [data["extensions"]]
            else:
                self.extensions = data["extensions"]
        if "year" in data:
            self.year = data["year"]
        if "platformType" in data:
            self.platform_type = data["platformType"]
        if "emuMoviesName" in data:
            self.emu_movies_name = data["emuMoviesName"]

        if data["romSets"]["TOSEC"] is not None:
            self.tosec = data["romSets"]["TOSEC"]
        if data["romSets"]["GoodSet"] is not None:
            self.goodset = [os.path.join(self.mstr_good_set, data["romSets"]["GoodSet"])]
        if data["romSets"]["NoIntro"] is not None:

            if type(data["romSets"]["NoIntro"]) is str:
                self.nointro = [os.path.join(self.mstr_no_intro, data["romSets"]["NoIntro"])]
            else:
                dirs = []
                for stuff in data["romSets"]["NoIntro"]:
                    dirs.append(os.path.join(self.mstr_no_intro, stuff))
                self.nointro = dirs
        if data["romSets"]["SoftwareLists"] is not None:
            if type(data["romSets"]["SoftwareLists"]) is str:
                self.software_lists = [os.path.join(self.mstr_sl, data["romSets"]["SoftwareLists"])]
            else:
                dirs = []
                for stuff in data["romSets"]["SoftwareLists"]:
                    dirs.append(os.path.join(self.mstr_sl, stuff))
                self.software_lists = dirs
        if data["romSets"]["NoGoodSet"] is not None:
            self.no_good_set = [os.path.join(self.mstr_non_good_set, data["romSets"]["NoGoodSet"])]
        #     self.software_lists = [os.path.join(self.mstr_sl, data["romSets"]["SoftwareLists"])]

        games_db = data["GamesDbData"]["Platform"]
        self.manufacturer = games_db["manufacturer"]

    # ----- Build ROM Set and helper functions -----

    def _filter_sets_by_crcs(self, source_set):
        """
        "_filter_sets_by_crcs" is a method that will build a dictionary of ROMs with unique crcs

        Args:
            source_set, type list, the source list of directories

        Returns:
            filtered list of dictionaries of ROM names with CRC and source file name

        Raises:
            None
        """
        crc_names = []
        index_id = 0

        for source_group in source_set:
            rom_names = os.listdir(source_group)
            num_of_roms = len(rom_names)
            msg = "Found {} files in {}".format(num_of_roms, source_group)
            logger.info(msg)

            for rom_file in rom_names:
                source_file = os.path.join(source_group, rom_file)
                if os.path.isfile(source_file):
                    c = Compressor(src_file=source_file)
                    try:
                        rom_crc_list = c.get_crc()
                    except:
                        msg = "Error with file: {}".format(rom_file)
                        logger.debug(msg)
                    for rom_name in rom_crc_list:
                        rom_name["name"] = source_file
                        crc_names.append(rom_name)

        msg = "Found {} ROMs in the folders".format(len(crc_names))
        logger.info(msg)

        # Filter out duplicate CRCs
        crcs_all = []
        final_crcs = []
        for i in range(len(crc_names)):
            crc = crc_names[i]['crc']
            if crc not in crcs_all:
                crcs_all.append(crc)
                final_crcs.append(crc_names[i])

        return final_crcs

    def _match_crcs(self, source_set):
        """
        "_match_crcs" is a method that will compare the RocketLauncher database ROM list with the available
        ROM list from the "_filter_sets_by_crcs" method

        Args:
            None

        Returns:
            final list of dictionaries of ROMs to copy

        Raises:
            None
        """

        # Get the ROM list from RocketLauncher's Database
        p = Paths()
        xml = os.path.join(p.rl_path, "RocketLauncherUI", "Databases", self.system, self.system + ".xml")
        hs = HyperSpin(self.system)
        db = hs.audit(files_to_audit=os.path.join(p.rom_path, self.system), db=xml, audit_type="rom")

        miss = [rom for rom in db if not rom["rom"]]
        # have = [rom for rom in db if rom["rom"]]

        msg ="There are {} ROMs missing from the ROM audit".format(len(miss))
        logger.info(msg)

        # Get the ROM list of available ROMs
        available_roms = self._filter_sets_by_crcs(source_set=source_set)
        msg = "Found {} unique ROMs in the folders".format(len(available_roms))
        logger.info(msg)

        # Final list
        final_rom_set = []
        for rom in miss:
            for available_rom in available_roms:
                if rom["crc"] == available_rom["crc"]:
                    f, ext = os.path.splitext(available_rom["compress_name"])
                    available_rom["dst"] = os.path.join(p.rom_path, self.system, "{}{}".format(rom["name"], ext))
                    final_rom_set.append(available_rom)

        msg = "Matched {} ROMs from the available ROMs to the missing ROMs".format(len(final_rom_set))
        logger.info(msg)

        return final_rom_set

    def build_rom_set(self, source_set, rename=True, compress=True):
        roms = self._match_crcs(source_set)

        for rom in roms:
            # Get compressed file
            if rom["compress_name"]:
                c = Compressor(rom["name"])
                try:
                    c.extract(rom["compress_name"], dst_dir=os.path.join(self.rom_path, self.system))
                    src = os.path.join(self.rom_path, self.system, rom["compress_name"])
                    dst = rom["dst"]
                    # Rename the ROM to the RocketLauncher Database Name
                    os.rename(src, dst)
                except FileExistsError:
                    msg = "File Exists - {}".format(rom["compress_name"])
                    logger.debug(msg)
                # Compress
                if rename:
                    r = Rom(name=dst, system=self.system)
                    new_dst = r.rename_extension(self.extensions)
                if compress:
                    c = Compressor(new_dst)
                    c.compress(ext="zip")


def main():
    nes = "Nintendo Entertainment System"
    jag = "Atari Jaguar"
    itv = "Mattel Intellivision"
    gg = "Sega Game Gear"

    platform = System(system=gg)
    ss = platform.nointro
    platform.build_rom_set(source_set=ss)


if __name__ == "__main__":
    main()
