from unittest.mock import patch

from django.test import SimpleTestCase

from validate.services import UrlValidateService


class UrlValidateServiceTestCase(SimpleTestCase):
    def setUp(self):
        self.service = UrlValidateService()

    @patch("validate.services.whois.whois")
    @patch("validate.services.extract_fields")
    def test_get_domain_info(self, mock_extract_fields, mock_whois):
        mock_whois.return_value = {"domain_name": "example.com"}
        mock_extract_fields.return_value = {"domain_name": "example.com"}
        info = self.service.get_domain_info("example.com")
        self.assertEqual(info, {"domain_name": "example.com"})