from http import HTTPStatus
from uuid import uuid4

from django.test import TestCase
from rest_framework.test import APIClient

from apps.urlinfo.tests.factories import URLInfoGenerator


class URLInfoAPITestCase(TestCase):
    """Test case for URLInfo API endpoints."""

    def setUp(self) -> None:
        """Initialize test client and dummy data."""
        self.client = APIClient()
        self.dummy_data = URLInfoGenerator.generate_dummy_data()

    def test_create_urlinfo_with_valid_url(self) -> None:
        """Test successful URL info creation with a valid URL."""
        url = "https://macktireh.dev"
        response = self.client.post(
            "/api/v1/urlinfo/",
            data={"url": url},
            format="json",
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_create_urlinfo_with_malformed_url(self) -> None:
        """Test URL info creation with an invalid URL format."""
        response = self.client.post(
            path="/api/v1/urlinfo/",
            data={"url": "example"},
            format="json",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_urlinfo_with_unreachable_url(self) -> None:
        """Test URL info creation with a valid URL that is unreachable."""
        response = self.client.post(
            path="/api/v1/urlinfo/",
            data={"url": "https://zzzzzzzz.com"},
            format="json",
        )
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_create_urlinfo_with_unsuccessful_status_code(self) -> None:
        """Test URL info creation with a reachable URL that returns an error status code."""
        response = self.client.post(
            path="/api/v1/urlinfo/",
            data={"url": "https://example.com/test"},
            format="json",
        )
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_create_urlinfo_with_existing_url(self) -> None:
        """Test URL info creation with a URL that already exists in the system."""
        existing_urlinfo = URLInfoGenerator.generate_from_url(url="https://macktireh.dev")
        response = self.client.post(
            path="/api/v1/urlinfo/",
            data={"url": existing_urlinfo.url},
            format="json",
        )
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)

    def test_retrieve_all_urlinfo(self) -> None:
        """Test retrieving all URL info objects."""
        response = self.client.get(path="/api/v1/urlinfo/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), len(self.dummy_data))

    def test_retrieve_urlinfo_by_public_id(self) -> None:
        """Test retrieving URL info by public ID."""
        response = self.client.get(path=f"/api/v1/urlinfo/detail/{self.dummy_data[0].public_id}")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data["publicId"], str(self.dummy_data[0].public_id))

    def test_retrieve_urlinfo_by_public_id_not_found(self) -> None:
        """Test retrieving URL info by a non-existing public ID."""
        response = self.client.get(path=f"/api/v1/urlinfo/detail/{uuid4()}")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_retrieve_urlinfo_by_url(self) -> None:
        """Test retrieving URL info by URL."""
        response = self.client.get(path=f"/api/v1/urlinfo/detail/?url={self.dummy_data[0].url}")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data["url"], self.dummy_data[0].url)

    def test_retrieve_urlinfo_by_url_not_found(self) -> None:
        """Test retrieving URL info by a non-existing URL."""
        response = self.client.get(path="/api/v1/urlinfo/detail/?url=https://example.com/test")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_urlinfo_by_public_id(self) -> None:
        """Test deleting URL info by public ID."""
        response = self.client.delete(path=f"/api/v1/urlinfo/detail/{self.dummy_data[0].public_id}")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_delete_urlinfo_by_url(self) -> None:
        """Test deleting URL info by URL."""
        response = self.client.delete(path=f"/api/v1/urlinfo/detail/?url={self.dummy_data[0].url}")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
