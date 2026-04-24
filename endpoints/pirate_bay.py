import logging
from typing import List
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
import re
from .site import Torrent, TorrentSite
from termcolor import colored

class PirateBay(TorrentSite):
    def __init__(self):
        super().__init__(
            "The Pirate Bay",
            [
                "https://thepiratebay.org",
                "https://tpb.party",
                "https://piratebay.party",
                "https://thepiratebay.zone",
                "https://pirateproxy.live",
                "https://thehiddenbay.com",
                "https://piratebay.live",
                "https://thepiratebay.rocks",
                "https://tpb.pm",
                "https://piratebay.ink"
            ]
        )
    
    def build_search_url(self, query, page=0):
        return f"{self.working_url}/s/?q={quote(query)}&page={page}&orderby=99"
    
    def parse_results(self, content):
        soup = BeautifulSoup(content, "lxml")
        results: List[Torrent] = []
        
        try:
            table = soup.find('table', id="searchResult")
            if not table:
                return results
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    name_cell = row.find('a', class_="detLink")
                    if not name_cell:
                        continue
                    
                    name = name_cell.get_text().strip()
                    detail_url = urljoin(self.working_url or "", str(name_cell['href']))
                    
                    # Get category
                    cat_cell = row.find('td', class_="vertTh")
                    category = "Unknown"
                    if cat_cell:
                        cat_links = cat_cell.find_all('a')
                        if len(cat_links) >= 2:
                            category = f"{cat_links[0].get_text()} > {cat_links[1].get_text()}"
                    
                    # Get uploader
                    uploader_cell = row.find('a', class_="detDesc")
                    uploader = uploader_cell.get_text() if uploader_cell else "Unknown"
                    
                    # Get seeds/leeches
                    seed_cells = row.find_all('td', align="right")
                    seeds = seed_cells[0].get_text() if len(seed_cells) > 0 else "0"
                    leeches = seed_cells[1].get_text() if len(seed_cells) > 1 else "0"
                    
                    # Get date and size
                    desc_cell = row.find('font', class_="detDesc")
                    date, size = "Unknown", "Unknown"
                    if desc_cell:
                        desc_text = desc_cell.get_text()
                        parts = desc_text.split(',')
                        if len(parts) >= 2:
                            date = parts[0].split()[-1] if parts[0] else "Unknown"
                            size_match = re.search(r'Size (\d+\.?\d*\s*[A-Za-z]+)', desc_text)
                            if size_match:
                                size = size_match.group(1)
                    
                    # Check uploader status
                    is_vip = row.find('img', {'title': "VIP"})
                    is_trusted = row.find('img', {'title': 'Trusted'})
                    
                    results.append(Torrent(
                        name=name,
                        category=category,
                        uploader=uploader,
                        seeds=seeds,
                        leeches=leeches,
                        date=date,
                        size=size,
                        detail_url=detail_url,
                        site=self.name,
                        is_vip=is_vip is not None,
                        is_trusted=is_trusted is not None
                    ))
                    
                except Exception as e:
                    logging.debug(f"Error parsing a result row in {self.name}: {e}")
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results
