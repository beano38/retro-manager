import time
import logging
import os
import xml.etree.cElementTree as ET

import requests
from bs4 import BeautifulSoup

from general import FrontEnd

TIME_STAMP = time.strftime(" %Y%m%d")

LOG_FILE = "arcade.log"
LOG_STAMP = time.strftime("%Y-%m-%d %H:%M:%S")
LOG_FORMAT = logging.Formatter("[{}] [%(levelname)s] [%(name)s] : %(message)s".format(LOG_STAMP))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(LOG_FORMAT)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(LOG_FORMAT)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class Databases(FrontEnd):

    def __init__(self, system):
        FrontEnd.__init__(self)

        self.system = system

    def read_system_xml(self):
        """
        "read_system_xml" Method returns info in a dictionary from the
        selected system's database

        Args:
            self

        Returns:
            List of Dictionaries for system header and system roms

        Raises:
            None
        """
        xml = os.path.join(self.db_path, self.system + ".xml")

        msg = "Extracting ROM info from {} . . .".format(self.system)
        logger.info(msg)

        tree = ET.parse(xml)
        doc = tree.getroot()

        # Read Header
        system = {}
        for header in doc.iter("header"):
            for dat in header.iter():
                system[dat.tag] = dat.text
        # Iterate thru the ROMs
        rom = {}
        roms = []
        for game in doc.iter('game'):
            rom['name'] = game.get('name')
            rom['image'] = game.get('image')
            rom['index'] = game.get('index')
            rom['have'] = False
            rom['artwork1'] = False
            rom['artwork2'] = False
            rom['artwork3'] = False
            rom['artwork4'] = False
            rom['wheel'] = False
            rom['video'] = False
            rom['theme'] = False

            for dat in game.iter():
                rom[dat.tag] = dat.text
            roms.append(dict(rom))

        for rom in roms:
            if rom["crc"]:
                rom["crc"] = rom["crc"].zfill(8).upper()

        return system, roms


class HyperList(FrontEnd):

    def __init__(self, system):
        FrontEnd.__init__(self)

        self.system = system

    def _get_hyperlist(self):
        """
        "get_hyperlist" Method downloads the HTML file from the URL for later use and
        returns a dictionary with info for the specified system

        Args:
            self

        Returns:
            parsed dictionary from the URL for the specified system

        Raises:
            None
        """
        url = "http://hyperlist.hyperspin-fe.com/"

        hyper_list_html = os.path.join(self.temp_path, "hyperlist" + TIME_STAMP + ".html")

        if os.path.exists(hyper_list_html):
            msg = "Using cached version of {}. The cache is good for one day".format(url)
            logger.info(msg)
            with open(hyper_list_html, "r") as data:
                soup = BeautifulSoup(data, "html.parser")
        else:
            msg = "Saving {} version for later use".format(url)
            logger.info(msg)
            r = requests.get(url)
            with open(hyper_list_html, "w") as data:
                data.write(r.text)
            soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find_all("table", attrs={"class": "tborder"})
        table = table[1]
        tbody = table.find('tbody')

        rows = tbody.find_all('tr')
        hyper_list = []
        hl = {}
        for row in rows:
            cols = row.find_all('td')
            hl["name"] = cols[0].text.strip()
            hl["count"] = cols[1].text.strip()
            hl["version"] = cols[2].text.strip()
            hl["last_update"] = cols[3].text.strip()
            hl["who"] = cols[4].text.strip()

            downloads = cols[5]
            links = downloads.find_all("a", href=True)
            if len(links) > 0:
                hl["link"] = url + links[0]["href"]
            else:
                hl["link"] = ""

            hyper_list.append(dict(hl))

        hyper_list_info = None

        for i in hyper_list:
            if self.system == i["name"]:
                hyper_list_info = i

        return hyper_list_info

    def download_db(self):
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        db_path = os.path.join(self.db_path, self.system + ".xml")
        try:
            url = self._get_hyperlist()["link"]
            response = requests.get(url)
            if response.status_code == 200:
                with open(db_path, mode="wb") as xml:
                    xml.write(response.content)
                return True
            else:
                return False
        except Exception as e:
            logger.debug(e)
            return False


class HyperSpin(Databases, HyperList):

    def __init__(self, system=None):
        Databases.__init__(self, system)
        HyperList.__init__(self, system)

        self.system = system

        # HyperSpin Paths
        self.db_path = os.path.join(self.hs_path, "Databases", self.system)
        self.media_path = os.path.join(self.hs_path, "Media", self.system)
        self.settings_path = os.path.join(self.hs_path, "Settings")
        # Images
        self.images_path = os.path.join(self.media_path, "Images")
        self.artwork1_path = os.path.join(self.images_path, "Artwork1")
        self.artwork2_path = os.path.join(self.images_path, "Artwork2")
        self.artwork3_path = os.path.join(self.images_path, "Artwork3")
        self.artwork4_path = os.path.join(self.images_path, "Artwork4")
        self.backgrounds_path = os.path.join(self.images_path, "Backgrounds")
        self.genre_backgrounds_path = os.path.join(self.images_path, "Genre", "Backgrounds")
        self.genre_wheel_path = os.path.join(self.images_path, "Genre", "Wheel")
        self.letters_path = os.path.join(self.images_path, "Letters")
        self.other_path = os.path.join(self.images_path, "Other")
        self.particle_path = os.path.join(self.images_path, "Particle")
        self.special_path = os.path.join(self.images_path, "Special")
        self.wheel_path = os.path.join(self.images_path, "Wheel")
        # Other Media
        self.themes_path = os.path.join(self.media_path, "Themes")
        self.video_path = os.path.join(self.media_path, "Video")


if __name__ == "__main__":
    platform = "Nintendo Entertainment System"
    hs = HyperSpin(platform)
    # header, roms = hs.read_system_xml()
    hs.download_db()


