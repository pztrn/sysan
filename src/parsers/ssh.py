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
            "accepted": {
                "connections"   : 0,
            },
            "rejected": {
                "connections"   : 0,
            }
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
            # We need only lines that contains "sshd" word.
            if "sshd" in line:
                # Checking that day and month are equal to requested.
                # Usually this is current date minus one day.
                if int(line.split()[1]) == self.day_raw and line.split()[0] == self.month_hr:
                    # Counting accepted connections.
                    if "Accepted" in line:
                        self.process_line("accepted", line)
                    if "Failed" in line:
                        self.process_line("rejected", line)

    def process_line(self, data_type, line):
        """
        Parse line and add parsed data into dict.
        """
        ip_address = line.split()[10]
        user = line.split()[8]
        last_login_time = "{0} {1} {2}".format(line.split()[0], line.split()[1], line.split()[2])
        print(last_login_time)
        # Incrementing total connections count.
        self.data[data_type]["connections"] += 1
        # If IP address not in "accepted" - create new
        # record for it.
        if not ip_address in self.data[data_type]:
            self.data[data_type][ip_address] = {}
            self.data[data_type][ip_address]["count"] = 1
            if not "users" in self.data[data_type][ip_address]:
                self.data[data_type][ip_address]["users"] = {}
            if not user in self.data[data_type][ip_address]["users"]:
                self.data[data_type][ip_address]["users"][user] = {}
                self.data[data_type][ip_address]["users"][user]["attempts"] = 1
            else:
                self.data[data_type][ip_address]["users"][user]["attempts"] += 1
        else:
            # We got IP address. Incrementing...
            self.data[data_type][ip_address]["count"] += 1
            if not "users" in self.data[data_type][ip_address]:
                self.data[data_type][ip_address]["users"] = {}
            if not user in self.data[data_type][ip_address]["users"]:
                self.data[data_type][ip_address]["users"][user] = {}
                self.data[data_type][ip_address]["users"][user]["attempts"] = 1
            else:
                self.data[data_type][ip_address]["users"][user]["attempts"] += 1
            
        self.data[data_type][ip_address]["last_login_time"] = last_login_time


    def format_data(self):
        """
        Format data into applicable format.
        """
        accepted_connections = self.data["accepted"]["connections"]
        rejected_connections = self.data["rejected"]["connections"]
        del(self.data["accepted"]["connections"])
        del(self.data["rejected"]["connections"])
        self.to_log = {}
        self.to_log["header"] = "SSHd Connection stats"
        text = ""
        text += "<!-- delimiter3 -->"
        text += "Accepted connections:          {0}\n".format(accepted_connections)
        text += "<!-- delimiter3 -->"
        for ip_address in self.data["accepted"]:
            text += "IP ADDRESS:                    {0}\n".format(ip_address)
            text += "Connections count:             {0}\n".format(self.data["accepted"][ip_address]["count"])

            users_line = ""
            for item in self.data["accepted"][ip_address]["users"]:
                users_line += "{0} ({1} connections)".format(item, self.data["accepted"][ip_address]["users"][item]["attempts"])
                users_line += " | "
            users_line = users_line[:-3]

            text += "Logins:                        {0}\n".format(users_line)
            text += "Last login time:               {0}\n".format(self.data["accepted"][ip_address]["last_login_time"])
            text += "<!-- delimiter2 -->"

        text += "<!-- delimiter -->"

        text += "<!-- delimiter3 -->"
        text += "Rejected connection attempts:  {0}\n".format(rejected_connections)
        text += "<!-- delimiter3 -->"
        for ip_address in self.data["rejected"]:
            text += "IP ADDRESS:                    {0}\n".format(ip_address)
            text += "Attempts count:                {0}\n".format(self.data["rejected"][ip_address]["count"])

            users_line = ""
            for item in self.data["rejected"][ip_address]["users"]:
                users_line += "{0} ({1} attempts)".format(item, self.data["rejected"][ip_address]["users"][item]["attempts"])
                if self.data["rejected"][ip_address]["users"][item]["attempts"] > int(self.config["ssh"]["max_failures"]):
                    users_line += " (BREAK-IN!)"

                users_line += " | "

            users_line = users_line[:-3]

            text += "Logins:                        {0}\n".format(users_line)
            text += "Last login time:               {0}\n".format(self.data["rejected"][ip_address]["last_login_time"])
            text += "<!-- delimiter2 -->"

        self.to_log["data"] = text

        self.add_to_log(self.to_log)


logs = {
    "arch"      : "auth.log",
    "debian"    : "auth.log"
}