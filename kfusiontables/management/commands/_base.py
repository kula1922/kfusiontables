from django.core.management.base import BaseCommand

from kfusiontables.kft import KFusionTables, KFusionTablesSync


class KFTBaseCommand(BaseCommand):
    """
    Base method for kft management commands.
    """
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """
        Create KFusionTables instance.
        """
        super(KFTBaseCommand, self).__init__(*args, **kwargs)
        self.kft = KFusionTables()
        self.kft_sync = KFusionTablesSync()

    def _standarize_options(self, options):
        """
        Join params like table_id and table_ids.
        """
        if options.get('table_names'):
            options['table_names'] = options['table_names'].split(',')
        if options.get('table_ids'):
            options['table_ids'] = options['table_ids'].split(',')
