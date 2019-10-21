import os

from general import Paths, Compressor

exclude_ext = [".zip", ".ZIP", ".7z", ".7Z", ".rar", ".RAR"]


class Rom(Compressor):

    def __init__(self, system=None, name=None):
        Paths.__init__(self)
        Compressor.__init__(self, os.path.join(self.rom_path, system, name))

        self.name = name
        self.system = system

    def rename_extension(self, extension):
        """
        "rename_extension" is a method that will rename the extension of the ROM to the
        first extension name in the system model

        Args:
            self

        Returns:
            Newly named ROM name

        Raises:
            None
        """
        if type(extension) == list:
            extension = ".{}".format(extension[0])
        elif type(extension) == str:
            extension = ".{}".format(extension)
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
            msg = "{}'s extension is named correctly".format(self.name)

        return os.path.join(self.rom_path, self.system, f + extension)


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
