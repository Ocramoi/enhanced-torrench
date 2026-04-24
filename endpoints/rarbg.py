import logging
from typing import List
from termcolor import colored
from endpoints.site import Torrent, TorrentSite
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup

class RARBG(TorrentSite):
    def __init__(self):
        super().__init__(
            "RARBG",
            [
                "https://rarbg.to",
                "https://rarbgprx.org",
                "https://rarbgenter.org",
                "https://rarbg.is",
                "https://rarbggo.org"
            ]
        )
    
    def build_search_url(self, query, page=0):
        return f"{self.working_url}/torrents.php?search={quote(query)}&page={page + 1}"
    
    def parse_results(self, content):
        soup = BeautifulSoup(content, "lxml")
        results: List[Torrent] = []
        
        try:
            table = soup.find('table', class_="lista2t")
            if not table:
                return results
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) < 8:
                        continue
                    
                    name_cell = cells[1].find('a')
                    if not name_cell:
                        continue
                    
                    name = name_cell.get_text().strip()
                    detail_url = urljoin(str(self.working_url), str(name_cell['href']))
                    
                    category = cells[0].get_text().strip()
                    date = cells[2].get_text().strip()
                    size = cells[3].get_text().strip()
                    seeds = cells[4].get_text().strip()
                    leeches = cells[5].get_text().strip()
                    
                    results.append(Torrent(
                        name=name,
                        category=category,
                        uploader="Unknown",
                        seeds=seeds,
                        leeches=leeches,
                        date=date,
                        size=size,
                        detail_url=detail_url,
                        site=self.name,
                        is_vip=False,
                        is_trusted=False
                    ))
                    
                except Exception as e:
                    logging.debug(f"Error parsing a result row in {self.name}: {e}")
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results
