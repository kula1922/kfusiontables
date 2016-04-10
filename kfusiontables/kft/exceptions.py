class TableExistException(Exception):
    """
    Raise this exception when want local table exist.
    """
    pass


class TableIdDoesNotExistException(Exception):
    """
    Raise this exception when want google fusiontables table id does not exist.
    """
    pass


class TableDoesNotExistException(Exception):
    """
    Raise this exception when want google fusiontables table does not exist.
    """
    pass


class ModelDoesNotExistException(Exception):
    """
    Raise this exception when want local table does not exist.
    """
    pass


class IncorrectTableNameException(Exception):
    """
    Raise this exception when table name is incorrect.
    """
    pass


class NoFusionTableSyncException(Exception):
    """
    Raise this exception when there is not tables to sync.
    """
    pass


class IncorrectParametersNumberException(Exception):
    """
    Raise this exception when given params number is incorrect.
    """
    pass


class IncorrectSendersNumberException(Exception):
    """
    Raise this exception when given senders number is incorrect.
    """
    pass
