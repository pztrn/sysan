# -*- coding: utf-8 -*-

# Parsers metaclass
import time

from lib import common

class SysAn_Parser:
    def __init__(self):
        common.LOGGER.print_data("Executing parser: {0} ({1})".format(self.parser_name, self.parser_description))
        #common.LOGGER.get_logger_namespace(self.parser_name)

        self.root_dir = common.ROOT_DIR
        self.distro = common.DISTRO

        self.config = common.CONFIG

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