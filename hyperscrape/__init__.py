"""
HyperScrape: Ultra High-Throughput 3-Tier Web Extraction & AI RAG Ingestion Engine
"""

__version__ = "1.0.0"
__author__ = "Aamir Zahran (@Amz34)"

from .engines.tier1_scrapling import ScraplingEngine
from .engines.tier2_lightpanda import LightpandaEngine
from .engines.tier3_rag import RagExtractorEngine
from .router import HyperScraper

__all__ = [
    "ScraplingEngine",
    "LightpandaEngine",
    "RagExtractorEngine",
    "HyperScraper"
]
