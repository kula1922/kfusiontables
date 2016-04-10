from django.db import models
from django_fake_model import models as fake_models

from kfusiontables.models import KFTModel


class FakeTestModel(fake_models.FakeModel, KFTModel):
    fake_test_field = models.CharField(
        max_length=255
    )
