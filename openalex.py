# openalex_fetch.py
import asyncio, httpx, orjson, pathlib
import os
from dotenv import load_dotenv


load_dotenv()
EMAIL = os.getenv("EMAIL", "your_email@example.com")

BASE = "https://api.openalex.org/works"
OUT = pathlib.Path("data/raw_openalex-3.jsonl")
OUT.parent.mkdir(exist_ok=True, parents=True)

def params_for(topics, cursor="*"):
    return {
        "search": " ".join(topics),                 # fulltext/title/abstract search
        "filter": "from_publication_date:2015-01-01,has_abstract:true",
        "per-page": 200,                            # <-- hyphenated
        "cursor": cursor,                           # first page: "*"
        "mailto": EMAIL,                            # helps with rate limits
    }

async def fetch_all(topics, limit=None):
    total = 0
    cursor = "*"
    OUT.parent.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient(timeout=60) as client:
        with open(OUT, "wb") as f:
            while True:
                r = await client.get(BASE, params=params_for(topics, cursor))
                if r.status_code == 400:
                    raise RuntimeError(f"400 from OpenAlex: {r.text}")
                r.raise_for_status()
                data = r.json()
                results = data.get("results") or []
                for row in results:
                    f.write(orjson.dumps(row) + b"\n")
                total += len(results)
                nxt = (data.get("meta") or {}).get("next_cursor")
                if not nxt or (limit and total >= limit):
                    break
                cursor = nxt

    print(f"Saved {total} records → {OUT}")

if __name__ == "__main__":
    asyncio.run(fetch_all([
        # "home cage monitoring",
        # "rodent behavior",
        # "computer vision mice",
        # "automated behavioral phenotyping"
        "MRI",
        "Deep Learning"
    ], limit=500))
