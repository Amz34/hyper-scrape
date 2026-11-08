import urllib.request
import json
import os
import sys
import time

os.environ["HOME"] = "/home/ubuntu"
sys.path.append("/home/ubuntu/ops/github/growth")
import publish_post

IMAGE_PATH = "/home/ubuntu/hyper-scrape/assets/hyperscrape-preview.jpg"
tok, _ = publish_post.li_token()
LI_AUTHOR = publish_post.LI_URN

print(f"[*] Registering image upload for {IMAGE_PATH}...")
reg_body = {
    "registerUploadRequest": {
        "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
        "owner": LI_AUTHOR,
        "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
    }
}

req = urllib.request.Request(
    "https://api.linkedin.com/v2/assets?action=registerUpload",
    data=json.dumps(reg_body).encode(),
    headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    },
    method="POST"
)

reg = json.loads(urllib.request.urlopen(req, timeout=30).read())
upload_url = reg["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
asset_urn = reg["value"]["asset"]
print(f"[+] Upload slot allocated: {asset_urn}")

# 2. Upload image binary
print("[*] Uploading image bytes...")
with open(IMAGE_PATH, "rb") as f:
    img_bytes = f.read()

up_req = urllib.request.Request(
    upload_url,
    data=img_bytes,
    headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "image/jpeg"
    },
    method="PUT"
)
with urllib.request.urlopen(up_req, timeout=60) as r:
    print(f"[+] Image binary uploaded successfully (HTTP {r.status})")

# 3. Create Full Rich Article Post with Image Asset attached via UGC API
full_post_text = """Stop burning 2 GB of RAM per tab on headless Chrome just to extract web data for AI agents.

Traditional headless browsers carry a massive rendering tax: Skia graphics, layout calculations, and paint passes that LLMs do not need.

Over the weekend, we benchmarked and open-sourced HyperScrape ⚡: an enterprise 3-tier web extraction engine designed specifically for LLM pipelines and autonomous agents:

🔹 Tier 1: Sub-200ms Adaptive TLS Bypass (Scrapling + curl_cffi)
Mimics modern browser TLS & JA4 fingerprints with zero rendering overhead. Covers 85% of high-volume scraping with ~35 MB memory footprint.

🔹 Tier 2: Headless DOM & V8 Execution (Lightpanda Zig + V8)
Executes pure JavaScript without a graphical rendering engine. In our Oracle Cloud ARM64 benchmarks, memory peaked at ~71 MB (a 16x reduction vs Chrome) and finished in ~660 ms.

🔹 Tier 3: LLM RAG Ingestion (Crawl4AI + Local Vector RAG)
Directly converts messy HTML into clean, BM25-pruned markdown ready for context window ingestion.

To give back to the developer community, we've open-sourced the entire repository, including our n8n automation workflow, zero-config CLI (`scrape <URL>`), and systemd production daemon.

👇 Links, live benchmarks, and architecture in the first comment!

#OpenSource #AIAgents #WebScraping #SoftwareEngineering #Python #Lightpanda #MachineLearning #RAG"""

ugc_body = {
    "author": LI_AUTHOR,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": full_post_text
            },
            "shareMediaCategory": "IMAGE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": "HyperScrape 3-Tier Enterprise Web Extraction & RAG Architecture"
                    },
                    "media": asset_urn,
                    "title": {
                        "text": "HyperScrape: 16x Lower Memory Headless Web Scraping"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

print("[*] Publishing full rich post to LinkedIn UGC...")
ugc_req = urllib.request.Request(
    "https://api.linkedin.com/v2/ugcPosts",
    data=json.dumps(ugc_body).encode(),
    headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    },
    method="POST"
)

with urllib.request.urlopen(ugc_req, timeout=30) as r:
    ugc_res = json.loads(r.read().decode())
    post_urn = ugc_res.get("id")
    print(f"[+] Full Rich Post Live! URN: {post_urn}")
    public_url = f"https://www.linkedin.com/feed/update/{post_urn}/"
    print(f"[+] Public URL: {public_url}")

# 4. Post First Comment
time.sleep(3)
first_comment = """🔗 Community GitHub Repository: https://github.com/Amz34/hyper-scrape

What's inside for the developer community:
⚡ Pre-configured n8n workflow for automated web extraction
⚡ Zero-config CLI (`scrape <URL>`)
⚡ FastAPI microservice daemon with Tailscale mesh readiness
⚡ Native ARM64 & x86_64 pre-compiled execution

Drop a comment below with your scraping bottlenecks—our automated benchmark responder is active to help compare memory/latency metrics for your stack!"""

print("[*] Adding first comment with GitHub repository...")
c_res = publish_post.post_comment_linkedin(post_urn, first_comment)
print(f"[+] Comment result: {c_res}")
