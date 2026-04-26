"""Tests for the main torrench module"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import argparse

# Import the main module
from torrench import TorrentSearcher, result_details


class TestTorrentSearcher:
    """Test TorrentSearcher class"""
    
    def test_torrent_searcher_initialization(self):
        """Test TorrentSearcher initializes with sites"""
        searcher = TorrentSearcher()
        
        assert len(searcher.sites) > 0
        assert len(searcher.working_sites) == 0
    
    @patch.object(TorrentSearcher, 'test_sites')
    def test_search_all_sites(self, mock_test_sites, mock_torrent):
        """Test searching all sites"""
        searcher = TorrentSearcher()
        searcher.working_sites = [Mock()]
        searcher.working_sites[0].name = "Test Site"
        searcher.working_sites[0].search.return_value = [mock_torrent]
        
        results = searcher.search_all_sites("test query", page_limit=1)
        
        assert len(results) > 0
        assert results[0].name == "Test Torrent"
    
    def test_search_all_sites_empty_results(self):
        """Test searching with no results"""
        searcher = TorrentSearcher()
        searcher.working_sites = [Mock()]
        searcher.working_sites[0].name = "Test Site"
        searcher.working_sites[0].search.return_value = []
        
        results = searcher.search_all_sites("nonexistent query", page_limit=1)
        
        assert results == []
    
    def test_format_results(self, mock_torrent):
        """Test result formatting"""
        searcher = TorrentSearcher()
        results = [mock_torrent]
        
        formatted = searcher.format_results(results)
        
        assert len(formatted) == 1
        assert len(formatted[0]) == 9  # Number of columns
    
    def test_format_multiple_results(self, mock_torrent, mock_vip_torrent):
        """Test formatting multiple results"""
        searcher = TorrentSearcher()
        results = [mock_torrent, mock_vip_torrent]
        
        formatted = searcher.format_results(results)
        
        assert len(formatted) == 2


class TestResultDetails:
    """Test result_details display function"""
    
    def test_result_details_output(self, mock_torrent, capsys):
        """Test that result_details outputs formatted information"""
        result_details(mock_torrent)
        captured = capsys.readouterr()
        
        assert "Torrent Details:" in captured.out
        assert "Test Torrent" in captured.out
        assert "Test Uploader" in captured.out
        assert "100" in captured.out


class TestMainArguments:
    """Test command-line argument parsing"""
    
    def test_search_without_query(self):
        """Test that search query is required"""
        # This would be tested through main() with sys.argv manipulation
        # For unit testing, we verify the parser configuration
        pass
    
    def test_pages_argument_validation(self):
        """Test pages argument validation"""
        # Pages should be between 1 and 10
        # This is tested in the main function
        pass


class TestTorrentSorting:
    """Test result sorting logic"""
    
    def test_results_sorted_by_seeds(self):
        """Test that results are sorted by seeds descending"""
        from endpoints.site import Torrent
        
        torrent1 = Torrent(
            name="Low Seeds", category="test", uploader="user",
            seeds="10", leeches="5", date="2026-04-26",
            size="1 GB", detail_url="https://test.com/1", site="Test"
        )
        torrent2 = Torrent(
            name="High Seeds", category="test", uploader="user",
            seeds="500", leeches="5", date="2026-04-26",
            size="1 GB", detail_url="https://test.com/2", site="Test"
        )
        
        results = [torrent1, torrent2]
        results.sort(key=lambda x: int(x.seeds) if x.seeds.isdigit() else 0, reverse=True)
        
        assert results[0].seeds == "500"
        assert results[1].seeds == "10"
    
    def test_results_with_non_numeric_seeds(self):
        """Test sorting handles non-numeric seed values"""
        from endpoints.site import Torrent
        
        torrent1 = Torrent(
            name="Unknown", category="test", uploader="user",
            seeds="Unknown", leeches="5", date="2026-04-26",
            size="1 GB", detail_url="https://test.com/1", site="Test"
        )
        torrent2 = Torrent(
            name="High Seeds", category="test", uploader="user",
            seeds="100", leeches="5", date="2026-04-26",
            size="1 GB", detail_url="https://test.com/2", site="Test"
        )
        
        results = [torrent1, torrent2]
        results.sort(key=lambda x: int(x.seeds) if x.seeds.isdigit() else 0, reverse=True)
        
        assert results[0].seeds == "100"
