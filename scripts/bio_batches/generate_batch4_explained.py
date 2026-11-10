import json

# Dictionary of explanations for questions 151 to 200 (indices 0 to 49)
explanations = {
    0: (
        "Baktérie a ich biochemické vlastnosti majú obrovské využitie v biotechnológiách a prírodných procesoch (b, c, e, f, g). "
        "Podľa oficiálneho kľúča testovnice UPJŠ LF sú označené možnosti b, c, e, f, g, ktoré zahŕňajú fermentačné procesy v mliekárenstve "
        "(jogurty, syry), uplatnenie v kvasnom a farmaceutickom priemysle, ako aj schopnosť pôdnych baktérií mineralizovať organické zvyšky "
        "a udržiavať biogeochemické cykly prvkov v prírode. Možnosti a, d, h neboli do oficiálneho kľúča pre túto otázku zaradené."
    ),
    1: (
        "V prirodzených ekosystémoch fungujú baktérie ako rozkladače (destruenty a reducenty), ktoré rozkladajú odumreté telá rastlín a živočíchov "
        "a mineralizujú organickú hmotu na jednoduché anorganické látky (d, g). Tým uzatvárajú biogeochemické cykly (nezastupiteľná úloha pri "
        "cyklickej premene látok) a výrazne prispievajú k samočisteniu vodných tokov (f, h). Väčšina baktérií kyslík do atmosféry neprodukuje (a), "
        "fotosyntéza rastlín vyžaduje anorganický CO2 a nie pôdne organické zlúčeniny (e), a patogénny účinok nie je základom ekologickej stability (b)."
    ),
    2: (
        "Podľa spôsobu zhrubnutia bunkovej steny a prítomnosti intercelulár sa trváce pletivá delia na tenkostenný parenchým, nerovnomerne zhrubnutý "
        "kolenchým a rovnomerne silno zhrubnutý sklerenchým, čo korešponduje aj s rozdelením na pletivá parenchymatické a mechanické (b, h). "
        "Rozdelenie na krycie, vodivé a základné vychádza z funkcie pletív (a, g), kým delivé a trváce predstavujú delenie podľa schopnosti mitózy (c)."
    ),
    3: (
        "Základné pletivo tvorí prevažnú časť rastlinného tela a je tvorené parenchymatickými bunkami, ktoré vypĺňajú priestor medzi krycím pletivom "
        "(pokožkou) a cievnymi zväzkami (f). Na rastových vrcholoch stoniek a koreňov sa nachádzajú vrcholové meristémy (a, b) a lyko s drevom tvoria "
        "samotné vodivé pletivá (c, e)."
    ),
    4: (
        "Parenchým a kolenchým sú tvorené živými bunkami, pričom kolenchým plní mechanickú funkciu a má bunkové steny zhrubnuté nerovnomerne, zvyčajne v hranách (a, e). "
        "Sklerenchým je pevné mechanické pletivo s rovnomerne zhrubnutými stenami, ktorých bunkové lúmeny sú pospájané kanálikmi s plazmodezmami (b, c). "
        "Pokožka nadzemných orgánov je epiderma (nie rizoderma) (f), koreňová pokožka je rizoderma (nie epiderma) (g), a pŕhľavé chlpy pŕhľavy sú trichómy, nie emergencie (h)."
    ),
    5: (
        "Prieduchy (stómy) sú špecializované štruktúry epidermy tvorené dvoma obličkovitými zatváravými bunkami obklopujúcimi prieduchovú štrbinu (c). "
        "Na rozdiel od ostatných buniek epidermy obsahujú zatváravé bunky chloroplasty (d), vďaka čomu regulujú výmenu dýchacích plynov (príjem CO2 a výdaj O2) "
        "a transpiráciu – výdaj vody vo forme vodnej pary (f, g). Výdaj kvapalnej vody prebieha cez hydatódy (e) a v rizoderme koreňa sa prieduchy nenachádzajú (h)."
    ),
    6: (
        "Hydatódy (vodné prieduchy) sú špeciálne modifikované prieduchy, ktoré stratili zatváraciu schopnosť a zostávajú trvalo otvorené (b, e). "
        "Slúžia na gutáciu – vylučovanie kvapalnej vody a rozpustených minerálnych solí pri vysokom pôdnom výtlaku a zníženej transpirácii (a). "
        "Podľa kľúča testovnice je označená aj možnosť h, hoci primárne ide o modifikácie epidermy (nie trichómy f, ani bunky rizodermy g)."
    ),
    7: (
        "Emergencie sú mnohobunkové ochranné výrastky, na vzniku ktorých sa podieľa nielen pokožka (epiderma), ale aj hlbšie podpokožkové pletivá (kôra). "
        "Typickým príkladom sú ostne ruže šípovej (e), pichliače egreša (a) a tentakuly mäsožravých rastlín (d), ktoré slúžia najmä na ochranu pred bylinožravcami (h). "
        "Chlpy muškátu a pŕhľavé chlpy pŕhľavy sú trichómy čisto epidermálneho pôvodu (b, c)."
    ),
    8: (
        "V xyléme (drevnej časti cievnych zväzkov) zabezpečujú vedenie vody a minerálnych solí (transpiračný prúd) cievy (trachey) a cievice (tracheidy) (d, e, f, g). "
        "Tracheidy sú vývojovo staršie pretiahnuté odumreté bunky so zachovanými šikmými priehradkami, kým trachey sú dlhé rúrky s perforovanými či zaniknutými stenami. "
        "Sitkovice vedú asimiláty vo floéme (c), kým prieduchy (a) a trichómy (h) patria medzi pletivá krycie."
    ),
    9: (
        "Sitkovice sú vodivé elementy floému (lykovej časti cievnych zväzkov), tvorené živými pretiahnutými bezjadrovými bunkami, ktorých priečne priehradky sú sitkovito perforované (a, g). "
        "Zabezpečujú vedenie asimilátov (sacharózy) z listov na miesta ich spotreby alebo ukladania a ich funkčnosť zvyčajne trvá len jedno až dve vegetačné obdobia, kým sa nezanesú kalózou (d, e). "
        "Odumreté bunky tvoriace súvislé trubice na vedenie vody patria xylému (cievy a cievice) (b, c, f, h)."
    ),
    10: (
        "Transpiračný prúd vedie vodu s rozpustenými anorganickými živinami pasívne smerom nahor z koreňov do listov a rastových vrcholov (e). "
        "Tento transport prebieha v drevnej časti cievnych zväzkov (xyléme) prostredníctvom ciev (tracheí) a cievic (tracheíd) vďaka transpirácii a koreňovému výtlaku (a, b, h). "
        "Lyková časť (floém) a sitkovice slúžia na vedenie asimilačného prúdu opačným smerom (c, d, g)."
    ),
    11: (
        "Asimilačný prúd transportuje organické látky syntetizované pri fotosyntéze (hotové asimiláty, najmä sacharózu) z fotosyntetizujúcich listov do koreňov, kvetov a plodov (d, e). "
        "Prúdi lykovou časťou cievnych zväzkov (floémom) prostredníctvom živých sitkovíc (b, g). Drevnou časťou (xylémom) stúpajú cievami a cievicami anorganické živiny (a, c, h)."
    ),
    12: (
        "Koreň (radix) vykonáva viacero kľúčových funkcií: upevňuje rastlinu v substráte (mechanická funkcia) a prijíma z pôdy vodu s minerálmi (vyživovacia funkcia) (a, b). "
        "Zároveň syntetizuje fytohormóny, aminokyseliny a sekundárne metabolity (metabolická funkcia) a umožňuje nepohlavné vegetatívne rozmnožovanie pomocou koreňových výmladkov (e, h). "
        "Transpirácia a fotosyntéza sú doménou listov (f, g) a pohlavné rozmnožovanie zabezpečujú generatívne orgány (d)."
    ),
    13: (
        "Rastúci koreňový vrchol s apikálnym meristémom je chránený koreňovou čiapočkou (kalyptrou) (g). "
        "Kalyptra je tvorená parenchymatickými bunkami, ktorých steny slizovatejú, čím uľahčujú prenikanie koreňa medzi pôdnymi časticami a znižujú mechanické trenie (h). "
        "Presýpací škrob vo vnútri čiapočky plní funkciu statolitového aparátu vnímajúceho gravitáciu (c, d, e), ale samotnú mechanickú ochranu tvorí čiapočka."
    ),
    14: (
        "Škrobové zrná (amyloplasty) v strednej časti koreňovej čiapočky fungujú ako statolitový aparát (h). "
        "Pôsobením zemskej príťažlivosti sedimentujú na spodnej strane buniek, čo vyvoláva asymetrickú distribúciu auxínu a indukuje pozitívny geotropický rast koreňa v smere zemskej tiaže (c, e). "
        "Tento škrob nemá vyživovaciu ani zásobnú funkciu, ide o senzorický mechanizmus gravitropizmu (a, d)."
    ),
    15: (
        "U rastlín rozlišujeme dva základné typy koreňových sústav: aloríziu (primárnu koreňovú sústavu) s dominantným hlavným koreňom a bočnými koreňmi (typickú pre dvojklíčnolistové a nahosemenné) "
        "a homoríziu (vedľajšiu alebo adventívnu koreňovú sústavu), kde hlavný koreň zakrpatieva a je nahradený zväzkom náhradných adventívnych koreňov zo stonky (typickú pre jednoklíčnolistové) (a, b, d, e, f). "
        "Pojmy ako meristematická či generatívna koreňová sústava v botanickej morfológii neexistujú (c, h)."
    ),
    16: (
        "Koreňové vlásky sú vychlípeniny buniek koreňovej pokožky (rizodermy) v absorpčnej zóne, ktoré stonásobne zväčšujú plochu na príjem vody a minerálnych živín. "
        "Podľa oficiálneho kľúča testovnice UPJŠ LF sú priradené možnosti b, d, h. V anatómii rastlinných orgánov koreň úzko integruje mechanické pletivá (h), "
        "vodivý systém s lúčovitým radiálnym usporiadaním (d) a dodáva anorganické živiny pre asimilačné procesy (b)."
    ),
    17: (
        "Vek stromov sa primárne určuje počítaním letokruhov, ktoré odrážajú ročné prírastky sekundárneho dreva tvoreného kambiom (d, f). "
        "Jarné a letné drevo sa výrazne líšia štruktúrou, hustotou a farbou, pričom hrúbka kmeňa a sekundárne vrstvy tiež korelujú s vekom (f). "
        "Podľa kľúča testovnice sú zaradené možnosti a, c, d, f, g, pričom kľúčovým biologickým ukazovateľom je práve striedanie jarného a letného dreva."
    ),
    18: (
        "Fylotaxia (postavenie listov na stonke) optimalizuje zachytávanie slnečného svetla a môže byť striedavé (z každého uzla vyrastá jeden list), "
        "protistojné (z uzla vyrastajú dva listy oproti sebe) alebo praslenovité (z jedného uzla vyrastajú tri a viac listov) (e, f, g). "
        "Pojmy perovité a dlaňovité označujú typ členenia čepele či žilnatiny (a, d), zložené vyjadruje stavbu listu z lístkov (b) a strapcovité je typ súkvetia (h)."
    ),
    19: (
        "Jarné drevo sa tvorí na jar počas intenzívneho prúdenia miazgy a je tvorené veľkými bunkami s tenkou bunkovou stenou, čo mu dodáva svetlejšiu farbu a menšiu hustotu (d, h). "
        "Letné drevo vzniká koncom vegetačného obdobia, plní najmä mechanickú spevňovaciu funkciu a pozostáva z menších buniek s hrubými stenami, preto je tmavšie a pevnejšie (e, h). "
        "Preto možnosti označujúce jarné drevo za tmavšie (c) alebo letné za svetlejšie (a) nie sú správne."
    ),
    20: (
        "Vek stromov sa exaktne určuje podľa počtu letokruhov (b), ktoré na priečnom reze kmeňom vytvárajú sústredné kruhy jarného a letného sekundárneho dreva (d, f). "
        "Každý letokruh reprezentuje prírastok sekundárneho dreva vyprodukovaný kambiom za jedno vegetačné obdobie. Podľa oficiálneho kľúča testovnice je v tejto položke označená aj možnosť h."
    ),
    21: (
        "Medzi metamorfózy (tvarové a funkčné premeny) stonky patria poplazy zabezpečujúce vegetatívne rozmnožovanie (napr. jahoda) (a), "
        "úponky slúžiace na prichytávanie popínavých rastlín (napr. vinič) (c), brachyblasty ako skrátené bočné konáriky (napr. smrekovec) (e) a podzemky slúžiace ako zásobné podzemné stonky (g). "
        "Bôrka a korok sú sekundárne krycie pletivá (b, f), buľva je metamorfózou koreňa a stonky (d) a stvol je bežná bezlistá stonka, nie metamorfóza (h)."
    ),
    22: (
        "Základnými fyziologickými funkciami typického zeleného asimilačného listu sú fotosyntetická asimilácia (syntéza organických látok pomocou chlorofylu a svetla) (g), "
        "transpirácia (vyparovanie vody chrániace rastlinu pred prehriatím a udržiavajúce transpiračný prúd) (c, d) a výmena dýchacích plynov (CO2 a O2) cez prieduchy (a). "
        "Rozvod živín a spevňovanie zabezpečujú cievne zväzky a mechanické pletivá stonky (b, e, f)."
    ),
    23: (
        "Gutácia je výdaj vody v kvapalnom stave (vo forme kvapôčok) pri vysokom koreňovom výtlaku a vysokej vzdušnej vlhkosti, kedy je obmedzená transpirácia. "
        "Uskutočňuje sa cez hydatódy (vodné prieduchy) (a), čo sú modifikované prieduchy, ktoré stratili schopnosť zatvárať sa a ostávajú trvalo otvorené (e). "
        "Bežné prieduchy zabezpečujú výdaj vody vo forme vodnej pary (b), lenticely slúžia na vetranie drevín (c) a tentakuly sú žliazkaté výrastky mäsožraviek (g)."
    ),
    24: (
        "Pri druhotne hrubnúcich stonkách drevín je primárna epiderma nahradená nepriedušným druhotným krycím pletivom – korkom (peridermom). "
        "Výmenu plynov (O2 a CO2) medzi vnútornými živými pletivami a vonkajším prostredím zabezpečujú lenticely (čočinky), ktoré predstavujú modifikované prevzdušňovacie prieduchové útvary (a). "
        "Tentakuly lapajú hmyz (b), nódy sú uzly stonky (f) a emergencie sú ochranné ostne (h)."
    ),
    25: (
        "Opadávanie listov (abscisia) je riadený proces urýchľovaný kyselinou abscisovou (ABA), pri ktorom sa na báze listovej stopky vytvorí parenchymatická odlučovacia vrstva "
        "a ochranná korková vrstvička zabraňujúca strate vody a infekcii (a, b, e). Pri listnáčoch opadávajú listy každoročne, zatiaľ čo ihličnany obmieňajú ihlice spravidla v intervale 2 až 3 roky, "
        "pričom pri niektorých druhoch ihlice pretrvávajú až 9 a viac rokov (g, h)."
    ),
    26: (
        "Vegetatívne orgány zabezpečujú individuálny rast, metabolizmus a výživu rastliny; patrí sem koreň (radix) (c, d), stonka (kaulom) (b, e) a listy (f). "
        "Naopak kvet (flos), semeno a plod sú generatívne (reprodukčné) orgány zabezpečujúce pohlavné rozmnožovanie a zachovanie druhu (a, g, h)."
    ),
    27: (
        "Reprodukčné orgány semenných rastlín sú metamorfovaného listového pôvodu (plodolisty, tyčinky, šupiny) (b) a ich primárnou úlohou je tvorba pohlavných buniek – gamét (h). "
        "U nahosemenných rastlín (borovicorastov) sú usporiadané do jednopohlavných samčích a samičích šištičiek (c, d), kým u krytosemenných rastlín (magnóliorastov) sú sústredené do kvetov (a, e, f). "
        "Samotné reprodukčné orgány nevznikajú opelením, ale proces opelenia a oplodnenia umožňujú (g)."
    ),
    28: (
        "Základnými rozmnožovacími časticami rastlín sú výtrusy (spóry) pri výtrusných rastlinách a semená pri semenných rastlinách (d, f). "
        "Spóry sú jednobunkové nepohlavné častice vznikajúce meiózou vo výtrusniciach (nie opelením h), kým semeno je mnohobunkový generatívny útvar obsahujúci zárodok (embryo) s vyživovacím pletivom. "
        "Listy, stonky a korene sú vegetatívne orgány (a, b, c)."
    ),
    29: (
        "Výtrusy (spóry) sú nepohlavné rozmnožovacie častice, ktoré vznikajú redukčným delením (meiózou) vo výtrusniciach (sporangiách) sporofytu (d, h). "
        "Vyvíjajú sa diferenciáciou somatických telových buniek materskej rastliny pred meiotickým delením (f, g). "
        "Spóry nevznikajú opelením ani oplodnením (a, b), ktoré vedú k vzniku semena pri semenných rastlinách."
    ),
    30: (
        "Vrcholíkovité (cymózne) súkvetia sú charakteristické tým, že hlavná os je skrátená, jej rast je ukončený vrcholovým kvetom a bočné osi ju prerastajú. "
        "Medzi vrcholíkovité monocháziá a dicháziá patrí skrutec (napr. nezábudka), kosáčik (napr. mečík), závinok a papraslen (a, c, f, h). "
        "Chocholík, okolík a hlávka patria medzi strapcovité (racemózne) súkvetia (b, d, e)."
    ),
    31: (
        "Strapcovité (racemózne) súkvetia majú dominantnú hlavnú os, ktorá neprestáva rásť a rozkonáruje sa monopodiálne; bočné kvety rozkvitajú akropetálne (zdola nahor). "
        "Patria sem klas (napr. skorocel), okolík (napr. prvosienka), šúľok (napr. kukurica), jahňada (napr. lieska, topoľ) a hlávka (napr. ďatelina) (a, b, e, g, h). "
        "Vrcholík, kosáčik a závinok sú súkvetia vrcholíkovité (c, d, f)."
    ),
    32: (
        "Dvojité oplodnenie je unikátnym evolučným znakom krytosemenných rastlín (magnóliorastov – Magnoliophyta) (b, d). "
        "Pri tomto procese jedna spermatozoidná bunka peľového vrecúška oplodní vajcovú bunku za vzniku diploidnej zygoty (2n) a druhá spermatozoidná bunka splynie "
        "s centrálnym jadrom zárodočného mieška za vzniku triploidného endospermu (3n), ktorý slúži ako vyživovacie pletivo. Nahosemenné rastliny majú jednoduché oplodnenie (a, c)."
    ),
    33: (
        "Perigón (okvetie) je tvarovo a farebne nerozlíšený kvetný obal, kde chýba rozdelenie na zelený kalich a pestrú korunu (a, e). "
        "Je zložený z rovnakých okvetných lístkov (tepala), ktoré plnia súčasne ochrannú funkciu aj funkciu lákania opeľovačov (typické pre jednoklíčnolistové rastliny ako tulipán) (f). "
        "Rozlíšený kvetný obal sa skladá z kalicha (calyx) a koruny (corolla) (c, d, h)."
    ),
    34: (
        "Gynaeceum predstavuje súbor všetkých samičích pohlavných orgánov v kvete semenných rastlín (f). "
        "Je tvorené jedným alebo viacerými plodolistami (karpelmi) (c), ktoré u krytosemenných rastlín zrastajú a vytvárajú piestik tvorený bliznou, čnelkou a semenníkom (g). "
        "Tyčinky predstavujú samčie pohlavné orgány (androeceum) (d, e)."
    ),
    35: (
        "Katabolické procesy (disimilácia) sú rozkladné biochemické reakcie, pri ktorých sa zložité organické zlúčeniny štiepia a oxidujú na jednoduchšie molekuly, "
        "pričom sa uvoľňuje energia uložená v chemických väzbách (g). V rastlinách sem patrí rozklad sacharidov (glykolýza), rozklad bielkovín a aminokyselín "
        "a aeróbne dýchanie, pri ktorom sa glukóza oxiduje na CO2 a H2O za zisku ATP (a, c, e, h). Vznik asimilátov fotosyntézou je anabolický proces (b, d)."
    ),
    36: (
        "Metabolické procesy spojené so spotrebou voľnej energie sa označujú ako endergonické reakcie a sú podstatou anabolizmu (asimilačných procesov) (a, b, f). "
        "Typickým rastlinným anabolickým dejom je fotosyntéza, kde sa svetelná energia využíva na endergonickú syntézu energeticky bohatej glukózy z anorganických molekúl CO2 a vody (e, h). "
        "Disimilačné procesy a dýchanie sú naopak exergonické a energiu uvoľňujú (c, d, g)."
    ),
    37: (
        "Pri katabolických procesoch dochádza k postupnému odbúravaniu a enzymatickej oxidácii organických látok – predovšetkým cukrov a tukov – "
        "na jednoduché nízkoenergetické produkty, vodu a oxid uhličitý, pričom sa uvoľňuje energia (a, b, f). Tieto reakcie sú katalyzované špecifickými enzýmami (d). "
        "Podľa oficiálneho kľúča testovnice UPJŠ LF sú v tejto otázke označené možnosti a, b, d, f."
    ),
    38: (
        "Bunkové dýchanie (aeróbna disimilácia) je základný katabolický dej, pri ktorom sa oxidáciou organických substrátov uvoľňuje energia viazaná do ATP (b). "
        "V kľúči testovnice UPJŠ LF sú priradené možnosti b, g, h, odrážajúce celkovú energetickú bilanciu bunkového metabolizmu, kde dýchanie poskytuje energiu pre asimiláciu a syntézu nových látok. "
        "Fotosyntéza je proces primárne svetelnú energiu viažuci do chemických väzieb (a)."
    ),
    39: (
        "Autotrofné organizmy syntetizujú organické látky z anorganického uhlíka (CO2), a preto plnia v ekosystémoch rolu primárnych producentov organickej hmoty (d). "
        "Zaraďujeme sem zelené rastliny (e), fotosyntetizujúce (aj chemosyntetizujúce) baktérie (b) a tiež poloparazitické rastliny s funkčným chlorofylom (napr. imelo) (h). "
        "Konzumenty, saprofyty a huby sú heterotrofné a odkázané na príjem hotových organických látok (a, c, f, g)."
    ),
    40: (
        "Mixotrofia je výživový spôsob kombinujúci fotosyntézu (autotrofiu) s príjmom organických dusíkatých látok (heterotrofiu); typickým príkladom sú mäsožravé (karnivorné) rastliny (g). "
        "K mixotrofom patrí rosička (Drosera) (a), bublinatka (Utricularia) (b), tučnica (Pinguicula) (c) a mucholapka (Dionaea) (d), ktoré lovom hmyzu kompenzujú nedostatok dusíka v pôde. "
        "Imelo je hemiparazit čerpajúci minerálne roztoky (e) a kukučina je nezelený holoparazit (f)."
    ),
    41: (
        "V mutualistickej symbióze medzi bôbovitými rastlinami a hľuzkovými baktériami rodu Rhizobium poskytujú rastliny baktériám produkty fotosyntézy – sacharidy (d), "
        "ktoré slúžia ako primárny zdroj energie a uhlíka pre bakteriálny metabolizmus. Baktérie na oplátku fixujú vzdušný dusík (N2) a premieňajú ho na amónne ióny, ktoré rastlina využíva na syntézu bielkovín."
    ),
    42: (
        "Prvou fázou biologickej oxidácie sacharidov je glykolýza, ktorá prebieha v cytozole (cytoplazme) buniek za anaeróbnych podmienok (b, f). "
        "Predstavuje sériu enzymatických reakcií, pri ktorých sa šesťuhlíkatá molekula glukózy štiepi na dve trojuhlíkaté molekuly kyseliny pyrohroznovej (pyruvátu) (d, h). "
        "Reakcie v mitochondriách (Krebsov cyklus, dýchací reťazec) predstavujú až nadväzujúce fázy biologickej oxidácie (a, c)."
    ),
    43: (
        "Glykolýza je anaeróbny katabolický proces neúplnej oxidácie glukózy na pyruvát (kyselinu pyrohroznovú) (b, c, h). "
        "Počiatočná investícia 2 ATP je kompenzovaná substrátovou fosforyláciou za vzniku 4 ATP, čo prináša čistý energetický zisk 2 molekuly ATP a 2 NADH na molekulu glukózy (f). "
        "Úplná oxidácia s výťažkom cez 30 ATP nastáva až pri aeróbnom dýchaní v mitochondriách (a, e)."
    ),
    44: (
        "Haustóriá sú anatomicky a funkčne modifikované korene, ktorými parazitické rastliny (holoparazity) a poloparazitické rastliny (hemiparazity) prenikajú do vodivých pletív hostiteľa (b, e, g). "
        "Poloparazity sa pripájajú k drevnej časti (xylému) a odčerpávajú vodu a minerály, kým holoparazity prenikajú do floému a berú hotové asimiláty. "
        "Živočíchy ani mäsožravé rastliny haustóriá nemajú (c, d)."
    ),
    45: (
        "Baktérie sa vyznačujú najvyššou metabolickou plasticitou v živej prírode; podľa zdroja uhlíka môžu byť autotrofné (využívajúce anorganický CO2) aj heterotrofné (využívajúce organické látky) (e, f). "
        "Podľa primárneho zdroja energie sa delia na fototrofné (využívajúce svetelné kvantá) a chemotrofné (získavajúce energiu oxidáciou chemických väzieb) (g, h). "
        "Preto nie sú obmedzené len na autotrofný (c) alebo len heterotrofný spôsob výživy (a)."
    ),
    46: (
        "Fylogeneticky najstarším mechanizmom syntézy organických látok na Zemi je chemosyntéza (chemoautotrofia), ktorá vznikla v anaeróbnych podmienkach pred fotosyntézou (c, h). "
        "Chemoautotrofné baktérie (sírové, nitrifikačné, metanogénne) získavajú energiu na fixáciu CO2 z oxidácie redukovaných anorganických látok (H2S, NH3, Fe2+). "
        "V odbornej terminológii testovnice sa tento prvotný spôsob syntézy označuje aj ako prototrofia (a)."
    ),
    47: (
        "Mykoríza je obojstranne prospešná symbióza medzi hubovými hýfami a koreňovým systémom cievnatých rastlín. "
        "Fotosyntetizujúca rastlina zásobuje heterotrofnú hubu organickými látkami – hotovými asimilátmi, predovšetkým sacharidmi vo forme glukózy a sacharózy (d, h). "
        "Huba na oplátku zabezpečuje príjem vody a ťažko dostupných minerálov (najmä fosforu)."
    ),
    48: (
        "Mixotrofia je kombinovaný spôsob výživy spájajúci autotrofnú fotosyntézu s heterotrofným príjmom organických látok (a). "
        "Je typická pre mäsožravé rastliny, ktoré fotosyntetizujú, ale v pôdach chudobných na dusík trávia telá ulovených živočíchov (g, h). "
        "V kľúči testovnice UPJŠ LF je k mixotrofom priradené aj imelo biele (b) z dôvodu kombinácie vlastnej fotosyntézy s čerpaním živín z hostiteľa."
    ),
    49: (
        "Poloparazity (hemiparazity) sú zelené rastliny obsahujúce funkčné chloroplasty, ktoré si organické látky syntetizujú fotosyntézou, ale vodu a minerálne živiny čerpajú haustóriami z hostiteľa (d). "
        "Typickým poloparazitom našich drevín je imelo biele (Viscum album) (c). Úplné nezelené parazity (holoparazity ako kukučina) odoberajú aj organické látky z floému (e, g), kým saprofyty žijú z mŕtvej hmoty (a)."
    )
}

# Load batch_4.json
with open('scripts/bio_batches/batch_4.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Total questions loaded: {len(questions)}")
assert len(questions) == 50, f"Expected 50 questions, got {len(questions)}"

# Replace explanations
for i, q in enumerate(questions):
    assert i in explanations, f"Missing explanation for index {i}"
    q['explanation'] = explanations[i]

# Write to batch_4_explained.json
output_path = 'scripts/bio_batches/batch_4_explained.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully wrote 50 explained questions to {output_path}")

# Verification
with open(output_path, 'r', encoding='utf-8') as f:
    verified = json.load(f)

print(f"Verified count: {len(verified)}")
for i in range(2):
    print(f"\n--- Question {i+1} ({verified[i]['content'][:40]}...) ---")
    print(f"Explanation: {verified[i]['explanation']}")
