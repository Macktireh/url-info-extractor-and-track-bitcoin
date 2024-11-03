from http import HTTPStatus
from unittest.mock import patch

from django.urls import reverse
from requests.exceptions import HTTPError
from rest_framework.test import APITestCase

from apps.common.exceptions import InternalServerException
from apps.crypto.services import CryptoBitcoinService
from apps.crypto.types import CryptoBitcoinPriceType


class CryptoBitcoinViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("bitcoin")
        self.crypto_service = CryptoBitcoinService()

    @patch.object(CryptoBitcoinService, "get_bitcoin_data")
    def test_get_bitcoin_data_success(self, mock_get_bitcoin_data):
        # Mock the successful response
        mock_data = CryptoBitcoinPriceType(
            bitcoin_eur=25000.0,
            eur_to_gbp=0.85,
            bitcoin_gbp=21250.0,
        )
        mock_get_bitcoin_data.return_value = mock_data

        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, mock_data)

    @patch.object(CryptoBitcoinService, "get_bitcoin_data")
    def test_get_bitcoin_data_bad_gateway_exception(self, mock_get_bitcoin_data):
        # Mock a BadGatewayException
        mock_get_bitcoin_data.side_effect = HTTPError("Error fetching data from external API")

        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn("Error fetching data from external API", str(response.data))

    @patch.object(CryptoBitcoinService, "get_bitcoin_data")
    def test_get_bitcoin_data_internal_server_exception(self, mock_get_bitcoin_data):
        # Mock an InternalServerException
        mock_get_bitcoin_data.side_effect = InternalServerException("Error parsing external API response")

        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn("Error parsing external API response", str(response.data))

    @patch.object(CryptoBitcoinService, "get_bitcoin_data")
    def test_get_bitcoin_data_unexpected_exception(self, mock_get_bitcoin_data):
        # Mock an unexpected exception
        mock_get_bitcoin_data.side_effect = Exception("Unexpected error")

        response = self.client.get(self.url)
        print()
        print(response.data)
        print()

        # Assertions
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn("Unexpected error", str(response.data))
