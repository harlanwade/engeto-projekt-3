# Elections Scraper

## Popis projektu

**Elections Scraper** je Python skript pro získávání výsledků voleb do Poslanecké sněmovny ČR, které proběhly v roce 2017. Skript umožňuje extrahovat data pro vybraný územní celek (okres) z veřejného webu a ukládat je do CSV souboru. Výstupní soubor obsahuje podrobné informace o hlasování pro jednotlivé obce včetně počtu voličů, vydaných obálek, platných hlasů a hlasů pro jednotlivé strany.

---

## Požadavky

- Python 3.7 a vyšší
- Virtuální prostředí s nainstalovanými potřebnými knihovnami (viz níže)

Použité knihovny:
- `requests`
- `beautifulsoup4`
- `validators`

---

## Instalace

1. **Vytvoření a aktivace virtuálního prostředí**
   ```bash
   python3 -m venv venv_projekt_3
   source venv_projekt_3/bin/activate
   ```

2. **Instalace závislostí**
   Nejprve stáhněte soubor `requirements.txt` a poté nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

---

## Použití

Skript přijímá dva argumenty:
1. URL odkaz na územní celek, který chcete scrapovat, z webu www.volby.cz.
2. Název výstupního souboru ve formátu `.csv`.

Příklad spuštění:
```bash
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=2101" vysledky_benesov.csv
```

### Ukázka výstupního souboru:
| Kód obce | Název obce | Voliči v seznamu | Vydané obálky | Platné hlasy | Strana 1 | Strana 2 | ... |
|------------|-------------|----------------------|----------------|----------------|----------|----------|-----|
| 529303     | Benešov    | 1200                | 1100          | 1050          | 500      | 300      | ... |

---

## Detaily implementace

### Funkce skriptu
- **`check_url(url)`**: Ověří, zda zadaná URL existuje a obsahuje požadovaná data.
- **`validate_arguments(url, file)`**: Ověří správnost argumentů (platná URL a soubor s příponou `.csv`).
- **`get_response(url)`**: Získá HTML obsah z dané URL.
- **`extract_links(response, url)`**: Najde všechny odkazy na detaily obcí.
- **`extract_data(link)`**: Extrahuje tabulková data z konkrétní stránky obce.
- **`create_header(data, file)`**: Vytvoří hlavičku CSV souboru.
- **`get_town_name(link)`**: Získá název obce z HTML stránky.
- **`get_votes_number(link)`**: Extrahuje počty hlasů pro jednotlivé strany.
- **`write_data(link, file)`**: Zapíše data do CSV souboru.
- **`main(url, file)`**: Hlavní funkce skriptu.

---

## Tipy pro ladění

1. Pokud skript hlásí chybu, ověřte:
   - Že URL adresa směřuje na stránku voleb.
   - Že máte aktivované virtuální prostředí.

2. Pokud CSV soubor neobsahuje očekávaná data:
   - Zkontrolujte, zda má stránka obce požadovaný formát (např. správné sloupce).

---

## Autor
- **Jméno**: Kryštof Karel
- **E-mail**: krystof.karel@gmail.com

---

## Licenční ujednání
Tento projekt je vytvořen pro vzdělávací účely v rámci Engeto Online Python Akademie.