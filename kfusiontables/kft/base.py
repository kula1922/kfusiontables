from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from kfusiontables.kftapi import KFTApi


class KFusionTablesBase:
    ACCESS_FILE_PATH_SETTINGS_FIELD_NAME = "KFUSIONTABLES_ACCESS_FILE_PATH"

    def __init__(self):
        """
        Build KFTApi.
        """
        if not hasattr(settings, self.ACCESS_FILE_PATH_SETTINGS_FIELD_NAME):
            raise ImproperlyConfigured(
                "'{0}' doesn\'t exist. Please add {0} to settings."
                .format(
                    self.ACCESS_FILE_PATH_SETTINGS_FIELD_NAME
                )
            )

        self.API = KFTApi(
            getattr(settings, self.ACCESS_FILE_PATH_SETTINGS_FIELD_NAME)
        )
