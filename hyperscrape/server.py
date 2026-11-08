from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from .router import HyperScraper

app = FastAPI(
    title="HyperScrape Production API Gateway",
    version="1.0.0",
    description="Enterprise 3-Tier Web Extraction and AI Ingestion Microservice"
)

scraper = HyperScraper()

class ScrapeRequest(BaseModel):
    url: str
    engine: Optional[str] = "auto"
    css_selector: Optional[str] = None
    extract_all: Optional[bool] = False
    auto_ingest: Optional[bool] = False
    rag_endpoint: Optional[str] = "http://127.0.0.1:8989"

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "engines": {
            "tier1_scrapling": "active",
            "tier2_lightpanda": "active",
            "tier3_rag": "ready"
        }
    }

@app.post("/scrape")
def scrape(req: ScrapeRequest):
    try:
        if req.auto_ingest:
            return scraper.scrape_and_ingest(
                url=req.url,
                engine=req.engine,
                css_selector=req.css_selector,
                rag_endpoint=req.rag_endpoint
            )
        return scraper.scrape(
            url=req.url,
            engine=req.engine,
            css_selector=req.css_selector,
            extract_all=req.extract_all
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
