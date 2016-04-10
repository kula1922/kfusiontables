from tabulate import tabulate

from kfusiontables.utils import flatten
LINE_SEPARATOR = '-'


def sync_tables_template(results):
    """
    Return filled template for insert rows.
    """
    return "Table sync complete!"


def sync_rows_template(results):
    """
    Return filled template for insert rows.
    """
    return "Rows sync complete!"


def insert_rows_template(results, errors):
    """
    Return filled template for insert rows.
    """
    errors = flatten(errors)

    results_str = '\n' + LINE_SEPARATOR*71 + '\n'
    for error in errors:
        results_str += '\n[ERROR] ' + error + '\n'
    results_str += '\n' + LINE_SEPARATOR*71 + '\n'
    for result in results:
        results_str += "Table"
        results_str += tabulate(
            [
                [i+1, res['table_id'], res['values']]
                for i, res in enumerate(result)
            ],
            headers=['', 'Fusion Table Id', 'values']
        ) + "\n"
    return results_str + LINE_SEPARATOR*71 + '\n\n'


def drop_tables_template(results, errors):
    """
    Return filled template for drop tables.
    """
    errors = flatten(errors)

    results_str = '\n' + LINE_SEPARATOR*71 + '\n'
    for error in errors:
        results_str += '\n[ERROR] ' + error + '\n'
    results_str += '\n' + LINE_SEPARATOR*71 + '\n'
    results_str += tabulate(
        [
            [i+1, result, 'Deleted']
            for i, result in enumerate(results)
        ],
        headers=['', 'Fusion Table Id', 'Status']
    ) + "\n"
    return results_str + LINE_SEPARATOR*71 + '\n\n'


def get_tables_template(results):
    """
    Return filled template for get tables.
    """
    results_str = '\n' + LINE_SEPARATOR*71 + '\n'
    if results.get('senders_connected'):
        results_str += 'Senders connected\n'
        results_str += tabulate(
            [
                [i+1, result[2].table_name, result[1]['tableId']]
                for i, result in enumerate(
                    results.get('senders_connected')
                )
            ],
            headers=['', 'Local Table Name', 'Fusion Table Id']
        ) + "\n"
        results_str += '\n' + LINE_SEPARATOR*71 + '\n'

    if results.get('senders_not_connected'):
        results_str += 'Senders not connected\n'
        results_str += tabulate(
            [
                [i+1, result[2].table_name, 'x']
                for i, result in enumerate(
                    results.get('senders_not_connected')
                )
            ],
            headers=['', 'Local Table Name', 'Fusion Table Id']
        ) + "\n"
        results_str += '\n' + LINE_SEPARATOR*71 + '\n'

    if results.get('ft_tables'):
        results_str += 'Fusion tables not connected\n'
        results_str += tabulate(
            [
                [i+1, result['tableId'], result['name']]
                for i, result in enumerate(results.get('ft_tables'))
            ],
            headers=['', 'Fusion Table Id', 'Fusion Table Name']
        ) + "\n"
    return results_str + LINE_SEPARATOR*71 + '\n\n'


def create_tables_template(results, errors):
    """
    Return filled template for create tables.
    """
    errors = flatten(errors)

    results_str = '\n' + LINE_SEPARATOR*71 + '\n'
    for error in errors:
        results_str += '\n[ERROR] ' + error + '\n'
    results_str += '\n' + LINE_SEPARATOR*71 + '\n'
    results_str += tabulate(
        [
            [i+1, result[0].table_name, result[0].ft_id, 'Created']
            for i, result in enumerate(results)
        ],
        headers=['', 'Local Table Name', 'Fusion Table Id', 'Status']
    ) + "\n"
    return results_str + LINE_SEPARATOR*71 + '\n\n'


def update_tables_template(results):
    """
    Return filled template for update tables.
    """
    results_str = '\n' + LINE_SEPARATOR*71 + '\n'
    results_str += tabulate(
        [
            [i+1, result['name'], result['tableId'], 'Updated']
            for i, result in enumerate(results)
        ],
        headers=['', 'Local Table Name', 'Fusion Table Id', 'Status']
    ) + "\n"
    return results_str + LINE_SEPARATOR*71 + '\n\n'


def get_rows_template(results):
    """
    Return filled template for get rows.
    """
    results_str = '\n' + LINE_SEPARATOR*71 + '\n'
    for result in results:
        results_str += "Fusiontables Table id: {0}\n".format(
            result[0]['table_id']
        )
        results_str += tabulate(
            result[1].get('rows', []),
            headers=result[1]['columns']
        ) + "\n"
        results_str += LINE_SEPARATOR*71 + '\n\n'
    return results_str


def delete_rows_template(results):
    """
    Return filled template for delete rows.
    """
    results_str = '\n' + LINE_SEPARATOR*71 + '\n'
    results_str += tabulate(
        [[result[0], result[1][0]['rows'][0][0]] for result in results],
        headers=['Fusion Table Id', 'Affected Rows']
    ) + "\n"
    results_str += LINE_SEPARATOR*71 + '\n\n'
    return results_str


def update_rows_template(results):
    """
    Return filled template for update rows.
    """
    results_str = '\n' + LINE_SEPARATOR*71 + '\n'
    for result in results:
        results_str += "Fusiontables Table id: {0}\n".format(
            result[0][0]
        )
        results_str += tabulate(
            [
                [i+1, rows[0], rows[1]['rows'][0][0]]
                for i, rows in enumerate(result[1])
            ],
            headers=['', 'Fusion Table Id', 'Affected Rows']
        ) + "\n"
        results_str += LINE_SEPARATOR*71 + '\n\n'
    results_str += LINE_SEPARATOR*71 + '\n\n'
    return results_str
