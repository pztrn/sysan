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

        # Get LogAn path
        self.path = "/".join(sys.modules["lib.config"].__file__.split("/")[:-2])

        self.config = configparser.ConfigParser()

        # Check for config existing.
        if os.path.exists(os.path.expanduser("~/.config/logan/conf.d/")):
            config_path = os.path.expanduser("~/.config/logan/conf.d/")
        elif os.path.exists(os.path.join(self.path, "conf.d")):
            config_path = os.path.join(self.path, "conf.d")
        else:
            config_path = "/etc/logan/conf.d/"

        self.print_data("Configuration found in: {0}".format(config_path))
        self.print_data("Loading configuration...")

        # Load configuration from conf.d directory.
        try:
            for filename in os.listdir(config_path):
                # Configuration file MUST ended with ".conf"
                if filename[-5:] == ".conf":
                    # Lets try to load config.
                    self.config.read(os.path.join(config_path, filename))
        except:
            raise Config_Load_Failed

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

class Config_Load_Failed(Sysan_Exception):
    """
    Raises when SysAn failed to load configuration file.
    """
    def __init__(self):
        print("Failed to load SysAn configuration!")
        exit(2)