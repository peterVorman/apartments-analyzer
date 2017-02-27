
class AnalyzerError(Exception):
    pass


class ApartmentAlreadyExists(AnalyzerError):
    pass


class StorageError(Exception):
    message = "StorageError"

    def __repr__(self):
        return self.message


class DuplicatedUniqueField(StorageError):
    def __init__(self, fields):
        self.message = "Object has duplicated value for fields: {}".format(fields)
