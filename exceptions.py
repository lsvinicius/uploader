class InvalidFile(Exception):
    pass


class FileTooLarge(InvalidFile):
    pass


class InvalidType(InvalidFile):
    pass


class AlreadyUploaded(InvalidFile):
    pass
