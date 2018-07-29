import os

from general import Paths, Compressor


def main():
    system = "Nintendo Entertainment System"
    rom = "3-D WorldRunner (USA).nes"
    zip = "3-D WorldRunner (USA).zip"
    seven_zip = "3-D WorldRunner (USA).7z"
    rar = "3-D WorldRunner (USA).rar"
    test = "test.7z"

    p = Paths()
    source_file = os.path.join(p.rom_path, system, test)

    cf = Compressor(src_file=source_file)
    # cf.compress(ext="7z", remove_source=False)

    info = cf.get_crc()
    cf.extract("1942 (Japan, USA).nes", dst_dir=p.rom_path)


if __name__ == "__main__":
    main()
