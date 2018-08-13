import os

from rocketlauncher import RocketLauncher


def main():
    nes = "Nintendo Entertainment System"
    snes = "Super Nintendo Entertainment System"
    atari = "Atari 2600"
    sega = "Sega Genesis"
    n64 = "Nintendo 64"

    rl = RocketLauncher(system=n64)

    rl.new_system()


if __name__ == "__main__":
    main()
