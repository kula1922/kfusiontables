from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class TableMap(models.Model):
    """
    Combines local tables with google fusion tables via
    fusiontable table id and local name created from app_label
    and model name.
    """
    table_name = models.CharField(
        max_length=255,
        default='',
        verbose_name=_("Local table name (<app_label>;<model__name>)")
    )
    ft_id = models.CharField(
        max_length=255,
        default='',
        verbose_name=_("Fusiontable table id")
    )


class KFTQuerySet(models.query.QuerySet):
    """
    KFT Query Set. Contains overwritten update methods.
    Update call post_save signal and pass to them required data.
    Moreover, added '__raw' flag which works like a 'raw' flag from
    base_save method.
    """
    def update(self, **kwargs):
        """
        Convert custom '__raw' flag to 'raw' flag from base_save.
        Call post_save signal on update.
        """
        raw = kwargs.get('__raw', False)
        if raw:
            del kwargs['__raw']
        super(KFTQuerySet, self).update(**kwargs)
        for instance in self._clone():
            post_save.send(
                sender=self.model,
                instance=instance,
                raw=raw
            )


class KFTManager(models.Manager):
    """
    KFT Manager. Required for modify update method from queryset.
    Check out KFTQuerySet class.
    """
    def get_queryset(self):
        return KFTQuerySet(self.model, using=self._db)


class KFTModel(models.Model):
    """
    Abstract base KFTModel. Add some required fields. Auto-synchronize
    tables must inherit from this abstract class.
    """
    class Meta:
        abstract = True

    objects = KFTManager()

    _fusiontablesync = True
    _ft_synced_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Date of the last synchronization")
    )
    _updated_at = models.DateTimeField(
        blank=False,
        null=False,
        auto_now=True,
        verbose_name=_("Date of the last update")
    )
    _ft_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Google fusiontable row id")
    )


# class TestModel1(KFTModel):
#     test_field11 = models.CharField(max_length=255)
#     test_field12 = models.CharField(max_length=255)


# class TestModel2(KFTModel):
#     test_field21 = models.CharField(max_length=255)
#     test_field22 = models.CharField(max_length=255)
