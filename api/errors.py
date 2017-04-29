"""ERRORS"""


class Error(Exception):

    def __init__(self, message):
        self.message = message


class UserNotFound(Error):
    pass


class UserDuplicated(Error):
    pass
