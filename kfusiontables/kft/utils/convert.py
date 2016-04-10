from copy import deepcopy

from django.contrib.contenttypes.models import ContentType

from kfusiontables.kft.exceptions import (
    IncorrectTableNameException,
    ModelDoesNotExistException,
    TableIdDoesNotExistException,
)
from kfusiontables.models import TableMap


def get_models_from_table_names(table_names, force=None):
    """
    Convert list of table names to table model classes.
    """
    models = []
    errors = []
    for table_name in table_names:
        try:
            models.append(
                get_model_from_table_name(table_name)
            )
        except (
            IncorrectTableNameException,
            ModelDoesNotExistException
        ) as exc:
            if not force:
                raise exc
            errors.append(exc.args)
    return models, errors


def get_models_from_table_ids(table_ids, force=None):
    """
    Convert list of table ids to table model classes.
    """
    models = []
    errors = []
    for table_id in table_ids:
        try:
            models.append(
                get_model_from_table_id(table_id)
            )
        except (
            IncorrectTableNameException,
            TableIdDoesNotExistException,
            ModelDoesNotExistException
        ) as exc:
            if not force:
                raise exc
            errors.append(exc.args)
    return models, errors


def get_model_from_table_id(table_id):
    """
    Convert google fusiontables table id to table model class.
    """
    try:
        table_map = TableMap.objects.get(ft_id=table_id)
    except TableMap.DoesNotExist:
        raise TableIdDoesNotExistException(
            "Given table id '{0}' does not exist in local"
            " table map".format(table_id)
        )
    return get_model_from_table_name(table_map.table_name)


def get_model_from_table_name(table_name):
    """
    Convert table name to table model class.
    """
    app_label, model_name = split_table_name(table_name)
    try:
        model = ContentType.objects.get(
            app_label=app_label,
            model=model_name
        ).model_class()
    except ContentType.DoesNotExist:
        raise ModelDoesNotExistException(
            "Model '{0}' does not exist.".format(
                table_name,

            )
        )
    return model


def get_table_name_from_model(model):
    """
    Convert model class to table name.
    """
    return "{0};{1}".format(model._meta.app_label, model._meta.model_name)


def convert_fields(fields, _fields):
    """
    Convert list of django field names to given field names.
    """
    mapper = {
        "id": "local_id",
        "local_id": "id"
    }
    fields = deepcopy(fields)
    for field in fields:
        if field['name'] in _fields:
            field['name'] = mapper[field['name']]
    return fields


def split_table_name(table_name):
    """
    Get app label and model name from table name.
    """
    try:
        return table_name.split(";")
    except ValueError:
        raise IncorrectTableNameException(
            "Given table name '{0}' is incorrect. Table"
            " name should have form: '<app_label>;<model_name>'".format(
                table_name
            )
        )
