"""The Norwegian (bokmål) version of the dashboard: update.py applies these replacements to the English
template to write output/dashboard-no.html.

PAIRS are exact replacements of English text (each must still be found in the template: update.py
stops with a list of any that are not, so a change to the English text is not silently left untranslated).
BLOCKS replace everything between two markers. REGEX handles the units. NAMES are the countries' names.
"""

# everything between these markers (the markers stay)
BLOCKS = [
    ('<ul class="notes">', '</ul>', '''
        <li><b>COFER</b> (<a href="https://data.imf.org/en/datasets/IMF.STA:COFER" target="_blank" rel="noopener">Currency Composition of Official Foreign Exchange Reserves</a>)
          er IMFs undersøkelse av hvilke valutaer sentralbankene holder valutareservene sine i. Landene rapporterer til IMF i fortrolighet; IMF
          publiserer bare verdenstallene som vises her. Valutareservene omfatter ikke gull, SDR og reserveposisjonen i IMF.</li>
        <li><b>Andeler</b> er prosent av de <i>fordelte</i> reservene: de der valutasammensetningen er kjent. I gjeldende utgave er de
          ufordelte reservene null fra 2000; i 1995–1999 var de omtrent en femdel av totalen (vist i grått i diagrammet i US-dollar).
          Fra 2025 K3 oppgir IMF også den delen av reservene der IMF selv har anslått sammensetningen, omtrent 10 %.</li>
        <li><b>Beløp</b> er i US-dollar til hver periodes markedskurser. En endring i et beløp blander derfor det sentralbankene
          har kjøpt eller solgt med verdiendringer: når dollaren stiger, er reserver i andre valutaer verdt færre dollar. Det samme gjelder andelene.</li>
        <li><b>Årstall</b> er beholdningene ved årets slutt (fjerde kvartal). Før 1999 finnes bare årstall, og euroens
          forløpere (tyske mark, franske franc, nederlandske gylden og ECU) vises samlet som <i>Euroens forløpere</i>.</li>
        <li><b>Andre valutaer</b> er alt utenom de åtte valutaene IMF viser hver for seg, for eksempel koreanske won,
          singaporske dollar og de nordiske valutaene. Renminbi vises for seg fra 2016 K4, australske og kanadiske dollar fra 2012 K4;
          før det inngår de i andre valutaer.</li>
        <li><b>Utforsk:</b> kappløpet rangerer valutaene hvert kvartal. <i>Valutakurser eller sentralbankenes valg</i> verdsetter hver
          valutas beholdning til valutakursene på startdatoen (kurser ved kvartalsslutt fra IMFs datasett
          <a href="https://data.imf.org/en/datasets/IMF.STA:ER" target="_blank" rel="noopener">Exchange Rates</a>): forskjellen
          mellom den faktiske andelen og den andelen er virkningen av valutakursene; resten er endringen i beholdningene. «Andre valutaer» har
          ingen enkelt valutakurs og holdes til dagens verdier. Kjøp og salg anslås på samme måte, kvartal for kvartal, til
          gjennomsnittet av kursene ved kvartalets start og slutt. Begge deler er anslag: endringer i hvilke land som rapporterer, og IMFs egne
          revisjoner og anslag, telles også som «beholdninger».</li>
        <li><b>Land:</b> hvert lands offisielle reserver fra IMFs
          <a href="https://data.imf.org/en/datasets/IMF.STA:IIP" target="_blank" rel="noopener">International Investment Position</a>-statistikk
          (valuta, gull til markedsverdi, SDR, reserveposisjonen i IMF og andre reserver), kvartalsvis der landet
          rapporterer kvartalsvis og ellers ved årsslutt, delt på samme kalenderårs BNP i US-dollar fra IMFs
          <a href="https://data.imf.org/en/datasets/IMF.RES:WEO" target="_blank" rel="noopener">World Economic Outlook</a> (siste år er
          et anslag fra IMF). Norges BNP er SSBs, etter <a href="https://www.ssb.no/nasjonalregnskap-og-konjunkturer/nasjonalregnskap/artikler/oppjustert-niva-og-vekst-for-verdiskaping-i-norge" target="_blank" rel="noopener">hovedrevisjonen av nasjonalregnskapet</a> i
          november 2025, som løftet BNP-nivået med om lag 4 prosent (for 2023). Kilder fra før revisjonen viser lavere BNP, som om lag 483 mrd. US$
          for 2024 mot 501 mrd. nå, og dermed høyere reserver som andel av BNP. Reservene er en beholdning og BNP en årlig strøm, slik de vanligvis sammenlignes. «Siste tilgjengelige» bruker hvert lands
          nyeste tall, hvis det ikke er mer enn to år gammelt. Der International Investment Position mangler et tall for gull (eller oppgir nesten
          ingenting der IRFCL har en milliard dollar eller mer, som for Tyrkia, der reservene også er oppgitt uten gullet), brukes gull til markedsverdi for kvartalet eller ved årsslutt fra IMFs <a href="https://data.imf.org/en/datasets/IMF.STA:IRFCL" target="_blank" rel="noopener">IRFCL</a>-statistikk
          (Norges gull, solgt i 2004, finnes bare der); mangler begge, antas landets sist rapporterte beholdning. Land som ikke er medlemmer av IMF (som Taiwan) eller ikke rapporterer, mangler.
          Dette er nasjonale totaler, ikke valutasammensetningen: den publiserer IMF bare for verden samlet.
          Avanserte økonomier og fremvoksende økonomier og regionene er gruppene i World Economic Outlook. Valutaregimene måles ut fra
          valutakursene ved månedsslutt de siste to årene (se merknaden under «Sammenlign grupper»); med månedstall kan noen få valutaer
          havne i en naboklasse til IMFs offisielle. For gruppene over tid bruker hvert år de to årene med valutakurser
          fram til årets slutt (fra IMFs fulle månedshistorikk; før 1999 står tyske mark, til euroens omregningskurs, for
          euroen), og land i euroområdet regnes som flytende fra året de tok i bruk euro. Avanserte og fremvoksende økonomier og regioner
          bruker dagens grupper fra IMF for alle år.</li>
        <li><b>Direkte fra IMF:</b> hver gang siden åpnes, spør den IMFs API etter gjeldende utgave av COFER, så nye kvartaler og revisjoner vises
          uten at siden bygges på nytt. Kan IMF ikke nås, viser siden kopien den ble bygd med. IMF publiserer COFER én gang i
          kvartalet, omtrent tre måneder etter at kvartalet er slutt, og reviderer tidligere tall når landene reviderer sine.</li>
      '''),
]

PAIRS = [
    # the page
    ('<html lang="en" data-theme="dark">', '<html lang="nb" data-theme="dark">'),
    ('<title>IMF COFER Dashboard</title>', '<title>IMF COFER-dashbord</title>'),
    ('const LANG = "en";', 'const LANG = "no";'),
    ('const SEPARATORS = ".,";', 'const SEPARATORS = ", ";'),
    ('v.toLocaleString("en-US",', 'v.toLocaleString("nb-NO",'),
    ('toLocaleString("en-GB",', 'toLocaleString("nb-NO",'),
    (': "unknown";', ': "ukjent";'),
    ('p.replace("-Q", " Q")', 'p.replace("-Q", " K")'),
    ('<h1>Currency composition of foreign exchange reserves</h1>', '<h1>Valutasammensetningen i verdens valutareserver</h1>'),
    ('''<p>The IMF's COFER data: the currencies the world's central banks hold their foreign exchange reserves in,
        quarterly since 1999 and yearly since 1995.</p>''',
     '''<p>IMFs COFER-data: valutaene verdens sentralbanker holder valutareservene sine i,
        kvartalsvis siden 1999 og årlig siden 1995.</p>'''),
    ('aria-label="Data status"', 'aria-label="Datastatus"'),
    ('type="button">Check for updates</button>', 'type="button">Se etter oppdateringer</button>'),
    ('updateBtn.textContent = "Check for updates";', 'updateBtn.textContent = "Se etter oppdateringer";'),
    ('updateBtn.textContent = "Checking…";', 'updateBtn.textContent = "Sjekker…";'),
    ('<span class="theme-label">Language</span>', '<span class="theme-label">Språk</span>'),
    ('aria-label="Language"', 'aria-label="Språk"'),
    ('<span class="theme-label">Theme</span>', '<span class="theme-label">Utseende</span>'),
    ('role="group" aria-label="Theme"><button data-v="dark">Dark</button><button data-v="light">Light</button><button data-v="auto">Auto</button>',
     'role="group" aria-label="Utseende"><button data-v="dark">Mørk</button><button data-v="light">Lys</button><button data-v="auto">Auto</button>'),
    ('aria-label="Latest quarter"', 'aria-label="Siste kvartal"'),
    ('aria-label="Views"', 'aria-label="Visninger"'),
    ('aria-controls="tab-shares">Currencies</button>', 'aria-controls="tab-shares">Valutaer</button>'),
    ('aria-controls="tab-changes">Changes</button>', 'aria-controls="tab-changes">Endringer</button>'),
    ('aria-controls="tab-countries">Countries</button>', 'aria-controls="tab-countries">Land</button>'),
    ('aria-controls="tab-explore">Explore ✦</button>', 'aria-controls="tab-explore">Utforsk ✦</button>'),
    ('aria-controls="tab-data">Data</button>', 'aria-controls="tab-data">Data</button>'),
    ('aria-controls="tab-country">Single country</button>', 'aria-controls="tab-country">Enkeltland</button>'),
    ('aria-controls="tab-gold">Gold</button>', 'aria-controls="tab-gold">Gull</button>'),
    ('''<p class="hint">The IMF has reported the Canadian and Australian dollars separately since 2012 Q4 and the Chinese renminbi since 2016 Q4;
        before then they are part of “Other currencies”, so that share drops at those dates without any change in holdings.</p>''',
     '''<p class="hint">IMF har rapportert kanadiske og australske dollar for seg siden 2012 K4 og kinesiske renminbi siden 2016 K4;
        før det inngår de i «Andre valutaer», så den andelen faller på disse tidspunktene uten at beholdningene har endret seg.</p>'''),
    ('''<p class="hint">The IMF has reported the Canadian and Australian dollars separately since 2012 Q4 and the Chinese renminbi since 2016 Q4;
        before then they are part of “Other currencies”, so that amount drops at those dates without any change in holdings.</p>''',
     '''<p class="hint">IMF har rapportert kanadiske og australske dollar for seg siden 2012 K4 og kinesiske renminbi siden 2016 K4;
        før det inngår de i «Andre valutaer», så det beløpet faller på disse tidspunktene uten at beholdningene har endret seg.</p>'''),
    ('aria-label="Selection"', 'aria-label="Utvalg"'),
    ('<span class="lbl">Currencies</span>', '<span class="lbl">Valutaer</span>'),
    ('id="cur-all">All</button>', 'id="cur-all">Alle</button>'),
    ('id="cur-nousd">All but the dollar</button>', 'id="cur-nousd">Alle utenom dollaren</button>'),
    ('<span class="lbl">Frequency</span>', '<span class="lbl">Frekvens</span>'),
    ('<button data-v="Q">Quarterly</button><button data-v="A">Yearly</button>', '<button data-v="Q">Kvartalsvis</button><button data-v="A">Årlig</button>'),
    ('<span class="lbl">Period</span>', '<span class="lbl">Periode</span>'),
    ('<button data-v="all">All</button><button data-v="2008">', '<button data-v="all">Alle</button><button data-v="2008">'),
    ('<button data-v="10y">10Y</button><button data-v="5y">5Y</button>', '<button data-v="10y">10 år</button><button data-v="5y">5 år</button>'),
    # Currencies tab
    ('<h2 id="sh-h2">Share of allocated reserves</h2>', '<h2 id="sh-h2">Andel av de fordelte reservene</h2>'),
    ('aria-label="Chart type"><button data-v="lines">Lines</button><button data-v="stack">Stacked</button><button data-v="multi">One chart each</button>',
     'aria-label="Diagramtype"><button data-v="lines">Linjer</button><button data-v="stack">Stablet</button><button data-v="multi">Ett diagram hver</button>'),
    ('aria-label="Chart type"><button data-v="stack">Stacked</button><button data-v="lines">Lines</button><button data-v="multi">One chart each</button>',
     'aria-label="Diagramtype"><button data-v="stack">Stablet</button><button data-v="lines">Linjer</button><button data-v="multi">Ett diagram hver</button>'),
    ('id="sh-log"> Log scale</label>', 'id="sh-log"> Logaritmisk skala</label>'),
    ('title="Shares of total reserves, foreign exchange plus monetary gold at market value, for the countries that report both to the IMF"><input type="checkbox" id="sh-gold"> Include gold</label>',
     'title="Andeler av de samlede reservene, valuta pluss monetært gull til markedsverdi, for landene som rapporterer begge deler til IMF"><input type="checkbox" id="sh-gold"> Ta med gull</label>'),
    ('CUR.GLD = { k: "GLD", name: "Gold", color: "--gold" };', 'CUR.GLD = { k: "GLD", name: "Gull", color: "--gold" };'),
    ('state.shGold ? "Share of reserves including gold" : "Share of allocated reserves"', 'state.shGold ? "Andel av reservene medregnet gull" : "Andel av de fordelte reservene"'),
    ('? "% of total reserves including gold at market value"', '? "% av de samlede reservene medregnet gull til markedsverdi"'),
    ('`Gold: COFER\'s currency shares are scaled to total reserves, foreign exchange plus monetary gold at market value. Gold\'s share is measured over the ${nRep.length ? `${Math.min(...nRep)} to ${Math.max(...nRep)}` : ""} countries reporting both to the IMF\'s International Investment Position, chain-linked so that countries joining or leaving the reporting do not move it; the newest quarters are left out until most countries have reported.`',
     '`Gull: COFERs valutaandeler er skalert til de samlede reservene, valuta pluss monetært gull til markedsverdi. Gullets andel måles over de ${nRep.length ? `${Math.min(...nRep)} til ${Math.max(...nRep)}` : ""} landene som rapporterer begge deler til IMFs International Investment Position, kjedet slik at land som kommer til eller faller fra i rapporteringen ikke flytter den; de nyeste kvartalene utelates til de fleste landene har rapportert.`'),
    ('title="Shares of total reserves including monetary gold at market value, or, in US dollars, gold implied by that share"><input type="checkbox" id="dt-gold"> Include gold</label>',
     'title="Andeler av de samlede reservene medregnet monetært gull til markedsverdi, eller, i US-dollar, gull beregnet fra den andelen"><input type="checkbox" id="dt-gold"> Ta med gull</label>'),
    ('name: k === "GLD" ? "Gold" : CUR[k].name', 'name: k === "GLD" ? "Gull" : CUR[k].name'),
    ('{ name: "Gold, implied from its share", y: gv, d: 1 }, { name: "Total reserves including gold", y: f.total.map((t, i) => fin(t) && fin(gv[i]) ? t + gv[i] : null), d: 1 },\n        { name: "Gold, % of total reserves", y: g.map(v => fin(v) ? 100 * v : null), d: 2 }',
     '{ name: "Gull, beregnet fra andelen", y: gv, d: 1 }, { name: "Samlede reserver medregnet gull", y: f.total.map((t, i) => fin(t) && fin(gv[i]) ? t + gv[i] : null), d: 1 },\n        { name: "Gull, % av samlede reserver", y: g.map(v => fin(v) ? 100 * v : null), d: 2 }'),
    ('(state.dtGold ? "Share of total reserves including gold at market value, %, newest first; gold\'s share chain-linked over the countries reporting both to the IMF" : "Share of allocated reserves, %, newest first")',
     '(state.dtGold ? "Andel av de samlede reservene medregnet gull til markedsverdi, %, nyeste først; gullets andel kjedet over landene som rapporterer begge deler til IMF" : "Andel av de fordelte reservene, %, nyeste først")'),
    ('+ (state.dtGold ? "; gold implied by its share of total reserves" : "")', '+ (state.dtGold ? "; gull beregnet fra andelen av de samlede reservene" : "")'),
    ('? "Share of total reserves including gold in %; changes in percentage points. "', '? "Andel av de samlede reservene medregnet gull i %; endringer i prosentpoeng. "'),
    ('id="am-log"> Log scale</label>', 'id="am-log"> Logaritmisk skala</label>'),
    ('<h2>Shares and how they changed</h2>', '<h2>Andelene og hvordan de har endret seg</h2>'),
    ('<h2>Reserves by currency, in US dollars</h2>', '<h2>Reserver etter valuta, i US-dollar</h2>'),
    ('<h2>Amounts and growth</h2>', '<h2>Beløp og vekst</h2>'),
    ('"click the chart for another date; a bar or a name in the legend for that currency alone, Ctrl+click to add or remove one"',
     '"klikk i diagrammet for en annen dato; på en stolpe eller et navn i forklaringen for bare den valutaen, Ctrl+klikk for å legge til eller ta bort en"'),
    ('`Total $${fmt(f.total[i] / 1000, 2)} tn · `', '`Totalt $${fmt(f.total[i] / 1000, 2)} bill. · `'),
    ('`${share ? "Shares" : "US$ billions"}, ${label(f.periods[i])}${i === w.i1 ? " (latest)" : ""}`',
     '`${share ? "Andeler" : "mrd. US$"}, ${label(f.periods[i])}${i === w.i1 ? " (siste)" : ""}`'),
    ('empty(el, "No figures for this date.")', 'empty(el, "Ingen tall for denne datoen.")'),
    ('"no figure a year earlier"', '"ikke noe tall et år før"'),
    ('" pp")} in a year`', '" pp")} på et år`'),
    ('"%")} in a year`', '"%")} på et år`'),
    ('name: "Unallocated", meta: "UN"', 'name: "Ufordelt", meta: "UN"'),
    ('name: "Unallocated", color: css("--unalloc")', 'name: "Ufordelt", color: css("--unalloc")'),
    ('bn<extra>Unallocated</extra>', 'mrd.<extra>Ufordelt</extra>'),
    ('`${state.freq === "Q" ? "Quarterly" : "Year-end"}, ${label(f.periods[w.i0])} to ${label(f.periods[w.i1])}, `',
     '`${state.freq === "Q" ? "Kvartalsvis" : "Ved årsslutt"}, ${label(f.periods[w.i0])} til ${label(f.periods[w.i1])}, `'),
    (': "% of reserves whose currency is known");', ': "% av reservene der valutaen er kjent");'),
    ('"Pick at least one currency above."', '"Velg minst én valuta ovenfor."'),
    ('[1, "1 quarter"] : null, [py, "1 year"], [5 * py, "5 years"], [10 * py, "10 years"]', '[1, "1 kvartal"] : null, [py, "1 år"], [5 * py, "5 år"], [10 * py, "10 år"]'),
    ('const head = `<tr><th>Currency</th><th>${label(f.periods[n])}</th>${back.map(([, t]) => `<th>vs ${t} earlier</th>`).join("")}\n    <th>since ${label(f.periods[w.i0])}</th><th>Highest</th><th>Lowest</th></tr>`;',
     'const head = `<tr><th>Valuta</th><th>${label(f.periods[n])}</th>${back.map(([, t]) => `<th>mot ${t} før</th>`).join("")}\n    <th>siden ${label(f.periods[w.i0])}</th><th>Høyest</th><th>Lavest</th></tr>`;'),
    (': "Share of allocated reserves in %; changes in percentage points. ") + "Highest and lowest are within the period chosen above."',
     ': "Andel av de fordelte reservene i %; endringer i prosentpoeng. ") + "Høyest og lavest gjelder perioden valgt ovenfor."'),
    ('`${state.freq === "Q" ? "End of each quarter" : "End of each year"}, US$ billions at market exchange rates`',
     '`${state.freq === "Q" ? "Ved slutten av hvert kvartal" : "Ved slutten av hvert år"}, mrd. US$ til markedskurser`'),
    ('(stack ? "; the grey area is reserves whose currency is not known" : multi ? "; each chart has its own scale" : "")',
     '(stack ? "; det grå feltet er reserver der valutaen ikke er kjent" : multi ? "; hvert diagram har sin egen skala" : "")'),
    ('const head = `<tr><th>Currency</th><th>${label(f.periods[n])}, US$ bn</th><th>vs 1 year earlier, bn</th><th>1 year, %</th>\n    <th>5 years, % a year</th><th>10 years, % a year</th></tr>`;',
     'const head = `<tr><th>Valuta</th><th>${label(f.periods[n])}, mrd. US$</th><th>mot 1 år før, mrd.</th><th>1 år, %</th>\n    <th>5 år, % per år</th><th>10 år, % per år</th></tr>`;'),
    ('row("Total foreign exchange reserves", f.total, true)', 'row("Valutareserver totalt", f.total, true)'),
    ('"Growth over 5 and 10 years is the average yearly rate (compound). Dollar amounts include exchange-rate valuation."',
     '"Veksten over 5 og 10 år er gjennomsnittlig årlig vekst (sammensatt). Dollarbeløpene omfatter verdiendringer fra valutakursene."'),
    # Changes tab
    ('<span class="lbl">From</span><select id="ch-from" aria-label="From">', '<span class="lbl">Fra</span><select id="ch-from" aria-label="Fra">'),
    ('<span class="lbl">To</span><select id="ch-to" aria-label="To">', '<span class="lbl">Til</span><select id="ch-to" aria-label="Til">'),
    ('<span class="lbl">Span</span>', '<span class="lbl">Spenn</span>'),
    ('<button data-v="1">1 period</button><button data-v="1y">1Y</button><button data-v="5y">5Y</button><button data-v="10y">10Y</button>',
     '<button data-v="1">1 periode</button><button data-v="1y">1 år</button><button data-v="5y">5 år</button><button data-v="10y">10 år</button>'),
    ('<span class="lbl">Measure</span>\n          <div class="seg" id="ch-metric-seg"><button data-v="bn">US$ billions</button><button data-v="pct">% change</button><button data-v="pp">Share, percentage points</button>',
     '<span class="lbl">Mål</span>\n          <div class="seg" id="ch-metric-seg"><button data-v="bn">mrd. US$</button><button data-v="pct">Endring i %</button><button data-v="pp">Andel, prosentpoeng</button>'),
    ('<h2 id="ch-title">Change by currency</h2>', '<h2 id="ch-title">Endring etter valuta</h2>'),
    ('<h2 id="ch2-title">Change in each period</h2>', '<h2 id="ch2-title">Endring i hver periode</h2>'),
    ('<select id="ch-cur" aria-label="Currency">', '<select id="ch-cur" aria-label="Valuta">'),
    ('<h2>Behind the change</h2>', '<h2>Bak endringen</h2>'),
    ('''<p class="sub">A change in the US-dollar amount includes valuation: when the dollar strengthens, reserves held in other
        currencies are worth fewer dollars even if no central bank sold any. Shares move for the same reason.</p>''',
     '''<p class="sub">En endring i dollarbeløpet omfatter verdiendringer: når dollaren styrker seg, er reserver i andre
        valutaer verdt færre dollar selv om ingen sentralbank har solgt noe. Andelene beveger seg av samme grunn.</p>'''),
    ('document.querySelector(\'#ch-span-seg [data-v="1"]\').textContent = state.freq === "Q" ? "1 quarter" : "1 year";',
     'document.querySelector(\'#ch-span-seg [data-v="1"]\').textContent = state.freq === "Q" ? "1 kvartal" : "1 år";'),
    ('bn: { unit: " bn", d: 0, title: "Change in holdings, US$ billions", prefix: "$" },', 'bn: { unit: " mrd.", d: 0, title: "Endring i beholdningene, mrd. US$", prefix: "$" },'),
    ('pct: { unit: "%", d: 1, title: "Change in holdings, %" },', 'pct: { unit: "%", d: 1, title: "Endring i beholdningene, %" },'),
    ('pp: { unit: " pp", d: 2, title: "Change in share, percentage points" },', 'pp: { unit: " pp", d: 2, title: "Endring i andel, prosentpoeng" },'),
    ('ticksuffix: m.unit.trim() === "bn" ?', 'ticksuffix: m.unit.trim() === "mrd." ?'),
    ('`${span}, by currency. Click a currency to see its change in each period on the right.`', '`${span}, etter valuta. Klikk på en valuta for å se endringen i hver periode til høyre.`'),
    ('const span = `${label(state.chFrom)} to ${label(state.chTo)}`;', 'const span = `${label(state.chFrom)} til ${label(state.chTo)}`;'),
    ('"None of the chosen currencies has figures for both dates."', '"Ingen av de valgte valutaene har tall for begge datoene."'),
    ('`${c.name}: change in each ${state.freq === "Q" ? "quarter" : "year"}`', '`${c.name}: endring i hvert ${state.freq === "Q" ? "kvartal" : "år"}`'),
    ('`${m.title.replace(/^Change in /, "").replace(/^./, s => s.toUpperCase())}, ${label(f.periods[w.i0])} to ${label(f.periods[w.i1])}`',
     '`${m.title.replace(/^Endring i /, "").replace(/^./, s => s.toUpperCase())}, ${label(f.periods[w.i0])} til ${label(f.periods[w.i1])}`'),
    ('`No figures for the ${inText(k)} in this period.`', '`Ingen tall for ${inText(k)} i denne perioden.`'),
    ('const head = `<tr><th>Currency</th><th>${pa}, bn</th><th>${pb}, bn</th><th>Change, bn</th><th>Change, %</th>\n    <th>Share ${pa}</th><th>Share ${pb}</th><th>Change, pp</th></tr>`;',
     'const head = `<tr><th>Valuta</th><th>${pa}, mrd.</th><th>${pb}, mrd.</th><th>Endring, mrd.</th><th>Endring, %</th>\n    <th>Andel ${pa}</th><th>Andel ${pb}</th><th>Endring, pp</th></tr>`;'),
    ('<td>Total foreign exchange reserves</td>', '<td>Valutareserver totalt</td>'),
    ('"The period chosen here sets the right-hand chart; the left one compares the two dates above it."', '"Perioden valgt her styrer diagrammet til høyre; det til venstre sammenligner de to datoene over det."'),
    # Data tab
    ('<h2>The numbers</h2>', '<h2>Tallene</h2>'),
    ('aria-label="Dataset"><button data-v="cur">World, by currency</button><button data-v="cty">Countries</button>', 'aria-label="Datasett"><button data-v="cur">Verden, etter valuta</button><button data-v="cty">Land</button>'),
    ('aria-label="Measure"><button data-v="share">Shares, %</button><button data-v="bn">US$ billions</button></div>',
     'aria-label="Mål"><button data-v="share">Andeler, %</button><button data-v="bn">mrd. US$</button></div>'),
    ('<select id="dt-year" aria-label="Date">', '<select id="dt-year" aria-label="Dato">'),
    ('id="dt-csv">Download CSV</button>', 'id="dt-csv">Last ned CSV</button>'),
    ('id="dt-xlsx">Download Excel</button>', 'id="dt-xlsx">Last ned Excel</button>'),
    ('title="Year-end shares by currency, one sheet without gold and one with, in the layout of a summary table">Download summary table (Excel)</button>',
     'title="Andeler per valuta ved årsslutt, ett ark uten gull og ett med, i oppsettet til en oppsummeringstabell">Last ned oppsummeringstabell (Excel)</button>'),
    ('sheet = { name: "Countries", freeze: 1', 'sheet = { name: "Land", freeze: 1'),
    ('sheet = { name: state.dtMetric === "share" ? "Shares" : "US$ bn", freeze: 1', 'sheet = { name: state.dtMetric === "share" ? "Andeler" : "mrd. US$", freeze: 1'),
    ('[[c("Period", "hdr")]', '[[c("Periode", "hdr")]'),
    ('about = [`${rows.length} countries, ${state.dtYear === "latest" ? "each country\'s latest figures" : `end of ${state.dtYear}`}, largest reserves first. Reserves include gold at market value; US$ billions.`,\n      "Reserves: IMF, International Investment Position. GDP: IMF, World Economic Outlook (the latest year an estimate). Exchange-rate regimes as measured over the last two years from the IMF\'s monthly exchange rates."];',
     'about = [`${rows.length} land, ${state.dtYear === "latest" ? "hvert lands nyeste tall" : `ved utgangen av ${state.dtYear}`}, største reserver først. Reservene inkluderer gull til markedsverdi; mrd. US$.`,\n      "Reserver: IMF, International Investment Position. BNP: IMF, World Economic Outlook (siste år er et anslag). Valutakursregimer målt over de siste to årene fra IMFs månedlige valutakurser."];'),
    ('"Source: IMF, Currency Composition of Official Foreign Exchange Reserves (COFER), world totals." + (state.dtGold ? " Gold: monetary gold at market value from the IMF\'s International Investment Position, its share chain-linked over the countries reporting both reserves and gold; the currency shares are COFER\'s shares scaled to total reserves including gold." : "")',
     '"Kilde: IMF, Currency Composition of Official Foreign Exchange Reserves (COFER), verdenstall." + (state.dtGold ? " Gull: monetært gull til markedsverdi fra IMFs International Investment Position, andelen kjedet over landene som rapporterer både reserver og gull; valutaandelene er COFERs andeler skalert til samlede reserver medregnet gull." : "")'),
    ('{ name: "About", cols: [110], grid: false, rows: [[c("IMF COFER dashboard", "title")], [c(`Generated ${new Date().toISOString().slice(0, 16).replace("T", " ")} UTC; data downloaded ${SNAPSHOT.downloaded || ""}`, "mut")]',
     '{ name: "Om", cols: [110], grid: false, rows: [[c("IMF COFER-dashbord", "title")], [c(`Laget ${new Date().toISOString().slice(0, 16).replace("T", " ")} UTC; data lastet ned ${SNAPSHOT.downloaded || ""}`, "mut")]'),
    ('cols.push({ name: "Unallocated", y: f.unallocated, d: 1 }, { name: "Total FX reserves", y: f.total, d: 1 });', 'cols.push({ name: "Ufordelt", y: f.unallocated, d: 1 }, { name: "Valutareserver totalt", y: f.total, d: 1 });'),
    ('{ name: "World GDP", y: wgdp, d: 0 }, { name: "FX reserves, % of world GDP",', '{ name: "Verdens BNP", y: wgdp, d: 0 }, { name: "Valutareserver, % av verdens BNP",'),
    ('{ name: "Imputed by the IMF, % of total",', '{ name: "Anslått av IMF, % av totalen",'),
    ('`<option value="latest">Latest available</option>` +\n    years.map(y => `<option value="${y}"${y === state.dtYear ? " selected" : ""}>End of ${y}</option>`)',
     '`<option value="latest">Siste tilgjengelige</option>` +\n    years.map(y => `<option value="${y}"${y === state.dtYear ? " selected" : ""}>Utgangen av ${y}</option>`)'),
    ('const head = ["Country", "Economy", "Region", "Exchange rate", "As of", "Reserves, US$ bn", "Gold, US$ bn", "Excluding gold, US$ bn",\n    "GDP, US$ bn", "Reserves, % of GDP", "Excluding gold, % of GDP"];',
     'const head = ["Land", "Økonomi", "Region", "Valutakurs", "Per", "Reserver, mrd. US$", "Gull, mrd. US$", "Uten gull, mrd. US$",\n    "BNP, mrd. US$", "Reserver, % av BNP", "Uten gull, % av BNP"];'),
    ('({ AE: "Advanced", EM: "Emerging and developing" })[CD.groups?.econ?.[c.k]]', '({ AE: "Avansert", EM: "Fremvoksende og utviklingsøkonomi" })[CD.groups?.econ?.[c.k]]'),
    ('`${rows.length} ${rows.length === 1 ? "country" : "countries"}, ${state.dtYear === "latest" ? "each country\'s latest figures" : `end of ${state.dtYear}`}, largest reserves first. ` +\n      "Reserves include gold at market value; exchange-rate regimes as measured over the last two years."',
     '`${rows.length} land, ${state.dtYear === "latest" ? "hvert lands nyeste tall" : `utgangen av ${state.dtYear}`}, største reserver først. ` +\n      "Reservene omfatter gull til markedsverdi; valutaregimer målt over de siste to årene."'),
    ('`Reserves: IMF, <a href="https://data.imf.org/en/datasets/IMF.STA:IIP" target="_blank" rel="noopener">International Investment Position</a>;\n      GDP: IMF, <a href="https://data.imf.org/en/datasets/IMF.RES:WEO" target="_blank" rel="noopener">World Economic Outlook</a> (the latest year an estimate).\n      "Download CSV" saves this table. ${fnNote()}`',
     '`Reserver: IMF, <a href="https://data.imf.org/en/datasets/IMF.STA:IIP" target="_blank" rel="noopener">International Investment Position</a>;\n      BNP: IMF, <a href="https://data.imf.org/en/datasets/IMF.RES:WEO" target="_blank" rel="noopener">World Economic Outlook</a> (siste år er et anslag).\n      «Last ned CSV» lagrer denne tabellen. ${fnNote()}`'),
    (': "US$ billions at market exchange rates, newest first; world GDP for the period\'s calendar year" +', ': "mrd. US$ til markedskurser, nyeste først; verdens BNP for periodens kalenderår" +'),
    ('`"Download CSV" saves the table as shown: the currencies, frequency and period chosen above.\n    The full dataset is on the <a href="https://data.imf.org/en/datasets/IMF.STA:COFER" target="_blank" rel="noopener">IMF data portal</a>.`',
     '`«Last ned CSV» lagrer tabellen slik den vises: valutaene, frekvensen og perioden valgt ovenfor.\n    Hele datasettet finnes på <a href="https://data.imf.org/en/datasets/IMF.STA:COFER" target="_blank" rel="noopener">IMFs dataportal</a>.`'),
    ('`<thead><tr><th>Period</th>', '`<thead><tr><th>Periode</th>'),
    ('[["Period", ...cols.map(c => c.name)]', '[["Periode", ...cols.map(c => c.name)]'),
    ('name = `reserves_by_country_${state.dtYear === "latest" ? "latest" : state.dtYear}.csv`;', 'name = `reserver_etter_land_${state.dtYear === "latest" ? "siste" : state.dtYear}.csv`;'),
    # tiles and status
    ('`<span class="${cls(v - d)}">${signed(v - d, 2, " pp")}</span> in a year`', '`<span class="${cls(v - d)}">${signed(v - d, 2, " pp")}</span> på et år`'),
    ('`Latest quarter: <b>${label(f.periods[n])}</b> · change over the past year, since ${py}`', '`Siste kvartal: <b>${label(f.periods[n])}</b> · endring det siste året, siden ${py}`'),
    ('tile("Total FX reserves", `$${fmt(t / 1000, 2)} tn`, `<span class="${cls(g)}">${signed(g, 1, "%")}</span> in a year`)',
     'tile("Valutareserver totalt", `$${fmt(t / 1000, 2)} bill.`, `<span class="${cls(g)}">${signed(g, 1, "%")}</span> på et år`)'),
    ('tile("Remaining currencies",', 'tile("Øvrige valutaer",'),
    ('</span> in a year · all but USD, EUR, JPY, CNY`', '</span> på et år · alle utenom USD, EUR, JPY, CNY`'),
    ('`Live from the IMF, checked <b>${when(source.at)}</b>`', '`Direkte fra IMF, sjekket <b>${when(source.at)}</b>`'),
    ('`Copy downloaded <b>${when(source.at)}</b>${source.checking ? " · asking the IMF for newer data…" : ""}`', '`Kopi lastet ned <b>${when(source.at)}</b>${source.checking ? " · spør IMF etter nyere tall…" : ""}`'),
    ('`<div>IMF COFER: latest data <b>${label(M.latest)}</b></div><div>${how}</div>`', '`<div>IMF COFER: siste tall <b>${label(M.latest)}</b></div><div>${how}</div>`'),
    ('<span>World totals, <b>${M.Q.periods.length}</b> quarters and <b>${M.A.periods.length}</b> years</span>', '<span>Verdenstall, <b>${M.Q.periods.length}</b> kvartaler og <b>${M.A.periods.length}</b> år</span>'),
    ('<span>Source: <a href="https://data.imf.org/en/datasets/IMF.STA:COFER" target="_blank" rel="noopener">IMF, COFER</a></span>', '<span>Kilde: <a href="https://data.imf.org/en/datasets/IMF.STA:COFER" target="_blank" rel="noopener">IMF, COFER</a></span>'),
    ('setUpdateMsg("Asking the IMF for the current COFER release…")', 'setUpdateMsg("Spør IMF etter gjeldende utgave av COFER…")'),
    ('`the IMF answered ${res.status}`', '`IMF svarte ${res.status}`'),
    ('`New data from the IMF: the figures now run to ${label(fresh.latest)} (were ${label(before)}).`', '`Nye tall fra IMF: tallene går nå til ${label(fresh.latest)} (før ${label(before)}).`'),
    ('`The IMF has revised ${changed} figure${changed === 1 ? "" : "s"} since this page was built; the page now shows the current ones.`',
     '`IMF har revidert ${changed} tall siden denne siden ble bygd; siden viser nå de gjeldende.`'),
    ('"Up to date: this is the IMF\'s current release."', '"Oppdatert: dette er IMFs gjeldende utgave."'),
    ('`Could not reach the IMF (${esc(err.message)}). Showing the copy downloaded ${when(SNAPSHOT.downloaded)}.`', '`Fikk ikke kontakt med IMF (${esc(err.message)}). Viser kopien lastet ned ${when(SNAPSHOT.downloaded)}.`'),
    ('"the IMF\'s data did not have the expected columns"', '"IMFs data hadde ikke de ventede kolonnene"'),
    ('"the IMF\'s data had no quarterly figures"', '"IMFs data hadde ingen kvartalstall"'),
    # currencies
    ('{ k: "USD", name: "US dollar", color: "--s1" },', '{ k: "USD", name: "US-dollar", color: "--s1" },'),
    ('{ k: "EUR", name: "Euro", color: "--s2" },', '{ k: "EUR", name: "Euro", color: "--s2" },'),
    ('name: "Euro predecessors",', 'name: "Euroens forløpere",'),
    ('name: "Japanese yen",', 'name: "Japanske yen",'),
    ('name: "Pound sterling",', 'name: "Britiske pund",'),
    ('name: "Chinese renminbi",', 'name: "Kinesiske renminbi",'),
    ('name: "Canadian dollar",', 'name: "Kanadiske dollar",'),
    ('name: "Australian dollar",', 'name: "Australske dollar",'),
    ('name: "Swiss franc",', 'name: "Sveitsiske franc",'),
    ('name: "Other currencies",', 'name: "Andre valutaer",'),
    ('CUR[k].name.replace(/^(Euro|Pound|Other)/, w => w.toLowerCase())', 'CUR[k].name.replace(/^(Euro|Japanske|Britiske|Kinesiske|Kanadiske|Australske|Sveitsiske|Andre)/, w => w.toLowerCase())'),
    # Explore
    ('<h2>The race for reserves</h2>', '<h2>Kappløpet om reservene</h2>'),
    ('<p class="sub" id="race-sub">Every quarter since 1999. Press play, or drag the slider.</p>', '<p class="sub" id="race-sub">Hvert kvartal siden 1999. Trykk spill av, eller dra i glidebryteren.</p>'),
    ('aria-label="Measure"><button data-v="share">Shares</button><button data-v="bn">US$ billions</button></div>\n          <label class="check"><input type="checkbox" id="race-nousd"> Without the dollar</label>',
     'aria-label="Mål"><button data-v="share">Andeler</button><button data-v="bn">mrd. US$</button></div>\n          <label class="check"><input type="checkbox" id="race-nousd"> Uten dollaren</label>'),
    ('aria-label="Currencies ranked by their share of reserves"', 'aria-label="Valutaene rangert etter andel av reservene"'),
    ('id="race-play" type="button">▶ Play</button>', 'id="race-play" type="button">▶ Spill av</button>'),
    ('id="b-play" type="button">▶ Play</button>', 'id="b-play" type="button">▶ Spill av</button>'),
    ('aria-label="Quarter">', 'aria-label="Kvartal">'),
    ('aria-label="Speed">', 'aria-label="Fart">'),
    ('"▶ Play"', '"▶ Spill av"'),
    ('"❚❚ Pause"', '"❚❚ Pause"'),
    ('`${bn ? "US$ billions" : "Share of allocated reserves"}, every quarter from ${label(M.Q.periods[0])} to ${label(M.latest)}. Press play, or drag the slider; click a currency to look at it below (Ctrl+click to add more).`',
     '`${bn ? "mrd. US$" : "Andel av de fordelte reservene"}, hvert kvartal fra ${label(M.Q.periods[0])} til ${label(M.latest)}. Trykk spill av, eller dra i glidebryteren; klikk på en valuta for å se nærmere på den nedenfor (Ctrl+klikk for flere).`'),
    ('["1999-Q1", "January 1999: the euro is launched."],', '["1999-Q1", "Januar 1999: euroen innføres."],'),
    ('["2008-Q3", "September 2008: Lehman Brothers collapses and the global financial crisis peaks."],', '["2008-Q3", "September 2008: Lehman Brothers kollapser, og finanskrisen når toppen."],'),
    ('["2010-Q2", "May 2010: Greece\'s first rescue starts the euro-area debt crisis."],', '["2010-Q2", "Mai 2010: Hellas\' første redningspakke innleder gjeldskrisen i euroområdet."],'),
    ('["2012-Q4", "From the end of 2012 COFER lists the Canadian and Australian dollars separately."],', '["2012-Q4", "Fra utgangen av 2012 viser COFER kanadiske og australske dollar hver for seg."],'),
    ('["2014-Q3", "Mid-2014 to 2015: the dollar rises sharply against most currencies."],', '["2014-Q3", "Midten av 2014 til 2015: dollaren stiger kraftig mot de fleste valutaer."],'),
    ('["2016-Q4", "October 2016: the renminbi joins the IMF\'s SDR basket; COFER lists it from the end of 2016."],', '["2016-Q4", "Oktober 2016: renminbi tas inn i IMFs SDR-kurv; COFER viser den fra utgangen av 2016."],'),
    ('["2020-Q1", "Early 2020: the COVID-19 pandemic."],', '["2020-Q1", "Tidlig i 2020: koronapandemien."],'),
    ('["2022-Q1", "February 2022: Russia invades Ukraine, and Western countries freeze much of Russia\'s central-bank reserves."],', '["2022-Q1", "Februar 2022: Russland invaderer Ukraina, og vestlige land fryser mye av den russiske sentralbankens reserver."],'),
    ('["2022-Q3", "September 2022: the dollar reaches its highest level in two decades."],', '["2022-Q3", "September 2022: dollaren når sitt høyeste nivå på tjue år."],'),
    ("<h2>Currency moves or central banks' choices?</h2>", '<h2>Valutakurser eller sentralbankenes valg?</h2>'),
    ('''<p class="sub">A currency's share of reserves changes for two reasons: central banks buy or sell it, or its exchange rate
            against the dollar moves. Holding every exchange rate at its level on the start date separates the two.</p>''',
     '''<p class="sub">En valutas andel av reservene endrer seg av to grunner: sentralbankene kjøper eller selger den, eller kursen
            mot dollaren endrer seg. Å holde alle valutakurser fast på nivået på startdatoen skiller de to.</p>'''),
    ('<span class="lbl">Since</span><select id="fx-base" aria-label="Start date">', '<span class="lbl">Siden</span><select id="fx-base" aria-label="Startdato">'),
    ('<span class="lbl">Currency</span><select id="fx-cur" aria-label="Currency">', '<span class="lbl">Valuta</span><select id="fx-cur" aria-label="Valuta">'),
    ('"The exchange rates could not be loaded from the IMF, so this part is not available right now."', '"Valutakursene kunne ikke hentes fra IMF, så denne delen er ikke tilgjengelig nå."'),
    ('empty(el, "No exchange rates.")', 'empty(el, "Ingen valutakurser.")'),
    ('`${c.name}: actual share and at ${label(b)} exchange rates`', '`${c.name}: faktisk andel og til valutakursene i ${label(b)}`'),
    ('name: "Actual" }', 'name: "Faktisk" }'),
    ('name: `At ${label(b)} exchange rates`', 'name: `Til kursene i ${label(b)}`'),
    ('`Change in share, ${label(b)} to ${label(e)}, in percentage points`', '`Endring i andel, ${label(b)} til ${label(e)}, i prosentpoeng`'),
    ('" (click a currency again for all)"', '" (klikk på valutaen igjen for alle)"'),
    ('name: "Holdings", y: names', 'name: "Beholdninger", y: names'),
    ('"%{y}, holdings: %{customdata[0]}<extra></extra>"', '"%{y}, beholdninger: %{customdata[0]}<extra></extra>"'),
    ('name: "Exchange rates", y: names', 'name: "Valutakurser", y: names'),
    ('"%{y}, exchange rates: %{customdata[0]}<extra></extra>"', '"%{y}, valutakurser: %{customdata[0]}<extra></extra>"'),
    ('name: "Total change", y: names', 'name: "Samlet endring", y: names'),
    ('"%{y}, total: %{customdata[0]}<extra></extra>"', '"%{y}, samlet: %{customdata[0]}<extra></extra>"'),
    ('`COFER lists the ${inText(k)} only from ${label(f.periods[f.share[k].findIndex(fin)])}: pick a later start date.`', '`COFER viser ${inText(k)} først fra ${label(f.periods[f.share[k].findIndex(fin)])}: velg en senere startdato.`'),
    ('''ins.innerHTML = `From ${label(b)} to ${label(e)} the ${esc(inText(k))}'s share ${z >= a ? "rose" : "fell"} from
      <b>${fmt(a, 2)}%</b> to <b>${fmt(z, 2)}%</b> (${signed(row.total, 2, " pp")}). Of that, <b>${signed(row.fx, 2, " pp")}</b> came from exchange-rate
      moves and <b>${signed(row.hold, 2, " pp")}</b> from what central banks hold. At ${label(b)} exchange rates the share would be ${fmt(C[k][ie], 2)}%.`;''',
     '''ins.innerHTML = `Fra ${label(b)} til ${label(e)} ${z >= a ? "steg" : "falt"} andelen for ${esc(inText(k))} fra
      <b>${fmt(a, 2)} %</b> til <b>${fmt(z, 2)} %</b> (${signed(row.total, 2, " pp")}). Av dette kom <b>${signed(row.fx, 2, " pp")}</b> fra endringer i
      valutakursene og <b>${signed(row.hold, 2, " pp")}</b> fra det sentralbankene holder. Til valutakursene i ${label(b)} ville andelen vært ${fmt(C[k][ie], 2)} %.`;'''),
    ('<h2>What central banks bought and sold</h2>', '<h2>Hva sentralbankene kjøpte og solgte</h2>'),
    ('''`Cumulative purchases (+) and sales (−) since ${label(b)}, US$ billions, with exchange-rate moves
    taken out. Other currencies are left out: they have no single exchange rate. Click a currency in the legend for it alone, Ctrl+click to add or remove one.`''',
     '''`Samlede kjøp (+) og salg (−) siden ${label(b)}, mrd. US$, uten virkningen av
    valutakursene. Andre valutaer er utelatt: de har ingen enkelt valutakurs. Klikk på en valuta i forklaringen for bare den, Ctrl+klikk for å legge til eller ta bort en.`'''),
    ('<h2>How many reserve currencies?</h2>', '<h2>Hvor mange reservevalutaer?</h2>'),
    ('''`The effective number of currencies, 1 ÷ the sum of the squared shares: what the
    reserves would amount to if they were spread evenly. It went from <b>${fmt(y[i0], 2)}</b> in ${label(f.periods[i0])} to a low of
    ${fmt(y[lo], 2)} in ${label(f.periods[lo])} and <b>${fmt(y[i1], 2)}</b> in ${label(f.periods[i1])}. "Other currencies" counts as one, so the true number is a little higher.`''',
     '''`Det effektive antallet valutaer, 1 ÷ summen av de kvadrerte andelene: hvor mange valutaer reservene
    ville tilsvart om de var jevnt fordelt. Det gikk fra <b>${fmt(y[i0], 2)}</b> i ${label(f.periods[i0])} til et bunnpunkt på
    ${fmt(y[lo], 2)} i ${label(f.periods[lo])} og <b>${fmt(y[i1], 2)}</b> i ${label(f.periods[i1])}. «Andre valutaer» teller som én, så det virkelige tallet er litt høyere.`'''),
    ('name: "Effective number"', 'name: "Effektivt antall"'),
    ('"%{y:.2f} currencies<extra></extra>"', '"%{y:.2f} valutaer<extra></extra>"'),
    # groups and regimes
    ('econ: { label: "Economy", cats: [', 'econ: { label: "Økonomi", cats: ['),
    ('region: { label: "Region", cats: [', 'region: { label: "Region", cats: ['),
    ('regime: { label: "Exchange rate", cats: [', 'regime: { label: "Valutaregime", cats: ['),
    ('{ k: "AE", name: "Advanced economies", color: "--s1" },\n    { k: "EM", name: "Emerging and developing economies", color: "--s2" }] },',
     '{ k: "AE", name: "Avanserte økonomier", color: "--s1" },\n    { k: "EM", name: "Fremvoksende og utviklingsøkonomier", color: "--s2" }] },'),
    ('{ k: "AE", name: "Advanced economies", color: "--s1" },\n    { k: "G505", name: "Emerging and developing Asia", color: "--s2" },\n    { k: "G903", name: "Emerging and developing Europe", color: "--s3" },\n    { k: "G205", name: "Latin America and the Caribbean", color: "--s4" },\n    { k: "G400", name: "Middle East and Central Asia", color: "--s5" },\n    { k: "G603", name: "Sub-Saharan Africa", color: "--s6" }] },',
     '{ k: "AE", name: "Avanserte økonomier", color: "--s1" },\n    { k: "G505", name: "Fremvoksende Asia", color: "--s2" },\n    { k: "G903", name: "Fremvoksende Europa", color: "--s3" },\n    { k: "G205", name: "Latin-Amerika og Karibia", color: "--s4" },\n    { k: "G400", name: "Midtøsten og Sentral-Asia", color: "--s5" },\n    { k: "G603", name: "Afrika sør for Sahara", color: "--s6" }] },'),
    ('{ k: "peg", name: "Pegged", color: "--s1" },\n    { k: "managed", name: "Managed", color: "--s2" },\n    { k: "float", name: "Floating", color: "--s3" }] },',
     '{ k: "peg", name: "Fast", color: "--s1" },\n    { k: "managed", name: "Styrt", color: "--s2" },\n    { k: "float", name: "Flytende", color: "--s3" }] },'),
    ('const ANCHOR = { USD: "the US dollar", EUR: "the euro", BASKET: "a dollar-euro basket",\n  AUS: "the Australian dollar", CHE: "the Swiss franc", ZAF: "the South African rand", IND: "the Indian rupee", SGP: "the Singapore dollar" };',
     'const ANCHOR = { USD: "US-dollaren", EUR: "euroen", BASKET: "en kurv av dollar og euro",\n  AUS: "australske dollar", CHE: "sveitsiske franc", ZAF: "sørafrikanske rand", IND: "indiske rupi", SGP: "singaporske dollar" };'),
    ('note: "Floating: the US dollar" }', 'note: "Flytende: US-dollaren" }'),
    ('note: "Floating: uses the euro" }', 'note: "Flytende: bruker euro" }'),
    ('note: `Pegged to ${ANCHOR[peg[0]]}` }', 'note: `Fast mot ${ANCHOR[peg[0]]}` }'),
    ('note: `Managed against ${ANCHOR[a]}` }', 'note: `Styrt mot ${ANCHOR[a]}` }'),
    ('else out[k] = { r: "float", note: "Floating" };', 'else out[k] = { r: "float", note: "Flytende" };'),
    ('{ k: "eu", name: "Europe" }, { k: "ap", name: "Asia and Pacific" }, { k: "am", name: "Americas" },\n  { k: "me", name: "Middle East and Central Asia" }, { k: "af", name: "Sub-Saharan Africa" }];',
     '{ k: "eu", name: "Europa" }, { k: "ap", name: "Asia og Stillehavet" }, { k: "am", name: "Amerika" },\n  { k: "me", name: "Midtøsten og Sentral-Asia" }, { k: "af", name: "Afrika sør for Sahara" }];'),
    ('const REG_NAMES = { peg: "pegged", managed: "managed", float: "floating" };', 'const REG_NAMES = { peg: "fast", managed: "styrt", float: "flytende" };'),
    ('g.geo === "all" ? "All regions" : GEO.find', 'g.geo === "all" ? "Alle regioner" : GEO.find'),
    ('g.econ === "AE" ? "advanced" : g.econ === "EM" ? "emerging and developing" : "",\n  g.reg.length === 3 ? "any exchange rate" : g.reg.map(r => REG_NAMES[r]).join(" or ")]',
     'g.econ === "AE" ? "avanserte" : g.econ === "EM" ? "fremvoksende" : "",\n  g.reg.length === 3 ? "alle valutaregimer" : g.reg.map(r => REG_NAMES[r]).join(" eller ")]'),
    # Countries tab
    ('<span class="lbl">Measure</span>\n          <div class="seg" id="c-measure-seg"><button data-v="pct">% of GDP</button><button data-v="bn">US$ billions</button>',
     '<span class="lbl">Mål</span>\n          <div class="seg" id="c-measure-seg"><button data-v="pct">% av BNP</button><button data-v="bn">mrd. US$</button>'),
    ('<span class="lbl">Gold</span>\n          <div class="seg" id="c-gold-seg"><button data-v="with">Including gold</button><button data-v="without">Excluding gold</button><button data-v="only">Only gold</button>',
     '<span class="lbl">Gull</span>\n          <div class="seg" id="c-gold-seg"><button data-v="with">Med gull</button><button data-v="without">Uten gull</button><button data-v="only">Bare gull</button>'),
    ('<span class="lbl">Date</span><select id="c-year" aria-label="Date">', '<span class="lbl">Dato</span><select id="c-year" aria-label="Dato">'),
    ('`<option value="latest">Latest available</option>` +\n    years.map(y => `<option value="${y}"${y === state.cYear ? " selected" : ""}>End of ${y}</option>`)',
     '`<option value="latest">Siste tilgjengelige</option>` +\n    years.map(y => `<option value="${y}"${y === state.cYear ? " selected" : ""}>Utgangen av ${y}</option>`)'),
    ('`<option value="">Add a country…</option>`', '`<option value="">Legg til et land…</option>`'),
    ('`live from the IMF, checked ${when(cLive.at)}`', '`direkte fra IMF, sjekket ${when(cLive.at)}`'),
    ('`the copy downloaded ${when(SNAPSHOT.downloaded)}; asking the IMF for newer figures…`', '`kopien lastet ned ${when(SNAPSHOT.downloaded)}; spør IMF etter nyere tall…`'),
    ('`the copy downloaded ${when(SNAPSHOT.downloaded)} (the IMF could not be reached)`', '`kopien lastet ned ${when(SNAPSHOT.downloaded)} (fikk ikke kontakt med IMF)`'),
    (': `the copy downloaded ${when(SNAPSHOT.downloaded)}`;', ': `kopien lastet ned ${when(SNAPSHOT.downloaded)}`;'),
    ('`${Object.keys(CC).length} countries; figures ${how}. ${fnNote()}`', '`${Object.keys(CC).length} land; tallene er ${how}. ${fnNote()}`'),
    ('const cUnit = () => state.cMeasure === "bn" ? "US$ billions" : "% of GDP";', 'const cUnit = () => state.cMeasure === "bn" ? "mrd. US$" : "% av BNP";'),
    ('const goldWords = () => ({ without: "excluding gold", only: "gold only" })[state.cGold] || "including gold";', 'const goldWords = () => ({ without: "uten gull", only: "bare gull" })[state.cGold] || "med gull";'),
    ('<h2>Build and compare groups of countries</h2>', '<h2>Bygg og sammenlign grupper av land</h2>'),
    ('const asOf = state.cYear === "latest" ? "latest figures" : `end of ${state.cYear}`;', 'const asOf = state.cYear === "latest" ? "siste tall" : `utgangen av ${state.cYear}`;'),
    ('`${cUnit()}, ${goldWords()}, ${asOf}. Exchange-rate regimes as measured over the last two years. ` +\n    "Change a group with its menus and buttons; click a bar to follow that country in the chart further down."',
     '`${cUnit()}, ${goldWords()}, ${asOf}. Valutaregimer målt over de siste to årene. ` +\n    "Endre en gruppe med menyene og knappene; klikk på en stolpe for å følge landet i diagrammet lenger ned."'),
    ('title="Remove this group" aria-label="Remove this group"', 'title="Fjern denne gruppen" aria-label="Fjern denne gruppen"'),
    ('<select class="gb-geo" aria-label="Region"><option value="all">All regions</option>', '<select class="gb-geo" aria-label="Region"><option value="all">Alle regioner</option>'),
    ('[["all", "All"], ["AE", "Advanced"], ["EM", "Emerging"]]', '[["all", "Alle"], ["AE", "Avanserte"], ["EM", "Fremvoksende"]]'),
    ('id="gb-add">+ Add a group</button>', 'id="gb-add">+ Legg til en gruppe</button>'),
    ('`<span><b>${n}</b> countries</span><span><b>${fmtBn(tot)}</b> in all</span><span>median <b>${cFmt(med)}</b></span>`',
     '`<span><b>${n}</b> land</span><span><b>${fmtBn(tot)}</b> i alt</span><span>median <b>${cFmt(med)}</b></span>`'),
    ('`<span>combined <b>${fmt(combined, 1)}%</b> of GDP</span>`', '`<span>samlet <b>${fmt(combined, 1)} %</b> av BNP</span>`'),
    ('"<span>No countries match.</span>"', '"<span>Ingen land passer.</span>"'),
    ('"No country with figures matches this group."', '"Ingen land med tall passer i denne gruppen."'),
    ('"<b>%{customdata[0]}</b><br>%{text} · %{customdata[2]}<br>%{customdata[1]}<extra></extra>"', '"<b>%{customdata[0]}</b><br>%{text} · %{customdata[2]}<br>%{customdata[1]}<extra></extra>"'),
    ('<h2>These groups over time</h2>', '<h2>Disse gruppene over tid</h2>'),
    (' · %{customdata} countries<extra>${esc(gbName(g))}</extra>`', ' · %{customdata} land<extra>${esc(gbName(g))}</extra>`'),
    ('''`${bn ? "Total reserves, US$ billions" : "Combined: the group's reserves ÷ its GDP"}, ${goldWords()}, at each year's end since 1990. ` +
    "Each country counts in the regime its currency had that year, so countries move in and out of the groups; the number of reporting countries also grows over time (hover for the count)."''',
     '''`${bn ? "Reserver totalt, mrd. US$" : "Samlet: gruppens reserver ÷ dens BNP"}, ${goldWords()}, ved hvert årsskifte siden 1990. ` +
    "Hvert land teller i det valutaregimet valutaen hadde det året, så land flytter inn og ut av gruppene; antallet land som rapporterer, øker også over tid (pek for antallet)."'''),
    ('"No figures for these groups."', '"Ingen tall for disse gruppene."'),
    ('<h2>Compare groups</h2>', '<h2>Sammenlign grupper</h2>'),
    ('aria-label="Chart"><button data-v="box">Box plot</button><button data-v="bars">Bars</button>', 'aria-label="Diagram"><button data-v="box">Boksplott</button><button data-v="bars">Stolper</button>'),
    ('`<span class="muted">${rs.length} ${rs.length === 1 ? "country" : "countries"} · median ${cFmt(st.med)}</span>', '`<span class="muted">${rs.length} land · median ${cFmt(st.med)}</span>'),
    ('aria-label="Scale"><button data-v="log">Log scale</button><button data-v="lin">Linear</button>', 'aria-label="Skala"><button data-v="log">Logaritmisk skala</button><button data-v="lin">Lineær</button>'),
    ('aria-label="Group by"><button data-v="econ">Advanced vs emerging</button><button data-v="region">Region</button><button data-v="regime">Exchange-rate regime</button>',
     'aria-label="Grupper etter"><button data-v="econ">Avanserte og fremvoksende</button><button data-v="region">Region</button><button data-v="regime">Valutaregime</button>'),
    ('`${cUnit()}, ${goldWords()}, ${state.cYear === "latest" ? "latest figures" : `end of ${state.cYear}`}. ` +\n    `${state.gView === "bars" ? "Each bar is a country, largest first; the dashed line is the median of the group." : "Each dot is a country; the box spans the middle half of each group and the line in it is the median."} ${state.gScale === "log" ? "Log" : "Linear"} scale.`',
     '`${cUnit()}, ${goldWords()}, ${state.cYear === "latest" ? "siste tall" : `utgangen av ${state.cYear}`}. ` +\n    `${state.gView === "bars" ? "Hver stolpe er et land, størst først; den stiplede linjen er gruppens median." : "Hvert punkt er et land; boksen dekker den midterste halvdelen av hver gruppe, og streken i den er medianen."} ${state.gScale === "log" ? "Logaritmisk" : "Lineær"} skala.`'),
    ('"No figures for this selection."', '"Ingen tall for dette utvalget."'),
    ('.replace("Emerging and developing", "Emerging &<br>developing").replace("Latin America and the Caribbean", "Latin America &<br>Caribbean").replace("Middle East and Central Asia", "Middle East &<br>Central Asia").replace("Advanced economies", "Advanced<br>economies").replace("Sub-Saharan Africa", "Sub-Saharan<br>Africa")',
     '.replace("Fremvoksende og utviklingsøkonomier", "Fremvoksende og<br>utviklingsøkonomier").replace("Latin-Amerika og Karibia", "Latin-Amerika<br>og Karibia").replace("Midtøsten og Sentral-Asia", "Midtøsten og<br>Sentral-Asia").replace("Avanserte økonomier", "Avanserte<br>økonomier").replace("Afrika sør for Sahara", "Afrika sør<br>for Sahara")'),
    ('` ${zeros} ${zeros === 1 ? "country has" : "countries have"} none and ${zeros === 1 ? "is" : "are"} left out of the chart.`', '` ${zeros} land har ingen og er utelatt fra diagrammet.`'),
    ('`<thead><tr><th>Group</th><th>Countries</th><th>Median</th>\n    ${bn ? "" : "<th>Combined, % of GDP</th>"}<th>Total, US$ bn</th><th>Share of the total</th></tr></thead>',
     '`<thead><tr><th>Gruppe</th><th>Land</th><th>Median</th>\n    ${bn ? "" : "<th>Samlet, % av BNP</th>"}<th>Totalt, mrd. US$</th><th>Andel av totalen</th></tr></thead>'),
    ('<div class="muted" style="font-size:12px">largest: ${esc(st.top.join(", "))}</div>', '<div class="muted" style="font-size:12px">størst: ${esc(st.top.join(", "))}</div>'),
    ('''`Exchange-rate regimes are measured from the IMF's end-of-month exchange rates over the last two years, following the IMF's de facto tests:
       <b>pegged</b> if the rate stayed within a 2% range against the US dollar or the euro (or 3% against the Australian dollar, Swiss franc,
       South African rand, Indian rupee or Singapore dollar, which some countries use or peg to one to one); <b>managed</b> if, in most 6-month stretches, it stayed
       within a 2% band around its trend against the dollar or a dollar-euro basket (stabilised, crawling and tightly managed rates); <b>floating</b>
       otherwise. Euro-area members float with the euro. This approximates the IMF's official classification (in its AREAER report), which is not
       available as data.`''',
     '''`Valutaregimene måles ut fra IMFs valutakurser ved månedsslutt de siste to årene, etter IMFs faktiske kriterier:
       <b>fast</b> hvis kursen holdt seg innenfor et spenn på 2 % mot US-dollaren eller euroen (eller 3 % mot australske dollar, sveitsiske franc,
       sørafrikanske rand, indiske rupi eller singaporske dollar, som noen land bruker eller knytter seg til én til én); <b>styrt</b> hvis den i de fleste seksmånedersperioder holdt seg
       innenfor et bånd på 2 % rundt trenden mot dollaren eller en kurv av dollar og euro (stabiliserte, glidende og tett styrte kurser); <b>flytende</b>
       ellers. Land i euroområdet flyter med euroen. Dette er en tilnærming til IMFs offisielle klassifisering (i rapporten AREAER), som ikke
       finnes som data.`'''),
    ('''`Groups as in the IMF's World Economic Outlook. "Combined" divides a group's total reserves by its total GDP, so large economies count for more;
       the median treats every country alike. `''',
     '''`Gruppene er som i IMFs World Economic Outlook. «Samlet» deler gruppens samlede reserver på dens samlede BNP, så store økonomier teller mer;
       medianen behandler alle land likt. `'''),
    (': number ${peers.indexOf(homeRow) + 1} of ${peers.length} in its group, ` +\n      `against a median of ${cFmt(st.med)}.<br>`',
     ': nummer ${peers.indexOf(homeRow) + 1} av ${peers.length} i gruppen, ` +\n      `mot en median på ${cFmt(st.med)}.<br>`'),
    ('<h2>GDP and reserves, year by year</h2>', '<h2>BNP og reserver, år for år</h2>'),
    ('<span class="lbl">Up the side</span>\n          <div class="seg" id="b-y-seg"><button data-v="bn">Reserves, US$</button><button data-v="pct">% of GDP</button>',
     '<span class="lbl">Loddrett</span>\n          <div class="seg" id="b-y-seg"><button data-v="bn">Reserver, US$</button><button data-v="pct">% av BNP</button>'),
    ('<span class="lbl">Labels</span>', '<span class="lbl">Navn</span>'),
    ('<button data-v="20">20</button><button data-v="all">All</button>', '<button data-v="20">20</button><button data-v="all">Alle</button>'),
    ('<span class="lbl">Colour by</span>\n          <div class="seg" id="b-color-seg"><button data-v="econ">Economy</button><button data-v="region">Region</button><button data-v="regime">Exchange rate</button>',
     '<span class="lbl">Farge etter</span>\n          <div class="seg" id="b-color-seg"><button data-v="econ">Økonomi</button><button data-v="region">Region</button><button data-v="regime">Valutaregime</button>'),
    ('letter-spacing:.03em">Show</span>', 'letter-spacing:.03em">Vis</span>'),
    ('letter-spacing:.03em">Include</span>', 'letter-spacing:.03em">Ta med</span>'),
    ('data-f="grEcon:AE">Advanced</button><button class="chip" type="button" data-f="grEcon:EM">Emerging &amp; developing</button>',
     'data-f="grEcon:AE">Avanserte</button><button class="chip" type="button" data-f="grEcon:EM">Fremvoksende</button>'),
    ('data-f="grReg:peg">Pegged</button><button class="chip" type="button" data-f="grReg:managed">Managed</button><button class="chip" type="button" data-f="grReg:float">Floating</button>',
     'data-f="grReg:peg">Fast</button><button class="chip" type="button" data-f="grReg:managed">Styrt</button><button class="chip" type="button" data-f="grReg:float">Flytende</button>'),
    ('id="grp-euro">Euro-area members</button>', 'id="grp-euro">Euroområdet</button>'),
    ('<select id="grp-geo" aria-label="Region"><option value="all">All regions</option><option value="eu">Europe</option><option value="ap">Asia and Pacific</option>\n          <option value="am">Americas</option><option value="me">Middle East and Central Asia</option><option value="af">Sub-Saharan Africa</option></select>',
     '<select id="grp-geo" aria-label="Region"><option value="all">Alle regioner</option><option value="eu">Europa</option><option value="ap">Asia og Stillehavet</option>\n          <option value="am">Amerika</option><option value="me">Midtøsten og Sentral-Asia</option><option value="af">Afrika sør for Sahara</option></select>'),
    ('id="grp-reset">Show all</button>', 'id="grp-reset">Vis alle</button>'),
    ('` Filtered: ${rows.length} ${rows.length === 1 ? "country" : "countries"}.`', '` Filtrert: ${rows.length} land.`'),
    ('data-f="bEcon:AE">Advanced</button><button class="chip" type="button" data-f="bEcon:EM">Emerging &amp; developing</button>',
     'data-f="bEcon:AE">Avanserte</button><button class="chip" type="button" data-f="bEcon:EM">Fremvoksende</button>'),
    ('data-f="bReg:peg">Pegged</button><button class="chip" type="button" data-f="bReg:managed">Managed</button><button class="chip" type="button" data-f="bReg:float">Floating</button>',
     'data-f="bReg:peg">Fast</button><button class="chip" type="button" data-f="bReg:managed">Styrt</button><button class="chip" type="button" data-f="bReg:float">Flytende</button>'),
    ('<select id="b-region" aria-label="Region"><option value="all">All regions</option><option value="AE">Advanced economies</option>\n          <option value="G505">Emerging and developing Asia</option><option value="G903">Emerging and developing Europe</option>\n          <option value="G205">Latin America and the Caribbean</option><option value="G400">Middle East and Central Asia</option>\n          <option value="G603">Sub-Saharan Africa</option></select>',
     '<select id="b-region" aria-label="Region"><option value="all">Alle regioner</option><option value="AE">Avanserte økonomier</option>\n          <option value="G505">Fremvoksende Asia</option><option value="G903">Fremvoksende Europa</option>\n          <option value="G205">Latin-Amerika og Karibia</option><option value="G400">Midtøsten og Sentral-Asia</option>\n          <option value="G603">Afrika sør for Sahara</option></select>'),
    ('aria-label="Year">', 'aria-label="År">'),
    ('const sub = `${y}${y === lastYear ? " (latest quarter)" : ", year end"}: ${shown.length} of ${rows.length} countries shown, ` +\n    `holding ${fmt(world ? total / world * 100 : 0, 1)}% of the reserves of all countries with figures, ${goldWords()}. Bubble area: share of world reserves. ` +\n    (state.bColor === "regime" || state.bReg.length < 3 ? "Exchange-rate regimes measured by this dashboard for each year from the IMF\'s exchange rates, with the IMF\'s de facto tests (a 2% band; see the note under “Compare groups”), approximating its official classification. " : "") + "Click a bubble to highlight that country (again to remove it).";',
     'const sub = `${y}${y === lastYear ? " (siste kvartal)" : ", årsslutt"}: ${shown.length} av ${rows.length} land vises, ` +\n    `med ${fmt(world ? total / world * 100 : 0, 1)} % av reservene til alle land med tall, ${goldWords()}. Boblenes areal: andel av verdens reserver. ` +\n    (state.bColor === "regime" || state.bReg.length < 3 ? "Valutaregimene er målt av dette dashbordet for hvert år ut fra IMFs valutakurser, med IMFs de facto-kriterier (et bånd på 2 %; se merknaden under «Sammenlign grupper»), som en tilnærming til IMFs offisielle klassifisering. " : "") + "Klikk på en boble for å fremheve landet (igjen for å fjerne det).";'),
    ('"<b>%{customdata[0]}</b> (%{customdata[5]})<br>GDP %{customdata[1]}<br>Reserves %{customdata[2]} = %{customdata[3]} of GDP<br>%{customdata[4]} of world reserves<extra></extra>"',
     '"<b>%{customdata[0]}</b> (%{customdata[5]})<br>BNP %{customdata[1]}<br>Reserver %{customdata[2]} = %{customdata[3]} av BNP<br>%{customdata[4]} av verdens reserver<extra></extra>"'),
    ('text: `reserves = ${k * 100}% of GDP`', 'text: `reserver = ${k * 100} % av BNP`'),
    ('title: { text: "GDP, US$ (log scale)",', 'title: { text: "BNP, US$ (logaritmisk skala)",'),
    ('title: { text: pctY ? "Reserves, % of GDP (log scale)" : "Reserves, US$ (log scale)",', 'title: { text: pctY ? "Reserver, % av BNP (logaritmisk skala)" : "Reserver, US$ (logaritmisk skala)",'),
    ('<h2>Ranking</h2><p class="sub" id="c-table-sub">Click a column to sort it, a country to add it to the chart.</p>', '<h2>Rangering</h2><p class="sub" id="c-table-sub">Klikk på en kolonne for å sortere, på et land for å legge det til i diagrammet.</p>'),
    ('<select id="c-filter" aria-label="Show"><option value="all">All countries</option><option value="econ:AE">Advanced economies</option>\n              <option value="econ:EM">Emerging and developing</option><option value="regime:peg">Pegged currencies</option>\n              <option value="regime:managed">Managed currencies</option><option value="regime:float">Floating currencies</option></select>',
     '<select id="c-filter" aria-label="Vis"><option value="all">Alle land</option><option value="econ:AE">Avanserte økonomier</option>\n              <option value="econ:EM">Fremvoksende og utviklingsøkonomier</option><option value="regime:peg">Fast valutakurs</option>\n              <option value="regime:managed">Styrt valutakurs</option><option value="regime:float">Flytende valutakurs</option></select>'),
    ('placeholder="Find a country" aria-label="Find a country"', 'placeholder="Finn et land" aria-label="Finn et land"'),
    ('placeholder="Search countries" aria-label="Search countries"', 'placeholder="Søk etter land" aria-label="Søk etter land"'),
    ('data-a="shown">Select those shown</button>', 'data-a="shown">Velg de som vises</button>'),
    ('data-a="none">Show all countries</button>', 'data-a="none">Vis alle land</button>'),
    ('title="Switzerland, Japan, Norway, New Zealand, Sweden, Canada, the UK, Australia and the US">Norway and peers</button>',
     'title="Sveits, Japan, Norge, New Zealand, Sverige, Canada, Storbritannia, Australia og USA">Norge og sammenlignbare land</button>'),
    ('role="group" aria-label="Countries"></div>', 'role="group" aria-label="Land"></div>'),
    ('${th("name", "Country")}${th("v", cUnit())}${th("d", state.cMeasure === "bn" ? "1 year, bn" : "1 year, pp")}<th>Economy · exchange rate</th>${th("p", "As of")}',
     '${th("name", "Land")}${th("v", cUnit())}${th("d", state.cMeasure === "bn" ? "1 år, mrd." : "1 år, pp")}<th>Økonomi · valutaregime</th>${th("p", "Per")}'),
    ('({ AE: "Advanced", EM: "Emerging" })[CD.groups?.econ?.[r.c.k]]', '({ AE: "Avansert", EM: "Fremvoksende" })[CD.groups?.econ?.[r.c.k]]'),
    ('`${rows.length} countries, ${goldWords()}. Click a column to sort it, a country to add it to the chart.`', '`${rows.length} land, ${goldWords()}. Klikk på en kolonne for å sortere, på et land for å legge det til i diagrammet.`'),
    ('<h2 id="c-line-title">Over time</h2>', '<h2 id="c-line-title">Over tid</h2>'),
    ('<select id="c-add" aria-label="Add a country">', '<select id="c-add" aria-label="Legg til et land">'),
    ('<span class="lbl">Show</span>\n            <div class="seg" id="c-lines-seg" role="group" aria-label="Show"><button data-v="countries">Chosen countries</button><button data-v="econ">Advanced vs emerging</button><button data-v="region">Regions</button><button data-v="regime">Exchange-rate regimes</button>',
     '<span class="lbl">Vis</span>\n            <div class="seg" id="c-lines-seg" role="group" aria-label="Vis"><button data-v="countries">Valgte land</button><button data-v="econ">Avanserte og fremvoksende</button><button data-v="region">Regioner</button><button data-v="regime">Valutaregimer</button>'),
    ('<span class="lbl">Per group</span>\n            <div class="seg" id="c-agg-seg" role="group" aria-label="Per group"><button data-v="combined">Combined</button><button data-v="median">Median country</button>',
     '<span class="lbl">Per gruppe</span>\n            <div class="seg" id="c-agg-seg" role="group" aria-label="Per gruppe"><button data-v="combined">Samlet</button><button data-v="median">Medianlandet</button>'),
    ('`${bn ? "Reserves" : "Reserves as a share of GDP"} by ${G.label.toLowerCase()}, year by year`', '`${bn ? "Reserver" : "Reserver som andel av BNP"} etter ${G.label.toLowerCase()}, år for år`'),
    ('''`${bn ? "Total, US$ billions" : median ? "The median country's % of GDP" : "Combined: the group's total reserves ÷ its total GDP"}, ${goldWords()}, at each year's end. ` +
    (by === "regime" ? "Each country counts in the regime its currency had that year (measured from the two years of exchange rates up to then), so countries move between groups. "
      : "Today's IMF groups for every year. ") +
    "The number of reporting countries grows over time, which makes totals jump; hover for the count."''',
     '''`${bn ? "Totalt, mrd. US$" : median ? "Medianlandets % av BNP" : "Samlet: gruppens samlede reserver ÷ dens samlede BNP"}, ${goldWords()}, ved hvert årsskifte. ` +
    (by === "regime" ? "Hvert land teller i det valutaregimet valutaen hadde det året (målt ut fra de to årene med valutakurser fram til da), så land flytter mellom gruppene. "
      : "Dagens grupper fra IMF for alle år. ") +
    "Antallet land som rapporterer, øker over tid, så totalene hopper; pek for antallet."'''),
    ('state.cMeasure === "bn" ? "Reserves over time" : "Reserves as a share of GDP over time"', 'state.cMeasure === "bn" ? "Reserver over tid" : "Reserver som andel av BNP over tid"'),
    ('`${cUnit()}, ${goldWords()}; quarterly where the country reports quarterly, otherwise at each year\'s end.`', '`${cUnit()}, ${goldWords()}; kvartalsvis der landet rapporterer kvartalsvis, ellers ved hvert årsskifte.`'),
    ('title="Always shown"', 'title="Vises alltid"'),
    ('title="Remove from the chart"', 'title="Fjern fra diagrammet"'),
    ('"Pick a country in the ranking, in the groups or in the list above."', '"Velg et land i rangeringen, i gruppene eller i listen ovenfor."'),
    ('throw new Error("the IMF\'s answer had no figures")', 'throw new Error("IMFs svar hadde ingen tall")'),
    ('name: "Norway", x: hx', 'name: "Norge", x: hx'),
    ('"%{y:,.0f} bn<extra>Norway</extra>" : "%{y:.1f}%<extra>Norway</extra>"', '"%{y:,.0f} mrd.<extra>Norge</extra>" : "%{y:.1f} %<extra>Norge</extra>"'),
    (' · %{customdata} countries<extra>${esc(cat.name)}</extra>`', ' · %{customdata} land<extra>${esc(cat.name)}</extra>`'),
]

# units, wherever they are written in text (not the code's own "bn")
REGEX = [
    (r'\} bn`', '} mrd.`'),
    (r'\} tn`', '} bill.`'),
    (r'" bn"', '" mrd."'),
    (r'" tn"', '" bill."'),
    (r'"\$([0-9.,]+) bn"', r'"$\1 mrd."'),
    (r'\$1,000 bn', '$1 000 mrd.'),
    (r'Q%q', 'K%q'),
]

NAMES = {
    "ABW": "Aruba", "AFG": "Afghanistan", "AGO": "Angola", "AIA": "Anguilla", "ALB": "Albania", "AND": "Andorra",
    "ARE": "De forente arabiske emirater", "ARG": "Argentina", "ARM": "Armenia", "ATG": "Antigua og Barbuda", "AUS": "Australia",
    "AUT": "Østerrike", "AZE": "Aserbajdsjan", "BDI": "Burundi", "BEL": "Belgia", "BEN": "Benin", "BFA": "Burkina Faso",
    "BGD": "Bangladesh", "BGR": "Bulgaria", "BHR": "Bahrain", "BHS": "Bahamas", "BIH": "Bosnia-Hercegovina", "BLR": "Belarus",
    "BLZ": "Belize", "BMU": "Bermuda", "BOL": "Bolivia", "BRA": "Brasil", "BRB": "Barbados", "BRN": "Brunei", "BTN": "Bhutan",
    "BWA": "Botswana", "CAF": "Den sentralafrikanske republikk", "CAN": "Canada", "CHE": "Sveits", "CHL": "Chile", "CHN": "Kina",
    "CIV": "Elfenbenskysten", "CMR": "Kamerun", "COD": "Kongo (Den demokratiske republikk)", "COG": "Kongo", "COL": "Colombia",
    "COM": "Komorene", "CPV": "Kapp Verde", "CRI": "Costa Rica", "CUW": "Curaçao", "CWX": "Curaçao og Sint Maarten",
    "CYM": "Caymanøyene", "CYP": "Kypros", "CZE": "Tsjekkia", "DEU": "Tyskland", "DJI": "Djibouti", "DMA": "Dominica",
    "DNK": "Danmark", "DOM": "Den dominikanske republikk", "DZA": "Algerie", "ECU": "Ecuador", "EGY": "Egypt", "ERI": "Eritrea",
    "ESP": "Spania", "EST": "Estland", "ETH": "Etiopia", "FIN": "Finland", "FJI": "Fiji", "FRA": "Frankrike", "FSM": "Mikronesia",
    "GAB": "Gabon", "GBR": "Storbritannia", "GEO": "Georgia", "GHA": "Ghana", "GIN": "Guinea", "GMB": "Gambia",
    "GNB": "Guinea-Bissau", "GNQ": "Ekvatorial-Guinea", "GRC": "Hellas", "GRD": "Grenada", "GTM": "Guatemala", "GUY": "Guyana",
    "HKG": "Hongkong", "HND": "Honduras", "HRV": "Kroatia", "HTI": "Haiti", "HUN": "Ungarn", "IDN": "Indonesia", "IND": "India",
    "IRL": "Irland", "IRN": "Iran", "IRQ": "Irak", "ISL": "Island", "ISR": "Israel", "ITA": "Italia", "JAM": "Jamaica",
    "JOR": "Jordan", "JPN": "Japan", "KAZ": "Kasakhstan", "KEN": "Kenya", "KGZ": "Kirgisistan", "KHM": "Kambodsja",
    "KIR": "Kiribati", "KNA": "Saint Kitts og Nevis", "KOR": "Sør-Korea", "KOS": "Kosovo", "KWT": "Kuwait", "LAO": "Laos",
    "LBN": "Libanon", "LBR": "Liberia", "LBY": "Libya", "LCA": "Saint Lucia", "LIE": "Liechtenstein", "LKA": "Sri Lanka",
    "LSO": "Lesotho", "LTU": "Litauen", "LUX": "Luxembourg", "LVA": "Latvia", "MAC": "Macao", "MAR": "Marokko", "MDA": "Moldova",
    "MDG": "Madagaskar", "MDV": "Maldivene", "MEX": "Mexico", "MHL": "Marshalløyene", "MKD": "Nord-Makedonia", "MLI": "Mali",
    "MLT": "Malta", "MMR": "Myanmar", "MNE": "Montenegro", "MNG": "Mongolia", "MOZ": "Mosambik", "MRT": "Mauritania",
    "MSR": "Montserrat", "MUS": "Mauritius", "MWI": "Malawi", "MYS": "Malaysia", "NAM": "Namibia", "NER": "Niger", "NGA": "Nigeria",
    "NIC": "Nicaragua", "NLD": "Nederland", "NOR": "Norge", "EZB": "Den europeiske sentralbanken", "NPL": "Nepal", "NRU": "Nauru", "NZL": "New Zealand", "OMN": "Oman",
    "PAK": "Pakistan", "PAN": "Panama", "PER": "Peru", "PHL": "Filippinene", "PLW": "Palau", "PNG": "Papua Ny-Guinea",
    "POL": "Polen", "PRI": "Puerto Rico", "PRT": "Portugal", "PRY": "Paraguay", "QAT": "Qatar", "ROU": "Romania",
    "RUS": "Russland", "RWA": "Rwanda", "SAU": "Saudi-Arabia", "SDN": "Sudan", "SEN": "Senegal", "SGP": "Singapore",
    "SLB": "Salomonøyene", "SLE": "Sierra Leone", "SLV": "El Salvador", "SMR": "San Marino", "SOM": "Somalia", "SRB": "Serbia",
    "SSD": "Sør-Sudan", "STP": "São Tomé og Príncipe", "SUR": "Surinam", "SVK": "Slovakia", "SVN": "Slovenia", "SWE": "Sverige",
    "SWZ": "Eswatini", "SXM": "Sint Maarten", "SYC": "Seychellene", "SYR": "Syria", "TCA": "Turks- og Caicosøyene", "TCD": "Tsjad",
    "TGO": "Togo", "THA": "Thailand", "TJK": "Tadsjikistan", "TKM": "Turkmenistan", "TLS": "Øst-Timor", "TON": "Tonga",
    "TTO": "Trinidad og Tobago", "TUN": "Tunisia", "TUR": "Tyrkia", "TUV": "Tuvalu", "TWN": "Taiwan", "TZA": "Tanzania",
    "UGA": "Uganda", "UKR": "Ukraina", "URY": "Uruguay", "USA": "USA", "UZB": "Usbekistan", "VCT": "Saint Vincent og Grenadinene",
    "VEN": "Venezuela", "VNM": "Vietnam", "VUT": "Vanuatu", "WBG": "Vestbredden og Gaza", "WSM": "Samoa", "YEM": "Jemen",
    "ZAF": "Sør-Afrika", "ZMB": "Zambia", "ZWE": "Zimbabwe",
}


def translate(template: str) -> tuple[str, list]:
    """The Norwegian template, and the English texts that were not found (none, when up to date)."""
    import re
    s, missing = template, []
    for start, end, new in BLOCKS:
        i0 = s.find(start)
        i1 = s.find(end, i0 + len(start)) if i0 >= 0 else -1
        if i0 < 0 or i1 < 0:
            missing.append(start)
            continue
        s = s[:i0 + len(start)] + new + s[i1:]
    for en, no in PAIRS:
        if en not in s:
            missing.append(en)
        s = s.replace(en, no)
    for pat, rep in REGEX:
        s = re.sub(pat, rep, s)
    return s, missing
