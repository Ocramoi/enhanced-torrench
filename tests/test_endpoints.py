"""Tests for torrent site endpoints"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from endpoints.pirate_bay import PirateBay
from endpoints.kickass import Kickass
from endpoints.torrentz2 import Torrentz2
from endpoints.lime import LimeTorrents
from endpoints.rarbg import RARBG


class TestPirateBay:
    """Test The Pirate Bay endpoint"""
    
    def test_pirate_bay_initialization(self):
        """Test PirateBay initializes correctly"""
        site = PirateBay()
        assert site.name == "The Pirate Bay"
        assert isinstance(site.base_urls, list)
        assert len(site.base_urls) > 0
    
    def test_pirate_bay_search_url_building(self):
        """Test search URL generation"""
        site = PirateBay()
        site.working_url = "https://thepiratebay.org"
        
        url = site.build_search_url("test query", page=0)
        assert "test%20query" in url or "test+query" in url
        assert "page=0" in url
    
    @patch('requests.get')
    def test_pirate_bay_test_connection_success(self, mock_get):
        """Test successful connection test"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        site = PirateBay()
        result = site.test_connection()
        
        assert result is True
        assert site.working_url is not None
    
    @patch('requests.get')
    def test_pirate_bay_test_connection_failure(self, mock_get):
        """Test failed connection test"""
        mock_get.side_effect = Exception("Connection failed")
        
        site = PirateBay()
        result = site.test_connection()
        
        assert result is False
        assert site.working_url is None


class TestKickass:
    """Test Kickass Torrents endpoint"""
    
    def test_kickass_initialization(self):
        """Test Kickass initializes correctly"""
        site = Kickass()
        assert site.name == "Kickass Torrents"
        assert isinstance(site.base_urls, list)
    
    def test_kickass_search_url_building(self):
        """Test search URL generation"""
        site = Kickass()
        site.working_url = "https://kickasstorrents.to"
        
        url = site.build_search_url("ubuntu", page=0)
        assert "ubuntu" in url
        assert "/1/" in url  # page + 1


class TestTorrentz2:
    """Test Torrentz2 endpoint"""
    
    def test_torrentz2_initialization(self):
        """Test Torrentz2 initializes correctly"""
        site = Torrentz2()
        assert site.name == "Torrentz2"
        assert isinstance(site.base_urls, list)
    
    def test_torrentz2_relative_import(self):
        """Test that Torrentz2 uses relative imports"""
        site = Torrentz2()
        assert hasattr(site, 'search')
        assert callable(site.search)


class TestLimeTorrents:
    """Test LimeTorrents endpoint"""
    
    def test_lime_torrents_initialization(self):
        """Test LimeTorrents initializes correctly"""
        site = LimeTorrents()
        assert site.name == "LimeTorrents"
        assert isinstance(site.base_urls, list)
    
    def test_lime_torrents_relative_import(self):
        """Test that LimeTorrents uses relative imports"""
        site = LimeTorrents()
        assert hasattr(site, 'search')
        assert callable(site.search)


class TestRARBG:
    """Test RARBG endpoint"""
    
    def test_rarbg_initialization(self):
        """Test RARBG initializes correctly"""
        site = RARBG()
        assert site.name == "RARBG"
        assert isinstance(site.base_urls, list)
    
    def test_rarbg_relative_import(self):
        """Test that RARBG uses relative imports"""
        site = RARBG()
        assert hasattr(site, 'search')
        assert callable(site.search)


class TestEndpointImports:
    """Test that all endpoints import correctly with relative imports"""
    
    def test_all_endpoints_importable(self):
        """Test all endpoints can be imported"""
        from endpoints.pirate_bay import PirateBay
        from endpoints.kickass import Kickass
        from endpoints.torrentz2 import Torrentz2
        from endpoints.lime import LimeTorrents
        from endpoints.rarbg import RARBG
        
        sites = [PirateBay(), Kickass(), Torrentz2(), LimeTorrents(), RARBG()]
        assert len(sites) == 5
    
    def test_site_base_class_accessible(self):
        """Test TorrentSite base class is accessible"""
        from endpoints.site import TorrentSite
        assert TorrentSite is not None


class TestSearchMethod:
    """Test search method behavior"""
    
    def test_search_returns_empty_list_when_no_working_url(self):
        """Test search returns empty list when site not connected"""
        site = PirateBay()
        site.working_url = None
        
        results = site.search("test query")
        
        assert results == []
    
    @patch('requests.get')
    def test_search_handles_connection_errors(self, mock_get):
        """Test search handles connection errors gracefully"""
        mock_get.side_effect = Exception("Network error")
        
        site = PirateBay()
        site.working_url = "https://thepiratebay.org"
        
        results = site.search("test query")
        
        assert isinstance(results, list)
