import logging

from kfusiontables.management.commands._base import KFTBaseCommand
from kfusiontables.management.commands._templates import (
    sync_tables_template
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
            choices=["sync_tables", "sync_rows"],
            help="Action for kft sync commandline interface."
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

    def sync_tables(self, **kwargs):
        """
        Sync tables to google fusiontables.
        """
        return "Not Implemented Yet!"

    def sync_rows(self, **kwargs):
        """
        Sync tables to google fusiontables.
        """
        pass

    def handle(self, *args, **options):
        self._standarize_options(options)

        try:
            return getattr(self, options.get("action"))(**options)
        except TypeError:
            return "Check help (-h)."
