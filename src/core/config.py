import os
from configparser import ConfigParser

from . import DEFAULT_BASEDIR as CORE_BASEDIR


config = ConfigParser()
config.read(os.path.join(CORE_BASEDIR, "config.ini"))
