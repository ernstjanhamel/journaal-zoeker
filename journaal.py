#!/usr/bin/env python3
"""Zoek journaalsegmenten in de open mediacatalogus van Beeld & Geluid.

Gebruik:
    python3 journaal.py "eerste kamer" --van 2026-04-15 --tot 2026-04-25
    python3 journaal.py asiel stikstof --van 2026-10-01 --tot 2026-11-08 --programma "20 uur"
    python3 journaal.py "eerste kamer" --van 2026-04-01 --tot 2026-04-30 --md resultaten.md

Zoekt in de naam en de beschrijving van segmenten (de eerste regels van de
presentatietekst). Meerdere termen = segment moet ze allemaal bevatten.
Houd de periode kort (dagen tot een paar weken): de server rekent het
zelf door en geeft bij te grote vragen een fout of time-out.

Bron: https://cat.apis.beeldengeluid.nl/sparql (open data, geen sleutel nodig).
De gewone journaals heten "20 uur Journaal", "18 uur Journaal" enz.
De open data loopt weken achter (begin nov 2026: t/m ca. 20 sept). Recentere journaals: zoeken.beeldengeluid.nl.
Tijdcodes staan niet in de open data, wel in de link naar zoeken.beeldengeluid.nl.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

ENDPOINT = "https://cat.apis.beeldengeluid.nl/sparql"


def sparql(query: str, timeout: int = 240) -> list[dict]:
    data = urllib.parse.urlencode({"query": query}).encode()
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Accept": "application/sparql-results+json",
                 "User-Agent": "journaal-zoeker (HU Journalistiek)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        sys.exit("De server gaf geen geldig antwoord. Maak de periode korter en probeer opnieuw.")
    return [{k: v["value"] for k, v in b.items()} for b in d["results"]["bindings"]]


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def bouw_query(termen, van, tot, programma, limiet):
    filters = " ".join(
        f'FILTER(CONTAINS(LCASE(CONCAT(STR(?cn), " ", COALESCE(STR(?ab), ""))), "{esc(t.lower())}"))'
        for t in termen)
    return f"""PREFIX sdo: <https://schema.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?d ?n ?cn ?ab ?u WHERE {{
  ?p sdo:datePublished ?d ; sdo:name ?n .
  FILTER(?d >= "{van}"^^xsd:date && ?d <= "{tot}"^^xsd:date)
  FILTER(CONTAINS(LCASE(STR(?n)), "{esc(programma.lower())}"))
  ?c sdo:isPartOf ?p ; sdo:name ?cn ; sdo:url ?u .
  OPTIONAL {{ ?c sdo:abstract ?ab }}
  {filters}
}} ORDER BY ?d LIMIT {limiet}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("termen", nargs="+", help="zoektermen (allemaal verplicht)")
    ap.add_argument("--van", required=True, help="begindatum JJJJ-MM-DD")
    ap.add_argument("--tot", required=True, help="einddatum JJJJ-MM-DD")
    ap.add_argument("--programma", default="journaal", help='deel van de programmanaam, bv. "20 uur" (standaard "journaal")')
    ap.add_argument("--limiet", type=int, default=50)
    ap.add_argument("--md", help="schrijf de resultaten ook naar dit markdownbestand")
    a = ap.parse_args()

    rijen = sparql(bouw_query(a.termen, a.van, a.tot, a.programma, a.limiet))
    if not rijen:
        print("Niets gevonden. Probeer een andere term, een ruimere periode of --programma \"\".")
        return

    regels = []
    for r in rijen:
        tekst = " ".join(r.get("ab", "").split())
        print(f"{r['d']}  {r['n'].strip()}  ·  {r['cn']}")
        print(f"    {tekst[:240]}")
        print(f"    {r['u']}\n")
        regels.append(f"| {r['d']} | {r['n'].strip()} | {r['cn']} | {tekst[:240]} | [B&G]({r['u']}) |")

    if a.md:
        with open(a.md, "w") as f:
            f.write(f"# Journaalsegmenten: {' + '.join(a.termen)} ({a.van} t/m {a.tot})\n\n")
            f.write("| Datum | Programma | Segment | Begin van de tekst | Link |\n|---|---|---|---|---|\n")
            f.write("\n".join(regels) + "\n")
        print(f"Geschreven naar {a.md}")


if __name__ == "__main__":
    main()
