"""Tests for endpoints.site module"""

import pytest
from endpoints.site import Torrent, TorrentSite


class TestTorrent:
    """Test Torrent dataclass"""
    
    def test_torrent_creation(self, mock_torrent):
        """Test creating a Torrent object"""
        assert mock_torrent.name == "Test Torrent"
        assert mock_torrent.category == "Test Category"
        assert mock_torrent.uploader == "Test Uploader"
        assert mock_torrent.seeds == "100"
        assert mock_torrent.leeches == "10"
        assert mock_torrent.site == "Test Site"
        assert not mock_torrent.is_vip
        assert not mock_torrent.is_trusted
    
    def test_torrent_formatted_output(self, mock_torrent):
        """Test formatted method returns correct structure"""
        formatted = mock_torrent.formatted(1)
        
        assert len(formatted) == 9
        assert formatted[0] == "Test Site"
        assert formatted[1] == "Test Category"
        assert formatted[3] == "--1--"
        assert formatted[4] == "Test Uploader"
        assert formatted[5] == "1.5 GB"
        assert formatted[6] == "100"
        assert formatted[7] == "10"
    
    def test_torrent_vip_flag(self, mock_vip_torrent):
        """Test VIP torrent flag is set"""
        assert mock_vip_torrent.is_vip is True
        assert mock_vip_torrent.is_trusted is False
    
    def test_torrent_trusted_flag(self, mock_trusted_torrent):
        """Test Trusted torrent flag is set"""
        assert mock_trusted_torrent.is_trusted is True
        assert mock_trusted_torrent.is_vip is False
    
    def test_torrent_default_values(self):
        """Test Torrent with default values"""
        torrent = Torrent(
            name="Test",
            category="Test",
            uploader="Test",
            seeds="0",
            leeches="0",
            date="2026-04-26",
            size="0 B",
            detail_url="https://test.com",
            site="Test"
        )
        
        assert torrent._magnet is None
        assert torrent.is_vip is False
        assert torrent.is_trusted is False


class TestTorrentSite:
    """Test TorrentSite base class"""
    
    def test_torrent_site_is_abstract(self):
        """Test that TorrentSite cannot be instantiated directly"""
        with pytest.raises(TypeError):
            TorrentSite("Test", ["https://test.com"])
    
    def test_torrent_site_subclass_must_implement_methods(self):
        """Test that subclass must implement abstract methods"""
        
        class IncompleteSite(TorrentSite):
            def __init__(self):
                super().__init__("Incomplete", ["https://test.com"])
        
        with pytest.raises(TypeError):
            IncompleteSite()
    
    def test_torrent_site_attributes(self):
        """Test TorrentSite initialization attributes"""
        from endpoints.pirate_bay import PirateBay
        
        site = PirateBay()
        assert site.name == "The Pirate Bay"
        assert isinstance(site.base_urls, list)
        assert len(site.base_urls) > 0
        assert site.working_url is None
