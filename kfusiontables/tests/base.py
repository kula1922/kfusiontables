import collections

from django.test import TestCase

from kfusiontables.tests.models import FakeTestModel


@FakeTestModel.fake_me
class KFTTestCase(TestCase):
    def assertListEqual(self, list1, list2, msg=None):
        self.assertEqual(len(list1), len(list2))
        for key, value1 in enumerate(list1):
            value2 = list2[key]

            self.assertEqual(type(value1), type(value2))
            if isinstance(value1, list):
                self.assertListEqual(value1, value2, msg)
            elif (isinstance(value1, collections.Iterable) and
                    not isinstance(value1, str)):
                self.assertDictEqual(value1, value2, msg)
            else:
                self.assertEqual(value1, value2, msg)

        return True

    def assertDictEqual(self, dict1, dict2, msg=None):
        for key, value1 in dict1.items():
            self.assertIn(key, dict2, msg)
            value2 = dict2[key]
            if (isinstance(value1, collections.Iterable) and
               not isinstance(value1, str)):
                self.assertDictEqual(value1, value2, msg)
            else:
                self.assertEqual(value1, value2, msg)
        return True
