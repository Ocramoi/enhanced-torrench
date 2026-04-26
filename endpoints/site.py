from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional
import requests
import logging
import re

from termcolor import colored

@dataclass
class Torrent:
    name: str
    category: str
    uploader: str
    seeds: str
    leeches: str
    date: str
    size: str
    detail_url: str
    site: str
    _magnet: Optional[str] = None
    is_vip: bool = False
    is_trusted: bool = False

    def formated(self, i: int = -1) -> List[Any]:
        """Return formatted torrent data for appending to table"""
        name = self.name
            
        # Apply color coding for VIP/Trusted
        if self.is_vip:
            name = colored(name, "green")
        elif self.is_trusted:
            name = colored(name, "magenta")

        return [
            self.site,
            self.category,
            name,
            f"--{i}--",
            self.uploader,
            self.size,
            self.seeds,
            self.leeches,
            self.date,
        ]

    @property
    def magnet(self) -> Optional[str]:
        """Return magnet link for this torrent"""

        if self._magnet is None:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(self.detail_url, headers=headers, timeout=5)
            if response.status_code == 200:
                # Try to find magnet link in the page content
                _match = re.search(r'href="(magnet:\?[^"]+)"', response.text)
                if _match:
                    self._magnet = _match.group(1)
                    return self._magnet
            else:
                logging.debug(f"Failed to fetch detail page for magnet link: {self.detail_url} - Status code: {response.status_code}")
        return self._magnet

class TorrentSite(ABC):
    name: str = "Baseline"
    base_urls: List[str] = []
    search_path: str = ""
    result_selector: str = ""
    working_url: Optional[str] = None
    
    """Base class for torrent sites"""
    def __init__(self, name, base_urls, search_path="", result_selector=""):
        self.name = name
        self.base_urls = base_urls if isinstance(base_urls, list) else [base_urls]
        self.search_path = search_path
        self.result_selector = result_selector
        self.working_url = None
    
    def test_connection(self):
        """Test if any of the base URLs are working"""
        for url in self.base_urls:
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    self.working_url = url
                    return True
            except Exception as e:
                logging.debug(f"Connection test failed for {url}: {e}")
                continue
        return False
    
    def search(self, query, page=0):
        """Search for torrents on this site"""
        if not self.working_url:
            return []
        
        try:
            search_url = self.build_search_url(query, page)
            response = requests.get(search_url, timeout=15)
            if response.status_code == 200:
                return self.parse_results(str(response.content))
        except Exception as e:
            print(colored(f"Error searching {self.name}: {e}", "red"))
        
        return []
    
    @abstractmethod
    def build_search_url(self, query: str, page: int = 0) -> str:
        """Build search URL - to be implemented by subclasses"""
        pass

    @abstractmethod
    def parse_results(self, content: str) -> List[Torrent]:
        """Parse search results - to be implemented by subclasses"""
        pass
