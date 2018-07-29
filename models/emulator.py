from models.control_panel import ControlPanel
from arcade import Arcade

import os
import re
import json
from collections import OrderedDict
import configparser
import shutil


class Emulator(ControlPanel):

    def __init__(self, model=None):
        ControlPanel.__init__(self)
        self.arcade = Arcade()
        self.model = model

    def create_dirs(self):
        modules = os.listdir(os.path.join(self.arcade.rl_path, "Modules"))
        for module in modules:
            try:
                os.makedirs(os.path.join(self.arcade.emulator_path, module, "Install Files"))
            except FileExistsError:
                print("{} exists".format(module))

    def read_module(self, module):
        modules = os.path.join(self.arcade.rl_path, "Modules")
        module_file = os.path.join(modules, module, module + ".ahk")
        if os.path.isfile(module_file):
            with open(module_file, "r", encoding="UTF-8") as f:
                results = {}
                notes = []
                for line in f.readlines():
                    search = re.compile('^([Mi].*) := (.*)$')
                    result = search.match(line)
                    if result is not None:
                        result_2 = re.sub('"', "", result.group(2))
                        # result_2.split(",")
                        results[result.group(1)] = result_2
                    note = re.search('^;(.*)$', line)
                    if note is not None:
                        notes.append(note)

            sys = results["MSystem"].split(',')
            results["MSystem"] = sys
            for k, v in results.items():
                print(k, v)

            return results

        else:
            msg = "EMU:  {} was not found".format(module)
            self.arcade.log(4, msg)

    def read_model(self):
        model = os.path.join(os.path.dirname(__file__), "emulators", self.model + ".json")
        shutil.copy(model, os.path.join(model + ".backup"))
        with open(model, mode="r") as f:
            data = json.load(f)

        if data["config_type"] == "ini":
            ini = os.path.join(self.arcade.emulator_path, self.model, data["dir_name"], data["config"])
            config = configparser.ConfigParser(dict_type=OrderedDict)
            config.optionxform = str
            config.read(ini)

            section = "main"

            config.set(section, data["controls"]["p1_d_up"], self.p1_d_up)
            config.set(section, data["controls"]["p1_d_down"], self.p1_d_down)
            config.set(section, data["controls"]["p1_d_left"], self.p1_d_left)
            config.set(section, data["controls"]["p1_d_right"], self.p1_d_right)
            config.set(section, data["controls"]["p1_coin"], self.p1_coin)
            config.set(section, data["controls"]["p1_start"], self.p1_start)
            config.set(section, data["controls"]["p1_b1"], self.p1_b1)
            config.set(section, data["controls"]["p1_b2"], self.p1_b2)
            config.set(section, data["controls"]["p1_b3"], self.p1_b3)
            config.set(section, data["controls"]["p1_b4"], self.p1_b4)

            with open(ini, mode="w") as f:
                config.write(f, space_around_delimiters=False)


def main():
    emu = Emulator()
    # emu.read_model()
    modules = os.listdir(os.path.join(emu.arcade.rl_path, "Modules"))
    for module in modules:
        results = emu.read_module(module)


if __name__ == "__main__":
    main()
