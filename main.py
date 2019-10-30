import os
import time

from rocketlauncher import RocketLauncher
from hyperspin import HyperSpin
from models.system import System


def install_arcade(fe="HyperSpin"):
    rl = RocketLauncher(system="MAME")
    rl.install()
    if fe == "HyperSpin" or fe == "all":
        hs = HyperSpin(system="MAME")
        hs.install()
    elif fe == "RetroFE" or fe == "all":
        pass
    elif fe == "MaLa" or fe == "all":
        pass


def create_system(system, fe="HyperSpin"):
    rl = RocketLauncher(system=system)
    rl.new_system()

    # Build ROM set
    platform = System(system=system)
    curated_sets = platform.tosec_dirs() + platform.software_lists + platform.nointro + platform.goodset
    platform.build_rom_set(source_set=curated_sets)

    # Set up Media
    rl.set_up_media(action="link")
    if fe == "HyperSpin" or fe == "all":
        hs = HyperSpin(system=system)
        hs.new_system(action="link", three_d=False)
    elif fe == "RetroFE" or fe == "all":
        pass
    elif fe == "MaLa" or fe == "all":
        pass


def update_system(system, source_set, action="copy", three_d=False, fe="HyperSpin", update_rl_media=False):
    # Build ROMs of missing ROMs
    platform = System(system=system)
    if len(source_set) == 0:
        curated_sets = platform.tosec_dirs() + platform.software_lists + platform.nointro + platform.goodset
        platform.build_rom_set(source_set=curated_sets)
    else:
        platform.build_rom_set(source_set=source_set)
    # Update the Media
    if update_rl_media:
        rl = RocketLauncher(system=system)
        rl.set_up_media(action="link")

    if fe == "HyperSpin" or fe == "all":
        hs = HyperSpin(system=system)
        hs.update_system(action=action, three_d=three_d)
    elif fe == "RetroFE" or fe == "all":
        pass
    elif fe == "MaLa" or fe == "all":
        pass


def delete_system(system, fe="HyperSpin", remove_assets=False):
    rl = RocketLauncher(system=system)
    rl.remove_system(remove_media=remove_assets)

    if fe == "HyperSpin" or fe == "all":
        hs = HyperSpin(system=system)
        hs.remove_system(remove_media=remove_assets)
    elif fe == "RetroFE" or fe == "all":
        pass
    elif fe == "MaLa" or fe == "all":
        pass


def bunch_of_new_stuff(group):
    for i in group:
        create_system(system=i, fe="all")
        update_system(system=i,
                      source_set=[r"N:\Arcade\ROMs\{}".format(i), r"R:\Unmatched\Cart\{}".format(i)],
                      action="link",
                      three_d=False,
                      fe="all",
                      update_rl_media=False)


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
    sg1k = "Sega SG-1000"
    sms = "Sega Master System"
    gen = "Sega Genesis"
    pico = "Sega Pico"
    s32 = "Sega 32x"
    gg = "Sega Game Gear"
    sfx = "NEC SuperGrafx"
    tg16 = "NEC TurboGrafx-16"
    pce = "NEC PC Engine"
    ngp = "SNK Neo Geo Pocket"
    ngc = "SNK Neo Geo Pocket Color"
    aes = "SNK Neo Geo AES"
    mvs = "SNK Neo Geo MVS"
    itv = "Mattel Intellivision"
    cv = "ColecoVision"
    mame = "MAME"
    ps1 = "Sony Playstation"
    ps2 = "Sony Playstation 2"
    psp = "Sony PSP"

    t1 = time.perf_counter()

    nintendo = [nes, nf, fds, snes, nsv, n64, gb, gba, gbc, vb]
    atari = [a26, a52, a78, jag, lynx]
    sega = [sg1k, sms, gen, pico, s32, gg]
    nec = [sfx, tg16, pce]
    snk = [ngp, ngc, aes, mvs]
    carts = [itv, cv]

    # install_arcade(fe="all")

    system = lynx
    # create_system(system=system, fe="all")
    update_system(system=system,
                  source_set=[r"N:\Arcade\ROMs\{}".format(system), r"R:\Unmatched\Cart\{}".format(system)],
                  action="link",
                  three_d=False,
                  fe="all",
                  update_rl_media=False)

    # delete_system(system=jag, remove_assets=True)

    # platform = System(system=system)
    # matches = platform.fuzzy_match_set(source_set=platform.nointro, assurance=.75, rename=True, compress=True)
    # matches = platform.fuzzy_match_set(
    #     source_set=[r"N:\Arcade\ROMs\{}".format(system), r"R:\Unmatched\Cart\{}".format(system)],
    #     assurance=.75, rename=True, compress=True)

    t2 = time.perf_counter()
    print("This took {} seconds".format(t2-t1))


if __name__ == "__main__":
    main()
