# -*- coding: utf-8 -*-

# Logger controller.
import os
import time
import socket

from lib import common

class Logger:
    def __init__(self):
        self.config = common.CONFIG
        # Get logs type.
        self.logs_type = self.config["logger"]["logs_type"]
        # Create empty dict for logs.
        self.log = []
        # Cronjob?
        self.cronjob_mode = common.CRON

    def print_data(self, data):
        """
        Print data in stdout.
        """
        if not self.cronjob_mode:
            print(data)

    def add_to_log(self, namespace, text):
        self.log.append([namespace, text])

    def produce_output(self):
        """
        Produce log output.
        """
        self.print_data("Formatting output...")
        if self.logs_type == "plain":
            data = self.produce_plain()
        else:
            data = self.produce_html()

        if self.config["mailer"]["enabled"] == "no":
            print(data)

        return data

    def produce_plain(self):
        """
        Produce plaintext log.
        """
        string = ""
        header_string = "SysAn report for {0} on {1}.".format(socket.gethostname(), common.DATE)
        #string += "\u250f" + "\u2501" * (len(header_string) + 2) + "\u2513\n"
        #string += "\u2503 " + header_string + " \u2503\n"
        #string += "\u2517" + "\u2501" * (len(header_string) + 2) + "\u251b\n"
        string += "-" * (len(header_string) + 4) + "\n"
        string += "| " + header_string + " |\n"
        string += "-" * (len(header_string) + 4) + "\n"


        for item in self.log:
            string += "\n"
            #string += "\u250f" + "\u2501" * (len(item[1]["header"]) + 2) + "\u2513\n"
            #string += "\u2503 " + item[1]["header"] + " \u2503\n"
            #string += "\u2517" + "\u2501" * (len(item[1]["header"]) + 2) + "\u251b\n"
            string += "-" * (len(item[1]["header"]) + 4) + "\n"
            string += "| " + item[1]["header"] + " |\n"
            string += "-" * (len(item[1]["header"]) + 2) + "\n"
            data = item[1]["data"].replace("<!-- delimiter -->", "\n")
            data = data.replace("<!-- delimiter2 -->", "*" * 40 + "\n")
            data = data.replace("<!-- delimiter3 -->", "=" * 40 + "\n")
            string += data

        return string

    def produce_html(self):
        """
        Produce HTML logs.
        """
        return "HTML isn't here."