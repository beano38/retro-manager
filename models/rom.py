import os

from general import Paths, Compressor
from models.system import System
from rocketlauncher import RocketLauncher

exclude_ext = [".zip", ".ZIP", ".7z", ".7Z", ".rar", ".RAR"]


class Rom(Compressor):

    def __init__(self, system=None, name=None):
        Paths.__init__(self)
        Compressor.__init__(self, os.path.join(self.rom_path, system, name))

        self.name = name
        self.system = system
        self.sys_info = System(self.system)

    def rename_extension(self):
        """
        "rename_extension" is a method that will rename the extension of the ROM to the
        first extension name in the system model

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        if type(self.sys_info.extensions) == list:
            extension = ".{}".format(self.sys_info.extensions[0])
        elif type(self.sys_info.extensions) == str:
            extension = ".{}".format(self.sys_info.extensions)
        else:
            extension = ".zip"
        rom_path = os.path.join(self.rom_path, self.system, self.name)
        f, ext = os.path.splitext(self.name)
        if ext != extension and ext not in exclude_ext and rom_path is not os.path.isdir(rom_path):
            dst = os.path.join(self.rom_path, self.system, f + extension)
            msg = "Renaming {} to {}".format(self.name, f + extension)
            print(msg)
            os.rename(rom_path, dst)
        else:
            msg = "{} is good".format(self.name)
            print(msg)


# def rename_extensions(system):
#     p = Paths()
#     roms = os.listdir(os.path.join(p.rom_path, system))
#     for rom in roms:
#         r = Rom(system=system, name=rom)
#         r.rename_extension()
#
#
# def compress_roms(system):
#     p = Paths()
#     roms = os.listdir(os.path.join(p.rom_path, system))
#     for rom in roms:
#         c = Compressor(src_file=os.path.join(p.rom_path, system, rom))
#         c.compress(ext="zip")


def main():
    nes = "Nintendo Entertainment System"
    jag = "Atari Jaguar"
    rom_name = "8 Eyes (USA).u1"
    rom = Rom(system=jag, name=rom_name)
    # print(rom.sys_info.extensions)
    # print(rom.rename_extension())


if __name__ == "__main__":
    main()
