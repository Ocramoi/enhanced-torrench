#!/usr/bin/env python3
"""
Enhanced Torrench - Multi-site torrent search tool
Supports multiple popular torrent sites with English search
"""

import logging
import sys
import argparse
import webbrowser
from typing import List, Optional
from tabulate import tabulate
from termcolor import colored
from endpoints.kickass import Kickass
from endpoints.lime import LimeTorrents
from endpoints.pirate_bay import PirateBay
from endpoints.rarbg import RARBG
from endpoints.site import Torrent
from endpoints.torrentz2 import Torrentz2

class TorrentSearcher:
    def __init__(self):
        self.sites = [
            PirateBay(),
            Kickass(),
            Torrentz2(),
            LimeTorrents(),
            RARBG()
        ]
        self.working_sites = []
    
    def test_sites(self):
        """Test which sites are working"""
        print(colored("Testing torrent sites...", "cyan"))
        
        for site in self.sites:
            print(f"Testing {site.name}...", end=" ")
            if site.test_connection():
                self.working_sites.append(site)
                print(colored("✓ Working", "green"))
            else:
                print(colored("✗ Not accessible", "red"))
        
        if not self.working_sites:
            print(colored("No working torrent sites found!", "red"))
            return False
        
        print(colored(f"\nFound {len(self.working_sites)} working sites", "green"))
        return True
    
    def search_all_sites(self, query, page_limit=1) -> List[Torrent]:
        """Search all working sites"""
        all_results: List[Torrent] = []
        
        for site in self.working_sites:
            print(colored(f"\nSearching {site.name}...", "yellow"))
            try:
                for page in range(page_limit):
                    results = site.search(query, page)
                    if results:
                        all_results.extend(results)
                        print(colored(f"Found {len(results)} results from {site.name} (page {page + 1})", "green"))
                    else:
                        break  # No more results
            except Exception as e:
                print(colored(f"Error searching {site.name}: {e}", "red"))
                continue
        
        return all_results
    
    def format_results(self, results: List[Torrent]):
        """Format results for display"""
        formatted_results = []
        
        for i, result in enumerate(results, 1):
            formatted_results.append(result.formated(i))

        return formatted_results

def result_details(result: Torrent):
    print(colored("\nTorrent Details:", "yellow", attrs=["bold"]))
    print(colored("-" * 40, "yellow"))
    print(f"Name: {result.name}")
    print(f"Site: {result.site}")
    print(f"Category: {result.category}")
    print(f"Uploader: {result.uploader}")
    print(f"Size: {result.size}")
    print(f"Seeds: {result.seeds}")
    print(f"Leeches: {result.leeches}")
    print(f"Date: {result.date}")
    print(f"Detail URL: {result.detail_url}")
    print(colored("-" * 40, "yellow"))
    
def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Torrench - Multi-site torrent search tool"
    )
    parser.add_argument(
        "search",
        help="Search query (in English)",
        nargs="?",
        default=None,
        metavar="QUERY"
    )
    parser.add_argument(
        "-p", "--pages",
        type=int,
        help="Number of pages to search per site (default: 1)",
        default=1,
        metavar="N"
    )
    parser.add_argument(
        "-s", "--sites",
        help="Comma-separated list of sites to search (default: all)",
        default="all",
        metavar="SITES"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        help="Maximum number of results to display (default: unlimited)",
        default=None,
        metavar="N"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Enhanced Torrench v2.0"
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode with verbose output",
    )
    
    args = parser.parse_args()
    
    if not args.search:
        print(colored("Please provide a search query in English", "red"))
        print("Example: python enhanced_torrench.py 'Ubuntu 22.04'")
        sys.exit(1)
    
    if args.pages <= 0 or args.pages > 10:
        print(colored("Page limit must be between 1 and 10", "red"))
        sys.exit(1)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        print(colored("Debug mode enabled", "yellow"))
    else:
        logging.basicConfig(level=logging.INFO)
        
    print(colored("Enhanced Torrench - Multi-site Torrent Search", "cyan", attrs=["bold"]))
    print(colored("=" * 50, "cyan"))
    
    searcher = TorrentSearcher()
    
    if not searcher.test_sites():
        print(colored("No working torrent sites available. Please check your internet connection or try using a VPN.", "red"))
        sys.exit(1)
    
    print(colored(f"\nSearching for: '{args.search}'", "yellow", attrs=["bold"]))
    
    results = searcher.search_all_sites(args.search, args.pages)
    
    if not results:
        print(colored("No results found!", "red"))
        sys.exit(0)
    
    # Sort results by seeds (descending)
    results.sort(key=lambda x: int(x.seeds) if x.seeds.isdigit() else 0, reverse=True)
    
    # Apply limit if specified
    if args.limit:
        results = results[:args.limit]
    
    # Display results
    formatted_results = searcher.format_results(results)
    
    print(colored("\n" + "=" * 80, "cyan"))
    print(colored("SEARCH RESULTS", "cyan", attrs=["bold"]))
    print(colored("=" * 80, "cyan"))
    
    headers = ['SITE', 'CATEGORY', 'NAME', 'INDEX', 'UPLOADER', 'SIZE', 'SEEDS', 'LEECHES', 'DATE']
    table = tabulate(formatted_results, headers=headers, tablefmt="grid")
    print(table)
    
    print(colored(f"\nTotal results: {len(results)}", "green", attrs=["bold"]))
    print(colored("Green = VIP | Magenta = Trusted", "yellow"))
    
    # Interactive detail viewing
    print(colored("\nEnter torrent index to view details (0 to exit, 'o' to open last selected torrent's URL):", "cyan"))

    current_index: Optional[int] = None
    while True:
        try:
            choice = input(colored("Index > ", "blue")).strip()
            
            if choice == '0' or choice.lower() == 'exit':
                break
            elif choice.lower() == 'o':
                if current_index is not None:
                    webbrowser.open(results[current_index].detail_url)
                else:
                    print(colored("No torrent selected to open!", "red"))
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(results):
                    current_index = index
                    result_details(results[index])
                else:
                    print(colored("Invalid index! Please try again.", "red"))
            except ValueError:
                print(colored("Please enter a valid number!", "red"))
                
        except KeyboardInterrupt:
            break
    
    print(colored("\nThank you for using Enhanced Torrench!", "green", attrs=["bold"]))

if __name__ == "__main__":
    main()
