import time
from typing import Dict, Any, Optional

class RagExtractorEngine:
    """Tier 3: Enterprise LLM Markdown & RAG Extraction using Crawl4AI."""

    def __init__(self):
        self.name = "crawl4ai-rag"

    async def extract_markdown(self, url: str) -> Dict[str, Any]:
        t0 = time.time()
        try:
            from crawl4ai import AsyncWebCrawler
            async with AsyncWebCrawler(verbose=False) as crawler:
                res = await crawler.arun(url=url)
                elapsed_ms = round((time.time() - t0) * 1000, 2)
                return {
                    "tier": 3,
                    "engine": "crawl4ai-rag",
                    "url": url,
                    "elapsed_ms": elapsed_ms,
                    "markdown": res.markdown[:1500] if hasattr(res, "markdown") and res.markdown else None,
                    "success": res.success if hasattr(res, "success") else True
                }
        except Exception as e:
            # Resilient fallback to Scrapling Selector if headless chrome is unconfigured in container
            from scrapling import Fetcher
            res = Fetcher.get(url)
            elapsed_ms = round((time.time() - t0) * 1000, 2)
            title = res.css("title::text").extract_first()
            p_text = " ".join(res.css("p::text").extract()[:10])
            return {
                "tier": 3,
                "engine": "rag-fallback-text",
                "url": url,
                "elapsed_ms": elapsed_ms,
                "markdown": f"# {title}\n\n{p_text}",
                "note": f"Fast fallback invoked: {str(e)}"
            }
