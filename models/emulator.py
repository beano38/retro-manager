from models.control_panel import ControlPanel
from general import Paths

import time
import logging
import os
import re
import json


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


class Emulator(ControlPanel):

    def __init__(self, model=None):
        ControlPanel.__init__(self)
        self.paths = Paths()
        self.model = model

    def read_module(self, module):
        modules = os.path.join(self.paths.rl_path, "Modules")
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
            msg = "{} was not found".format(module)
            logger.info(msg)

    def read_model(self):
        model = os.path.join(os.path.dirname(__file__), "emulators", self.model + ".json")
        with open(model, mode="r") as f:
            data = json.load(f)
        return data


def main():
    emu = Emulator(model="AAE")
    data = emu.read_model()
    print(json.dumps(data, indent=2))
    emu.read_module("AAE")


if __name__ == "__main__":
    main()
