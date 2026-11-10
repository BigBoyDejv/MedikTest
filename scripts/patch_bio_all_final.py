import json
import urllib.request
import os
import sys
import re

sys.path.insert(0, os.path.abspath("."))
from scripts.merge_and_upload_bio import env, url, key, get_admin_token

PATCH_SYS = {
    1260: {
        "content": "1260. Námeľ je:",
        "options": [
            {"id": "a", "text": "drevokazovitá huba"},
            {"id": "b", "text": "útvar, ktorý vzniká v dôsledku pôsobenia parazitujúcej huby u rôznych druhov lipnicovitých"},
            {"id": "c", "text": "pestovaný umelo najmä na raži siatej"},
            {"id": "d", "text": "infikovaný semenník raži premenený na tvrdý, černastý útvar"},
            {"id": "e", "text": "tmavý, rôžkovitý útvar obsahujúci alkaloidy"},
            {"id": "f", "text": "ražná hubka"},
            {"id": "g", "text": "vačkovitý nádor na kukurici"},
            {"id": "h", "text": "surovina na výrobu liekov na úpravu krvného tlaku"}
        ]
    },
    1265: {
        "content": "1265. Ako huby spájavé sa označujú:",
        "options": [
            {"id": "a", "text": "napr. peronospóra"},
            {"id": "b", "text": "napr. pleseň hlavičkatá"},
            {"id": "c", "text": "paplesňotvaré huby"},
            {"id": "d", "text": "micelárne huby"},
            {"id": "e", "text": "endomycéty"},
            {"id": "f", "text": "bazídiové huby"},
            {"id": "g", "text": "spájavé plesne"},
            {"id": "h", "text": "Zygomycetes"}
        ]
    },
    1267: {
        "content": "1267. Kyjanička purpurová:",
        "options": [
            {"id": "a", "text": "cudzopasí na rybách"},
            {"id": "b", "text": "cudzopasí na raži"},
            {"id": "c", "text": "vytvára útvar nazývaný námeľ"},
            {"id": "d", "text": "patrí medzi bazídiové huby"},
            {"id": "e", "text": "sa využíva pri výrobe liečiv"},
            {"id": "f", "text": "môže spôsobovať hromadné otravy poľnohospodárskych zvierat"},
            {"id": "g", "text": "patrí medzi vreckaté huby"},
            {"id": "h", "text": "môže produkovať toxické látky"}
        ]
    },
    1271: {
        "content": "1271. Červené riasy (Rhodophyta):",
        "options": [
            {"id": "a", "text": "charakterizuje červené farbivo – fukoxantín"},
            {"id": "b", "text": "sa využívajú na produkciu antibiotík"},
            {"id": "c", "text": "sa využívajú na produkciu agaru"},
            {"id": "d", "text": "sa využívajú na produkciu látok využívaných v mikrobiológii"},
            {"id": "e", "text": "patria medzi vyššie rastliny"},
            {"id": "f", "text": "patria medzi nižšie rastliny"},
            {"id": "g", "text": "charakterizuje červené farbivo – fykoerytrín"},
            {"id": "h", "text": "sú zastúpené predovšetkým chaluhami"}
        ]
    },
    1275: {
        "content": "1275. Zelené riasy sa rozdeľujú na triedy:",
        "options": [
            {"id": "a", "text": "zelené bičíkovce, vláknité zelené riasy, bunkové zelené riasy"},
            {"id": "b", "text": "vlastné zelené riasy a zelené bičíkovce"},
            {"id": "c", "text": "chaluhy a cháry"},
            {"id": "d", "text": "Chlorophyceae, Conjugatophyceae, Charophyceae"},
            {"id": "e", "text": "rozsievky a hnedé riasy"},
            {"id": "f", "text": "vlastné zelené riasy, spájavky a cháry"},
            {"id": "g", "text": "kryptomonády a panciernatky"},
            {"id": "h", "text": "cháry, spájavky, zelené bičíkovce"}
        ]
    },
    1281: {
        "content": "1281. Rozsievky:",
        "options": [
            {"id": "a", "text": "majú bunkovú stenu inkrustovanú oxidom kremičitým"},
            {"id": "b", "text": "majú jednobunkovú stielku obsahujúcu v plastidoch hnedé farbivá"},
            {"id": "c", "text": "vytvárajú sedimentačnú horninu známu ako diatomit (biolit)"},
            {"id": "d", "text": "sú mikroskopické organizmy"},
            {"id": "e", "text": "sú jednobunkové riasy"},
            {"id": "f", "text": "žijú len v kolóniách"},
            {"id": "g", "text": "patria do triedy hnedé riasy"},
            {"id": "h", "text": "majú v bunkovej stene oxid vápenatý"}
        ]
    },
    1285: {
        "content": "1285. Označte nesprávne odpovede:",
        "options": [
            {"id": "a", "text": "oplodnenie pri semenných rastlinách je viazané na prítomnosť vody"},
            {"id": "b", "text": "ihličnany sú prevažne jednodomé stromy"},
            {"id": "c", "text": "semenné rastliny sú rôznovýtrusné"},
            {"id": "d", "text": "šišky smreka obyčajného visia smerom nadol a opadávajú vcelku"},
            {"id": "e", "text": "ihličnany sú najčastejšie dvojdomé rastliny"},
            {"id": "f", "text": "magnóliorasty patria medzi nahosemenné rastliny"},
            {"id": "g", "text": "ginkgo dvojlaločné patrí do radu tisotvaré"},
            {"id": "h", "text": "ihličnany sú triedou oddelenia borovicorasty"}
        ]
    },
    1286: {
        "content": "1286. Označte správne odpovede:",
        "options": [
            {"id": "a", "text": "sporofyt vytvára výtrusy, gametofyt pohlavné bunky"},
            {"id": "b", "text": "gametofyt vytvára výtrusy, sporofyt pohlavné bunky"},
            {"id": "c", "text": "riasy patria medzi semenné rastliny"},
            {"id": "d", "text": "telo semenných rastlín tvorí diferencovaná stielka"},
            {"id": "e", "text": "u machorastov je dominantné štádium gametofytu"},
            {"id": "f", "text": "sladičorasty sú výtrusné rastliny"},
            {"id": "g", "text": "porastnica mnohotvárna je dvojdomá rastlina"},
            {"id": "h", "text": "jasene, bresty a duby sú dreviny mäkkého lúžneho lesa"}
        ]
    },
    1297: {
        "content": "1297. Biogenetický zákon:",
        "options": [
            {"id": "a", "text": "tvrdí, že všetky vlastnosti organizmov sa prenášajú z rodičov na potomkov"},
            {"id": "b", "text": "tvrdí, že organizmy prekonávajú vo svojom embryonálnom vývine skrátený vývoj – fylogenézu"},
            {"id": "c", "text": "charakterizuje podstatu prenosu génov z generácie na generáciu"},
            {"id": "d", "text": "vyjadruje, že každý organizmus uskutočňuje vo svojej fylogenéze skrátenú ontogenézu"},
            {"id": "e", "text": "sa nazýva tiež zákon rekapitulácie"},
            {"id": "f", "text": "tvrdí, že všetky organizmy prekonávajú v svojom embryonálnom vývine skrátený vývoj – ontogenézu"},
            {"id": "g", "text": "sa nazýva tiež zákon retrospektívy"},
            {"id": "h", "text": "tvrdí, že všetky biologické vlastnosti organizmu sú podmienené geneticky"}
        ]
    },
    1298: {
        "content": "1298. Označte správne usporiadanie systematických jednotiek od najvyššej po najnižšiu:",
        "options": [
            {"id": "a", "text": "ríša, kmeň, trieda, rad, čeľaď, rod, druh"},
            {"id": "b", "text": "rad, čeľaď, rod, druh, ríša, kmeň, trieda"},
            {"id": "c", "text": "kmeň, ríša, trieda, čeľaď, rad, rod, druh"},
            {"id": "d", "text": "ríša, kmeň, podkmeň, trieda, rad, čeľaď, rod, druh"},
            {"id": "e", "text": "kmeň, trieda, ríša, rad, čeľaď, rod, druh"},
            {"id": "f", "text": "ríša, trieda, kmeň, rad, čeľaď, druh, rod"},
            {"id": "g", "text": "ríša, kmeň, trieda, podtrieda, rad, čeľaď, rod, druh"},
            {"id": "h", "text": "druh, rod, čeľaď, rad, trieda, kmeň, ríša"}
        ]
    },
    1302: {
        "content": "1302. Meňavka červienková:",
        "options": [
            {"id": "a", "text": "v agresívnej forme magna spôsobuje krvácanie do čreva a hnačky"},
            {"id": "b", "text": "v neškodnej forme minuta sa živí črevnými baktériami"},
            {"id": "c", "text": "spôsobuje v niektorých oblastiach epidémie"},
            {"id": "d", "text": "patrí medzi cudzopasné výtrusovce"},
            {"id": "e", "text": "patrí medzi cudzopasné koreňonožce"},
            {"id": "f", "text": "žije v čreve človeka v troch formách: minuta, magna a cysta"},
            {"id": "g", "text": "v agresívnej forme minuta napáda črevný epitel"},
            {"id": "h", "text": "v neškodnej forme magna sa živí črevnými baktériami"}
        ]
    },
    1303: {
        "content": "1303. Toxoplazma gondii:",
        "options": [
            {"id": "a", "text": "patrí medzi výtrusovce"},
            {"id": "b", "text": "vyvoláva zápal mozgových blán"},
            {"id": "c", "text": "patrí medzi nálevníky"},
            {"id": "d", "text": "vyvoláva spavú nemoc"},
            {"id": "e", "text": "môže spôsobiť potratenie plodu"},
            {"id": "f", "text": "môže spôsobiť poškodenie plodu"},
            {"id": "g", "text": "sa prenáša pohlavným stykom"},
            {"id": "h", "text": "sa prenáša cystami pri nedostatočnej hygiene"}
        ]
    },
    1311: {
        "content": "1311. Zástupcovia kmeňa hubky (Porifera):",
        "options": [
            {"id": "a", "text": "žijú prisadnuto"},
            {"id": "b", "text": "trávia svoju potravu intracelulárne"},
            {"id": "c", "text": "majú telo lúčovito súmerné"},
            {"id": "d", "text": "majú telo nepravidelného tvaru"},
            {"id": "e", "text": "sú výhradne vodné živočíchy, ale patria tu i suchozemské živočíchy"},
            {"id": "f", "text": "dráždivú činnosť prejavujú až v dospelosti"},
            {"id": "g", "text": "sa rozmnožujú pohlavne i nepohlavne"},
            {"id": "h", "text": "v nepriaznivých podmienkach vytvárajú vnútorné puky – gemule"}
        ]
    },
    1312: {
        "content": "1312. Pŕhlivce:",
        "options": [
            {"id": "a", "text": "už majú pohlavné žľazy a oplodnenie je vnútorné"},
            {"id": "b", "text": "majú vysokú schopnosť regenerácie"},
            {"id": "c", "text": "patria sem 4 triedy: polypovce, medúzovce, štvorhranovce a koraly"},
            {"id": "d", "text": "sú vždy dravé živočíchy"},
            {"id": "e", "text": "majú telo lúčovito súmerné"},
            {"id": "f", "text": "majú telo dvojstranne súmerné"},
            {"id": "g", "text": "majú gastrovaskulárnu sústavu"},
            {"id": "h", "text": "majú difúznu nervovú sústavu"}
        ]
    },
    1313: {
        "content": "1313. Trojlistovce - Triblastica:",
        "options": [
            {"id": "a", "text": "majú telo tvorené ektodermom, endodermom a mezodermom"},
            {"id": "b", "text": "sú oproti dvojlistovcom na vyššom fylogenetickom stupni"},
            {"id": "c", "text": "sú oproti dvojstranovcom na vyššom fylogenetickom stupni"},
            {"id": "d", "text": "majú telo dvojstranne i lúčovito súmerné"},
            {"id": "e", "text": "sú všetky dvojstranne súmerné a preto sa nazývajú tiež dvojstranovce – Bilateralia"},
            {"id": "f", "text": "majú telo vždy tvorené troma zárodočnými vrstvami – ektodermom, endodermom a mezenchýmom"},
            {"id": "g", "text": "sa delia na prvoúste a druhoúste"},
            {"id": "h", "text": "sa delia na prvoúste, kde z prvotného otvoru – prvoúst vzniká análny otvor a ústny sa znovu otvorí a na druhoúste, kde na mieste prvoúst vznikajú ústa a análny otvor sa znovu otvára"}
        ]
    },
    1316: {
        "content": "1316. Ploskavce (Plathelminthes):",
        "options": [
            {"id": "a", "text": "nemajú vo svojom vývine larvu"},
            {"id": "b", "text": "majú črevo bez análneho otvoru"},
            {"id": "c", "text": "dýchajú protonefrídiami"},
            {"id": "d", "text": "dýchajú celým povrchom tela"},
            {"id": "e", "text": "sú voľne žijúce i parazitické živočíchy"},
            {"id": "f", "text": "sú dvojstranne súmerné"},
            {"id": "g", "text": "nie sú v žiadnom prípade parazity"},
            {"id": "h", "text": "majú zmyslové orgány tvorené miskovitými očami"}
        ]
    },
    1321: {
        "content": "1321. Označte správne odpovede:",
        "options": [
            {"id": "a", "text": "Trichinella spiralis spôsobuje zdurenie a gigantizmus častí tela"},
            {"id": "b", "text": "hlísty a mrle patria medzi hlístovce"},
            {"id": "c", "text": "pijavice patria k ektoparazitom"},
            {"id": "d", "text": "Enterobius vermicularis vyvoláva nočné svrbenie"},
            {"id": "e", "text": "mnohé hlístovce dokážu žiť aj v podmienkach bez kyslíka"},
            {"id": "f", "text": "dracunkulózu spôsobuje vlasovec medinský"},
            {"id": "g", "text": "Ascaris lumbricoides dosahuje veľkosť do 20 mm"},
            {"id": "h", "text": "medzi hlístovce patria aj parazity rastlín"}
        ]
    },
    1322: {
        "content": "1322. Pásomnice:",
        "options": [
            {"id": "a", "text": "sú hermafrodity"},
            {"id": "b", "text": "potravu prijímajú celým povrchom tela"},
            {"id": "c", "text": "majú na prednom konci tela ústny otvor, potom hltan a rozkonárené črevo"},
            {"id": "d", "text": "dosahujú dĺžku až 10 m"},
            {"id": "e", "text": "sú gonochoristy"},
            {"id": "f", "text": "nemajú gastrovaskulárnu sústavu"},
            {"id": "g", "text": "patria k ektoparazitom"},
            {"id": "h", "text": "patria k zooparazitom"}
        ]
    },
    1326: {
        "content": "1326. U zástupcov kmeňa mäkkýše (Mollusca):",
        "options": [
            {"id": "a", "text": "sa nachádza hemolymfa"},
            {"id": "b", "text": "sa v ústach nachádza ozubený strúhací orgán – planula"},
            {"id": "c", "text": "sa nachádza krvomiazga"},
            {"id": "d", "text": "sa už vyskytuje lymfa"},
            {"id": "e", "text": "nachádzame rozptýlenú nervovú sústavu"},
            {"id": "f", "text": "sa vyskytuje vonkajšie oplodnenie"},
            {"id": "g", "text": "sa v ústach nachádza ozubený strúhací orgán – radula"},
            {"id": "h", "text": "sa vyskytuje vnútorné oplodnenie"}
        ]
    },
    1332: {
        "content": "1332. Článkonožce majú:",
        "options": [
            {"id": "a", "text": "na každom článku pár článkovaných končatín"},
            {"id": "b", "text": "uzatvorenú cievnu sústavu"},
            {"id": "c", "text": "hydrolymfu"},
            {"id": "d", "text": "otvorenú cievnu sústavu"},
            {"id": "e", "text": "homonómnu článkovanosť tela"},
            {"id": "f", "text": "na každom článku pár tykadiel"},
            {"id": "g", "text": "heteronómnu článkovanosť tela"},
            {"id": "h", "text": "hemolymfu"}
        ]
    },
    1336: {
        "content": "1336. Pri kôrovcoch:",
        "options": [
            {"id": "a", "text": "veľmi pokročila diferenciácia končatín"},
            {"id": "b", "text": "sa končatiny nachádzajú aj na brušku"},
            {"id": "c", "text": "sa končatiny nachádzajú len na hlavohrudi"},
            {"id": "d", "text": "sa nachádza statocysta"},
            {"id": "e", "text": "už nachádzame rovnovážny orgán"},
            {"id": "f", "text": "sú končatiny dvojvetvové"},
            {"id": "g", "text": "niektoré druhy v nepriaznivých podmienkach vytvárajú statocystu"},
            {"id": "h", "text": "na rozdiel od klepietkavcov nedochádza k diferenciácii končatín"}
        ]
    },
    1337: {
        "content": "1337. Označte nesprávne odpovede:",
        "options": [
            {"id": "a", "text": "larvy blchy ľudskej sa vyvíjajú mimo tela človeka"},
            {"id": "b", "text": "Yersinia pestis je pôvodcom moru"},
            {"id": "c", "text": "blcha ľudská je endoparazit"},
            {"id": "d", "text": "samička vši detskej nakladie počas života asi 3 000 vajíčok"},
            {"id": "e", "text": "ploštica posteľná patrí medzi bzdochy"},
            {"id": "f", "text": "ploštica posteľná sa živí odumretými bunkami ľudskej pokožky"},
            {"id": "g", "text": "iba samčeky komára piskľavého sa živia paraziticky"},
            {"id": "h", "text": "samičky komára piskľavého sa živia rastlinnými šťavami"}
        ]
    },
    1340: {
        "content": "1340. Chrobáky:",
        "options": [
            {"id": "a", "text": "prechádzajú počas svojho vývinu úplnou premenou"},
            {"id": "b", "text": "majú slabo vyvinuté, zakrpatené tykadlá"},
            {"id": "c", "text": "majú druhý pár krídel blanitý"},
            {"id": "d", "text": "majú prvý pár krídel premenený na krovky"},
            {"id": "e", "text": "sa počas svojho vývinu zakukľujú"},
            {"id": "f", "text": "patria k hmyzu s neúplnou premenou"},
            {"id": "g", "text": "majú druhý pár krídel premenený na krovky"},
            {"id": "h", "text": "majú vzdušnice umiestnené i v krídlach"}
        ]
    },
    1341: {
        "content": "1341. Komár Anofeles môže prenášať na človeka:",
        "options": [
            {"id": "a", "text": "blchy"},
            {"id": "b", "text": "krvinkovky"},
            {"id": "c", "text": "kokcídie"},
            {"id": "d", "text": "ochorenie tse-tse"},
            {"id": "e", "text": "spavú nemoc"},
            {"id": "f", "text": "mor"},
            {"id": "g", "text": "škvrnitý týfus"},
            {"id": "h", "text": "pôvodcu malárie"}
        ]
    },
    1352: {
        "content": "1352. Neoténia:",
        "options": [
            {"id": "a", "text": "môže byť výsledkom osobitnej evolúcie"},
            {"id": "b", "text": "sa nazýva tiež hibernácia"},
            {"id": "c", "text": "je jav, keď sa živočíchy nikdy nevyvinú do podoby dospelých jedincov"},
            {"id": "d", "text": "je typická napr. pre axolotla a jaskyniara"},
            {"id": "e", "text": "je jav, keď aj v dospelosti si živočíchy zachovávajú niektoré larválne znaky"},
            {"id": "f", "text": "sa nazýva tiež juvenilizácia"},
            {"id": "g", "text": "môže byť dôsledkom určitých podmienok prostredia"},
            {"id": "h", "text": "je jav, keď larválne štádium má určité znaky dospelého živočícha"}
        ]
    },
    1362: {
        "content": "1362. V čreve človeka parazituje:",
        "options": [
            {"id": "a", "text": "háďatko"},
            {"id": "b", "text": "pásomnica dlhá"},
            {"id": "c", "text": "Lucilia sericata"},
            {"id": "d", "text": "hlísta detská"},
            {"id": "e", "text": "Enterobius vermicularis"},
            {"id": "f", "text": "vlasovec miazgový"},
            {"id": "g", "text": "motolica"},
            {"id": "h", "text": "mrľa ľudská"}
        ]
    }
}

PATCH_EKO = {
    1366: {
        "content": "1366. Vývoj na Zemi možno rozdeliť na dva hlavné eóny:",
        "options": [
            {"id": "a", "text": "prekambrium a kambrium"},
            {"id": "b", "text": "prekambrium a kenozoikum"},
            {"id": "c", "text": "kenozoikum a fanerozoikum"},
            {"id": "d", "text": "prekambrium a fanerozoikum"},
            {"id": "e", "text": "kambrium a fanerozoikum"},
            {"id": "f", "text": "kambrium a paleozoikum"},
            {"id": "g", "text": "paleozoikum a fanerozoikum"},
            {"id": "h", "text": "kenozoikum a paleozoikum"}
        ]
    },
    1378: {
        "content": "1378. Vychladnutie severnej pologule a rozšírenie človeka nastalo:",
        "options": [
            {"id": "a", "text": "v treťohorách"},
            {"id": "b", "text": "v štvrtohorách"},
            {"id": "c", "text": "v druhohorách"},
            {"id": "d", "text": "v paleocéne"},
            {"id": "e", "text": "v pleistocéne"},
            {"id": "f", "text": "v kriede"},
            {"id": "g", "text": "v miocéne"},
            {"id": "h", "text": "v kenozoiku"}
        ]
    },
    1390: {
        "content": "1390. Proces, ktorým vznikol rod človek sa nazýva:",
        "options": [
            {"id": "a", "text": "homidizácia"},
            {"id": "b", "text": "sapientácia"},
            {"id": "c", "text": "antropizácia"},
            {"id": "d", "text": "progresia"},
            {"id": "e", "text": "hominizácia"},
            {"id": "f", "text": "bipédia"},
            {"id": "g", "text": "habilitácia"},
            {"id": "h", "text": "humanizácia"}
        ]
    },
    1401: {
        "content": "1401. Epocha oligocén je časťou:",
        "options": [
            {"id": "a", "text": "prvohôr"},
            {"id": "b", "text": "prekambria"},
            {"id": "c", "text": "štvrtohôr"},
            {"id": "d", "text": "treťohôr"},
            {"id": "e", "text": "druhohôr"},
            {"id": "f", "text": "kenozoika"},
            {"id": "g", "text": "prechodného obdobia medzi mezozoikom a kenozoikom"},
            {"id": "h", "text": "mezozoika"}
        ]
    },
    1411: {
        "content": "1411. Organizmus zahynie, ak:",
        "options": [
            {"id": "a", "text": "všetky podmienky prostredia pre život organizmu sú nevhodné"},
            {"id": "b", "text": "minimálne jedna základná ekologická podmienka prostredia je pre život organizmu nevhodná"},
            {"id": "c", "text": "všetky podmienky prostredia sú v ekologickej valencii"},
            {"id": "d", "text": "aspoň jedna základná ekologická podmienka prostredia klesne pod minimálnu (dolnú) hranicu tolerancie organizmu"},
            {"id": "e", "text": "aspoň jedna základná ekologická podmienka prostredia presiahne maximálnu (hornú) hranicu tolerancie organizmu"},
            {"id": "f", "text": "všetky podmienky prostredia sú optimálne"},
            {"id": "g", "text": "má narušený biotický potenciál"},
            {"id": "h", "text": "aspoň jedna podmienka prostredia je v optime"}
        ]
    },
    1424: {
        "content": "1424. Stúpajúce množstvo CO2 v ovzduší:",
        "options": [
            {"id": "a", "text": "ak je nepatrné, môže spôsobiť zvýšenie intenzity fotosyntézy"},
            {"id": "b", "text": "neovplyvňuje podnebie"},
            {"id": "c", "text": "ovplyvňuje vznik skleníkového efektu"},
            {"id": "d", "text": "je spôsobené najmä vulkanickou činnosťou"},
            {"id": "e", "text": "vyvoláva oteplenie"},
            {"id": "f", "text": "môže spôsobiť rozširovanie tropického podnebia"},
            {"id": "g", "text": "môže spôsobiť rozširovanie arktického podnebia"},
            {"id": "h", "text": "nemá žiaden vplyv na teplotu biosféry"}
        ]
    },
    1425: {
        "content": "1425. Označte správne odpovede:",
        "options": [
            {"id": "a", "text": "rozpätie hodnôt ekologického faktora, ktoré organizmus znáša, sa označuje ako tolerancia organizmu"},
            {"id": "b", "text": "schopnosť organizmu znášať rôzne podmienky prostredia je ekologická valencia organizmu"},
            {"id": "c", "text": "organizmom sa najlepšie darí v oblasti optima ekologického faktora"},
            {"id": "d", "text": "hraničné podmienky ekologického faktora sú pesimum"},
            {"id": "e", "text": "kozmopolitné organizmy majú širokú ekologickú valenciu"},
            {"id": "f", "text": "bioindikátory majú väčšinou úzku ekologickú valenciu k niektorej podmienke prostredia"},
            {"id": "g", "text": "medzidruhové vzťahy môžu byť neutrálne"},
            {"id": "h", "text": "symbióza patrí k záporným medzidruhovým vzťahom"}
        ]
    },
    1433: {
        "content": "1433. Označte správnu odpoveď:",
        "options": [
            {"id": "a", "text": "slnečné žiarenie je základným zdrojom energie pre život na Zemi"},
            {"id": "b", "text": "teplo ovplyvňuje rýchlosť a priebeh životných procesov"},
            {"id": "c", "text": "lokomócia je pasívny pohyb pomocou určitého prostriedku"},
            {"id": "d", "text": "O2 (78%) vo vzduchu je podmienkou dýchania"},
            {"id": "e", "text": "chorobnosť sa ináč nazýva aj mortalita"},
            {"id": "f", "text": "viditeľné svetlo je dôležité pre fotosyntézu"},
            {"id": "g", "text": "rýchlosť rastu populácie závisí najmä od pomeru natality a mortality organizmov"},
            {"id": "h", "text": "lišajníky sú tvorené autotrofnými riasami alebo sinicami a hubovými vláknami"}
        ]
    },
    1434: {
        "content": "1434. Označte správne odpovede:",
        "options": [
            {"id": "a", "text": "lišajník je príkladom symbiózy"},
            {"id": "b", "text": "parazit svojho hostiteľa zvyčajne zabíja"},
            {"id": "c", "text": "parazit odčerpáva hostiteľovi živiny"},
            {"id": "d", "text": "príkladom komenzalizmu je epifyt rastúci na strome"},
            {"id": "e", "text": "korisť sa živí predátorom"},
            {"id": "f", "text": "konkurencia je zvyčajne vzťah medzi druhmi s rovnakou ekologickou nikou"},
            {"id": "g", "text": "predátor loví korisť"},
            {"id": "h", "text": "pri neutralizme sú organizmy od seba nezávislé"}
        ]
    },
    1439: {
        "content": "1439. Druhy schopné znášať len malé kolísanie faktorov životného prostredia sa nazývajú:",
        "options": [
            {"id": "a", "text": "euryekné"},
            {"id": "b", "text": "stenoekné"},
            {"id": "c", "text": "bioindikátory"},
            {"id": "d", "text": "fytoindikátory"},
            {"id": "e", "text": "stenovalentné"},
            {"id": "f", "text": "synantropné"},
            {"id": "g", "text": "alelopatické"},
            {"id": "h", "text": "planktonické"}
        ]
    },
    1444: {
        "content": "1444. Ktoré tvrdenie je nesprávne:",
        "options": [
            {"id": "a", "text": "v ústiach riek do mora sú brakické vody"},
            {"id": "b", "text": "sladká voda má najvyššiu hustotu pri 0°C"},
            {"id": "c", "text": "svetlo vo vode preniká len do hĺbky asi 200 m"},
            {"id": "d", "text": "fytoplanktón tvoria aj drobné kôrovce a larvy mäkkýšov"},
            {"id": "e", "text": "zooplanktón tvoria aj sinice"},
            {"id": "f", "text": "planktónom sa živia napr. hubky a lastúrniky"},
            {"id": "g", "text": "baktérie završujú kolobeh látok v prírode"},
            {"id": "h", "text": "voda má najväčšiu hustotu pri teplote 14°C"}
        ]
    },
    1445: {
        "content": "1445. Habitus:",
        "options": [
            {"id": "a", "text": "je súbor genetických znakov vlastných všetkým členom určitej populácie"},
            {"id": "b", "text": "je súbor morfologických znakov vlastných niektorým jedincom populácie"},
            {"id": "c", "text": "súbor morfologických znakov vlastných všetkým členom určitej populácie"},
            {"id": "d", "text": "predstavuje napr. tvar tela a sfarbenie jedincov populácie"},
            {"id": "e", "text": "predstavuje napr. veľkosť, hmotnosť jedincov populácie"},
            {"id": "f", "text": "závisí od natality"},
            {"id": "g", "text": "závisí od hustoty populácie"},
            {"id": "h", "text": "je daný podielom hynutia jedincov v populácii za časovú jednotku"}
        ]
    },
    1449: {
        "content": "1449. Mortalita:",
        "options": [
            {"id": "a", "text": "označuje populáciu rýb žijúcu v mori"},
            {"id": "b", "text": "je úmrtnosť jedincov v populácii vyjadrená počtom jedincov uhynutých za určitú časovú jednotku"},
            {"id": "c", "text": "je pôrodnosť jedincov v populácii"},
            {"id": "d", "text": "je v dlhšom časovom úseku vyrovnávaná prírastkom v populácii, čím sa udržiava približne rovnaká hustota"},
            {"id": "e", "text": "ak nastáva prirodzeným spôsobom, je pre veľkosť a štruktúru populácie potrebná"},
            {"id": "f", "text": "je schopnosť populácie rozmnožovať sa"},
            {"id": "g", "text": "medzi tatranské glaciálne relikty patrí dryádka osemlupienková"},
            {"id": "h", "text": "endemity sú druhy vyskytujúce sa výhradne na určitom území"}
        ]
    },
    1459: {
        "content": "1459. Označte správnu odpoveď:",
        "options": [
            {"id": "a", "text": "prechodnou formou medzi rybami a obojživelníkmi boli krytolebce"},
            {"id": "b", "text": "vekom obojživelníkov nazývame karbón"},
            {"id": "c", "text": "prvé plazy vznikli z násadcoplutvých rýb"},
            {"id": "d", "text": "priamymi predchodcami cicavcov boli zverotvaré plazy"},
            {"id": "e", "text": "v priebehu evolúcie sa vtáky vyvinuli z plazov"},
            {"id": "f", "text": "všetky dnes žijúce organizmy majú spoločného predchodcu"},
            {"id": "g", "text": "makroevolúcia sa odohráva na úrovni jedinca"},
            {"id": "h", "text": "náhodné kolísanie početnosti alel je tým väčšie, čím je populácia väčšia"}
        ]
    },
    1464: {
        "content": "1464. Rudimentárne orgány:",
        "options": [
            {"id": "a", "text": "majú pre daný organizmus podstatný význam"},
            {"id": "b", "text": "majú pre organizmus minimálny alebo žiadny význam"},
            {"id": "c", "text": "sú historickým pozostatkom štruktúr, zohrávajúcich významnú úlohu v živote dávnych predkov daného organizmu"},
            {"id": "d", "text": "sú napríklad krídla vtákov"},
            {"id": "e", "text": "sú napríklad zadné končatiny a panva u veľrýb"},
            {"id": "f", "text": "sú vždy novovytvorené orgány u daného jedinca"},
            {"id": "g", "text": "sú všetky orgány jedinca"},
            {"id": "h", "text": "sú napríklad kostrč a červovitý prívesok slepého čreva u človeka"}
        ]
    },
    1466: {
        "content": "1466. Vyberte správne tvrdenia: reprodukčná bariéra",
        "options": [
            {"id": "a", "text": "zabraňuje vzájomnému kríženiu medzi príslušníkmi rôznych druhov"},
            {"id": "b", "text": "mulica a tapír sú príkladom neplodných hybridov"},
            {"id": "c", "text": "liger a tiglon sú schopní ďalšieho rozmnožovania"},
            {"id": "d", "text": "evolúcia jedného druhu môže ovplyvňovať aj ostatné druhy"},
            {"id": "e", "text": "geografická bariéra je najznámejším príkladom reprodukčnej bariéry"},
            {"id": "f", "text": "mutácie sú zdrojom evolučných noviniek"},
            {"id": "g", "text": "pôsobením prírodnej selekcie nevznikajú nové gény"},
            {"id": "h", "text": "reprodukčnou bariérou môžu byť aj odlišnosti v organizácii genetického materiálu"}
        ]
    },
    1468: {
        "content": "1468. Označte nesprávne odpovede:",
        "options": [
            {"id": "a", "text": "podľa kreacionizmu sa druhy v priebehu času nemenia"},
            {"id": "b", "text": "podľa transformizmu sa druhy v priebehu času nemenia"},
            {"id": "c", "text": "organizmy majú tendenciu produkovať viac potomstva ako je prostredie schopné uživiť"},
            {"id": "d", "text": "selekcia prírodou je podľa darwinizmu hybnou silou evolúcie dlhého časového obdobia druhu"},
            {"id": "e", "text": "podľa kreacionizmu druhy vznikli evolučným vývojom"},
            {"id": "f", "text": "podľa lamarckizmu organizmy získané vlastnosti nededia"},
            {"id": "g", "text": "podľa darwinizmu jedince v populácii nie sú premenlivé"},
            {"id": "h", "text": "selekcia prírodou podporuje prežitie najmenej prispôsobených jedincov"}
        ]
    },
    1473: {
        "content": "1473. Progenot:",
        "options": [
            {"id": "a", "text": "je hypotetický spoločný predok všetkých organizmov"},
            {"id": "b", "text": "je iné označenie pre sinice"},
            {"id": "c", "text": "je nefunkčný gén"},
            {"id": "d", "text": "je prabunka"},
            {"id": "e", "text": "je predchodca baktérií, archeónov a eukaryotov"},
            {"id": "f", "text": "mal v jednoduchej podobe rozvinuté všetky vlastnosti života"},
            {"id": "g", "text": "je prabunka, v ktorej pravdepodobne prebiehali procesy translácie RNA"},
            {"id": "h", "text": "je prabunka, v ktorej pravdepodobne prebiehali procesy replikácie DNA"}
        ]
    },
    1477: {
        "content": "1477. Označte správnu odpoveď:",
        "options": [
            {"id": "a", "text": "počas evolúcie sa najprv vyvinuli eukaryotické organizmy"},
            {"id": "b", "text": "všetky dnes žijúce organizmy majú jedného spoločného predchodcu"},
            {"id": "c", "text": "prvé prokaryotické organizmy sa objavili pred viac ako 3,5 miliardami rokov"},
            {"id": "d", "text": "prvé eukaryotické bunky vznikli pred približne 1,8 miliardami rokov"},
            {"id": "e", "text": "evolúcia života na bunkovej úrovni trvala na Zemi viac ako 3 miliardy rokov"},
            {"id": "f", "text": "archeóny sú schopné života pri teplotách až 113°C"},
            {"id": "g", "text": "ribozým je katalyticky aktívna molekula DNA"},
            {"id": "h", "text": "eukaryotické organizmy vznikli skôr ako baktérie a archeóny"}
        ]
    },
    1483: {
        "content": "1483. Označte správnu odpoveď:",
        "options": [
            {"id": "a", "text": "proces záverečnej fázy vývoja človeka sa nazýva antropogenetika"},
            {"id": "b", "text": "Homo sapiens sa vyvinul na americkom kontinente"},
            {"id": "c", "text": "Homo habilis sa vyvinul na území Ázie"},
            {"id": "d", "text": "Homo sapiens sa vyvinul v Afrike"},
            {"id": "e", "text": "Homo habilis sa ináč nazýva aj ako človek vzpriamený"},
            {"id": "f", "text": "človek zručný sa ináč nazýva aj ako Homo erectus"},
            {"id": "g", "text": "pri sapientácii ide najmä o rozvoj mozgu a myslenia"},
            {"id": "h", "text": "pri sapientácii ide najmä o zmeny súvisiace s bipédiou"}
        ]
    },
    1485: {
        "content": "1485. Označte správnu odpoveď:",
        "options": [
            {"id": "a", "text": "v ázijských populáciách je žltý odtieň pokožky spôsobený adaptáciou na chladnejšiu klímu"},
            {"id": "b", "text": "v skupinách ľudí, ktoré sa formovali v oblastiach s vysokou intenzitou slnečného žiarenia, sa znížil obsah pigmentu v koži"},
            {"id": "c", "text": "v skupinách ľudí, ktoré sa formovali v oblastiach s vysokou intenzitou slnečného žiarenia, sa zvýšil obsah pigmentu v koži"},
            {"id": "d", "text": "v skupinách ľudí, ktoré majú pôvod v Európe, sa môže vyskytovať ružová koža, blond vlasy a modré oči"},
            {"id": "e", "text": "u obyvateľov Európy došlo počas vývoja k čiastočnej strate melanínu v dôsledku menšieho množstva slnečného žiarenia v tejto oblasti"},
            {"id": "f", "text": "u obyvateľov Európy došlo počas vývoja k zvýšeniu množstva melanínu v dôsledku menšieho množstva slnečného žiarenia v tejto oblasti"},
            {"id": "g", "text": "v skupinách ľudí, ktoré sa formovali v oblastiach s nižšou intenzitou slnečného žiarenia, sa znížil obsah pigmentu v koži"},
            {"id": "h", "text": "pred vysokými dávkami UV žiarenia sú hlboké vrstvy kože chránené zvýšeným obsahom melanínu"}
        ]
    },
    1488: {
        "content": "1488. Ekologická valencia:",
        "options": [
            {"id": "a", "text": "popisuje hustotu populácie"},
            {"id": "b", "text": "určuje rozsah tolerancie druhu"},
            {"id": "c", "text": "je pre všetky organizmy rovnaká"},
            {"id": "d", "text": "je určená minimom a maximom intenzity faktora"},
            {"id": "e", "text": "je napr. euryvalencia, ak má amplitúda a optimum faktora úzke rozpätie"},
            {"id": "f", "text": "je napr. stenovalencia, ak má amplitúda a optimum faktora široké rozpätie"},
            {"id": "g", "text": "je napr. euryvalencia, ak má amplitúda a optimum faktora široké rozpätie"},
            {"id": "h", "text": "je napr. stenovalencia, ak má amplitúda a optimum faktora úzke rozpätie"}
        ]
    },
    1491: {
        "content": "1491. Označte správnu odpoveď:",
        "options": [
            {"id": "a", "text": "kozmopolitné druhy sú rozšírené najmä v kozme"},
            {"id": "b", "text": "bioindikátory sú viazané na určitý typ biotopu"},
            {"id": "c", "text": "rastliny osídľujú na Zemi dva podstatne odlišné typy prostredia: suchozemské a vodné"},
            {"id": "d", "text": "biotop tvoria dve základné zložky: neživá – biotická a živá – abiotická"},
            {"id": "e", "text": "synantropné druhy rastlín sú často rozširované činnosťou človeka"},
            {"id": "f", "text": "symbióza je vzťah, keď jeden organizmus rastie na úkor toho druhého"},
            {"id": "g", "text": "rastlinné spoločenstvo sa ináč nazýva aj zoocenóza"},
            {"id": "h", "text": "najčastejší typ konkurencie u rastlín je mykoríza"}
        ]
    }
}

def apply_patches():
    with open("data_bio_answers_451_1500.json", "r", encoding="utf-8") as f:
        answers = {int(k): v for k, v in json.load(f).items()}

    # 1. Update Systém
    with open("data/system_rastlin_zivocichov_1251_1365.json", "r", encoding="utf-8") as f:
        sys_items = json.load(f)

    for it in sys_items:
        num = int(it["content"].split(".")[0])
        if num in PATCH_SYS:
            patch = PATCH_SYS[num]
            it["content"] = patch["content"]
            it["options"] = patch["options"]
            it["correct_answers"] = answers.get(num, [])
            it["explanation"] = f"Správne možnosti podľa oficiálneho kľúča LF UPJŠ: {', '.join([c.upper() for c in it['correct_answers']])}."

    with open("data/system_rastlin_zivocichov_1251_1365.json", "w", encoding="utf-8") as f:
        json.dump(sys_items, f, ensure_ascii=False, indent=2)
    print("Patched and saved data/system_rastlin_zivocichov_1251_1365.json")

    # 2. Update Ekológia
    with open("data/ekologia_evolucia_1366_1500.json", "r", encoding="utf-8") as f:
        eko_items = json.load(f)

    for it in eko_items:
        num = int(it["content"].split(".")[0]) if it["content"].split(".")[0].isdigit() else int(re.match(r"^(\d+)", it["content"]).group(1))
        if num in PATCH_EKO:
            patch = PATCH_EKO[num]
            it["content"] = patch["content"]
            it["options"] = patch["options"]
            it["correct_answers"] = answers.get(num, [])
            it["explanation"] = f"Správne možnosti podľa oficiálneho kľúča LF UPJŠ: {', '.join([c.upper() for c in it['correct_answers']])}."

    with open("data/ekologia_evolucia_1366_1500.json", "w", encoding="utf-8") as f:
        json.dump(eko_items, f, ensure_ascii=False, indent=2)
    print("Patched and saved data/ekologia_evolucia_1366_1500.json")

    # Verify no issues remain
    for name, items in [("Systém", sys_items), ("Ekológia", eko_items)]:
        bad = []
        for it in items:
            num = it["content"].split(".")[0]
            if "Otázka č." in it["content"] or any("Možnosť " in opt["text"] for opt in it["options"]) or len(it["options"]) != 8:
                bad.append(num)
        print(f"Verification {name}: {len(bad)} issues found: {bad}")

    # Now upload the patched items to Supabase
    admin_token = get_admin_token()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    # Upload Systém
    req = urllib.request.Request(f"{url}/rest/v1/categories?name=eq.{urllib.parse.quote('Systém rastlín a živočíchov')}&select=id", headers=headers)
    with urllib.request.urlopen(req) as resp:
        sys_cat_id = json.loads(resp.read().decode())[0]["id"]

    for num, patch in PATCH_SYS.items():
        # find question id in Supabase
        q_url = f"{url}/rest/v1/questions?category_id=eq.{sys_cat_id}&content=like.{num}.*&select=id"
        req_q = urllib.request.Request(q_url, headers=headers)
        with urllib.request.urlopen(req_q) as resp:
            qs = json.loads(resp.read().decode())
        if qs:
            qid = qs[0]["id"]
            up_body = json.dumps({
                "content": patch["content"],
                "options": patch["options"],
                "correct_answers": answers.get(num, []),
                "explanation": f"Správne možnosti podľa oficiálneho kľúča LF UPJŠ: {', '.join([c.upper() for c in answers.get(num, [])])}."
            }).encode("utf-8")
            req_up = urllib.request.Request(f"{url}/rest/v1/questions?id=eq.{qid}", data=up_body, headers=headers, method="PATCH")
            urllib.request.urlopen(req_up)

    print("Updated patched questions in Supabase category 'Systém rastlín a živočíchov'!")

    # Upload Ekológia
    req = urllib.request.Request(f"{url}/rest/v1/categories?name=eq.{urllib.parse.quote('Ekológia a evolúcia')}&select=id", headers=headers)
    with urllib.request.urlopen(req) as resp:
        eko_cat_id = json.loads(resp.read().decode())[0]["id"]

    for num, patch in PATCH_EKO.items():
        q_url = f"{url}/rest/v1/questions?category_id=eq.{eko_cat_id}&content=like.{num}*&select=id"
        req_q = urllib.request.Request(q_url, headers=headers)
        with urllib.request.urlopen(req_q) as resp:
            qs = json.loads(resp.read().decode())
        if qs:
            qid = qs[0]["id"]
            up_body = json.dumps({
                "content": patch["content"],
                "options": patch["options"],
                "correct_answers": answers.get(num, []),
                "explanation": f"Správne možnosti podľa oficiálneho kľúča LF UPJŠ: {', '.join([c.upper() for c in answers.get(num, [])])}."
            }).encode("utf-8")
            req_up = urllib.request.Request(f"{url}/rest/v1/questions?id=eq.{qid}", data=up_body, headers=headers, method="PATCH")
            urllib.request.urlopen(req_up)

    print("Updated patched questions in Supabase category 'Ekológia a evolúcia'!")

if __name__ == "__main__":
    apply_patches()
