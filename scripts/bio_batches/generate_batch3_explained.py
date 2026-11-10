import json

# Read batch_3.json
with open('scripts/bio_batches/batch_3.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

assert len(questions) == 50, f"Expected 50 questions, got {len(questions)}"

explanations = [
    # 101
    "Tonoplast je jednoduchá semipermeabilná (polopriepustná) biomembrána oddeľujúca vnútro rastlinnej vakuoly (bunkovú šťavu) od cytoplazmy, čím obaľuje vakuoly a zohráva kľúčovú úlohu v osmoregulácii. Nie je voľne priepustná a nenachádza sa na povrchu leukoplastov (ktoré majú dvojitú membránu), lyzozómov ani transportných vezikúl.",
    
    # 102
    "V strome (základnej hmote) chloroplastov sa nachádza vnútorný tylakoidný membránový systém s fotosyntetickými pigmentmi vrátane karotenoidov, vlastná semiautonómna kruhová DNA (cpDNA) a plastidové ribozómy prokaryotického typu (70S). Chromatín a lineárna DNA sú lokalizované v bunkovom jadre, hydrolytické enzýmy v lyzozómoch a bunková šťava vo vakuolách.",
    
    # 103
    "Základnými postulátmi bunkovej teórie (Schleiden, Schwann, Virchow) je, že bunka je základnou štrukturálnou a funkčnou jednotkou všetkých rastlinných a živočíšnych organizmov, a princíp, že každá bunka vzniká výlučne delením z už existujúcej bunky („omnis cellula e cellula“). Najjednoduchšími živými sústavami sú nebunkové formy života (vírusy) a bunky nie sú tvorené prevažne anorganickými makromolekulami.",
    
    # 104
    "Prvú ucelenú evolučnú teóriu predostrel francúzsky prírodovedec Jean-Baptiste Lamarck vo svojom diele Philosophie zoologique (1809), v ktorej predpokladal dedenie získaných vlastností a vnútornú snahu organizmov o zdokonaľovanie. Louis Pasteur vyvrátil abiogenézu, Carl Linné zaviedol binomickú nomenklatúru a William Harvey objavil systém krvného obehu.",
    
    # 105
    "Louis Pasteur definitívne vyvrátil teóriu samoplodenia (abiogenézy) mikroskopických organizmov pomocou experimentov s labutími bankami, a Theodor Schwann patrí spolu s Schleidenom k zakladateľom bunkovej teórie. Biopolyméry (bielkoviny a polysacharidy) majú v bunke zásadnú stavebnú funkciu; zakladateľom modernej systematiky bol Carl Linné (nie Schleiden).",
    
    # 106
    "Bunkovú teóriu formulovali v rokoch 1838–1839 nemecký botanik Matthias Jacob Schleiden a zoológ Theodor Schwann, pričom významný predstih v jej formulácii a pozorovaní bunkových štruktúr mal český vedec Jan Evangelista Purkyně (prednáška v Prahe 1837). Robert Hooke iba zaviedol pojem bunka pri mikroskopovaní mŕtveho korku a Antoni van Leeuwenhoek pozoroval voľné jednobunkové organizmy.",
    
    # 107
    "Správnou odpoveďou v testovnici UPJŠ LF je možnosť E (J. E. Purkyně). V širšom biologickom kontexte položil základy modernej anatómie Andreas Vesalius (1543), kým Purkyně rozvinul histológiu a fyziológiu; Galénos s Aristotelom predstavujú starovekú náuku a Harvey objaviteľský prínos pre fyziológiu obehu.",
    
    # 108
    "Fyziologické vedy skúmajú funkcie, životné procesy a činnosť jednotlivých orgánov a systémov živých tiel; podľa skúmaných objektov zahŕňajú fyziológiu rastlín, živočíchov a fyziológiu človeka. Histológia (veda o tkanivách) a embryológia (náuka o ontogenéze zárodku) patria medzi vedy morfologické, zamerané na štruktúru, nie primárne na funkciu.",
    
    # 109
    "Parazitológia je biologická disciplína, ktorá skúma cudzopasné organizmy (vírusy, baktérie, parazitické prvoky a červy) a definuje biologické zákonitosti zložitých vzťahov medzi parazitom a hostiteľom. Ekológia skúma celkové vzťahy organizmov k vonkajšiemu prostrediu, etológia študuje vrodené a naučené správanie a genetika sa zaoberá zákonitosťami dedičnosti a premenlivosti.",
    
    # 110
    "Model priestorovej štruktúry DNA ako pravotočivej dvojzávitnice a molekulárny mechanizmus prenosu genetickej informácie komplementaritou báz objasnili v roku 1953 americký genetik James Watson a britský biofyzik Francis Crick. V roku 1944 Avery, MacLeod a McCarty experimentálne dokázali transformáciu genetickej informácie prostredníctvom DNA a Mendel svoje zákony publikoval v roku 1866.",
    
    # 111
    "Voda tvorí hlavnú kvapalnú zložku bunky, v ktorej pôsobí ako univerzálne polárne rozpúšťadlo a substrátové médium vytvárajúce prostredie pre priebeh biochemických reakcií, pričom vďaka vysokej tepelnej kapacite zohráva kľúčovú úlohu v tepelnom hospodárení. Voda neposkytuje žiadnu metabolicky využiteľnú energiu (ako sacharidy či lipidy) a netvorí monomérnu stavebnú jednotku biopolymérov.",
    
    # 112
    "Lipidy predstavujú energeticky najvýdatnejší a najhospodárnejší zdroj energie (poskytujú až 38 kJ/g), sú kľúčovou štrukturálnou zložkou biomembrán (fosfolipidy, cholesterol), tvoria ochranné vrstvy (vosky na kutikule rastlín) a pôsobia regulačne (steroidné hormóny, lipofilné vitamíny A, D, E, K). Katalytickú funkciu a špecifickú obrannú funkciu protilátok zabezpečujú bielkoviny, nie lipidy.",
    
    # 113
    "Základnými stavebnými monomérmi bielkovín sú proteinogénne L-alfa-aminokyseliny, ktoré sa navzájom spájajú do polypeptidových reťazcov. Nukleotidy sú stavebnými jednotkami nukleových kyselín, monosacharidy tvoria polysacharidy a peptidy predstavujú už zreťazené polyméry aminokyselín.",
    
    # 114
    "V primárnej štruktúre bielkovín sú jednotlivé aminokyseliny pospájané kovalentnými peptidovými väzbami (-CO-NH-), ktoré vznikajú kondenzáciou alfa-karboxylovej a alfa-aminoskupiny dvoch aminokyselín. Esterové väzby sú prítomné v lipidoch, fosfodiesterové väzby prepájajú nukleotidy v nukleových kyselinách a vodíkové mostíky stabilizujú až vyššie (sekundárne a terciárne) štruktúry.",
    
    # 115
    "Bielkoviny majú mnohostranné biologické funkcie: fibrilárne bielkoviny (napr. kolagén, elastín, keratín) zabezpečujú mechanickú oporu a štruktúrnu funkciu buniek a tkanív, kým globulárne bielkoviny (enzýmy, hormóny, transportéry) vykonávajú metabolické funkcie. Informačnú funkciu v bunke plnia nukleové kyseliny a najhospodárnejším zdrojom energie sú lipidy.",
    
    # 116
    "Základnými monomérmi makromolekúl nukleových kyselín sú nukleotidy, konkrétne ribonukleotidy pri RNA a deoxyribonukleotidy pri DNA. Dusíkaté bázy, pentózy alebo nukleozidy sú len čiastkovými štruktúrnymi zložkami nukleotidov a samy osebe nie sú kompletnými monomérmi schopnými polymerizácie do polynukleotidového reťazca.",
    
    # 117
    "Nukleové kyseliny sú z chemického hľadiska makromolekulové biopolyméry tvorené dlhými lineárnymi reťazcami pospájaných nukleotidov, preto sa označujú ako polynukleotidy. Polypeptidy tvorené aminokyselinami sú bielkoviny a estery glycerolu s vyššími mastnými kyselinami sú acylglyceroly (tuky).",
    
    # 118
    "Pojmom mikroorganizmy sa označujú mikroskopické organizmy nepostihnuteľné voľným okom, ktorých štúdiom sa zaoberá mikrobiológia; patria sem všetky baktérie a archeóny, eukaryotické jednobunkovce a v širšom zmysle aj onkogénne vírusy. Nie sú obmedzené len na eukaryota (zahŕňajú prokaryota aj nebunkové formy) a voľným okom jednotlivé mikroorganizmy nie sú viditeľné.",
    
    # 119
    "Medzi prokaryotické organizmy (Prokaryota) patria domény baktérie (Bacteria) a archeóny (Archaea), ktoré tvoria špecifickú skupinu mikroorganizmov s jednoduchou bunkovou organizáciou bez jadrovej membrány a organel. Riasy a bičíkovce sú eukaryotické bunky s pravým jadrom a vírusy či bakteriofágy sú nebunkové formy života.",
    
    # 120
    "Medzi nebunkové formy života patria vírusy vrátane onkovírusov a bakteriofágov, ktoré fungujú ako striktné molekulárne vnútrobunkové parazity bez vlastného metabolizmu a bunkovej štruktúry. Sinice, spirily a spirochéty sú plnohodnotné prokaryotické bunky a erytrocyty sú špecializované diferencované bunky živočíšnych tkanív.",
    
    # 121
    "Vírusy sú nebunkové nukleoproteínové častice zložené z nukleovej kyseliny a bielkovinového obalu, ktoré sú schopné vyvolávať infekčné ochorenia v rôznych organizmoch. Nemajú vlastný metabolizmus ani aparát na tvorbu energie a proteínov, preto sú striktnými vnútrobunkovými parazitmi a nemožno ich radiť medzi prokaryota.",
    
    # 122
    "U človeka spôsobujú vírusy ochorenia ako besnota (Rhabdoviridae), vírusová žltačka (hepatitída A, B, C), chrípka (Orthomyxoviridae) a kiahne (varicella či variola). Tuberkulóza (Mycobacterium) a kvapavka (Neisseria) sú bakteriálneho pôvodu, krívačka a slintačka je primárne zoonóza hospodárskych zvierat a Downov syndróm je autozómová genetická porucha (trizómia 21).",
    
    # 123
    "Vírusy sa nerozmnožujú delením (mitózou, amitózou ani meiózou), ale replikujú sa výhradne vo vnútri živých hostiteľských buniek, kde využívajú ich translačný a enzymatický aparát; in vitro je ich množenie možné v bunkových kultúrach. Mimo živej hostiteľskej bunky sú metabolicky inertné a nie sú schopné reprodukcie.",
    
    # 124
    "Pôvodcom detskej obrny (poliomyelitídy) je poliovírus (ľudský enterovírus), ktorý predstavuje nebunkovú infekčnú nukleoproteínovú časticu tvorenú RNA a bielkovinovým kapsidom. Nejde o baktériu (Salmonella, Shigella a streptokoky sú baktérie vyvolávajúce iné ochorenia) ani o bakteriofág, ktorý napadá výlučne bakteriálne bunky.",
    
    # 125
    "Ochranný bielkovinový obal vírusu sa nazýva kapsid alebo bielkovinový plášť a je tvorený bielkovinovými podjednotkami nazývanými kapsoméry. Virión je označenie pre celú kompletnú infekčnú časticu vírusu, nukleoid je bakteriálny chromozóm a cysty či spóry sú pokojové štruktúry buniek.",
    
    # 126
    "Vírusy vyvolávajú u ľudí pestrú škálu infekčných ochorení, vrátane osýpok, bežnej nádchy (rhinovírusy), oparu (herpes simplex), AIDS (vírus HIV) a prostredníctvom transformácie buniek môžu zapríčiniť aj zhubné nádory (napr. HPV alebo EBV). Syfilis je bakteriálna spirochétová infekcia (Treponema pallidum) a mozaiková choroba je ochorenie rastlín.",
    
    # 127
    "Vírusy sa replikujú reprogramovaním vnútrobunkového aparátu hostiteľskej bunky, ktorá na základe vnesenej vírusovej genetickej informácie (s obsahom ribózy pri RNA alebo deoxyribózy pri DNA) syntetizuje nové virióny. Do živočíšnych buniek prenikajú často pinocytózou (endocytózou) či fúziou; mitóza, meióza ani pučanie ako formy bunkového delenia u vírusov neexistujú.",
    
    # 128
    "Vírusy sa od všetkých ostatných mikroorganizmov odlišujú svojou nebunkovou povahou, nanometrovými rozmermi (15–300 nm) a tým, že ich genetickú informáciu tvorí výhradne jeden typ nukleovej kyseliny (buď DNA, alebo RNA, nikdy nie obe súčasne). Bunkové mikroorganizmy majú mikrometrové rozmery, obsahujú oba typy nukleových kyselín a nesú bunkovú stavbu.",
    
    # 129
    "Bakteriofág (alebo fág) je špecifický bakteriálny vírus, teda vírus, ktorý infikuje a vnútrobunkovo parazituje v bunkách baktérií. Nejde o baktériu so schopnosťou fagocytózy ani o tkanivový makrofág imunitného systému a jeho rozmnožovanie je viazané výlučne na prokaryotické bunky.",
    
    # 130
    "Každý zrelý virión sa povinne skladá z genetickej informácie vo forme nukleovej kyseliny (DNA alebo RNA, nikdy nie oboch súčasne) a ochranného bielkovinového plášťa (kapsidu). Vonkajší lipidový obal majú len obalené vírusy a hlavičku s bičíkom majú iba zložité bakteriofágy.",
    
    # 131
    "Vírusy sú nebunkové obligátne vnútrobunkové parazity, ktoré študuje virológia (odbor mikrobiológie), pričom ich prirodzeným rezervoárom a prenášačom v prírode bývajú mnohé bezstavovce (napr. kliešte a komáre). Nemajú prokaryotickú ani inú bunkovú stavbu a ich kapsid je výlučne proteínovej, nie lipidovej povahy.",
    
    # 132
    "Vírus chrípky (influenzavírus) je obalený submikroskopický RNA vírus s priemerom približne 50–80 nm, pozorovateľný len elektrónovým mikroskopom. Jeho nukleokapsid s bielkovinovými monomérmi kapsidu je obalený vonkajšou lipidovou membránou odvodenou z hostiteľskej bunky; nukleoid sa u vírusov nevyskytuje, keďže ide o štruktúru baktérií.",
    
    # 133
    "Medzi vírusové ochorenia patria vírusové hepatitídy (žltačka), mumps (zápal príušných žliaz), aseptické zápaly mozgových blán (vírusová meningitída), ako aj mor hydiny a ochorenie listov tabaku (vírus tabakovej mozaiky). Angína a tuberkulóza sú bakteriálne infekcie a maláriu spôsobuje jednobunkový parazitický prvok (Plasmodium).",
    
    # 134
    "Rastlinné vírusy (fytovírusy) sú infekčné častice parazitujúce v bunkách rastlín, kde vyvolávajú virózy charakterizované mozaikami či zakrpatením, pričom ich genóm tvorí zvyčajne jednoreťazcová RNA (napr. vírus tabakovej mozaiky má ssRNA, nie dsRNA). Cyanofágy napadajú sinice a fytovírusy nie sú schopné replikácie v prokaryotoch.",
    
    # 135
    "Baktérie sú prokaryotické mikroorganizmy s obrovskou metabolickou diverzitou: zahŕňajú autotrofy (fototrofné sinice/cyanobaktérie a chemoautotrofy) aj heterotrofy (pôdne saprofyty či symbiotické baktérie čreva človeka) a za optimálnych podmienok majú generačnú dobu len 15–30 minút. Rozmnožujú sa priamym priečnym delením (nie mitózou) a peptidoglykán je lokalizovaný v bunkovej stene, nie v plazmatickej membráne.",
    
    # 136
    "Kokovité baktérie sú guľovité bunky, ktoré nemajú bičíky, nevykonávajú aktívny pohyb a môžu sa zoskupovať do strapcovitých útvarov (stafylokoky). Na rozdiel od vírusov ide o samostatné bunky schopné rastu a delenia na živných pôdach mimo hostiteľa; tuberkulózu však vyvoláva tyčinkovitá baktéria (Mycobacterium tuberculosis).",
    
    # 137
    "Baktérie rodu Streptococcus sa delia v jednej rovine a jednotlivé guľovité bunky zostávajú po delení spojené do charakteristických retiazok. Strapce sú typické pre stafylokoky, dvojice buniek pre diplokoky a paličkovitý tvar majú bacily.",
    
    # 138
    "Stafylokoky (rod Staphylococcus) sa nepravidelne delia vo viacerých rovinách, čím vytvárajú priestorové zhluky pripomínajúce strapce hrozna. Retiazky sú typickým morfologickým znakom streptokokov, paličky patria bacilom a spóry slúžia baktériám na prežitie nepriaznivých podmienok, nie primárne na rozmnožovanie.",
    
    # 139
    "Baktérie sa rozmnožujú nepohlavne, primárne priamym priečnym delením (binárnym delením), pri ktorom sa po replikácii chromozómu bunka rozdelí na dve rovnaké dcérske bunky; vláknité formy sa môžu rozmnožovať aj fragmentáciou (rozpadom). Nepriame delenie (mitóza) je výsadou eukaryotov a prenos plazmidov pri konjugácii predstavuje genetickú rekombináciu, nie proces rozmnožovania.",
    
    # 140
    "Každá typická bakteriálna bunka obligátne obsahuje cytoplazmu, proteosyntetický aparát v podobe 70S ribozómov, mureínovú bunkovú stenu a genetickú informáciu lokalizovanú v nukleoide tvorenom jedným kruhovým chromozómom. Bičíky, puzdrá či schopnosť fotosyntézy sú fakultatívne znaky, ktoré sa nachádzajú len u niektorých druhov baktérií.",
    
    # 141
    "Špirálovitý (závitnicový) tvar bunky majú spirily (tuhé skrutkovité bunky), spirochéty (pružné špirálovité bunky schopné vlnivého pohybu) a napríklad fototrofná baktéria Rhodospirillum rubrum. Streptokoky a stafylokoky majú guľovitý tvar, bacily sú tyčinkovité a virióny nemajú bunkovú stavbu.",
    
    # 142
    "Bakteriálny chromozóm (nukleoid) je tvorený jedinou dvojreťazcovou kruhovou molekulou DNA (dsDNA), ktorá voľne leží v cytoplazme bez ohraničenia jadrovou membránou a býva prichytená k vnútornej strane cytoplazmatickej membrány. Nie je lineárny, netvorí pravý eukaryotický chromatín s jadrovými histónmi a nie je obalený žiadnou membránou.",
    
    # 143
    "Medzi živočíšne vírusy (zoovírusy) patria vírusy infikujúce živočíchy a človeka, ako je vírus slintačky a krívačky, patogénne vírusy vyvolávajúce závažné humánne infekcie a onkogénne vírusy (onkovírusy) schopné vyvolať nádorovú transformáciu buniek. Bakteriofágy (vrátane fágu lambda a vírusov E. coli) parazitujú v baktériách a vírus mozaiky zemiakov v rastlinách.",
    
    # 144
    "V prostredí s extrémnou salinitou 20–26 % NaCl (napr. v Mŕtvom mori) dokážu rásť extrémne halofilné organizmy zo skupiny haloarcheónov, kam patria rody Halobacterium a Halococcus. Tieto organizmy majú špeciálne adaptované proteíny a iónové pumpy na zabránenie dehydratácii; bežné baktérie (ako Pseudomonas) či patogény v takto hypertonickom prostredí okamžite podliehajú fatálnej plazmolýze.",
    
    # 145
    "Archeóny sa od baktérií odlišujú absenciou peptidoglykánu (mureínu) v bunkovej stene (majú pseudopeptidoglykán alebo proteínovú S-vrstvu), unikátnym zložením membránových lipidov s éterovou väzbou a adaptáciou na fyziologicky extrémne stanovištia (extrémofily); zároveň nie sú známe žiadne patogénne druhy archeónov. Obe skupiny sú jednobunkové mikroskopické prokaryota bez pravého jadra, ktoré sa delia binárnym delením.",
    
    # 146
    "Chemoautotrofné baktérie sú autotrofné organizmy bez fotosyntetických pigmentov, ktoré využívajú oxid uhličitý (CO2) ako hlavný zdroj uhlíka a energiu na jeho asimiláciu získavajú oxidáciou anorganických látok (napr. amoniaku, dusitanov, sírovodíka či železa). Nevyužívajú slnečné žiarenie s chlorofylom (ako fototrofy) ani rozklad organických látok (ako heterotrofné saprofyty).",
    
    # 147
    "Fototrofné prokaryota sú zastúpené sinicami (cyanobaktériami), ktoré vykonávajú oxygennú fotosyntézu a podľa endosymbiotickej teórie boli pohltené eukaryotickou bunkou, čím dali vznik chloroplastom rastlín. Ako typické prokaryota majú bunkovú stenu spevnenú mureínom (peptidoglykánom), nie celulózou, a nepatria medzi rastliny ani heterotrofné saprofyty.",
    
    # 148
    "Patogénne baktérie sú heterotrofné mikroorganizmy vyvolávajúce infekčné ochorenia u rastlín, živočíchov a ľudí (vrátane venerických ochorení ako syfilis či kvapavka), pričom sa rozmnožujú priamym binárnym delením. Nemnožia sa eukaryotickou mitózou a v mliekarenstve sa využívajú nepatogénne kvasné baktérie mliečneho kvasenia.",
    
    # 149
    "Baktérie rodu Streptococcus vyvolávajú široké spektrum respiračných ochorení (napr. tonzilitídu, bronchitídu, pneumóniu), Salmonella spôsobuje črevné hnačkové infekcie a Mycobacterium tuberculosis je pôvodcom tuberkulózy. Kvapavku vyvoláva Neisseria gonorrhoeae (nie Treponema pallidum, ktorá vyvoláva syfilis), kým kiahne, besnota a slintačka sú vírusové ochorenia.",
    
    # 150
    "Tuberkulózu (Mycobacterium tuberculosis), kvapavku (Neisseria gonorrhoeae) a syfilis (Treponema pallidum) spôsobujú baktérie, preto nepatria medzi vírusové ochorenia. Naopak kliešťová a herpetická encefalitída, detská obrna (poliovírus), chrípka (influenzavírus), opar (HSV) aj besnota (lyssavírus) sú spôsobené vírusmi."
]

assert len(explanations) == 50, f"Expected 50 explanations, got {len(explanations)}"

for i, q in enumerate(questions):
    q['explanation'] = explanations[i]

with open('scripts/bio_batches/batch_3_explained.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Saved scripts/bio_batches/batch_3_explained.json with 50 explained questions.")
