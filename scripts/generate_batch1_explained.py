# -*- coding: utf-8 -*-
import json

explanations = {
    1: "Cytológia (bunková biológia) je veda skúmajúca bunku ako základnú štruktúrnu a funkčnú jednotku živých sústav, jej tvar, štruktúru organel a životné deje na bunkovej úrovni (c, e, g). Štúdiom tkanív sa zaoberá histológia (b), mikroorganizmami mikrobiológia (d), vírusmi virológia (f) a skúmanie na úrovni molekúl patrí do molekulárnej biológie a biochémie (a, h).",
    
    2: "Prokaryotická bunka obsahuje plazmatickú membránu, 70S ribozómy, nukleoid (kruhovú molekulu DNA bez jadrového obalu) a fotosyntetizujúce sinice majú v cytoplazme tylakoidy (a, c, d, e). Nemá pravé chloroplasty ani kompartmentovaný vnútorný priestor (b, g), jej DNA nie je lineárna (f) a neobsahuje párové (homologické) chromozómy, pretože je haploidná (h).",
    
    3: "Prokaryotické bunky nemajú membránou ohraničené organely (mitochondrie, plastidy, diktyozómy) ani nemembránové štruktúry eukaryotov ako jadierko a centriol (a, d, f, g, h), a ich cytoplazma nie je členená membránami na kompartmenty (b). Naopak, univerzálnymi štruktúrami prokaryotickej bunky sú cytoplazmatická membrána a prokaryotické ribozómy (c, e).",
    
    4: "Prokaryoty nemajú mitochondrie, preto sú dýchacie enzýmy a elektrónový transportný reťazec lokalizované priamo v cytoplazmatickej membráne alebo jej vchlípeninách, kde dochádza k aeróbnej respirácii a tvorbe ATP (e). Ribozómy zabezpečujú transláciu, tylakoidy fotosyntézu a mitochondrie či diktyozómy sa v prokaryotických bunkách nevyskytujú.",
    
    5: "Bunka predstavuje základnú morfologickú a fyziologickú jednotku schopnú samostatnej existencie, metabolizmu, rastu a autoreprodukcie (b). Vírusy sú nebunkové formy neschopné samostatného života bez hostiteľskej bunky (a), biopolyméry sú len stavebné makromolekuly (d) a mnohobunkové organizmy či populácie predstavujú vyššie úrovne organizácie živej hmoty.",
    
    6: "Vírusy sú nebunkové častice a z hľadiska organizácie najjednoduchšie živé sústavy na molekulárnej úrovni, ktoré uchovávajú vlastnú genetickú informáciu vo forme DNA alebo RNA (b, c, e). Nemajú vlastný metabolický aparát a sú obligátnymi vnútrobunkovými (nie extracelulárnymi) parazitmi, ktorých rozmnožovanie je striktne viazané na hostiteľskú bunku (g, h); nie sú schopné samostatnej autoreprodukcie bez hostiteľa (f) ani to nie sú jednobunkové organizmy (d).",
    
    7: "Podľa vnútornej organizácie a prítomnosti membránou ohraničeného pravého jadra rozdeľujeme všetky bunky do dvoch základných typov: prokaryotické a eukaryotické (d). Rozdelenie na rastlinné a živočíšne je podkategóriou eukaryotov (a) a rozdelenie na somatické a gaméty zohľadňuje ich reprodukčnú funkciu v mnohobunkovom tele (h).",
    
    8: "Indivíduá vyššieho rádu (superorganizmy) sú obligátne spoločenstvá jedincov, typické pre sociálny hmyz (včely, mravce, termity), ktoré nemôžu trvalo existovať samostatne (a, d). Jednotlivé kasty vykazujú trvalú a nezameniteľnú morfologicko-anatomickú a funkčnú špecializáciu (e, g), preto medzi ne nepatria voľné svorky vlkov (b) ani skupiny so zameniteľnou deľbou práce (f).",
    
    9: "Bunky rovnakého pôvodu, štruktúry a funkcie tvoria u rastlín pletivá a u mnohobunkových živočíchov tkanivá (c, f). Z pletív a tkanív sa následne skladajú orgány (a), zatiaľ čo indivíduá vyššieho rádu predstavujú koloniálne spoločenstvá celých organizmov (e).",
    
    10: "Základnú kostru biomembrány tvorí fluidná dvojvrstva fosfolipidov (amfipatických lipidov), do ktorej sú ponorené integrálne a periférne bielkoviny (c, f). Cytoplazmatická membrána nie je tvorená bielkovinovou dvojvrstvou (a, h) ani celulózou (b), a cytosól spolu s matrix tvorí tekutý obsah cytoplazmy (d, e).",
    
    11: "K základným povrchovým štruktúram eukaryotickej bunky patrí univerzálna cytoplazmatická membrána (plazmaléma) a u rastlín a húb aj tuhá bunková stena (a, e, f). Karyoléma je vnútorná dvojitá membrána ohraničujúca jadro (b, h), kým pelikula, kutikula a slizové puzdrá sú špecializované alebo bakteriálne útvary (c, d, g).",
    
    12: "Plazmaléma tvorí základný selektívne permeabilný bunkový povrch, u prokaryotov predstavuje zvyčajne jedinú biomembránu a pomocou receptorových proteínov zachytáva signály z okolia (a, b, c, e, f). Karyoléma je obal jadra (d), metabolické vnútrobunkové prostredie zabezpečuje cytoplazma (g) a primárnu mechanickú ochranu bunky plní tuhá bunková stena (h).",
    
    13: "Biologické membrány sú tvorené súvislou dvojvrstvou amfipatických fosfolipidov, v ktorej sú mozaikovite rozmiestnené molekuly integrálnych a periférnych bielkovín (b, e, h). Membrány netvoria bielkovinovú dvojvrstvu (a, d, f) a sacharidy sa v nich vyskytujú iba naviazané na lipidy a proteíny na vonkajšej strane (glykokalyx), netvoria samostatnú vrstvu (c).",
    
    14: "Eukaryotické bunky sa vyznačujú prítomnosťou pravého jadra s dvojitou membránou (karyolémou) a prítomnosťou membránových organel, ktoré rozčleňujú vnútro bunky na samostatné funkčné kompartmenty (a, c, g). Chromozómy eukaryotov sú lineárne (nie kruhové) (e), bunky sú rádovo väčšie (f) a genetický materiál majú oba bunkové typy (h).",
    
    15: "Živočíšne bunky nemajú celulózovú bunkovú stenu (f), ich hlavným lytickým aparátom sú lyzozómy s hydrolytickými enzýmami (b) a obsahujú špecifické fibrilárne štruktúry ako myofibrily či neurofibrily (h). Cytoplazmatickú membránu majú oba typy buniek (a), pričom veľké centrálne vakuoly s tonoplastom a intercelulárne plazmodezmy sú typické pre rastlinné bunky (c, e, g).",
    
    16: "Cytoskelet je dynamická trojrozmerná proteínová sieť, ktorá zaisťuje priestorové rozmiestnenie organel, mechanickú oporu bunky a zúčastňuje sa na endocytových procesoch (pinocytóze a fagocytóze) prestavbou mikrofilamentov (a, d, e, h). Cytoskelet nie je statický (b), netvoria ho nukleoproteíny (g) a nepodieľa sa na pasívnych dejoch ako difúzia a osmóza (c, f).",
    
    17: "Cytoskelet patrí k fibrilárnym nemembránovým štruktúram a tvorí dynamickú kostru bunky zloženú z troch hlavných zložiek: mikrotubulov, mikrofilamentov a intermediárnych filamentov (c, e, g). Je živou súčasťou bunky a podieľa sa na všetkých formách bunkových pohybov vrátane delenia bunky a toku cytoplazmy (b), pričom nie je statický ani nukleoproteínový (d, h).",
    
    18: "Drsné endoplazmatické retikulum nesie na povrchu membrán ribozómy, vďaka čomu je centrom syntézy bielkovín (proteínov) určených na export alebo do membrán a lyzozómov (d, e). Súčasne slúži ako systém membránových cisterien zabezpečujúci vnútrobunkový a medzibunkový transport látok (f, g), zatiaľ čo syntéza lipidov a steroidov (vrátane vitamínu D) je úlohou hladkého retikula (a, b).",
    
    19: "Hladké endoplazmatické retikulum nemá na svojich membránach ribozómy (a) a zabezpečuje syntézu lipidov, fosfolipidov a steroidných látok vrátane prekurzorov vitamínu D a transport molekúl v bunke (c, d, h). Proteosyntéza prebieha na drsnom retikule (g), hydrolytické enzýmy patria do lyzozómov (e) a jeho jemná tubulárna štruktúra je viditeľná len elektrónovým mikroskopom (b).",
    
    20: "Lyzozómy sú vezikuly naplnené kyslými hydrolytickými enzýmami (hydrolázami), ktoré štiepia nepotrebné bunkové štruktúry pri autofágii a cudzorodý materiál pohltený endocytózou pri vnútrobunkovom trávení (a, b, g, h). Neobsahujú polymerázy (c) ani neslúžia na posttranslačnú úpravu a sekréciu látok von z bunky, čo vykonáva Golgiho aparát (d, e).",
    
    21: "Mitochondrie sú semiautonómne organely ohraničené dvoma biomembránami, prítomné výhradne v eukaryotických bunkách ako centrá bunkového dýchania a syntézy ATP (a, b, c, e). Ich počet odráža energetickú spotrebu daného bunkového typu (g); v prokaryotoch úplne chýbajú (d) a vyskytujú sa tak v živočíšnych, ako aj v rastlinných bunkách (h).",
    
    22: "Bunkové jadro eukaryotov (nucleus, karyon) uchováva jadrovú DNA komplexovanú s histónmi vo forme chromatínu a riadi životné procesy v bunke (a, b, e). Jeho obal (karyoléma) tvoria dve rovnobežné biomembrány s pórmi (f, h), zatiaľ čo plazmaléma obaľuje celú bunku (g) a jadrové chromozómy eukaryotov sú lineárne, nie kruhové (d).",
    
    23: "Ribozómy sú submikroskopické nemembránové štruktúry s veľkosťou okolo 20–30 nm, ktoré je možné pozorovať výlučne elektrónovým mikroskopom (c, d, e). Ide o ribonukleoproteínové častice zložené z molekúl rRNA a bielkovín (h), pričom neobsahujú DNA (g) a nepripájajú sa na hladké, ale na drsné endoplazmatické retikulum (f).",
    
    24: "Mitochondrie sú ohraničené dvoma membránami a majú semiautonómny charakter – v matrix nesú vlastnú kruhovú DNA a ribozómy, čo im umožňuje syntézu niektorých vlastných bielkovín (b, c, d). V matrix obsahujú enzýmy Krebsovho cyklu a na kristách vnútornej membrány komponenty dýchacieho reťazca a ATP syntázu (e, h); bunková šťava sa nachádza vo vakuolách (f) a kostru bunky tvorí cytoskelet (g).",
    
    25: "Mitochondrie majú presne dve biomembrány: vonkajšiu hladkú membránu a vnútornú membránu selektívne priepustnú a zriasnenú do záhybov – krist (c). Počet membrán je stály a nemení sa podľa energetických nárokov ani bunkového typu (d, g).",
    
    26: "V Golgiho aparáte prebiehajú posttranslačné modifikácie proteínov a lipidov prijatých z ER a ich balenie do sekrečných vezikúl na vylúčenie z bunky (b). Dochádza tu tiež k syntéze pektínov a polysacharidov pre bunkovú stenu rastlín (d) a k odškrcovaniu primárnych lyzozómov (c); degradáciu vykonávajú lyzozómy (a) a bunkové oxidácie prebiehajú v mitochondriách (e, g).",
    
    27: "Diktyozómy sú súbory sploštených membránových cisterien, ktoré spoločne tvoria Golgiho aparát typický pre eukaryotické bunky (b, f). Prokaryoty diktyozómy nemajú (e) a nie sú súčasťou chloroplastov, lyzozómov ani mitochondrií.",
    
    28: "Nukleolus (jadierko) je nemembránová štruktúra lokalizovaná vnútri eukaryotického jadra, kde dochádza k transkripcii rRNA a syntéze ribozomálnych podjednotiek (d, e). Je to dynamická štruktúra, ktorá počas profázy jadrového delenia mizne a rekonštituuje sa v telofáze (f); nemá vlastnú membránu a v prokaryotických bunkách chýba (a, g, h).",
    
    29: "Jadro je mikroskopická riadiaca a reprodukčná organela obsahujúca genetickú informáciu vo forme chromatínu (a, c, d). Vyskytuje sa vo všetkých eukaryotických bunkách okrem niektorých plne diferencovaných špecializovaných buniek, akými sú zrelé erytrocyty cicavcov (h); centriol leží v cytoplazme mimo jadra (b) a jadro je dobre viditeľné v bežnom svetelnom mikroskope (g).",
    
    30: "Bunkové štruktúry a organely obalené jednoduchou alebo dvojitou biomembránou (jadro, mitochondrie, plastidy, ER, Golgiho aparát, vakuoly, lyzozómy) označujeme ako membránové organely alebo membránové štruktúry (c, f). Vytvárajú bunkové kompartmenty, na rozdiel od nemembránových štruktúr, ako sú ribozómy, centrioly či cytoskelet.",
    
    31: "Medzi nemembránové štruktúry patria ribozómy (ribonukleoproteíny), cytoskelet (bielkovinové vlákna), centriol, jadierko a bakteriálny nukleoid, ktoré nemajú biomembránové ohraničenie (a, c, e, f, g). Naopak, lyzozómy, mitochondrie a vakuoly sú typické membránové organely (b, d, h).",
    
    32: "Membránovými organelami sú Golgiho aparát, lyzozómy a rastlinné vakuoly, pretože sú ohraničené fosfolipidovou biomembránou (e, g, h). Centrioly, centrozómy, ribozómy, chromozómy a jadierka sú štruktúry nemembránového charakteru (a, b, c, d, f).",
    
    33: "Mitotický aparát zabezpečujúci rozchod sesterských chromatíd pri delení bunky pozostáva z deliaceho vretienka tvoreného mikrotubulmi, páru centriolov (u živočíchov) a lúčovitej astrosféry vybiehajúcej z centrozómov (c, d, f). Chromozómy a centroméry sú štruktúry prenášaného genetického materiálu, nie samotného deliaceho aparátu (a, b, g).",
    
    34: "Chromozómy predstavujú maximálne kondenzované nukleoproteínové vlákna (DNA a históny), ktoré sa stávajú svetelno-mikroskopicky viditeľnými iba počas bunkového delenia (a, e). Skladajú sa z dvoch ramien spojených primárnym zúžením – centromérou (f) a v metafáze mitózy obsahujú dve geneticky identické sesterské chromatídy (g); v interfáze sú despiralizované (b) a v eukaryotickom jadre sú vždy lineárne (h).",
    
    35: "Voda tvorí v priemere okolo 65 % celkovej hmotnosti eukaryotických buniek a jej zastúpenie priamo závisí od veku bunky, metabolickej aktivity daného orgánu a hydratácie prostredia (a, c, d, e). Obsah vody v mladých tkanivách je vyšší než v starších (f, g) a hodnota 10–40 % je výnimočná (napr. v semenách) (h).",
    
    36: "Endocytóza je aktívny transport makromolekúl a častíc do vnútra bunky spojený so spotrebou energie ATP a dynamickou štrukturálnou prestavbou plazmatickej membrány (b, d). Zahŕňa pohlcovanie pevných častíc prostredníctvom panôžok – fagocytózu – aj príjem tekutých kvapôčok mikrovliačkami a vezikulami – pinocytózu (a, h); transport látok z bunky von sa nazýva exocytóza (e).",
    
    37: "V hypertonickom roztoku dochádza k osmotickému úniku vody z vakuoly a cytoplazmy rastlinnej bunky do prostredia s vyššou koncentráciou rozpustených látok (a, g). Následkom straty turgoru sa zmenšuje objem protoplastu a plazmatická membrána sa oddeľuje od pevnej bunkovej steny – prebieha plazmolýza (d, h).",
    
    38: "Živočíšna bunka v prostredí s nižšou koncentráciou osmoticky aktívnych látok (napr. v hypotonickom roztoku či destilovanej vode) osmoticky nasáva vodu, napúča a zväčšuje svoj objem (f, g). Keďže nemá pevnú bunkovú stenu, nadmerný hydrostatický tlak spôsobí jej prasknutie – plazmoptýzu (pri erytrocytoch osmotickú lýzu) (b, c).",
    
    39: "V hypertonickom prostredí voda osmoticky uniká z bunky von v smere koncentračného spádu rozpustených látok (c). Živočíšna bunka stráca tekutinu, zmenšuje svoj vnútorný objem a zmršťuje sa (podlieha krenácii) (a, h); pojem plazmolýza je viazaný výlučne na bunky s pevnou bunkovou stenou (d) a plazmoptýza nastáva v hypotonickom prostredí (e).",
    
    40: "Jednoduchá difúzia aj osmóza sú formy pasívneho transportu, ktoré prebiehajú spontánne v smere koncentračného gradientu bez akejkoľvek spotreby metabolickej energie (ATP) (c, f, g, h). Neprebiehajú proti koncentračnému gradientu (d) a na rozdiel od endocytózy pri nich nedochádza k štrukturálnej prestavbe membrány (e).",
    
    41: "Základnou semipermeabilnou bunkovou štruktúrou riadiacou transport a výmenu látok medzi bunkou a vonkajším prostredím je cytoplazmatická membrána, synonymne nazývaná plazmaléma alebo plazmatická membrána (b, d, f). Bunková stena je plne permeabilná (c), jadrová membrána ohraničuje jadro (a) a cytoskelet tvorí vnútornú oporu cytoplazmy (h).",
    
    42: "Pasívny transport (jednoduchá difúzia, osmóza a sprostredkovaná difúzia) prebieha výlučne v smere koncentračného spádu danej látky bez spotreby chemickej energie ATP (a, d, e, f). Týmto spôsobom prechádzajú cez lipidovú dvojvrstvu malé nepolárne molekuly, plyny (O2, CO2), etanol a molekuly vody (h), zatiaľ čo transport proti spádu je aktívny proces (b, c).",
    
    43: "Hypotonické prostredie má nižšiu koncentráciu osmoticky aktívnych látok v porovnaní s bunkovým obsahom, čo podmieňuje osmotické nasávanie vody do bunky (a, g, h). V živočíšnych bunkách spôsobuje takéto nadmerné nasávanie vody prasknutie bunky – plazmoptýzu, respektíve lýzu červených krviniek (d, e); plazmolýzu vyvoláva hypertonické prostredie (c, f).",
    
    44: "Transportné membránové bielkoviny (kanály a transportéry) špecificky viažu a prenášajú vybrané polárne molekuly alebo ióny cez hydrofóbnu zónu membrány (c, d). Uplatňujú sa pri facilitovanej (sprostredkovanej) difúzii v smere gradientu aj pri primárnom a sekundárnom aktívnom transporte (h); nie sú univerzálne pre všetky látky (b) a neprenášajú látky vezikulami pri endocytóze (a, e).",
    
    45: "Úloha žiada vybrať biologicky nepravdivé výroky. Cytoskelet sa podieľa na mnohých typoch pohybov vo všetkých eukaryotoch (a), mikrofilamenty tvorí bielkovina aktín (nie pektín) (d), deliace vretienko sa vytvára medzi centrozómami (nie centromérami) (e), plastidy sú nadradenou kategóriou chloroplastov (f), mikrofilamenty aj mikrotubuly plnia komplexné mechanické úlohy (g) a tylakoidy sú štruktúry obsahujúce molekuly chlorofylu (h). Naopak, výroky b a c sú vecne správne.",
    
    46: "Prostou pasívnou difúziou cez fosfolipidovú dvojvrstvu prechádzajú dýchacie plyny, etanol a voda, a facilitovanou difúziou cez kanály aj vybrané ióny (c, d, e, f, g). Difúzia nie je univerzálna pre všetky molekuly (makromolekuly ňou neprechádzajú) (a, b) a zo svojej fyzikálnej podstaty nikdy nemôže prebiehať proti koncentračnému spádu (h).",
    
    47: "Rýchlosť prostej difúzie sa riadi Fickovým zákonom a je priamo závislá od strmosti koncentračného spádu a od teploty prostredia, ktorá zvyšuje kinetickú energiu molekúl (d, e). Keďže ide o pasívny nestrukturálny proces bez transportných proteínov, nezávisí od zásob ATP (b), proteínových prenášačov (c) ani od prestavby cytoplazmatickej membrány (a).",
    
    48: "Bunka tvorí pseudopódie (panôžky) prostredníctvom riadenej polymerizácie aktínových mikrofilamentov cytoskeletu (b, e). Využíva ich pri fagocytóze na obklopenie pevnej častice, ktorú následne uzatvára do vznikajúcej fagocytovej vakuoly (c, f); pri pinocytóze panôžky nevznikajú (a) a osmóza je pasívny transport vody (d).",
    
    49: "Aktívny transport prebieha prostredníctvom špecifických membránových transportných bielkovín (púmp) spravidla proti smeru koncentračného spádu za spotreby energie ATP (e, h). Zabezpečuje presun iónov Ca2+ (d) a asymetrický transport iónov sodnodraselnou pumpou (Na+/K+-ATPáza), ktorá čerpá tri ióny Na+ von z bunky a dva ióny K+ dovnútra (f, g); voda a plyny prechádzajú pasívne (a, b).",
    
    50: "Bunkový cyklus je geneticky naprogramovaný proces zahŕňajúci prípravné interfázové fázy (postmitotickú G1 a predmitotickú G2) a mitotickú M-fázu (b, f). Je prísne riadený kontrolnými bodmi bunky, z ktorých kľúčový je hlavný kontrolný uzol v G1-fáze, a môže byť deregulovaný napr. onkogénnymi vírusmi vedúcimi k nekontrolovanému deleniu (d, e); celkový čas cyklu sa nazýva generačná (nie regeneračná) doba (a)."
}

with open('scripts/bio_batches/batch_1.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

assert len(questions) == 50, f"Expected 50 questions, found {len(questions)}"
assert len(explanations) == 50, f"Expected 50 explanations, found {len(explanations)}"

for idx, q in enumerate(questions):
    q_num = idx + 1
    assert q_num in explanations, f"Missing explanation for Q{q_num}"
    q['explanation'] = explanations[q_num]

with open('scripts/bio_batches/batch_1_explained.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Successfully written batch_1_explained.json with 50 explained questions.")
