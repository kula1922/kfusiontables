"""Exceptions for kft management"""


class CannotCreateInstanceException(Exception):
    """
    Raise this exception when cannot create model class from contentype
    instance.
    """
    pass


class ParamsRequiredException(Exception):
    """
    Raise this exception when some of required params
    are not passed to method.
    """
    pass


class SkipException(Exception):
    """
    Raise this exception when want to skip something.
    """
    pass
