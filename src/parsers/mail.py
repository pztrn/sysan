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

        self.to_log = {
            "mails"             : {
                "sent"          : {},
                "rejected"      : {}
            },
            "connections"       : {
                "accepted"      : {
                    "incoming"  : {
                        "total" : 0
                    },
                    "outgoing"  : {
                        "total" : 0
                    }
                },
                "rejected"      : {
                    "incoming"  : {
                        "total" : 0
                    },
                    "outgoing"  : {
                        "total" : 0
                    }
                }
            },
            "spam"              : {
                "filtered"      : 0,
                "not_filtered"  : 0
            }
        }

    def execute(self):
        # Get logs list.
        self.get_logs_list(logs[self.distro[0]])

        # Let's roll!
        for filename in self.logs_list:
            self.parse_log(filename)

        # Format data
        self.format_log()

    def parse_log(self, filename):
        """
        Parse log.
        """
        file_data = self.read_file(filename)
        for line in file_data:
            # Parse line :)
            self.process_line(line)

    def process_line(self, line):
        """
        Parse log line.
        """
        if int(line.split()[1]) == self.day_raw and line.split()[0] == self.month_hr:
            if self.config["mailservers"]["incoming_server"] == "dovecot":
                if "dovecot" in line:
                    self.process_dovecot_line(line)
            if self.config["mailservers"]["outgoing_server"] == "postfix":
                if "postfix" in line:
                    self.process_postfix_line(line)
            if self.config["mailservers"]["antispam_server"] == "spamassassin":
                if "spamd" in line:
                    self.process_spamassassin_line(line)

    def process_dovecot_line(self, line):
        """
        Parse dovecot log line.
        """
        if "Login" in line:
            try:
                self.username = line.split()[7].split("=")[1][1:][:-2]
                if self.username not in self.to_log["connections"]["accepted"]["incoming"]:
                    self.to_log["connections"]["accepted"]["incoming"][self.username] = 0
                else:
                    self.to_log["connections"]["accepted"]["incoming"][self.username] += 1
            except:
                # No username in line
                pass
            self.to_log["connections"]["accepted"]["incoming"]["total"] += 1

        if "unknown user" in line:
            user_name = line.split()[6].split("(")[1].split(",")
            self.username = user_name[0] + "@" + user_name[1][:-2]
            if self.username not in self.to_log["connections"]["rejected"]["incoming"]:
                self.to_log["connections"]["rejected"]["incoming"][self.username] = 0
            else:
                self.to_log["connections"]["rejected"]["incoming"][self.username] += 1

            try:
                self.to_log["connections"]["accepted"]["incoming"][self.username] -= 1
                self.to_log["connections"]["accepted"]["incoming"]["total"] -= 1
            except:
                # Username not in "accepted". Passing.
                pass
            self.to_log["connections"]["rejected"]["incoming"]["total"] += 1

    def process_postfix_line(self, line):
        """
        Parse postfix log line.
        """
        pass

    def process_spamassassin_line(self, line):
        """
        Parse spamassassin log line.
        """
        pass

    def format_log(self):
        """
        Format parsed data into logger-compatible format.
        """
        total_accepted = self.to_log["connections"]["accepted"]["incoming"]["total"]
        total_rejected = self.to_log["connections"]["rejected"]["incoming"]["total"]
        del(self.to_log["connections"]["accepted"]["incoming"]["total"])
        del(self.to_log["connections"]["rejected"]["incoming"]["total"])
        self.to_log["header"] = "Mail Daemons statistics"

        text = ""
        text += "Connections statistics\n"
        text += "<!-- delimiter3 -->"
        text += "Accepted incoming connections: {0}\n".format(total_accepted)
        text += "By users:\n"
        for user in self.to_log["connections"]["accepted"]["incoming"]:
            text += "  * {0} ({1} connections)\n".format(user, self.to_log["connections"]["accepted"]["incoming"][user])

        text += "<!-- delimiter2 -->"
        text += "Rejected incoming connections: {0}\n".format(total_rejected)
        text += "By users:\n"
        for user in self.to_log["connections"]["rejected"]["incoming"]:
            text += "  * {0} ({1} connections)\n".format(user, self.to_log["connections"]["rejected"]["incoming"][user])
        text += "<!-- delimiter2 -->"


        self.to_log["data"] = text
        self.add_to_log(self.to_log)

logs = {
    "arch"      : "mail.log",
    "debian"    : "mail.log"
}