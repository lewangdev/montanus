# coding=utf8

"""all possible exceptions"""

class MontanusException(Exception):
    """There was an ambiguous exception that occurred while
    handling montanus process"""
    pass

class ConfigSyntaxError(MontanusException):
    """JSON Syntax Error occurred in config.json"""
    pass
