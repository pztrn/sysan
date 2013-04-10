# -*- coding: utf-8 -*-

# Mail log parser
import os

from lib.parser import SysAn_Parser

class MAIL_Parser(SysAn_Parser):
    parser_name = "MAIL"
    parser_description = "Mail logs parser"
    parser_author = "Stanislav N. aka pztrn"
    parser_author_email = "pztrn@pztrn.name"

    def __init__(self):
        SysAn_Parser.__init__(self)

        self.mail_logs = []

        self.to_log = {}

    def execute(self):
        # Get list of SSH logs files.
        logs_list = os.listdir(self.root_dir + "/var/log")
        for item in logs_list:
            if "gz" in item:
                if self.config["mail"]["parse_compressed"] == "yes":
                    if logs[self.distro[0]] in item:
                        self.mail_logs.append(self.root_dir + "/var/log/" + item)
            else:
                if logs[self.distro[0]] in item:
                    self.mail_logs.append(self.root_dir + "/var/log/" + item)

        self.format_log()

    def format_log(self):
        """
        Format parsed data into logger-compatible format.
        """
        self.to_log["header"] = "Mail Daemons statistics"
        self.to_log["data"] = "TBD"
        self.add_to_log(self.to_log)

logs = {
    "arch"      : "mail.log",
    "debian"    : "mail.log"
}