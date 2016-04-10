import logging

from django.conf import settings
from django.db.models.signals import post_save, post_delete, pre_migrate
from django.dispatch import receiver

from kfusiontables import (
    CannotCreateInstanceException,
    SkipException
)
from kfusiontables.kft import KFusionTables
from kfusiontables.kft.utils import is_fusiontablesync


logger = logging.getLogger(__name__)


def _get_kft_instance(*args, **kwargs):
    """
    Return kft api instance or raise excetion.
    """
    if not getattr(settings, 'KFUSIONTABLES_ROW_SYNC_SIGNALS', False):
        raise SkipException(
            'Auto synchronization is off. For turn auto synchronization'
            ' add to settings KFUSIONTABLES_ROW_SYNC_SIGNALS=True or set'
            ' KFUSIONTABLES_SKIP_ROW_SYNC_ON_MIGRATE=False'
        )

    if kwargs.get('raw'):
        raise SkipException('Raw=True')

    if not is_fusiontablesync(kwargs.get('sender')):
        raise SkipException('Sender have no _fusiontablesync')

    return True, KFusionTables()


@receiver(post_delete)
def post_delete_handler(sender, instance, **kwargs):
    """
    Called when row is deleted.
    """
    logger.info(
        'Singal sync on post_delete from django to google fusiontables'
        ' for model: %s and row id: %s',
        sender._meta.db_table,
        instance.id
    )

    try:
        kft = _get_kft_instance(sender=sender, raw=kwargs.get('raw'))[1]
        kft.delete_rows(sender=sender, row_id=instance._ft_id)
    except SkipException as exc:
        logger.debug("Skip synchronization: %s", exc.args)
    # else:
    #     raise CannotCreateInstanceException(
    #         "Internal error: Cannot create kfusiontables instance."
    #     )


@receiver(post_save)
def post_save_handler(sender, instance, **kwargs):
    """
    Called when any of models saved or updated.
    """
    logger.info(
        'Singal sync on post_save from django to google fusiontables'
        ' for model: %s and row id: %s',
        sender._meta.db_table,
        instance.id
    )

    try:
        kft = _get_kft_instance(sender=sender, raw=kwargs.get('raw'))[1]
        if not instance._ft_id:
            kft.insert_rows(sender=sender, row_id=instance.id)
        else:
            kft.update_rows(sender=sender, row_id=instance._ft_id)
    except SkipException as exc:
        logger.debug("Skip synchronization: %s", exc.args)
    # else:
    #     raise CannotCreateInstanceException(
    #         "Internal error: Cannot create kfusiontables instance."
    #     )


@receiver(pre_migrate)
def pre_migrate_handler(sender, *args, **kwargs):
    """
    Called on migrations. Update table schema.
    """
    if (
        getattr(settings, 'KFUSIONTABLES_SKIP_ROW_SYNC_ON_MIGRATE', False) or
        not getattr(settings, 'KFUSIONTABLES_MIGRATE_SYNC_SIGNALS', True)
    ):
        settings.KFUSIONTABLES_ROW_SYNC_SIGNALS = False

    if getattr(settings, 'KFUSIONTABLES_MIGRATE_SYNC_SIGNALS', False):
        # TODO: UPDATE TABLE LOGIC
        pass
