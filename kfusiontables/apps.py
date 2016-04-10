from __future__ import unicode_literals

from django.apps import AppConfig


class KfusiontablesConfig(AppConfig):
    name = 'kfusiontables'

    def ready(self):
        """
        Apply signals.
        """
        import kfusiontables.signals  # noqa
