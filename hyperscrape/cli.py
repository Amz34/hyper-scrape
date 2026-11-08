import sys
import json
import argparse
from .router import HyperScraper

def main():
    parser = argparse.ArgumentParser(
        description="HyperScrape: Ultra High-Throughput 3-Tier Web Extraction CLI"
    )
    parser.add_argument("url", help="Target URL to scrape")
    parser.add_argument(
        "--engine",
        choices=["auto", "scrapling", "lightpanda"],
        default="auto",
        help="Extraction tier engine"
    )
    parser.add_argument("--css", default="title::text", help="CSS Selector for extraction")
    parser.add_argument("--all", action="store_true", help="Extract all matching selector elements")
    parser.add_argument("--rag", action="store_true", help="Automatically ingest into local Vector RAG")

    args = parser.parse_args()

    scraper = HyperScraper()
    if args.rag:
        res = scraper.scrape_and_ingest(args.url, engine=args.engine, css_selector=args.css)
    else:
        res = scraper.scrape(args.url, engine=args.engine, css_selector=args.css, extract_all=args.all)

    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
