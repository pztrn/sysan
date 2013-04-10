# -*- config: utf-8 -*-

# Distro detector module. Detects distro
import os
import platform

from lib import common

class Distro_Detector:
    def __init__(self):
        pass

    def detect_distro(self):
        distro_name = platform.linux_distribution()

        common.set_distro(distro_name)