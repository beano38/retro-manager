from models.emulator import Emulator

import logging
import time
import os
import shutil
import re
import configparser
import json

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


class Mame(Emulator):

    def __init__(self):
        Emulator.__init__(self, model="MAME")
        self.model = Emulator.read_model(self)
        self.mame_path = os.path.join("X:\MAME", "MAME 0.202")
        # self.cfg_options = self.read_config_file()

    def read_config_file(self):
        """
        "read_config_file" Method reads mame config file

        Args:
            self

        Returns:
            dictionary of configuration file

        Raises:
            None
        """

        cfg_options = {}
        with open(self.ini, mode="r", encoding="UTF-8-sig") as f:
            for i in f.readlines():
                stuff = re.compile(r'(^[\w]*)(\s*)(.*)')
                if stuff.match(i):
                    if ";" in stuff.match(i)[3]:
                        cfg_options[stuff.match(i)[1]] = stuff.match(i)[3].split(";")
                    else:
                        cfg_options[stuff.match(i)[1]] = stuff.match(i)[3]
        return cfg_options

    def write_config_file(self, key, replace, cfg_file="mame.ini"):
        """
        "write_config_file" updates a value for a given key

        Args:
            key(required): the key which to update the value of
            replace(required): the value to replace
            cfg_file(optional, default="mame.ini") the config file to update

        Returns:
            None

        Raises:
            None
        """
        src = os.path.join(self.mame_path, cfg_file)
        dst = os.path.join(self.mame_path, cfg_file + ".bak")
        shutil.copy(src, dst)
        with open(src, mode="r", encoding="UTF-8-sig") as f:
            for line in f.readlines():
                stuff = re.compile(r'(^[\w]*)(\s*)(.*)')
                if stuff.match(line):
                    if key in stuff.match(line)[1]:
                        f = stuff.match(line)[0]
                        r = "{}{}{}".format(stuff.match(line)[1], stuff.match(line)[2], replace)
        with open(dst, mode="r", encoding="UTF-8-sig") as f1:
            with open(src, mode="w", encoding="UTF-8-sig") as f2:
                for line in f1.readlines():
                    f2.write(line.replace(f, r))

    def execute_cli(self, list_of_options):
        """
        "execute_cli" Method creates the mame.ini file for the first time

        Args:
            list_of_options(required): List of options to pass to the executable

        Returns:
            None

        Raises:
            None
        """
        import subprocess
        executable = os.path.join(self.mame_path, self.model["exe"])
        command = [executable] + list_of_options
        msg = "Executing {}".format(command)
        logger.debug(msg)
        execute = subprocess.Popen(command, cwd=self.mame_path)

    def set_defaults(self):
        self.execute_cli(list_of_options=["-createconfig"])
        time.sleep(.4)  # Wait for the config files to be generated

        self.write_config_file("rompath", "roms;X:\\MAME\\ROMs;X\\MAME\\BIOS;X:\\Software Lists")
        self.write_config_file("artpath", "artwork;X:\\MAME\\Extras\\Artwork")
        self.write_config_file("samplepath", "samples;X:\\MAME\\Samples")
        self.write_config_file("snapshot_directory", "snap;X:\\MAME\\Extras")
        self.write_config_file("cheatpath", "cheat;X:\\MAME\\Extras")
        self.write_config_file("skip_gameinfo", "1")

        self.write_config_file("historypath", "history;dats;.;X:\\MAME\\Extras\\dats", cfg_file="ui.ini")
        self.write_config_file("categorypath", "folders;X:\\MAME\\Extras\\folders", cfg_file="ui.ini")
        self.write_config_file("cabinets_directory", "cabinets;cabdevs;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("cpanels_directory", "cpanel;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("pcbs_directory", "pcb;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("flyers_directory", "flyers;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("titles_directory", "titles;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("ends_directory", "ends;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("marquees_directory", "marquees;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("artwork_preview_directory", "artwork preview;artpreview;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("bosses_directory", "bosses;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("logos_directory", "logo;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("scores_directory", "scores;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("versus_directory", "versus;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("gameover_directory", "gameover;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("howto_directory", "howto;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("select_directory", "select;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("icons_directory", "icons;X:\\MAME\\Extras", cfg_file="ui.ini")
        self.write_config_file("covers_directory", "covers;X:\\MAME\\Extras", cfg_file="ui.ini")

    @staticmethod
    def move_chd_to_root(chd_path):
        """
        "move_chd_to_root" Method moves a .CHD file up one level in the directory structure.
        This is needed when one downloads a merged CHD set and MAME is setup for
        split CHD set.  Afterwards, run clrmamepro scanner to fix the ROM set

        Args:
            chd_path(required, default=None): Path of MAME machine to fix

        Returns:
            None

        Raises:
            None
        """
        dirs = os.listdir(chd_path)

        file_list = []
        for item in dirs:
            if os.path.isdir(os.path.join(chd_path, item)):
                files = os.listdir(os.path.join(chd_path, item))
                for f in files:
                    file_list.append(os.path.join(chd_path, item, f))

        for f in file_list:
            dst = os.path.join(chd_path, os.path.basename(f))
            if os.path.isfile(dst):
                msg = "CHD {} exists already, deleting duplicate".format(f)
                logger.info(msg)
                os.remove(f)
            else:
                shutil.move(f, dst)
                msg = "CHD {} moved".format(os.path.basename(f))
                logger.info(msg)


def main():
    m = Mame()
    m.set_defaults()


if __name__ == "__main__":
    main()
