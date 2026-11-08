import time
from typing import Dict, Any, Optional
from scrapling import Fetcher, Selector

class ScraplingEngine:
    """Tier 1: Sub-200ms Adaptive TLS Bypass Engine powered by curl_cffi and lxml."""

    def __init__(self):
        self.name = "scrapling"

    def fetch(self, url: str, css_selector: Optional[str] = None, extract_all: bool = False) -> Dict[str, Any]:
        t0 = time.time()
        res = Fetcher.get(url)
        elapsed_ms = round((time.time() - t0) * 1000, 2)
        
        extracted = None
        if css_selector:
            if extract_all:
                extracted = res.css(css_selector).extract()
            else:
                extracted = res.css(css_selector).extract_first()

        title = res.css("title::text").extract_first()

        return {
            "tier": 1,
            "engine": "scrapling-tls",
            "url": url,
            "status_code": res.status,
            "elapsed_ms": elapsed_ms,
            "title": title,
            "extracted": extracted,
            "body_preview": res.body[:500] if hasattr(res, "body") and res.body else None
        }
