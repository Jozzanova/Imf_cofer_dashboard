"""Download the IMF's COFER data and build the dashboard.

Usage:
    python update.py            # download the latest data, then build
    python update.py --offline  # build from the copy in data/raw
    python update.py --open     # also open the dashboard in your browser

It also downloads the end-of-quarter exchange rates of the listed currencies (IMF, Exchange Rates
dataset), which the Explore tab uses to separate currency moves from central banks' own choices.

The dashboard is a single file, output/dashboard.html, with this download embedded. When it is
opened it also asks the IMF for newer data itself, so a quarter published since the last build
appears without running this script again.
"""

import json
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
CSV_TYPE = "application/vnd.sdmx.data+csv;version=2.0.0"


def download(url: str) -> str:
    req = urllib.request.Request(url, headers={"Accept": CSV_TYPE, "User-Agent": "cofer-dashboard"})
    with urllib.request.urlopen(req, timeout=120) as res:
        text = res.read().decode("utf-8")
    if not text.startswith("STRUCTURE") or "OBS_VALUE" not in text.splitlines()[0]:
        raise RuntimeError(f"the IMF did not return data in the expected CSV format ({url})")
    return text


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
        status = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else {}
    else:
        text, er = download(DATA_URL), download(ER_URL)
        status = {"downloaded": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        RAW.parent.mkdir(parents=True, exist_ok=True)
        RAW.write_text(text, encoding="utf-8")
        RAW_ER.write_text(er, encoding="utf-8")
        STATUS.write_text(json.dumps(status), encoding="utf-8")
    status["latest"] = latest_quarter(text)

    snapshot = json.dumps({"csv": text, "er": er, **status}, separators=(",", ":"))
    html = TEMPLATE.read_text(encoding="utf-8").replace("__SNAPSHOT__", snapshot.replace("</", "<\\/"))
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"COFER data through {status['latest']} (downloaded {status.get('downloaded', 'unknown')})")
    print(f"Dashboard written to {OUTPUT}")
    if "--open" in sys.argv:
        webbrowser.open(OUTPUT.as_uri())


if __name__ == "__main__":
    main()
