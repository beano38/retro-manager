import logging
import time
import json
import os

from general import Paths

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
            self.extensions = data["extensions"]
        if "year" in data:
            self.year = data["year"]
        if "platformType" in data:
            self.platform_type = data["platformType"]

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


def main():
    atari = "Atari 8-Bit"
    nes = "Nintendo Entertainment System"
    other = "Sony PSP"
    platform = System(system=nes)

    print(platform.emulator)
    print(platform.system)
    print(platform.extensions)
    print(platform.platform_type)


if __name__ == "__main__":
    main()
