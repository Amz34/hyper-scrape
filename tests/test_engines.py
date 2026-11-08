import pytest
from hyperscrape.router import HyperScraper

def test_tier1_engine():
    scraper = HyperScraper()
    res = scraper.scrape("https://example.com", engine="scrapling", css_selector="title::text")
    assert res["status_code"] == 200
    assert "Example Domain" in res["extracted"]

def test_tier2_engine():
    scraper = HyperScraper()
    res = scraper.scrape("https://example.com", engine="lightpanda", css_selector="title::text")
    assert res["status_code"] == 200
    assert res["tier"] == 2
