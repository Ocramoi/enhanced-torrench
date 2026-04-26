"""Pytest configuration and shared fixtures"""

import pytest
from unittest.mock import Mock, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_torrent():
    """Create a mock Torrent object for testing"""
    from endpoints.site import Torrent
    
    return Torrent(
        name="Test Torrent",
        category="Test Category",
        uploader="Test Uploader",
        seeds="100",
        leeches="10",
        date="2026-04-26",
        size="1.5 GB",
        detail_url="https://example.com/torrent/1",
        site="Test Site",
        is_vip=False,
        is_trusted=False
    )


@pytest.fixture
def mock_vip_torrent():
    """Create a mock VIP Torrent object"""
    from endpoints.site import Torrent
    
    return Torrent(
        name="VIP Test Torrent",
        category="Test",
        uploader="VIP Uploader",
        seeds="500",
        leeches="5",
        date="2026-04-26",
        size="2 GB",
        detail_url="https://example.com/torrent/2",
        site="Test Site",
        is_vip=True,
        is_trusted=False
    )


@pytest.fixture
def mock_trusted_torrent():
    """Create a mock Trusted Torrent object"""
    from endpoints.site import Torrent
    
    return Torrent(
        name="Trusted Test Torrent",
        category="Test",
        uploader="Trusted Uploader",
        seeds="250",
        leeches="20",
        date="2026-04-26",
        size="1 GB",
        detail_url="https://example.com/torrent/3",
        site="Test Site",
        is_vip=False,
        is_trusted=True
    )


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get for testing HTTP calls"""
    return mocker.patch('requests.get')


@pytest.fixture
def sample_html_response():
    """Sample HTML response for testing parsers"""
    return """
    <html>
        <body>
            <table id="searchResult">
                <tr><th>Header</th></tr>
                <tr>
                    <td><a class="detLink" href="/torrent/123">Sample Torrent</a></td>
                    <td class="vertTh">
                        <a>Category</a>
                        <a>Sub-Category</a>
                    </td>
                    <td><a class="detDesc">TestUploader</a></td>
                    <td align="right">100</td>
                    <td align="right">10</td>
                    <td><font class="detDesc">2026-04-26, Size 1.5 GB</font></td>
                </tr>
            </table>
        </body>
    </html>
    """
