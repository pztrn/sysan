# -*- coding: utf-8 -*-

# LogAn exceptions

class Sysan_Exception(Exception):
    """
    Base Exception class for every excception LogAn can produce.
    """
    pass

class Parser_Load_Failure(Sysan_Exception):
    """
    Raises when SysAn failed to load parser.
    """
    def __init__(self, parser_name):
        print("ERROR: Failed to load parser '{0}'".format(parser_name))

class Parser_Execute_Failure(Sysan_Exception):
    """
    Raises when SysAn failed to execute parser's "execute()" method.
    """
    def __init__(self, parser_name):
        print("ERROR: Failed to execute parser '{0}'".format(parser_name))