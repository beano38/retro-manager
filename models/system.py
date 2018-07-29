import json
import os
import configparser

from gamesdb import GamesDB
from arcade import Arcade


class System(Arcade):

    def __init__(self, system=None, logLevel=3):
        Arcade.__init__(self, logLevel)
        self.system = system

        # --- GamesDB Attributes ---
        self.games_db_name = None
        self.games_db_id = None
        self.overview = None
        self.developer = None
        self.manufacturer = None
        self.cpu = None
        self.memory = None
        self.graphics = None
        self.sound = None
        self.display = None
        self.media = None
        self.maxcontrollers = None
        self.rating = None
        self.banners = None
        self.fanarts = None
        self.consoleart = None
        self.controllerart = None

        # ----- Model Attributes -----
        self.emulator = None
        self.extensions = None
        self.year = None
        self.platform_type = None

        self.tosec = None
        self.goodset = None
        self.nointro = None
        self.software_lists = None
        self.no_good_set = None

        try:
            self.read_model()
        except FileNotFoundError:
            msg = "SYS: Model for {} not defined".format(self.system)
            self.log(2, msg)

        # ----- ROM Set Paths -----
        try:
            self.tosecs = self.tosec_dirs()
        except:
            self.tosecs = None

    def parse_platform_list(self, try_name=None):
        gdb = GamesDB()
        system_list = gdb.get_platforms_list()
        # print(json.dumps(system_list, indent=4))
        systems = system_list["Data"]["Platforms"]["Platform"]
        systems_returned = []
        system = {}

        for sys in systems:
            if try_name:
                if try_name in sys["name"]:
                    system["id"] = sys["id"]
                    system["name"] = sys["name"]
                    systems_returned.append(dict(system))
            elif self.system in sys["name"]:
                system["id"] = sys["id"]
                system["name"] = sys["name"]
                systems_returned.append(dict(system))

        num = 1
        if len(systems_returned) > 1:
            for i in systems_returned:
                print("{}.  {}".format(num, i["name"]))
                num += 1

            prompt = input("\nPick a Number of the System you want:  ")
            pick = int(prompt) - 1
            print("You picked {}".format(systems_returned[pick]["name"]))
            system_id = systems_returned[pick]["id"]
            system_name = systems_returned[pick]["name"]
            return system_id
        elif len(systems_returned) == 1:
            system_id = systems_returned[0]["id"]
            system_name = systems_returned[0]["name"]
            return system_id
        else:
            split = self.system.split()
            new_sys = "{} {}".format(split[0], split[1])
            self.parse_platform_list(try_name=new_sys)
            system_id = 0
            system_name = "Nothing Found"
            return system_id

        # print(system_id, system_name)
        #
        # return system_id

    def create_system(self):
        system_id = self.parse_platform_list()

        def item_if(key, system):
            if key in system:
                return system[key]
            else:
                return None

        gdb = GamesDB()
        stuff = gdb.get_platform(platform_id=system_id)
        print(json.dumps(stuff, indent=4))
        baseImgUrl = stuff["Data"]["baseImgUrl"]
        system = stuff["Data"]["Platform"]
        self.games_db_name = system["Platform"]
        self.games_db_id = system["id"]
        self.overview = item_if("overview", system)
        self.developer = item_if("developer", system)
        self.manufacturer = item_if("manufacturer", system)
        self.cpu = item_if("cpu", system)
        self.memory = item_if("memory", system)
        self.graphics = item_if("graphics", system)
        self.sound = item_if("sound", system)
        self.display = item_if("display", system)
        self.media = item_if("media", system)
        self.maxcontrollers = item_if("maxcontrollers", system)
        self.rating = item_if("rating", system)

        # self.banners = [baseImgUrl + banner["#text"] for banner in stuff["Data"]["Platform"]["Images"]["banner"]]
        # print(stuff["Data"]["Platform"]["Images"]["boxart"]["#text"])
        # #     boxarts = [baseImgUrl + boxart["#text"] for boxart in stuff["Data"]["Platform"]["Images"]["boxart"]]
        # # else:
        # #     boxarts = stuff["Data"]["Platform"]["Images"]["boxart"]["#text"]
        # self.fanarts = [baseImgUrl + fanart["original"]["#text"] for fanart in system["Images"]["fanart"]]
        self.consoleart = baseImgUrl + item_if("consoleart", system["Images"])
        self.controllerart = baseImgUrl + item_if("controllerart", system["Images"])

    def write_system_json(self):
        self.create_system()
        json_file = "platforms.json"

        gamesdb = {}
        gamesdb["gamesdbname"] = self.games_db_name
        gamesdb["id"] = self.games_db_id
        gamesdb["overview"] = self.overview
        gamesdb["developer"] = self.developer
        gamesdb["manufacturer"] = self.manufacturer
        gamesdb["cpu"] = self.cpu
        gamesdb["memory"] = self.memory
        gamesdb["graphics"] = self.graphics
        gamesdb["sound"] = self.sound
        gamesdb["display"] = self.display
        gamesdb["media"] = self.media
        gamesdb["maxcontrollers"] = self.maxcontrollers
        gamesdb["rating"] = self.rating
        gamesdb["banners"] = self.banners
        gamesdb["fanarts"] = self.fanarts
        gamesdb["consoleart"] = self.consoleart
        gamesdb["controllerart"] = self.controllerart

        platform = {}
        platform[self.system] = dict(gamesdb)

        print(json.dumps(platform, indent=4))

        # with open(json_file, mode="a") as f:
        #     f.write(json.dumps(platform, indent=4))

    def write_system_ini(self):
        ini = "systems.ini"

        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini)

        if not config.has_section(self.system):
            msg = "PL: Adding {} to system.ini file".format(self.system)
            self.log(3, msg)
            config.add_section(self.system)
        else:
            msg = "PL: Adding attributes from GamesDB".format(self.system)
            self.log(3, msg)

        def if_none(item):
            if item:
                return item
            else:
                return ""

        config.set(self.system, "GamesDB_Name", self.games_db_name)
        config.set(self.system, "GamesDB_ID", self.games_db_id)
        config.set(self.system, "Overview", self.overview, )
        config.set(self.system, "Developer", self.developer)
        config.set(self.system, "Manufacturer", self.manufacturer)
        config.set(self.system, "CPU", self.cpu)
        config.set(self.system, "Memory", self.memory)
        config.set(self.system, "Graphics", self.graphics)
        config.set(self.system, "Sound", self.sound)
        config.set(self.system, "Display", self.display)
        config.set(self.system, "Media", self.media)
        config.set(self.system, "Max_Controllers", self.maxcontrollers)
        config.set(self.system, "Rating", if_none(self.rating))
        # config.set(self.system, "Banners", self.banners)
        # config.set(self.system, "Fan_Art", self.fanarts)
        config.set(self.system, "Console_Art", self.consoleart)
        config.set(self.system, "Controller_Art", self.controllerart)

        with open(ini, mode="w") as f:
            config.write(f, space_around_delimiters=True)

    # ----- TOSEC -----

    def tosec_dirs(self):
        path = os.path.join(self.mstr_tosec, self.manufacturer, self.tosec)
        dirs = [x[0] for x in os.walk(path)]

        return dirs

    # ----- Read System Model -----

    def read_model(self):
        model = os.path.join(os.path.dirname(__file__), "systems", self.system + ".json")
        with open(model, mode="r") as f:
            data = json.load(f)

        # print(json.dumps(data, indent=4))

        if "emulator" in data:
            self.emulator = data["emulator"]
        if "extensions" in data:
            self.extensions = data["extensions"]
        if "year" in data:
            self.year = data["year"]
        if "platformType" in data:
            self.platform_type = data["platformType"]

        if data["romSets"]["TOSEC"] is not None:
            self.tosec = data["romSets"]["TOSEC"]
        if data["romSets"]["GoodSet"] is not None:
            self.goodset = [os.path.join(self.mstr_good_set, data["romSets"]["GoodSet"])]
        if data["romSets"]["NoIntro"] is not None:

            if type(data["romSets"]["NoIntro"]) is str:
                self.nointro = [os.path.join(self.mstr_no_intro, data["romSets"]["NoIntro"])]
            else:
                dirs = []
                for stuff in data["romSets"]["NoIntro"]:
                    dirs.append(os.path.join(self.mstr_no_intro, stuff))
                self.nointro = dirs
        if data["romSets"]["SoftwareLists"] is not None:
            if type(data["romSets"]["SoftwareLists"]) is str:
                self.software_lists = [os.path.join(self.mstr_sl, data["romSets"]["SoftwareLists"])]
            else:
                dirs = []
                for stuff in data["romSets"]["SoftwareLists"]:
                    dirs.append(os.path.join(self.mstr_sl, stuff))
                self.software_lists = dirs
        if data["romSets"]["NoGoodSet"] is not None:
            self.no_good_set = [os.path.join(self.mstr_non_good_set, data["romSets"]["NoGoodSet"])]
        #     self.software_lists = [os.path.join(self.mstr_sl, data["romSets"]["SoftwareLists"])]

        games_db = data["GamesDbData"]["Platform"]
        self.manufacturer = games_db["manufacturer"]


def main():
    atari = "Atari 8-Bit"
    nes = "Nintendo Entertainment System"
    other = "Sony PSP"
    sys = System(system=other)
    # sys.create_system()
    # sys.write_system_json()
    # sys.write_system_ini()

    print(sys.tosecs)
    print(sys.goodset)
    print(sys.nointro)
    print(sys.software_lists)

    print(sys.platform_type)


if __name__ == "__main__":
    main()
