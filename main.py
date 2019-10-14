import os

from rocketlauncher import RocketLauncher
from models.system import System


def install_arcade():
    rl = RocketLauncher(system="Nintendo Entertainment System")
    rl.install()


def create_system(system):
    rl = RocketLauncher(system=system)
    rl.new_system()
    # Build ROM set
    platform = System(system=system)
    curated_sets = platform.tosec_dirs() + platform.software_lists + platform.nointro + platform.goodset
    platform.build_rom_set(source_set=curated_sets)


def delete_system(system, remove_assets=False):
    rl = RocketLauncher(system=system)
    rl.remove_system(remove_media=remove_assets)


def main():
    nes = "Nintendo Entertainment System"
    snes = "Super Nintendo Entertainment System"
    gb = "Nintendo Game Boy"
    gba = "Nintendo Game Boy Advance"
    gbc = "Nintendo Game Boy Color"
    vb = "Nintendo Virtual Boy"
    a26 = "Atari 2600"
    a52 = "Atari 5200"
    a78 = "Atari 7800"
    jag = "Atari Jaguar"
    lynx = "Atari Lynx"
    sms = "Sega Master System"
    gen = "Sega Genesis"
    tg16 = "NEC TurboGrafx-16"
    pce = "NEC PC Engine"
    ngp = "SNK Neo Geo Pocket"
    ngc = "SNK Neo Geo Pocket Color"
    itv = "Mattel Intellivision"
    mame = "MAME"
    ps1 = "Sony Playstation"
    ps2 = "Sony Playstation 2"
    psp = "Sony PSP"

    # install_arcade()
    create_system(system=gen)
    # delete_system(system=nes, remove_assets=True)


if __name__ == "__main__":
    main()
