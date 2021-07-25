import re

from django.test import SimpleTestCase
from django.test.client import RequestFactory

from ..utils import get_client_ip


class UtilsTests(SimpleTestCase):
    def setUp(self) -> None:
        factory = RequestFactory()
        self.request = factory.get('/graphql')

    def test_get_client_ip(self) -> None:
        ip = get_client_ip(self.request)
        ip_regex = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

        assert isinstance(ip, str)
        self.assertRegex(ip, ip_regex)
