# -*- coding: utf-8 -*-

# Parsers metaclass
from lib import common

class SysAn_Parser:
    def __init__(self):
        common.LOGGER.print_data("Executing parser: {0} ({1})".format(self.parser_name, self.parser_description))
        #common.LOGGER.get_logger_namespace(self.parser_name)

        self.root_dir = common.ROOT_DIR
        self.distro = common.DISTRO

        self.config = common.CONFIG

    def add_to_log(self, text):
        common.LOGGER.add_to_log(self.parser_name, text)