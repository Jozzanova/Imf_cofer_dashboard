"""Download the IMF's COFER data and build the dashboard.

Usage:
    python update.py            # download the latest data, then build
    python update.py --offline  # build from the copy in data/raw
    python update.py --open     # also open the dashboard in your browser

It also downloads the end-of-quarter exchange rates of the listed currencies (IMF, Exchange Rates
dataset), which the Explore tab uses to separate currency moves from central banks' own choices,
and, for the Countries tab, each country's reserves and gold (International Investment Position)
and GDP (World Economic Outlook).

The dashboard is a single file, output/dashboard.html, with this download embedded. When it is
opened it also asks the IMF for newer data itself, so a quarter published since the last build
appears without running this script again.
"""

import json
import math
import sys
import urllib.request
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "cofer.csv"
RAW_ER = ROOT / "data" / "raw" / "exchange_rates.csv"
STATUS = ROOT / "data" / "raw" / "status.json"
TEMPLATE = ROOT / "templates" / "dashboard.html"
OUTPUT = ROOT / "output" / "dashboard.html"

# World totals (G001), every indicator, currency, unit and frequency, as SDMX-CSV.
# The page itself uses the same address for its live check (DATA_URL in the template).
DATA_URL = "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/COFER/+/G001.*.*.*.*"
# End-of-quarter exchange rates (domestic currency per US dollar) of the currencies COFER lists,
# from the IMF's Exchange Rates dataset; used by the Explore tab (ER_URL in the template).
ER_URL = "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/ER/+/G163+JPN+GBR+CHN+CAN+AUS+CHE.XDC_USD.EOP_RT.Q"
# For the Countries tab: each country's reserve assets and its monetary gold (IMF, International
# Investment Position), quarterly and yearly, and GDP in US dollars (IMF, World Economic Outlook).
# The page uses the same addresses (COUNTRY_URLS in the template).
IIP_URL = "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/IIP/+/*.A_P.R+R_F11_MV.USD.{f}"
COUNTRY_URLS = {
    "iipQ": IIP_URL.format(f="Q"),
    "iipA": IIP_URL.format(f="A"),
    "weo": "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/WEO/+/*.NGDPD.A",
    # monthly end-of-month exchange rates (domestic currency per US dollar) of every country for the last
    # three years, to measure how each currency behaves (pegged, managed or floating)
    "erM": "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/ER/+/*.XDC_USD.EOP_RT.M?c%5BTIME_PERIOD%5D=ge:{start}",
}
# The full monthly history of the same exchange rates (about 14 MB), used only here, to measure each
# country's exchange-rate regime year by year (the page then needs only the result).
ER_HISTORY_URL = "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/ER/+/*.XDC_USD.EOP_RT.M"
# The year each euro-area member adopted the euro; from then on it floats with the euro.
EURO_SINCE = {"AUT": 1999, "BEL": 1999, "FIN": 1999, "FRA": 1999, "DEU": 1999, "IRL": 1999, "ITA": 1999, "LUX": 1999,
              "NLD": 1999, "PRT": 1999, "ESP": 1999, "GRC": 2001, "SVN": 2007, "CYP": 2008, "MLT": 2008, "SVK": 2009,
              "EST": 2011, "LVA": 2014, "LTU": 2015, "HRV": 2023, "BGR": 2026}
DEM_PER_EUR = 1.95583
# The IMF's grouping of countries in the World Economic Outlook: advanced economies (including the
# euro area) and emerging and developing economies by region.
GROUPS_URL = "https://api.imf.org/external/sdmx/3.0/structure/hierarchy/IMF.RES/H_WEO_COUNTRIES/+"
NAMES_URL = "https://api.imf.org/external/sdmx/3.0/structure/codelist/IMF/CL_COUNTRY/+"
CSV_TYPE = "application/vnd.sdmx.data+csv;version=2.0.0"

# The IMF's official names, shortened for tables and the map.
SHORT_NAMES = {
    "CHN": "China", "HKG": "Hong Kong", "MAC": "Macao", "KOR": "South Korea", "PRK": "North Korea",
    "COD": "DR Congo", "COG": "Congo", "NLD": "Netherlands", "GMB": "Gambia", "FSM": "Micronesia",
    "NRU": "Nauru", "TWN": "Taiwan", "LAO": "Laos", "SYR": "Syria",
}


def download(url: str) -> str:
    req = urllib.request.Request(url, headers={"Accept": CSV_TYPE, "User-Agent": "cofer-dashboard"})
    with urllib.request.urlopen(req, timeout=120) as res:
        text = res.read().decode("utf-8")
    if not text.startswith("STRUCTURE") or "OBS_VALUE" not in text.splitlines()[0]:
        raise RuntimeError(f"the IMF did not return data in the expected CSV format ({url})")
    return text


def series(text: str, indicator_col: str = "INDICATOR") -> dict:
    """SDMX-CSV -> {indicator: {country: {period: value in US$ billions}}}, countries only."""
    lines = text.strip().splitlines()
    h = lines[0].split(",")
    c, i, t, v = (h.index(n) for n in ("COUNTRY", indicator_col, "TIME_PERIOD", "OBS_VALUE"))
    out = {}
    for line in lines[1:]:
        r = line.split(",")
        # countries only (not aggregates such as G163, the euro area), from 1980, when the WEO's GDP starts
        if not (len(r[c]) == 3 and r[c].isalpha()) or r[t] < "1980":
            continue
        try:
            val = float(r[v])
        except ValueError:
            continue
        out.setdefault(r[i], {}).setdefault(r[c], {})[r[t]] = round(val / 1e9, 3)
    return out


def monthly_rates(text: str) -> dict:
    """SDMX-CSV of exchange rates -> {country: {month: rate}}; keeps G163 (the euro) for the comparisons."""
    lines = text.strip().splitlines()
    h = lines[0].split(",")
    c, t, v = (h.index(n) for n in ("COUNTRY", "TIME_PERIOD", "OBS_VALUE"))
    out = {}
    for line in lines[1:]:
        r = line.split(",")
        try:
            val = float(r[v])
        except ValueError:
            continue
        if val > 0 and ((len(r[c]) == 3 and r[c].isalpha()) or r[c] == "G163"):
            out.setdefault(r[c], {})[r[t]] = float(f"{val:.6g}")
    return out


def classify(usd: list, eur: list) -> str:
    """One window of 25 end-of-month rates (domestic currency per US dollar, and per euro) -> "P" pegged,
    "M" managed or "F" floating. The same rule as measureRegimes() in the template: pegged if within a
    2% range against the dollar or the euro; managed if in at least half of the 6-month windows the rate
    stays within a 2% band around its trend against the dollar or a 50/50 dollar-euro basket."""
    def span(xs):
        v = [math.log(x) for x in xs]
        return (math.exp(max(v) - min(v)) - 1) * 100

    def banded(xs):
        v = [math.log(x) for x in xs]
        ok = n = 0
        for i in range(len(v) - 6):
            w = v[i:i + 7]
            my = sum(w) / 7
            b = sum((x - 3) * (y - my) for x, y in enumerate(w)) / 28
            res = [y - (my + b * (x - 3)) for x, y in enumerate(w)]
            n += 1
            ok += (max(res) - min(res)) * 100 <= 2
        return ok / n if n else 0

    if span(usd) <= 2 or span(eur) <= 2:
        return "P"
    basket = [u / e ** 0.5 for u, e in zip(usd, [u / x for u, x in zip(usd, eur)])]
    return "M" if max(banded(usd), banded(basket)) >= 0.5 else "F"


def regime_history(text: str, first_year: int = 1980) -> dict:
    """Each country's measured regime at the end of every year since first_year, from the 25 months up to
    then: {country: "PPMMF-F..."} ("-" where there are too few rates)."""
    rates = monthly_rates(text)
    eur = dict(rates.get("G163", {}))  # euros per dollar; before 1999 the Deutsche mark at the euro's rate
    for m, v in rates.get("DEU", {}).items():
        if m < "1999-M01":
            eur[m] = v / DEM_PER_EUR
    months = sorted(eur)
    last = int(months[-1][:4])
    out = {}
    for c, rs in rates.items():
        if not (len(c) == 3 and c.isalpha()):
            continue
        have = [m for m in months if m in rs]
        code = ""
        for y in range(first_year, last + 1):
            # the dollar, the euro, and the Deutsche mark (the euro's stand-in before 1999) are the anchors
            if c in ("USA", "DEU") or EURO_SINCE.get(c, 9999) <= y:
                code += "F"
                continue
            ms = [m for m in have if m <= f"{y}-M12"][-25:]
            if len(ms) < 19 or ms[-1] < f"{y}-M01":
                code += "-"
                continue
            code += classify([rs[m] for m in ms], [rs[m] / eur[m] for m in ms])
        if code.strip("-"):
            out[c] = code
    return {"from": first_year, "codes": out}


def country_groups(text: str) -> dict:
    """The WEO hierarchy -> {"econ": {country: "AE" or "EM"}, "region": {country: group}, "euro": [...]}."""
    world = json.loads(text)["data"]["hierarchies"][0]["hierarchicalCodes"][0]
    code = lambda node: node["id"].split("___")[-1]

    def leaves(node):
        kids = node.get("hierarchicalCodes", [])
        return [code(node)] if not kids else [c for k in kids for c in leaves(k)]

    econ, region, euro = {}, {}, []
    for group in world["hierarchicalCodes"]:
        g = code(group)
        for sub in group.get("hierarchicalCodes", []):
            for k in leaves(sub):
                if not (len(k) == 3 and k.isalpha()):
                    continue
                econ[k] = "AE" if g == "G110" else "EM"
                region[k] = "AE" if g == "G110" else code(sub)
                if code(sub) == "G163":
                    euro.append(k)
    return {"econ": econ, "region": region, "euro": sorted(set(euro))}


def country_names(text: str) -> dict:
    codes = json.loads(text)["data"]["codelists"][0]["codes"]
    return {x["id"]: SHORT_NAMES.get(x["id"], x["name"].split(",")[0]) for x in codes if len(x["id"]) == 3 and x["id"].isalpha()}


def countries(raw: dict) -> dict:
    q, a, weo = series(raw["iipQ"]), series(raw["iipA"]), series(raw["weo"])
    data = {"resQ": q.get("R", {}), "goldQ": q.get("R_F11_MV", {}), "resA": a.get("R", {}),
            "goldA": a.get("R_F11_MV", {}),
            "gdp": weo.get("NGDPD", {}), "rates": monthly_rates(raw["erM"]), "groups": country_groups(raw["groups"]),
            "regHist": regime_history(raw["erHist"])}
    used = set().union(*(data[k].keys() for k in ("resQ", "resA", "goldQ", "goldA", "gdp")))
    names = country_names(raw["names"])
    data["names"] = {k: names.get(k, k) for k in sorted(used)}
    return data


def latest_quarter(text: str) -> str:
    header = text.splitlines()[0].split(",")
    freq, period = header.index("FREQUENCY"), header.index("TIME_PERIOD")
    return max(row.split(",")[period] for row in text.splitlines()[1:] if row and row.split(",")[freq] == "Q")


def main():
    if "--offline" in sys.argv:
        if not RAW.exists():
            sys.exit("No downloaded data yet: run without --offline first.")
        text = RAW.read_text(encoding="utf-8")
        er = RAW_ER.read_text(encoding="utf-8") if RAW_ER.exists() else ""
        raw = {k: (RAW.parent / f"{k}.csv").read_text(encoding="utf-8") for k in COUNTRY_URLS}
        raw["names"] = (RAW.parent / "names.json").read_text(encoding="utf-8")
        raw["groups"] = (RAW.parent / "groups.json").read_text(encoding="utf-8")
        raw["erHist"] = (RAW.parent / "erHist.csv").read_text(encoding="utf-8")
        status = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else {}
    else:
        text, er = download(DATA_URL), download(ER_URL)
        start = f"{datetime.now().year - 3}-M{datetime.now().month:02d}"
        raw = {k: download(url.format(start=start)) for k, url in COUNTRY_URLS.items()}
        raw["erHist"] = download(ER_HISTORY_URL)
        for k, url in (("names", NAMES_URL), ("groups", GROUPS_URL)):
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "cofer-dashboard"}), timeout=120) as res:
                raw[k] = res.read().decode("utf-8")
        status = {"downloaded": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        RAW.parent.mkdir(parents=True, exist_ok=True)
        RAW.write_text(text, encoding="utf-8")
        RAW_ER.write_text(er, encoding="utf-8")
        for k, t in raw.items():
            (RAW.parent / f"{k}.{'json' if k in ('names', 'groups') else 'csv'}").write_text(t, encoding="utf-8")
        STATUS.write_text(json.dumps(status), encoding="utf-8")
    status["latest"] = latest_quarter(text)

    snapshot = json.dumps({"csv": text, "er": er, "countries": countries(raw), **status}, separators=(",", ":"))
    html = TEMPLATE.read_text(encoding="utf-8").replace("__SNAPSHOT__", snapshot.replace("</", "<\\/"))
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"COFER data through {status['latest']} (downloaded {status.get('downloaded', 'unknown')})")
    print(f"Dashboard written to {OUTPUT}")
    if "--open" in sys.argv:
        webbrowser.open(OUTPUT.as_uri())


if __name__ == "__main__":
    main()
