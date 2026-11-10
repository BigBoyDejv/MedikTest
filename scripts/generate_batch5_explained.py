# -*- coding: utf-8 -*-
import json

explanations = {
    201: (
        "Mykoríza predstavuje mutualistické symbiotické spolužitie podhubia húb s koreňovým systémom vyšších rastlín (odpovede a, h). "
        "Huba uľahčuje rastline príjem vody a rozpustených minerálnych látok (najmä fosforu) a hostiteľská rastlina jej dodáva organické asimiláty z fotosyntézy. "
        "Spolužitie húb s riasami alebo sinicami sa označuje ako lichenizmus (lišajníky; c, d), zatiaľ čo mykóza je pomenovanie pre hubové ochorenie (f)."
    ),
    202: (
        "Chemosyntéza je autotrofný spôsob výživy fylogeneticky najstarších mikroorganizmov (najmä baktérií bez asimilačných pigmentov, ako sú nitrifikačné či sírne baktérie), ktoré fixujú CO2 ako zdroj uhlíka (odpovede a, c, e, h). "
        "Energiu na syntézu organických látok nezískavajú zo svetla, ale z oxidácie anorganických látok (napr. amoniaku, sírovodíka). "
        "Na rozdiel od heterotrofných organizmov nevyužívajú organický uhlík (glukózu) a sú vývojovo staršie než fotosyntéza (b, d, f, g)."
    ),
    203: (
        "Poloparazity (hemiparazity, napr. imelo biele) disponujú funkčným asimilačným aparátom s chlorofylom a organické látky si syntetizujú samostatne fotosyntézou (odpoveď a). "
        "Od hostiteľskej rastliny odčerpávajú pomocou premenených koreňov (haustórií) iba vodu a rozpustené minerálne látky z drevnej časti cievnych zväzkov (xylému). "
        "Hotové organické látky z lykovej časti cievnych zväzkov odčerpávajú iba úplné parazity (holoparazity, napr. kukučina; g)."
    ),
    204: (
        "Chemosyntetizujúce baktérie sú autotrofné organizmy bez asimilačných pigmentov, ktoré využívajú energiu uvoľnenú oxidáciou jednoduchých anorganických substrátov na syntézu organických látok z CO2 (odpovede b, d, e, g). "
        "Medzi typické chemoautotrofy patria sírne, železité, vodíkové a pôdne baktérie zapojené do kolobehu dusíka. "
        "Pretože nepoužívajú svetelné kvantá ani chlorofyly, nie sú pigmentované a nepatria medzi heterotrofy (a, c, f, h)."
    ),
    205: (
        "Denitrifikačné baktérie sú pôdne mikroorganizmy, ktoré v anaeróbnych podmienkach redukujú nitráty (dusičnany) na plynný dusík (N2), ktorý uniká do atmosféry (odpovede a, d, e). "
        "Týmto procesom ochudobňujú pôdu o prístupné formy dusíka, čo má v poľnohospodárstve negatívny hospodársky dopad. "
        "Nitrifikáciu (opačný dej oxidácie amoniaku na dusitany a dusičnany) uskutočňujú aeróbne nitrifikačné baktérie Nitrosomonas a Nitrobacter (b, c, f, g, h)."
    ),
    206: (
        "Potravové reťazce v prírode uzatvárajú reducenty (dekompozitory, saprofyty), predovšetkým pôdne baktérie a huby, ktoré rozkladajú mŕtvu organickú hmotu a mineralizujú ju na jednoduché anorganické živiny (odpovede a, d, h). "
        "Tým umožňujú opätovné využitie biogénnych prvkov primárnymi producentmi (zelenými rastlinami). "
        "Konzumenty a parazity čerpajú živiny zo živých organizmov a haustóriá slúžia na parazitovanie na živých hostiteľoch, nie na saprofytizmus (b, c, e, f, g)."
    ),
    207: (
        "Katabolické (disimilačné) procesy v rastlinách predstavujú degradačné biochemické dráhy, pri ktorých dochádza k štiepeniu zložitých organických molekúl na jednoduchšie látky za súčasného uvoľňovania energie (exergonické deje, napr. bunkové dýchanie; odpovede a, d, f, h). "
        "Časť uvoľnenej energie chemických väzieb sa ukladá vo forme makroergických väzieb ATP. "
        "Syntetické procesy spojené so spotrebou energie (endergonické, asimilačné deje ako fotosyntéza) tvoria anabolizmus (b, c, e, g)."
    ),
    208: (
        "Anabolické (asimilačné) procesy sú syntetické reakcie, pri ktorých rastlinná bunka z jednoduchých anorganických alebo organických zlúčenín buduje zložitejšie organické látky bohaté na energiu (napr. fotosyntéza; odpovede b, d, e, g). "
        "Tieto procesy sú endergonické, čo znamená, že prebiehajú so spotrebou voľnej energie (ATP alebo fotónov svetla). "
        "Katabolické deje (ako dýchanie) sú naopak disimilačné a energiu uvoľňujú (exergonické; a, c, f, h)."
    ),
    209: (
        "Cyanobaktérie (sinice) obsahujú ako hlavný asimilačný pigment chlorofyl a, doplnený o vo vode rozpustné fykobiliproteíny – modrý fykocyanín a červený fykoerytrín (fykobilíny), a β-karotén (odpovede a, b, c, g, h). "
        "Tieto pigmenty sú usporiadané do fykobilizómov a zachytávajú svetlo aj vo vlnových dĺžkach, ktoré chlorofyl neabsorbuje. "
        "Hemoglobín je krvné farbivo živočíchov a α-karotén či xantofyly u siníc netvoria hlavné fotosyntetické pigmenty (d, e, f)."
    ),
    210: (
        "Asimilačné farbivá zelených rastlín (chlorofyly a karotenoidy) sú zakotvené v membránach tylakoidov chloroplastov a slúžia ako svetlozberné antény absorbujúce fotóny viditeľného svetla v rozsahu 400 až 700 nm (odpovede b, d, f, g, h). "
        "Absorpcia svetla je vysoko špecifická pre jednotlivé pigmenty (absorpčné maximá v modrej a červenej oblasti). "
        "Prokaryoty nemajú chloroplasty a bakteriochlorofyly sú pigmentmi fotosyntetizujúcich baktérií, nie zelených rastlín (a, c, e)."
    ),
    211: (
        "Fotolýza vody (Hillova reakcia) je kľúčový proces primárnej (fotochemickej, svetelnej) fázy fotosyntézy viazaný na fotosystém II v tylakoidnej membráne (odpovede b, f). "
        "Svetlom indukované rozštiepenie molekuly vody poskytuje elektróny pre transportný reťazec, protóny (H+) na redukciu NADP+ a uvoľňuje molekulárny kyslík (O2). "
        "Calvinov cyklus patrí do sekundárnej fázy a Krebsov cyklus či glykolýza sú súčasťou katabolického bunkového dýchania (a, c, d, e, g, h)."
    ),
    212: (
        "Konečnými produktmi primárnych (svetelných) procesov fotosyntézy na tylakoidoch sú molekulárny kyslík (uvoľňovaný pri fotolýze vody), chemická energia vo forme ATP (vznikajúca fotofosforyláciou) a redukčné ekvivalenty NADPH + H+ (odpoveď f). "
        "Tieto produkty (ATP a NADPH + H+) sú následne využité v stróme chloroplastov v sekundárnych procesoch na redukciu CO2. "
        "Syntéza glukózy a iných sacharidov prebieha až v sekundárnej fáze (Calvinovom cykle; b, c, g)."
    ),
    213: (
        "Mäsožravé (karnivórne) rastliny obsahujú rozmanité biologicky aktívne látky (napr. naftochinóny ako plumbagín a flavonoidy), vďaka čomu sa využívajú v medicíne, farmácii a pri výskume liečiv proti nádorovým ochoreniam (odpovede b, c, e, h). "
        "Mnohé z nich (napr. Drosera) patria medzi chránené a vzácne liečivé rastliny. "
        "Sú to fotosyntetizujúce producenty prispôsobené pôdam chudobným na minerálny dusík, pričom vzdušný dusík viazať nedokážu a reducentmi nie sú (a, d, f, g)."
    ),
    214: (
        "Syntéza ATP v rastlinnej bunke prebieha na membránach prostredníctvom enzýmu ATP-syntázy poháňanej elektrochemickým protónovým gradientom: na vnútornej mitochondriálnej membráne (kristách) oxidačnou fosforyláciou a na membráne tylakoidov chloroplastov fotofosforyláciou (odpovede a, b, f). "
        "Menšie množstvo ATP vzniká substrátovou fosforyláciou v cytosóle, ale hlavným miestom syntézy sú spomínané semiautonómne organely. "
        "Jadro ani drsné endoplazmatické retikulum ATP nesyntetizujú (c, d, e, g, h)."
    ),
    215: (
        "Kyslík (O2) uvoľňovaný do ovzdušia počas fotosyntézy pochádza výlučne z vody, ktorá sa štiepi v primárnej fáze pri fotolýze vody spojenej s fotosystémom II (odpovede a, e). "
        "Voda slúži ako primárny donor elektrónov na redukciu oxidovaného reakčného centra P680. "
        "Kyslík nachádzajúci sa v molekulách CO2 sa využíva v Calvinovom cykle a zabudováva sa do molekúl sacharidov a novovznikajúcej vody (b, c, d, g, h)."
    ),
    216: (
        "Sekundárne procesy fotosyntézy (Calvinov cyklus a Hatch-Slackov cyklus) prebiehajú v stróme chloroplastov nezávisle od svetla a využívajú chemickú energiu ATP a NADPH na redukciu CO2 na sacharidy (odpovede a, b, c, g, h). "
        "Rastliny fixujú CO2 dvoma mechanizmami: pri C3 rastlinách je primárnym akceptorom pentóza ribulóza-1,5-bisfosfát a pri C4 rastlinách trojuhlíkatý fosfoenolpyruvát (PEP). "
        "Acetyl-CoA nefunguje ako akceptor CO2 pri fotosyntéze a možnosti e, f priraďujú akceptory opačne (d, e, f)."
    ),
    217: (
        "Fotochemická (svetelná) fáza fotosyntézy je podmienená prítomnosťou svetla a prebieha na membránach tylakoidov chloroplastov (odpovede a, c, e, g). "
        "Zahŕňa excitáciu chlorofylu, fotolýzu vody s uvoľnením O2 a elektrónov a fotofosforyláciu (syntézu ATP a redukciu NADP+ na NADPH + H+). "
        "Syntéza organických látok a spotreba ATP na fixáciu CO2 prebieha až v sekundárnej fáze, pričom fotolýza CO2 neexistuje (b, d, f, h)."
    ),
    218: (
        "Fotolýza vody je fotochemická disociácia molekuly vody účinkom absorbovaného svetelného žiarenia, ktorá prebieha v tylakoidoch chloroplastov pri fotosystéme II (odpovede a, d, f). "
        "Tento proces je viazaný striktne na svetlo a patrí medzi ústredné deje primárnych procesov fotosyntézy. "
        "Cyklická a necyklická môže byť fotofosforylácia (tok elektrónov), nie samotná fotolýza, a fotolýza neprebieha v cytoplazme ani v sekundárnej fáze (b, c, e, g, h)."
    ),
    219: (
        "Celková bilancia fotosyntézy zahŕňa uvoľnenie molekulárneho kyslíka (O2), tvorbu ATP a NADPH + H+ v primárnej fáze a následnú syntézu glukózy (a iných asimilátov) v sekundárnej fáze (odpovede b, c, g, h). "
        "Oxid uhličitý (CO2) je pri fotosyntéze spotrebovávaný, nie tvorený, a kyslík sa do nej nečerpá ako reaktant. "
        "Vznik 36 molekúl ATP je teoretický energetický zisk úplnej aeróbnej oxidácie glukózy pri dýchaní (a, d, e, f)."
    ),
    220: (
        "Pri sekundárnych procesoch fotosyntézy dochádza ku enzymatickej fixácii oxidu uhličitého na špecifický organický akceptor (odpovede a, d, g). "
        "Pri C3 rastlinách sa CO2 viaže na ribulóza-1,5-bisfosfát (RuBP) pôsobením enzýmu RuBisCO, zatiaľ čo pri C4 rastlinách sa viaže na fosfoenolpyruvát (PEP) pomocou PEP-karboxylázy. "
        "Anorganické substráty ani polysacharidy ako akceptory nepôsobia a oxalacetát je produktom, nie akceptorom C4 fixácie (b, c, e, f, h)."
    ),
    221: (
        "Fotoautotrofia (fotosyntéza) je typ autotrofnej výživy, pri ktorej organizmy (najmä rastliny, riasy a sinice) využívajú svetelnú energiu na tvorbu energeticky bohatých organických látok a kyslíka z anorganických zlúčenín (CO2 a H2O; odpovede b, d). "
        "Oxidácia anorganických látok s fixáciou CO2 je chemosyntéza (chemoautotrofia; h). "
        "Fotorespirácia je svetlom stimulované dýchanie spojené so stratami uhlíka a spaľovanie s uvoľňovaním energie je katabolizmus (a, c, e, f, g)."
    ),
    222: (
        "Dýchací reťazec je lokalizovaný vo vnútornej membráne mitochondrií (kristách) a tvorí ho sled enzýmových komplexov prenášajúcich elektróny na koncový akceptor – kyslík, za vzniku vody (odpovede d, f). "
        "Uvoľnená energia poháňa prenos protónov cez membránu, čím vzniká protónový gradient využívaný na syntézu ATP (oxidačná fosforylácia). "
        "V matrix prebieha Krebsov cyklus, chloroplasty slúžia fotosyntéze a dýchací reťazec ATP syntetizuje, neštiepi ho (a, b, c, e, g, h)."
    ),
    223: (
        "Rastliny vykonávajú bunkové dýchanie nepretržite vo dne aj v noci vo všetkých živých bunkách, pričom prijímajú atmosférický kyslík (O2), oxidujú organické substráty a do prostredia uvoľňujú CO2 a vodu (odpovede c, d, f, h). "
        "Cez deň je však respiračný výdaj CO2 prekrytý oveľa intenzívnejšou fotosyntézou, pri ktorej rastlina CO2 spotrebúva a O2 produkuje. "
        "Dýchanie nie je obmedzené iba na tmu a fotosyntetická premena slnečnej energie je odlišný fyziologický proces (a, b, e, g)."
    ),
    224: (
        "Glykolýza je fylogeneticky najstaršia, prvá etapa biologickej oxidácie glukózy, ktorá prebieha v cytoplazme aeróbnych aj anaeróbnych buniek (odpovede b, d, e, f, h). "
        "Ide o postupnú neúplnú anaeróbnu oxidáciu šesťuhlíkatej glukózy na dve trojuhlíkaté molekuly kyseliny pyrohroznovej (pyruvátu) za zisku 2 ATP a 2 NADH. "
        "Neprebieha v mitochondriách a na rozdiel od kvasenia nekončí laktátom či etanolom, hoci kvasenie na ňu pri nedostatku O2 nadväzuje (a, c, g)."
    ),
    225: (
        "Celkový energetický zisk pri úplnom aeróbnom odbúraní jednej molekuly glukózy cez glykolýzu, pyruvátdehydrogenázu, Krebsov cyklus a oxidačnú fosforyláciu na CO2 a H2O predstavuje 30 až 32 molekúl ATP (odpovede c, h). "
        "Tento zisk zodpovedá vytvoreniu 30 až 32 makroergických fosfátových väzieb schopných poháňať bunkovú prácu. "
        "Pri samotnej anaeróbnej glykolýze vznikajú iba 2 ATP a fotosyntéza glukózu naopak syntetizuje (a, b, d, f)."
    ),
    226: (
        "Kyselina pyrohroznová (pyruvát) je ústredný trojuhlíkatý produkt glykolýzy v cytoplazme, ktorý sa za aeróbnych podmienok transportuje do matrix mitochondrií (odpovede b, c, f). "
        "V mitochondriálnej matrix podlieha oxidačnej dekarboxylácii, pri ktorej vzniká acetyl-koenzým A (acetyl-CoA) a uvoľňuje sa CO2. "
        "Pyruvát nevstupuje priamo do Krebsovho cyklu, ale až po premene na acetyl-CoA, a Calvinov cyklus je súčasťou fotosyntézy (d, e, g, h)."
    ),
    227: (
        "Oxidačná fosforylácia je proces aeróbnej oxidácie redukovaných koenzýmov (NADH, FADH2) v dýchacom reťazci vnútornej membrány mitochondrií spriahnutý s fosforyláciou ADP na ATP (odpovede c, e, h). "
        "Prenos elektrónov na kyslík vytvára protónový gradient, ktorého energia sa prostredníctvom ATP-syntázy transformuje do makroergických väzieb ATP. "
        "Ide o aeróbny dej vyžadujúci O2 (konečný produkt je H2O, nie peroxidy) a fosforyluje sa ADP, nie ATP (a, b, d, f, g)."
    ),
    228: (
        "Pravé kvasenie (fermentácia) je anaeróbny rozklad organických látok (najmä sacharidov) pôsobením enzýmov mikroorganizmov (kvasinky, baktérie) alebo pri deficite kyslíka vo svaloch (odpovede c, f, g, h). "
        "Kvasinky pivné realizujú alkoholové kvasenie s tvorbou etanolu a CO2, kým v ľudských svaloch prebieha mliečne kvasenie s tvorbou kyseliny mliečnej. "
        "Kvasenie prebieha bez účasti molekulárneho kyslíka (ktorý ho tlmí) a nekončí oxidáciou na H2O a CO2 ani pyruvátom (a, b, d, e)."
    ),
    229: (
        "Oxidačná dekarboxylácia pyruvátu je spojovací metabolický stupeň medzi cytoplazmatickou glykolýzou a Krebsovým cyklom, lokalizovaný v matrix mitochondrií (odpovede b, d, e). "
        "Enzýmovým komplexom sa z pyruvátu odštiepi CO2, redukuje sa NAD+ na NADH a vzniká aktivovaná dvojuhlíkatá skupina viazaná na koenzým A – acetyl-CoA, ktorý vstupuje do citrátového cyklu. "
        "Prvou fázou dýchania je glykolýza a táto reakcia sama o sebe priamo neprodukuje 30 molekúl ATP (a, c, f, g, h)."
    ),
    230: (
        "Energia viazaná v asimilátoch (sacharidoch) sa v rastlinných bunkách uvoľňuje disimilačnými procesmi: štiepením uhlíkového skeletu glukózy pri glykolýze, biologickými oxidáciami v Krebsovom cykle a oxidačnou fosforyláciou v dýchacom reťazci (odpovede a, c, d, e, f). "
        "Týmito katabolickými reakciami sa energia chemických väzieb premieňa na univerzálnu formu energie v ATP. "
        "Fotosyntéza a fotofosforylácia energiu do asimilátov ukladajú a glukoneogenéza je energeticky náročná syntéza glukózy (b, g, h)."
    ),
    231: (
        "Izogamia je forma pohlavného rozmnožovania, pri ktorej splývajú dve haploidné gaméty rovnakého tvaru, veľkosti a pohyblivosti (morfologicky nerozlíšiteľné), líšiace sa však fyziologicky a pohlavným typom (+ a -; odpovede b, e, g). "
        "Vznikajúca zygota je diploidná a geneticky unikátna, gaméty teda nie sú identické. "
        "Diferenciácia na makrogaméty a mikrogaméty sa uplatňuje pri anizogamii, nie izogamii (a, c, d, f, h)."
    ),
    232: (
        "Anizogamia (heterogamia) je typ pohlavného rozmnožovania, pri ktorom dochádza k fúzii dvoch haploidných gamét výrazne sa líšiacich veľkosťou, morfológiou, pohyblivosťou (veľká nepohyblivá makrogaméta a menšia pohyblivá mikrogaméta) aj geneticky a fyziologicky (odpovede a, c, e, f, g, h). "
        "Obe gaméty reprezentujú odlišné pohlavné typy, čím sa zabezpečuje genetická variabilita potomstva. "
        "Pohlavné bunky nikdy nie sú geneticky identické a nemôžu pochádzať z rovnakého pohlavného typu (b, d)."
    ),
    233: (
        "Rodozmena (metagenéza) predstavuje biologický životný cyklus vyšších rastlín a niektorých rias, pri ktorom dochádza k pravidelnému striedaniu pohlavnej generácie (haploidného gametofytu) a nepohlavnej generácie (diploidného sporofytu; odpovede b, c, e). "
        "Gametofyt tvorí gaméty mitózou a po oplodnení vyrastá sporofyt tvoriaci meiózou výtrusy. "
        "Gametogenéza je tvorba gamét, mutagenéza je vznik mutácií a partenogenéza vývin neoplodneného vajíčka (a, d, f, g, h)."
    ),
    234: (
        "Gametofyt machorastov tvorí dominantnú zelenú, fotosyntetizujúcu časť rastliny (stielku alebo príchytné vlákna, pabyľku a palístky), ktorá je haploidná (1n; odpovede a, e, h). "
        "Vzniká mitotickým delením z jednobunkového haploidného výtrusu (spóry) cez štádium prvoklíka (protonémy). "
        "Gametofyt netvorí cievnatý kormus ani výtrusnice (tie nesie diploidný sporofyt vznikajúci mitózami zygoty; b, c, d, f, g)."
    ),
    235: (
        "Nepohlavné (asexuálne) rozmnožovanie rastlín je vývojovo starší reprodukčný spôsob, pri ktorom nový jedinec vzniká mitózami priamo zo somatických buniek materského tela (vegetatívne rozmnožovanie) alebo výtrusmi (sporogenéza u výtrusných rastlín; odpovede a, b, d, f, g). "
        "Potomstvo je geneticky zhodné s rodičom (klon). "
        "Pohlavné rozmnožovanie zahŕňa fúziu gamét a gametogónia je tvorba pohlavných buniek, nie asexuálny proces (c, e, h)."
    ),
    236: (
        "Výtrusy (spóry) machorastov a papraďorastov sú haploidné nepohlavné rozmnožovacie častice, ktoré vznikajú redukčným delením (meiózou) v sporangiách sporofytu (odpovede c, e, f, g, h). "
        "U suchozemských rastlín sú nepohyblivé a prispôsobené na šírenie vetrom (anemochória). "
        "Nejde o pohlavné bunky (tými sú gaméty) a nevznikajú mitózou materských buniek (a, b, d)."
    ),
    237: (
        "Sporofyt machorastov (štet s tobolkou) predstavuje nepohlavnú generáciu, ktorej bunky sú diploidné (2n; odpovede a, c, d, h). "
        "Keďže takmer alebo vôbec neobsahuje asimilačné pletivá, nie je schopný samostatnej fotosyntézy a vyživuje sa paraziticky na materskom zelenom gametofyte. "
        "Prvoklík je počiatočným štádiom gametofytu a rodozmena ako celok je heteromorfná (b, e, f, g)."
    ),
    238: (
        "Rôznotvará (heteromorfná) rodozmena znamená, že gametofyt (pohlavná generácia) a sporofyt (nepohlavná generácia) sa od seba výrazne líšia vzhľadom, morfológiou, veľkosťou aj dĺžkou života (odpovede b, d, e). "
        "Tento typ rodozmeny je charakteristický pre všetky vyššie rastliny (kormofyty). "
        "Izomorfná (rovnotvará) rodozmena, kde sú obe generácie vzhľadovo totožné, sa vyskytuje len pri niektorých riasach (a, c, f, g, h)."
    ),
    239: (
        "Redukčné delenie (meióza) prebieha počas rodozmeny výhradne v diploidnej nepohlavnej generácii – v sporofyte, konkrétne v jeho výtrusniciach (sporangiách; odpovede c, d). "
        "Z diploidných materských buniek výtrusov (2n) tu vznikajú haploidné výtrusy (spóry, 1n). "
        "V gametofyte sú všetky bunky haploidné, preto v ňom meióza nemôže prebiehať a gaméty vznikajú mitózou (a, b, e, f, g, h)."
    ),
    240: (
        "V životnom cykle semenných rastlín nastáva úplná dominancia diploidného sporofytu, ktorý tvorí celú vlastnú autotrofnú rastlinu (koreň, stonku, listy, kvety) a zabezpečuje výživu (odpovede a, c, e, f). "
        "Haploidný gametofyt je silne redukovaný a vyvíja sa ako mikroskopická integrálna súčasť sporofytu (peľové zrnko a zárodočný miešok). "
        "Prevaha gametofytu a jeho vyživovacia úloha voči sporofytu sa zachovala výhradne u machorastov (b, d, g, h)."
    ),
    241: (
        "Gaméty u machorastov vznikajú v haploidnej pohlavnej generácii, ktorú predstavuje gametofyt (samotná zelená rastlinka; odpovede a, c, e). "
        "Tvoria sa v mnohobunkových pohlavných orgánoch – gametangiách (plemenníčkach – anterídiách a zárodočníkoch – archegóniách) mitotickým delením. "
        "Sporofyt je nepohlavná diploidná generácia, v ktorej výtrusnici vznikajú meiózou spóry, nie gaméty (b, d, f, g, h)."
    ),
    242: (
        "Gametofyt machorastov sa od sporofytu líši morfologicky (zelená listnatá rastlinka verzus nezelený štet s tobolkou) a cytologicky ploidiou, pretože gametofyt je haploidný (1n) a sporofyt diploidný (2n; odpovede a, b, d, g). "
        "Gametofyt nesie pohlavné orgány (gametangiá) a má vyvinutý funkčný fotosyntetický aparát (stroma chloroplastov), zatiaľ čo sporofyt nesie výtrusnicu. "
        "Tvrdenie c má obrátenú ploidiu a možnosť h priraďuje štruktúry opačne (c, e, f, h)."
    ),
    243: (
        "Výdaj vody rastlinou sa realizuje dvoma spôsobmi: vyparovaním plynnej vody cez prieduchy alebo cez kutikulu (transpirácia – stomatárna a kutikulárna, prebiehajúca prevažne cez deň) a výdajom kvapalnej vody cez hydatódy (gutácia, prebiehajúca prevažne v noci a nad ránom pri vysokom koreňovom výtlaku; odpovede b, d, g, h). "
        "Transpirácia v noci ustáva, pretože prieduchy sa zatvárajú. "
        "Kohézne sily slúžia na súdržnosť vodného stĺpca v xyléme a pojem prieduchový výtlak neexistuje (a, c, e, f)."
    ),
    244: (
        "Na pasívnom aj aktívnom diaľkovom transporte vody drevnou časťou cievnych zväzkov (xylémom) sa podieľa sacia sila transpirácie listov, koreňový výtlak a fyzikálne vlastnosti vody – adhézia (priľnavosť k stenám ciev), kohézia (súdržnosť molekúl vody) a kapilarita (odpovede a, b, c, d, e). "
        "Vďaka kohézii a adhézii sa v tracheách a tracheidách nevytvoria vzduchové bubliny (kavitácia). "
        "Gutácia je dôsledok výdaja vody na listoch, nie transportná sila v cievach, a vlastnosti pôdy sú vonkajšími faktormi príjmu (f, g, h)."
    ),
    245: (
        "Auxíny patria medzi najstaršie známe fytohormóny (rastové regulátory), ktoré v rastline koordinujú morfogenézu, predlžovací rast buniek a apikálnu dominanciu (odpovede b, d, e, f, g, h). "
        "Syntetizujú sa najmä v rastových vrcholoch a meristémoch a v praxi sa uplatňujú pri stimulácii zakoreňovania odrezkov a tvorbe bočných koreňov. "
        "Prirodzené auxíny sú telu vlastné stimulátory, nie chemické jedy, hoci ich syntetické deriváty vo vysokých koncentráciách slúžia ako herbicídy (a, c)."
    ),
    246: (
        "Medzi základné stimulačné rastové hormóny (stimulátory rastu) patria auxíny, giberelíny a cytokiníny (odpovede d, f, g). "
        "Tieto fytohormóny podporujú delenie a elongáciu buniek, diferenciáciu pletív, zakoreňovanie a klíčenie semien. "
        "Kyselina abscisová (ABA) a etylén sú naopak rastové inhibítory (navodzujú dormanciu, starnutie a opad listov) a kyselina oxaloctová je medziprodukt Krebsovho cyklu (a, b, c, e, h)."
    ),
    247: (
        "Životný cyklus rastliny zahŕňa celý ontogenetický vývinový sled druhu od vzniku reprodukčného útvaru po vznik rovnakej novej diaspóry – pri semenných rastlinách od semena po semeno a pri výtrusných od výtrusu po výtrus (odpovede c, d, f, g). "
        "Typické striedanie fáz a dominancia určitej generácie v životnom cykle predstavuje charakteristický znak dosiahnutej fylogenetickej úrovne danej rastlinnej línie. "
        "Život jednotlivca od zrodu po smrť je ontogenéza a evolučný vývoj celého druhu je fylogenéza (a, b, e, h)."
    ),
    248: (
        "Ekologické sucho nastáva pri fyzickom deficite dostupnej kvapalnej vody v prostredí, napríklad v zime pri mrazoch, kedy voda zamrzne (c). "
        "Fyziologické sucho znamená, že voda v prostredí je, no rastlina ju nedokáže koreňmi prijať (napr. v chladných, ílovitých, premokrených či kyslých pôdach; d). "
        "Príjem vody koreňmi je aktívny metabolický proces závislý od prítomnosti O2 v pôde pre dýchanie buniek (f), a plytké kyprenie pôdy bráni odparovaniu prerušením pôdnych kapilár („suché zalievanie“; e). "
        "Vyšší osmotický tlak pôdy príjem vody naopak blokuje a bunka s plným turgorom nie je špongiová (g, h)."
    ),
    249: (
        "Transpiračný koeficient je fyziologický ukazovateľ vyjadrujúci množstvo vody v litroch (alebo gramoch), ktoré rastlina spotrebuje a odparí počas vegetačného obdobia na vytvorenie 1 kg (alebo gramu) sušiny (odpovede d, e, f). "
        "Používa sa na hodnotenie hospodárenia rastliny s vodou, produkcie biomasy a stanovenie nárokov poľnohospodárskych plodín na vlahu. "
        "Množstvo vody odparené za jednotku času vyjadruje intenzita transpirácie (a, b, c, g, h)."
    ),
    250: (
        "Respiračný kvocient (RQ) je bezrozmerný pomer objemu vyprodukovaného oxidu uhličitého k objemu spotrebovaného kyslíka pri bunkovom dýchaní (RQ = V(CO2) / V(O2); odpovede a, d, f). "
        "Vyjadruje intenzitu dýchania a charakter oxidovaného substrátu: pri úplnej oxidácii glukózy je RQ = 1,0 (pretože na 6 molekúl O2 pripadá 6 molekúl CO2), pri tukoch je to približne 0,7 a pri proteínoch 0,8. "
        "Netýka sa fotosyntézy, glykolýzy ani pomeru plynov v pľúcach (b, c, e, g, h)."
    ),
}

with open('scripts/bio_batches/batch_5.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions.")

for i, q in enumerate(questions):
    q_num = 201 + i
    if q_num not in explanations:
        raise ValueError(f"Missing explanation for question {q_num}")
    q['explanation'] = explanations[q_num]

output_path = 'scripts/bio_batches/batch_5_explained.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Saved {len(questions)} questions to {output_path}.")
