import os
import configparser


class ControlPanel:

    def __init__(self):

        self.p1_d_up = None
        self.p1_d_down = None
        self.p1_d_left = None
        self.p1_d_right = None
        self.p1_start = None
        self.p1_coin = None
        self.p1_b1 = None
        self.p1_b2 = None
        self.p1_b3 = None
        self.p1_b4 = None
        self.p1_b5 = None
        self.p1_b6 = None
        self.p1_b7 = None
        self.p1_b8 = None

        self.p2_d_up = None
        self.p2_d_down = None
        self.p2_d_left = None
        self.p2_d_right = None
        self.p2_start = None
        self.p2_coin = None
        self.p2_b1 = None
        self.p2_b2 = None
        self.p2_b3 = None
        self.p2_b4 = None
        self.p2_b5 = None
        self.p2_b6 = None
        self.p2_b7 = None
        self.p2_b8 = None

        self.b1 = None
        self.b2 = None
        self.b3 = None
        self.b4 = None
        self.b5 = None
        self.b6 = None

        self.read_controls_ini()

    def set_p1(self):
        self.p1_d_up = input("Player 1 Up: ")
        self.p1_d_down = input("Player 1 Down: ")
        self.p1_d_left = input("Player 1 Left: ")
        self.p1_d_right = input("Player 1 Right: ")
        self.p1_start = input("Player 1 Start: ")
        self.p1_coin = input("Player 1 Coin: ")
        self.p1_b1 = input("Player 1 Button 1: ")
        self.p1_b2 = input("Player 1 Button 2: ")
        self.p1_b3 = input("Player 1 Button 3: ")
        self.p1_b4 = input("Player 1 Button 4: ")
        self.p1_b5 = input("Player 1 Button 5: ")
        self.p1_b6 = input("Player 1 Button 6: ")
        self.p1_b7 = input("Player 1 Button 7: ")
        self.p1_b8 = input("Player 1 Button 8: ")

        self.player_1 = {"up": self.p1_d_up, "down": self.p1_d_down, "left": self.p1_d_left, "right": self.p1_d_right,
                         "start": self.p1_start, "coin": self.p1_coin, "b1": self.p1_b1, "b2": self.p1_b2, "b3": self.p1_b3,
                         "b4": self.p1_b4, "b5": self.p1_b5, "b6": self.p1_b6, "b7": self.p1_b7, "b8": self.p1_b8}

    def set_p2(self):
        self.p2_d_up = input("Player 2 Up: ")
        self.p2_d_down = input("Player 2 Down: ")
        self.p2_d_left = input("Player 2 Left: ")
        self.p2_d_right = input("Player 2 Right: ")
        self.p2_start = input("Player 2 Start: ")
        self.p2_coin = input("Player 2 Coin: ")
        self.p2_b1 = input("Player 2 Button 1: ")
        self.p2_b2 = input("Player 2 Button 2: ")
        self.p2_b3 = input("Player 2 Button 3: ")
        self.p2_b4 = input("Player 2 Button 4: ")
        self.p2_b5 = input("Player 2 Button 5: ")
        self.p2_b6 = input("Player 2 Button 6: ")
        self.p2_b7 = input("Player 2 Button 7: ")
        self.p2_b8 = input("Player 2 Button 8: ")

    def read_controls_ini(self):
        ini = os.path.join(os.path.dirname(__file__), "..", "Settings", "controls.ini")
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        self.p1_d_up = config.get("player 1", "up")
        self.p1_d_down = config.get("player 1", "down")
        self.p1_d_left = config.get("player 1", "left")
        self.p1_d_right = config.get("player 1", "right")
        self.p1_start = config.get("player 1", "start")
        self.p1_coin = config.get("player 1", "coin")
        self.p1_b1 = config.get("player 1", "b1")
        self.p1_b2 = config.get("player 1", "b2")
        self.p1_b3 = config.get("player 1", "b3")
        self.p1_b4 = config.get("player 1", "b4")
        self.p1_b5 = config.get("player 1", "b5")
        self.p1_b6 = config.get("player 1", "b6")
        self.p1_b7 = config.get("player 1", "b7")
        self.p1_b8 = config.get("player 1", "b8")

        self.p2_d_up = config.get("player 2", "up")
        self.p2_d_down = config.get("player 2", "down")
        self.p2_d_left = config.get("player 2", "left")
        self.p2_d_right = config.get("player 2", "right")
        self.p2_start = config.get("player 2", "start")
        self.p2_coin = config.get("player 2", "coin")
        self.p2_b1 = config.get("player 2", "b1")
        self.p2_b2 = config.get("player 2", "b2")
        self.p2_b3 = config.get("player 2", "b3")
        self.p2_b4 = config.get("player 2", "b4")
        self.p2_b5 = config.get("player 2", "b5")
        self.p2_b6 = config.get("player 2", "b6")
        self.p2_b7 = config.get("player 2", "b7")
        self.p2_b8 = config.get("player 2", "b8")

        self.b1 = config.get("other", "b1")
        self.b2 = config.get("other", "b2")
        self.b3 = config.get("other", "b3")
        self.b4 = config.get("other", "b4")
        self.b5 = config.get("other", "b5")
        self.b6 = config.get("other", "b6")


def main():
    cp = ControlPanel()
    print(cp.p1_d_left)


if __name__ == "__main__":
    main()
