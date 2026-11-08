import time
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from scrapling import Selector

class LightpandaEngine:
    """Tier 2: Headless DOM & V8 JavaScript Execution (Zig + V8 Core, 16x lower memory)."""

    def __init__(self, binary_path: Optional[str] = None):
        self.name = "lightpanda"
        # Search candidate paths
        candidates = [
            binary_path,
            "/home/ubuntu/lightpanda-bin/lightpanda",
            str(Path(__file__).resolve().parent.parent.parent / "bin" / "lightpanda"),
            shutil.which("lightpanda")
        ]
        self.bin = next((c for c in candidates if c and Path(c).is_file()), None)

    def fetch(self, url: str, css_selector: Optional[str] = None, extract_all: bool = False, timeout: int = 15) -> Dict[str, Any]:
        if not self.bin:
            raise FileNotFoundError(
                "Lightpanda binary not found. Download the aarch64 or x86_64 binary into bin/lightpanda or system PATH."
            )

        t0 = time.time()
        proc = subprocess.run(
            [self.bin, "fetch", "--dump", url],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        elapsed_ms = round((time.time() - t0) * 1000, 2)

        if proc.returncode != 0:
            raise RuntimeError(f"Lightpanda execution error (code {proc.returncode}): {proc.stderr}")

        html = proc.stdout
        doc = Selector(html)
        extracted = None
        if css_selector:
            if extract_all:
                extracted = doc.css(css_selector).extract()
            else:
                extracted = doc.css(css_selector).extract_first()

        title = doc.css("title::text").extract_first()

        return {
            "tier": 2,
            "engine": "lightpanda-v8",
            "url": url,
            "status_code": 200,
            "elapsed_ms": elapsed_ms,
            "title": title,
            "extracted": extracted,
            "dom_bytes": len(html)
        }
