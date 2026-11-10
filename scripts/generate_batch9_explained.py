# -*- coding: utf-8 -*-
"""
Generate explained batch 9 for biology questions 401-450.
"""
import json

explanations = {
    401: (
        "V mieche je nervové tkanivo organizované tak, že sivá hmota (tvorená najmä telami neurónov a synapsiami) "
        "tvorí vnútorné jadro tvaru motýlích krídel, zatiaľ čo biela hmota ju obklopuje na povrchu. "
        "Bielu hmotu tvoria zväzky myelinizovaných nervových vlákien (axónov), ktoré zabezpečujú vzostupné senzitívne "
        "a zostupné motorické dráhy. Nesprávne možnosti zamieňajú polohu sivej a bielej hmoty alebo zamieňajú nervové vlákna s inými anatomickými štruktúrami."
    ),
    402: (
        "Miecha je fylogeneticky najstarším oddielom centrálnej nervovej sústavy stavovcov, slúži ako reflexné centrum "
        "pre motoriku končatín a trupu (cez motoneuróny predných rohov) a v bočných rohoch obsahuje autonómne centrá (napr. mikcia, defekácia). "
        "Zrakové a sluchové reflexy sú však riadené stredným mozgom a centrom rovnováhy je mozoček a vestibulárny aparát. "
        "Fylogeneticky najmladšou časťou je neokortex, nie miecha."
    ),
    403: (
        "Autonómne (vegetatívne) nervy inervujú vnútorné orgány, hladkú svalovinu ciev a žľazy, pričom fungujú nezávisle od našej vôle. "
        "Vychádzajú z mozgového kmeňa (hlavový parasympatikus) aj z miechy (sympatikus z hrudno-driekovej miechy, parasympatikus z krížovej miechy). "
        "Vegetatívna sústava zabezpečujúca homeostázu vnútorného prostredia je vývojovo staršia než somatická nervová sústava riadiaca vôľou ovládané kostrové svaly."
    ),
    404: (
        "Základnými funkčnými vlastnosťami neurónov sú dráždivosť (schopnosť prijímať podnety a meniť pokojový membránový potenciál) "
        "a vodivosť (schopnosť generovať a viesť akčný potenciál bez straty či zmeny kódovanej informácie). "
        "Zrelé neuróny sa na rozdiel od iných buniek spravidla nedelia, nie sú améboidne pohyblivé a nemajú schopnosť svalovej kontrakcie ani leukocytárnej diapedézy."
    ),
    405: (
        "Stredný mozog (mesencephalon) cicavcov obsahuje štvorhrbolie (tectum), ktoré je ústredím nepodmienených zrakových a sluchových orientačných reflexov. "
        "Zároveň sa tu nachádzajú motorické jadrá (nucleus ruber, substantia nigra) a retikulárna formácia, ktoré riadia vzpriamenú polohu hlavy a tela. "
        "Koordináciu pohybov zabezpečuje predovšetkým mozoček, termoreguláciu hypotalamus a kardiovaskulárne centrá sú v predĺženej mieche."
    ),
    406: (
        "Spontánne, automatické dýchanie je generované respiračným centrom v predĺženej mieche (medulla oblongata), "
        "ktoré je modulované pneumotaxickým a apneustickým centrom v moste (pons Varoli). "
        "Predĺžená miecha aj most patria k zadnému mozgu (rhombencephalon) a tvoria mozgový kmeň. "
        "Mozoček, medzimozog ani predný mozog nie sú centrami generovania spontánneho dychového rytmu."
    ),
    407: (
        "Mozgová kôra je fylogeneticky najmladším oddielom nervovej sústavy (jej rozvoj začína u plazov a vrcholí u cicavcov, kde je vysoko zvrásnená u primátov, slonov či kytovcov). "
        "Je funkčne rozdelená na korové centrá (senzorické, motorické, asociačné) a u vtákov tvorí iba tenkú vrstvičku, keďže u nich prevažujú bazálne gangliá. "
        "Nesprávne tvrdenia uvádzajú, že zvrásnenie majú len evolučne staršie cicavce, že integruje len vonkajšie podnety alebo že obsahuje samotné periférne receptory."
    ),
    408: (
        "Mozgová kôra (neokortex) dosahuje najvyšší fylogenetický rozvoj a plošné zvrásnenie (gyrifikáciu) u cicavcov, "
        "pričom mimoriadne rozvinutá je u primátov a veľkých cicavcov s vysokou kognitívnou kapacitou, ako sú slony a delfíny. "
        "U rýb, obojživelníkov a plazov je kôra vyvinutá iba primitívne (archikortex, paleokortex), u žralokov chýba a u vtákov tvorí len tenký lem."
    ),
    409: (
        "Mozoček (cerebellum) je kľúčovým centrom pre udržiavanie rovnováhy tela, svalového tonusu a koordinácie motoriky. "
        "Tieto funkcie vykonáva vďaka priamemu príjmu aferentných signálov z vestibulárneho aparátu vnútorného ucha a proprioreceptorov svalov a šliach. "
        "Centrá dýchania a obranných reflexov (kýchanie) sú v predĺženej mieche, vnímanie bolesti zabezpečuje talamus s kôrou a najvyšším autonómnym centrom je hypotalamus."
    ),
    410: (
        "Najvyšším nadradeným centrom vegetatívneho (autonómneho) riadenia vnútorných orgánov a neuroendokrinnej integrácie je hypotalamus, "
        "ktorého slovenský anatomický názov je podlôžko. "
        "Hypotalamus koordinuje činnosť sympatika, parasympatika a endokrinného systému. Talamus (lôžko) slúži ako prepájacia stanica senzorických dráh, kým mozoček riadi motorickú koordináciu."
    ),
    411: (
        "Nižšia nervová činnosť zahŕňa geneticky fixované, vrodené reakcie organizmu, medzi ktoré patria nepodmienené reflexy a inštinkty (reťazce nepodmienených reflexov). "
        "Patria sem aj elementárne emócie a vrodené afektívne prejavy ako strach viazané na subkortikálne štruktúry. "
        "Naopak získané reakcie, podmienené reflexy a procesy učenia patria k vyššej nervovej činnosti."
    ),
    412: (
        "Podmienený reflex je základným prejavom vyššej nervovej činnosti a mechanizmom adaptívneho učenia, "
        "ktorý sa vytvára počas individuálneho života (ontogenézy) opakovaným spojením indiferentného podnetu s nepodmieneným reflexom. "
        "Jeho neurobiologickým podkladom je vznik dočasných nervových spojení v mozgovej kôre. Nie je vrodený, fylogeneticky daný a bez nácviku nevzniká."
    ),
    413: (
        "Vyššia nervová činnosť (VNČ) zabezpečuje dynamické prispôsobovanie sa organizmu meniacim sa podmienkam na základe skúseností. "
        "Zahŕňa tvorbu podmienených reflexov, pamäť, procesy učenia a u človeka aj abstraktné myslenie. "
        "Nepodmienené reflexy, inštinkty (vrátane rodičovského) a vrodený strach patria do nižšej nervovej činnosti."
    ),
    414: (
        "Fagocytóza je evolučne najstarší imunitný mechanizmus, ktorý sa vyvinul z fagotrofného spôsobu výživy jednobunkovcov a je spoločný pre všetky živočíšne kmene. "
        "Predstavuje nešpecifickú, vrodenú bunkovú imunitu zabezpečovanú profesionálnymi fagocytmi (makrofágmi, neutrofilmi). "
        "Nie je špecifická ani protilátková a nemá nič spoločné so sluchovým Cortiho orgánom."
    ),
    415: (
        "Špecifickú bunkovú (celulárnu) imunitnú odpoveď zabezpečujú T lymfocyty (cytotoxické a pomocné T bunky), "
        "ktoré vznikajú v kostnej dreni a dozrievajú v detskej žľaze – týmuse. "
        "B lymfocyty a z nich odvodené plazmatické bunky zabezpečujú špecifickú humorálnu (protilátkovú) imunitu, zatiaľ čo granulocyty a monocyty patria k nešpecifickej imunite."
    ),
    416: (
        "Objaviteľom fagocytózy ako základného obranného mechanizmu buniek bol ruský biológ Iľja Iľjič Mečnikov (I. I. Mečnikov), "
        "ktorý tento fenomén opísal pri štúdiu buniek lariev hviezdic a získal Nobelovu cenu. "
        "P. Ehrlich rozpracoval teóriu protilátkovej imunity, I. P. Pavlov objavil podmienené reflexy a L. Pasteur vyvinul vakcináciu."
    ),
    417: (
        "Najdokonalejšie vyvinutý sluch s vnímaním vysokofrekvenčného ultrazvuku majú netopiere a veľryby (najmä ozubené veľryby ako delfíny), "
        "ktoré ultrazvukové signály aktívne vysielajú a prijímajú na priestorovú orientáciu a lov metódou echolokácie. "
        "Hoci šelmy počujú vyššie frekvencie než človek, nemajú echolokačný ultrazvukový aparát v takom rozsahu, a ryby či bezstavovce ultrazvuk nevnímajú."
    ),
    418: (
        "Protilátky (imunoglobulíny) sú špecifické bielkoviny secernované plazmatickými bunkami, ktoré vznikajú terminálnou diferenciáciou B lymfocytov po stimulácii antigénom. "
        "Vyznačujú sa vysokou špecificitou, vďaka čomu sa viažu výlučne na ten antigén, ktorý vyvolal ich tvorbu. "
        "Protilátky netvoria T lymfocyty, nie sú to polysacharidy a nie sú totožné s antigénmi."
    ),
    419: (
        "Špecifická humorálna imunita je založená na rozpoznaní antigénu B lymfocytmi a následnej syntéze špecifických protilátok plazmatickými bunkami. "
        "Fylogeneticky ide o mladší mechanizmus než vrodená nešpecifická imunita, pretože adaptívna imunita sa vyvinula až u čeľustnatých stavovcov. "
        "T lymfocyty zabezpečujú bunkovú imunitu a netvoria cirkulujúce protilátky."
    ),
    420: (
        "Protilátky neutralizujú vírusy a bakteriálne toxíny, bunkovú špecifickú imunitu riadia T lymfocyty (dozrievajúce v primárnom lymfatickom orgáne – týmuse) "
        "a fagocytóza predstavuje vrodenú nešpecifickú bunkovú obranu. Materské mlieko obsahuje sekrečné protilátky (najmä sIgA), ktoré novorodencovi poskytujú pasívnu imunizáciu. "
        "Špecifická imunita sa nevyvinula u článkonožcov a fagocytóza nepatrí medzi protilátkové mechanizmy."
    ),
    421: (
        "Proprioreceptory sú špecializované interoreceptory (mechanoreceptory) lokalizované vo svaloch (svalové vretienka) a šľachách (Golgiho šľachové telieska). "
        "Poskytujú centrálnemu nervovému systému informácie o napätí svalov, kĺbovom uhle a polohe jednotlivých častí tela v priestore. "
        "Neintegrujú vonkajšie prostredie (nie sú to exteroreceptory) a nereagujú na elektromagnetické žiarenie (nie sú to radioreceptory)."
    ),
    422: (
        "Chemoreceptory sú senzorické bunky citlivé na chemické látky – chuťové receptory reagujú na látky rozpustené v tekutinách (kontaktný zmysel) "
        "a čuchové receptory reagujú na prchavé látky v ovzduší (diaľkový zmysel). "
        "Sluchové a rovnovážne receptory sú mechanoreceptory, fotoreceptory zachytávajú svetlo a tepelné receptory zmeny teploty."
    ),
    423: (
        "Radioreceptory sú receptory zachytávajúce vlnenie elektromagnetického poľa a teplo; delia sa na fotoreceptory, termoreceptory a špecifické radioreceptory. "
        "V jednoduchšej podobe (napr. stigma) ich nachádzame už u jednobunkovcov a mnohým živočíchom umožňujú vnímať magnetizmus Zeme či polarizované svetlo pre sezónnu navigáciu. "
        "Človek nemá vyvinuté všetky typy (chýba nám napr. magnetorecepcia) a radioreceptory nereagujú na chemické ani zvukové podnety."
    ),
    424: (
        "Statocysta je rovnovážny orgán bezstavovcov, typicky vyvinutý u kôrovcov (na báze tykadiel) a mäkkýšov. "
        "Ide o vačok vystlaný zmyslovými brvami, v ktorom ťažký statolit (zrnko piesku alebo uhličitanu vápenatého) svojím tlakom dráždi receptorové bunky pri zmene polohy. "
        "Stavovce majú rovnovážny statokinetický aparát vo vnútornom uchu, nie statocystu."
    ),
    425: (
        "Statokinetický orgán zabezpečuje vnímanie polohy (statická zložka) a pohybu/uhlového zrýchlenia (kinetická zložka) tela. "
        "U cicavcov leží vo vnútornom uchu (predsieň a tri polkruhovité kanáliky), u rakov je lokalizovaný na báze tykadiel; jeho základom sú vláskové bunky s mechanocíliami reagujúcimi na posun endolymfy a otolitov. "
        "Cortiho orgán slúži na sluch, nie na rovnováhu, a tympanálny orgán hmyzu je sluchovým ústrojom."
    ),
    426: (
        "Mechanoreceptorové bunky meniace mechanickú energiu vlnenia na nervový vzruch sa u cicavcov nachádzajú v Cortiho orgáne slimáka vnútorného ucha, "
        "u vtákov v sluchovom papile vnútorného ucha, u rýb v receptoroch bočnej čiary (zaznamenávajú nízke frekvencie a prúdenie) a u hmyzu v tympanálnych orgánoch. "
        "Cortiho orgán nie je vo vonkajšom ani v strednom uchu a statocysta primárne slúži na vnímanie rovnováhy, nie zvuku."
    ),
    427: (
        "Hmyz má zložené (facetové) oči, ktoré sú zložené z veľkého počtu samostatných funkčných optických jednotiek – omatídií. "
        "Tento typ oka poskytuje mozaikový obraz a vyniká schopnosťou registrovať rýchly pohyb a vnímať polarizované svetlo. "
        "Komorové oči s jednou šošovkou a sietnicou sú typické pre stavovce a hlavonožce."
    ),
    428: (
        "Chemoreceptory zachytávajú chemické molekuly vo vode a vo vzduchu – chuťové poháriky slúžia na kontaktnú chuťovú analýzu, "
        "zatiaľ čo čuch je vysoko vyvinutý u makrosmatických cicavcov (pes, kôň). U druhotne vodných veľrýb je čuch redukovaný až celkom chýba. "
        "Chemoreceptory chemické reakcie neriadia (to robia enzýmy), chuť nie je diaľkový receptor a hmyz má chemoreceptory mimoriadne citlivé."
    ),
    429: (
        "Ektotermné (poikilotermné) živočíchy nedokážu produkovať dostatok metabolického tepla na udržanie stálej telesnej teploty, "
        "preto ich telesná teplota kolíše a závisí od teploty vonkajšieho prostredia. "
        "Medzi ektotermy patria všetky bezstavovce, ako aj drsnokožce, ryby, obojživelníky a plazy. "
        "Stálu teplotu nezávislú od okolia majú iba endotermné vtáky a cicavce."
    ),
    430: (
        "Endotermia (homeotermia) predstavuje schopnosť živočícha udržať si stálu telesnú teplotu nezávisle od výkyvov vonkajšieho prostredia vďaka intenzívnej produkcii tepla vlastným metabolizmom. "
        "Hormón tyroxín priamo zvyšuje bazálny metabolizmus a produkciu tepla v tele, čím je kľúčový pre endotermiu. "
        "Neznamená podchladenie (hypotermiu) ani prehriatie (hypertermiu) a teplo sa tvorí v hlbokom jadre, nie v periférnom obale."
    ),
    431: (
        "Spomedzi recentných živočíchov sú pravými endotermnými organizmami so schopnosťou fyziologickej termoregulácie výlučne vtáky a cicavce. "
        "Všetky ostatné skupiny – bezstavovce, drsnokožce, ryby, obojživelníky aj plazy – sú ektotermné (ich teplota priamo závisí od teploty prostredia)."
    ),
    432: (
        "Fyzikálna termoregulácia reguluje výdaj tepla do okolia fyzikálnymi procesmi bez zmeny produkcie tepla: "
        "radiáciou (vyžarovaním), konvekciou (prúdením), kondukciou a evaporáciou (odparovaním potu). "
        "To je sprostredkované zmenou prietoku krvi v koži (vazodilatácia výdaj tepla zvyšuje, vazokonstrikcia ho šetrí). Zvýšenie metabolizmu a svalový tras patria k chemickej termoregulácii."
    ),
    433: (
        "Hibernanty (pravé zimné spáče ako jež, plch, sysel) sú heterotermné živočíchy, ktoré pri poklese teploty okolia (typicky pod cca 10 °C) "
        "upadajú do torporu, pričom drasticky tlmia metabolizmus a znižujú teplotu telesného jadra. "
        "Ako jediný zdroj energie využívajú zásoby tuku (najmä hnedého a bieleho tuku). Medveď nie je pravý hibernant a metabolizmus sa nezvyšuje, ale klesá."
    ),
    434: (
        "V pokojovom stave u endotermných živočíchov tvorí hlavný podiel metabolického tepla pečeň, "
        "pretože v jej hepatocytoch nepretržite prebieha obrovské množstvo exergonických biochemických reakcií látkovej premeny. "
        "Kostrové svaly produkujú najviac tepla pri fyzickej práci alebo svalovom trase, avšak v bazálnom pokoji dominuje pečeň."
    ),
    435: (
        "Estivácia je letný spánok – kľudový stav, ktorým púštne, stepné a subtropické živočíchy prekonávajú nepriaznivé horúce a suché obdobia "
        "s nedostatkom vody. Znižuje sa pri nej látková premena a hormonálna aktivita (v kľúči testovnice figuruje inzulín v metabolickom kontexte). "
        "Hibernácia je naopak zimný spánok chrániaci pred mrazom."
    ),
    436: (
        "Heterotermia je schopnosť niektorých endotermných živočíchov prechodne znížiť reguláciu telesnej teploty a prispôsobiť sa teplote okolia, "
        "čím sa v nepriaznivých podmienkach (chlad, nedostatok potravy) stávajú dočasne ektotermnými (napr. pri hibernácii alebo dennom torpore). "
        "Umožňuje to šetriť energetické zásoby znížením rozdielu medzi telom a okolím, pričom bazálny metabolizmus nestúpa, ale klesá."
    ),
    437: (
        "Epifýza (šuškovité teliesko) je neuroendokrinná žľaza epitalamu, ktorá reaguje na striedanie svetla a tmy "
        "a v tme secernuje hormón melatonín regulujúci cirkadiánne a sezónne biorytmy organizmu. "
        "Nepatrí k hypofýze, neprodukuje rastový hormón (ten tvorí adenohypofýza) ani pigment melanín (ten tvoria melanocyty v koži)."
    ),
    438: (
        "Hormóny štítnej žľazy – tyroxín (T4) a trijódtyronín (T3) – stimulujú bazálny metabolizmus, spotrebu kyslíka a rast tkanív. "
        "U obojživelníkov sú nevyhnutným spúšťačom a regulátorom metamorfózy žubriežky na dospelého jedinca. "
        "Nie sú to stavebné látky ani gestagény, netvoria sa v hypofýze a metabolizmus sodíka riadi aldosterón z kôry nadobličiek."
    ),
    439: (
        "Endokrinná regulácia hmyzu zahŕňa neurosekrečné bunky mozgového ganglia (produkujúce aktivačný hormón), predhrudné žľazy (ekdyzón vyvolávajúci zvliekanie) "
        "a telieska corpora allata (juvenilný hormón brániaci dospelej premene), ktoré koordinujú metamorfózu. "
        "Hmyz tiež uvoľňuje feromóny slúžiace na vnútrodruhovú komunikáciu. Malpighiho trubice sú vylučovacie orgány a hmyz nemá uzavretú krvnú ani lymfatickú sústavu."
    ),
    440: (
        "Prištítne telieska (glandulae parathyroideae) a ich hormón parathormón sa fylogeneticky prvýkrát objavujú u obojživelníkov "
        "v súvislosti s prechodom stavovcov z vody na súš a potrebou prísnej regulácie hladiny vápnika v krvi a kostnom tkanive. "
        "Ryby a bezstavovce prištítne telieska nemajú."
    ),
    441: (
        "Inzulín je peptidový hormón B-buniek Langerhansových ostrovčekov pankreasu, ktorý pôsobí hypoglykemicky (znižuje glykémiu). "
        "Podporuje vstup glukózy do buniek, stimuluje syntézu glykogénu v pečeni a svaloch (glykogenézu) a pôsobí ako priamy fyziologický antagonista glukagónu. "
        "Rozklad glykogénu naopak inhibuje."
    ),
    442: (
        "Hormóny sú vysoko účinné biochemické regulátory syntetizované endokrinnými žľazami alebo tkanivami, ktoré pôsobia špecificky "
        "na cieľové bunky nesúce zodpovedajúce receptory a riadia ich metabolické a fyziologické funkcie. "
        "V telových tekutinách vykazujú rôzny polčas účinku od niekoľkých minút po dni. Neslúžia ako zdroj energie (ATP) ani ako stavebné zložky buniek."
    ),
    443: (
        "Hormonálna regulácia je fylogeneticky veľmi stará a uplatňuje sa už u bezstavovcov (najmä neurosekrécia), "
        "pričom u stavovcov sa vyvinul komplexný endokrinný aparát prepojený s nervovou sústavou (neurohumorálna regulácia cez hypotalamus). "
        "Látkový transport hormónov krvou/cievami je pomalší než šírenie nervových vzruchov, ale má dlhodobejší účinok."
    ),
    444: (
        "Feromóny hmyzu sú exohormóny uvoľňované do vonkajšieho prostredia, ktoré vyvolávajú špecifické behaviorálne odpovede u príslušníkov rovnakého druhu: "
        "pohlavné feromóny stimulujú párenie a priťahujú partnera, kým poplašné feromóny vyvolávajú únikové alebo koordinované obranné reakcie kolónie. "
        "Nespôsobujú útlm rastu ani zablokovanie premeny."
    ),
    445: (
        "Predný lalok hypofýzy (adenohypofýza) je žľazový oddiel produkujúci glandotropné hormóny riadiace iné endokrinné žľazy (napr. ACTH riadi kôru nadobličiek), "
        "ako aj prolaktín (stimuluje laktáciu) a rastový hormón (somatotropín). "
        "Zadný lalok je neurohypofýza, ktorá len skladuje vazopresín a oxytocín vytvorené v hypotalame, a melanotropný hormón produkuje stredný lalok."
    ),
    446: (
        "K výskumu správania zvierat patrí klasická etológia skúmajúca vrodené aj naučené správanie v prirodzenom prostredí, "
        "behaviorizmus skúmajúci odpovede organizmu na stimuly a fyziológia vyššej nervovej činnosti zameraná na reflexy a hormonálne vplyvy (v kľúči testovnice vrátane pôsobenia testosterónu). "
        "Anatómia a cytológia skúmajú morfologickú štruktúru orgánov a buniek, nie samotné správanie."
    ),
    447: (
        "Komunikácia živočíchov spočíva v prenose informácií medzi jedincami pomocou signálov, ktoré môžu byť akustické, optické, dotykové, chemické či elektrické. "
        "Tieto signály majú identifikačnú, varovnú alebo teritoriálnu funkciu a priamo ovplyvňujú správanie prijímateľa, čo je podstatou sociálneho a teritoriálneho správania. "
        "Tvrdenia o absencii informačnej funkcie sú v priamom rozpore s definíciou komunikácie."
    ),
    448: (
        "Fakultatívne učenie je nepovinná, flexibilná forma učenia, ktorá nie je vekovo obmedzená, prebieha počas celej ontogenézy jedinca "
        "na základe zvedavosti a individuálnych skúseností a vedie k neustálemu zdokonaľovaniu činnosti. "
        "Naopak obligatórne učenie (napr. vpečatenie – imprinting) prebieha výlučne v ranom veku počas citlivej fázy života."
    ),
    449: (
        "Inštinktívne správanie je vrodená, druhovo špecifická forma správania tvorená reťazcami nepodmienených reflexov, "
        "ktorú skúma etológia a ktorá je modulovaná vnútorným hormonálnym stavom (v kľúči testovnice progesterón ovplyvňujúci materské správanie). "
        "Zahŕňa napr. obranné, únikové či komfortné správanie (starostlivosť o telo). Nie je založené na podmienených reflexoch a nezahŕňa abstraktnú generalizáciu."
    ),
    450: (
        "V otázke č. 450 došlo v tlači testovnice UPJŠ LF k tlačovej chybe (možnosti patria enzýmu ptyalín). "
        "Ptyalín (slinná alfa-amyláza) je produkovaný najmä príušnými žľazami (glandula parotis) a vylučovaný do slín v ústnej dutine, kde začína štiepenie polysacharidov (škrobu). "
        "Sliny obsahujú aj baktericídny lyzozým a trávenina prechádza ďalej do žalúdka a čreva; ptyalín neštiepi bielkoviny (tie štiepi až pepsín v žalúdku)."
    )
}

def main():
    with open('scripts/bio_batches/batch_9.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 50, f"Expected 50 questions, got {len(data)}"

    for i, q in enumerate(data):
        q_num = i + 401
        assert q_num in explanations, f"Missing explanation for Q{q_num}"
        q['explanation'] = explanations[q_num]

    out_path = 'scripts/bio_batches/batch_9_explained.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully processed {len(data)} questions and saved to {out_path}.")

if __name__ == '__main__':
    main()
