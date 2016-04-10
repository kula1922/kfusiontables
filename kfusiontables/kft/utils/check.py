from kfusiontables.kft.exceptions import (
    IncorrectParametersNumberException
)
from kfusiontables.models import TableMap
from kfusiontables.kft.utils.convert import (
    get_model_from_table_name,
    get_model_from_table_id
)


def _fusiontable_table_exist(sender):
    """
    Check from sender if fusiontables table exist.
    """
    try:
        table_map = TableMap.objects.get(
            table_name="{0};{1}".format(
                sender._meta.app_label,
                sender._meta.model_name
            )
        )
        if table_map.ft_id:
            return True
    except TableMap.DoesNotExist:
        pass
    return False


def fusiontable_table_exist(table_name=None, table_id=None, sender=None):
    """
    Check if fusiontables table exist.
    """
    params_count = len(
        list(filter(lambda x: x, [table_name, table_id, sender]))
    )
    if 0 > params_count > 1:
        raise IncorrectParametersNumberException(
            "Fuction 'table_exist' got {0} but can take only 1.".format(
                params_count
            )
        )
    if table_name:
        sender = get_model_from_table_name(table_name)
    if table_id:
        sender = get_model_from_table_id(table_id)
    return _fusiontable_table_exist(sender)


def is_fusiontablesync(model):
    """
    Check if mode is fusiontables syncable.
    """
    return True if getattr(model, '_fusiontablesync', False) else False
