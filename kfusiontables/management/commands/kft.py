import logging

from kfusiontables.management.commands._base import KFTBaseCommand
from kfusiontables.management.commands._templates import (
    create_tables_template,
    delete_rows_template,
    drop_tables_template,
    get_rows_template,
    get_tables_template,
    insert_rows_template,
    update_rows_template,
    update_tables_template
)


logger = logging.getLogger(__name__)


class Command(KFTBaseCommand):
    """
    Contains table commands. (e.g., create table, get rows)
    """

    help = "KFT main command line interface"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            type=str,
            nargs="?",
            choices=[
                "create_tables",
                "get_tables",
                "update_tables",
                "drop_tables",
                "get_rows",
                "insert_rows",
                "delete_rows",
                "update_rows"
            ],
            help="Action for kft commandline interface."
        )
        parser.add_argument(
            "-f", "--force",
            action="store_true",
            default=False,
            dest="force",
            help=("Force run.")
        )
        parser.add_argument(
            "--all",
            action="store_true",
            default=False,
            dest="_all",
            help=("Run for all.")
        )
        parser.add_argument(
            "--table-id",
            action="store",
            default=None,
            dest="table_id",
            help="Set google fusiontables table id."
        )
        parser.add_argument(
            "--table-ids",
            action="store",
            default=None,
            dest="table_ids",
            help="Set google fusiontables table ids. (1,2,3...)"
        )
        parser.add_argument(
            "--row-id",
            action="store",
            default=None,
            dest="table_id",
            help="Set google fusiontables row id."
        )
        parser.add_argument(
            "--row-ids",
            action="store",
            default=None,
            dest="table_ids",
            help="Set google fusiontables row ids. (1,2,3...)"
        )
        parser.add_argument(
            "--table-name",
            action="store",
            default=None,
            dest="table_name",
            help="Set local table name. ('<app_label>;<model_name>')"
        )
        parser.add_argument(
            "--table-names",
            action="store",
            default=None,
            dest="table_names",
            help=("Set local table names. ('<app_label>;<model_name>',"
                  "'<app_label>;<model_name>')")
        )

    def drop_tables(self, **kwargs):
        """
        Drop tables from google fusiontables.
        """
        results, errors = self.kft.drop_tables(
            table_id=kwargs.get('table_id'),
            table_ids=kwargs.get('table_ids'),
            table_name=kwargs.get('table_name'),
            table_names=kwargs.get('table_names'),
            _all=kwargs.get('_all')
        )
        return drop_tables_template(results, errors)

    def insert_rows(self, **kwargs):
        """
        Insert rows to google fusiontables.
        """
        results, errors = self.kft.insert_rows(
            row_id=kwargs.get('row_id'),
            row_ids=kwargs.get('row_ids'),
            table_name=kwargs.get('table_name'),
            table_names=kwargs.get('table_names'),
            _all=kwargs.get('_all'),
            force=kwargs.get('force')
        )
        return insert_rows_template(results, errors)

    def update_rows(self, **kwargs):
        """
        Update rows in google fusiontables.
        """
        results = self.kft.update_rows(
            table_name=kwargs.get('table_name'),
            table_names=kwargs.get('table_names'),
            _all=kwargs.get('_all'),
            force=kwargs.get('force')
        )
        return update_rows_template(results)

    def get_rows(self, **kwargs):
        """
        Get rows from google fusiontables.
        """
        results = self.kft.get_rows(
            table_id=kwargs.get('table_id'),
            table_ids=kwargs.get('table_ids'),
            table_name=kwargs.get('table_name'),
            table_names=kwargs.get('table_names'),
            _all=kwargs.get('_all')
        )
        return get_rows_template(results)

    def delete_rows(self, **kwargs):
        """
        Delete rows in google fusiontables.
        """
        results = self.kft.delete_rows(
            table_id=kwargs.get('table_id'),
            table_ids=kwargs.get('table_ids'),
            table_name=kwargs.get('table_name'),
            table_names=kwargs.get('table_names'),
            _all=kwargs.get('_all'),
            force=kwargs.get('force')
        )
        return delete_rows_template(results)

    def update_tables(self, **kwargs):
        """
        Update tables schema in google fusiontables.
        """
        results = self.kft.update_tables(
            table_name=kwargs.get('table_name'),
            table_names=kwargs.get('table_names'),
            _all=kwargs.get('_all'),
            force=kwargs.get('force')
        )
        return update_tables_template(results)

    def create_tables(self, **kwargs):
        """
        Create new tables in google fusiontables.
        """
        results, errors = self.kft.create_tables(
            table_name=kwargs.get('table_name'),
            table_names=kwargs.get('table_names'),
            _all=kwargs.get('_all'),
            force=kwargs.get('force')
        )
        return create_tables_template(results, errors)

    def get_tables(self, **kwargs):
        """
        Get tables from google fusiontables.
        """
        results = self.kft.get_tables(
            table_id=kwargs.get('table_id'),
            table_ids=kwargs.get('table_ids'),
            table_name=kwargs.get('table_name'),
            table_names=kwargs.get('table_names'),
            _all=kwargs.get('_all')
        )
        return get_tables_template(results)

    def _standarize_options(self, options):
        """
        Join params like table_id and table_ids.
        """
        if options.get('table_names'):
            options['table_names'] = options['table_names'].split(',')
        if options.get('table_ids'):
            options['table_ids'] = options['table_ids'].split(',')

    def handle(self, *args, **options):
        self._standarize_options(options)

        try:
            return getattr(self, options.get("action"))(**options)
        except TypeError:
            return "Check help (-h)."
