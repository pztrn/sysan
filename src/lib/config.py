# -*- coding: utf-8 -*-

# Configuration for SysAn
import os
import sys
import configparser

from lib import common
from lib.exceptions import Sysan_Exception

class Configuration:
    def __init__(self):
        self.print_data("Starting configuration initialization...")
        self.config_read_failed = [False, False, False]

        # Get LogAn path
        self.path = "/".join(sys.modules["lib.config"].__file__.split("/")[:-2])

        self.config = configparser.ConfigParser()

        # Load configuration. First - from SysAn directory, 
        # then from /etc/sysan/conf.d/, and then from user home
        # directory
        self.print_data("Loading configuration...")
        if not os.path.exists(os.path.expanduser("~/.config/sysan/conf.d/")):
            if not os.path.exists("/etc/sysan/conf.d/"):
                if not os.path.exists(os.path.join(self.path, "conf.d")):
                    raise Config_Load_Failed
                else:
                    self.read_config(os.path.join(self.path, "conf.d"))
            else:
                self.read_config("/etc/sysan/conf.d/")
        else:
            self.read_config(os.path.expanduser("~/.config/sysan/conf.d/"))

    def get_config(self):
        """
        Returns a configuration.
        """
        return self.config

    def print_data(self, data):
        """
        """
        if not common.CRON:
            print(data)

    def read_config(self, config_path):
        """
        Reads configuration. Really.
        """
        print(config_path)
        for filename in os.listdir(config_path):
            # Configuration file MUST ended with ".conf"
            if filename[-5:] == ".conf":
                # Lets try to load config.
                self.config.read(os.path.join(config_path, filename))


class Config_Load_Failed(Sysan_Exception):
    """
    Raises when SysAn failed to load configuration file.
    """
    def __init__(self):
        print("Failed to load SysAn configuration!")
        exit(2)