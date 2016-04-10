class IncorrectAccessFilePathException(Exception):
    """
    Raise this exception when given file path is incorrect.
    """
    pass


class UndefinedRequestErrorException(Exception):
    """
    Raise this exception when google send not expected response.
    """
    pass


class TableDoesNotExistException(Exception):
    """
    Raise this exception when google fusiontables table does not exist.
    """
    pass
