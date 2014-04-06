from unittest import TestCase

from synology.utils import jsonprint

class TestUtils(TestCase):
    def endpoint_is_str(self):
        endpoint = 'toto'
        self.assertTrue(isinstance(endpoint, str))
