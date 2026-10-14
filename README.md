# IMF COFER dashboard

An interactive dashboard of the IMF's **COFER** data (Currency Composition of Official Foreign
Exchange Reserves): which currencies the world's central banks hold their reserves in, as shares
and in US dollars, quarterly since 1999 and yearly since 1995.

```
python update.py --open      # download the latest data, build, open the page
python update.py --offline   # rebuild from the copy in data/raw
```

No packages to install: the build uses only Python's standard library, and the page loads
Plotly from a CDN.

The output is a single file, `output/dashboard.html`, with the downloaded data embedded. Each
time the page opens it also fetches the current release straight from the IMF's API (which
allows requests from any web page). New quarters and revisions therefore appear without
rebuilding; "Check for updates" asks again. If the IMF cannot be reached, the page shows the
embedded copy. The current view is stored in the URL after `#`, so a bookmarked or shared link
reopens the same selection.

Tabs:
- **Currencies**: shares of allocated reserves as lines, stacked, or one chart per currency,
  with the changes over 1 quarter, 1, 5 and 10 years and the highs and lows; and the same
  currencies in US$ billions (stacked, lines or one chart each), with growth rates. Beside each
  chart, bars show every currency on one date: the latest, or any date clicked on the chart.
- **Changes**: the change between any two dates, by currency, in US$, % or share points, and
  each quarter's change for one currency.
- **Data** (last): the numbers as a table, with a CSV download: the world by currency (shares or
  US$, with world GDP and FX reserves as % of it), or every country (reserves with and without
  gold, gold, GDP and % of GDP, with its economy, region and exchange-rate regime; a selector with a
  search box picks which countries to show and download).
- **Countries**: each country's reserves (IMF, International Investment Position) as % of GDP
  (IMF, World Economic Outlook) or in US$, with or without gold: a group builder (groups of
  countries by region, economy and exchange-rate regime, up to four side by side as ranked bars,
  and compared year by year since 1990; to start, Europe's advanced economies with floating
  currencies against those with pegged ones), a sortable ranking and a chart over time for chosen countries; a bubble chart of GDP against reserves (bubble area: share of
  world reserves) that plays year by year since 1990, with filters for advanced/emerging,
  pegged/managed/floating and region; also gold alone, and comparisons of advanced and
  emerging economies, regions, and pegged, managed and floating currencies (measured from the
  IMF's monthly exchange rates), also year by year since 1980.
- **Norway** (last): a slide set comparing Norway with similar countries (advanced economies with
  their own floating currency) and with advanced and emerging economies with floating, managed and
  pegged currencies: key figures, the peers ranked, fixed against floating, the medians over time,
  gold and a table. Each slide has a comment worked out from the latest figures and its sources, and
  downloads as a 16:9 PNG on a white background for presentations.
- **Explore**: a bar chart race of the currencies since 1999; how much of each currency's change in
  share came from exchange-rate moves and how much from central banks' holdings (with the IMF's
  exchange rates); estimated purchases and sales; and the effective number of reserve currencies.

The page comes in English (`output/dashboard.html`, online at `/`) and Norwegian
(`output/dashboard-no.html`, online at `/no/`), with a switch at the top that keeps the current
view. The Norwegian page is made from the same template by `i18n_no.py`, a list of translations
(with the countries' Norwegian names). If a text in the template changes, the build stops and lists
the translations that no longer match, so nothing is left in English by accident.

Files:
- `update.py`: downloads the data and writes the pages
- `templates/dashboard.html`: the page; all calculations run in the browser
- `i18n_no.py`: the Norwegian translation

Data: IMF, [COFER](https://data.imf.org/en/datasets/IMF.STA:COFER), from the SDMX 3.0 API at
`https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/COFER/+/G001.*.*.*.*`
(world totals; the IMF stopped publishing the advanced/emerging split after 1999).

## Online (public)

Served at https://imf-cofer.jskjeltorp.workers.dev (Cloudflare Workers static assets, open to
everyone). The page fetches the IMF's current data itself, so it stays up to date without
redeploying; redeploy only to refresh the embedded copy or after changing the page:

    python update.py
    rm -rf site && mkdir -p site/no && cp output/dashboard.html site/index.html \
      && cp output/dashboard-no.html site/no/index.html \
      && printf '/*\n  Cache-Control: no-cache\n' > site/_headers
    wrangler deploy
