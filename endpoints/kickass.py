#!/usr/bin/env python3

import re
from typing import List
from .site import Torrent, TorrentSite
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
from termcolor import colored

class Kickass(TorrentSite):
    def __init__(self):
        super().__init__(
            "Kickass Torrents",
            [
                "https://kickasstorrents.to",
                "https://kat.cr",
                "https://katcr.co",
                "https://kickass.cm",
                "https://kat.am",
                "https://kickasstorrents.cr"
            ]
        )
    
    def build_search_url(self, query, page=0):
        return f"{self.working_url}/usearch/{quote(query)}/{page + 1}/"
    
    def parse_results(self, content):
        soup = BeautifulSoup(content, "lxml")
        results: List[Torrent] = []

        entry_cleaner = r"[\n\r\t\b]|(\\.)"
        
        try:
            table = soup.find('table', class_="data")
            if not table:
                return results
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) < 5:
                        continue
                    
                    name_cell = cells[0].find('a', class_="cellMainLink")
                    if not name_cell:
                        continue
                    
                    name = re.sub(entry_cleaner, '', name_cell.get_text()).strip()
                    detail_url = urljoin(self.working_url or "", str(name_cell['href']))
                    
                    size = re.sub(entry_cleaner, '', cells[1].get_text()).strip()
                    seeds = re.sub(entry_cleaner, '', cells[4].get_text()).strip()
                    leeches = re.sub(entry_cleaner, '', cells[5].get_text()).strip() if len(cells) > 5 else "0"
                    
                    results.append(Torrent(
                        name=name,
                        category="Unknown",
                        uploader="Unknown",
                        seeds=seeds,
                        leeches=leeches,
                        date="Unknown",
                        size=size,
                        detail_url=detail_url,
                        site=self.name,
                        is_vip=False,
                        is_trusted=False
                    ))
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results
