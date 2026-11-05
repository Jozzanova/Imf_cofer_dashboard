# Monthly update and letter routine

You keep the IMF COFER dashboard current and write its dated reserves letter, in English and in Norwegian. You start with
a fresh clone of this repository; the raw data is not in it and is downloaded by the update script. Do the steps in order.

## 1. Refresh and build

    git pull --rebase origin main
    python update.py                      # downloads COFER, exchange rates, IIP, WEO, IRFCL gold, gold price, SSB; builds output/*.html. Give it a 15-minute timeout.
    python brief.py                       # the numbers for the letter

`update.py` writes `output/dashboard.html` (English) and `output/dashboard-no.html` (Norwegian). If a download fails it
stops with an error; report it and try once more before giving up. Dependencies: Python 3 standard library only.

## 2. Decide what the letter covers

The brief states the latest COFER quarter and the previous letter's date. COFER is published at the end of March, June,
September and December, so in January, April, July and October the letter leads with the new quarter's currency
composition; in other months it says COFER is unchanged and leads with gold. The gold and Norway notes are in every letter.

## 3. Write the letter in both languages

Create `data/letters/YYYY-MM-DD.md` (English) and `data/letters/YYYY-MM-DD.no.md` (Norwegian bokmål, the same content, not a
word-for-word translation but the same facts), dated today (UTC). Format:

    # Reserves letter, 3 December 2026            (Norwegian: # Reservebrev, 3. desember 2026)

    Lead paragraph: the most important development, with its number.

    ## Currency composition          (## Valutasammensetning)
    ## Gold                          (## Gull)
    ## Norway                        (## Norge)
    ## Data status                   (## Datastatus)

Length 350 to 600 words. Every figure from the brief, with the quarter or month it refers to. For the currency composition,
use the exchange-rate against holdings split the brief gives: say whether a currency's share moved because of its exchange
rate or because central banks changed their holdings. For gold, give the value and share, the price move, and the named
buyers and sellers in tonnes, and say which quarter the panel is full for. For Norway, reserves in USD bn, the share of GDP
and of mainland GDP, the change over a year, and the rank among advanced economies. In Data status, say what the IMF has
published, how far the IIP panel is complete, and when the next COFER release is due (end of the next quarter month). Say
plainly what is not yet known. No investment advice.

## 4. Publish

    rm -rf site && mkdir -p site/no && cp output/dashboard.html site/index.html && cp output/dashboard-no.html site/no/index.html && printf '/*\n  Cache-Control: no-cache\n' > site/_headers
    npx --yes wrangler@4 deploy            # needs CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID; skip and say so if missing
    git add data/letters
    git commit -m "Reserves letter YYYY-MM-DD: <the lead sentence, shortened>"
    git pull --rebase origin main && git push origin main

The letters are the only files to commit (data and output are not versioned; the next run rebuilds them). Note: `update.py`
embeds the letters, so run it before the site is assembled; if you wrote the letter after building, run
`python update.py --offline` to rebuild from the downloaded copy and then assemble and deploy.

Finish with a short report: what the letter says, what was new in the data, and anything that failed.
