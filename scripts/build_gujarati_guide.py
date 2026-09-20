# -*- coding: utf-8 -*-
"""
Script to generate Master_Thesis_Complete_Guide_Gujarati.html
Provides a complete, easy-to-understand, in-depth explanation in Gujarati
with English technical keywords for Ritik Ghoghari's Master Thesis.
"""

html_content = """<!DOCTYPE html>
<html lang="gu">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catching Greenwashing from Space — માસ્ટર થીસીસ સંપૂર્ણ ગાઈડ (ગુજરાતી)</title>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-green: #34d399;
      --accent-orange: #fb923c;
      --accent-rose: #fb7185;
      --accent-violet: #a78bfa;
      --code-bg: #0b1120;
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg: #f8fafc;
        --card-bg: #ffffff;
        --card-border: #e2e8f0;
        --text-main: #0f172a;
        --text-muted: #64748b;
        --accent: #0284c7;
        --accent-green: #059669;
        --accent-orange: #ea580c;
        --accent-rose: #e11d48;
        --accent-violet: #7c3aed;
        --code-bg: #f1f5f9;
      }
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Shruti', 'Gujarati Sangam MN', 'Noto Sans Gujarati', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      line-height: 1.8;
      padding: 40px 20px;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
    }
    header {
      border-bottom: 2px solid var(--card-border);
      padding-bottom: 28px;
      margin-bottom: 36px;
    }
    .badge {
      display: inline-block;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background-color: rgba(56, 189, 248, 0.15);
      color: var(--accent);
      margin-bottom: 14px;
    }
    h1 {
      font-size: 2.3rem;
      font-weight: 800;
      letter-spacing: -0.01em;
      margin-bottom: 12px;
      color: var(--text-main);
    }
    .subtitle {
      font-size: 1.15rem;
      color: var(--text-muted);
      margin-bottom: 20px;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-top: 20px;
      font-size: 0.92rem;
    }
    .meta-item {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      padding: 12px 16px;
      border-radius: 8px;
    }
    .meta-item strong {
      display: block;
      color: var(--text-muted);
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 2px;
    }
    .toc {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 40px;
    }
    .toc h2 {
      font-size: 1.25rem;
      margin-bottom: 14px;
      color: var(--accent);
      border-left: none;
      padding-left: 0;
    }
    .toc ul {
      list-style: none;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 10px;
      margin-left: 0;
    }
    .toc a {
      color: var(--text-main);
      text-decoration: none;
      font-size: 0.95rem;
      transition: color 0.15s;
    }
    .toc a:hover {
      color: var(--accent);
      text-decoration: underline;
    }
    section {
      margin-bottom: 50px;
    }
    h2 {
      font-size: 1.65rem;
      font-weight: 700;
      border-left: 4px solid var(--accent);
      padding-left: 14px;
      margin-bottom: 20px;
      color: var(--text-main);
    }
    h3 {
      font-size: 1.3rem;
      font-weight: 600;
      margin-top: 26px;
      margin-bottom: 12px;
      color: var(--text-main);
    }
    p, li {
      color: var(--text-main);
      font-size: 1.02rem;
    }
    p {
      margin-bottom: 16px;
    }
    ul, ol {
      margin-left: 26px;
      margin-bottom: 18px;
    }
    li {
      margin-bottom: 8px;
    }
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 18px;
      margin: 20px 0;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 22px;
    }
    .card.blue { border-top: 4px solid var(--accent); }
    .card.green { border-top: 4px solid var(--accent-green); }
    .card.orange { border-top: 4px solid var(--accent-orange); }
    .card.rose { border-top: 4px solid var(--accent-rose); }
    .card.violet { border-top: 4px solid var(--accent-violet); }
    .card h4 {
      font-size: 1.15rem;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .formula-box {
      background: var(--code-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 20px;
      margin: 20px 0;
      text-align: center;
      font-size: 1.25rem;
      font-weight: 600;
      color: var(--accent);
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 0.94rem;
      background: var(--card-bg);
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--card-border);
    }
    th, td {
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid var(--card-border);
    }
    th {
      background-color: rgba(255, 255, 255, 0.04);
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      font-size: 0.78rem;
      letter-spacing: 0.06em;
    }
    tr:last-child td {
      border-bottom: none;
    }
    tr:hover td {
      background-color: rgba(56, 189, 248, 0.05);
    }
    td.num {
      text-align: right;
      font-variant-numeric: tabular-nums;
      font-weight: 500;
    }
    th.num {
      text-align: right;
    }
    pre {
      background: var(--code-bg);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 16px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.9rem;
      color: var(--text-main);
      overflow-x: auto;
      margin: 16px 0;
      line-height: 1.6;
    }
    .quote-box {
      border-left: 4px solid var(--accent-green);
      background: rgba(52, 211, 153, 0.08);
      padding: 18px 22px;
      border-radius: 0 8px 8px 0;
      margin: 18px 0;
    }
    .print-btn {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--accent);
      color: #000;
      border: none;
      padding: 12px 22px;
      font-weight: 700;
      border-radius: 9999px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
      font-size: 0.92rem;
      transition: transform 0.15s;
    }
    .print-btn:hover {
      transform: scale(1.05);
    }
    @media print {
      body { background: #fff; color: #000; padding: 0; }
      .print-btn, .toc { display: none; }
      .card, table, pre, .meta-item { border: 1px solid #ccc; background: #fff; color: #000; }
      th { color: #555; background: #eee; }
      .formula-box { background: #f5f5f5; color: #000; border: 1px solid #ccc; }
      h2 { border-left-color: #000; color: #000; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">માસ્ટર થીસીસ સંપૂર્ણ ટેકનિકલ ગાઈડ (ગુજરાતી)</span>
      <h1>અંતરિક્ષમાંથી ગ્રીનવોશિંગ પકડવું (Catching Greenwashing from Space)</h1>
      <div class="subtitle">
        સેટેલાઇટ રિમોટ સેન્સિંગ અને નેચરલ લેંગ્વેજ પ્રોસેસિંગ (NLP) દ્વારા પામ ઓઇલ કંપનીઓના શૂન્ય-વૃક્ષછેદન (Zero-Deforestation) દાવાઓની ચકાસણી
      </div>

      <div class="meta-grid">
        <div class="meta-item">
          <strong>વિદ્યાર્થી (Author)</strong>
          રિતિક ઘોઘારી (Ritik Ghoghari)
        </div>
        <div class="meta-item">
          <strong>ડિગ્રી અને યુનિવર્સિટી</strong>
          M.Sc. Data Science, AI &amp; Digital Business &bull; GISMA University, બર્લિન
        </div>
        <div class="meta-item">
          <strong>પ્રોફેસર / સુપરવાઇઝર</strong>
          પ્રોફેસર મોહમ્મદ હોસૈની (Prof. Mohamad Hoseini)
        </div>
        <div class="meta-item">
          <strong>થીસીસ સબમિશન તારીખ</strong>
          26 સપ્ટેમ્બર 2026
        </div>
        <div class="meta-item">
          <strong>પ્રોજેક્ટ સ્ટેટસ</strong>
          100% પૂર્ણ (23 માંથી 23 યુનિટ ટેસ્ટ પાસ)
        </div>
      </div>
    </header>

    <nav class="toc">
      <h2>અનુક્રમણિકા (Table of Contents)</h2>
      <ul>
        <li><a href="#prologue">1. મોટી તસવીર: શા માટે આ થીસીસ બનાવવામાં આવ્યો?</a></li>
        <li><a href="#first-principles">2. પાયાના ખ્યાલો અને ઇન્ડસ્ટ્રીની મૂળભૂત બાબતો</a></li>
        <li><a href="#post-2020-detail">3. ઊંડાણપૂર્વક સમજૂતી: "Post-2020" એટલે શું?</a></li>
        <li><a href="#remote-sensing">4. રિમોટ સેન્સિંગ અને સેટેલાઇટ વિજ્ઞાન</a></li>
        <li><a href="#nlp-science">5. નેચરલ લેંગ્વેજ પ્રોસેસિંગ (NLP) અને AI મોડેલ્સ</a></li>
        <li><a href="#chronology">6. પ્રોજેક્ટની ક્રમિક પ્રક્રિયા (8 તબક્કા)</a></li>
        <li><a href="#math">7. ગણિત અને સ્કોરિંગ ફોર્મ્યુલા</a></li>
        <li><a href="#findings">8. મુખ્ય પરિણામો અને 11 કંપનીઓની કેસ સ્ટડીઝ</a></li>
        <li><a href="#validations">9. સ્વતંત્ર ક્રોસ-વેલિડેશન (4 ચકાસણીઓ)</a></li>
        <li><a href="#engineering">10. ડેટા એન્જિનિયરિંગની 108 કલાકની લડાઈઓ</a></li>
        <li><a href="#summary-card">11. ઝડપી રિવિઝન રેફરન્સ કાર્ડ</a></li>
      </ul>
    </nav>

    <!-- SECTION 1 -->
    <section id="prologue">
      <h2>1. મોટી તસવીર: શા માટે આ થીસીસ બનાવવામાં આવ્યો?</h2>
      <p>
        છેલ્લા 10 વર્ષોમાં સમગ્ર વિશ્વમાં પર્યાવરણ અંગે જાગૃતિ વધી છે. દુનિયાની મોટી મોટી બ્રાન્ડ્સ અને પામ ઓઇલ બનાવતી જાયન્ટ કંપનીઓ પર જંગલો ન કાપવા માટે ભારે દબાણ આવ્યું. તેના જવાબમાં લગભગ બધી જ મોટી કંપનીઓએ પોતાના સત્તાવાર સસ્ટેનેબિલિટી રિપોર્ટ્સમાં મોટા મોટા દાવા કર્યા કે: <strong>"અમે શૂન્ય વનનાબૂદી (Zero Deforestation), નો પીટ (No Peat), નો એક્સપ્લોઇટેશન (NDPE) પોલિસીનું 100% પાલન કરીએ છીએ."</strong>
      </p>
      <p>
        પરંતુ અત્યાર સુધી કંપનીઓની આ વાતો સાચી છે કે ખોટી તે તપાસવામાં એક <strong>મોટી ખામી (Verification Gap)</strong> હતી:
      </p>
      <ul>
        <li>
          <strong>ફક્ત લખાણ તપાસવું (Text-Only Auditing):</strong> અત્યાર સુધી AI અને NLP ટૂલ્સ ફક્ત કંપનીના PDF રિપોર્ટ્સ વાંચી શકતા હતા. તેઓ કહી શકતા કે કંપનીએ સારી ભાષા વાપરી છે કે નહીં. પરંતુ લખાણ વાંચનારા મોડેલ્સ જમીન પર જોઈ શકતા નથી. કંપની AC ઓફિસમાં બેસીને "અમે 100% ગ્રીન છીએ" તેવું લખે, પણ હજારો કિલોમીટર દૂર જંગલમાં બુલડોઝર ચાલતા હોય તો ટેક્સ્ટ મોડેલને ખબર પડતી નથી.
        </li>
        <li>
          <strong>ફક્ત સેટેલાઇટ ફોટા જોવા (Satellite-Only Auditing):</strong> ગ્લોબલ ફોરેસ્ટ વોચ કે પામવોચ જેવા સેટેલાઇટ પ્લેટફોર્મ્સ અંતરિક્ષમાંથી જંગલો કપાતા જોઈ શકે છે. પરંતુ સેટેલાઇટ ટૂલ્સ એ નથી જાણતા કે કંપનીના ડાયરેક્ટરે રિપોર્ટમાં શું વચન આપ્યું હતું. તેઓ જંગલ કપાવાની નોંધ રાખે છે પણ કંપનીના જૂઠાણા કે સત્યતાને માપતા નથી.
        </li>
      </ul>
      <div class="quote-box">
        <strong>તમારા થીસીસનું મુખ્ય યોગદાન (Core Thesis Contribution):</strong><br>
        તમે આ બંને સ્વતંત્ર ટેકનોલોજીને એક સાથે જોડી દીધી છે! એક બાજુ NLP મોડેલ કંપનીના PDF રિપોર્ટમાંથી કરેલા ચોક્કસ વાયદા તપાસે છે, અને બીજી બાજુ ગુગલ અર્થ એન્જિન (GEE) અને સેટેલાઇટ કંપનીની મિલોની આજુબાજુનું સાચું જંગલ કટિંગ માપે છે. બંનેને સરખાવીને તમારો કોડ એક નવો વૈજ્ઞાનિક સ્કોર બનાવે છે: <strong>મિસમેચ સ્કોર (Mismatch Score: 0 થી 100)</strong>. જો સ્કોર ઊંચો આવે તો સાબિત થાય છે કે કંપની ગ્રીનવોશિંગ (Greenwashing) કરી રહી છે!
      </div>
    </section>

    <!-- SECTION 2 -->
    <section id="first-principles">
      <h2>2. પાયાના ખ્યાલો અને ઇન્ડસ્ટ્રીની મૂળભૂત બાબતો</h2>
      <p>આ થીસીસ ડેટા સાયન્સ અને ખેતીવાડી/ઉદ્યોગ બંનેનું મિશ્રણ છે. તેથી નીચેના શબ્દો સમજવા સૌથી વધુ જરૂરી છે:</p>

      <div class="card-grid">
        <div class="card blue">
          <h4>🌴 પામ ઓઇલ (Palm Oil - *Elaeis guineensis*)</h4>
          <p>
            તેલ આપતા તાડના ઝાડના ફળમાંથી નીકળતું વનસ્પતિ તેલ છે. દુનિયામાં એક હેક્ટર દીઠ સૌથી વધુ તેલ આપતો આ પાક છે. સુપરમાર્કેટમાં મળતી 50% પ્રોડક્ટ્સમાં પામ ઓઇલ હોય છે (જેમ કે ચોકલેટ, બિસ્કિટ, સાબુ, શેમ્પૂ, લિપસ્ટિક અને બાયોફ્યુઅલ). દુનિયાનું 85% પામ ઓઇલ ફક્ત બે જ દેશો બનાવે છે: ઇન્ડોનેશિયા અને મલેશિયા. આ પાક વાવવા માટે ઐતિહાસિક રીતે બોર્નિયો અને સુમાત્રાના લાખો હેક્ટર રેઈનફોરેસ્ટ કાપી નાખવામાં આવ્યા છે.
          </p>
        </div>

        <div class="card orange">
          <h4>🏭 પામ ઓઇલ મિલ (The Palm Oil Mill &amp; 24-Hour Rule)</h4>
          <p>
            મિલ એટલે પ્લાન્ટેશન (બગીચા) ની બિલકુલ નજીક આવેલી ફેક્ટરી જ્યાં ફળોને કચરીને તેલ કાઢવામાં આવે છે. ઝાડ પરથી જે ફળો ઉતારવામાં આવે તેને <strong>Fresh Fruit Bunches (FFB)</strong> કહેવાય છે. <br><br>
            <strong>24 થી 48 કલાકનો તાજગીનો કડક નિયમ:</strong> ફળ ઝાડ પરથી કપાય કે તરત જ તેમાં એન્ઝાઇમેટિક એસિડ બનવા લાગે છે. જો <strong>24 થી 48 કલાકમાં</strong> ફળ મિલમાં પીલાય નહીં, તો તેલ ખરાબ થઈ જાય છે (Free Fatty Acids વધી જાય છે) અને વેચવા લાયક રહેતું નથી. તેથી ખેડૂતો કે ટ્રકો ફળોને દૂરના શહેરોમાં લઈ જઈ શકતા નથી. ફળ હંમેશા નજીકની જ મિલમાં જવું પડે છે. તેથી મિલ એ જમીન પરનો સ્થાયી કેન્દ્રબિંદુ (Anchor Point) છે.
          </p>
        </div>

        <div class="card green">
          <h4>📐 હેક્ટર એટલે શું? (What is a Hectare / ha?)</h4>
          <p>
            જમીન માપવાનો આંતરરાષ્ટ્રીય મેટ્રિક એકમ છે (1 હેક્ટર = 10,000 ચોરસ મીટર, એટલે કે 100 મીટર લાંબો અને 100 મીટર પહોળો ચોરસ ટુકડો). <br><br>
            <strong>સરળ સરખામણી:</strong> 1 હેક્ટર એટલે આશરે <strong>1.4 સ્ટાન્ડર્ડ ફૂટબોલ મેદાન</strong>. <br>
            તમારા થીસીસમાં 290 મિલોની આસપાસ કુલ <strong>890,168 હેક્ટર</strong> જંગલ 2020 પછી કપાયેલું પકડાયું છે. આ વિસ્તાર બર્લિન શહેર કરતાં 10 ગણો મોટો છે, અથવા સાયપ્રસ દેશ જેટલો મોટો વિસ્તાર છે!
          </p>
        </div>

        <div class="card violet">
          <h4>⭕ 10 કિલોમીટરનો બફર અને કેચમેન્ટ (10 km Buffer)</h4>
          <p>
            દરેક મિલના જીપીએસ પોઇન્ટની આસપાસ તમારો પાયથોન કોડ <strong>10 કિમી ત્રિજ્યા (Radius) નું ગોળ વર્તુળ</strong> દોરે છે (જે 314 ચોરસ કિમી, અથવા 31,400 હેક્ટર વિસ્તાર આવરી લે છે). જંગલના કાચા રસ્તાઓ પર ટ્રક 24 કલાકમાં આશરે 10 થી 20 કિમી જ મુસાફરી કરી શકે છે. <br><br>
            આ 10 કિમીનો નિયમ આંતરરાષ્ટ્રીય <strong>PalmWatch</strong> પદ્ધતિ મુજબનો છે. તે મિલની નજીક થયેલી વનનાબૂદી દર્શાવે છે (Spatial Proximity).
          </p>
        </div>

        <div class="card blue">
          <h4>🌲 ટ્રી કવર લોસ vs ખરી વનનાબૂદી (Tree Cover Loss vs Deforestation)</h4>
          <p>
            <strong>Hansen Global Forest Change:</strong> આ સેટેલાઇટ ડેટા 30-મીટરના પિક્સેલ પર ફક્ત એ જુએ છે કે ઝાડનું છત્ર (Canopy) કપાયું કે નહીં. તેને <em>Tree Cover Loss</em> કહેવાય. તે એ નથી બતાવતું કે ઝાડ પામ ઓઇલ માટે કપાયું, લાકડા માટે કે આગ લાગી. <br><br>
            ખરી <em>Deforestation</em> એટલે જંગલ કાયમ માટે સાફ કરીને બીજી જમીન બનાવી દેવી. આ શંકા દૂર કરવા માટે તમારા થીસીસમાં <strong>Descals et al. (2021)</strong> નો AI મેપ ઉમેરવામાં આવ્યો, જેણે સાબિત કર્યું કે કપાયેલી જમીનમાંથી 56% જમીન પામ ઓઇલ પ્લાન્ટેશન બની ગઈ છે!
          </p>
        </div>

        <div class="card rose">
          <h4>⚖️ ગ્રીનવોશિંગ વિરુદ્ધ સસ્તી વાતો (Greenwashing vs Cheap Talk)</h4>
          <p>
            <strong>ગ્રીનવોશિંગ (Greenwashing):</strong> પર્યાવરણનું સાચું રક્ષણ કરવાને બદલે પબ્લિક રિલેશન્સ અને માર્કેટિંગમાં મોટી-મોટી ડંફાસો મારવી. પામ ઓઇલમાં તેનો અર્થ એ છે કે કંપની રિપોર્ટમાં લખે કે "અમે 100% વૃક્ષો બચાવીએ છીએ", પરંતુ તેની મિલો આસપાસ જંગલો કપાતા હોય.<br><br>
            <strong>સસ્તી વાતો (Cheap Talk):</strong> એવા સુંદર વાક્યો જેનો કોઈ પુરાવો ન માંગી શકાય, બોલવાનો કોઈ ખર્ચ ન થાય અને જેને ખોટા પણ સાબિત ન કરી શકાય (જેમ કે: "અમે કુદરતને ખૂબ પ્રેમ કરીએ છીએ").
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION 3 -->
    <section id="post-2020-detail">
      <h2>3. ઊંડાણપૂર્વક સમજૂતી: "Post-2020" એટલે શું?</h2>
      <p>થીસીસમાં વારંવાર આવતા શબ્દ <strong>Post-2020</strong> નો ચોક્કસ અર્થ નીચે મુજબ છે:</p>

      <div class="card-grid">
        <div class="card blue">
          <h4>1. શાબ્દિક અર્થ અને સમયગાળો (Literal Meaning)</h4>
          <p>
            <strong>"Post-2020" એટલે 31 ડિસેમ્બર 2020 પછી થયેલું કોઈપણ જંગલ કટિંગ.</strong><br><br>
            તમારા ડેટાસેટમાં આમાં કેલેન્ડર વર્ષ <strong>2021, 2022, 2023, 2024 અને 2025</strong> નો સમાવેશ થાય છે.<br><br>
            તમે તપાસેલી તમામ 290 મિલોમાં આ સમયગાળા દરમિયાન કુલ <strong>890,168 હેક્ટર</strong> જંગલ કપાયું છે. અભ્યાસની દરેક એક મિલ (290 માંથી 290) પર 2020 પછી જંગલ કપાવાના પુરાવા મળ્યા છે.
          </p>
        </div>

        <div class="card green">
          <h4>2. કાયદાકીય પાયો: યુરોપનો EUDR કાયદો</h4>
          <p>
            આ 31 ડિસેમ્બર 2020 ની તારીખ કોઈ અંદાજે પસંદ કરેલી તારીખ નથી. તે યુરોપિયન યુનિયનના સત્તાવાર કાયદા <strong>EUDR (Regulation EU 2023/1115)</strong> ની કાયદેસરની કટઓફ તારીખ છે.<br><br>
            આ કાયદા મુજબ યુરોપમાં પામ ઓઇલ, સોયા, બીફ, કોકો, કોફી કે રબર ત્યારે જ વેચી શકાય જો તે સાબિત થાય કે તે 31 ડિસેમ્બર 2020 પછી કાપેલા જંગલની જમીન પર નથી ઉગાડાયું:<br>
            <em>"31 ડિસેમ્બર 2020 પછી કપાયેલી જમીન પરથી આવેલો કોઈપણ માલ યુરોપિયન યુનિયનમાં વેચવો ગેરકાયદેસર છે."</em><br><br>
            તેથી તમારા થીસીસનું મૂલ્યાંકન કંપનીઓ પર લાગુ પડતા સાચા આંતરરાષ્ટ્રીય કાયદા પર આધારિત છે.
          </p>
        </div>

        <div class="card orange">
          <h4>3. જૂની વનનાબૂદી vs 2020 પછીની ચાલુ વનનાબૂદી</h4>
          <p>
            ગ્રીનવોશિંગ સાબિત કરવા માટે આ ભેદ સમજવો સૌથી મહત્વનો છે:<br><br>
            • <strong>જૂની વનનાબૂદી (2021 પહેલા):</strong> જો કોઈ કંપનીએ 2005 કે 2012 માં જંગલ કાપ્યું હોય, તો કંપનીના માલિકો બહાનું કાઢી શકે કે: <em>"એ તો વર્ષો પહેલા બન્યું હતું, ત્યારે અમારી પાસે સસ્ટેનેબિલિટી પોલિસી નહોતી."</em><br><br>
            • <strong>2020 પછીની ચાલુ વનનાબૂદી (2021 થી 2025):</strong> 2020 સુધીમાં તો આ બધી જ 11 કંપનીઓએ સત્તાવાર નો-ડિફોરેસ્ટેશન (NDPE) પોલિસી જાહેર કરી દીધી હતી! જો 2022 કે 2024 માં તેમની મિલ પાસે જંગલ કપાય, તો તેઓ કોઈ બહાનું કાઢી શકતા નથી. એક તરફ તેઓ જાહેરાત કરે કે અમે 100% ગ્રીન છીએ અને બીજી તરફ જંગલો કપાય છે. આ જ ગ્રીનવોશિંગ છે.
          </p>
        </div>

        <div class="card violet">
          <h4>4. પાયથોન કોડમાં "Post-2020" નું ફિલ્ટર</h4>
          <p>
            Hansen સેટેલાઇટ ડેટામાં દરેક પિક્સેલને વર્ષ મુજબ એક નંબર (ઇન્ટીજર કોડ) આપવામાં આવે છે જેને <code>lossyear</code> કહેવાય છે:<br>
            • <code>lossyear = 0</code> : કોઈ જંગલ કપાયું નથી<br>
            • <code>lossyear = 1</code> : 2001 માં જંગલ કપાયું<br>
            • <code>lossyear = 20</code> : 2020 માં જંગલ કપાયું (કટઓફ પહેલા)<br>
            • <code>lossyear = 21</code> : 2021 માં જંગલ કપાયું (કટઓફ પછી - Post-2020)<br>
            • <code>lossyear = 25</code> : 2025 માં જંગલ કપાયું (Post-2020)<br><br>
            તમારા કોડ (<code>scripts/all_companies_yearly_loss.py</code>) માં તમે સ્પષ્ટ ફિલ્ટર લગાવ્યું છે:
          </p>
          <pre># 2021 કે ત્યાર પછીના વર્ષોનું જંગલ કટિંગ ફિલ્ટર કરવું (lossyear >= 21)
post2020_loss = lossyear.gte(21)</pre>
        </div>
      </div>
    </section>

    <!-- SECTION 4 -->
    <section id="remote-sensing">
      <h2>4. રિમોટ સેન્સિંગ અને સેટેલાઇટ વિજ્ઞાન</h2>
      <p>
        રિમોટ સેન્સિંગ (Remote Sensing) એટલે જમીન પર ગયા વગર આકાશમાંથી વિમાન કે સેટેલાઇટ કેમેરા દ્વારા પૃથ્વીની સપાટીનું અવલોકન અને માપણી કરવી.
      </p>

      <h3>અર્થ ઓબ્ઝર્વેશન સેટેલાઇટ એટલે શું? (Earth Observation Satellite)</h3>
      <p>
        તે પૃથ્વીથી 500 થી 800 કિલોમીટર ઊંચાઈએ અંતરિક્ષમાં સતત ફરતું માનવરહિત સ્પેસક્રાફ્ટ છે. પૃથ્વી નીચે ફરતી જાય અને સેટેલાઇટના સેન્સર લાઈન-બાય-લાઈન ફોટો પાડતા જાય. સેટેલાઇટ દર થોડા દિવસે બરાબર તે જ જગ્યા પર પાછો આવે છે. આથી ગાઢ અને દુર્ગમ જંગલોમાં માણસોને જોખમમાં મૂક્યા વગર આખા દાયકાનો ઇતિહાસ અને ફેરફારો અંતરિક્ષમાંથી જોઈ શકાય છે.
      </p>

      <h3>સેટેલાઇટના 4 મુખ્ય ટેકનિકલ ખ્યાલો:</h3>
      <div class="card-grid">
        <div class="card blue">
          <h4>1. પિક્સેલ રિઝોલ્યુશન: 30-મીટર vs 10-મીટર</h4>
          <p>
            સેટેલાઇટ ઇમેજ નાના ચોરસ પિક્સેલ્સની બનેલી હોય છે:<br><br>
            • <strong>30-મીટર રિઝોલ્યુશન (Landsat):</strong> સ્ક્રીન પરનો એક પિક્સેલ જમીન પર 30 મીટર લાંબો અને 30 મીટર પહોળો વિસ્તાર (900 ચોરસ મીટર, અથવા 0.09 હેક્ટર) દર્શાવે છે. જો જંગલમાં એક નાનું ઝાડ કપાય તો Landsat ને ખબર નહીં પડે. પણ જો ફૂટબોલ ગ્રાઉન્ડ જેટલો મોટો ટુકડો સાફ થાય તો પિક્સેલનો રંગ તરત લીલામાંથી બદલાઈ જાય છે.<br><br>
            • <strong>10-મીટર રિઝોલ્યુશન (Sentinel-2):</strong> એક પિક્સેલ 10 મીટર બાય 10 મીટર (100 ચોરસ મીટર) દર્શાવે છે. તે 9 ગણી વધુ ડિટેલ આપે છે, જેથી રસ્તાઓ, કેનાલો અને નાના કટિંગ સ્પષ્ટ દેખાય છે.
          </p>
        </div>

        <div class="card green">
          <h4>2. મલ્ટિ-સ્પેક્ટ્રલ બેન્ડ્સ અને ક્લોરોફિલ રિફ્લેક્શન</h4>
          <p>
            માણસની આંખ ફક્ત ત્રણ રંગો (લાલ, લીલો, વાદળી - RGB) જોઈ શકે છે. સેટેલાઇટ કેમેરા અદ્રશ્ય પ્રકાશ પણ જુએ છે:<br><br>
            • <strong>નિયર ઇન્ફ્રારેડ (NIR, ~842 nm):</strong> જીવંત લીલા પાંદડાઓમાં રહેલા કોષો (Mesophyll) અરીસાની જેમ ઇન્ફ્રારેડ કિરણોને ઉછાળે છે. સેટેલાઇટના NIR કેમેરામાં તંદુરસ્ત જંગલ સખત ચમકે છે. જ્યારે ઝાડ કપાય કે બળી જાય ત્યારે NIR રિફ્લેક્શન તરત શૂન્ય થઈ જાય છે.<br><br>
            • <strong>શોર્ટવેવ ઇન્ફ્રારેડ (SWIR, 1610 nm &amp; 2190 nm):</strong> તે પાંદડામાં રહેલા પાણી અને ભેજ પ્રત્યે સંવેદનશીલ છે. લીલું જંગલ SWIR ને શોષી લે છે; ખુલ્લી સૂકી જમીન SWIR ને ખૂબ રિફ્લેક્ટ કરે છે. NIR અને SWIR ની સરખામણીથી કમ્પ્યુટર આપોઆપ વનનાબૂદી પકડી પાડે છે.
          </p>
        </div>

        <div class="card orange">
          <h4>3. વાદળો દૂર કરવાની રીત (Cloud Masking &amp; Median Composites)</h4>
          <p>
            ઇન્ડોનેશિયા અને મલેશિયા વિષુવવૃત્ત (Equator) પર આવેલા હોવાથી ત્યાં દરરોજ આકાશમાં ભારે વાદળો અને ધુમ્મસ હોય છે. સાદા કેમેરા વાદળોની આરપાર જોઈ શકતા નથી.<br><br>
            <strong>ટેકનિકલ ઉપાય:</strong> એક દિવસના ફોટા પર નિર્ભર રહેવાને બદલે ગુગલ અર્થ એન્જિન આખા વર્ષના બધા ફોટા ભેગા કરે છે (દા.ત. 2024 માં લીધેલા 30 ફોટા). તેમાંથી વાદળાં અને પડછાયા વાળા પિક્સેલ કાઢી નાખે છે અને બાકી બચેલા સ્વચ્છ પિક્સેલ્સનો <strong>મીડિયન (સરેરાશ)</strong> કાઢે છે. આનાથી એકદમ ચોખ્ખો, વાદળ વગરનો ફોટો તૈયાર થાય છે.
          </p>
        </div>

        <div class="card violet">
          <h4>4. સેન્ટિનેલ-1 સિન્થેટિક અપર્ચર રડાર (Sentinel-1 SAR)</h4>
          <p>
            ઓપ્ટિકલ સેટેલાઇટ સૂર્યપ્રકાશ પર આધાર રાખે છે, જ્યારે રડાર સેટેલાઇટ પોતે માઇક્રોવેવ કિરણો (C-band, 5.6 સેમી તરંગલંબાઈ) જમીન તરફ ફેંકે છે અને પાછા આવતા સિગ્નલને માપે છે.<br><br>
            માઇક્રોવેવ્સ વાદળો, વરસાદ અને ધુમાડાની આરપાર સીધા નીકળી જાય છે! ઝાડ કપાઈ જાય એટલે રડારનું સિગ્નલ બદલાઈ જાય છે. આ ટેકનોલોજીથી <strong>Wageningen RADD alerts</strong> બને છે.
          </p>
        </div>
      </div>

      <h3>થીસીસમાં વપરાયેલા 3 મુખ્ય સેટેલાઇટ્સનું ટેબલ:</h3>
      <table>
        <thead>
          <tr>
            <th>સેટેલાઇટનું નામ</th>
            <th>ચલાવતી એજન્સી / દેશ</th>
            <th>સેન્સર અને રિઝોલ્યુશન</th>
            <th>તમારા થીસીસમાં મુખ્ય ભૂમિકા</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Landsat 7 / 8 / 9</strong></td>
            <td>NASA અને USGS (અમેરિકા)</td>
            <td>ઓપ્ટિકલ મલ્ટિ-સ્પેક્ટ્રલ &bull; 30-મીટર રિઝોલ્યુશન</td>
            <td>મુખ્ય પુરાવો: Hansen Global Forest Change ડેટા આના પરથી બને છે. બધી 290 મિલોમાં થયેલું 890,168 હેક્ટર નુકસાન આ સેટેલાઇટથી માપવામાં આવ્યું છે.</td>
          </tr>
          <tr>
            <td><strong>Sentinel-2 (A &amp; B)</strong></td>
            <td>યુરોપિયન સ્પેસ એજન્સી (ESA)</td>
            <td>ઓપ્ટિકલ મલ્ટિ-સ્પેક્ટ્રલ &bull; 10-મીટર રિઝોલ્યુશન</td>
            <td>હાઇ-રિઝોલ્યુશન ચકાસણી અને AI: 290 મિલોના 300 DPI વાળા હાઇ-ક્વોલિટી ક્લિયરિંગ મેપ્સ બનાવવા અને IBM/NASA Prithvi ફાઉન્ડેશન મોડેલ માટે વપરાયું.</td>
          </tr>
          <tr>
            <td><strong>Sentinel-1 (A &amp; B)</strong></td>
            <td>યુરોપિયન સ્પેસ એજન્સી (ESA)</td>
            <td>સિન્થેટિક અપર્ચર રડાર (SAR) &bull; C-band માઇક્રોવેવ્સ</td>
            <td>વાદળ-મુક્ત રડાર ક્રોસ-વેલિડેશન: વાદળો અને વરસાદ વચ્ચેથી જમીન પરની ખલેલ (RADD એલર્ટ્સ) પકડીને ટોચની 5 માંથી 4 મિલોમાં વનનાબૂદી સાબિત કરી.</td>
          </tr>
        </tbody>
      </table>

      <h3>ગુગલ અર્થ એન્જિન (Google Earth Engine - GEE) ક્લાઉડ પ્લેટફોર્મ</h3>
      <p>
        ગુગલ અર્થ એન્જિન એક વિશાળ પ્લેનેટરી-સ્કેલ સુપર-કમ્પ્યુટિંગ ક્લાઉડ છે. આપણા લેપટોપમાં ટેરાબાઇટ્સ જેટલા ભારે સેટેલાઇટ ફોટા ડાઉનલોડ કરવાને બદલે આપણો પાયથોન કોડ સીધો ગુગલના ક્લાઉડ સર્વર પર રન થાય છે:
      </p>
      <ul>
        <li><code>ee.Image("UMD/hansen/global_forest_change_2025_v1_13")</code>: 2000 થી 2025 સુધીનો વિશ્વભરનો જંગલ કટિંગ ડેટા લોડ કરે છે.</li>
        <li><code>ee.Geometry.Point([lon, lat]).buffer(10000)</code>: દરેક મિલના જીપીએસ પોઇન્ટ પર 10,000 મીટર (10 કિમી) નું ગોળ વર્તુળ બનાવે છે.</li>
        <li><code>reduceRegion(ee.Reducer.sum(), region, scale=30)</code>: વર્તુળમાં રહેલા તમામ 30-મીટર લોસ પિક્સેલ્સનો ચોક્કસ સરવાળો ગણે છે.</li>
        <li><code>maxPixels = 1e10</code>: 290 મિલોના 91,000 ચોરસ કિમી વિસ્તારમાં મેમરી ક્રેશ ન થાય તે માટે ગુગલની મેમરી લિમિટ વધારીને 10 અબજ પિક્સેલ (10<sup>10</sup> pixels) સેટ કરી.</li>
      </ul>

      <h3>સેટેલાઇટ કેવી રીતે ગ્રીનવોશિંગ પકડે છે - 5 સરળ પગલાં:</h3>
      <ol>
        <li>કંપની પોતાનો વાર્ષિક સસ્ટેનેબિલિટી રિપોર્ટ બહાર પાડીને દાવો કરે છે કે અમે 100% જંગલોનું રક્ષણ કરીએ છીએ.</li>
        <li>તમારો પાયથોન કોડ Universal Mill List માંથી તે કંપનીની તમામ મિલોના સાચા GPS કોઓર્ડિનેટ્સ શોધી કાઢે છે.</li>
        <li>ગુગલ અર્થ એન્જિન દરેક મિલની આસપાસ 10 કિમીનું વર્તુળ દોરે છે અને 2021 થી 2025 સુધીના સેટેલાઇટ ફોટા તપાસે છે.</li>
        <li>સેટેલાઇટ નિષ્પક્ષ પુરાવો આપે છે કે તે મિલોની આસપાસ ખરેખર કેટલા હેક્ટર જંગલ કાપી નાખવામાં આવ્યું.</li>
        <li>તમારું સ્કોરિંગ એન્જિન કંપનીના બોલેલા શબ્દો અને સેટેલાઇટના સાચા નુકસાનની સરખામણી કરીને 0 થી 100 નો મિસમેચ સ્કોર ફાળવે છે.</li>
      </ol>
    </section>

    <!-- SECTION 5 -->
    <section id="nlp-science">
      <h2>5. નેચરલ લેંગ્વેજ પ્રોસેસિંગ (NLP) અને AI મોડેલ્સ</h2>
      <p>
        નેચરલ લેંગ્વેજ પ્રોસેસિંગ (NLP) એ આર્ટિફિશિયલ ઇન્ટેલિજન્સ (AI) ની શાખા છે જે કમ્પ્યુટરને માણસ દ્વારા લખાયેલી ભાષા સમજવાની, તેનું વિશ્લેષણ કરવાની અને તેમાંથી મહત્વના તારણો કાઢવાની શક્તિ આપે છે.
      </p>

      <h3>સાદા કીવર્ડથી ટ્રાન્સફોર્મર (BERT) સુધી:</h3>
      <p>
        જૂની પદ્ધતિમાં ફક્ત કીવર્ડ સર્ચ થતું હતું (દા.ત. રિપોર્ટમાં "deforestation" શબ્દ છે કે નહીં). પરંતુ કીવર્ડ સર્ચથી ઘણી ભૂલો થતી હતી કારણ કે અનુક્રમણિકા કે હેડિંગમાં પણ તે શબ્દ આવી જતો હતો.
      </p>
      <p>
        તમારા થીસીસમાં અત્યાધુનિક <strong>Transformers</strong> અને <strong>BERT</strong> મોડેલ્સ વાપરવામાં આવ્યા છે. BERT આખા વાક્યના સંદર્ભ (Context) ને આગળ અને પાછળ બંને બાજુથી સમજે છે.
      </p>

      <h3>થીસીસમાં વપરાયેલા 4 NLP AI મોડેલ્સ:</h3>
      <div class="card-grid">
        <div class="card blue">
          <h4>1. ક્લેઇમ ડિટેક્શન: <code>climatebert/environmental-claims</code></h4>
          <p>
            કંપનીના હજારો વાક્યોમાંથી કયું વાક્ય સાચો પર્યાવરણીય દાવો (Environmental Claim) છે અને કયું વાક્ય સામાન્ય વાત છે તે ઓળખે છે. તમારા 150 વાક્યોના ગોલ્ડ ડેટાસેટ પર આ મોડેલે <strong>97.3% એક્યુરેસી અને 0.981 F1 સ્કોર</strong> પ્રાપ્ત કર્યો!
          </p>
        </div>

        <div class="card green">
          <h4>2. સ્પેસિફિસિટી સ્કોરિંગ: <code>climatebert/distilroberta-base-climate-specificity</code></h4>
          <p>
            વાક્ય કેટલું ચોક્કસ (Specific) છે તેને 0.0 થી 1.0 વચ્ચે સ્કોર આપે છે. જે વાક્યમાં તારીખ, ટકાવારી, ટાર્ગેટ કે જીપીએસ લોકેશન હોય તેને ઊંચો સ્કોર મળે છે. જે વાક્યમાં ફક્ત હવાઈ વાતો ("અમે પર્યાવરણને પ્રેમ કરીએ છીએ") હોય તેને 0 સ્કોર મળે છે.
          </p>
        </div>

        <div class="card orange">
          <h4>3. સેન્ટિમેન્ટ એનાલિસિસ: <code>ProsusAI/finbert</code></h4>
          <p>
            ફાઇનાન્સિયલ ડોમેનનું ટ્રાન્સફોર્મર મોડેલ છે જે કંપનીના લખાણનો ટોન માપે છે. કંપની રિપોર્ટમાં કેટલી ઉત્સાહી, આત્મવિશ્વાસુ કે પ્રોમોશનલ વાતો કરે છે તે પકડે છે. વધારે પડતો પોઝિટિવ સેન્ટિમેન્ટ જ્યારે જંગલ કટિંગ સાથે મળે છે ત્યારે ગ્રીનવોશિંગ સાબિત થાય છે.
          </p>
        </div>

        <div class="card violet">
          <h4>4. ESG કેટેગરી ક્લાસિફાયર: <code>nbroad/ESG-BERT</code></h4>
          <p>
            દરેક પકડાયેલા દાવાને SASB સસ્ટેનેબિલિટી કેટેગરીમાં વહેંચે છે: ગ્રીનહાઉસ ગેસ ઉત્સર્જન (GHG Emissions), ઇકોલોજીકલ ઇમ્પેક્ટ, એનર્જી મેનેજમેન્ટ કે સપ્લાય ચેઇન.
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION 6 -->
    <section id="chronology">
      <h2>6. પ્રોજેક્ટની ક્રમિક પ્રક્રિયા (8 તબક્કા)</h2>
      <p>તમારો થીસીસ કાચા ડેટાથી અંતિમ પરિણામ સુધી નીચેના 8 તબક્કામાં તૈયાર થયો છે:</p>

      <div class="card-grid">
        <div class="card blue">
          <h4>તબક્કો 1: PDF રિપોર્ટ્સનું કલેક્શન</h4>
          <p>11 મોટી કંપનીઓના તાજેતરના સસ્ટેનેબિલિટી અને એન્યુઅલ PDF રિપોર્ટ્સ ડાઉનલોડ કર્યા. લખાણ બહાર કાઢ્યું અને નોન-બ્રેકિંગ સ્પેસ (<code>\u00a0</code>) ની એન્કોડિંગ ખામીઓ સાફ કરી.</p>
        </div>

        <div class="card green">
          <h4>તબક્કો 2: મિલ રજિસ્ટ્રીની ભૂલો સુધારવી</h4>
          <p>Universal Mill List માંથી 290 મિલો મેળવી. દરિયામાં ફેંકાઈ ગયેલા બગડેલા જીપીએસ પોઇન્ટ્સ સુધાર્યા. SD Guthrie ની મિલો 2 થી વધારીને 42 કરી.</p>
        </div>

        <div class="card orange">
          <h4>તબક્કો 3: NLP મોડેલિંગ અને ગોલ્ડ બેન્ચમાર્ક</h4>
          <p>403 સંભવિત વાક્યોમાંથી 55 ગ્રૂપ-લેવલ દાવાઓ અલગ કર્યા. સ્પેસિફિસિટી અને સેન્ટિમેન્ટ માપ્યા. 150 વાક્યોના મેન્યુઅલ ગોલ્ડ ડેટાસેટ પર 4 ટાસ્કમાં મોડેલ્સ ટેસ્ટ કર્યા.</p>
        </div>

        <div class="card violet">
          <h4>તબક્કો 4: ગુગલ અર્થ એન્જિન સેટેલાઇટ એનાલિસિસ</h4>
          <p>290 મિલોની આસપાસ 10 કિમી બફર બનાવ્યા. Hansen v1.13 ડેટાથી 2021-2025 નું જંગલ કટિંગ માપ્યું (કુલ 890,168 હેક્ટર). મેમરી લિમિટ વધારીને 10 અબજ પિક્સેલ કરી.</p>
        </div>

        <div class="card rose">
          <h4>તબક્કો 5: કેનોનિકલ મિસમેચ એન્જિન અને ટેસ્ટ</h4>
          <p><code>scripts/build_scores_v2.py</code> કોડ બનાવ્યો. 4 ઘટકો વાળી માન્ય ફોર્મ્યુલા લાગુ કરી. pytest દ્વારા 23 ટેસ્ટ પાસ કર્યા.</p>
        </div>

        <div class="card blue">
          <h4>તબક્કો 6: મલ્ટિ-સેન્સર ક્રોસ-વેલિડેશન</h4>
          <p>IBM/NASA Prithvi ફાઉન્ડેશન મોડેલ 290 મિલો પર ચલાવ્યું (Spearman rho = 0.172). RADD રડારથી વાદળો પાછળ ચકાસણી કરી (4/5 પાસ). Descals ઓઇલ પામ મેપથી સાબિત કર્યું કે 56% જમીન પામ ઓઇલ બની ગઈ છે.</p>
        </div>
      </div>
    </section>

    <!-- SECTION 7 -->
    <section id="math">
      <h2>7. ગણિત અને સ્કોરિંગ ફોર્મ્યુલા</h2>
      <p>
        તમારા થીસીસનું હૃદય આ વૈજ્ઞાનિક સ્કોરિંગ ફોર્મ્યુલા છે જે તમામ સ્ક્રિપ્ટ્સ, ટેસ્ટ્સ અને પ્રકરણોમાં સમાન છે:
      </p>

      <div class="formula-box">
        Mismatch Score = 0.35 × Forest Loss + 0.35 × Specificity + 0.15 × Sentiment + 0.15 × Spatial Match
      </div>

      <p>
        તમામ ચારેય મેટ્રિક્સને ભેગા કરતા પહેલા સ્ટાન્ડર્ડ Min-Max Normalization દ્વારા 0 થી 100 ના સ્કેલ પર લાવવામાં આવે છે:
      </p>
      <div class="formula-box" style="font-size: 1.05rem;">
        Normalized Value = [ (Value - Min) / (Max - Min) ] × 100
      </div>

      <h3>ચારેય ઘટકો શા માટે મહત્વના છે?</h3>
      <ul>
        <li>
          <strong>Forest Loss Score (35% વજન):</strong> વર્ષ 2000 ના મૂળ જંગલમાંથી 2020 પછી મિલની આસપાસ કેટલા ટકા જંગલ કપાઈ ગયું તે માપે છે.
        </li>
        <li>
          <strong>Specificity Score (35% વજન):</strong> કંપનીના દાવા કેટલા ચોક્કસ અને સ્પષ્ટ છે તે માપે છે. જો દાવો એકદમ સ્પષ્ટ હોય અને જંગલ પણ કપાયું હોય તો મિસમેચ સૌથી વધુ ગણાય.
        </li>
        <li>
          <strong>Sentiment Score (15% વજન):</strong> કંપનીએ પોતાના રિપોર્ટમાં કેટલી મીઠી અને પોઝિટિવ વાતો કરી છે તે માપે છે.
        </li>
        <li>
          <strong>Spatial Match Score (15% વજન):</strong> કંપનીની કેટલી ટકા મિલો સમગ્ર ડેટાસેટના સરેરાશ નુકસાન (2,653 હેક્ટર) કરતાં વધુ નુકસાન ધરાવે છે તે માપે છે. જો બધી મિલોમાં વનનાબૂદી ફેલાયેલી હોય તો સ્કોર વધે છે.
        </li>
      </ul>

      <h3>ગણતરીનું સ્પષ્ટ ઉદાહરણ: KLK કંપની (રેન્ક 1)</h3>
      <p>KLK નો રેન્ક 1 સ્કોર 65.6 કેવી રીતે આવ્યો તે જુઓ:</p>
      <pre>
1. Forest Loss Score:    33.9  ×  0.35  =  11.9
2. Specificity Score:   100.0  ×  0.35  =  35.0   (સૌથી ચોક્કસ દાવા કર્યા હતા)
3. Sentiment Score:      68.4  ×  0.15  =  10.3
4. Spatial Match Score:  56.7  ×  0.15  =   8.5
───────────────────────────────────────────────
કુલ મિસમેચ સ્કોર (TOTAL MISMATCH SCORE):   65.6  (Rank 1 - સૌથી મોટું ગ્રીનવોશિંગ)
      </pre>

      <h3>ઇવેલ્યુએશન મેટ્રિક્સની સરળ ગુજરાતી વ્યાખ્યા:</h3>
      <ul>
        <li><strong>Accuracy (એક્યુરેસી):</strong> કુલ વાક્યોમાંથી મોડેલે કેટલા ટકા વાક્યો સાચા ઓળખ્યા.</li>
        <li><strong>Precision (પ્રિસિઝન):</strong> મોડેલે જે વાક્યોને "ક્લેઇમ" કહ્યા તેમાંથી ખરેખર કેટલા સાચા ક્લેઇમ હતા.</li>
        <li><strong>Recall (રિકોલ):</strong> રિપોર્ટમાં રહેલા તમામ સાચા દાવાઓમાંથી મોડેલ કેટલા દાવા પકડી શક્યું.</li>
        <li><strong>F1 Score:</strong> પ્રિસિઝન અને રિકોલનો સંતુલિત હાર્મોનિક મીન (શ્રેષ્ઠ સંતુલન માપવા માટે).</li>
        <li><strong>Cohen's Kappa (&kappa;):</strong> બે મોડેલ કે માણસો વચ્ચે તુક્કા વગર સાચો સહમતી દર કેટલો છે.</li>
        <li><strong>Spearman's Rank Correlation (&rho;):</strong> બે રેન્કિંગ વચ્ચેનો સંબંધ માપે છે (Prithvi AI અને Hansen સેટેલાઇટ લોસ વચ્ચેની સુસંગતતા).</li>
      </ul>
    </section>

    <!-- SECTION 8 -->
    <section id="findings">
      <h2>8. મુખ્ય પરિણામો અને 11 કંપનીઓની કેસ સ્ટડીઝ</h2>

      <p>
        તમારા સમગ્ર અભ્યાસમાં <strong>11 કંપનીઓ</strong>, <strong>290 મિલો</strong> અને <strong>890,168 હેક્ટર</strong> જંગલ કટિંગ આવરી લેવાયું છે:
      </p>

      <table>
        <thead>
          <tr>
            <th>રેન્ક</th>
            <th>કંપનીનું નામ</th>
            <th class="num">મિસમેચ સ્કોર</th>
            <th class="num">લોસ (35%)</th>
            <th class="num">ચોક્કસાઈ (35%)</th>
            <th class="num">સેન્ટિમેન્ટ (15%)</th>
            <th class="num">સ્પેશિયલ (15%)</th>
            <th class="num">2020 પછીનું નુકસાન</th>
            <th class="num">મિલો</th>
            <th class="num">મૂળ જંગલનું % નુકસાન</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>1</strong></td><td><strong>KLK</strong></td><td class="num"><strong>65.6</strong></td><td class="num">33.9</td><td class="num">100.0</td><td class="num">68.4</td><td class="num">56.7</td><td class="num">92,209 ha</td><td class="num">30</td><td class="num">12.18%</td></tr>
          <tr><td><strong>2</strong></td><td><strong>GAR</strong></td><td class="num"><strong>63.1</strong></td><td class="num">50.2</td><td class="num">67.6</td><td class="num">91.6</td><td class="num">54.0</td><td class="num">171,236 ha</td><td class="num">50</td><td class="num">13.87%</td></tr>
          <tr><td><strong>3</strong></td><td><strong>Musim Mas</strong></td><td class="num"><strong>56.2</strong></td><td class="num">26.9</td><td class="num">85.1</td><td class="num">63.6</td><td class="num">50.0</td><td class="num">53,060 ha</td><td class="num">18</td><td class="num">11.45%</td></tr>
          <tr><td><strong>4</strong></td><td><strong>IOI</strong></td><td class="num"><strong>56.1</strong></td><td class="num">100.0</td><td class="num">0.0</td><td class="num">60.3</td><td class="num">80.0</td><td class="num">74,385 ha</td><td class="num">15</td><td class="num">19.04%</td></tr>
          <tr><td><strong>5</strong></td><td><strong>SD Guthrie</strong></td><td class="num"><strong>55.2</strong></td><td class="num">55.4</td><td class="num">32.9</td><td class="num">100.0</td><td class="num">61.9</td><td class="num">142,131 ha</td><td class="num">42</td><td class="num">14.41%</td></tr>
          <tr><td><strong>6</strong></td><td><strong>Wilmar</strong></td><td class="num"><strong>50.3</strong></td><td class="num">26.4</td><td class="num">67.2</td><td class="num">70.0</td><td class="num">46.7</td><td class="num">127,606 ha</td><td class="num">45</td><td class="num">11.40%</td></tr>
          <tr><td><strong>7</strong></td><td><strong>First Resources</strong></td><td class="num"><strong>41.7</strong></td><td class="num">15.7</td><td class="num">75.6</td><td class="num">27.8</td><td class="num">37.5</td><td class="num">40,090 ha</td><td class="num">16</td><td class="num">10.29%</td></tr>
          <tr><td><strong>8</strong></td><td><strong>Genting</strong></td><td class="num"><strong>39.5</strong></td><td class="num">28.4</td><td class="num">46.6</td><td class="num">41.4</td><td class="num">46.7</td><td class="num">44,362 ha</td><td class="num">15</td><td class="num">11.61%</td></tr>
          <tr><td><strong>9</strong></td><td><strong>Bumitama</strong></td><td class="num"><strong>38.5</strong></td><td class="num">0.0</td><td class="num">67.1</td><td class="num">71.4</td><td class="num">28.6</td><td class="num">30,549 ha</td><td class="num">14</td><td class="num">8.66%</td></tr>
          <tr><td><strong>10</strong></td><td><strong>SIPEF</strong></td><td class="num"><strong>26.1</strong></td><td class="num">17.0</td><td class="num">28.3</td><td class="num">41.0</td><td class="num">27.3</td><td class="num">27,341 ha</td><td class="num">11</td><td class="num">10.42%</td></tr>
          <tr><td><strong>11</strong></td><td><strong>Astra Agro</strong></td><td class="num"><strong>17.6</strong></td><td class="num">20.2</td><td class="num">13.8</td><td class="num">0.0</td><td class="num">38.2</td><td class="num">87,198 ha</td><td class="num">34</td><td class="num">10.76%</td></tr>
        </tbody>
      </table>

      <h3>મહત્વની 4 કંપનીઓની ઊંડાણપૂર્વક કેસ સ્ટડી:</h3>
      <div class="card-grid">
        <div class="card blue">
          <h4>KLK (રેન્ક 1 — સ્કોર: 65.6)</h4>
          <p>
            KLK એ રિપોર્ટમાં ખૂબ જ ચોક્કસ તારીખો, જીપીએસ મેપિંગ અને કડક ઓડિટના વચનો આપ્યા હતા (સ્પેસિફિસિટી સ્કોર 100.0). પરંતુ સેટેલાઇટે તેની 30 મિલો આસપાસ <strong>92,209 હેક્ટર</strong> જંગલ કપાયેલું પકડ્યું (12.18% મૂળ જંગલ સાફ). જ્યારે આટલા ચોક્કસ દાવા સામે આટલું મોટું નુકસાન દેખાયું ત્યારે મોડેલે તેને સૌથી મોટો વિરોધાભાસ (Rank 1) જાહેર કર્યો.
          </p>
        </div>

        <div class="card green">
          <h4>Golden Agri-Resources / GAR (રેન્ક 2 — સ્કોર: 63.1)</h4>
          <p>
            GAR આખા અભ્યાસમાં સૌથી વધુ જમીન સાફ કરનારી કંપની નીકળી: 50 મિલોની આસપાસ <strong>171,236 હેક્ટર</strong> જંગલ કપાયું! તેના 2025 ના રિપોર્ટમાં તે દાવો કરે છે કે અમારી પાસે <strong>99.8% ટ્રેસેબિલિટી</strong> છે અને ખૂબ ઉત્સાહી ટોન વાપરે છે (91.6 સેન્ટિમેન્ટ). તેની એકલી NAGA SAKTI મિલ પાસે 10,197 હેક્ટર જંગલ સાફ થઈ ગયું છે.
          </p>
        </div>

        <div class="card rose">
          <h4>IOI Corporation (રેન્ક 4 — સ્કોર: 56.1)</h4>
          <p>
            IOI પાસે સમગ્ર અભ્યાસમાં સૌથી ભયાનક વનનાબૂદીનો દર છે: <strong>19.04% મૂળ જંગલ સાફ</strong> (મિલ દીઠ સરેરાશ 4,959 હેક્ટર). સમગ્ર પ્રોજેક્ટની સૌથી વધુ નુકસાન વાળી મિલ IOI ની <strong>SYARIMO</strong> મિલ (12,318 હેક્ટર લોસ) છે! છતાં IOI 4થા નંબરે કેમ રહ્યું? કારણ કે તેના 66 દાવા સાવ અસ્પષ્ટ અને હવાઈ વાતો (0.0 સ્પેસિફિસિટી) હતા. કંપનીએ કશું ચોક્કસ ન બોલીને પોતાનો સ્કોર બચાવી લીધો (Cheap Talk shield).
          </p>
        </div>

        <div class="card orange">
          <h4>Astra Agro Lestari (રેન્ક 11 — સ્કોર: 17.6)</h4>
          <p>
            Astra Agro પાસે <strong>87,198 હેક્ટર</strong> જંગલ કટિંગ છે, છતાં તે સૌથી છેલ્લા (11મા) નંબરે આવી. કેમ? કારણ કે તેણે રિપોર્ટમાં કોઈ મોટી ડંફાસો મારી જ નહોતી (સેન્ટિમેન્ટ: 0.0, સ્પેસિફિસિટી: 13.8). 11મો રેન્ક એટલે કંપની પવિત્ર છે તેવું નથી, પણ તેના શબ્દો અને કામ વચ્ચે મોટો વિરોધાભાસ પકડી શકાતો નથી કારણ કે તેણે વાતો જ ઓછી કરી છે.
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION 9 -->
    <section id="validations">
      <h2>9. સ્વતંત્ર ક્રોસ-વેલિડેશન (4 ચકાસણીઓ)</h2>
      <p>
        કોઈ એમ ન કહી શકે કે આ પરિણામો ફક્ત એક સેટેલાઇટની ભૂલ છે, તે સાબિત કરવા માટે તમારા થીસીસમાં 4 સ્વતંત્ર ટેસ્ટ કરવામાં આવ્યા:
      </p>

      <div class="card-grid">
        <div class="card violet">
          <h4>1. IBM/NASA Prithvi AI ફાઉન્ડેશન મોડેલ</h4>
          <p>
            નાસા અને આઈબીએમ દ્વારા બનાવેલું 300M પેરામીટર વાળું અત્યાધુનિક સેટેલાઇટ વિઝન ટ્રાન્સફોર્મર મોડેલ છે. તેને કોઈ પણ વધારાની ટ્રેનિંગ આપ્યા વગર (Zero-shot) 2019 અને 2024 ના સેન્ટિનેલ-2 ફોટા સરખાવવા માટે વાપર્યું. તેણે 290 મિલો પર Hansen સાથે નોંધપાત્ર સંબંધ (Spearman rho = 0.172, p &lt; 0.0001) બતાવ્યો.
          </p>
        </div>

        <div class="card blue">
          <h4>2. રડાર વનનાબૂદી એલર્ટ્સ: Wageningen RADD</h4>
          <p>
            સેન્ટિનેલ-1 રડારથી વાદળો અને વરસાદની આરપાર જમીન તપાસી. ટોચની 5 કંપનીઓની સૌથી વધુ નુકસાન વાળી મિલો ચેક કરી. <strong>5 માંથી 4 મિલોમાં રડારે જમીન પર વનનાબૂદીની પુષ્ટિ આપી</strong>, જે સાબિત કરે છે કે ઓપ્ટિકલ સેટેલાઇટના તારણો સાચા છે.
          </p>
        </div>

        <div class="card green">
          <h4>3. જમીન વપરાશનો પુરાવો: Descals et al. (2021)</h4>
          <p>
            સેટેલાઇટથી દેખાયેલું કટિંગ પામ ઓઇલ માટે જ હતું તે સાબિત કરવા 10-મીટર ડીપ લર્નિંગ પામ ઓઇલ મેપ સરખાવ્યો. સાબિત થયું કે <strong>2020 પછી કપાયેલી 56.0% જમીન (અને IOI માં 89.8% જમીન) સીધી પામ ઓઇલ પ્લાન્ટેશન બની ગઈ છે</strong>!
          </p>
        </div>

        <div class="card orange">
          <h4>4. બફર અંતરની સંવેદનશીલતા (5 થી 30 કિમી)</h4>
          <p>
            મિલની આસપાસ 5, 10, 15, 20 અને 30 કિમીના બફર ટેસ્ટ કર્યા. કંપનીઓનું રેન્કિંગ લગભગ સમાન રહ્યું (Spearman rho = 0.80 થી 0.96). 30 કિમી પર બહારનો અવાજ આવવા લાગે છે, જેથી 10 કિમીનો બફર સૌથી યોગ્ય સાબિત થયો.
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION 10 -->
    <section id="engineering">
      <h2>10. ડેટા એન્જિનિયરિંગની 108 કલાકની લડાઈઓ</h2>
      <p>
        થીસીસના પ્રકરણ 3 ના ટેબલ 3.4 માં વાસ્તવિક દુનિયાના ડેટાની ખામીઓ સુધારવામાં વિતાવેલા 108 કલાકનો હિસાબ નોંધાયેલો છે:
      </p>

      <table>
        <thead>
          <tr>
            <th>પાઇપલાઇન તબક્કો</th>
            <th>સામે આવેલી ટેકનિકલ સમસ્યા</th>
            <th>તમે અમલમાં મૂકેલો ઉકેલ</th>
            <th class="num">ખર્ચેલા કલાક</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>મિલ રજિસ્ટ્રી પાર્સિંગ</strong></td>
            <td>UML ફાઇલમાં લેટ/લોંગ નંબરો બગડી ગયા હતા, જેનાથી મિલો દરિયામાં દેખાતી હતી.</td>
            <td>અસલ લખાણ વાળી કોલમમાંથી ટેક્સ્ટ જીપીએસ કાઢ્યું અને બાઉન્ડિંગ બોક્સ ચેક મૂક્યા.</td>
            <td class="num">4</td>
          </tr>
          <tr>
            <td><strong>કંપની મેચિંગ</strong></td>
            <td>SD Guthrie ની પેટાકંપનીઓ અલગ નામ હેઠળ હોવાથી ફક્ત 2 જ મિલ મળતી હતી.</td>
            <td>Group Name અને Parent Company બંનેમાં સર્ચ કર્યું, જેથી મિલો 2 થી વધીને 42 થઈ અને 142k હેક્ટર ડેટા બચી ગયો.</td>
            <td class="num">5</td>
          </tr>
          <tr>
            <td><strong>લખાણની સફાઈ</strong></td>
            <td>PDF માં રહેલી અદ્રશ્ય નોન-બ્રેકિંગ સ્પેસ (<code>\u00a0</code>) ના લીધે પંડાસ ડેટા મર્જ થતો નહોતો.</td>
            <td>વ્હાઇટસ્પેસ રેજેક્સ નોર્મલાઇઝેશન કર્યું અને <code>regex=False</code> લાગુ કર્યું.</td>
            <td class="num">3</td>
          </tr>
          <tr>
            <td><strong>સેટેલાઇટ એક્સ્ટ્રેક્શન</strong></td>
            <td>ગુગલ અર્થ એન્જિનની મેમરી લિમિટ (1 કરોડ પિક્સેલ) 91,000 ચોરસ કિમીના વિસ્તારમાં ક્રેશ થઈ જતી હતી.</td>
            <td>મેમરી વધારીને 10 અબજ પિક્સેલ (<code>maxPixels = 1e10</code>) કરી અને ઇન્ટરમીડિયેટ કેશિંગ બનાવ્યું.</td>
            <td class="num">12</td>
          </tr>
          <tr>
            <td><strong>NLP મોડેલિંગ</strong></td>
            <td>FinBERT અને ClimateBERT સેન્ટિમેન્ટ વચ્ચે ફક્ત 53% સહમતી હતી (Kappa = 0.08).</td>
            <td>સમજાયું કે FinBERT કોર્પોરેટ ડંફાસો પકડે છે જ્યારે ClimateBERT બધું ન્યુટ્રલ ગણે છે. FinBERT પસંદ કર્યું.</td>
            <td class="num">6</td>
          </tr>
          <tr>
            <td><strong>ગોલ્ડ બેન્ચમાર્ક</strong></td>
            <td>પામ ઓઇલ માટે ચકાસાયેલો કોઈ સ્ટાન્ડર્ડ AI ડેટાસેટ ઉપલબ્ધ નહોતો.</td>
            <td>150 વાક્યોનું જાતે મેન્યુઅલ લેબલિંગ કર્યું અને 4 ટાસ્ક પર મોડેલ ટેસ્ટ કર્યા.</td>
            <td class="num">10</td>
          </tr>
          <tr>
            <td><strong>પ્રોડક્શન થિયરી</strong></td>
            <td>કંપનીઓના રિપોર્ટમાં FFB, CPO અને રિફાઇનરીના આંકડાઓમાં ભારે વિસંગતતા હતી.</td>
            <td>રેન્કિંગમાં અવાજ ન આવે તે માટે પ્રોડક્શન થિયરીને થીસીસમાંથી કાયમ માટે પડતી મૂકી દીધી.</td>
            <td class="num">8</td>
          </tr>
          <tr>
            <td><strong>સેટેલાઇટ મેપ્સ</strong></td>
            <td>વિષુવવૃત્તીય વાદળો અને ધુમ્મસના લીધે સેટેલાઇટ ફોટા અંધારા દેખાતા હતા.</td>
            <td>ક્લાઉડ-માસ્કિંગ મીડિયન કમ્પોઝિટ અને પર્સેન્ટાઇલ કોન્ટ્રાસ્ટ સ્ટ્રેચિંગથી 290 મિલોના 300 DPI મેપ્સ બનાવ્યા.</td>
            <td class="num">14</td>
          </tr>
          <tr>
            <td><strong>Prithvi AI સ્કેલિંગ</strong></td>
            <td>300M પેરામીટર મોડેલ લોકલ કમ્પ્યુટર પર ખૂબ ધીમું ચાલતું હતું.</td>
            <td>Google Colab GPU વર્કફ્લો બનાવ્યો અને બધી 290 મિલો પર પ્રિથ્વી મોડેલ રન કર્યું.</td>
            <td class="num">12</td>
          </tr>
          <tr>
            <td><strong>ક્રોસ-વેલિડેશન</strong></td>
            <td>બફર વિસ્તારની મર્યાદાઓ સામે સવાલો ઉઠી શકે તેમ હતા.</td>
            <td>Descals 10m પામ ઓવરલે, RADD રડાર અને બફર ડિસ્ટન્સ સેન્સિટિવિટી રન કરી.</td>
            <td class="num">10</td>
          </tr>
          <tr>
            <td><strong>ટેસ્ટિંગ અને ક્વોલિટી</strong></td>
            <td>સ્કોરિંગ ફોર્મ્યુલા અને બાઉન્ડ્સ ક્યારેય ન તૂટે તેની ખાતરી કરવી.</td>
            <td>23 પાયટેસ્ટ (pytest) યુનિટ ટેસ્ટ્સનો કડક સ્યુટ બનાવ્યો.</td>
            <td class="num">4</td>
          </tr>
          <tr>
            <td><strong>થીસીસ લેખન (LaTeX)</strong></td>
            <td>સંપૂર્ણ 9 પ્રકરણોનું ડ્રાફ્ટિંગ અને ઓવરલીફ માટે તૈયારી.</td>
            <td>19,565 શબ્દો, શૂન્ય એમ-ડેશ, શૂન્ય AI બઝવર્ડ્સ અને સંપૂર્ણ બેલેન્સ્ડ થીસીસ.</td>
            <td class="num">20</td>
          </tr>
          <tr style="font-weight: 700; background: rgba(56, 189, 248, 0.08);">
            <td colspan="3">કુલ ટેકનિકલ એન્જિનિયરિંગ અને સમસ્યા નિવારણ સમય</td>
            <td class="num">108 કલાક</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- SECTION 11 -->
    <section id="summary-card">
      <h2>11. ઝડપી રિવિઝન રેફરન્સ કાર્ડ</h2>
      <div class="card-grid">
        <div class="card blue">
          <h4>મુખ્ય ઉદ્દેશ્ય (Core Goal)</h4>
          <p>પામ ઓઇલ કંપનીઓના 100% નો-ડિફોરેસ્ટેશનના દાવાઓને સેટેલાઇટ ફોટા સાથે સરખાવીને 0 થી 100 નો ઓબ્જેક્ટિવ મિસમેચ સ્કોર આપવો.</p>
        </div>

        <div class="card green">
          <h4>ચકાસાયેલા મુખ્ય આંકડા (Headline Numbers)</h4>
          <p><strong>11 કંપનીઓ &bull; 290 મિલો &bull; 890,168 હેક્ટર</strong> જંગલ કટિંગ 2020 પછી પકડાયું. તમામ 290 મિલો પર નુકસાન નોંધાયું.</p>
        </div>

        <div class="card orange">
          <h4>સ્કોરિંગ ફોર્મ્યુલા વજન (Formula Weights)</h4>
          <p><code>Mismatch = 0.35*Loss + 0.35*Specificity + 0.15*Sentiment + 0.15*Spatial</code>. બરાબર 50% સેટેલાઇટ / 50% લખાણ. વજનનો સરવાળો = 1.0.</p>
        </div>

        <div class="card rose">
          <h4>ટોપ અને બોટમ રેન્કિંગ</h4>
          <p><strong>KLK રેન્ક 1 (65.6)</strong> કારણ કે 100 ચોક્કસાઈ વાળા દાવા સામે 92k હેક્ટર નુકસાન મળ્યું. <strong>Astra Agro રેન્ક 11 (17.6)</strong> કારણ કે તેણે વાતો જ ઓછી કરી હતી.</p>
        </div>

        <div class="card violet">
          <h4>મુખ્ય ક્રોસ-વેલિડેશન પરિણામ</h4>
          <p>Descals AI મેપે સાબિત કર્યું કે કપાયેલી <strong>56.0% જમીન (અને IOI માં 89.8% જમીન)</strong> સીધી પામ ઓઇલ પ્લાન્ટેશન બની ગઈ છે.</p>
        </div>
      </div>
    </section>
  </div>

  <button class="print-btn" onclick="window.print()">પ્રિન્ટ / PDF સેવ કરો</button>
</body>
</html>
"""

output_path = r"C:\Users\Allah o akbar\thesis\Master_Thesis_Complete_Guide_Gujarati.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated {output_path} with {len(html_content)} characters.")
