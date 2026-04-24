import logging
import re
from typing import List
from termcolor import colored
from endpoints.site import Torrent, TorrentSite
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup

class Torrentz2(TorrentSite):
    def __init__(self):
        super().__init__(
            "Torrentz2",
            [
                "https://torrentz2.eu",
                "https://torrentz2.is",
                "https://torrentz2.me",
                "https://torrentz2.cc"
            ]
        )
    
    def build_search_url(self, query, page: int = 0):
        return f"{self.working_url}/search?f={quote(query)}"
    
    def parse_results(self, content):
        soup = BeautifulSoup(content, "lxml")
        results: List[Torrent] = []
        
        try:
            result_divs = soup.find_all('div', class_="results")[0] if soup.find_all('div', class_="results") else None
            if not result_divs:
                return results
            
            for dl in result_divs.find_all('dl'):
                try:
                    dt = dl.find('dt')
                    dd = dl.find('dd')
                    
                    if not dt or not dd:
                        continue
                    
                    link = dt.find('a')
                    if not link:
                        continue
                    
                    name = link.get_text().strip()
                    detail_url = urljoin(str(self.working_url), str(link['href']))
                    
                    # Parse additional info from dd
                    info = dd.get_text().strip()
                    size_match = re.search(r'(\d+\.?\d*\s*[A-Za-z]+)', info)
                    size = size_match.group(1) if size_match else "Unknown"
                    
                    results.append(Torrent(
                        name=name,
                        category="Unknown",
                        uploader="Unknown",
                        seeds="Unknown",
                        leeches="Unknown",
                        date="Unknown",
                        size=size,
                        detail_url=detail_url,
                        site=self.name,
                        is_vip=False,
                        is_trusted=False
                    ))
                
                except Exception as e:
                    logging.debug(f"Error parsing individual result in {self.name}: {e}")
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results
