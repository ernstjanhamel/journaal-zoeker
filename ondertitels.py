#!/usr/bin/env python3
"""Zoek in de ondertitels van het NOS Journaal op NPO Start, met tijdcodes.

Gebruik:
    python3 ondertitels.py "eerste kamer" --van 2026-04-20 --tot 2026-04-22
    python3 ondertitels.py asiel --van 2026-11-01 --tot 2026-11-08 --serie nos-journaal-20-00-uur
    python3 ondertitels.py "raad van state" --van 2026-10-01 --tot 2026-11-08 --md rvs.md

Werkwijze (onofficieel, kan breken als NPO de site verandert):
1. https://npo.nl/start/api/domain/series-seasons?slug=<serie>  -> seizoenen
2. https://npo.nl/start/api/domain/programs-by-season?guid=<seizoen>  -> afleveringen met productId (POW_...)
3. https://cdn.npoplayer.nl/subtitles/nl/<productId>.vtt  -> ondertitels (WebVTT)
Idee voor stap 3: Shing Lyu, "From DevTools Detective to Automation Hero" (juni 2025).

Afspelen: https://npo.nl/start/afspelen/<slug>?start=<seconden>. De speler begint
dan op die seconde (getest 9 nov 2026).
NPO Start bewaart afleveringen ongeveer een jaar of langer; het 20 uur Journaal
staat er (nov 2026) vanaf februari 2024.
"""
import argparse
import datetime as dt
import json
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (journaal-zoeker, HU Journalistiek)"}
API = "https://npo.nl/start/api/domain"


def haal(url, as_json=True):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        body = r.read().decode("utf-8", "replace")
    return json.loads(body) if as_json else body


def afleveringen(serie, van, tot):
    for s in haal(f"{API}/series-seasons?slug={serie}"):
        try:
            progs = haal(f"{API}/programs-by-season?guid={s['guid']}&type=timebound_daily")
        except Exception:
            continue
        for p in progs:
            ts = p.get("firstBroadcastDate")
            if not ts or not p.get("productId"):
                continue
            moment = dt.datetime.fromtimestamp(ts, dt.timezone.utc).astimezone()
            if van <= moment.date() <= tot:
                yield moment, p["productId"], p["slug"]


def cues(vtt):
    """Geeft (start, tekst) per ondertitelblok."""
    vtt = vtt.replace("\r\n", "\n").replace("\r", "\n")
    for blok in re.split(r"\n\s*\n", vtt):
        regels = blok.strip().splitlines()
        tijd = next((r for r in regels if "-->" in r), None)
        if not tijd:
            continue
        tekst = " ".join(re.sub(r"<[^>]+>", "", r) for r in regels[regels.index(tijd) + 1:])
        yield tijd.split(" --> ")[0].split(".")[0], tekst.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("termen", nargs="+", help="zoektermen (allemaal in hetzelfde stukje)")
    ap.add_argument("--van", required=True)
    ap.add_argument("--tot", required=True)
    ap.add_argument("--serie", default="nos-journaal-20-00-uur",
                    help="slug op NPO Start, bv. nos-journaal-20-00-uur of nos-journaal")
    ap.add_argument("--context", type=int, default=2, help="aantal ondertitelblokken voor en na")
    ap.add_argument("--md", help="schrijf de resultaten ook naar dit markdownbestand")
    a = ap.parse_args()
    van, tot = dt.date.fromisoformat(a.van), dt.date.fromisoformat(a.tot)
    termen = [t.lower() for t in a.termen]

    md = []
    for moment, pid, slug in sorted(afleveringen(a.serie, van, tot)):
        try:
            blokken = list(cues(haal(f"https://cdn.npoplayer.nl/subtitles/nl/{pid}.vtt", as_json=False)))
        except Exception:
            print(f"{moment:%Y-%m-%d %H:%M}  geen ondertitels ({pid})", file=sys.stderr)
            continue
        laatst = -99
        for i, (tc, _) in enumerate(blokken):
            venster = " ".join(t for _, t in blokken[max(0, i - a.context): i + a.context + 1]).lower()
            if all(t in venster for t in termen) and all(t in blokken[i][1].lower() for t in termen[:1]) and i - laatst > a.context * 2:
                laatst = i
                tekst = " ".join(t for _, t in blokken[max(0, i - a.context): i + a.context + 1])
                h, m, s = (int(x) for x in tc.split(":"))
                link = f"https://npo.nl/start/afspelen/{slug}?start={h * 3600 + m * 60 + s}"
                print(f"{moment:%Y-%m-%d %H:%M}  {tc}  {link}\n    {tekst}\n")
                md.append(f"| {moment:%Y-%m-%d} | {tc} | {tekst} | [NPO Start]({link}) |")

    if not md:
        print("Niets gevonden.")
    if a.md and md:
        with open(a.md, "w") as f:
            f.write(f"# Ondertitels: {' + '.join(a.termen)} ({a.van} t/m {a.tot}, {a.serie})\n\n")
            f.write("| Datum | Tijdcode | Tekst | Link |\n|---|---|---|---|\n" + "\n".join(md) + "\n")
        print(f"Geschreven naar {a.md}")


if __name__ == "__main__":
    main()
