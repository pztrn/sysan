# -*- coding: utf-8 -*-

# Common module - a very useful piece of shit.

# SysAn configuration
CONFIG = {}
# Distro tuple
DISTRO = ""
# Logger instance
LOGGER = ""
# Root directory, e.g. for chroot override.
ROOT_DIR = ""
# Cronjob?
CRON = False
# Date to analyze.
DATE = ""

def set_config(config):
    global CONFIG
    CONFIG = config

def set_distro(distro):
    global DISTRO
    DISTRO = distro

def set_logger(logger):
    global LOGGER
    LOGGER = logger

def set_root_dir(root_dir):
    global ROOT_DIR
    ROOT_DIR = root_dir

def set_cronjob():
    print("Cron mode enabled.")
    global CRON
    CRON = True

def set_date(date):
    global DATE
    DATE = date