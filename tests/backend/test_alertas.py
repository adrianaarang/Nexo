"""Comprehensive test suite for the alerts API module.

Covers GDACS RSS data parsing and integration contracts, query parameter
filtering, descending chronological sorting, in-memory caching performance,
and resilience against malformed XML payloads, missing fields, and external 
network failures.
"""

from typing import Any
from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest

from integrations import gdacs_client
from main import app

@pytest.fixture(autouse=True)
def reset_gdacs_cache():
    gdacs_client._cache = {"timestamp": 0.0, "data": []}
    yield


class TestAlertsBase:
    """Base test class holding shared fixtures and mock datasets."""

    client: TestClient = TestClient(app)

    MOCK_GDACS_RSS_XML: str = """<?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0" xmlns:gdacs="http://www.gdacs.org" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
        <channel>
            <item>
                <title>Earthquake - Spain</title>
                <description>Sismo registrado en la región de Granada</description>
                <link>https://www.gdacs.org/report.aspx?eventid=1001</link>
                <pubDate>Wed, 29 Apr 2026 08:30:00 GMT</pubDate>
                <gdacs:eventtype>EQ</gdacs:eventtype>
                <gdacs:alertlevel>Green</gdacs:alertlevel>
                <gdacs:country>Spain</gdacs:country>
                <geo:lat>37.17</geo:lat>
                <geo:long>-3.60</geo:long>
            </item>
            <item>
                <title>Flood - Spain</title>
                <description>Inundación en la cuenca del Ebro</description>
                <link>https://www.gdacs.org/report.aspx?eventid=1002</link>
                <pubDate>Thu, 30 Apr 2026 13:07:47 GMT</pubDate>
                <gdacs:eventtype>FL</gdacs:eventtype>
                <gdacs:alertlevel>Red</gdacs:alertlevel>
                <gdacs:country>Espania</gdacs:country>
                <geo:lat>41.65</geo:lat>
                <geo:long>-0.88</geo:long>
            </item>
            <item>
                <title>Tropical Cyclone - Philippines</title>
                <description>Ciclón en Filipinas</description>
                <link>https://www.gdacs.org/report.aspx?eventid=1003</link>
                <pubDate>Tue, 28 Apr 2026 10:00:00 GMT</pubDate>
                <gdacs:eventtype>TC</gdacs:eventtype>
                <gdacs:alertlevel>Orange</gdacs:alertlevel>
                <gdacs:country>Philippines</gdacs:country>
                <geo:lat>12.87</geo:lat>
                <geo:long>121.77</geo:long>
            </item>
        </channel>
    </rss>
    """

    MOCK_XML_MISSING_FIELDS: str = """<?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0" xmlns:gdacs="http://www.gdacs.org">
        <channel>
            <item>
                <title>Alert with missing fields</title>
                <description>Alerta sin fecha ni pais</description>
                <link>https://www.gdacs.org/report.aspx?eventid=9999</link>
                <gdacs:eventtype>EQ</gdacs:eventtype>
                <gdacs:alertlevel>Green</gdacs:alertlevel>
            </item>
        </channel>
    </rss>
    """


class TestAlertsContractAndSorting(TestAlertsBase):
    """Test cases focused on contract status, schema compliance, and ordering."""

    @patch("integrations.gdacs_client.requests.get")
    def test_read_alerts_success_status_and_schema(
        self, mock_get: Any
    ) -> None:
        """Verifies 200 OK status code and response schema integrity."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_GDACS_RSS_XML.encode("utf-8")

        response = self.client.get("/api/alertas")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

        expected_keys = {
            "id",
            "fuente",
            "tipo",
            "titulo",
            "descripcion",
            "severidad",
            "pais",
            "lat",
            "lon",
            "fecha",
            "enlace",
        }
        for item in data:
            assert expected_keys.issubset(item.keys())

    @patch("integrations.gdacs_client.requests.get")
    def test_read_alerts_chronological_sorting(self, mock_get: Any) -> None:
        """Ensures alerts are sorted in descending chronological order."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_GDACS_RSS_XML.encode("utf-8")

        response = self.client.get("/api/alertas")
        assert response.status_code == 200

        data = response.json()
        assert data[0]["tipo"] == "inundacion"
        assert data[1]["tipo"] == "terremoto"
        assert data[2]["tipo"] == "ciclon"


class TestAlertsFiltering(TestAlertsBase):
    """Test cases focused on query parameter filtering mechanisms."""

    @patch("integrations.gdacs_client.requests.get")
    def test_filter_by_alert_level(self, mock_get: Any) -> None:
        """Tests filtering results by severidad attribute."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_GDACS_RSS_XML.encode("utf-8")

        response = self.client.get("/api/alertas?severidad=red")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["severidad"] == "red"
        assert data[0]["tipo"] == "inundacion"

    @patch("integrations.gdacs_client.requests.get")
    def test_filter_by_event_type(self, mock_get: Any) -> None:
        """Tests filtering results by tipo attribute."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_GDACS_RSS_XML.encode("utf-8")

        response = self.client.get("/api/alertas?tipo=terremoto")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["tipo"] == "terremoto"

    @patch("integrations.gdacs_client.requests.get")
    def test_filter_case_insensitivity_and_partial_country(
        self, mock_get: Any
    ) -> None:
        """Ensures query filtering is case-insensitive and supports country substrings."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_GDACS_RSS_XML.encode("utf-8")

        response = self.client.get("/api/alertas?pais=ESPA&severidad=red")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["severidad"] == "red"
        assert "espania" in data[0]["pais"].lower()

    @patch("integrations.gdacs_client.requests.get")
    def test_filter_no_matches_returns_empty_list(self, mock_get: Any) -> None:
        """Verifies that queries with no matching entities return an empty JSON list."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_GDACS_RSS_XML.encode("utf-8")

        response = self.client.get("/api/alertas?tipo=volcan")
        assert response.status_code == 200
        assert response.json() == []

    def test_invalid_enum_filter_returns_422_validation_error(self) -> None:
        """Validates OpenAPI contract validation when passing illegal Enum query options."""
        response = self.client.get("/api/alertas?tipo=invalid_type")
        assert response.status_code == 422


class TestAlertsCachingAndPerformance(TestAlertsBase):
    """Test cases verifying caching performance requirements."""

    @patch("integrations.gdacs_client.requests.get")
    def test_caching_mechanism_prevents_duplicate_http_calls(
        self, mock_get: Any
    ) -> None:
        """Validates that a second request retrieves data from in-memory cache."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_GDACS_RSS_XML.encode("utf-8")

        res1 = self.client.get("/api/alertas")
        assert res1.status_code == 200

        res2 = self.client.get("/api/alertas")
        assert res2.status_code == 200

        assert mock_get.call_count <= 1


class TestAlertsResilienceAndEdgeCases(TestAlertsBase):
    """Test cases covering resilience against errors, network issues, and bad input."""

    @patch("integrations.gdacs_client.requests.get")
    def test_resilience_on_external_network_exception(
        self, mock_get: Any
    ) -> None:
        """Ensures service handles network timeouts gracefully."""
        mock_get.side_effect = Exception("Connection Timeout Error")

        response = self.client.get("/api/alertas")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @patch("integrations.gdacs_client.requests.get")
    def test_resilience_on_500_server_error_from_gdacs(
        self, mock_get: Any
    ) -> None:
        """Ensures service handles HTTP error status codes from GDACS gracefully."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.content = b"Internal Server Error"

        response = self.client.get("/api/alertas")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @patch("integrations.gdacs_client.requests.get")
    def test_resilience_on_malformed_xml_payload(self, mock_get: Any) -> None:
        """Verifies that unparseable RSS XML responses do not crash the endpoint."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"<rss><channel><unclosed_tag></channel>"

        response = self.client.get("/api/alertas")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @patch("integrations.gdacs_client.requests.get")
    def test_read_alerts_handles_missing_fields_gracefully(
        self, mock_get: Any
    ) -> None:
        """Verifies missing non-essential XML tags do not cause internal server errors."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_XML_MISSING_FIELDS.encode(
            "utf-8"
        )

        response = self.client.get("/api/alertas")
        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 0

    @patch("integrations.gdacs_client.requests.get")
    def test_read_alerts_handles_invalid_date_format(
        self, mock_get: Any
    ) -> None:
        """Ensures unparseable date strings default safely without crashing."""
        bad_date_xml = self.MOCK_GDACS_RSS_XML.replace(
            "Thu, 30 Apr 2026 13:07:47 GMT", "Invalid-Date-String"
        )
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = bad_date_xml.encode("utf-8")

        response = self.client.get("/api/alertas")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3

    @patch("integrations.gdacs_client.requests.get")
    def test_read_alerts_empty_query_string_parameters(
        self, mock_get: Any
    ) -> None:
        """Verifies empty query parameters are ignored without failing."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.MOCK_GDACS_RSS_XML.encode("utf-8")

        response = self.client.get("/api/alertas?pais=&tipo=&severidad=")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3