import logging
import time
import os
import shutil

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


def move_chd_to_root(chd_path):
    """
    "move_chd_to_root" Method moves a .CHD file up one level in the directory structure.
    This is needed when one downloads a merged CHD set and MAME is setup for
    split CHD set.  Afterwards, run clrmamepro scanner to fix

    Args:
        chd_path(required, default=None): Path of MAME machine to fix

    Returns:
        None

    Raises:
        None
    """
    dirs = os.listdir(chd_path)

    file_list = []
    for item in dirs:
        if os.path.isdir(os.path.join(chd_path, item)):
            files = os.listdir(os.path.join(chd_path, item))
            for f in files:
                file_list.append(os.path.join(chd_path, item, f))

    for f in file_list:
        dst = os.path.join(chd_path, os.path.basename(f))
        if os.path.isfile(dst):
            msg = "CHD {} exists already, deleting duplicate".format(f)
            logger.info(msg)
            os.remove(f)
        else:
            shutil.move(f, dst)
            msg = "CHD {} moved".format(os.path.basename(f))
            logger.info(msg)


if __name__ == "__main__":
    print(move_chd_to_root.__doc__)
    chd_path = "X:\\Software Lists\\psx"
    move_chd_to_root(chd_path)
