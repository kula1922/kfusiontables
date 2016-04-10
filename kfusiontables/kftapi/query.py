import logging


logger = logging.getLogger(__name__)


WHERE_TEMPLATES = {
    "NOT IN": "{0} {1} ({2})",
    "=": "{0} {1} '{2}'",
    "IN": "{0} {1} ({2})",
}


def delete_row_query(table_id, row_id=None):
    """
    Return filled fusiontables query for delete rows.
    """

    logger.debug(
        'Prepare delete row query for table id: %s and row id: %s',
        table_id, row_id
    )

    query = "DELETE FROM {0}".format(table_id)
    if row_id:
        query += " WHERE ROWID = '{0}'".format(row_id)

    return query


def get_row_query(table_id, fields, where=None):
    """
    Return filled fusiontables query for get rows.
    """

    logger.debug(
        'Prepare get rows query for table id: %s, fields: %s,'
        ' and conditions: %s',
        table_id, fields, where
    )

    query = "SELECT {0} FROM {1}".format(','.join(fields), table_id)
    if where:
        # Conver list with data to correct sql query string
        query += " WHERE {0}".format(
            *map(
                lambda x: WHERE_TEMPLATES[x[1]].format(
                    x[0],
                    x[1],
                    ','.join(x[2]) if isinstance(x[2], list) else x[2]
                ),
                where
            )
        )

    return query


def insert_row_query(table_id, columns, values):
    """
    Return filled fusiontables query for insert single row.
    """

    logger.debug(
        'Prepare insert rows query for table id: %s, columns: %s,'
        ' and values: %s',
        table_id, columns, values
    )

    return "INSERT INTO {0} ({1}) VALUES ({2})".format(
        table_id,
        ','.join(map(lambda x: x['name'], columns)),
        ','.join(values)
    )


def update_row_query(table_id, row_id, columns, values):
        """
        Return filled fusiontables query for update single row.
        """

        logger.debug(
            'Prepare update row query for table id: %s, row id: %s,'
            ' columns: %s and values: %s',
            table_id, row_id, columns, values
        )

        return "UPDATE {0} SET {1} WHERE {2}".format(
            table_id,
            ",".join([
                c['name'] + '=' + values[i] for i, c in enumerate(columns)
            ]),  # Build sets '<column_name>=<data>, '
            "ROWID='{0}'".format(row_id)
        )
