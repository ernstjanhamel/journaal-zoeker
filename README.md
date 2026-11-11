# journaal-zoeker

Twee scripts om journaalfragmenten terug te vinden. Alleen Python 3 nodig, geen sleutels.

## 1. ondertitels.py: zoeken in wat er gezegd is, met tijdcode (aanrader)

```bash
python3 ondertitels.py "eerste kamer" --van 2026-04-21 --tot 2026-04-21
python3 ondertitels.py "raad van state" --van 2026-10-01 --tot 2026-11-08 --md rvs.md
python3 ondertitels.py asiel --van 2026-11-01 --tot 2026-11-08 --serie nos-journaal
```

Zoekt in de ondertitels van het NOS Journaal op NPO Start. Per treffer: datum, tijdcode, de tekst eromheen en de afspeellink op NPO Start.

- Standaard het 20 uur Journaal (`nos-journaal-20-00-uur`). Andere series met `--serie` (de slug uit de NPO Start-URL).
- Bereik op NPO Start (geteld 9 nov 2026): 20 uur Journaal vanaf 2024 compleet (ca. 320 per jaar), `nos-journaal` (alle journaals van de dag) vanaf 2024 ca. 4.500 per jaar, `nieuwsuur` vanaf 2019 compleet. Daarvoor alleen losse afleveringen. Ca. 1 seconde per uitzending.
- De link krijgt `?start=<seconden>` mee. De speler begint dan op die seconde (getest 9 nov 2026).
- Onofficieel: gebruikt de interne API van NPO Start en `cdn.npoplayer.nl/subtitles/nl/<POW-id>.vtt`. Kan breken als NPO de site verandert. Idee van Shing Lyu (blog, juni 2025).
- Live-ondertiteling loopt soms een paar seconden achter op het beeld.

## 2. journaal.py: zoeken in de catalogus van Beeld & Geluid

```bash
python3 journaal.py "eerste kamer" --van 2026-04-21 --tot 2026-04-21 --programma "20 uur"
```

Zoekt in de segmentbeschrijvingen van Beeld & Geluid (open SPARQL-API). Per segment: datum, segmentnaam (bv. "2000 Asielwetten stemming"), het begin van de presentatietekst en een link naar zoeken.beeldengeluid.nl.

- Handig voor alles vóór 2024, en voor andere journaals (6:30 tot 22 uur, gebarentaal, Jeugdjournaal, radio).
- Volledig vanaf ca. 2021: elk journaal, met segmenten en meestal tekst. In 2010 en 2016 zijn er wel segmenten (vooral bij het 20 uur Journaal) maar zonder tekst, dus dan zoek je alleen op segmentnaam.
- Loopt weken achter (9 nov 2026: t/m ca. 20 sept).
- Traag: ca. 50 seconden per zoekvraag. Houd de periode kort.
- Geen tijdcodes, en afspelen kan alleen bij B&G (inloggen).
