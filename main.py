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
    # Set up Media
    rl.set_up_media(action="link")


def update_roms(system, source_set):
    platform = System(system=system)
    platform.build_rom_set(source_set=source_set)


def delete_system(system, remove_assets=False):
    rl = RocketLauncher(system=system)
    rl.remove_system(remove_media=remove_assets)


def main():
    nes = "Nintendo Entertainment System"
    nf = "Nintendo Famicom"
    fds = "Nintendo Famicom Disk System"
    snes = "Super Nintendo Entertainment System"
    nsv = "Nintendo Satellaview"
    n64 = "Nintendo 64"
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
    gg = "Sega Game Gear"
    tg16 = "NEC TurboGrafx-16"
    pce = "NEC PC Engine"
    ngp = "SNK Neo Geo Pocket"
    ngc = "SNK Neo Geo Pocket Color"
    itv = "Mattel Intellivision"
    mame = "MAME"
    ps1 = "Sony Playstation"
    ps2 = "Sony Playstation 2"
    psp = "Sony PSP"

    nintendo = [nes, nf, fds, snes, nsv, n64, gb, gba, gbc, vb]
    atari = [a26, a52, a78, jag, lynx]
    sega = [sms, gen, gg]

    # install_arcade()
    create_system(system=nsv)
    # delete_system(system=a52, remove_assets=True)

    other_set = [r"N:\Arcade\ROMs\{}".format(nes)]
    other_set = [r"R:\Unmatched\Cart\{}".format(nes)]
    # update_roms(system=nes, source_set=other_set)

    # build = [create_system(build) for build in nintendo]
    # delete = [delete_system(system=delete, remove_assets=True) for delete in nintendo]


if __name__ == "__main__":
    main()
