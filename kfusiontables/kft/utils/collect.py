from django.contrib.contenttypes.models import ContentType

from kfusiontables.kft.exceptions import (
    IncorrectParametersNumberException
)
from kfusiontables.kft.utils.check import is_fusiontablesync
from kfusiontables.kft.utils.convert import (
    get_model_from_table_id,
    get_model_from_table_name,
    get_models_from_table_ids,
    get_models_from_table_names,
    get_table_name_from_model,
)
from kfusiontables.models import TableMap


# Django fields type to fusiontables fields type.
MAPPER = {
    "CharField": "STRING",
    "AutoField": "STRING",
    "BigAutoField": "STRING",
    "BigIntegerField": "NUMBER",
    "BinaryField": "STRING",
    "BooleanField": "STRING",
    "CommaSeparatedIntegerField": "STRING",
    "DateField": "DATETIME",
    "DateTimeField": "DATETIME",
    "DecimalField": "NUMBER",
    "DurationField": "NUMBER",
    "EmailField": "STRING",
    "FilePathField": "STRING",
    "FloatField": "NUMBER",
    "GenericIPAddressField": "STRING",
    "IPAddressField": "STRING",
    "IntegerField": "STRING",
    "NullBooleanField": "STRING",
    "PositiveIntegerField": "NUMBER",
    "PositiveSmallIntegerField": "NUMBER",
    "SlugField": "STRING",
    "SmallIntegerField": "NUMBER",
    "TextField": "STRING",
    "TimeField": "DATETIME",
    "URLField": "STRING",
    "UUIDField": "STRING",
}


def get_values(instance, columns):
    """
    Get values from instance for given columns.
    """
    values = [
        "{0}".format(getattr(instance, c) or "") for c in columns
    ]

    return values


def _get_columns(sender):
    """
    Get columns from sender. Excelude kfusiontables private columns.
    """
    fields = set(["name", "type"])

    # return dict with keys are taken from fields but values from obj
    # e.g., return {"name", "id", "type": "IntegerField"}
    def _formatter(obj):
        formatters = {"type": lambda x, y: y.get_internal_type()}
        return {
            field: formatters.get(
                field, lambda x, y: getattr(y, x)
            )(field, obj)
            for field in fields
        }
    # Build nested fieldset where each column is represented
    # by dict with keys "name", "type" etc.
    # Exclude kfusiontables columns and id column.
    columns = filter(
        lambda x: x["name"][0] != "_",
        [_formatter(field) for field in sender._meta.fields]
    )

    return list(map(
        lambda x: {
            key: MAPPER.get(x[key]) or x[key] for key in x.keys()
        },
        columns
    ))


def get_columns(table_name=None, table_id=None, sender=None):
    """
    Get sender from given params and then get columns from sender."
    " Excelude kfusiontables private columns.
    """
    params_count = len(
        list(filter(lambda x: x, [table_name, table_id, sender]))
    )
    if 0 > params_count > 1:
        raise IncorrectParametersNumberException(
            "Fuction 'get_columns' got {0} but can take only 1.".format(
                params_count
            )
        )
    if table_name:
        sender = get_model_from_table_name(table_name)
    if table_id:
        sender = get_model_from_table_id(table_id)
    return _get_columns(sender)


def get_all_models():
    """
    Get all existing models.
    """
    models = []
    for content_type in ContentType.objects.all():
        models.append(content_type.model_class())
    return models


def get_table_maps(table_id=None, table_ids=None, table_name=None,
                   table_names=None, _all=None, sender=None, senders=None):
    """
    Get table maps for given params.
    """
    table_maps = []
    if _all:
        return TableMap.objects.all()
    else:
        if table_name or table_names:
            _table_maps = TableMap.objects.filter(
                table_name__in=(
                    (table_names or []) + ([table_name] if table_name else [])
                )
            )
            table_maps += _table_maps

        if sender or senders:
            _table_maps = TableMap.objects.filter(
                table_name__in=(
                    list(map(
                        lambda x: get_table_name_from_model(x),
                        (senders or []) + ([sender] if sender else [])
                    ))
                )
            )
            table_maps += _table_maps

        if table_id or table_ids:
            _table_maps = TableMap.objects.filter(
                ft_id__in=(
                    (table_ids or []) + ([table_id] if table_id else [])
                )
            )
            table_maps += _table_maps

    return table_maps


def get_senders(table_id=None, table_ids=None, table_name=None,
                table_names=None, _all=None, sender=None, senders=None,
                force=None):
    """
    Get senders maps for given params.
    """
    models = (senders or []) + ([sender] if sender else [])
    errors = []

    if _all:
        models = get_all_models()
    else:
        if table_id or table_ids:
            _models, _errors = (
                get_models_from_table_ids(
                    (table_ids or []) + ([table_id] if table_id else []),
                    force
                )
            )
            models += _models
            errors += _errors

        if table_name or table_names:
            _models, _errors = (
                get_models_from_table_names(
                    (table_names or []) + ([table_name] if table_name else []),
                    force
                )
            )
            models += _models
            errors += _errors

    senders = []
    for model in models:
        if is_fusiontablesync(model):
            senders.append(model)

    return senders, errors


def get_rows(sender, row_id=None, row_ids=None, _all=None, force=None):
    """
    Get rows for given sender and params.
    """
    _row_ids = (row_ids or []) + ([row_id] if row_id else [])
    if _all:
        if force:
            return sender.objects.all()
        return sender.objects.filter(_ft_id='')
    else:
        if force:
            return sender.objects.filter(id__in=_row_ids)
        else:
            return sender.objects.filter(_ft_id='').filter(id__in=_row_ids)


def get_or_create_table_map(model, table_id=None):
    """
    Get table map or create new one. Fill google fusiontables id if passed.
    """
    table_map, status = TableMap.objects.get_or_create(
        table_name=get_table_name_from_model(model)
    )
    if table_id:
        table_map.ft_id = table_id
        table_map.save_base(raw=True)
    return table_map
