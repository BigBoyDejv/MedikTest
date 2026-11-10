# -*- coding: utf-8 -*-
import json

with open('scripts/bio_batches/batch_8.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions.")

explanations = {
    351: (
        "Malpighiho žľazy (trubice) hmyzu a pavúkovcov sú tenké rúrkovité výbežky omývané hemolymfou, "
        "ktoré ústia na rozhraní stredného a zadného čreva, kde odovzdávajú metabolity (najmä kyselinu močovú). "
        "Ostatné vylučovacie orgány vyúsťujú na povrch tela (napr. metanefrídie obrúčkavcov nefropórom, tykadlové žľazy "
        "kôrovcov pri báze tykadiel, protonefrídie ploskavcov pórmi v pokožke) alebo u cicavcov ústia nefróny do zberných kanálikov obličiek."
    ),
    352: (
        "Protonefrídie sú fylogeneticky pôvodné vylučovacie a osmoregulačné orgány ploskavcov (Plathelminthes) a hlístovcov, "
        "ktoré začínajú slepo v mezenchýme plamienkovou bunkou s vírivým zväzkom bičíkov. Mäkkýše a obrúčkavce majú vyvinuté "
        "metanefrídie (resp. Bojanove orgány), prvoky vylučujú pulzujúcimi vakuolami a stavovce vrátane rýb a cicavcov (aj vtákopyska) majú obličky."
    ),
    353: (
        "Základnými párovými vylučovacími orgánmi všetkých stavovcov sú obličky (pronefros, mezonefros/opistonefros u bezblanovcov "
        "a metanefros u amniotov). Nefrón je základná mikroskopická stavebná a funkčná jednotka obličkového parenchýmu, nie samostatný orgán. "
        "Ostatné možnosti (protonefrídie, metanefrídie, Malpighiho trubice, tykadlové žľazy) predstavujú exkrečné orgány bezstavovcov."
    ),
    354: (
        "Malpighiho žľazy (trubice) sú typickým vylučovacím ústrojom suchozemských článkonožcov – hmyzu, stonožiek a pavúkovcov, "
        "pričom ich sekrét (kyselina močová) odchádza do čreva s minimálnou stratou vody. Nemajú ich však všetky článkonožce (kôrovce majú "
        "modifikované metanefrídie – tykadlové alebo čeľustné žľazy). Obrúčkavce a mäkkýše majú metanefrídie a ploskavce protonefrídie."
    ),
    355: (
        "Nefrón ako základná funkčná jednotka obličky cicavcov pozostáva z renálneho (Malpighiho) telieska – tvoreného glomerulom "
        "a Bowmanovým puzdrom – a tubulárneho systému zahŕňajúceho proximálny stočený kanálik, Henleho slučku a distálny stočený kanálik. "
        "Močovod, močový mechúr a obličková panvička tvoria vývodné močové cesty a nie sú súčasťou samotného nefrónu. Plamienková bunka je súčasťou "
        "protonefrídií a Malpighiho žľaza patrí článkonožcom."
    ),
    356: (
        "Primárny moč vzniká glomerulárnou filtráciou krvnej plazmy cez stenu kapilár Malpighiho telieska do Bowmanovho puzdra "
        "a odtiaľ odteká do proximálneho tubulu a ďalších častí nefrónu. Predstavuje prakticky deproteinizovaný ultrafiltrát krvi, preto obsahuje "
        "vodu, nízkomolekulové minerály, glukózu, aminokyseliny a močovinu, no za normálnych okolností neobsahuje krvné bunky ani vysokomolekulové "
        "bielkoviny. Do močovodov a mechúra vstupuje až definitívny moč po spätnej resorpcii v tubuloch."
    ),
    357: (
        "Morské ryby žijú v hypertonickom prostredí a nadbytok prijatých solí aktívne vylučujú von špecializovanými chloridovými bunkami "
        "na žiabrach. Sladkovodné ryby v hypotonickom prostredí naopak čelia strate solí, preto soli cez žiabre aktívne vychytávajú z vody do krvi. "
        "Morské plazy (krokodíly, leguány) a morské vtáky (napr. čajky) eliminujú nadbytok solí špeciálnymi nosovými a soľnými žľazami."
    ),
    358: (
        "Otvorená cievna sústava, v ktorej sa telová tekutina (hemolymfa) vylieva z ciev priamo do medzibunkových priestorov a lakún, "
        "je typická pre väčšinu mäkkýšov, článkonožce a plášťovce (Tunicata). Naopak obrúčkavce, hlavonožce a stavovce (plazy, cicavce) "
        "majú dokonale uzavretú cievnu sústavu s kapilárnym riečiskom. Ploskavce cievnu sústavu nemajú vôbec."
    ),
    359: (
        "Telové tekutiny živočíchov (hydrolymfa, hemolymfa, krv, miazga) plnia predovšetkým transportnú funkciu – privádzajú k tkanivám kyslík, "
        "živiny, hormóny a vitamíny a odvádzajú katabolity. Obsahujú rôzne rozpustené organické zložky vrátane enzýmov, ktoré sa zúčastňujú "
        "biochemických premien. Nevznikajú výlučne vo vylučovacej sústave a neprenášajú nervové vzruchy, ktoré sa šíria po membránach neurónov."
    ),
    360: (
        "Hydrolymfa je fylogeneticky najjednoduchšia telová tekutina bezstavovcov (najmä pŕhlivcov a ploskavcov), ktorej zloženie je blízke "
        "okolitej vode a obsahuje len minimálne množstvo buniek a transportných proteínov. Voľne prúdi v telových dutinách alebo štrbinách. "
        "Obrúčkavce a stavovce majú pokročilejšie tekutiny (krv, lymfu) cirkulujúce v diferencovaných cievnych sústavách."
    ),
    361: (
        "Obehová sústava stavovcov je uzavretá kardiovaskulárna sústava tvorená srdcom a cievami, v ktorej krv koluje bez priameho vylievania "
        "do tkanív a sprostredkúva látkovú výmenu medzi kapilárami a bunkami. Lymfatická sústava stavovcov predstavuje samostatný odvodný "
        "cievny systém, ktorý do krvného obehu ústi až v oblasti veľkých žíl. U suchozemských stavovcov s rozvojom pľúc došlo k vytvoreniu dvoch "
        "krvných obehov a rozdeleniu srdca, čím je ich sústava zložitejšia ako u vodných stavovcov (rýb)."
    ),
    362: (
        "Krv cicavcov pozostáva z tekutej zložky (krvnej plazmy) a formovaných krvných elementov (erytrocyty, leukocyty, trombocyty). "
        "Plazma obsahuje vodu, anorganické soli, plazmatické bielkoviny a transportované hormóny. Cicavčie erytrocyty aj krvné doštičky "
        "(trombocyty ako úlomky megakaryocytov) sú bezjadrové, kým leukocyty sú vždy plnohodnotné bunky obsahujúce bunkové jadro."
    ),
    363: (
        "Väčšina plazmatických bielkovín (albumíny, fibrinogén, časť globulínov a zrážacie faktory) je syntetizovaná hepatocytmi v pečeni, "
        "pričom kostná dreň a slezina ich v takomto rozsahu netvoria (imunoglobulíny tvoria plazmatické B-bunky). Tieto bielkoviny reverzibilne "
        "viažu a prenášajú nerozpustné látky (hormóny, lipidy, kovy), udržiavajú onkotický tlak krvi, zúčastňujú sa na zrážaní krvi a tvoria "
        "zložky imunitnej obrany."
    ),
    364: (
        "Krvná plazma cicavcov je slabo zásaditá tekutina s úzkym fyziologickým rozmedzím pH (7,35 – 7,45) a prísne regulovanou homeostázou. "
        "Obsahuje približne 90 – 92 % vody a 8 – 10 % sušiny, v ktorej dominujú plazmatické bielkoviny (cca 60 – 80 g/l), elektrolyty, glukóza "
        "a dusíkaté splodiny metabolizmu bielkovín (močovina, kreatinín). Leukocyty sú bunkové elementy krvi, nie súčasť plazmy, a sú vždy jadrové."
    ),
    365: (
        "Pečeň je hlavným syntetickým centrom tela pre plazmatické bielkoviny – produkuje prakticky všetky albumíny, fibrinogén, protrombín "
        "a väčšinu alfa- a beta-globulínov. Výnimkou sú iba imunoglobulíny (gama-globulíny), ktoré vznikajú v plazmatických bunkách odvodených "
        "z B-lymfocytov v lymfatických tkanivách. Erytrocyty, srdce, kostná dreň ani slezina hlavnú masu plazmatických bielkovín nesyntetizujú."
    ),
    366: (
        "V krvnej plazme človeka tvoria bielkoviny približne 60 až 80 g na liter, čo z nich robí zďaleka najviac zastúpenú skupinu organických "
        "látok (tvoria vyše 80 % celkovej organickej sušiny plazmy). Hoci celkovo najviac je v plazme vody (vyše 90 %), tá je anorganickou zlúčeninou. "
        "Ostatné organické látky, ako napríklad glukóza, lipidy, močovina či kreatín, sú prítomné v podstatne nižších koncentráciách."
    ),
    367: (
        "Medzi krvné telieska (formované krvné elementy) patria erytrocyty (červené krvinky), rôzne typy leukocytov (biele krvinky – granulocyty "
        "a agranulocyty vrátane lymfocytov) a trombocyty (krvné doštičky). Lyzozómy sú vnútrobunkové organely, krvné farbivá (napr. hemoglobín) "
        "sú bielkovinové makromolekuly a antigény predstavujú imunologické štruktúry na membránach, nie samostatné krvné telieska."
    ),
    368: (
        "Všetky typy krviniek cicavcov vznikajú v postnatálnom období procesom hematopoézy v červenej kostnej dreni z jednotnej pluripotentnej "
        "krvotvornej kmeňovej bunky. Diferencované bunky majú rozdielnu životnosť – erytrocyty cirkulujú približne 120 dní, trombocyty 7 až 10 dní, "
        "niektoré granulocyty len hodiny, kým pamäťové lymfocyty môžu prežívať celé roky. Krvotvorné bunky sa nenachádzajú v plazme a u dospelých "
        "krvinky nevznikajú v pečeni."
    ),
    369: (
        "Leukocyty (biele krvinky) sú plnohodnotné jadrové bunky, ktoré sa podľa prítomnosti a farbiteľnosti špecifických granúl v cytoplazme "
        "delia na granulocyty (neutrofily, eozinofily, bazofily) a agranulocyty (monocyty, lymfocyty). V krvi ich je rádovo menej než červených "
        "krviniek (cca 4 – 10 × 10⁹/l oproti miliónom erytrocytov) a bežne vystupujú z krvného obehu diapedézou do lymfy a intersticiálnych tkanív."
    ),
    370: (
        "Leukocyty (biele krvinky) predstavujú kľúčovú bunkovú zložku imunitnej obrany organizmu, pričom zabezpečujú fagocytózu cudzorodých častíc "
        "(neutrofily, makrofágy) aj špecifickú protilátkovú a bunkovú imunitu (lymfocyty). Prenos dýchacích plynov (kyslíka a oxidu uhličitého) "
        "zabezpečujú erytrocyty prostredníctvom hemoglobínu, zatiaľ čo primárne zastavenie krvácania riadia trombocyty a koagulačné faktory."
    ),
    371: (
        "Bezjadrové erytrocyty sú charakteristickým evolučným znakom cicavcov – strata jadra a organel počas erytropoézy v kostnej dreni "
        "vytvára bikonkávny tvar a maximalizuje priestor pre väzbu kyslíka na hemoglobín. Všetky ostatné triedy stavovcov (ryby, obojživelníky, "
        "plazy aj vtáky) majú erytrocyty oválne a trvalo jadrové. Podľa oficiálneho kľúča testovnice sú priradené možnosti c a f."
    ),
    372: (
        "Počet erytrocytov na jednotku objemu krvi je regulovaný fyziologickými aj environmentálnymi faktormi: androgény stimulujú erytropoézu "
        "(samce majú vyšší počet), mláďatá a novorodenci majú spravidla vyššie hodnoty a nadmorská výška spôsobuje hypoxiu stimulujúcu tvorbu "
        "erytropoetínu. U nižších ektotermných stavovcov sa počet mení aj s ročným obdobím v závislosti od metabolickej aktivity."
    ),
    373: (
        "Leukocyty sa od erytrocytov líšia imunitnou špecializáciou, rôznou a často kratšou životnosťou, prítomnosťou jadra a mitochondrií "
        "s aeróbnym metabolizmom, odlišnou vetvou diferenciácie z kmeňovej bunky a schopnosťou prenikať do tkanív celého tela. Zároveň je ich "
        "koncentrácia v krvi tisícnásobne nižšia než počet erytrocytov. Cicavčie leukocyty sú jadrové, kým ich erytrocyty sú bezjadrové."
    ),
    374: (
        "Monocyty sú najväčšie cirkulujúce biele krvinky patriace k agranulocytom, ktoré vznikajú v kostnej dreni z myeloblastickej línie. "
        "Majú výraznú schopnosť diapedézy (prestupu cez stenu kapilár) do tkanív, kde sa diferencujú na makrofágy s vysokou schopnosťou fagocytózy "
        "patogénov a odumretých buniek. Nepodieľajú sa na transporte plynov ani živín, ich funkcia je čisto obranná."
    ),
    375: (
        "Trombocyty cicavcov sú bezjadrové bunkové fragmenty (doštičky), ktoré vznikajú v červenej kostnej dreni odlamovaním cytoplazmy "
        "obrovských megakaryocytov. Sú nevyhnutné pri hemostáze – tvoria primárnu zátku pri poranení cievy a vylučujú faktory udržiavajúce "
        "celistvosť a tonus cievneho endotelu. Nevznikajú v slezine ani pečeni a nemajú jadro (na rozdiel od jadrových trombocytov vtákov či plazov)."
    ),
    376: (
        "Podstatou hemokoagulácie je séria kaskádovitých enzymatických reakcií, ktorej vyvrcholením je trombínom sprostredkovaná premena "
        "rozpustného plazmatického proteínu fibrinogénu na nerozpustné vlákna fibrínu. Tie vytvoria hustú priestorovú sieť zachytávajúcu krvinky "
        "a definitívne uzavrú poškodenie cievnej steny. Vazokonstrikcia a doštičková zátka krvácanie tlmia, no samotnú koaguláciu definuje vznik fibrínu."
    ),
    377: (
        "Zastavenie krvácania (hemostáza) je koordinovaný biologický a biochemický proces pozostávajúci z vazokonstrikcie poškodenej cievy, "
        "tvorby provizórnej doštičkovej zátky a následnej koagulačnej kaskády vedúcej k fibrínovej sieti. U bezstavovcov s otvoreným obehom "
        "sa uplatňuje najmä stiahnutie svaloviny v okolí rany. Heparín je prirodzený inhibítor zrážania krvi (antikoagulant), takže proces nespúšťa ani neurýchľuje."
    ),
    378: (
        "Fibrinogén je vysokomolekulová rozpustná bielkovina krvnej plazmy (koagulačný faktor I) syntetizovaná hepatocytmi v pečeni. "
        "Počas procesu zrážania krvi sa po odštiepení fibrinopeptidov pôsobením trombínu mení na nerozpustný fibrín tvoriaci kostru krvnej zrazeniny. "
        "Nenachádza sa vo vnútri erytrocytov, neslúži na prenos dýchacích plynov a nepôsobí proti zrážaniu krvi."
    ),
    379: (
        "Biely trombus (primárna doštičková zátka) vzniká v prvých fázach hemostázy adhéziou a agregáciou aktivovaných krvných doštičiek "
        "na obnažený kolagén poranenej cievnej steny. Vytvára sa predovšetkým v mieste menších poškodení mikrocirkulácie, ktoré dokáže provizórne "
        "uzavrieť ešte pred dobehnutím plnej koagulačnej kaskády. Červený trombus vzniká až zachytením erytrocytov do fibrínovej siete."
    ),
    380: (
        "Aglutinogény sú špecifické antigénne štruktúry (glykoproteíny a glykolipidy) pevne viazané na vonkajšom povrchu membrány erytrocytov, "
        "ktoré určujú krvnú skupinu (napr. v systémoch AB0 a Rh). Ich syntéza a štruktúra sú striktne geneticky kódované dedičnými alelami. "
        "Protilátky prítomné v plazme sa nazývajú aglutiníny, nie aglutinogény."
    ),
    381: (
        "Aglutiníny sú špecifické protilátky (imunoglobulíny) rozpustené v krvnej plazme namierené proti cudzím erytrocytovým antigénom. "
        "Pri reakcii s príslušným aglutinogénom na povrchu krviniek (napr. anti-A s antigénom A) vyvolávajú aglutináciu (zhlukovanie) a následnú "
        "hemolýzu červených krviniek. Za normálnych okolností jedinec nikdy netvorí aglutiníny proti vlastným krvinkám (autotolerancia)."
    ),
    382: (
        "Hemolymfa (krvomiazga) je cirkulujúca tekutina bezstavovcov s otvorenou cievnou sústavou (článkonožce, mäkkýše), ktorá sa z ciev voľne "
        "rozlieva do telových dutín (lakún). Obsahuje voľne rozpustené dýchacie farbivá (napr. hemocyanín s meďou alebo hemoglobín) a zabezpečuje "
        "rozvoz plynov a živín. Neobsahuje tvarované prvky ako cicavčie erytrocyty a trombocyty a u stavovcov sa vôbec nevyskytuje."
    ),
    383: (
        "Tkanivový mok vypĺňa medzibunkové štrbiny tkanív a vytvára bezprostredné tekuté mikroprostredie pre bunky organizmu. Vzniká filtráciou "
        "krvnej plazmy cez stenu kapilár a zabezpečuje difúziu dýchacích plynov, živín a nízkomolekulových látok medzi krvou a bunkami. Za normálnych "
        "okolností obsahuje len minimálne množstvo bielkovín; prebytočný tkanivový mok sa odvádza ako lymfa."
    ),
    384: (
        "Miazga (lymfa) vzniká vstrebávaním prebytočného tkanivového moku do slepo začínajúcich lymfatických kapilár, preto sa jej riečisko "
        "u stavovcov označuje ako otvorený lymfatický systém ústiaci do žíl. Obsahuje biele krvinky (prevažne lymfocyty), enzýmy a vstrebané lipidy, "
        "pričom prechádza cez lymfatické uzliny, ktoré pôsobia ako biologické filtre imunitného systému. Erytrocyty sa v nej fyziologicky nenachádzajú."
    ),
    385: (
        "Medzi lymfatické orgány stavovcov patria centrálne (týmus, Fabriciov vačok u vtákov, kostná dreň) a periférne lymfatické orgány "
        "(slezina, lymfatické uzliny, mandle a červovitý prívesok slepého čreva – apendix). Tieto štruktúry zabezpečujú dozrievanie, proliferáciu "
        "a aktiváciu lymfocytov. Chylus je samotná črevná lymfa, statocysta je zmyslový orgán bezstavovcov a srdce s pankreasom patria do iných sústav."
    ),
    386: (
        "Lymfatická sústava je fylogeneticky viazaná výlučne na stavovce (ryby, obojživelníky, plazy, vtáky, cicavce), u ktorých dopĺňa "
        "uzavretý krvný obeh odvádzaním prebytočnej tekutiny a účasťou na imunite. Bezstavovce (mäkkýše, obrúčkavce, článkonožce, ploskavce) "
        "lymfatickú sústavu nemajú, pretože ich transportné a imunitné funkcie zabezpečuje hydrolymfa, hemolymfa alebo coelomová tekutina."
    ),
    387: (
        "Lymfatická sústava plní kľúčovú úlohu v imunitnom systéme – lymfatické uzliny a tkanivá zachytávajú a ničia cudzorodé mikroorganizmy, "
        "antigény aj transformované nádorové bunky. Okrem toho odvádza prebytočný tkanivový mok a transportuje vstrebané lipidy z tráviacej sústavy "
        "späť do krvného obehu. Výmenu dýchacích plynov a termoreguláciu rozvodom tepla zabezpečuje krvný obeh, nie miazga."
    ),
    388: (
        "Srdce rýb je čisto venózne a skladá sa z jednej predsiene a jednej komory (s nadväzujúcim sinus venosus a bulbus/conus arteriosus), "
        "ktorými prúdi výlučne odkysličená krv. Z komory je táto krv vháňaná ventrálnou aortou do žiabrových oblúkov, kde sa okysličuje a následne "
        "bez opätovného návratu do srdca rozvádza chrbtovou aortou do celého tela. Ryby nemajú srdce rozdelené na dve predsiene."
    ),
    389: (
        "Úplne rozdelenú komorovú priehradku (septum interventriculare), a teda dokonale štvorkomorové srdce s oddeleným pľúcnym a telovým obehom, "
        "majú spomedzi stavovcov vtáky a cicavce (a spomedzi plazov krokodíly). U rýb a obojživelníkov je komora nerozdelená a u ostatných plazov "
        "(jašterice, hady, korytnačky) je priehradka neúplná, čo umožňuje miešanie venóznej a arteriálnej krvi."
    ),
    390: (
        "Dospelé obojživelníky majú srdce tvorené dvoma predsieňami (do pravej prichádza odkysličená krv z tela, do ľavej okysličená krv z pľúc a kože) "
        "a jednou spoločnou svalnatou komorou, v ktorej dochádza k čiastočnému miešaniu krvi. Z komory je krv vháňaná do arteriálneho kmeňa "
        "(conus arteriosus) a rozvádzaná do pľúcno-kožného aj telového obehu. Podľa testovnicového kľúča sú označené možnosti a a c."
    ),
    391: (
        "U cicavcov prúdi okysličená krv zo zberného pľúcneho riečiska štyrmi pľúcnymi žilami (venae pulmonales) do ľavej predsiene srdca. "
        "Odtiaľ preteká cez dvojcípu chlopňu do ľavej komory, ktorá ju počas systoly vháňa aortou do veľkého (telového) krvného obehu k všetkým tkanivám. "
        "Pravá komora vháňa odkysličenú krv do pľúcnice a malého pľúcneho obehu, zatiaľ čo pečeňová vrátnica vedie žilovú krv zo zažívacieho traktu."
    ),
    392: (
        "Podnety na srdcovú činnosť vznikajú vďaka automacii a rytmicite priamo v samotnom srdci, presnejšie v jeho prevodovom systéme "
        "(primárnym pacemakerom je sinoatriálny uzol v pravej predsieni). Autonómne nervy zo sympatika a parasympatika (z centier v predĺženej mieche) "
        "spolu s hormónmi srdcovú frekvenciu a silu sťahu iba regulujú, nie sú však pôvodcami samotného základného rytmu."
    ),
    393: (
        "Grafický záznam časového priebehu elektrických potenciálov vznikajúcich depolarizáciou a repolarizáciou myokardu pri práci srdca "
        "sa nazýva elektrokardiogram, v skratke EKG. EEG (elektroencefalogram) registruje elektrické biopotenciály mozgu, EMG (elektromyogram) "
        "sníma aktivitu kostrových svalov a fonokardiogram zaznamenáva akustické srdcové ozvy."
    ),
    394: (
        "Základným meradlom celkovej mechanickej výkonnosti srdca je minútový objem srdca (srdcový výdaj), ktorý vyjadruje množstvo krvi "
        "prečerpané jednou komorou za jednu minútu (v pokoji približne 5 litrov/min). Závisí od súčinu systolického (tepového) objemu a frekvencie srdcových sťahov. "
        "Samotný systolický objem vyjadruje len výkon pri jedinej kontrakcii, nie celkový minútový výdaj."
    ),
    395: (
        "Koronárne (vencovité) tepny odstupujú priamo z bázy vzostupnej aorty hneď za polmesiačikovitými chlopňami a bohato sa vetvia "
        "do hustej kapilárnej siete zabezpečujúcej nepretržité zásobovanie myokardu kyslíkom a živinami. Preteká nimi významná časť srdcového výdaja "
        "(okolo 5 až 10 % krvi vytlačenej do aorty). Nevychádzajú z dutých žíl ani z pľúcnice a zásobenie srdca je nevyhnutné pre jeho neustálu prácu."
    ),
    396: (
        "Úplné oddelenie pľúcneho a telového krvného obehu je podmienené kompletnou komorovou priehradkou, ktorá úplne zamedzuje miešaniu "
        "okysličenej a odkysličenej krvi v srdci. Tento pokročilý obehový systém majú vtáky a cicavce (a spomedzi plazov krokodíly). "
        "Obojživelníky majú komoru nerozdelenú a väčšina plazov má priehradku neúplnú, preto sa u nich krv čiastočne mieša."
    ),
    397: (
        "Vrátnicový (portálny) obeh je funkčný žilový obeh tvorený vrátnicou (vena portae), ktorá zbiera odkysličenú krv bohatú na vstrebané "
        "živiny z kapilár nepárových brušných orgánov (žalúdok, črevá, pankreas, slezina) a privádza ju do pečeňových sínusoidov. Predstavuje súčasť "
        "veľkého telového obehu a umožňuje pečeni bezprostredne metabolizovať, ukladať a detoxikovať vstrebané látky pred ich vstupom do dolnej dutej žily."
    ),
    398: (
        "K vlastnej výmene dýchacích plynov, živín a odpadových látok medzi krvou a tkanivovým mokom dochádza výhradne v kapilárach (vlásočniciach). "
        "Ich stena je tvorená len jedinou vrstvou endotelových buniek na bazálnej membráne a vďaka obrovskej ploche a pomalému toku krvi poskytuje "
        "ideálne podmienky pre difúziu. Tepny, žily a veľké kmene majú hrubé trojvrstvové steny a slúžia len ako rozvodné potrubia."
    ),
    399: (
        "Neurón je základnou stavebnou a funkčnou jednotkou nervovej sústavy, ktorá sa skladá z tela bunky (somy) a výbežkov dvojakého typu. "
        "Dendrity privádzajú vzruchy do tela bunky (vedenie dostredivé / celulipetálne), zatiaľ čo jediný axón (neurit) vedie nervové vzruchy "
        "z tela bunky (vedenie odstredivé / celulifugálne). Neuróny komunikujú s inými nervovými alebo efektorovými bunkami prostredníctvom synapsií."
    ),
    400: (
        "Dostredivé výbežky nervovej bunky sa nazývajú dendrity – vedú elektrické podráždenie dostredivo, teda smerom do tela bunky (celulipetálne). "
        "Bývajú spravidla početné, relatívne krátke a bohato stromovito rozvetvené, pričom na svojom povrchu vytvárajú synaptické spoje s inými "
        "neurónmi. Odstredivým výbežkom vedúcim vzruch z tela bunky je neurit (axón)."
    )
}

print(f"Defined explanations for {len(explanations)} questions.")

# Update questions
updated_count = 0
for i, q in enumerate(questions):
    q_num = 351 + i
    # Verify q_num matches question content
    assert str(q_num) in q['content'], f"Mismatch: expected {q_num} in {q['content']}"
    assert q_num in explanations, f"Missing explanation for {q_num}"
    q['explanation'] = explanations[q_num]
    updated_count += 1

out_path = 'scripts/bio_batches/batch_8_explained.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully updated {updated_count} questions and saved to {out_path}.")

# Verification
with open(out_path, 'r', encoding='utf-8') as f:
    verified_data = json.load(f)

assert len(verified_data) == 50, f"Expected 50 items, found {len(verified_data)}"
for idx, item in enumerate(verified_data):
    assert len(item['explanation'].strip()) > 30, f"Explanation too short at index {idx}"
    assert not item['explanation'].startswith("Správna odpoveď podľa"), f"Old explanation text at index {idx}"

print("All 50 questions verified successfully!")
print("\n--- First question (351) ---")
print(verified_data[0]['content'])
print(verified_data[0]['explanation'])
print("\n--- Second question (352) ---")
print(verified_data[1]['content'])
print(verified_data[1]['explanation'])

