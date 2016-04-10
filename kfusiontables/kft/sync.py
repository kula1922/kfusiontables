import logging

from kfusiontables.kft import KFusionTables


logger = logging.getLogger(__name__)


class KFusionTablesSync(KFusionTables):
    def sync_tables(self, table_name=None, table_names=None, sender=None,
                    senders=None, _all=None, force=None):
        """
        Synchronize local tables to google fusiontables.
        """
        pass

    def sync_rows(self, table_id=None, table_ids=None,
                  table_name=None, table_names=None, sender=None,
                  senders=None, row_id=None, row_ids=None,
                  _all=None, force=None):
        """
        Synchronize local rows to google fusiontables.
        """
        pass
