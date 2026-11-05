"""Prints a numeric brief for the monthly letter agent, from the data embedded in output/dashboard.html (run update.py first).

    python brief.py

Sections: COFER (latest quarter's currency shares, changes over one and four quarters, amounts, the split of each share
change into exchange-rate and holdings effects, the imputed part); gold (central-bank gold value and share, the price, the
largest buyers and sellers of the latest quarter by ounces); Norway (reserves, gold, percent of GDP, change over a year, rank
among advanced economies); data status. Nothing is downloaded.
"""
from __future__ import annotations
import csv, io, json, re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
html = (ROOT / "output" / "dashboard.html").read_text(encoding="utf-8")
i = html.index("const SNAPSHOT = "); j = html.index("\n", i)
S = json.loads(html[i + len("const SNAPSHOT = "):j].rstrip(";"))
out = []; P = out.append
f = lambda x, d=1: "n/a" if x is None else f"{x:,.{d}f}"
sg = lambda x, d=2, u="": "n/a" if x is None else f"{x:+,.{d}f}{u}"

def sdmx(text):
    lines = text.strip().splitlines(); h = lines[0].split(",")
    return [dict(zip(h, l.split(","))) for l in lines[1:]]

# ---- COFER ----
rows = [r for r in sdmx(S["csv"]) if r["COUNTRY"] == "G001" and r["FREQUENCY"] == "Q"]
share, val, total, imputed = {}, {}, {}, {}
for r in rows:
    p, v = r["TIME_PERIOD"], float(r["OBS_VALUE"]) if r["OBS_VALUE"] not in ("", "NaN") else None
    if v is None: continue
    cur = r["FXR_CURRENCY"].replace("CI_", "")
    if r["INDICATOR"] == "AFXRA" and r["TYPE_OF_TRANSFORMATION"] == "SHRO_PT": share.setdefault(cur, {})[p] = v
    if r["INDICATOR"] == "AFXRA" and r["TYPE_OF_TRANSFORMATION"] == "NV_USD": val.setdefault(cur, {})[p] = v / 1e9
    if r["INDICATOR"] == "TFXRA" and r["TYPE_OF_TRANSFORMATION"] == "NV_USD" and cur == "T": total[p] = v / 1e9
    if r["INDICATOR"] == "TFXRA_IMP" and r["TYPE_OF_TRANSFORMATION"] == "SHRO_PT": imputed[p] = v
periods = sorted(total); t = periods[-1]; t1 = periods[-2]; t4 = periods[-5] if len(periods) >= 5 else None
CURS = ["USD", "EUR", "JPY", "GBP", "CNY", "CAD", "AUD", "CHF", "OTHC"]
NAME = {"USD": "US dollar", "EUR": "euro", "JPY": "yen", "GBP": "sterling", "CNY": "renminbi", "CAD": "Canadian dollar", "AUD": "Australian dollar", "CHF": "Swiss franc", "OTHC": "other currencies"}
P(f"BRIEF {date.today().isoformat()}; data downloaded {S.get('downloaded')}; COFER latest quarter {t} (previous {t1})")
P(f"\n== COFER, shares of allocated reserves, {t} ==")
P(f"total FX reserves {f(total[t], 0)} bn USD ({sg(100 * (total[t] / total[t1] - 1), 1, ' %')} vs {t1}{f'; {sg(100 * (total[t] / total[t4] - 1), 1, chr(37))} vs {t4}' if t4 else ''}); imputed by the IMF {f(imputed.get(t), 1)} % of total")
for c in CURS:
    s = share.get(c, {}); a = val.get(c, {})
    if t not in s: continue
    P(f"- {NAME[c]}: {f(s[t], 2)} % ({sg(s[t] - s.get(t1), 2, ' pp')} vs {t1}{f', {sg(s[t] - s.get(t4), 2, chr(32) + chr(112) + chr(112))} vs {t4}' if t4 and t4 in s else ''}); {f(a.get(t), 0)} bn USD ({sg(a.get(t, 0) - a.get(t1, 0), 0, ' bn')} vs {t1})")
# revisions: compare the previous quarter's share now with ... (not available without the old release) -> skip
# exchange-rate vs holdings split of the latest quarter's share changes
er = [r for r in sdmx(S["er"]) if r["FREQUENCY"] == "Q" and r["OBS_VALUE"] not in ("", "NaN")]
rate = {}
for r in er: rate.setdefault(r["COUNTRY"], {})[r["TIME_PERIOD"]] = float(r["OBS_VALUE"])
CTRY = {"EUR": "G163", "JPY": "JPN", "GBP": "GBR", "CNY": "CHN", "CAD": "CAN", "AUD": "AUS", "CHF": "CHE"}
const = {}
for c in CURS:
    a = val.get(c, {})
    if t not in a: continue
    r = rate.get(CTRY.get(c, ""), {})
    const[c] = a[t] * (r[t] / r[t1]) if c in CTRY and t in r and t1 in r else a[t]   # current holdings revalued at last quarter's rates
tot_const = sum(const.values())
if tot_const:
    P(f"share change {t1} -> {t} split into exchange rates and holdings (pp):")
    for c in CURS:
        if c not in const or t not in share.get(c, {}) or t1 not in share.get(c, {}): continue
        sc = 100 * const[c] / tot_const; d = share[c][t] - share[c][t1]
        P(f"- {NAME[c]}: total {sg(d, 2)}; exchange rates {sg(share[c][t] - sc, 2)}; holdings {sg(sc - share[c][t1], 2)}")
    P("(other currencies have no single exchange rate and are held at current values)")
# a year of history for context
P(f"shares a year of quarters back ({', '.join(periods[-5:])}): " + "; ".join(f"{c} " + "/".join(f(share[c].get(p), 1) for p in periods[-5:]) for c in ("USD", "EUR", "JPY", "GBP", "CNY") if c in share))

# ---- gold ----
C = S["countries"]; G = S["gold"]; res, gold, vol, price = C["resQ"], C["goldQ"], G["vol"], G["price"]
qs = sorted({p for c in gold for p in gold[c]}); n_by_q = {p: sum(1 for c in gold if gold[c].get(p) is not None and res.get(c, {}).get(p)) for p in qs}
full = [p for p in qs if n_by_q[p] >= 0.75 * max(n_by_q[x] for x in qs[-12:])]; gq = full[-1]; gq1 = qs[qs.index(gq) - 1]; gq4 = qs[qs.index(gq) - 4]
def panel(p):
    cs = [c for c in gold if gold[c].get(p) is not None and res.get(c, {}).get(p)]
    return sum(gold[c][p] for c in cs), sum(res[c][p] for c in cs), len(cs)
gp, rp, n = panel(gq)
P(f"\n== Gold, latest quarter with a full panel {gq} ({n} countries reporting reserves and gold) ==")
P(f"- gold {f(gp, 0)} bn USD at market value = {f(100 * gp / rp, 1)} % of those countries' total reserves (a year earlier {f(100 * panel(gq4)[0] / panel(gq4)[1], 1)} %)")
months = sorted(price); pm = months[-1]
def q_month(q): y, k = q.split("-Q"); return f"{y}-M{int(k) * 3:02d}"
pq, pq1, pq4 = price.get(q_month(gq)), price.get(q_month(gq1)), price.get(q_month(gq4))
P(f"- gold price {f(price[pm], 0)} USD/oz in {pm}; quarter-end {gq} {f(pq, 0)} ({sg(100 * (pq / pq1 - 1), 1, ' %') if pq and pq1 else 'n/a'} vs {gq1}; {sg(100 * (pq / pq4 - 1), 1, ' %') if pq and pq4 else 'n/a'} vs {gq4})")
# ounces: some countries report a thousand times too many or too few; the page corrects them from the gold's value, so do the same
val = G["val"]
def oz(c, q):
    v = vol[c].get(q)
    if v is None: return None
    pr = price.get(q_month(q)); w = val.get(c, {}).get(q)
    if pr and w:
        ratio = (v * pr / 1000) / w          # value implied by the ounces / reported value (both bn USD)
        if ratio > 300: v /= 1000
        elif ratio < 1 / 300: v *= 1000
    return v
chg = []
for c in vol:
    a, b = oz(c, gq1), oz(c, gq)
    if a is not None and b is not None and abs(b - a) * 31.1035 >= 0.5: chg.append((b - a, c))   # million troy ounces, at least half a tonne
chg.sort()
names = C.get("names", {})
tonnes = lambda moz: moz * 31.1035   # million oz -> tonnes
P("- largest buyers in the quarter (tonnes): " + (", ".join(f"{names.get(c, c)} {tonnes(d):+,.0f}" for d, c in sorted(chg, reverse=True)[:5] if d > 0) or "none"))
P("- largest sellers in the quarter (tonnes): " + (", ".join(f"{names.get(c, c)} {tonnes(d):+,.0f}" for d, c in chg[:5] if d < 0) or "none"))
ychg = sorted(((oz(c, gq) - oz(c, gq4)), c) for c in vol if oz(c, gq) is not None and oz(c, gq4) is not None)
P("- largest buyers over four quarters (tonnes): " + ", ".join(f"{names.get(c, c)} {tonnes(d):+,.0f}" for d, c in sorted(ychg, reverse=True)[:5] if d > 0))
P("- net change over four quarters, all reporters: " + f"{tonnes(sum(d for d, c in ychg)):+,.0f} tonnes ({len(ychg)} countries)")
top = sorted(((gold[c].get(gq) or 0), c) for c in gold if gold[c].get(gq)); top.reverse()
P("- largest holders by value, bn USD: " + ", ".join(f"{names.get(c, c)} {f(v, 0)}" for v, c in top[:6]))
dropped = [c for c in gold if gold[c].get(gq1) is not None and gold[c].get(gq) is None]
P(f"- countries reporting in {gq1} but not yet in {gq}: {len(dropped)}; quarters after {gq} are not yet full")

# ---- Norway ----
P("\n== Norway ==")
nq = sorted(k for k, v in res.get("NOR", {}).items() if v); q = nq[-1]; q4 = nq[-5] if len(nq) >= 5 else None
gdp = C["gdp"].get("NOR", {}); yr = q[:4]; g = gdp.get(yr) or gdp.get(str(int(yr) - 1))
ng = (gold.get("NOR", {}).get(q) or C.get("goldIrfcl", {}).get("NOR", {}).get(yr) or 0)
P(f"- reserves {f(res['NOR'][q], 1)} bn USD at {q} (gold {f(ng, 1)} bn), {f(100 * res['NOR'][q] / g, 1) if g else 'n/a'} % of {yr} GDP ({f(g, 0)} bn USD)" + (f"; vs {q4}: {sg(res['NOR'][q] - res['NOR'][q4], 1, ' bn')} ({sg(100 * (res['NOR'][q] / res['NOR'][q4] - 1), 1, ' %')})" if q4 else ""))
noFn = C.get("noFn") or {}
if isinstance(noFn, dict) and noFn.get(yr): P(f"- mainland Norway is {f(100 * noFn[yr], 0)} % of GDP: reserves are {f(100 * res['NOR'][q] / (g * noFn[yr]), 1)} % of mainland GDP")
ae = [c for c in res if C["groups"]["econ"].get(c) == "AE" and res[c].get(q)]
rank = sorted(ae, key=lambda c: -res[c][q]); pct = {c: res[c][q] / (C["gdp"].get(c, {}).get(yr) or C["gdp"].get(c, {}).get(str(int(yr) - 1)) or 0) for c in ae if C["gdp"].get(c)}
pct = {c: v for c, v in pct.items() if v}
P(f"- rank among {len(ae)} advanced economies at {q}: {rank.index('NOR') + 1 if 'NOR' in rank else 'n/a'} by reserves; {sorted(pct, key=lambda c: -pct[c]).index('NOR') + 1 if 'NOR' in pct else 'n/a'} of {len(pct)} by reserves to GDP")
peers = [c for c in rank if c != "NOR"][:8]
P("- largest advanced-economy reserve holders, bn USD: " + ", ".join(f"{names.get(c, c)} {f(res[c][q], 0)}" for c in rank[:8]))
nq_hist = [p for p in nq if p.endswith("Q4")][-6:]
P("- Norway year-ends, bn USD: " + ", ".join(f"{p[:4]} {f(res['NOR'][p], 0)}" for p in nq_hist))

# ---- status ----
P("\n== Data status ==")
latest_iip = qs[-1]; P(f"- COFER through {t}; IIP reserves/gold through {latest_iip} ({n_by_q[latest_iip]} reporters so far; full panel through {gq}); gold ounces through {sorted({p for c in vol for p in vol[c]})[-1]}; gold price through {pm}; GDP (WEO) estimates through {max(gdp)}")
ltr = S.get("letters") or []
if ltr: P(f"- previous letter: {ltr[-1]['date']} ({(ltr[-1].get('en') or {}).get('title', '')})")
print("\n".join(out))
