# Fragmenten zoeken op NPO Start, met tijdcode

Op YouTube vind je zo een fragment. Op NPO Start niet: je kunt alleen op programmatitel zoeken, niet op wat er gezegd wordt. Dit script lost dat op. Het zoekt in de ondertitels van NPO-programma's en geeft per treffer een link die meteen op de goede seconde begint.

## Wat kun je doorzoeken?

In principe alles op NPO Start met ondertitels. Getest:
- NOS Journaal 20 uur, en alle andere NOS-journaals van de dag: vanaf 2024
- Nieuwsuur: vanaf 2019
- De Avondshow met Arjen Lubach: 2022 tot en met 2024
- Ook Zembla, Buitenhof en Pointer staan erin, sommige al met afleveringen van jaren terug

Het zoekt in wat er gezegd wordt: door de presentator, een minister, een verslaggever of iemand op straat. Niet alleen in de titel.

## Een voorbeeld

Je vraagt aan je AI:

> Gebruik ondertitels.py om in het NOS Journaal van 20 uur van het afgelopen jaar te zoeken naar "spreidingswet". Zet de resultaten in een tabel met datum, tijdcode, tekst en link.

Na ongeveer een minuut krijg je 36 treffers. Twee daarvan:

| Datum | Tijdcode | Wat er gezegd wordt | Link |
|---|---|---|---|
| 27 nov 2025 | 1:51 | "Gemeenten proberen te voldoen aan de spreidingswet, landelijk beleid om de opvang eerlijker te verdelen. Maar groepen tegenstanders..." | npo.nl/start/afspelen/nos-journaal_101923?start=111 |
| 27 nov 2025 | 2:46 | "Het hete hangijzer voor veel gemeenten is de spreidingswet... Een wet die in Den Haag is bedacht, maar lokaal moet worden uitgevoerd." | npo.nl/start/afspelen/nos-journaal_101923?start=166 |

Klik op de link en de uitzending begint op dat moment.

Wil je een ander programma, noem het dan: "zoek in Nieuwsuur" of "zoek in de Avondshow met Arjen Lubach". Het script heeft daarvoor de naam uit het webadres van het programma nodig (bv. `nieuwsuur`). Dat zoekt de AI zelf uit.

Tip: zoek op een woord dat alleen in jouw onderwerp voorkomt. "Spreidingswet" werkt beter dan "asiel", en "Eerste Kamer" levert treffers over van alles op. Twee woorden mag ook: dan moeten ze allebei in hetzelfde stukje voorkomen.

## Welke AI kan dit?

De AI moet de code zelf kunnen uitvoeren én op internet mogen. Dat kan niet elke versie.

- Werkt: AI op je eigen computer die code mag draaien. Bijvoorbeeld de Claude-app (tabblad Code), Claude Code, OpenAI Codex of Gemini CLI. Getest met Claude. Met Codex en Gemini CLI zou het hetzelfde moeten werken, maar dat heb ik niet geprobeerd.
- Werkt meestal niet: de gewone chat in de browser van ChatGPT, Gemini of claude.ai. Die draaien code in een afgeschermde omgeving zonder toegang tot npo.nl.
- Altijd mogelijk: draai het zelf in de Terminal (Mac) of de opdrachtprompt (Windows). Plak het script in ChatGPT of Gemini en vraag: "Leg me stap voor stap uit hoe ik dit op mijn computer draai om te zoeken naar ...". Je hebt alleen Python nodig, verder niks.

Er is geen account, sleutel of betaalde dienst nodig.

## Twee scripts, welke gebruik je?

- **ondertitels.py**: bijna altijd deze. Zoekt in alles wat er gezegd is, geeft tijdcodes en een link die meteen afspeelt. Werkt voor alles wat nu op NPO Start staat.
- **journaal.py**: alleen voor oudere journaals, van vóór 2024. Die staan niet meer op NPO Start. Het zoekt in de catalogus van Beeld en Geluid: korte beschrijvingen per item vanaf ongeveer 2021, daarvoor alleen de titels van de items. Langzamer, zonder tijdcodes, en afspelen kan alleen bij Beeld en Geluid zelf.

## Goed om te weten

- Downloaden kan niet. NPO beveiligt de video's, dus je speelt het fragment af via NPO Start.
- Bij live-uitzendingen lopen de ondertitels soms een paar seconden achter. Begint de link net te laat, schuif dan even terug.
- Het script gebruikt de website van NPO Start zelf, niet een officiële koppeling. Bouwt NPO de site om, dan kan het stoppen met werken.

Vragen: Ernst-Jan Hamel
