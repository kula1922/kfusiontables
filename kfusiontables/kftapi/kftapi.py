import logging

from googleapiclient.errors import HttpError as GoogleHttpError

from kfusiontables.kftapi import KFTApiBase
from kfusiontables.kftapi.exceptions import (
    TableDoesNotExistException,
    UndefinedRequestErrorException
)
from kfusiontables.kftapi.query import (
    delete_row_query,
    get_row_query,
    insert_row_query,
    update_row_query
)


logger = logging.getLogger(__name__)


class KFTApi(KFTApiBase):
    def create_tables(self, tables_data, force=None):
        """
        Create google fusiontables tables.
        """
        responses = []
        errors = []
        for table_data in tables_data:
            try:
                pass
                responses.append(self.create_table(table_data))
            except UndefinedRequestErrorException as exc:
                if not force:
                    raise exc
                errors.append(exc)
        return responses, errors

    def create_table(self, table_data):
        """
        Create google fusiontables table.
        """
        logger.info('Executing oauth2client API for create table.')
        try:
            return self.SERVICE.table().insert(body=table_data).execute()
        except GoogleHttpError as exc:
            raise UndefinedRequestErrorException(exc.args)

    def get_tables(self, table_ids=None, _all=None):
        """
        Get google fusiontables tables.
        """
        if not (table_ids or _all):
            return []
        else:
            tables = self.SERVICE.table().list().execute()

            if table_ids:
                filter(lambda x: x['tableId'] in table_ids, tables['items'])

            return tables['items']

    def update_tables(self, data, force=None):
        """
        Update google fusiontables tables.
        """
        results = []
        for table in data:
            results.append(
                self.SERVICE.table().update(
                    tableId=table['table_id'],
                    body=table['data']
                ).execute()
            )
        return results

    def drop_tables(self, table_ids, force=None):
        """
        Delete google fusiontables tables.
        """
        results = []
        errors = []

        for table_id in table_ids:
            try:
                results = {table_id: self.drop_table(table_id)}
            except GoogleHttpError:
                msg = "Table '{0}' does not exist.".format(
                    table_id
                )
                if not force:
                    raise TableDoesNotExistException(msg)
                errors.append(msg)
        return results, errors

    def drop_table(self, table_id=None):
        """
        Delete google fusiontables table.
        """
        logger.debug('Delete table with id:  %s.', table_id)

        return self.SERVICE.table().delete(tableId=table_id).execute()

    def insert_rows(self, data):
        """
        Insert rows to google fusiontables.
        """
        results = []
        for table_data in data:
            for row_data in table_data:
                row_id = None
                for i, column in enumerate(row_data['columns']):
                    if column['name'] == 'local_id':
                        row_id = row_data['values'][i]
                results.append([
                    [row_data['table_id'], row_id],
                    self.insert_row(**row_data)
                ])
        return results

    def insert_row(self, table_id, columns, values):
        """
        Insert row to google fusiontables.
        """
        return self.execute_query(
            insert_row_query(table_id, columns, values)
        )

    def _get_all_table_fields(self):
        """
        Return schema for all tables from google fusiontables.
        """
        table_fields = {}
        for table in self.SERVICE.table().list().execute()['items']:
            table_fields[table['tableId']] = ['ROWID'] + [
                column['name']
                for column in table['columns']
            ]
        return table_fields

    def get_rows(self, data, row_ids=None):
        """
        Get rows from google fusiontables.
        """
        table_fields = self._get_all_table_fields()

        results = []
        for table in data:
            where = table.get('where') or []
            if row_ids:
                where.append(['ROWID', 'IN', row_ids])

            results.append([
                table,
                self.execute_query(
                    get_row_query(
                        table.get('table_id'),
                        fields=table.get(
                            'fields',
                            table_fields.get(table.get('table_id'), ['*'])
                        ),
                        where=where,
                    )
                )
            ])

        return results

    def update_rows(self, data):
        """
        Update rows in google fusiontables.
        """
        results = []
        for table in data:
            rows_results = []
            for row in table['rows']:
                rows_results.append([
                    row['row_id'],
                    self.execute_query(
                        update_row_query(
                            table['table_id'],
                            row['row_id'],
                            row['columns'],
                            row['values']
                        )
                    )
                ])
            results.append(rows_results)
        return results

    def delete_rows(self, data):
        """
        Delete rows from google fusiontables.
        """
        results = []
        for table in data:
            rows = table.get('rows')
            if rows:
                for row in rows:
                    if row:
                        results.append([
                            table.get('table_id'),
                            self.delete_row(table.get('table_id'), row_id=row)
                        ])
            else:
                results.append([
                    table.get('table_id'),
                    self.delete_row(
                        table.get('table_id'),
                        id_not_in=table.get('id_not_in')
                    )
                ])
        return results

    def delete_row(self, table_id, row_id=None, id_not_in=None, _all=False):
        """
        Delete row from google fusiontables.
        """
        if row_id:
            return [
                self.execute_query(
                    delete_row_query(table_id, row_id=row_id)
                )
            ]
        elif id_not_in:
            rows_to_delete = self.execute_query(
                get_row_query(
                    table_id,
                    fields=['rowid'],
                    where=[['rowid', 'NOT IN', id_not_in]],
                )
            )

            deleted_rows = []
            for row in rows_to_delete.get('rows', []):
                deleted_rows.append(
                    self.execute_query(
                        delete_row_query(table_id, row_id=row[0])
                    )
                )
            return deleted_rows
        else:
            return [
                self.execute_query(delete_row_query(table_id))
            ]
