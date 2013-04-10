# -*- coding: utf-8 -*-

# SSHd logs parser.
import os
import time

from lib.parser import SysAn_Parser

class SSH_Parser(SysAn_Parser):
    parser_name = "SSH"
    parser_description = "SSH logs parser"
    parser_author = "Stanislav N. aka pztrn"
    parser_author_email = "pztrn@pztrn.name"

    def __init__(self):
        SysAn_Parser.__init__(self)

        self.ssh_logs = []
        self.data = {
            "accepted": {},
            "rejected": {}
        }

    def execute(self):
        """
        Analyze SSHd logs, count uniques IPs.
        """
        # Get list of SSH logs files.
        logs_list = os.listdir(self.root_dir + "/var/log")
        for item in logs_list:
            if "gz" in item:
                if self.config["ssh"]["parse_compressed"] == "yes":
                    if logs[self.distro[0]] in item:
                        self.ssh_logs.append(self.root_dir + "/var/log/" + item)
            else:
                if logs[self.distro[0]] in item:
                    self.ssh_logs.append(self.root_dir + "/var/log/" + item)

        # Let's roll!
        for filename in self.ssh_logs:
            self.parse_log(filename)

        # Format data
        self.format_data()

    def parse_log(self, filename):
        """
        Parse specified file.
        """
        file_data = open(filename, "r").read().split("\n")
        for line in file_data:
            if "Accepted" in line:
                month = time.strftime("%b", time.localtime())
                day = time.localtime()[2]
                if int(line.split()[1]) == int(day) - 1 and line.split()[0] == month:
                    ip_address = line.split()[10]
                    user = line.split()[8]
                    last_login_time = "{0} {1} {2}".format(line.split()[0], line.split()[1], line.split()[2])
                    if not ip_address in self.data["accepted"]:
                        self.data["accepted"][ip_address] = {}
                        self.data["accepted"][ip_address]["count"] = 1
                        if not "users" in self.data["accepted"][ip_address]:
                            self.data["accepted"][ip_address]["users"] = {}
                        if not user in self.data["accepted"][ip_address]["users"]:
                            self.data["accepted"][ip_address]["users"][user] = 1
                        else:
                            self.data["accepted"][ip_address]["users"][user] += 1
                        self.data["accepted"][ip_address]["last_login_time"] = last_login_time
                    else:
                        self.data["accepted"][ip_address]["count"] += 1
                        if not "users" in self.data["accepted"][ip_address]:
                            self.data["accepted"][ip_address]["users"] = {}
                            if not user in self.data["accepted"][ip_address]["users"]:
                                self.data["accepted"][ip_address]["users"][user] = 1
                            else:
                                self.data["accepted"][ip_address]["users"][user] += 1

                        self.data["accepted"][ip_address]["last_login_time"] = last_login_time

    def format_data(self):
        """
        Format data into applicable format.
        """
        self.to_log = {}
        self.to_log["header"] = "SSHd Connection stats"
        text = ""
        for ip_address in self.data["accepted"]:
            text += "IP ADDRESS:          {0}\n".format(ip_address)
            text += "Connections count:   {0}\n".format(self.data["accepted"][ip_address]["count"])

            users_line = ""
            for item in self.data["accepted"][ip_address]["users"]:
                users_line += "{0} ({1} connections)".format(item, self.data["accepted"][ip_address]["users"][item])

            text += "Logins:              {0}\n".format(users_line)
            text += "Last login time:     {0}\n".format(self.data["accepted"][ip_address]["last_login_time"])
            text += "<!-- delimiter -->"

        self.to_log["data"] = text

        self.add_to_log(self.to_log)


logs = {
    "arch"      : "auth.log",
    "debian"    : "auth.log"
}