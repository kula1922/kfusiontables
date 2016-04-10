import os
import sys


def main(settings_module='kfusiontables.settings', pre_args=None):
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    from django.core.management import execute_from_command_line

    for pre_arg in reversed(pre_args or []):
        sys.argv.insert(1, pre_arg)

    execute_from_command_line(sys.argv)


def test():
    """
    Use kfusiontables for tests.
    """
    main('kfusiontables.tests.settings')


def prod():
    """
    Use kfusiontables as production module.
    """
    main('kfusiontables.settings')


def cmd_kft():
    """
    Use kfusiontables for command interface.
    """
    main('kfusiontables.settings', ['kft'])


def cmd_kft_sync():
    """
    Use kfusiontables for sync command interface.
    """
    main('kfusiontables.settings', ['kft_sync'])


if __name__ == '__main__':
    main('kfusiontables.settings')
