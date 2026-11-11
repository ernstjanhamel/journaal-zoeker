#!/usr/bin/env python3
"""Zet per serie de afleveringenlijst van NPO Start in docs/data/<slug>.json.

De zoekpagina (docs/index.html) kan de NPO Start-API niet zelf aanroepen: die
server staat geen verzoeken van andere websites toe. De ondertitels op
cdn.npoplayer.nl mag de browser wel ophalen. Dit script draait daarom elke
nacht via GitHub Actions (.github/workflows/indexeer.yml).

Uitvoer per aflevering: [unix-tijd uitzending, productId, slug, titel].
Series staan in docs/series.json.
"""
import json
import pathlib
import sys
import time
from datetime import datetime, timezone
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (journaal-zoeker)"}
API = "https://npo.nl/start/api/domain"
DOCS = pathlib.Path(__file__).parent / "docs"


def haal(url):
    for poging in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.loads(r.read())
        except Exception:
            if poging == 2:
                raise
            time.sleep(3)


def afleveringen(serie):
    rijen = {}
    for s in haal(f"{API}/series-seasons?slug={serie}"):
        try:
            progs = haal(f"{API}/programs-by-season?guid={s['guid']}")
        except Exception as e:
            print(f"  seizoen {s.get('label')} overgeslagen: {e}", file=sys.stderr)
            continue
        for p in progs:
            ts = p.get("firstBroadcastDate") or p.get("publishedDateTime")
            if ts and p.get("productId"):
                rijen[p["productId"]] = [ts, p["productId"], p["slug"], p.get("title") or ""]
    return sorted(rijen.values())


def main():
    fouten = 0
    for serie in json.loads((DOCS / "series.json").read_text()):
        slug = serie["slug"]
        try:
            rijen = afleveringen(slug)
        except Exception as e:
            print(f"{slug}: mislukt ({e}), oude lijst blijft staan", file=sys.stderr)
            fouten += 1
            continue
        if not rijen:
            print(f"{slug}: niets gevonden, oude lijst blijft staan", file=sys.stderr)
            fouten += 1
            continue
        (DOCS / "data" / f"{slug}.json").write_text(json.dumps(rijen, ensure_ascii=False, separators=(",", ":")))
        print(f"{slug}: {len(rijen)} afleveringen")
    (DOCS / "data" / "bijgewerkt.json").write_text(json.dumps(datetime.now(timezone.utc).isoformat(timespec="minutes")))
    sys.exit(1 if fouten == len(json.loads((DOCS / "series.json").read_text())) else 0)


if __name__ == "__main__":
    main()
