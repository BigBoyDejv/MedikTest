# -*- coding: utf-8 -*-
import json

explanations = {
    201: (
        "Chemická väzba predstavuje interakciu medzi atómami sprostredkovanú valenčnými elektrónmi, "
        "pričom podmienkou jej vzniku je priblíženie atómov a prekrytie ich valenčných orbitálov (b, h). "
        "Koordinačná (datívna) väzba vzniká prekrytím orbitálu s voľným elektrónovým párom donora s vakantným orbitálom akceptora, "
        "pričom po svojom vzniku má rovnaké vlastnosti ako bežná kovalentná väzba (e, f). "
        "Čím viac energie sa pri vzniku väzby uvoľní, tým je stabilnejšia (nie labilnejšia; a), "
        "a s rastúcou násobnosťou sa pevnosť väzby zvyšuje a jej dĺžka sa skracuje (c, g)."
    ),
    202: (
        "Sulfán (H2S) je plyn tvorený diskrétnymi molekulami s polárnymi kovalentnými väzbami, ktorý v tuhom stave tvorí "
        "molekulové (nie iónové) kryštály viazané slabými medzimolekulovými silami (a). Chlorid cézny (CsCl) je typická iónová "
        "zlúčenina s veľkým rozdielom elektronegativít (Δχ > 2,1), kde je väzba iónová, nie polárna kovalentná (h). "
        "Atómové kryštály ako diamant neobsahujú voľné elektróny ani ióny a nevedú elektrický prúd (b), "
        "pričom väzby v molekulách H2S aj metáne CH4 sú kovalentné (e, f)."
    ),
    203: (
        "V molekule fluoridu sírového SF6 má centrálny atóm síry hybridizáciu sp3d2, čo zodpovedá geometrii pravidelného osemstena (oktaédra), "
        "a v zlúčenine CsCl je vďaka veľkému rozdielu elektronegativít väzba iónová (a, b). Polarita chemickej väzby je priamo určená "
        "rozdielom elektronegativít atómov a model hybridizácie objasňuje vznik energeticky rovnocenných väzieb zmiešaním rôznych atómových orbitálov (f, h). "
        "V metáne CH4 sú väzby kovalentné (nie koordinačné; c) a molekula vody H2O vykazuje neekvivalentnú hybridizáciu sp3 (nie sp2; g)."
    ),
    204: (
        "Centrálny atóm uhlíka v kyseline uhličitej (H2CO3) je v stave hybridizácie sp2, vďaka čomu má planárne usporiadanie "
        "a atómy uhlíka a kyslíka ležia v jednej rovine s väzbovými uhlami približne 120° (a, e, h). "
        "Molekula obsahuje päť jednoduchých väzieb σ (dve väzby C–O, dve väzby O–H a jednu v rámci dvojitej väzby C=O) "
        "a jednu väzbu π medzi uhlíkom a karbonylovým kyslíkom (b). Uhlík nie je v stave hybridizácie sp (c) a molekula nemá lineárny tvar (f)."
    ),
    205: (
        "Jednoduchá kovalentná väzba je tvorená jedným spoločným elektrónovým párom (väzba σ) a je charakteristická pre nasýtené "
        "uhľovodíky (alkány) aj homonukleárne molekuly halogénov, ako je Br2 (d, e, g). Vzniká osovým prekrytím valenčných orbitálov, "
        "napríklad orbitálu s a p (c). Nemusí byť vždy polárna (v Br2 je nepolárna; b) a pri rozdiele elektronegativít nad 1,7 už väzba "
        "nadobúda prevažne iónový charakter (f)."
    ),
    206: (
        "Dvojitá kovalentná väzba je zložená z dvoch elektrónových párov – jednej pevnej väzby σ a jednej reaktívnejšej väzby π "
        "vznikajúcej bočným prekrytím p-orbitálov, pričom sa nachádza napríklad v molekule CS2 (S=C=S) (a, d). Prítomnosť voľnejšie viazaných "
        "π-elektrónov spôsobuje vyššiu chemickú reaktivitu dvojitej väzby a jej schopnosť podliehať adíciám, ktorými prechádza na jednoduchú väzbu (g, h). "
        "V molekule dusíka N2 je trojitá väzba (c) a eliminačnou reakciou násobné väzby naopak vznikajú (f)."
    ),
    207: (
        "V molekule vody H2O je medzi atómom vodíka a kyslíka jednoduchá kovalentná väzba s výraznou polaritou, "
        "keďže rozdiel elektronegativít kyslíka a vodíka je približne 1,24 (a, h). Táto väzba je mimoriadne pevná a stabilná, "
        "čomu zodpovedá jej vysoká väzbová energia 463 kJ·mol⁻¹ (g). Vodíkové mostíky vo vode predstavujú medzimolekulové interakcie, "
        "nie kovalentnú väzbu vnútri molekuly (d), a rozdiel elektronegativít nie je dostatočný na vznik iónovej väzby (e)."
    ),
    208: (
        "Väzbovosť je číslo udávajúce počet kovalentných väzieb (zdieľaných elektrónových párov), ktorými sa atóm viaže v danej zlúčenine (h). "
        "Na jej odvodenie je často nutné vychádzať z excitovaného stavu atómu, napríklad pri síre v SF6, kde je šesťväzbová vďaka sp3d2 hybridizácii (c, f). "
        "Dusík môže mať rôznu väzbovosť podľa typu zlúčeniny (trojväzbový v NH3, štvorväzbový s využitím voľného páru v NH4+; g). "
        "Uhlík má v excitovanom stave konfiguráciu 2s1 2p3, teda tri elektróny v p-orbitáloch, nie štyri (e)."
    ),
    209: (
        "Medzi základné typy jednoduchej hybridizácie patria sp, sp2 a sp3, pričom pri neekvivalentnej hybridizácii sp3 (napr. H2O, NH3) "
        "voľné elektrónové páry odpudzujú väzbové páry a deformujú pravidelný štvorsten (a, b). V karboxylovej skupine je atóm uhlíka "
        "v hybridizácii sp2 s planárnym usporiadaním a dsp2 hybridné orbitály smerujú do vrcholov štvorca (d, g). "
        "Molekula PCl5 má tvar trojbokého (trigonálneho), nie štvorbokého bipyramídu (h), a alkény majú planárnu trojuholníkovú geometriu (f)."
    ),
    210: (
        "Keďže priama reakcia redukcie oxidu železitého vykazuje kladnú zmenu entalpie (ΔH = +463,8 kJ > 0), ide o endotermický proces "
        "spotrebovávajúci teplo z okolia (b, h). V súlade s Le Chatelierovým princípom posunie zvýšenie teploty chemickú rovnováhu v smere "
        "endotermického deja, teda v smere tvorby kovového železa (d). Na vznik jedného mólu Fe je potrebné dodať štvrtinu reakčného tepla "
        "(463,8 / 4 = 115,95 kJ), nie celé teplo (f), pričom možnosti b, d, g, h tvoria oficiálny kľúč testovnice."
    ),
    211: (
        "Reakcia je endotermická (ΔH > 0), pričom uhlík vystupuje ako redukovadlo redukujúce Fe2O3 na elementárne železo (a, h). "
        "Na redukciu dvoch mólov Fe2O3 sa spotrebuje 463,8 kJ, čo znamená, že na 1 mol Fe2O3 pripadá presne 231,9 kJ tepla (b). "
        "Oficiálny kľúč testovnice zahŕňa možnosti a, b, d, h; pri endotermickom deji sa teplo zo sústavy neuvoľňuje, ale pohlcuje (c)."
    ),
    212: (
        "Zmena entalpie pri rozrušení kryštálovej štruktúry je kladná (endotermická mriežková energia, +781 kJ·mol⁻¹) a celkový tepelný "
        "efekt rozpúšťania je daný súčtom tejto energie a exotermickej hydratačnej energie (-773 kJ·mol⁻¹) (a, d). "
        "Pretože mriežková energia prevyšuje hydratačnú, výsledný dej je mierne endotermický (ΔH = +8 kJ·mol⁻¹) a závisí od teploty (f, h). "
        "Keďže sa teplo spotrebováva, roztok sa pri rozpúšťaní nezahrieva, ale nepatrne ochladzuje (b, e, g)."
    ),
    213: (
        "Aktivačná energia (Ea) predstavuje energetickú bariéru medzi reaktantmi a produktmi, ktorú musia častice prekonať na vytvorenie "
        "aktivovaného komplexu, pričom sa rovná rozdielu energie aktivovaného komplexu a reaktantov (a, b, d). "
        "Prítomnosť katalyzátora otvára novú reakčnú cestu s nižšou aktivačnou energiou (e). Aktivačná energia má jednotku kJ·mol⁻¹ "
        "(nie je bezrozmerná; c) a prekonávajú ju častice s energiou rovnou alebo vyššou než Ea (f)."
    ),
    214: (
        "Entalpia (H) je extenzívna stavová veličina s jednotkou kJ·mol⁻¹, ktorá sa využíva na popis tepelnej bilancie chemických dejov "
        "pri konštantnom tlaku (izobarické podmienky) (b, f). Rozdiel entalpií produktov a reaktantov sa pri konštantnom tlaku rovná "
        "reakčnému teplu Qp (ΔH = Qp) (c, h). Mieru neusporiadanosti sústavy vyjadruje entropia S, nie entalpia (e), "
        "a entalpia priamo závisí od látkového množstva systému (g)."
    ),
    215: (
        "Rýchlosť chemickej reakcie závisí od frekvencie a úspešnosti zrážok reagujúcich častíc, čo priamo ovplyvňuje koncentrácia "
        "reaktantov, teplota sústavy a plošný obsah povrchu tuhých fáz v heterogénnych sústavách (a, e, f). "
        "Prítomnosť katalyzátora znižuje aktivačnú energiu a dramaticky zvyšuje reakčnú rýchlosť (c). "
        "Tlak nemá výrazný vplyv na reakcie tuhých látok (b) a koncentrácia produktov ani rovnovážna konštanta neurčujú počiatočnú rýchlosť priamej reakcie (d, g)."
    ),
    216: (
        "Poriadok chemickej reakcie je empiricky stanovená veličina určujúca, ako závisí rýchlosť reakcie od koncentrácie reaktantov (e, f). "
        "Definuje sa ako súčet exponentov pri koncentráciách látok v rýchlostnej rovnici v = k·[A]^α·[B]^β a môže nadobúdať celočíselné, "
        "zlomkové aj nulové hodnoty (reakcie nultého poriadku) (a, b). Počet zrážajúcich sa častíc vyjadruje molekularita, nie poriadok reakcie (d)."
    ),
    217: (
        "Samovoľnosť reakcie podmieňuje pokles Gibbsovej energie (ΔG = ΔH – T·ΔS < 0). Teplota rovnovážneho obratu je T = ΔH / ΔS = "
        "(-100 000 J·mol⁻¹) / (-200 J·mol⁻¹·K⁻¹) = 500 K, čo zodpovedá 227 °C (e, h). Keďže reakcia je exotermická (ΔH < 0), "
        "no sprevádzaná poklesom entropie (ΔS < 0), prebieha spontánne len pri teplotách pod 500 K (pod 227 °C), kde entalpický člen "
        "preváži nad členom –T·ΔS (d, g)."
    ),
    218: (
        "Entropia (S) je mierou neusporiadanosti systému, pričom k jej výraznému nárastu (ΔS > 0) dochádza pri procesoch spojených so vznikom "
        "plynných látok z kvapalín alebo pevných fáz, keďže plyny majú podstatne vyššiu molekulovú voľnosť (a, d, e, h). "
        "Pri vyparovaní vody (a), rozklade CaCO3 (d), rozklade HgO (e) a termickom rozklade dichrómanu amónneho (h) vzniká plynné skupenstvo. "
        "Naopak pri tuhnutí vody (f) alebo zlučovaní plynu na pevnú látku (b, c, g) entropia klesá."
    ),
    219: (
        "Pri exotermickej reakcii sa reakčné teplo uvoľňuje do okolia (ΔH < 0) (a). Reakcia prebieha samovoľne iba vtedy, ak je exergonická, "
        "teda ak je celková zmena Gibbsovej energie záporná (ΔG < 0) (h). Ak je však exotermická reakcia spojená s poklesom entropie (ΔS < 0), "
        "pri vysokých teplotách člen –T·ΔS preváži nad zápornou entalpiou, ΔG nadobudne kladnú hodnotu a reakcia sa stane endergonickou (f)."
    ),
    220: (
        "Entropia (S) je termodynamická stavová veličina vyjadrujúca mieru neusporiadanosti a pravdepodobnosti mikrostavov sústavy "
        "podľa Boltzmannovho vzťahu S = k·ln W (a, g, h). Termodynamicky je jej zmena pri vratnom deji vyjadrená podielom vymeneného tepla "
        "a absolútnej teploty (ΔS = Q/T) (d). Rýchlosť reakcie skúma chemická kinetika (b) a tepelné efekty izobarických reakcií popisuje entalpia (c)."
    ),
    221: (
        "Súčin rozpustnosti (Ks) je rovnovážna konštanta charakterizujúca heterogénnu dynamickú rovnováhu medzi tuhou fázou málo rozpustného "
        "elektrolytu a jeho voľnými iónmi v nasýtenom roztoku (c). Pre zlúčeninu typu AxBy je definovaný vzťahom Ks = [A]^x · [B]^y (f). "
        "Ako každá rovnovážna konštanta je teplotne závislý (e) a nepriamo kvantifikuje rozpustnosť danej látky v rozpúšťadle (d). "
        "Čím je hodnota Ks vyššia, tým je elektrolyt v danom rozpúšťadle rozpustnejší (g)."
    ),
    222: (
        "Disociačná konštanta komplexu (Kd) vyjadruje mieru rozpadu komplexnej častice na centrálny atóm a ligandy; čím je jej hodnota nižšia, "
        "tým menej komplex v roztoku disociuje a tým je stabilnejší (stálejší) (d). Konštanta stability (tvorenia, β) je prevrátenou hodnotou "
        "disociačnej konštanty (β = 1/Kd), takže s klesajúcou Kd stabilita aj pravdepodobnosť vzniku komplexu rastie (f, h). "
        "Nízka hodnota Kd teda jednoznačne svedčí o vysokej termodynamickej stálosti koordinačnej zlúčeniny (a, e)."
    ),
    223: (
        "Pri aluminotermickej redukcii oxidu železitého hliníkom (Fe2O3 + 2 Al → 2 Fe + Al2O3) sa uvoľňuje 850 kJ tepla, "
        "preto sa v klasickej termochemickej rovnici uvoľnené teplo zapisuje s kladným znamienkom na strane produktov (+850 kJ) (d). "
        "Kľúč testovnice UPJŠ pre túto úlohu označuje možnosti d, f, h (d, f, h). "
        "V modernom termodynamickom zápise pomocou reakčnej entalpie má exotermická reakcia záporné reakčné teplo (ΔH = -850 kJ/mol)."
    ),
    224: (
        "Endotermické reakcie sú deje sprevádzané pohlcovaním tepla zo susedstva, pričom teplo vystupuje na strane reaktantov s kladným znamienkom "
        "(ako pri Boudouardovej reakcii: CO2 + C + 110 kJ → 2 CO), prípadne je reakčná entalpia kladná (ΔH > 0) (d). "
        "Oficiálny kľúč testovnice UPJŠ pre túto otázku priraďuje možnosti b, d, g (b, d, g). "
        "Naopak exotermické reakcie uvoľňujú teplo na strane produktov (a, e)."
    ),
    225: (
        "Pri endotermických reakciách je reakčné teplo absorbované zo susedstva (ΔH > 0), pričom celkový tepelný efekt je priamo úmerný "
        "látkovému množstvu zreagovaných látok (d, h). Hoci je kladná hodnota entalpie pre samovoľnosť nevýhodná, proces môže prebehnúť, "
        "ak je sprevádzaný nárastom entropie (ΔS > 0) a pri dostatočnej teplote člen –T·ΔS zabezpečí zápornú Gibbsovu energiu (ΔG < 0) (f). "
        "Možnosti c, d, f, h tvoria oficiálnu kombináciu kľúča testovnice UPJŠ."
    ),
    226: (
        "Pri reakcii H2O(g) + C(s) ⇌ CO(g) + H2(g) vznikajú z jedného mólu plynu dva móly plynných produktov, preto zníženie tlaku "
        "v súlade s Le Chatelierovým princípom posunie rovnováhu v smere väčšieho objemu plynov, teda doprava k produktom (b). "
        "Rovnako odčerpávanie produktov alebo pokles koncentrácie CO núti systém kompenzovať stratu tvorbou nových produktov (f, h). "
        "Oficiálny kľúč testovnice UPJŠ pre túto otázku zahŕňa kombináciu možností b, e, f, h."
    ),
    227: (
        "Rozpúšťacie teplo vyjadruje tepelnú bilanciu pri rozpustení jedného mólu látky v rozpúšťadle, ktorá pozostáva z endotermického rozpadu "
        "kryštálovej štruktúry a exotermickej solvatácie (hydratácie) vzniknutých iónov (f). V závislosti od prevahy jedného z týchto príspevkov "
        "sa teplo pri rozpúšťaní môže uvoľňovať (ΔH < 0, napr. NaOH) alebo pohlcovať a nadobúdať kladné hodnoty (ΔH > 0, napr. NH4NO3) (c, h). "
        "Oficiálny kľúč testovnice UPJŠ pre túto úlohu kombinuje možnosti b, c, f, h."
    ),
    228: (
        "Rýchlosť reakcie vyjadruje časovú zmenu látkovej koncentrácie reaktantov alebo produktov a jej základnou jednotkou je mol·dm⁻³·s⁻¹ (g). "
        "Podľa Guldbergovho-Waageovho zákona rýchlosť priamo závisí od okamžitých koncentrácií reaktantov (c), a katalyzátor ju zvyšuje "
        "znižovaním aktivačnej energie (e). Podľa empirického van 't Hoffovho pravidla zvýšenie teploty o 10 °C urýchľuje chemickú reakciu "
        "približne 2- až 4-násobne v dôsledku nárastu podielu aktívnych zrážok (h)."
    ),
    229: (
        "Rýchlostná konštanta k charakterizuje kinetiku danej reakcie a je nezávislá od okamžitých koncentrácií reagujúcich látok, "
        "avšak významne závisí od teploty sústavy (c). Teplotnú závislosť rýchlostnej konštanty kvantitatívne popisuje Arrheniova rovnica "
        "k = A·exp(-Ea/RT), z ktorej vyplýva exponenciálny nárast k so zvyšujúcou sa teplotou (g). "
        "Oficiálny kľúč testovnice UPJŠ pre túto testovú otázku označuje kombináciu možností c, e, g, h."
    ),
    230: (
        "Rýchlosť a hĺbku premeny reaktantov na produkty vyjadruje rovnovážna konštanta K podľa zákona účinku hmotností. "
        "Veľmi vysoká hodnota K (K >> 1) značí, že v rovnovážnej zmesi prevládajú takmer výlučne produkty a reakcia prebehla prakticky úplne (f). "
        "Naopak nízka hodnota K (K << 1) indikuje, že rovnováha leží výrazne vľavo a v systéme zostali prítomné prakticky iba pôvodné reaktanty (c). "
        "Kombinácia možností b, c, f, g predstavuje formálny kľúč testovnice UPJŠ."
    ),
    231: (
        "Rýchlosť chemických reakcií (vrátane endotermických) stúpa so zvyšujúcou sa teplotou v dôsledku vyššej kinetickej energie molekúl "
        "a vyššieho podielu účinných zrážok (a). Katalyzátory znižujú aktivačnú energiu a urýchľujú priamu aj spätnú reakciu, pričom z reakcie "
        "vystupujú v chemicky nezmenenej forme (c). Oficiálny kľúč testovnice UPJŠ priraďuje pre túto úlohu možnosti a, c, f, h; "
        "v skutočnosti katalyzátor hodnotu rovnovážnej konštanty K vôbec nemení."
    ),
    232: (
        "Úloha požaduje vybrať tvrdenia, ktoré pre rýchlostnú konštantu k NEPLATIA. Z Arrheniovej rovnice vyplýva, že rýchlostná konštanta "
        "závisí exponenciálne od teploty, preto tvrdenie o jej nezávislosti od teploty neplatí (a). Kľúč testovnice UPJŠ označuje "
        "ako neplatiace možnosti a, c, d (a, c, d). V skutočnosti je hodnota k pri konštantnej teplote nezávislá od okamžitých koncentrácií reaktantov."
    ),
    233: (
        "Hoci záhlavie otázky uvádza pojem inhibítory, obsah možností a oficiálny kľúč testovnice UPJŠ (a, b, e, g) sa vzťahujú "
        "na posuny rovnováhy pri disociácii oxidu dusičitého (N2O4 ⇌ 2 NO2) (a, b, e, g). Podľa Le Chatelierovho princípu prídavok NO2 "
        "núti sústavu znížiť jeho koncentráciu posunom rovnováhy v smere tvorby diméru N2O4 (e). Zníženie tlaku či zmeny teploty menia polohu "
        "rovnováhy v závislosti od stechiometrie plynných častíc a tepelného efektu premeny (a, b, g)."
    ),
    234: (
        "Pre endotermickú disociáciu N2O4(g) ⇌ 2 NO2(g) (ΔH = +58 kJ·mol⁻¹) platí, že zvýšenie teploty posúva chemickú rovnováhu "
        "v smere endotermického deja, teda v smere tvorby produktov (doprava) (h). Rovnováhu doprava posúva aj kontinuálne odoberanie "
        "produktu NO2 zo systému (d). Naopak pridaním NO2 sa rovnováha v súlade s princípom akcie a reakcie posunie doľava v prospech reaktantu N2O4 (e)."
    ),
    235: (
        "Chemická rovnováha sa riadi Le Chatelierovým princípom akcie a reakcie, podľa ktorého vonkajší zásah vyvolá dej smerujúci k jeho zoslabeniu, "
        "preto zvýšenie teploty podporuje endotermický smer reakcie (c, e). Katalyzátor znižuje aktivačnú energiu priamej aj spätnej reakcie "
        "v rovnakej miere, urýchľuje iba ustavenie rovnováhy a nemá žiadny vplyv na rovnovážne zloženie zmesi (a). "
        "Oficiálny kľúč testovnice UPJŠ pre túto otázku kombinuje možnosti a, c, d, e."
    ),
    236: (
        "Rýchlosť chemickej reakcie je definovaná ako časový úbytok koncentrácie reaktantov alebo prírastok produktov. "
        "Keďže koncentrácia reaktantov (metanolu a kyseliny mravčej) v priebehu reakcie klesá, pred deriváciu sa kladie záporné znamienko: "
        "v = -d[CH3OH]/dt a v = -d[HCOOH]/dt, aby hodnota rýchlosti zostala kladná (c, f). "
        "Oficiálny kľúč testovnice UPJŠ uvádza pre túto otázku možnosti a, c, e, f."
    ),
    237: (
        "Rovnovážna konštanta K je termodynamická veličina závislá výlučne od teploty a typu reakcie (c). Ak je hodnota K veľmi nízka, "
        "v rovnovážnej zmesi dominujú reaktanty a premena na produkty je nepatrná (b). Pri heterogénnom rozklade vápenca "
        "CaCO3(s) ⇌ CaO(s) + CO2(g) v uzavretom systéme je rovnovážna konštanta priamo úmerná rovnovážnemu parciálnemu tlaku CO2 "
        "(Kp = p(CO2)) (h), pričom oficiálny kľúč testovnice zahŕňa možnosti b, c, f, h."
    ),
    238: (
        "Pri heterogénnom termickom rozklade MgCO3(s) ⇌ MgO(s) + CO2(g) v uzavretom systéme je rovnovážna konštanta priamo určená "
        "parciálnym tlakom plynného CO2 (Kp = p(CO2)) (b). Spaľovanie metánu je nevratná reakcia s mimoriadne vysokou hodnotou K, "
        "pri ktorej je spätná reakcia prakticky neuskutočniteľná (c). Oficiálny kľúč testovnice UPJŠ priraďuje k tejto otázke možnosti b, c, d, h; "
        "katalyzátor (ureáza) v skutočnosti rovnovážnu konštantu K nemení, iba urýchľuje jej ustavenie."
    ),
    239: (
        "Podľa Guldbergovho-Waageovho zákona účinku hmotností je rovnovážna konštanta K pre reakciu 2 FeCl3 + SnCl2 ⇌ 2 FeCl2 + SnCl4 "
        "daná podielom rovnovážnych koncentrácií produktov a reaktantov s príslušnými exponentmi: K = ([FeCl2]² · [SnCl4]) / ([FeCl3]² · [SnCl2]) (c). "
        "Keďže reakcia prebieha v roztoku bez prítomnosti plynnej fázy, zmena tlaku nemá na polohu chemickej rovnováhy žiadny vplyv (g). "
        "Možnosti a, b, c, g tvoria formálny kľúč testovnice UPJŠ."
    ),
    240: (
        "Zmeny rovnovážneho zloženia vplyvom teploty, tlaku a koncentrácií sa riadia Le Chatelierovým princípom akcie a reakcie. "
        "Zvýšenie teploty podporuje endotermické deje, kým zníženie teploty posúva rovnováhu v prospech exotermických procesov, "
        "a zmena tlaku vplýva len na plynné sústavy so zmenou počtu mólov (c, f, g, h). "
        "Možnosti c, f, g, h predstavujú správne odpovede podľa oficiálnej testovnice UPJŠ LF."
    ),
    241: (
        "Zmena tlaku neovplyvňuje rovnovážny stav plynných reakcií vtedy, ak na oboch stranách rovnice vystupuje rovnaký počet mólov plynu (Δn(g) = 0). "
        "Pri syntéze HI (1 H2 + 1 I2 ⇌ 2 HI), spaľovaní metánu na paru (1 CH4 + 2 O2 → 1 CO2 + 2 H2O) aj oxidácii CO (1 CO + 1 NO2 → 1 CO2 + 1 NO) "
        "je látkové množstvo plynov na oboch stranách rovnaké, takže tlak stav rovnováhy nezmení (e, f, g). "
        "Oficiálny kľúč testovnice UPJŠ uvádza kombináciu možností c, e, f, g."
    ),
    242: (
        "Chemické reakcie sú deje, pri ktorých dochádza k zániku pôvodných chemických väzieb v reaktantoch a vzniku nových väzieb v produktoch (a). "
        "Podľa mechanizmu a prenášaných častíc sa delia na protolytické (výmena H+), redoxné (výmena elektrónov), zrážacie (vznik zrazeniny) "
        "a komplexotvorné (vznik donor-akceptorových väzieb) (e). Kľúč testovnice UPJŠ pre túto otázku označuje ako správne možnosti a, e, f, g."
    ),
    243: (
        "V priebehu chemických reakcií platí zákon zachovania hmotnosti a prvkov: atómy nezanikajú ani nevznikajú, iba sa preskupujú do nových molekúl, "
        "takže celkový počet a druh atómov reagujúcich látok zostáva konštantný (c, h). Pri bežných chemických dejoch sa nemenia atómové jadrá, "
        "ale dochádza k zmenám v elektrónových obaloch. Oficiálny kľúč testovnice UPJŠ zahŕňa možnosti a, b, c, e, h."
    ),
    244: (
        "Reakčné teplo predstavuje množstvo tepla vymenené medzi sústavou a okolím pri stechiometrickom priebehu reakcie, pričom pri endotermických "
        "dejoch nadobúda kladné hodnoty (ΔH > 0), pretože sústava teplo absorbuje (f). Pri izobarických dejoch sa reakčné teplo rovná zmene entalpie "
        "(Qp = ΔH) a pri izochorických dejoch zmene vnútornej energie (Qv = ΔU). Kľúč testovnice UPJŠ uvádza pre túto otázku možnosti c, d, f, g."
    ),
    245: (
        "Úloha vyžaduje vybrať nesprávne tvrdenia o reakčnom teple. Reakčné teplo za konštantného tlaku zodpovedá zmene entalpie (ΔH), "
        "nie zmene entropie (ΔS), ktorá kvantifikuje neusporiadanosť sústavy (f). Reakčné teplo závisí od skupenstva reagujúcich látok "
        "a pri exotermických dejoch sa teplo uvoľňuje (ΔH < 0). Podľa kľúča testovnice UPJŠ sú ako nesprávne tvrdenia vyznačené možnosti a, b, f, h."
    ),
    246: (
        "Pri syntéze SO3 (2 SO2 + O2 ⇌ 2 SO3) dochádza k úbytku plynných častíc z troch na dva móly, preto zvýšenie tlaku posúva rovnováhu "
        "v smere menšieho objemu, teda v prospech vzniku oxidu sírového (e). Reakčné teplo tejto oxidácie možno klasifikovať aj ako spaľovacie "
        "teplo oxidu siričitého (f). Podľa prvého termochemického zákona (Lavoisier-Laplace) je reakčné teplo priamej a spätnej reakcie "
        "rovnaké čo do absolútnej hodnoty a líši sa len znamienkom (c, g)."
    ),
    247: (
        "Reakcia je exergonická vtedy, ak je celková zmena Gibbsovej voľnej energie záporná (ΔG < 0), čo znamená, že premena prebieha samovoľne "
        "a sústava energiu uvoľňuje (d). Ak je reakcia súčasne exotermická (ΔH < 0) a sprevádzaná nárastom entropie (ΔS > 0), ΔG je záporná "
        "pri každej teplote (f). Pri vzniku HCl sa uvoľní viac energie (863 kJ) než sa spotrebovalo na rozštiepenie väzieb (678 kJ), čo vedie "
        "k uvoľneniu energie (e). Kľúč testovnice UPJŠ uvádza možnosti b, d, e, f."
    ),
    248: (
        "Pri exotermických reakciách sa uvoľňuje teplo (ΔH < 0), preto podľa Le Chatelierovho princípu privádzanie tepla (zvýšenie teploty) "
        "posúva chemickú rovnováhu v smere reaktantov, aby sa dodané teplo spotrebovalo (d). Katalyzátor urýchľuje dosiahnutie rovnovážneho "
        "stavu znížením Ea, ale množstvo uvoľneného reakčného tepla nemení (a). Možnosti d, e, f, h tvoria oficiálny kľúč testovnice UPJŠ LF."
    ),
    249: (
        "Pri syntéze amoniaku (N2 + 3 H2 ⇌ 2 NH3) vznikajú zo štyroch mólov plynu iba dva, čo znamená zníženie neusporiadanosti a pokles entropie (ΔS < 0) (e). "
        "Zvýšenie tlaku podľa Le Chatelierovho princípu posunie rovnováhu v smere menšieho počtu plynných molekúl, teda tvorby amoniaku (d). "
        "Reakcia je exotermická a v praxi prebieha pri zvýšenej teplote a tlaku (b), pričom tlaková rovnovážna konštanta je Kp (g)."
    ),
    250: (
        "Chemická rovnováha je dynamický stav uzavretej sústavy, v ktorom prebieha priama aj spätná reakcia rovnakou rýchlosťou, "
        "koncentrácie látok sa nemenia a systém je charakterizovaný rovnovážnou konštantou K pri danej teplote (c). V otvorenej sústave s unikajúcim "
        "plynným produktom sa rovnováha nemôže ustaviť, kým v heterogénnych sústavách bežne existuje (napr. súčin rozpustnosti). "
        "Oficiálny kľúč testovnice UPJŠ pre túto otázku zahŕňa kombináciu možností a, c, d, e, g."
    )
}

def main():
    with open('scripts/chem_batches/batch_5.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} questions from batch_5.json")
    assert len(data) == 50, f"Expected 50 questions, found {len(data)}"

    for i, q in enumerate(data):
        q_num = 201 + i
        if q_num not in explanations:
            raise KeyError(f"Missing explanation for question {q_num}")
        q['explanation'] = explanations[q_num]

    out_path = 'scripts/chem_batches/batch_5_explained.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(data)} explained questions to {out_path}")

    # Verification
    with open(out_path, 'r', encoding='utf-8') as f:
        check = json.load(f)
    print(f"Verified {len(check)} items in {out_path}")
    for i in range(len(check)):
        assert 'explanation' in check[i]
        assert len(check[i]['explanation']) > 50

    print("Verification passed! First 2 explanations:")
    print("Q201:", check[0]['explanation'])
    print("---")
    print("Q202:", check[1]['explanation'])

if __name__ == '__main__':
    main()
