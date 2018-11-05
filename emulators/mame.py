from models.emulator import Emulator

import os
import shutil
import re
import configparser
import json


class Mame(Emulator):

    def __init__(self):
        Emulator.__init__(self, model="MAME")
        self.model = Emulator.read_model(self)
        self.ini = os.path.join("X:\\MAME\\MAME 0.202", self.model["config"])
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
                        cfg_options[stuff.match(i)[1]] = stuff.match(i)[3]
                    else:
                        cfg_options[stuff.match(i)[1]] = stuff.match(i)[3]
        return cfg_options

    def write_config_file(self, key, replace):
        dst = os.path.join(os.path.dirname(self.ini), self.model["config"] + ".bak")
        shutil.copy(self.ini, dst)
        with open(self.ini, mode="r", encoding="UTF-8-sig") as f:
            for line in f.readlines():
                stuff = re.compile(r'(^[\w]*)(\s*)(.*)')
                if stuff.match(line):
                    if key in stuff.match(line)[1]:
                        f = stuff.match(line)[0]
                        r = "{}{}{}".format(stuff.match(line)[1], stuff.match(line)[2], replace)
        with open(dst, mode="r", encoding="UTF-8-sig") as f1:
            with open(self.ini, mode="w", encoding="UTF-8-sig") as f2:
                for line in f1.readlines():
                    f2.write(line.replace(f, r))

    def write_ui_file(self, key, replace):
        src = os.path.join(os.path.dirname(self.ini), "ui.ini")
        dst = os.path.join(os.path.dirname(self.ini), "ui.ini.bak")
        shutil.copy(src, dst)
        r = ""
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

    def set_defaults(self):
        self.write_config_file("rompath", "X:\\MAME\\ROMs;X\\MAME\\BIOS;X:\\Software Lists")
        self.write_config_file("samplepath", "X:\\MAME\\Samples")
        self.write_config_file("snapshot_directory", "X:\\MAME\\Extras")

        self.write_ui_file("cabinets_directory", "X:\\MAME\\Extras")
        self.write_ui_file("cpanels_directory", "X:\\MAME\\Extras")
        self.write_ui_file("pcbs_directory", "X:\\MAME\\Extras")
        self.write_ui_file("flyers_directory", "X:\\MAME\\Extras")
        self.write_ui_file("titles_directory", "X:\\MAME\\Extras")
        self.write_ui_file("ends_directory", "X:\\MAME\\Extras")
        self.write_ui_file("marquees_directory", "X:\\MAME\\Extras")
        self.write_ui_file("artwork_preview_directory", "X:\\MAME\\Extras")
        self.write_ui_file("bosses_directory", "X:\\MAME\\Extras")
        self.write_ui_file("logos_directory", "X:\\MAME\\Extras")
        self.write_ui_file("scores_directory", "X:\\MAME\\Extras")
        self.write_ui_file("versus_directory", "X:\\MAME\\Extras")
        self.write_ui_file("gameover_directory", "X:\\MAME\\Extras")
        self.write_ui_file("howto_directory", "X:\\MAME\\Extras")
        self.write_ui_file("select_directory", "X:\\MAME\\Extras")
        self.write_ui_file("icons_directory", "X:\\MAME\\Extras")
        self.write_ui_file("covers_directory", "X:\\MAME\\Extras")


def main():
    m = Mame()
    # print(json.dumps(m.cfg_options, indent=2))
    m.set_defaults()


if __name__ == "__main__":
    main()
