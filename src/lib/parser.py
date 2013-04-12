# -*- coding: utf-8 -*-

# Parsers metaclass
import gzip
import os
import time

from lib import common

class SysAn_Parser:
    def __init__(self):
        common.LOGGER.print_data("Executing parser: {0} ({1})".format(self.parser_name, self.parser_description))
        #common.LOGGER.get_logger_namespace(self.parser_name)

        self.root_dir = common.ROOT_DIR
        self.distro = common.DISTRO

        self.config = common.CONFIG

        self.logs_list = []

        # Developer mode enabled? :)
        if self.config["parsers"]["override_day_to_analyze"] == "yes":
            # Overriding date to parse.
            date_string = time.strptime(self.config["parsers"]["day_to_analyze"], "%Y-%m-%d")
            self.day_raw = date_string[2]
        else:
            # Use current date.
            date_string = time.localtime()
            if self.config["parsers"]["analyze_previous_day"] == "yes":
                self.day_raw = date_string[2] - 1

        self.year = date_string[0]
        # Raw month. Can be 2digit or 1digit.
        self.month_raw = date_string[1]
        # If length of "month_raw" string is 1 - append zero to it.
        if len(str(self.month_raw)) == 1:
            self.month = "{0}{1}".format("0", self.month_raw)
        else:
            self.month = self.month_raw
        # ...and do it also for day
        if len(str(self.day_raw)) == 1:
            self.day = "{0}{1}".format("0", self.day_raw)
        else:
            self.day = self.day_raw
        self.month_hr = time.strftime("%b", date_string)

        # Constructing date for other modules/parsers usage.
        # Dirty and must be rewritten.
        if common.DATE == "":
            common.set_date("{0}-{1}-{2}".format(self.year, self.month, self.day))

    def add_to_log(self, text):
        common.LOGGER.add_to_log(self.parser_name, text)

    def get_logs_list(self, log_name):
        """
        Get logs list for parser.
        """
        logs_list = os.listdir(self.root_dir + "/var/log")
        for item in logs_list:
            if "gz" in item:
                if self.config[self.parser_name.lower()]["parse_compressed"] == "yes":
                    if log_name in item:
                        self.logs_list.append(self.root_dir + "/var/log/" + item)
            else:
                if log_name in item:
                    self.logs_list.append(self.root_dir + "/var/log/" + item)

    def read_file(self, file_name):
        """
        Read file and return a list, splitted by line break.
        """
        if "gz" in file_name:
            data = gzip.open(file_name, "r")
            data = data.read()
            data = str(data).split("\n")
        else:
            data = open(file_name, "r")

        return data