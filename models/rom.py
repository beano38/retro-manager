import os
import zipfile
import binascii

from arcade import Arcade
from models.system import System

exclude_ext = [".zip", ".ZIP", ".7z", ".7Z", ".rar", ".RAR"]


class Rom(Arcade):

    def __init__(self, system=None, name=None, logLevel=3):
        Arcade.__init__(self, logLevel)

        self.name = name
        self.system = system
        self.sys_info = System(self.system)
        self.crc = self.crc32()

    def rename_extension(self):
        if type(self.sys_info.extensions) == list:
            extension = ".{}".format(self.sys_info.extensions[0])
        elif type(self.sys_info.extensions) == str:
            extension = ".{}".format(self.sys_info.extensions)
        else:
            extension = ".zip"
        rom_path = os.path.join(self.rom_path, self.system, self.name)
        f, ext = os.path.splitext(self.name)
        if ext != extension and ext not in exclude_ext and not os.path.isdir(rom_path):
            dst = os.path.join(self.rom_path, self.system, f + extension)
            msg = "Renaming {} to {}".format(self.name, f + extension)
            print(msg)
            os.rename(rom_path, dst)
        # else:
        #     msg = "{} is good".format(self.name)
        #     print(msg)

    def compress(self):
        rom_path = os.path.join(self.rom_path, self.system, self.name)
        f, ext = os.path.splitext(self.name)
        if os.path.isfile(rom_path) and ext not in exclude_ext:
            dst = os.path.join(self.rom_path, self.system, "{}.zip".format(f))
            with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as f:
                f.write(rom_path, os.path.basename(rom_path))
            os.remove(rom_path)

    def crc32(self):
        f, ext = os.path.splitext(self.name)
        if ext == ".zip" or ext == ".ZIP":
            crc = self.crc32_from_zipfile()
            crc_info = crc[0]["crc"]
        else:
            crc_info = self.crc32_from_file()
        return crc_info

    def crc32_from_zipfile(self):
        crc_to_check = zipfile.ZipFile(os.path.join(self.rom_path, self.system, self.name))
        crc_files = crc_to_check.infolist()
        crcs = []
        crc_info = {}
        for i in crc_files:
            crc = str(hex(i.CRC)[2:].zfill(8))
            crc = crc.upper()
            crc_info["compress_name"] = i.filename
            crc_info["crc"] = crc
            crcs.append(dict(crc_info))
        return crcs

    def crc32_from_file(self):
        crc_to_check = os.path.join(self.rom_path, self.system, self.name)
        if os.path.isfile(crc_to_check):
            buf = open(crc_to_check, 'rb').read()
            buf = (binascii.crc32(buf) & 0xFFFFFFFF)
            return "%08X" % buf


def main():
    system = "Sega 32x"
    rom_name = "After Burner (Japan, USA).zip"
    rom = Rom(system=system, name=rom_name)

    print(rom.crc)
    rom.compress()
    rom.rename_extension()


if __name__ == "__main__":
    main()
