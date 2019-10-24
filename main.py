import os
import time

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


def update_system(system, source_set=[]):
    # Build ROMs of missing ROMs
    platform = System(system=system)
    if len(source_set) == 0:
        curated_sets = platform.tosec_dirs() + platform.software_lists + platform.nointro + platform.goodset
        platform.build_rom_set(source_set=curated_sets)
    else:
        platform.build_rom_set(source_set=source_set)
    # Update the Media
    rl = RocketLauncher(system=system)
    # rl.set_up_media(action="link")


def update_system1(system, source_set=[]):
    import concurrent.futures
    # Build ROMs of missing ROMs
    platform = System(system=system)
    rl = RocketLauncher(system=system)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if len(source_set) == 0:
            curated_sets = platform.tosec_dirs() + platform.software_lists + platform.nointro + platform.goodset
            executor.submit(platform.build_rom_set, curated_sets)
        else:
            executor.submit(platform.build_rom_set, source_set)
        # Update the Media
        executor.submit(rl.set_up_media, action="link")


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
    sg1k = "Sega SG-1000"
    sms = "Sega Master System"
    gen = "Sega Genesis"
    pico = "Sega Pico"
    s32 = "Sega 32x"
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

    t1 = time.perf_counter()

    nintendo = [nes, nf, fds, snes, nsv, n64, gb, gba, gbc, vb]
    atari = [a26, a52, a78, jag, lynx]
    sega = [sg1k, sms, gen, pico, s32, gg]

    # install_arcade()
    # create_system(system=jag)
    # delete_system(system=jag, remove_assets=True)

    dirs = [x[0] for x in os.walk(r"T:\Downloads\NESroms")]
    update_system(system=nes, source_set=dirs)

    platform = System(system=nes)

    # matches = platform.fuzzy_match_set(source_set=["N:\Arcade\ROMs\{}".format(nes)], assurance=.75)
    # for i in matches:
    #     print(i)

    # build = [create_system(build) for build in sega]
    # delete = [delete_system(system=delete, remove_assets=True) for delete in nintendo]

    # for plat in atari:
    #     other_sets = [r"N:\Arcade\ROMs\{}".format(plat), r"R:\Unmatched\Cart\{}".format(plat)]
    #     update_system(system=plat, source_set=other_sets)

    t2 = time.perf_counter()
    print("This took {} seconds".format(t2-t1))


if __name__ == "__main__":
    main()
