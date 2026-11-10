# -*- coding: utf-8 -*-
import json

explanations = {
    301: (
        "Vodný roztok vykazuje neutrálne pH (pH ≈ 7), ak v ňom nedochádza k prevahe iónov H3O+ alebo OH-. "
        "V prípade solí slabých kyselín a slabých zásad s porovnateľnými disociačnými konštantami (ako NH4CN, kde Ka ≈ Kb) zostáva pH prakticky neutrálne, rovnako ako pri roztokoch solí silných kyselín a zásad (NaClO3). "
        "Podľa oficiálneho kľúča testovnice sú vyznačené možnosti c, e, f, g, pričom soli silných zásad so slabými kyselinami (CH3COOK, Na2CO3) reagujú zásadito a soli slabých zásad so silnými kyselinami (AlCl3) hydrolyzujú za vzniku kyslého prostredia."
    ),
    302: (
        "Stálosť pH (pufračnú kapacitu) voči prídavku kyseliny zabezpečujú tlmivé roztoky obsahujúce konjugovaný pár slabej kyseliny a jej soli, prípadne zmesi schopné viazať dodané oxóniové katióny. "
        "Typickým príkladom je acetátový pufer tvorený kyselinou octovou a octanom sodným (odpoveď h), prípadne zmesi kyselín a solí (b, e, f), kde prítomné anióny tlmia náhly nárast acidity. "
        "Samotné zmesi silných kyselín a hydroxidov po prekročení bodu ekvivalencie tlmivú schopnosť nemajú."
    ),
    303: (
        "Roztoky, ktorých pH sa výrazne nemení ani po prídavku menšieho množstva kyseliny alebo zásady, fungujú ako tlmivé roztoky (pufre). "
        "Patria sem fyziologicky významný hydrogénfosfátový pufer (KH2PO4/K2HPO4; odpoveď a) a hydrogénuhličitanový pufer (Na2CO3/NaHCO3; g), ktoré efektívne eliminujú pridané H+ ióny posunom protolytickej rovnováhy, ako aj zmesi v možnostiach c a h. "
        "Naopak zmesi silných minerálnych kyselín s ich neutrálnymi soľami (b, d) pufračnú schopnosť nevykazujú."
    ),
    304: (
        "Konjugovaný pár podľa Brønstedovej teórie tvorí dvojica častíc, ktoré sa navzájom líšia o jeden protón (H+). "
        "V uvedenej reakcii vystupuje kyselina octová (CH3COOH) ako kyselina a odovzdaním H+ prechádza na konjugovanú bázu acetát (CH3COO-; f), zatiaľ čo anilín (C6H5NH2) viaže protón za vzniku anilíniového katiónu (C6H5NH3+; e). "
        "Možnosti a, e, f, g predstavujú správne označené reagujúce a konjugované dvojice protolytickej rovnováhy."
    ),
    305: (
        "So vzrastajúcim oxidačným číslom chlóru v kyslíkatých kyselinách stúpa ich acidita, pretože rastúci počet atómov kyslíka odčerpáva elektrónovú hustotu a uľahčuje odštiepenie protónu. "
        "S rastúcou silou kyseliny vzrastá hodnota disociačnej konštanty Ka (odpoveď h) a zvyšuje sa aj stupeň disociácie α v roztoku (odpoveď f). "
        "V súlade s kľúčom testovnice sú správne vyznačené možnosti d, e, f, h, ktoré reflektujú termodynamické a rovnovážne parametre v rade týchto kyselín."
    ),
    306: (
        "Sila kyselín a zásad vyjadruje ich schopnosť odovzdávať alebo prijímať protón a je kvantitatívne daná disociačnou konštantou (Ka, Kb; odpoveď f). "
        "V konkrétnom roztoku sa sila elektrolytu prejavuje mierou disociácie, výslednou koncentráciou voľných iónov, hodnotou pH a počtom uvoľniteľných H+ či OH- skupín (odpovede a, b, h). "
        "Izoelektrický bod (d) charakterizuje amfióny (napr. aminokyseliny) pri nulovom čistom náboji a silu anorganických kyselín a zásad neurčuje."
    ),
    307: (
        "Zásaditú reakciu (pH > 7) majú vodné roztoky solí vytvorených zo silnej zásady a slabej kyseliny, ktorých anión podlieha zásaditej hydrolýze. "
        "Hydrolýzou octanového a hydrogénuhličitanového aniónu (CH3COOK, NaHCO3; odpoveď c), mravčanu a dusitanu (KNO2, HCOONa; g) či vínanu draselného (f) vznikajú voľné hydroxidové ióny OH-. "
        "Soli odvodené od silných kyselín a silných zásad (ako NaNO3, K2SO4; b, d) nehydrolyzujú a ich roztoky sú neutrálne."
    ),
    308: (
        "Kyslá reakcia vodného prostredia vzniká disociáciou alebo hydrolýzou, pri ktorej dochádza k uvoľňovaniu oxóniových katiónov H3O+. "
        "Možnosti a, c, g, h zahŕňajú protolytické rovnováhy a disociačné deje amfotérnych či kyslých aniónov vo vodnom roztoku. "
        "Bázické reakcie amínov a solí slabých kyselín (ako b a f) produkujú hydroxidové anióny OH-, a preto vedú k zásaditému pH."
    ),
    309: (
        "Podľa Brønstedovej teórie vystupuje voda ako kyselina vtedy, ak odovzdáva protón (H+) bázickej častici a mení sa na hydroxidový anión OH-. "
        "Tento dej prebieha pri reakcii s mravčanovým aniónom (c: HCOO- + H2O → HCOOH + OH-) aj pri protonácii amoniaku (g: NH3 + H2O → NH4+ + OH-). "
        "V možnostiach a, c, g, h vystupuje voda v protolytických procesoch ako amfotérne rozpúšťadlo schopné výmeny protónov."
    ),
    310: (
        "Vodný roztok uhličitanu draselného K2CO3 reaguje v dôsledku hydrolýzy uhličitanového aniónu zásadito (odpoveď h: CO3(2-) + H2O ⇌ HCO3- + OH-). "
        "Podľa oficiálneho kľúča testovnice sú správne možnosti a, d, e, h, ktoré vystihujú súvislosť medzi koncentráciou, rovnovážnymi konštantami a acidobázickým charakterom roztokov. "
        "Tvrdenie g neplatí, pretože roztok K2CO3 ako soli silnej zásady a slabej kyseliny nemôže byť kyslý."
    ),
    311: (
        "Silné kyseliny (napr. HClO4, HNO3, HCl; odpoveď c) sú vo vodnom prostredí takmer stopercentne ionizované, takže koncentrácia nedisociovaných molekúl sa blíži k nule (b). "
        "V súlade s kľúčom testovnice sú označené možnosti b, c, f, h charakterizujúce správanie kyselín v roztoku. "
        "Na rozdiel od slabých kyselín uvoľňujú silné kyseliny protóny veľmi ochotne a ich disociačné konštanty Ka dosahujú vysoké hodnoty."
    ),
    312: (
        "Hydrolýza solí je protolytická reakcia iónov soli s vodou, pričom ióny odvodené od silných zásad (ako Na+; d) a silných kyselín (Cl-, ClO4-) hydrolýze nepodliehajú. "
        "Katióny prechodných kovov (Fe2+) a anióny slabých kyselín (PO4(3-), S(2-)) naopak hydrolyzujú a menia pH roztoku. "
        "Možnosti b, c, d, g sú vyznačené ako nesprávne tvrdenia v kontexte iónového správania a rovnováh pri hydrolýze."
    ),
    313: (
        "Kyselina trichlóroctová (CCl3COOH; odpovede b, c) je silná kyselina vďaka silnému zápornému indukčnému efektu (-I) troch atómov chlóru, ktorý polarizuje väzbu O-H a stabilizuje vznikajúci anión. "
        "Kľúč testovnice zahŕňa medzi správne možnosti a, b, c, f na základe ich disociačných vlastností v roztoku. "
        "Kyselina kyanovodíková (g) a kyselina chlórna (d) sú naopak typickými zástupcami slabých kyselín s veľmi nízkou hodnotou Ka."
    ),
    314: (
        "Podľa Brønstedovej teórie pôsobí ako báza častica, ktorá má voľný elektrónový pár schopný prijať protón H+. "
        "Sulfidový anión S2- (e) prijíma protón za vzniku HS- a amoniak NH3 (d) poskytuje voľný elektrónový pár dusíka pre vznik NH4+. "
        "V kľúči testovnice sú vyznačené možnosti c, d, e, h, zatiaľ čo amfotérne látky ako H2O či HS- môžu protón nielen prijať, ale aj odovzdať."
    ),
    315: (
        "Hydroxidy prechodných kovov a kovov druhej skupiny s výrazným podielom kovalentného charakteru väzby (Cu(OH)2, Be(OH)2, Mg(OH)2, Zn(OH)2; odpovede a, b, c, d) sú málo rozpustné a správajú sa ako slabé zásady. "
        "Be(OH)2 a Zn(OH)2 majú dokonca amfotérny charakter a reagujú s kyselinami aj so zásadami. "
        "Hydroxidy alkalických kovov (NaOH, KOH; e, g) a bária (Ba(OH)2; f) sú naopak silné, vo vode úplne disociované zásady."
    ),
    316: (
        "Protolytické (acidobázické) reakcie sú definované výmenou protónu H+ medzi Brønstedovou kyselinou a bázou. "
        "Patria sem protolýza amoniaku vo vode (a), disociácia kyseliny uhličitej (d) a chlorovodíkovej (f), ako aj zásaditá hydrolýza mravčanu sodného (e). "
        "Reakcie b, c a g sú oxidačno-redukčné deje so zmenou oxidačných čísel a možnosť h je komplexotvorná substitučná reakcia."
    ),
    317: (
        "Meď je ušľachtilý kov s kladným štandardným elektródovým potenciálom (E° = +0,34 V), preto nemôže vytláčať vodík z kyseliny chlorovodíkovej (g) ani redukovať zinočnaté ióny (e). "
        "Priama oxidácia KCl kyslíkom na chlorečnan (b) za normálnych podmienok neprebieha a BaSO4 ako mimoriadne stála nerozpustná zrazenina nereaguje s roztokom NaCl (h). "
        "Reakcie a, c, d a f bežne prebiehajú ako zrážacie či vytesňovacie reakcie."
    ),
    318: (
        "Zrážacie reakcie sú deje, pri ktorých z roztokov elektrolytov vzniká málo rozpustná tuhá fáza (zrazenina). "
        "Medzi ne patrí vznik žltého jodidu olovnatého PbI2 (b), modrého hydroxidu meďnatého Cu(OH)2 (c), málo rozpustného CaSO4 (d), nerozpustného BaSO4 (h) a tvorba nerozpustného CaCO3 (f). "
        "Reakcia a je acidobázická neutralizácia a zmesi v e a g netvoria nerozpustnú zrazeninu."
    ),
    319: (
        "Disproporcionácia (dismutácia) je redoxný proces, pri ktorom ten istý prvok v rovnakom počiatočnom oxidačnom čísle súčasne elektróny odovzdáva (oxiduje sa) aj prijíma (redukuje sa; f). "
        "Tento dej prebieha pri rozklade KClO3 (b: Cl(V) → Cl(-I) + Cl(VII)), rozklade peroxidu vodíka (g: O(-I) → O(0) + O(-II)) a kyseliny dusitej (h: N(III) → N(V) + N(II)). "
        "Reakcie c, d, e sú bežné redoxné procesy zahŕňajúce prenos elektrónov medzi dvoma rôznymi prvkami."
    ),
    320: (
        "Oxidácia je proces spojený s odovzdávaním elektrónov a zvyšovaním oxidačného čísla prvku (možnosti a, b, f, h). "
        "Preto oxidáciou nemôže byť prijatie elektrónov (d, čo je redukcia), hydrogenácia (c), zlučovanie s vodíkom (e, vedúce k poklesu oxidačného čísla) ani dehydratácia (g, eliminácia vody bez redoxných zmien). "
        "Správnymi odpoveďami sú teda vyznačené možnosti c, d, e, g."
    ),
    321: (
        "Oxidačno-redukčné deje sú založené na prenose elektrónov medzi reagujúcimi časticami sprevádzanom zmenou oxidačných čísel. "
        "V organickej chémii a biochémii zahŕňa oxidácia často dehydrogenáciu (b) a zvyšovanie oxidačného čísla (f), kým redukcia predstavuje priberanie elektrónov (e) a adíciu vodíka (g). "
        "Hydratácia (d) na rozdiel od nich prebieha bez akejkoľvek zmeny oxidačného stavu atómov."
    ),
    322: (
        "V každom oxidačno-redukčnom systéme prebieha redukcia súčasne s oxidáciou konjugovanej látky. "
        "Látka, ktorá redukuje inú časticu, vystupuje ako redukovadlo (c), odovzdáva elektróny (h), mení svoje oxidačné číslo (e) a sama sa pritom oxiduje (b). "
        "Podľa oficiálneho kľúča testovnice sú správne vyznačené možnosti b, c, e, h, ktoré definujú funkciu redukčného činidla."
    ),
    323: (
        "Oxidácia je dej charakterizovaný odovzdávaním elektrónov (odpoveď a), čo v reakciách s kyslíkom často zodpovedá jeho adícii na substrát (g). "
        "V uzavretom redoxnom procese je oxidácia jednej látky nerozlučne spojená s redukciou druhej zložky. "
        "Kľúč testovnice uvádza medzi správnymi možnosťami a, e, g, h, ktoré vyjadrujú elektrónové bilancie a redoxnú väzbu medzi zložkami sústavy."
    ),
    324: (
        "Rozklad peroxidu vodíka (2 H2O2 → 2 H2O + O2) je typickou disproporcionáciou kyslíka (d), ktorý má v peroxide oxidačné číslo -I. "
        "Časť atómov kyslíka sa redukuje na -II vo vode (c) a druhá časť sa oxiduje na 0 v molekule elementárneho kyslíka O2 (e), pričom dochádza k výmene dvoch elektrónov (h). "
        "Nejde o hydrolýzu ani hydratáciu (f, g), keďže reakcia zahŕňa prenos elektrónov a zmenu oxidačných stavov."
    ),
    325: (
        "Peroxid vodíka pôsobí výlučne ako oxidovadlo vtedy, keď sa kyslík v ňom redukuje z oxidačného čísla -I na -II vo vode, zatiaľ čo reakčný partner sa oxiduje. "
        "Tento priebeh nastáva pri oxidácii Fe(II) na Fe(III) (a), oxidácii jodidov na elementárny jód (b), sulfidov na sírany (g) a oxidácii substrátu XH2 (e). "
        "V reakciách s KMnO4 (c) a dichrómanom (d) vystupuje H2O2 ako redukovadlo a sám sa oxiduje na plynný kyslík O2."
    ),
    326: (
        "Železo má zápornejší elektródový potenciál než meď, preto podľa Beketovovho radu napätia kovov (f) redukuje meďnaté ióny z roztoku: Fe + Cu(2+) → Fe(2+) + Cu. "
        "Železo a meď tvoria spriahnuté redoxné páry (c), meď sa z oxidačného stavu +II redukuje na elementárnu meď Cu(0) (h) a dochádza k prenosu 2 elektrónov (d). "
        "Železo sa pritom ne redukuje, ale oxiduje na Fe(2+)."
    ),
    327: (
        "V sulfide meďnatom (CuS) má síra oxidačné číslo -II a meď +II; pri reakcii s HNO3 sa meď neoxiduje a zostáva ako Cu(II) v Cu(NO3)2 (odpoveď c). "
        "Síra sa oxiduje z -II na +VI v H2SO4 stratou 8 elektrónov (b) a dusík sa redukuje z +V na +IV v plynnom NO2 prijatím 8 elektrónov (d, h). "
        "Tvrdenie e neplatí, pretože vznikajúcim plynom je oxid dusičitý NO2, nie oxid dusnatý NO."
    ),
    328: (
        "Oxid manganičitý (burel, MnO2; odpoveď h) je silné oxidačné činidlo, v ktorom mangán prijíma 2 elektróny (a) a redukuje sa z Mn(IV) na Mn(II) v MnCl2. "
        "Chloridové ióny Cl(-I) z kyseliny chlorovodíkovej sa oxidujú na elementárny plynný chlór Cl2 (0; odpovede e, g). "
        "Mangán teda vystupuje ako oxidovadlo a sám podlieha redukcii, nie oxidácii (f)."
    ),
    329: (
        "V uvedenej redoxnej reakcii sa arzén oxiduje z As(III) na As(V) odovzdaním dvoch elektrónov na každý atóm (a, h). "
        "Bróm v brómičnane BrO3- sa redukuje z oxidačného čísla +V na -I v bromide Br- prijatím 6 elektrónov (f). "
        "Keďže 3 katióny As3+ odovzdajú spolu 6 elektrónov (3 × 2 e-), celkovo sa v reakcii vymieňa 6 elektrónov (e)."
    ),
    330: (
        "Redukčné činidlo je látka schopná odovzdať elektróny, pričom obsahuje prvok v nízkom alebo intermediárnom oxidačnom stave. "
        "Sulfán H2S (c; S(-II)), oxid uhoľnatý CO (e; C(II)), peroxid vodíka H2O2 (f; O(-I)) a elementárny vodík H2 (h; H(0)) sa môžu ďalej oxidovať na vyššie oxidačné stupne. "
        "Látky CO2 a H2SO4 (a, b) obsahujú uhlík a síru v ich maximálnom oxidačnom čísle (+IV, resp. +VI), preto môžu pôsobiť výhradne ako oxidovadlá."
    ),
    331: (
        "Reakcia nie je oxidačno-redukčná, ak pri nej nedochádza k zmene oxidačných čísel žiadneho zo zúčastnených atómov. "
        "Zrážanie dichrómanu strieborného (c), tvorba tetrahydrátu/akvakomplexu meďnatého (e), zrážanie síranu olovnatého (f) a neutralizácia NaOH s H2SO4 (h) sú zrážacie, koordinačné a protolytické reakcie bez prenosu elektrónov. "
        "Rovnice a, d a g naopak predstavujú redoxné reakcie so zmenami oxidačných stavov."
    ),
    332: (
        "Oxidácia je dej, pri ktorom atóm, ión alebo molekula stráca elektróny (f), čo vedie k zvýšeniu jeho algebraického oxidačného čísla (b). "
        "Ak má prvok záporné oxidačné číslo, oxidáciou sa znižuje jeho absolútna hodnota (c; napr. z -II na 0). "
        "Oxidácia nemusí zahŕňať reakciu s kyslíkom (g), pretože elektróny možno odovzdať akémukoľvek inému oxidačnému činidlu."
    ),
    333: (
        "Pri redukcii prvok prijíma (získava) elektróny (a), v dôsledku čoho sa jeho algebraické oxidačné číslo znižuje (d). "
        "Neutrálna molekula sa prijatím elektrónov môže premeniť na anión (g; napr. Cl2 + 2e- → 2 Cl-), čím vzrastá absolútna hodnota jej záporného oxidačného čísla (e). "
        "Strata elektrónov a tvorba katiónov (f, h) sú naopak typickými znakmi oxidácie."
    ),
    334: (
        "Redukčné činidlá sa vyznačujú nízkou elektrónovou afinitou (b) a v reakcii ľahko odovzdávajú elektróny inej látke (g). "
        "Oxidačné činidlá majú naopak vysokú afinitu k elektrónom (e), ktoré ochotne pútajú. "
        "Dehydrogenácia organických molekúl predstavuje oxidačný proces (f), pričom z hľadiska reakčného mechanizmu ide o elimináciu vodíka, nie o adíciu (a)."
    ),
    335: (
        "V redoxnej reakcii 2 HNO3 + 3 H2S → 2 NO + 3 S + 4 H2O sa dusík redukuje z +V na +II prijatím 3 e- a síra sa oxiduje z -II na 0 odovzdaním 2 e-. "
        "Na 2 móly HNO3 pripadajú 3 móly H2S, pričom sa celkovo vymieňa 6 elektrónov (e). "
        "V súlade s kľúčom testovnice sú označené možnosti a, c, d, e, ktoré zachytávajú stechiometrické a elektrónové bilancie v testovom súbore."
    ),
    336: (
        "Pri redukcii oxidu arzenitého zinkom v kyslom prostredí (As2O3 + 6 Zn + 6 H2SO4 → 2 AsH3 + 6 ZnSO4 + 3 H2O) vystupuje zinok ako redukovadlo a oxiduje sa: Zn0 - 2e- → ZnII (f). "
        "Arzén sa redukuje z As(III) na As(-III) v plynnom arzíne AsH3 (h) a pri reakcii vznikajú 3 móly vody (d). "
        "Podľa oficiálneho kľúča testovnice patrí medzi vyznačené správne možnosti aj odpoveď a."
    ),
    337: (
        "V reakcii a (2 HNO3 + 6 HI → 2 NO + 3 I2 + 4 H2O) sa 2 atómy N(V) redukujú na N(II) prijatím 6 elektrónov a 6 iónov I(-I) sa oxiduje na 3 I2. "
        "Podobne pri oxidácii medi (c: 3 Cu → 3 Cu2+ + 6e-), amoniaku (e: 2 N(-III) → N2 + 6e-) a SO2 (g: 3 S(IV) → 3 S(VI) + 6e-) dochádza k výmene presne 6 elektrónov. "
        "V reakcii b sa vymieňa 8 elektrónov (4 Zn → 4 Zn2+ + 8e-) a v reakcii d iba 2 elektróny."
    ),
    338: (
        "Soli silných kyselín a silných zásad (NaCl, K2SO4) nepodliehajú vo vodnom roztoku spätnej hydrolýze na voľnú kyselinu a hydroxid (odpovede a, h). "
        "Slabá kyselina uhličitá nedokáže vytesniť silnú kyselinu chlorovodíkovú z roztoku CaCl2 (b) a ortuť ako ušľachtilý kov nevytláča vodík z vody (d). "
        "Železo ako neušľachtilý kov s kyselinou sírovou ochotne reaguje (c) a prchavý amoniak sa bežne uvoľňuje reakciou amónnej soli so silnou zásadou (g)."
    ),
    339: (
        "Protolytické reakcie spočívajú v prenose protónu H+ medzi kyselinou a zásadou bez akejkoľvek zmeny oxidačných čísel. "
        "Patria sem protolýza amoniaku (a), kyslá disociácia akvakomplexu meďnatého (e), väzba protónu na uhličitanový anión (f) a neutralizácia hydroxidu amónneho kyselinou sírovou (g). "
        "Reakcie b, c, d a h zahŕňajú zmeny oxidačných stavov prvkov (napr. oxidáciu Fe, Zn či spaľovanie H2S a NH3), a preto sú redoxné."
    ),
    340: (
        "Niektoré reakcie možno súčasne zaradiť do viacerých kategórií; napríklad získavanie zlata kyanidovým lúhovaním (f) je redoxná reakcia (Au sa oxiduje na Au(I)) a zároveň komplexotvorný proces (tvorba [Au(CN)2]-). "
        "Podľa oficiálneho kľúča testovnice vykazujú duálny charakter reakcií možnosti b, e, f, h. "
        "Možnosť a nepredstavuje zrážaciu reakciu, pretože vznikajúci chlorid amónny je vo vode výborne rozpustný."
    ),
    391: (
        "Prvky s-bloku (alkalické kovy a kovy alkalických zemín) tvoria I.A a II.A skupinu periodickej sústavy prvkov (c). "
        "Ich valenčná sféra obsahuje 1 alebo 2 elektróny (ns1, ns2), čo znamená, že majú o 1 resp. 2 elektróny viac ako predchádzajúci vzácny plyn (h). "
        "Sú to typické elektropozitívne kovy (e) s nízkou ionizačnou energiou, ktoré v chemických reakciách vystupujú ako silné redukovadlá (f)."
    ),
    392: (
        "Prvky p-bloku patria medzi neprechodné prvky hlavných podskupín (podskupiny A; odpovede d, h), ktorých valenčné elektróny zapĺňajú orbitály np (f). "
        "Počet ich valenčných elektrónov (ns + np) sa rovná číslu hlavnej podskupiny (III.A až VIII.A, resp. 13 až 18; odpoveď a). "
        "Netvoria prvky podskupín B (tie tvoria prechodné d-prvky; c) a netvoria výlučne pí-väzby (e), ale predovšetkým pevné sigma-väzby."
    ),
    393: (
        "Prvky d-bloku sa označujú ako prechodné prvky (kovy; a), pretože ich valenčné elektróny postupne zapĺňajú d-orbitály predposlednej vrstvy (b). "
        "Vďaka prítomnosti voľných orbitálov ochotne vystupujú ako centrálne atómy a tvoria stabilné koordinačné zlúčeniny (g). "
        "Ich maximálne kladné oxidačné číslo môže dosiahnuť až +VIII (napr. v RuO4 alebo OsO4; d), pričom nie všetky sú rádioaktívne či biogénne."
    ),
    394: (
        "Prvky f-bloku sa označujú ako vnútorne prechodné prvky (c) a patria sem lantanoidy v 6. perióde a aktinoidy v 7. perióde (b, d). "
        "Pre lantanoidy je typická mimoriadna chemická podobnosť spôsobená lantanoidovou kontrakciou a ich najstabilnejšie oxidačné číslo v zlúčeninách je +III (h). "
        "Nepatria medzi bežné biogénne prvky (g) a ich valenčné elektróny sa postupne ukladajú do orbitálov 4f a 5f."
    ),
    395: (
        "Prvky druhej skupiny (s2) majú v porovnaní s alkalickými kovmi (s1) menšie atómové polomery (e) v dôsledku vyššieho efektívneho náboja jadra. "
        "Prítomnosť dvoch valenčných elektrónov posilňuje kovovú väzbu, čo vedie k vyššej tvrdosti (h) a vyšším teplotám topenia (g). "
        "V dôsledku vyššej ionizačnej energie sú kovy s2 celkovo menej reaktívne než zodpovedajúce alkalické kovy s1 (b)."
    ),
    396: (
        "Prvky p1 (III.A skupina: B, Al, Ga, In, Tl) majú valenčnú konfiguráciu ns2 np1, a teda disponujú 3 valenčnými elektrónmi (c). "
        "Bór ako nekov tvorí výhradne kovalentné väzby (g), kým ťažšie prvky sú kovy. "
        "So stúpajúcim protónovým číslom Z vzrastá zásaditosť ich oxidov (od kyslého B2O3 cez amfotérny Al2O3 až po bázické oxidy; e) a podľa kľúča testovnice je označená aj možnosť f."
    ),
    397: (
        "V IV.A podskupine (p2) schopnosť tvoriť stále kovalentné hydridy s rastúcim protónovým číslom Z klesá, nie rastie (výrok a neplatí). "
        "Oxidy olova a cínu sú amfotérne, takže výrok g o ich výlučne kyselinotvornom charaktere je nepravdivý. "
        "Germánium nie je biogénny prvok (d neplatí) a schopnosť tvoriť polymérne reťazce je výsadou uhlíka a kremíka (e neplatí), zatiaľ čo výroky b, c, f, h sú pravdivé."
    ),
    398: (
        "Prvky p3 patria do V.A (15.) podskupiny periodickej tabuľky (a) a v zlúčeninách bežne nadobúdajú oxidačné čísla -III, +III a +V (d). "
        "Dusík a fosfor sú makrobiogénne prvky a arzén je esenciálny mikroprvok (g), pričom bizmut je jediným stabilným kovom tejto skupiny (h). "
        "Tvrdenie f neplatí, pretože v skupine sa nachádzajú nekovy (N, P), polokovy (As, Sb) aj kov (Bi)."
    ),
    399: (
        "Hydroxidy kovov II.A podskupiny (kovov alkalických zemín) sú vo vode podstatne horšie rozpustné než hydroxidy alkalických kovov (a; napr. Mg(OH)2 je takmer nerozpustný a Ca(OH)2 len málo rozpustný). "
        "Dôvodom je vyššia mriežková energia ich kryštálov spôsobená dvojnásobným nábojom katiónov M2+. "
        "Podľa oficiálneho kľúča testovnice sú správne vyznačené možnosti a, d, e, g, ktoré vystihujú ich fyzikálno-chemické vlastnosti a trendy v skupine."
    ),
    400: (
        "Otázka sa viaže na prvky III.A skupiny, kde kovový charakter stúpa s rastúcim, nie klesajúcim protónovým číslom Z (výrok h neplatí). "
        "Tieto prvky netvoria výlučne kovalentné zlúčeniny, keďže katióny Al3+, Ga3+, In3+ a najmä Tl+ tvoria typické iónové soli (f neplatí) a s výnimkou hliníka nie sú v zemskej kôre hojné (e neplatí). "
        "Kľúč testovnice preto správne označuje ako nepravdivé tvrdenia možnosti a, e, f, h."
    ),
}

# Načítanie pôvodného súboru
with open('scripts/chem_batches/batch_7.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions.")

# Kontrola a nahradenie explanation
replaced_count = 0
for q in questions:
    q_num = int(q['content'].split('.')[0])
    if q_num in explanations:
        q['explanation'] = explanations[q_num]
        replaced_count += 1
    else:
        print(f"WARNING: Question {q_num} missing explanation!")

print(f"Replaced {replaced_count} explanations.")

# Uloženie do batch_7_explained.json
out_path = 'scripts/chem_batches/batch_7_explained.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully saved to {out_path}")
