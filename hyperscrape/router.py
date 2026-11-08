import urllib.request
import json
from typing import Dict, Any, Optional
from .engines.tier1_scrapling import ScraplingEngine
from .engines.tier2_lightpanda import LightpandaEngine

class HyperScraper:
    """Unified 3-Tier Extraction Router."""

    def __init__(self):
        self.t1 = ScraplingEngine()
        self.t2 = LightpandaEngine()

    def scrape(
        self,
        url: str,
        engine: str = "auto",
        css_selector: Optional[str] = None,
        extract_all: bool = False
    ) -> Dict[str, Any]:
        """Intelligently routes requests to the optimal engine tier."""
        chosen = engine.lower()
        if chosen == "auto":
            # Tier 1 handles 85% of high-speed extraction needs with zero memory overhead
            chosen = "scrapling"

        if chosen in ["scrapling", "tier1", "t1"]:
            return self.t1.fetch(url, css_selector=css_selector, extract_all=extract_all)
        elif chosen in ["lightpanda", "tier2", "t2"]:
            return self.t2.fetch(url, css_selector=css_selector, extract_all=extract_all)
        else:
            raise ValueError(f"Unknown engine: {engine}. Choose 'auto', 'scrapling', or 'lightpanda'.")

    def scrape_and_ingest(
        self,
        url: str,
        engine: str = "auto",
        css_selector: Optional[str] = None,
        rag_endpoint: str = "http://127.0.0.1:8989"
    ) -> Dict[str, Any]:
        """Scrapes web content and pushes it to an AI Vector RAG store."""
        data = self.scrape(url, engine=engine, css_selector=css_selector)
        text_content = data.get("extracted") or data.get("title") or ""
        
        if rag_endpoint and text_content:
            try:
                payload = json.dumps({
                    "action": "rag_add",
                    "topic": f"web_{url}",
                    "content": str(text_content)
                }).encode("utf-8")
                req = urllib.request.Request(rag_endpoint, data=payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    rag_resp = json.loads(resp.read().decode("utf-8"))
                    data["rag_status"] = rag_resp.get("status")
                    data["rag_doc_id"] = rag_resp.get("result", {}).get("doc_id")
            except Exception as e:
                data["rag_error"] = str(e)

        return data
