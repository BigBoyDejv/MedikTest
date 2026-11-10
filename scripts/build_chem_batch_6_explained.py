import json

# Dictionary of explanations for questions 251 to 300
explanations = {
    251: (
        "Podľa Le Chatelierovho princípu akcie a reakcie sa rovnováha reakcie posunie v smere produktov (zvýšenie koncentrácie NO) "
        "takými zásahmi, ktoré kompenzujú vonkajší vplyv. Keďže ide o silne exotermickú reakciu (ΔH < 0), chladenie systému (d) posúva rovnováhu "
        "v smere tvorby produktov, zatiaľ čo ohrievanie (c) by ju posunulo k reaktantom. Na strane reaktantov je 9 mólov plynu a na strane produktov "
        "10 mólov plynu, preto zníženie tlaku (e) alebo zväčšenie objemu nádoby (g) posunie rovnováhu v smere väčšieho počtu plynných mólov. "
        "Odstraňovaním vodnej pary zo systému (a) sa rovnováha taktiež posúva doprava v prospech produktov, kým katalyzátor (h) iba urýchľuje ustavenie rovnováhy."
    ),
    252: (
        "I. termochemický zákon (Lavoisierov-Laplaceov) hovorí, že reakčné teplo priamej a spätnej reakcie je až na znamienko rovnaké, "
        "čo dokladujú opačné rovnice oxidácie CO a redukcie CO2 (e). Zmena Gibbsovej energie ΔG v sebe spája entalpický člen (ΔH) vyjadrujúci zmenu väzbových energií "
        "a entropický člen (TΔS) odrážajúci mieru neusporiadanosti systému podľa vzťahu ΔG = ΔH - TΔS (h). Zlučovacie teplo je definované pre vznik 1 mólu zlúčeniny "
        "priamo z prvkov v štandardnom stave, nie spálením 1 kg látky (f), a Gibbsova energia charakterizuje izotermicko-izobarické deje (g). "
        "Správne možnosti (b, d, e, h) vychádzajú z termochemických zákonov a termodynamických definícií stavových veličín."
    ),
    253: (
        "Chemická reakcia môže prebiehať samovoľne za normálnych podmienok vtedy, ak je zmena Gibbsovej energie záporná (ΔG < 0, exergonický dej). "
        "Reakcie alkalických kovov s vodou (b), vytesňovanie vodíka z kyselín zinkom a horčíkom (g, h), neutralizácia NaOH s HCl (d) a reakcia CaCO3 s HCl (c) "
        "sú silne exotermické reakcie často sprevádzané nárastom entropie (únik plynov), takže ΔG < 0. Naopak endotermické redukčné a rozkladné deje (a, e, f) "
        "majú za bežných teplôt ΔG > 0 a vyžadujú trvalé dodávanie tepla pri vysokých teplotách."
    ),
    254: (
        "Kritériom samovoľnosti izotermicko-izobarického deja je pokles Gibbsovej energie (ΔG < 0), preto tvrdenie o vzraste G je nesprávne (a). "
        "Podľa Gibbsovej rovnice ΔG = ΔH - TΔS je pri exotermických syntézach (ΔH < 0, ΔS < 0) samovoľný priebeh závislý od teploty a nastáva len pri dostatočne "
        "nízkych teplotách, kedy entalpický člen preváži nad záporným entropickým (e). Endotermické syntézy (ΔH > 0, ΔS < 0) majú vždy ΔG > 0, takže nikdy "
        "neprebiehajú samovoľne (f), zatiaľ čo endotermické rozklady (ΔH > 0, ΔS > 0) môžu byť pri vysokých teplotách samovoľné, keď člen TΔS prevýši kladné ΔH (g)."
    ),
    255: (
        "Rovnovážna konštanta spätnej reakcie je definovaná ako prevrátená hodnota konštanty priamej reakcie K' = 1/K = K^-1 (c). "
        "Veľmi nízka hodnota rovnovážnej konštanty (K < 10^-4) znamená, že rovnováha je takmer úplne posunutá k reaktantom a reakcia v smere produktov prakticky neprebieha (e). "
        "Pri nulovej zmene štandardnej Gibbsovej energie (ΔG° = 0) je rovnovážna konštanta K = 1 a systém je v rovnováhe (h). "
        "Výsledná rýchlosť vratného deja je daná súčtom (bilanciou) rýchlostí v oboch smeroch (b), pričom rovnovážna konštanta celkovej reakcie je daná súčinom, nie súčtom čiastkových konštánt (a)."
    ),
    256: (
        "Chemická reakcia je dej, pri ktorom dochádza k premene východiskových látok (reaktantov) na látky s iným chemickým zložením a štruktúrou väzieb (produkty) (e, h). "
        "Ak sa pri deji zloženie molekúl nemení a dochádza len ku zmene skupenstva či tvaru, ide o fyzikálny dej (c). "
        "Miernym zahriatím látky často dochádza len k zvýšeniu kinetickej energie častíc alebo k fázovému prechodu bez chemického rozkladu molekúl (b). "
        "Horenie je naopak typický oxidačný chemický dej (d) a topenie je zmena skupenstva, teda fyzikálny proces (a)."
    ),
    257: (
        "Tepelný efekt rozpúšťania je výslednicou endotermického rozrušovania kryštálovej mriežky (spotreba tepla) a exotermickej hydratácie/solvatácie iónov (uvoľnenie tepla), "
        "preto môže mať celkový proces exotermický aj endotermický charakter (f). Molové rozpúšťacie teplo vyjadruje množstvo tepla vymeneného so sústavou pri rozpustení 1 mólu látky (b). "
        "Pri riedení koncentrovaného NaOH vodou alebo koncentrovanej kyseliny sírovej prevažuje silná hydratácia iónov, pri ktorej sa uvoľňuje veľké množstvo tepla a roztok sa prudko zahrieva (d, g). "
        "Rozpúšťanie KCl a NH4NO3 je naopak endotermické a roztok sa ochladzuje (a, c)."
    ),
    258: (
        "Rozpúšťanie kryštalickej látky pozostáva z rozpadu kryštálovej štruktúry na jednotlivé častice (vyžaduje dodanie energie na prekonanie mriežkových síl) "
        "a z ich následnej hydratácie molekulami vody (energia sa uvoľňuje) (b, c). Celkový tepelný efekt je súčtom mriežkovej a hydratačnej entalpie, "
        "takže proces môže byť exotermický alebo endotermický (d). Proces je exotermický práve vtedy, ak je entalpia potrebná na rozrušenie kryštálovej mriežky "
        "menšia ako entalpia uvoľnená pri hydratácii vzniknutých častíc (e)."
    ),
    259: (
        "V nasýtenom roztoku málo rozpustnej zlúčeniny sa ustavuje dynamická heterogénna rovnováha medzi nerozpustenou pevnou fázou a voľnými iónmi v roztoku, "
        "popísaná súčinom rozpustnosti Ks (d). Zrazenina málo rozpustnej látky vzniká vtedy, keď iónový súčin koncentrácií príslušných iónov v roztoku prekročí "
        "tabuľkovú hodnotu súčinu rozpustnosti Ks pri danej teplote (f). Rozpustnosť a hodnota Ks závisia od reakčnej teploty, a s klesajúcou hodnotou Ks "
        "pravdepodobnosť vzniku zrazeniny rastie, nie klesá (b, c sú nesprávne)."
    ),
    260: (
        "Zvýšenie teploty podľa Arrheniovej rovnice exponenciálne zvyšuje rýchlostnú konštantu a tým aj rýchlosť chemických reakcií (d). "
        "Podľa Le Chatelierovho princípu zvýšenie teploty favorizuje endotermické deje – podporuje endotermický rozklad uhličitanu vápenatého (b) "
        "a endotermické rozpúšťanie pevných látok s kladnou entalpiou rozpúšťania (c). Naopak pri exotermickej syntéze amoniaku vyššia teplota posúva "
        "rovnováhu v smere reaktantov a znižuje výťažok reakcie (e)."
    ),
    261: (
        "Kyselina chlorovodíková je silná jednosýtna kyselina, ktorá vo vodnom roztoku úplne disociuje, takže pôvodná hodnota pH = -log(0,1) = 1. "
        "Pri 1000-násobnom zriedení (faktor 10^3) klesne koncentrácia H3O+ na 0,0001 mol/l (10^-4 mol/l), takže výsledné pH = -log(10^-4) = 4, "
        "čo znamená zväčšenie pH o 3 jednotky oproti pôvodnému roztoku (d, e, h). Pri 25 °C platí pH + pOH = 14, takže pOH = 10, z čoho vyplýva, "
        "že výsledné pH (4) je menšie ako pOH (10) a roztok ostáva kyslý (g)."
    ),
    262: (
        "Slabé elektrolyty sú látky, ktoré vo vodnom roztoku disociujú na ióny len čiastočne a ich disociačný stupeň je veľmi nízky (α << 1). "
        "Medzi slabé elektrolyty patria slabé karboxylové kyseliny ako kyselina octová a mravčia (b), slabé anorganické kyseliny ako HNO2, H2S a HCN (d, e), "
        "slabé bázy vrátane amoniaku vo vode (NH4OH) (e) a amfotérne hydrogenanióny HPO4(2-) či samotná voda (f). Naopak silné kyseliny (H2SO4, HCl) "
        "a rozpustné soli (Na2SO4, CuSO4, NH4Cl, Na2CO3) patria medzi silné elektrolyty, ktoré vo vode disociujú prakticky úplne (a, c, g, h)."
    ),
    263: (
        "Medzi silou kyseliny a jej konjugovanej zásady platí nepriama úmera vyjadrená vzťahom Ka * Kb = Kv, čo znamená, že čím je kyselina silnejšia, "
        "tým je jej konjugovaná zásada slabšia (tvrdenia a, g sú nesprávne). Sila zásady nezávisí od počtu hydroxidových skupín v molekule, "
        "ale od afinity k protónu vyjadrenej disociačnou konštantou Kb (c je nesprávne). Neutralizácia je navyše blesková iónová reakcia "
        "s minimálnou aktivačnou energiou, kde voda vzniká ako reakčný produkt, nie ako reaktant (e je nesprávne)."
    ),
    264: (
        "Voda podlieha autoprotolýze (2 H2O <=> H3O+ + OH-), čo je vlastná samovoľná ionizácia molekúl vody (a). "
        "Disociačná konštanta autoprotolýzy vody má extrémne nízku hodnotu (pKd ≈ 15,7), takže disociuje len nepatrný zlomok molekúl "
        "a koncentrácia vody sa považuje za konštantnú a zahŕňa sa do iónového súčinu Kv = [H3O+][OH-] (c, e). "
        "Autoprotolýza je endotermický dej, preto s rastúcou teplotou stupeň disociácie stúpa a hodnota iónového súčinu vody Kv rastie (f)."
    ),
    265: (
        "Pri štandardnej teplote 25 °C platí vo všetkých vodných roztokoch iónový súčin vody Kv = [H3O+] * [OH-] = 10^-14 mol^2.dm^-6 a súčet pH + pOH = 14. "
        "Ak je pH = 6, potom [H3O+] = 10^-6 mol.dm^-3, z čoho priamo vyplýva pOH = 8 a [OH-] = 10^-8 mol.dm^-3 (c, d, e). "
        "Koncentrácia [OH-] = 0,01 μmol.dm^-3 predstavuje 0,01 * 10^-6 = 10^-8 mol.dm^-3, čo taktiež zodpovedá hodnote pH = 6 (g)."
    ),
    266: (
        "Osmotický tlak patrí medzi koligatívne vlastnosti roztokov a podľa van 't Hoffovho zákona (π = i * c * R * T) závisí od látkovej koncentrácie "
        "a celkového počtu disociovaných častíc v jednotke objemu (a, c, f). Fyziologický roztok má osmolaritu približne 0,30 osmol/l (0,15 mol/l NaCl disociuje na 2 ióny). "
        "Neelektrolyt fruktóza pri c = 0,3 mol/l poskytuje 0,30 osmol/l častíc a FeCl2 pri c = 0,1 mol/l disociuje na 3 ióny (0,1 * 3 = 0,30 osmol/l), "
        "preto sú oba roztoky izotonické voči fyziologickému roztoku (g)."
    ),
    267: (
        "Fyziologický roztok (0,9 % NaCl) je izotonický s krvnou plazmou, pretože má zhodný osmotický tlak (b). "
        "V hypotonickom roztoku voda v dôsledku osmózy prúdi do červených krviniek (endosmóza), bunky zväčšujú svoj objem a praskajú, čo sa nazýva osmotická hemolýza (d). "
        "Závislosť osmotického tlaku od termodynamickej teploty popisuje van 't Hoffov vzťah π = i * c * R * T (e). "
        "Tvrdenia b, d, e, f reflektujú testovnicové formulácie koligatívnych vlastností roztokov a správania buniek."
    ),
    268: (
        "Fyziologický roztok je 0,9 % (hmotnostných) vodný roztok chloridu sodného, čo zodpovedá rozpusteniu približne 9 g NaCl v 1 litri roztoku (d, h). "
        "Vzhľadom na molárnu hmotnosť NaCl (58,44 g/mol) zodpovedá táto koncentrácia približne 0,15 mol/l NaCl (a). "
        "Keďže NaCl úplne disociuje na 2 ióny (Na+ a Cl-), jeho celková osmolarita je 2 * 0,15 = 0,30 osmol/l, čo vytvára rovnaký osmotický tlak "
        "ako 0,3 mol/l roztok nedisociujúcej sacharózy (e)."
    ),
    269: (
        "Červené krvinky zostávajú tvarovo i funkčne nezmenené výlučne v izotonických roztokoch, ktorých osmolarita zodpovedá krvnej plazme (približne 0,30 osmol/l) (d). "
        "Jodid draselný KI pri c = 0,15 mol/l disociuje na 2 ióny (osmolarita 2 * 0,15 = 0,30 osmol/l) (a), glukóza ako neelektrolyt pri c = 0,3 mol/l poskytuje osmolaritu "
        "0,30 osmol/l (e) a dusičnan vápenatý Ca(NO3)2 pri c = 0,1 mol/l disociuje na 3 ióny (osmolarita 3 * 0,1 = 0,30 osmol/l) (f). "
        "V hypotonických roztokoch by došlo k hemolýze a v hypertonických k plazmorýze."
    ),
    270: (
        "Tlmivé roztoky (pufre) sú zmesi slabej kyseliny a jej konjugovanej zásady alebo slabej zásady a jej konjugovanej kyseliny (c, e). "
        "Ich základnou úlohou je udržiavať stabilnú hodnotu pH pri pridaní menšieho množstva kyseliny či zásady alebo pri zriedení systému (g). "
        "Umožňujú pripraviť a presne nastaviť požadovanú hodnotu pH podľa Hendersonovej-Hasselbalchovej rovnice (f). "
        "Zmesi silných kyselín a silných zásad pufrovací účinok nemajú."
    ),
    271: (
        "Iónový súčin vody Kv = [H3O+] * [OH-] je rovnovážnou konštantou autoprotolýzy vody, do ktorej je zahrnutá konštantná koncentrácia nedisociovanej vody (b). "
        "Pri 25 °C má štandardnú hodnotu Kv = 10^-14 mol^2.l^-2 (g). Keďže ide o rovnovážnu konštantu, jej hodnota je pri danej teplote rovnaká vo všetkých "
        "zriedených vodných roztokoch bez ohľadu na prítomnosť iných látok (d), avšak so zmenou teploty sa mení, pretože autoprotolýza je endotermický proces (c)."
    ),
    272: (
        "Podľa Brönstedovej protolytickej teórie je kyselina donorom protónu H+. Častice NH4+, H2PO4-, H3O+ a aromatický fenol obsahujú odštiepiteľné "
        "atómy vodíka a správajú sa ako kyseliny. Naopak anióny HCOO-, OH-, CN- a CO3(2-) vystupujú v acidobázických dejoch ako akceptory protónu "
        "(Brönstedove zásady) a nepatria medzi kyseliny, keďže nemajú disociovateľný kyslý protón (d, e, g, h)."
    ),
    273: (
        "Amfotérny (amfiprotický) charakter majú látky, ktoré môžu podľa podmienok vystupovať ako donor aj ako akceptor protónu, čo spĺňa voda, "
        "glycín a hydrogenanióny viacsýtnych kyselín ako HPO4(2-) a HCO3- (b, c, d, e). Naopak plne protonizované anorganické kyseliny H3PO4, "
        "H2CO3, HCN a H2SO4 môžu vo vodnom roztoku protón výlučne odovzdávať a správajú sa len ako kyseliny, nie ako amfolyty (a, f, g, h)."
    ),
    274: (
        "Konjugovaný pár kyseliny a zásady tvoria dve častice líšiace sa presne o jeden protón H+. Pár anilín/anilínium C6H5NH2 a C6H5NH3+ (a), "
        "hydrogensiričitan/kyselina siričitá HSO3- a H2SO3 (d), hydrogensiričitan/siričitan HSO3- a SO3(2-) (e) a protonizovaná/neutrálna forma "
        "glycínu (g) sa navzájom líšia o jeden protón H+. Látky v ostatných možnostiach sa líšia atómom kyslíka (HClO2/HClO), stupňom hydrogenácie "
        "(pyridín/piperidín) alebo ide o dve rôzne kyseliny (CH3COOH/HCOOH)."
    ),
    275: (
        "Chlorid amónny NH4Cl je soľ slabej zásady a silnej kyseliny, ktorej katión hydrolyzuje (NH4+ + H2O <=> NH3 + H3O+), čo spôsobuje kyslé pH < 7 (b). "
        "Fosforečnan sodný Na3PO4 je soľ silnej zásady a slabej kyseliny, ktorej anión silne hydrolyzuje na OH-, takže vytvára zásadité prostredie (e). "
        "Chlorid draselný KCl nehydrolyzuje a má neutrálne pH = 7 (f). Uhličitan amónny (NH4)2CO3 je soľ slabej kyseliny a slabej zásady s podobnými pK hodnotami, "
        "preto hydrolyzujú oba ióny a roztok je približne neutrálny (g)."
    ),
    276: (
        "Hydrolýza soli je definovaná ako protolytická reakcia iónov rozpustenej soli s vodou (možnosť a). "
        "Uvedené možnosti b, c, d, f, g nepredstavujú hydrolýzu soli, ale opisujú zmeny sfarbenia rôznych acidobázických indikátorov "
        "(pentametoxylová červená, tymolová modrá, fenolftaleín, alizarínová žltá R, dinitrofenol) pri špecifických koncentráciách H3O+ a OH- "
        "v kyslých a zásaditých roztokoch."
    ),
    277: (
        "Vodný roztok NH4Cl vykazuje kyslé pH v dôsledku hydrolýzy amónneho katiónu za vzniku H3O+ (a). "
        "Chlorid sodný NaCl je soľ silnej kyseliny a silnej zásady, jeho ióny s vodou nehydrolyzujú a roztok si zachováva neutrálne pH (c). "
        "Pri hydrolýze aniónu soli slabej kyseliny a silnej zásady sa protón viaže na anión a uvoľňujú sa ióny OH-, ktoré spôsobujú zásaditosť (f). "
        "Čistá voda pri 25 °C má v dôsledku rovnováhy autoprotolýzy neutrálnu hodnotu pH = 7 (h)."
    ),
    278: (
        "Podľa Brönstedovej teórie sa voda správa ako kyselina vtedy, keď odovzdáva protón H+ druhej častici (akceptoru), pričom sama prechádza na konjugovanú zásadu OH-. "
        "K tomu dochádza pri reakcii s amoniakom za vzniku NH4+ a OH- (d), so sulfidovým aniónom S(2-) za vzniku HS- a OH- (h), ako aj pri reakcii "
        "s hydrogénsíranovým alebo šťavelanovým aniónom (b, g). V reakciách s kyselinami HNO2, HCN a fenolom (a, e, f) naopak voda protón prijíma "
        "a vystupuje ako zásada za vzniku H3O+."
    ),
    279: (
        "Zvýšenie pH znamená posun roztoku do zásaditej oblasti v dôsledku vzniku nadbytku hydroxidových iónov OH-. "
        "Amoniak je slabá zásada, ktorá priamo reaguje s vodou za uvoľnenia OH- (g). Soli slabých jednosýtnych kyselín a silných zásad (chlórnan draselný KClO, "
        "kyanid draselný KCN a dusitan sodný NaNO2) podliehajú aniónovej hydrolýze (napr. ClO- + H2O <=> HClO + OH-), čím generujú OH- ióny a zvyšujú pH (a, b, e). "
        "Neutrálne soli (NaCl, K2SO4) pH nemenia a dusičnan amónny roztok okysľuje."
    ),
    280: (
        "K zníženiu pH (okysleniu roztoku) dochádza pri zvýšení koncentrácie oxóniových iónov H3O+. Fenol a kyanovodík sú slabé Brönstedove kyseliny schopné "
        "disociácie a odovzdania protónu vode (a, f). Síran amónny (NH4)2SO4 je soľ slabej zásady a silnej kyseliny, ktorej amónny katión NH4+ hydrolyzuje "
        "za vzniku H3O+ (d). Žalúdočná šťava obsahuje koncentrovanú kyselinu chlorovodíkovú (pH 1–2), preto významne okysľuje vodné prostredie (g)."
    ),
    281: (
        "Hydrolýza soli predstavuje reakciu iónov rozpustenej soli s vodou. Protolytické reakcie amoniaku a kyanovodíka vo vode (a, e) sú rovnovážnymi "
        "disociáciami slabej zásady a slabej kyseliny, nie hydrolýzou solí. Možnosti f a h navyše chybne označujú odštiepenie protónu za prejav zásady "
        "(HPO4(2-) a H2PO4- tu odovzdávajú protón za vzniku H3O+, čo je prejavom kyseliny), a preto taktiež nereprezentujú proces hydrolýzy soli."
    ),
    282: (
        "Tlmivý roztok (pufer) je schopný tlmiť a udržiavať konštantnú hodnotu pH pri pridaní menších množstiev kyselín alebo hydroxidov (a). "
        "Kľúčovú úlohu pri udržiavaní acidobázickej rovnováhy krvi zohrávajú fyziologické tlmivé sústavy: hydrogénuhličitanový pufer, fosfátový pufer "
        "a bielkovinové systémy vrátane hemoglobínu (f). Výpočet pH a zloženia pufrových sústav sa realizuje pomocou Hendersonovej-Hasselbalchovej rovnice (h). "
        "Uvedené možnosti (a, f, g, h) vystihujú podstatu tlmivých systémov podľa oficiálnej testovnice."
    ),
    283: (
        "Disociačná konštanta je rovnovážna konštanta protolytickej disociačnej reakcie kyseliny alebo zásady (b), pričom iónový súčin vody Kv je špecifickou "
        "konštantou autoprotolýzy vody (a). Sila zásady je priamo úmerná schopnosti prijať protón, preto čím je zásada slabšia, tým menšiu hodnotu "
        "disociačnej konštanty Kb dosahuje (d). Hodnota disociačnej konštanty je termodynamicky závislá od teploty (f), zatiaľ čo pre silnejšie kyseliny "
        "je hodnota Ka vyššia (nie nižšia)."
    ),
    284: (
        "Dihydrogenfosforečnanový anión H2PO4- je amfolyt, pretože môže protón odovzdať za vzniku HPO4(2-) aj prijať za vzniku H3PO4 (d). "
        "Voči kyseline fosforečnej H3PO4 vystupuje ako jej konjugovaná zásada, pretože vznikla odštiepením jedného protónu (h), zatiaľ čo voči "
        "hydrogenfosforečnanu HPO4(2-) je konjugovanou kyselinou (g). Spolu s aniónom HPO4(2-) tvorí konjugovaný pár intracelulárneho fosfátového pufru (e)."
    ),
    285: (
        "Hydrogenfosforečnany (HPO4^2-) hydrolyzujú prevažne zásadito (aniónová hydrolýza HPO4^2- + H2O <=> H2PO4- + OH-), kým roztoky "
        "dihydrogenfosforečnanov (H2PO4^-) reagujú slabo kyslo, preto hydrogenfosforečnany nereagujú kyslejšie než dihydrogenfosforečnany (c je nesprávne tvrdenie). "
        "Terciárne fosforečnany PO4(3-) nemajú kyslý vodík schopný disociácie, takže nemôžu vystupovať ako donory protónu a nemajú amfotérny charakter (e je nesprávne). "
        "K2HPO4 je štandardnou bázickou zložkou fosfátového pufru (d je nesprávne)."
    ),
    286: (
        "Elektrolyty sú látky schopné viesť elektrický prúd v roztoku alebo tavenine vďaka voľným iónom vzniknutým elektrolytickou disociáciou (c). "
        "Roztoky elektrolytov vznikajú rozpúšťaním iónových zlúčenín a polárnych látok v polárnych rozpúšťadlách, kde interakcia s dipólmi rozpúšťadla "
        "spôsobí rozpad mriežky a hydratáciu iónov (g). Silné elektrolyty, akými sú roztoky silných kyselín (HClO4) či solí (NaCl), "
        "sú v zriedených vodných roztokoch disociované prakticky na 100 % (h)."
    ),
    287: (
        "Pri rozpúšťaní kryštalických solí vo vode dochádza k prekonaniu mriežkových síl a uvoľneniu iónov (ionizácia) a k ich obklopeniu molekulami vody (hydratácia) (a, b). "
        "Octan sodný CH3COONa je soľ slabej kyseliny a silnej zásady, ktorej anión hydrolyzuje za vzniku OH-, takže roztok vykazuje zásadité pH > 7 a pOH < 7 (c). "
        "Síran sodný Na2SO4 je soľ silnej kyseliny a silnej zásady, nehydrolyzuje a jeho roztok zostáva neutrálny (e)."
    ),
    288: (
        "Kyslý charakter roztoku pri 25 °C určuje podmienka pH < 7, pOH > 7, resp. [OH-] < 10^-7 mol/l. "
        "Koncentrácia [OH-] = 10^-10 mol/l zodpovedá pOH = 10 a pH = 4, čo je kyslé prostredie (c). "
        "Hodnoty pOH = 9 a pOH = 14 zodpovedajú kyslému pH = 5 a silne kyslému pH = 0 (e, f). "
        "Hodnota pH = 0 priamo vyjadruje extrémne kyslý roztok s koncentráciou [H3O+] = 1 mol/l (h)."
    ),
    289: (
        "Kyslé a zásadité vlastnosti látok sa podľa Brönstedovej protolytickej teórie prejavujú v reakciách spojených s výmenou protónu H+, "
        "ktoré sa označujú ako protolytické alebo acidobázické reakcie (a, f). Typickým reprezentantom acidobázických reakcií je neutralizácia, "
        "pri ktorej kyselina reaguje so zásadou za vzniku soli a vody (g). Redoxné reakcie sú založené na výmene elektrónov a zrážacie na vylučovaní málo rozpustnej tuhej fázy."
    ),
    290: (
        "Brönstedova kyselina je definovaná ako častica schopná odovzdať protón H+ (donor protónu). Kyselina chlorovodíková HCl je silným donorom protónu (a), "
        "hydrogenfosforečnanový anión (HPO4)2- odovzdáva protón za vzniku (PO4)3- (c), voda H2O môže pôsobiť ako kyselina odštiepením H+ za vzniku OH- (d) "
        "a hydrogénuhličitan (HCO3)- disociuje na (CO3)2- (h). Častice Cl-, NH3, pyridín a OH- sú naopak akceptormi protónov (zásadami)."
    ),
    291: (
        "Brönstedova zásada je akceptor protónu, teda častica schopná viazať protón H+ pomocou voľného elektrónového páru. "
        "Chloridový anión Cl- viaže protón za vzniku HCl (b), molekula vody H2O vystupuje ako zásada prijatím protónu za vzniku H3O+ (d), "
        "síranový anión (SO4)2- prijatím protónu tvorí hydrogénsíran (f) a hydroxidový anión OH- prijatím protónu tvorí vodu (g). "
        "Molekuly HCl, H3PO4, H2CO3 a katión NH4+ sú naopak donormi protónov."
    ),
    292: (
        "Kyselina octová je slabý elektrolyt, ktorý vo vode disociuje len z nepatrnej časti (okolo 1 %), preto je v jej roztoku koncentrácia "
        "voľného octanového aniónu c(CH3COO-) veľmi nízka (e). Octan draselný je silný elektrolyt a disociuje úplne, takže c(CH3COO-) v roztoku soli "
        "je mnohonásobne vyššia než v roztoku kyseliny o rovnakej látkovej koncentrácii (a). Roztok soli navyše aniónovou hydrolýzou vytvára "
        "zásadité prostredie s vyššou c(OH-) než kyslý roztok kyseliny octovej (g). Zmiešaním roztoku slabej kyseliny octovej a jej soli vzniká acetátová tlmivá sústava (h)."
    ),
    293: (
        "Pri rovnakej molárnej koncentrácii H2SO4 a Na2SO4 obe zlúčeniny disociujú za uvoľnenia rovnakého počtu síranových aniónov, "
        "takže koncentrácia c(SO4^2-) je v oboch roztokoch zhodná (b). Kyselina sírová je silná dvojsýtna kyselina produkujúca vysokú koncentráciu H3O+, "
        "čo vedie k nízkemu pH a vysokému pOH (e, h). Roztok neutrálnej soli Na2SO4 nehydrolyzuje a má neutrálne pH = 7, čo predstavuje výrazne vyššiu "
        "koncentráciu OH- iónov (10^-7 mol/l) než v silne kyslom roztoku H2SO4 (f)."
    ),
    294: (
        "Neutralizácia je acidobázická reakcia medzi kyselinou a zásadou (d), ktorej podstatou je zlučovanie oxóniových katiónov H3O+ "
        "a hydroxidových aniónov OH- za vzniku neutrálnych molekúl vody a príslušnej soli reagujúcej kyseliny (h). Táto stechiometrická reakcia "
        "s nízkou aktivačnou energiou tvorí základ odmerného stanovenia v analytickej chémii – acidobázických titrácií (c). Neutralizácia je exotermická reakcia uvoľňujúca neutralizačné teplo."
    ),
    295: (
        "Podľa Brönstedovej teórie sú kyseliny látky, ktoré sú schopné v protolytickej reakcii odštiepiť a odovzdať vodíkový katión – protón H+ (donory protónu) (a, e, h). "
        "Akceptormi protónov sú zásady (b) a prenos elektrónov je základom redoxných dejov alebo Lewisovej teórie (c, d). "
        "Kyseliny neuvoľňujú plynný molekulárny vodík H2, ale hydratovaný ión H+ (f)."
    ),
    296: (
        "Brönstedova zásada je definovaná ako akceptor protónu, teda častica schopná prijať protón H+ v protolytickej reakcii (b, h). "
        "Keďže protón nesie jeden elementárny kladný náboj, neutrálna zásada po jeho prijatí zvyšuje svoj kladný náboj (napr. NH3 -> NH4+) (f). "
        "Záporne nabitá zásada zasa po naviazaní H+ znižuje veľkosť svojho záporného náboja v absolútnej hodnote (napr. CH3COO- -> CH3COOH) (g). "
        "Prijímanie elektrónov definuje Lewisovu kyselinu alebo oxidovadlo (c, d)."
    ),
    297: (
        "Podľa Lewisovej teórie je kyselina akceptorom elektrónového páru, ktorý obsahuje voľný orbitál schopný tento pár prijať (a, h). "
        "Lewisova zásada je donorom elektrónového páru a musí obsahovať aspoň jeden voľný (nevodiaci) elektrónový pár (g). "
        "Pretože každá Brönstedova zásada viaže protón prostredníctvom svojho voľného elektrónového páru, všetky Brönstedove zásady môžu vystupovať aj ako Lewisove zásady (c)."
    ),
    298: (
        "Chlorid draselný KCl je soľ silnej kyseliny a silnej zásady, vo vode nehydrolyzuje a roztok má neutrálne pH = 7 (a). "
        "Dusičnan amónny NH4NO3 je soľ slabej zásady a silnej kyseliny; katión NH4+ hydrolyzuje za uvoľnenia H3O+ a vytvára kyslé pH (c). "
        "Kyanidy NaCN a KCN sú soli slabej kyseliny HCN a silných zásad; kyanidový anión CN- hydrolyzuje podľa rovnice CN- + H2O <=> HCN + OH-, "
        "čo vedie k uvoľneniu OH- a zásaditému pH (d, f)."
    ),
    299: (
        "Pri rozpustení soli slabej kyseliny a silnej zásady prebieha aniónová hydrolýza produkujúca hydroxidové ióny OH-, takže pH stúpa (je zásadité), "
        "nie klesá (d je nepravdivý výrok). Roztok NH4Cl je v dôsledku hydrolýzy katiónu kyslý s pH < 7, nie pH > 7 (e je nepravdivý). "
        "Sulfid draselný K2S hydrolyzuje zásadito (S^2- + H2O <=> HS- + OH-), takže pH sa mení (f je nepravdivý). "
        "Chloristan draselný KClO4 je soľ silnej kyseliny a silnej zásady a hydrolýze vôbec nepodlieha (g je nepravdivý)."
    ),
    300: (
        "Kyslé pH vykazujú vodné roztoky solí slabej zásady a silnej kyseliny, ktorých katióny podliehajú katiónovej hydrolýze. "
        "Amónny katión v NH4NO3 a NH4Cl hydrolyzuje reakciou NH4+ + H2O <=> NH3 + H3O+, čím uvoľňuje oxóniové ióny (c, g). "
        "Katióny prechodných kovov Fe2+ v FeSO4 a Al3+ v Al(ClO4)3 tvoria vo vode hydratované hexaaqua komplexy, ktoré odštiepením protónu "
        "z koordinačnej sféry pôsobia ako Brönstedove kyseliny a okysľujú roztok (e, f). Soli K2SO4 sú neutrálne a roztoky Na2CO3, KCN a CH3COOK reagujú zásadito."
    )
}

def main():
    with open('scripts/chem_batches/batch_6.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)

    print(f"Loaded {len(questions)} questions from batch_6.json.")

    assert len(questions) == 50, f"Expected 50 questions, found {len(questions)}"
    assert len(explanations) == 50, f"Expected 50 explanations, found {len(explanations)}"

    for i, q in enumerate(questions):
        q_num = 251 + i
        # Ensure q starts with correct number
        assert q['content'].startswith(f"{q_num}."), f"Question number mismatch at index {i}: {q['content'][:15]}"
        assert q_num in explanations, f"Missing explanation for {q_num}"
        
        # Update explanation
        q['explanation'] = explanations[q_num]

    out_path = 'scripts/chem_batches/batch_6_explained.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(questions)} explained questions to {out_path}.")

if __name__ == '__main__':
    main()
