#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SysAn - System Analyzer.
# Copyright (C) 2012-2013, Stanislav N. (pztrn) <pztrn@pztrn.name>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
import sys

from lib import common
from lib import config
from lib import distro_detector
from lib import exceptions
from lib import logger
from lib import mailer

class SysAn:
    """
    Hello, this is SysAn.
    """
    def __init__(self):
        # Parse options
        self.parse_options()

        # Creating config instance.
        self.config = config.Configuration().get_config()
        common.set_config(self.config)

        # Detect distro.
        self.distro_detector = distro_detector.Distro_Detector()
        self.distro_detector.detect_distro()

        # Create logger instance and make it global thru "common"
        # module.
        self.logger = logger.Logger()
        common.set_logger(self.logger)

        # Get parsers list from config, import them and execute.
        # "[1:]" and "[:-1]" are required for doublequotes elimination.
        parsers_list = self.config["parsers"]["parsers"][1:][:-1].split()
        
        for parser in parsers_list:
            try:
                __import__("parsers." + parser)
                pm = sys.modules["parsers." + parser]
                exec("self.pm = pm." + parser.upper() + "_Parser()")
            except:
                raise exceptions.Parser_Load_Failure(parser)

            try:
                self.pm.execute()
            except:
                raise exceptions.Parser_Execute_Failure(parser)

        # Produce logger output after all.
        data = self.logger.produce_output()

        # If mailer enabled - send an email.
        if self.config["mailer"]["enabled"] == "yes":
            self.mailer = mailer.Mailer()
            self.mailer.process_mail(data)

    def parse_options(self):
        """
        Parse SysAn options.
        """
        options = sys.argv[1:]

        if "-h" in options or "--help" in options:
            self.show_help()
            exit()

        # Root directory.
        if "-r" in options or "--root" in options:
            # Get index.
            try:
                index = options.index("-r")
            except:
                index = options.index("--root")

            root_dir = options[index + 1]
            # Remove item from options.
            options.pop(index + 1)
            options.pop(index)

            # Set root directory.
            common.set_root_dir(root_dir)
        else:
            common.set_root_dir("/")

        # Cronjob.
        if "-c" in options or "--cronjob" in options:
            # Get index.
            try:
                index = options.index("-c")
            except:
                index = options.index("--cronjob")
            # Remove item from options.
            options.pop(index)

            # Set cronjob mode.
            common.set_cronjob()

    def show_help(self):
        """
        Show help message.
        """
        print("""SysAn - System log Analyzer.
Copyright (c) 2013, Stanislav N. aka pztrn <pztrn@pztrn.name>

Syntax:
    ./sysan.py [-r|--root root dir] [-c|--cronjob] [-h]

Available options:
    -r, --root      Override root directory. Useful for parsing
                    logs inside chroot environment or for
                    testing.
    -c, --cronjob   Disable all output. Designed to run with cron.
    -h, --help      This message

Report bugs at https://github.com/pztrn/sysan/issues""")

if __name__ == "__main__":
    SysAn()
else:
    print("SysAn doesn't designed to be imported somewhere!")