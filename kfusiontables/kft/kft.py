import logging

from django.db.models import F
from django.utils import timezone

from kfusiontables.kft import KFusionTablesBase
from kfusiontables.kft.utils import (
    convert_fields,
    fusiontable_table_exist,
    get_columns,
    get_or_create_table_map,
    get_rows,
    get_senders,
    get_table_maps,
    get_table_name_from_model,
    get_model_from_table_id,
    get_model_from_table_name,
    get_values
)
from kfusiontables.kft.exceptions import (
    IncorrectSendersNumberException,
    TableDoesNotExistException,
    TableExistException
)
from kfusiontables.models import TableMap


logger = logging.getLogger(__name__)


class KFusionTables(KFusionTablesBase):
    def create_tables(self, table_name=None, table_names=None, sender=None,
                      senders=None, _all=None, force=None):
        """
        Create new google fusiontables tables.
        """
        senders, sender_errors = get_senders(
            table_name=table_name,
            table_names=table_names,
            sender=sender,
            senders=senders,
            _all=_all,
            force=force
        )

        for sender in senders:
            if fusiontable_table_exist(sender=sender):
                msg = "For model {0} fusion table exist.".format(
                    get_table_name_from_model(sender)
                )
                if not force:
                    raise TableExistException(msg)
                sender_errors.append(msg)

        data = []
        for sender in senders:
            table_name = get_table_name_from_model(sender)
            data.append({
                "name": table_name,
                "columns": convert_fields(get_columns(sender=sender), ["id"]),
                "description": "Django {0} table.".format(table_name),
                "isExportable": True
            })

        results = []
        responses, request_errors = self.API.create_tables(data, force=force)
        for response in responses:
            table_map = get_or_create_table_map(
                get_model_from_table_name(response['name']),
                response['tableId']
            )
            results.append([table_map, response])

        return results, sender_errors + request_errors

    def get_tables(self, table_id=None, table_ids=None, table_name=None,
                   table_names=None, sender=None, senders=None, _all=None):
        """
        Get google fusiontables tables.
        """
        senders, sender_errors = get_senders(
            table_id=table_id,
            table_ids=table_ids,
            table_name=table_name,
            table_names=table_names,
            sender=sender,
            senders=senders,
            _all=_all,
            force=True
        )
        ft_tables = self.API.get_tables(
            (table_ids or []) + ([table_id] if table_id else []),
            _all=_all
        )

        senders_connected = []
        senders_not_connected = []
        for sender in senders:
            table_map = get_or_create_table_map(sender)
            connected_ft_table = None
            for ft_table in ft_tables:
                if table_map.ft_id == ft_table['tableId']:
                    connected_ft_table = ft_table
                    ft_tables.remove(ft_table)
                    break
            connected_obj = [sender, connected_ft_table, table_map]
            if connected_ft_table:
                senders_connected.append(connected_obj)
            else:
                senders_not_connected.append(connected_obj)

        return {
            "senders_connected": senders_connected,
            "senders_not_connected": senders_not_connected,
            "ft_tables": ft_tables,
        }

    def update_tables(self, table_name=None, table_names=None, sender=None,
                      senders=None, _all=None, force=False):
        """
        Update google fusiontables tables schema.
        """
        senders, sender_errors = get_senders(
            table_name=table_name,
            table_names=table_names,
            sender=sender,
            senders=senders,
            _all=_all,
            force=True
        )

        # TODO if ft exist (look create)

        data = []
        for sender in senders:
            table_map = get_or_create_table_map(sender)
            if table_map.ft_id:
                data.append({
                    "table_id": table_map.ft_id,
                    "data": {
                        "name": table_map.table_name,
                        "columns": convert_fields(
                            get_columns(sender=sender), ["id"]
                        ),
                        "description": "Django {0} table.".format(table_name),
                        "isExportable": True
                    }
                })

        return self.API.update_tables(data, force=force)

    def drop_tables(self, table_id=None, table_ids=None, table_name=None,
                    table_names=None, sender=None, senders=None, _all=None):
        """
        Delete google fusiontables tables.
        """
        table_maps = get_table_maps(
            table_name=table_name,
            table_names=table_names,
            sender=sender,
            senders=senders,
            _all=_all,
        )
        table_ids_for_delete = list(map(lambda x: x.ft_id, table_maps))

        if _all:
            table_ids_for_delete += list(map(
                lambda x: x['tableId'],
                self.API.get_tables(_all=_all)
            ))
        else:
            table_ids_for_delete += (
                (table_ids or []) + ([table_id] if table_id else [])
            )

        results, errors = self.API.drop_tables(
            table_ids=set(table_ids_for_delete),
            force=True
        )

        TableMap.objects.filter(ft_id__in=table_ids_for_delete).delete()

        return results, errors

    def insert_rows(self, table_name=None, table_names=None, sender=None,
                    senders=None, row_id=None, row_ids=None,
                    _all=None, force=None):
        """
        Insert new rows to google fusiontables.
        """
        senders, sender_errors = get_senders(
            table_name=table_name,
            table_names=table_names,
            sender=sender,
            senders=senders,
            _all=_all,
            force=True
        )

        if row_id or row_ids:
            if 0 > len(senders) > 1:
                raise IncorrectSendersNumberException(
                    "If you set rows for insert you must specify only"
                    " 1 table.".format(
                        len(senders)
                    )
                )

        data = []
        for sender in senders:
            rows = get_rows(
                sender,
                row_id=row_id,
                row_ids=row_ids,
                _all=_all,
                force=force
            )

            table_map = get_or_create_table_map(sender)
            if not table_map.ft_id:
                if not force:
                    raise TableDoesNotExistException(
                        "Fusiontables table for '{0}' does not exist.".format(
                            table_map.table_name
                        )
                    )
                self.API.create_tables([{
                    "name": table_map.table_name,
                    "columns": convert_fields(
                        get_columns(sender=sender),
                        ["id"]
                    ),
                    "description": "Django {0} table.".format(
                        table_map.table_name
                    ),
                    "isExportable": True
                }])

            rows_data = []
            columns = get_columns(sender=sender)
            for row in rows:
                rows_data.append({
                    "table_id": table_map.ft_id,
                    "columns": convert_fields(columns, ["id"]),
                    "values": list(map(
                        lambda x: "'{0}'".format(x),
                        get_values(
                            row,
                            map(
                                lambda x: x['name'],
                                columns
                            )
                        )
                    ))
                })
            if rows_data:
                data.append(rows_data)

        results = self.API.insert_rows(data=data)

        for result in results:
            sender = get_model_from_table_id(result[0][0])
            instance = sender.objects.get(
                id=result[0][1].strip("'")
            )
            instance._ft_id = result[1]['rows'][0][0]
            instance.save_base(raw=True)

        return data, sender_errors

    def update_rows(self, table_name=None, table_names=None, sender=None,
                    senders=None, row_id=None, row_ids=None, _all=None,
                    force=None):
        """
        Update rows in google fusiontables.
        """
        senders, sender_errors = get_senders(
            table_name=table_name,
            table_names=table_names,
            sender=sender,
            senders=senders,
            _all=_all,
            force=True
        )

        results = []
        for sender in senders:
            table_map = get_or_create_table_map(sender)
            if not table_map.ft_id:
                self.API.create_tables([{
                    "name": table_map.table_name,
                    "columns": convert_fields(
                        get_columns(sender=sender),
                        ["id"]
                    ),
                    "description": "Django {0} table.".format(
                        table_map.table_name
                    ),
                    "isExportable": True
                }])

            columns = get_columns(sender=sender)
            rows_data = []

            rows = get_rows(
                sender,
                row_id=row_id,
                row_ids=row_ids,
                _all=_all,
                force=force
            )
            if not rows:
                rows = sender.objects.filter(
                    _ft_synced_at__lt=F('_updated_at')
                ).exclude(
                    _ft_id=''
                )

            for row in rows:
                rows_data.append({
                    "row_id": row._ft_id,
                    "columns": convert_fields(columns, ["id"]),
                    "values": list(map(
                        lambda x: "'{0}'".format(x),
                        get_values(
                            row,
                            map(
                                lambda x: x['name'],
                                columns
                            )
                        )
                    ))
                })
            if rows_data:
                results.append([
                    table_map.ft_id,
                    self.API.update_rows([{
                        "table_id": table_map.ft_id,
                        "rows": rows_data
                    }])[0]
                ])
            sender.objects.all().update(
                __raw=True,
                _ft_synced_at=timezone.now()
            )
        return results

    def get_rows(self, table_id=None, table_ids=None,
                 table_name=None, table_names=None, sender=None,
                 senders=None, _all=None, _local=False):
        """
        Get rows from google fusiontables.
        """
        table_maps = get_table_maps(
            table_name=table_name,
            table_names=table_names,
            sender=sender,
            senders=senders,
            _all=_all,
        )
        _table_ids = list(map(lambda x: x.ft_id, table_maps))

        if _all:
            _table_ids += list(map(
                lambda x: x['tableId'],
                self.API.get_tables(_all=_all)
            ))
        else:
            _table_ids += (
                (table_ids or []) + ([table_id] if table_id else [])
            )

        data = []
        for _table_id in set(_table_ids):
            data.append({
                'table_id': _table_id,
            })

        results = self.API.get_rows(data=data)

        return results

    def delete_rows(self, table_id=None, table_ids=None,
                    table_name=None, table_names=None, sender=None,
                    senders=None, row_id=None, row_ids=None, _all=None,
                    force=False):
        table_maps = get_table_maps(
            table_name=table_name,
            table_names=table_names,
            sender=sender,
            senders=senders,
            _all=_all,
        )
        """
        Delete rows in google fusiontables.
        """
        _table_ids = list(map(lambda x: x.ft_id, table_maps))

        if _all:
            _table_ids += list(map(
                lambda x: x['tableId'],
                self.API.get_tables(_all=_all)
            ))
        else:
            _table_ids += (
                (table_ids or []) + ([table_id] if table_id else [])
            )

        _table_ids = list(set(_table_ids))

        data = []
        for _table_id in _table_ids:
            data.append({
                "table_id": _table_id,
                "rows": (row_ids or []) + ([row_id] if row_id else [])
            })

        results = self.API.delete_rows(data)

        if _all:
            for _table_id in _table_ids:
                sender = get_model_from_table_id(_table_id)
                sender.objects.all().update(__raw=True, _ft_id='')
        else:
            sender = get_model_from_table_id(_table_ids[0])
            sender.objects.all().update(__raw=True, _ft_id='')

        return results
