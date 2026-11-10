# -*- coding: utf-8 -*-
import json

explanations = {
    401: (
        "V IV.A podskupine (14. skupina) stúpa s rastúcim protónovým číslom kovový charakter od nekovového uhlíka cez polokovy Si, Ge až po typické kovy Sn a Pb (odpoveď b). "
        "Uhlík nemá vo valenčnej vrstve d-orbitály, preto je schopný tvoriť maximálne 4 kovalentné väzby, zatiaľ čo ťažšie prvky môžu využitím d-orbitálov prekročiť oktet (odpoveď c). "
        "V oxidačnom stave +IV prevažuje kovalentný charakter väzieb vďaka vysokej hustote kladného náboja (odpoveď d) a všetky tieto prvky môžu vystupovať aj v oxidačnom stave +II, ktorého stálosť smerom k olovu stúpa v dôsledku efektu inertného elektrónového páru (odpoveď f). "
        "Cín Sn už patrí medzi kovy a elektronegativita v skupine neklesá rovnomerne (a, e, g, h)."
    ),
    402: (
        "Prvky V.A podskupiny (p3 prvky) majú 5 valenčných elektrónov (ns2 np3), takže prijatím troch elektrónov alebo vytvorením troch kovalentných väzieb môžu dosiahnuť stabilnú konfiguráciu nasledujúceho vzácneho plynu (odpoveď a). "
        "So stúpajúcim protónovým číslom klesá nekovový charakter (od N po Bi) a stúpa charakter kovový (odpoveď b). "
        "V dôsledku efektu inertného s-elektrónového páru klesá stabilita zlúčenín s oxidačným číslom +V (odpoveď f) a kyslý charakter oxidov prechádza od silne kyslých cez amfotérne až k zásaditému Bi2O3 (odpoveď g). "
        "Tieto prvky nie sú všetky polokovy a nie sú limitované len štvorväzbovosťou (c, d, e, h)."
    ),
    403: (
        "Prvky VIII.A podskupiny (18. skupina) sú nekovové vzácne plyny s plne obsadenou valenčnou vrstvou s2p6 (hélium 1s2), čo im dodáva mimoriadnu chemickú stálosť (odpovede a, d). "
        "Vďaka tejto stabilite a nízkej reaktivite netvoria viacatómové molekuly, ale vyskytujú sa ako jednoatómové plyny (odpoveď c). "
        "V zemskej atmosfére tvoria približne 1 objemové percento, pričom zďaleka najhojnejším z nich je argón s podielom cca 0,93 % (odpoveď g; možnosti e, f, h sú nesprávne)."
    ),
    404: (
        "S rastúcim protónovým číslom alkalických kovov (I.A) sa zväčšuje atómový polomer a klesá ionizačná energia, preto atómy ľahšie odovzdávajú svoj valenčný elektrón, čo vedie k rastu reaktivity a redukčných účinkov (odpovede d, e). "
        "Zväčšujúci sa polomer katiónov znižuje ich polarizačný účinok na hydroxidovú skupinu, čím rastie disociácia vo vode a zásaditosť ich hydroxidov (odpoveď a). "
        "Hustota alkalických kovov so stúpajúcim Z v skupine vo všeobecnosti rastie (odpoveď g), zatiaľ čo ich elektronegativita klesá a kyseliny netvoria (b, c, f, h)."
    ),
    405: (
        "V podskupine halogénov (VII.A) so zväčšujúcim sa protónovým číslom klesá oxidačná schopnosť elementárnych prvkov a naopak rastie redukčný účinok halogenidových aniónov (I- je najsilnejšie redukovadlo; odpoveď a). "
        "S rastom atómového polomeru klesá acidobázická sila a kyslý charakter ich oxidov (odpoveď b). "
        "Vplyvom silnejúcich medzimolekulových disperzných síl stúpa teplota topenia a varu, mení sa skupenstvo od plynov (F2, Cl2) cez kvapalinu (Br2) po pevnú látku (I2; odpoveď g) a zároveň sa prehlbuje sfarbenie od svetložltého po fialovočierny (odpoveď e; c, d, f, h sú nesprávne)."
    ),
    406: (
        "Podskupinu I.B (11. skupina) tvoria prechodné d-prvky meď (Cu), striebro (Ag) a zlato (Au), ktoré majú valenčnú konfiguráciu (n-1)d10 ns1 s plne zaplnenou stabilnou d-podslupkou (odpovede a, f, g). "
        "V Beketovom rade napätia kovov ležia napravo od vodíka (majú kladný štandardný elektródový potenciál E° > 0), patria medzi ušľachtilé kovy a pre svoju nízku reaktivitu sa v prírode vyskytujú aj v rýdzej elementárnej forme (odpoveď e). "
        "Netvoria štvormocné katióny a sú neporovnateľne menej reaktívne než alkalické kovy (b, c, d, h)."
    ),
    407: (
        "Prvky II.B podskupiny (Zn, Cd, Hg) majú v tej istej perióde oproti prvkom II.A vyššie protónové číslo, a teda väčší náboj jadra (odpoveď d), a ich valenčná sféra obsahuje plne zaplnené d-orbitály (n-1)d10 ns2 (odpoveď f). "
        "V dôsledku horšieho tienenia jadra d-elektrónmi dochádza ku kontrakcii elektrónového obalu, takže majú menšie atómové polomery (odpoveď h). "
        "Majú tiež podstatne slabšiu kovovú väzbu a nižšie teploty topenia než kovy alkalických zemín, pričom ortuť je za normálnych podmienok dokonca kvapalná (odpoveď g; možnosti a, b, c, e neplatia)."
    ),
    408: (
        "Vodík existuje v troch izotopoch: prócium (1H), deutérium (2H) a rádioaktívne trícium (3H; odpoveď a). "
        "Vo väčšine reakcií vystupuje ako redukčné činidlo (odpoveď c) a s prechodnými kovmi tvorí intersticiálne kovové hydridy (odpoveď d). "
        "Spolu s uhlíkom, kyslíkom a dusíkom predstavuje základný makrobiogénny prvok živých organizmov (odpoveď f). "
        "S alkalickými kovmi tvorí iónové hydridy s aniónom H- (nie kovalentné) a pri stužovaní tukov sa aduje, nie uvoľňuje (b, e, g, h)."
    ),
    409: (
        "Pre alkalické kovy neplatia tvrdenia a, c, d, e: v skutočnosti sú mimoriadne reaktívne vďaka nízkej ionizačnej energii, v rámci periódy majú najväčšie atómové polomery, ich hustota vo všeobecnosti stúpa a s vodou reagujú explozívne, preto sa uchovávajú pod petrolejom. "
        "Tvrdenia b, f, g, h naopak platia, keďže alkalické kovy sú silnými redukovadlami, dobrými vodičmi a ich teploty topenia so stúpajúcim Z klesajú."
    ),
    410: (
        "Hydroxid sodný (NaOH) je biela hygroskopická látka, ktorá pohlcuje vzdušnú vlhkosť aj oxid uhličitý za vzniku uhličitanu sodného (odpoveď b). "
        "Vo vode sa rozpúšťa mimoriadne dobre za silného uvoľňovania tepla (odpoveď a) a reaguje s oxidom kremičitým v skle, čím dochádza k jeho pomalému leptaniu (odpoveď c). "
        "V laboratóriu ho možno demonštrovať reakciou kovového sodíka s vodou za vzniku NaOH a vodíka (odpoveď d). "
        "Priemyselne sa vyrába elektrolýzou soľanky (NaCl), nie zo síranu sodného (e, f, g, h neplatia)."
    ),
    411: (
        "Sóda (kalcinovaná sóda) je uhličitan sodný so vzorcom Na2CO3 (odpoveď b). "
        "Priemyselne sa vyrába Solvayovým spôsobom založeným na reakcii roztoku NaCl, amoniaku a oxidu uhličitého s následnou kalcináciou vzniknutého NaHCO3 (odpoveď c). "
        "Vo veľkom meradle sa využíva v sklárskom priemysle ako tavivo pri výrobe skla (odpoveď f). "
        "Ako soľ silnej zásady a slabej kyseliny vo vode hydrolyzuje zásadito v dôsledku reakcie CO3(2-) + H2O <=> HCO3(-) + OH(-) (odpoveď h; a, d, e, g sú nesprávne)."
    ),
    412: (
        "Jedlá sóda je hydrogénuhličitan sodný so vzorcom NaHCO3 (odpoveď a), ktorý vzniká ako kľúčový medziprodukt pri Solvayovom procese výroby sódy (odpoveď c). "
        "V medicíne sa používa ako antacidum na neutralizáciu nadbytočnej HCl v žalúdočnej šťave (odpoveď e) a v kuchyni ako kypriaci prášok do pečiva, keďže sa teplom rozkladá za uvoľňovania CO2 (odpoveď f). "
        "Na2CO3 je kalcinovaná sóda a roztok NaHCO3 vykazuje mierne zásadité pH (b, d, g, h sú nepravdivé)."
    ),
    413: (
        "Kovový sodík je mäkký alkalický kov s nízkou hustotou a slabou kovovou väzbou, vďaka čomu sa dá ľahko krájať nožom (odpoveď b). "
        "S vodou reaguje spontánne a búrlivo za vzniku hydroxidu sodného a uvoľnenia vodíka (odpoveď c). "
        "Katión Na+ je hlavným osmoticky aktívnym extracelulárnym katiónom organizmu (odpoveď d) a jeho emisia v plameni spôsobuje charakteristické intenzívne žlté sfarbenie (odpoveď e). "
        "Katión K+ je prevažne intracelulárny a potaš je uhličitan draselný (a, f, h neplatia)."
    ),
    414: (
        "Horčík (Mg) je kľúčový biogénny prvok viazaný ako centrálny ión v porfyrínovom kruhu chlorofylu (odpoveď b). "
        "V ľudskom tele predstavuje po draslíku druhý najdôležitejší intracelulárny katión, nevyhnutný pre aktivitu stoviek enzýmov spojených s ATP (odpoveď c). "
        "V litosfére sa vo veľkých množstvách vyskytuje v mineráloch magnezit (MgCO3) a dolomit (CaMg(CO3)2; odpovede f, g). "
        "Vitamín B12 obsahuje kobalt a malachit je minerál medi (a, d, e, h sú nesprávne)."
    ),
    415: (
        "Vápnik je najvýznamnejší biogénny makroprvok v tele stavovcov, ktorý tvorí anorganickú minerálnu zložku kostí a zubov vo forme hydroxyapatitu (odpoveď a). "
        "Vo fyziológii zohráva nezastupiteľnú úlohu ako signálny spúšťač svalovej kontrakcie a kofaktor zrážania krvi (odpoveď e). "
        "Ako reaktívny kov alkalických zemín rozkladá vodu už za laboratórnej teploty za vývoja vodíka a vzniku Ca(OH)2 (odpoveď g) a za bežných podmienok na vzduchu samovoľne nehorí (odpoveď c). "
        "Ca2+ je typicky extracelulárny ión, ktorého koncentrácia v cytozole je udržiavaná na veľmi nízkej úrovni (b, d, f, h neplatia)."
    ),
    416: (
        "Sadra je hemihydrát síranu vápenatého so vzorcom CaSO4 . 0,5 H2O (odpovede d, e). "
        "Pripravuje sa zo sadrovca (CaSO4 . 2 H2O) jeho termickým odvodnením (pražením) pri teplote 120–150 °C (odpoveď f). "
        "Po zmiešaní s vodou spätne hydratuje na dihydrát sadrovec, pričom rýchlo tuhne s miernym nárastom objemu, čo sa široko využíva v zdravotníctve na fixáciu fraktúr a v stomatológii (odpoveď c; a, b, g, h sú nesprávne)."
    ),
    417: (
        "Oxid hlinitý (Al2O3) vzniká prudkou syntézou z prvkov pri vysokých teplotách (odpoveď a), ale na vzduchu sa tvorí aj pri izbovej teplote v podobe jemnej vrstvičky, ktorá hliník pasivuje (odpoveď b). "
        "V prírode tvorí minerál korund, ktorý s tvrdosťou 9 na Mohsovej stupnici patrí medzi najtvrdšie nerasty (odpoveď d). "
        "Vďaka vysokému mernému povrchu a adsorpčnej schopnosti sa aktívny Al2O3 používa ako stacionárna fáza v chromatografii (odpoveď f). "
        "Al2O3 je nerozpustný vo vode a je amfotérny, takže sa rozpúšťa v kyselinách aj v zásadách (c, e, g, h sú nesprávne)."
    ),
    418: (
        "Hliník sa priemyselne vyrába Hallovým-Héroultovým procesom – energeticky náročnou elektrolýzou taveniny bauxitu v kryolite Na3[AlF6] (odpoveď a). "
        "Ľahko tvorí podvojné sírany, tzv. kamence typu KAl(SO4)2 . 12 H2O (odpoveď d), vykazuje amfotérne vlastnosti reakciou s kyselinami aj hydroxidmi a pasivuje sa ochrannou vrstvou oxidu (v kľúči správne a, d, f, g). "
        "Hliník nie je biogénnym prvkom a v prírode sa pre vysokú reaktivitu voľný nevyskytuje (b, e, h neplatia)."
    ),
    419: (
        "Uhlík je základným makrobiogénnym prvkom, ktorého atómy tvoria stabilné kovalentné väzby C-C a umožňujú reťazenie do lineárnych, rozvetvených aj cyklických organických štruktúr (odpovede a, d). "
        "Jeho alotropická modifikácia diamant je vďaka trojrozmernej priestorovej sp3 sieti najtvrdším prírodným nerastom (odpoveď e). "
        "V medicíne sa aktívne (živočíšne) uhlie využíva ako účinné adsorbens na naviazanie toxínov v gastrointestinálnom trakte (odpoveď h). "
        "Diamant je elektrický izolant a elementárny uhlík sa v prírode voľne vyskytuje (b, c, f neplatia)."
    ),
    420: (
        "Oxid uhličitý (CO2) vzniká termickým rozkladom (pálením) vápenca CaCO3 na CaO a CO2 (odpoveď b), dokonalým spaľovaním uhlia a uhlíka (odpoveď c) a oxidáciou oxidu uhoľnatého 2 CO + O2 -> 2 CO2 (odpoveď g). "
        "Uvoľňuje sa tiež ako prirodzený vedľajší produkt alkoholového aj bunkového kvasenia glukózy (odpoveď e). "
        "CO2 je ťažší ako vzduch (M = 44 g/mol vs 29 g/mol) a nie je prudkým jedom, hoci vo vysokých koncentráciách pôsobí dusivo (a, d, f, h sú nepravdivé)."
    ),
    421: (
        "Oxid uhoľnatý (CO) je bezfarebný plyn bez chuti a zápachu, ktorý vzniká pri nedokonalom spaľovaní uhlíkatých palív pri deficite kyslíka (odpovede b, f). "
        "Tvorí sa tiež reakciou uhlíka s oxidom uhličitým za vysokej teploty podľa Boudouardovej rovnováhy C + CO2 <=> 2 CO (odpoveď h). "
        "Pre človeka je vysoko toxický, pretože sa s mimoriadne vysokou afinitou viaže na hémové železo hemoglobínu za vzniku karboxyhemoglobínu a znemožňuje transport kyslíka (odpoveď g; a, c, d, e neplatia)."
    ),
    422: (
        "Oxid uhoľnatý (CO) je prudký jed blokujúci transport kyslíka a bunkové dýchanie (odpoveď a), kyanid draselný (KCN) okamžite zastavuje bunkové dýchanie inhibíciou cytochróm c oxidázy (odpoveď b). "
        "Sírouhlík (CS2) pôsobí ako silný neurotoxický a cievny jed (odpoveď d) a amoniak (NH3) je toxický odpadový metabolit dráždiaci dýchacie cesty a poškodzujúci mozog (odpoveď g). "
        "Látky H2CO3, NaHCO3 a CO2 tvoria fyziologický bikarbonátový tlmivý systém krvi a N2 je inertný atmosférický plyn (c, e, f, h nepatria medzi jedy)."
    ),
    423: (
        "Kyselina kyanovodíková (vodný roztok plynného kyanovodíka HCN) je veľmi slabá jednosýtna kyselina, ktorá je vo vode výborne rozpustná a miešateľná vo všetkých pomeroch (odpoveď b). "
        "Patrí medzi extrémne prudké jedy, pretože uvoľnený anión CN- ireverzibilne inhibuje cytochróm c oxidázu v dýchacom reťazci mitochondrií (odpoveď c; v kľúči správne b, c, f, g). "
        "Kyanovodík je prchavá kvapalina s teplotou varu okolo 26 °C a vôňou horkých mandlí, nie pevná látka (a, e, h sú nesprávne)."
    ),
    424: (
        "Kremík kryštalizuje v kubickej diamantovej štruktúre, vďaka čomu je veľmi tvrdý, ale krehký (odpoveď d). "
        "Priemyselne sa vyrába redukciou oxidu kremičitého uhlíkom v elektrickej oblúkovej peci: SiO2 + 2 C -> Si + 2 CO (odpoveď e). "
        "Pre svoje polovodičové vlastnosti je základnou surovinou mikroelektroniky (odpoveď f) a jeho nerasty (kremenný piesok) sa využívajú pri výrobe skla (odpoveď g). "
        "Elementárny kremík sa v prírode voľný nenachádza a najrozšírenejším prvkom v zemskej kôre je kyslík (a, b, c, h neplatia)."
    ),
    425: (
        "Dusík nemá vo valenčnej vrstve d-orbitály, preto môže vytvoriť maximálne 4 kovalentné väzby (napr. v amónnom katióne NH4+; odpoveď b). "
        "Dvojatómová molekula N2 obsahuje mimoriadne pevnú trojitú väzbu (:N≡N:), čo spôsobuje jej nízku reaktivitu a vysokú chemickú inertnosť pri bežnej teplote (odpoveď d), v dôsledku čoho reaguje s väčšinou látok až pri zahriatí (odpoveď h). "
        "S molárnou hmotnosťou 28 g/mol je o niečo ľahší ako vzduch (M ≈ 29 g/mol; odpoveď e; a, c, f, g neplatia)."
    ),
    426: (
        "Amoniak (NH3) je bezfarebný štipľavý plyn (odpoveď e), ktorý má na atóme dusíka v hybridizácii sp3 jeden voľný elektrónový pár (odpoveď c). "
        "Vďaka tomuto páru vystupuje v koordinačných zlúčeninách ako Lewisova báza – donor elektrónov (amminový ligand; odpoveď g). "
        "Vo vode sa vynikajúco rozpúšťa tvorbou vodíkových väzieb a disociuje ako slabá zásada za vzniku iónov NH4+ a OH- (odpoveď d). "
        "Amoniak je polárna molekula s dipólovým momentom tvoriaca katión NH4+, nie NH3+ (a, b, f, h sú nesprávne)."
    ),
    427: (
        "Oxid dusný (N2O, rajský plyn) je bezfarebný plyn so sladkastou chuťou a vôňou, ktorý sa pre inertnosť a rozpustnosť v tukoch používa v šľahačkových sprejoch (odpovede a, g). "
        "Oxid dusičitý (NO2) je naopak hnedočervený, agresívny a prudko toxický plyn spôsobujúci pľúcny edém (odpoveď e; v kľúči správne a, c, e, g). "
        "Oxidy dusíka patria medzi hlavné zložky fotochemického smogu a kyslých zrážok, a preto výrazne znečisťujú životné prostredie (b, f, h neplatia)."
    ),
    428: (
        "Kyselina dusičná (HNO3) je silná jednosýtna kyselina, ktorá vo vodnom roztoku plne disociuje na H+ a NO3- (odpoveď f). "
        "S vodou tvorí azeotropnú zmes s maximom varu pri koncentrácii približne 68 % HNO3 (odpoveď d). "
        "Pôsobí ako silné oxidačné činidlo, ktoré oxiduje väčšinu kovov (okrem Au a Pt) a organické látky, pričom sa redukuje na oxidy dusíka (odpoveď h; v kľúči správne b, d, f, h). "
        "Priemyselne sa vyrába Ostwaldovým procesom oxidácie amoniaku a je výrazne silnejšia než HNO2 (a, e, g sú nesprávne)."
    ),
    429: (
        "Fosfor sa v prírode vyskytuje výhradne v mineráloch obsahujúcich fosforečnany, napríklad v apatite a fosforite (odpoveď e). "
        "Jeho modifikácie majú odlišné vlastnosti: biely fosfor (P4) je prudko toxický a na vzduchu samozápalný (odpoveď f), červený fosfor je netoxický polymér tvorený reťazcami fosforových atómov (odpoveď h) a čierny fosfor vykazuje polokovové vlastnosti s elektrickou vodivosťou (odpoveď c). "
        "Všetky modifikácie nie sú toxické a voľný fosfor v prírode neexistuje (a, b, d, g sú nesprávne)."
    ),
    430: (
        "Oxid fosforečný vzniká dokonalým spaľovaním elementárneho fosforu v nadbytku kyslíka (odpoveď h) a existuje v dimérnej forme tetraméru P4O10 (odpoveď a). "
        "Je to biela kryštalická látka s mimoriadne silnými hygroskopickými vlastnosťami, ktorá ochotne a prudko reaguje s vodou, a preto slúži ako jedno z najúčinnejších laboratórnych sušidiel (odpoveď b). "
        "Nie je červený a pri nedokonalom horení vzniká oxid fosforitý P4O6 (c, d, e, f, g neplatia)."
    ),
    431: (
        "Kyselina trihydrogenfosforečná (H3PO4) je v bezvodom stave bezfarebná kryštalická látka (odpoveď a). "
        "Predstavuje veľmi stálu, neoxidačnú stredne silnú trojsýtnu kyselinu (odpoveď e), ktorá postupnou disociáciou vytvára tri rady solí – dihydrogénfosforečnany, hydrogénfosforečnany a fosforečnany (odpoveď h). "
        "Zahrievaním dochádza k jej kondenzácii na polyfosforečné kyseliny (odpoveď g) a pri zvýšenej teplote reaguje s väčšinou kovov (odpoveď f). "
        "Nemá oxidačné vlastnosti porovnateľné s HNO3 (b, c, d sú nepravdivé)."
    ),
    432: (
        "Kyslík je druhým najelektronegatívnejším prvkom periodickej tabuľky, preto v drvivej väčšine reakcií vystupuje ako silné oxidovadlo a sám sa redukuje na oxidačné číslo -II (odpovede a, d). "
        "Vo vode sa čiastočne rozpúšťa, čo zabezpečuje dýchanie vodných organizmov (odpoveď e). "
        "V laboratóriu ho možno pripraviť termickým rozkladom kyslíkatých solí, napríklad manganistanu alebo chloristanu draselného (odpoveď h). "
        "Kyslík je veľmi reaktívny a jeho najvyššie oxidačné číslo je +II v OF2 (b, c, f, g sú nesprávne)."
    ),
    433: (
        "Ozón (O3) je alotropická modifikácia kyslíka s mimoriadne silnými oxidačnými účinkami prevyšujúcimi molekulový O2 (odpoveď b). "
        "V prírode vzniká v atmosfére pri elektrických výbojoch bleskov počas búrok (odpoveď c) a ľahko sa rozpadá za uvoľnenia vysoko reaktívneho atomárneho kyslíka (odpoveď e). "
        "Pre svoje baktericídne a virocídne schopnosti sa využíva pri sterilizácii a dezinfekcii vody a vzduchu (odpoveď g). "
        "Ozón nevystupuje ako redukovadlo a sám sa ľahko redukuje (a, d, f, h neplatia)."
    ),
    434: (
        "O síre neplatia tvrdenia a, d, g, h: síra nepatrí medzi halogény (je chalkogén 16. skupiny), predstavuje biogénny makroprvok (súčasť aminokyselín cysteínu a metionínu), má konfiguráciu [Ne] 3s2 3p4 a ide o nekov, nie kov. "
        "Tvrdenia b, c, e, f sú pravdivé, keďže síra tvorí kryštalické alotropické modifikácie (kosoštvorcovú a jednoklonnú), vo vode je nerozpustná a pri zahrievaní jej tavenina tmavne v dôsledku otvárania kruhov S8 na dlhé polymérne reťazce."
    ),
    435: (
        "Sulfán (H2S) je prudko jedovatý plyn s typickým zápachom po skazených vajciach, ktorý blokuje bunkové dýchanie inhibíciou cytochróm c oxidázy (odpovede g, h). "
        "Vo vode sa rozpúšťa za vzniku slabej dvojsýtnej kyseliny sulfánovej (odpoveď b) a pri nedostatku vzduchu zhorí nedokonalým spaľovaním na elementárnu síru a vodu: 2 H2S + O2 -> 2 S + 2 H2O (odpoveď d). "
        "Síra je v sulfáne v minimálnom oxidačnom čísle -II, preto má výlučne redukčné vlastnosti a nemôže pôsobiť ako oxidovadlo (a, c, e, f sú nesprávne)."
    ),
    436: (
        "Bezvodá kyselina sírová je bezfarebná olejovitá kvapalina (odpoveď c). "
        "V koncentrovanom stave má mimoriadne silné hygroskopické účinky, ktorými odníma vodu aj organickým zlúčeninám (odpoveď d), a dymivá kyselina sírová obsahujúca rozpustený SO3 sa nazýva oleum (odpoveď e). "
        "Zriedená kyselina sírová oxiduje výhradne katiónmi H+, preto reaguje iba s neušľachtilými kovmi za vývoja plynného vodíka (odpoveď f). "
        "Koncentrovaná kyselina pasivuje železo a pri jej riedení sa zásadne pridáva kyselina do vody (a, b, g, h neplatia)."
    ),
    437: (
        "Fluór je svetložltý, mimoriadne reaktívny a prudko toxický plyn s najvyššou elektronegativitou spomedzi všetkých prvkov (odpoveď b; v kľúči správne b, c, d, g). "
        "V prírode sa nachádza výlučne viazaný v zlúčeninách, najmä v mineráli kazivci (fluorite CaF2; odpoveď c). "
        "Ako najsilnejšie oxidačné činidlo prudko oxiduje aj vodu za vývoja kyslíka: 2 F2 + 2 H2O -> 4 HF + O2 (odpoveď g). "
        "Fluór patrí medzi biogénne mikroprvky dôležité pre pevnosť zubnej skloviny, nie makroprvky (a, e sú nepravdivé)."
    ),
    438: (
        "Chlór patrí medzi biogénne makroprvky, pričom chloridový anión Cl- je dominantným extracelulárnym aniónom v ľudskom tele (odpoveď a). "
        "Spomedzi všetkých halogénov je v prírode najrozšírenejší (najmä v morskej vode vo forme NaCl; odpoveď b) a v elementárnom stave je pre človeka dusivým jedovatým plynom (odpoveď h). "
        "Pri bežnej laboratórnej teplote s čistým uhlíkom nereaguje (odpoveď e). "
        "V prírode sa voľný nenachádza a v HCl netvorí vodíkové väzby (c, d, f, g neplatia)."
    ),
    439: (
        "Bróm je ťažká, červenohnedá kvapalina, ktorá sa za bežných podmienok ľahko odparuje na dráždivé pary (odpoveď e). "
        "Priemyselne sa vyrába oxidáciou bromidov prítomných v morskej vode pomocou chlóru: 2 Br- + Cl2 -> 2 Cl- + Br2 (odpoveď f). "
        "Jeho nerozpustná soľ bromid strieborný (AgBr) sa vďaka citlivosti na svetlo historicky využíva vo fotografii (odpoveď c) a kvarterná amóniová soľ s bromidovým aniónom tvorí dezinfekčný liek Ajatin (odpoveď g; a, b, d, h neplatia)."
    ),
    440: (
        "Jód je esenciálny biogénny mikroprvok nevyhnutný pre syntézu tyroidných hormónov tyroxínu (T4) a trijódtyronínu (T3) v štítnej žľaze (odpoveď a). "
        "Tvorí fialovočierne kryštáliky s kovovým leskom (odpoveď h), ktoré sa pri miernom zahriatí ľahko čistia sublimáciou (odpoveď f). "
        "V medicíne sa široko využíva ako dezinfekcia vo forme Lugolovho roztoku (roztok I2 v jodide draselnom KI; odpoveď d). "
        "V čistej vode sa rozpúšťa veľmi slabo a nečistí sa destiláciou (b, c, e, g sú nesprávne)."
    ),
    441: (
        "Medzi biogénne mikroprvky (stopové prvky) nepatria sodík a vápnik, pretože sú to biogénne makroprvky tvoriace podstatnú časť hmotnosti tela (odpovede b, c). "
        "Plutónium (Pu) je syntetický rádioaktívny aktinoid bez biologickej funkcie (odpoveď e) a argón (Ar) je inertný atmosférický plyn, ktorý sa v metabolizme neuplatňuje (odpoveď h). "
        "Zinok, meď, selén a kobalt naopak patria medzi esenciálne biogénne mikroprvky (a, d, f, g)."
    ),
    442: (
        "O železe neplatia tvrdenia a, b, d, g: chlorofyl obsahuje ako centrálny ión horčík, v koncentrovanej H2SO4 sa železo pasivuje ochrannou vrstvou oxidov, v tele sa nachádza nielen v hemoglobíne, ale aj v myoglobíne, cytochrómoch a feritíne, a žltá krvná soľ je priemyselný komplex K4[Fe(CN)6], nie náhrada krvi. "
        "Tvrdenia c, e, h sú pravdivé, pretože železo ľahko hrdzavie, najvyššie oxidačné číslo dosahuje vo feranoch (+VI) a zelená skalica je FeSO4 . 7 H2O."
    ),
    443: (
        "Chróm je biogénny stopový prvok (mikroprvok), ktorého trojmocná forma sa podieľa na regulácii metabolizmu sacharidov sprostredkovanej inzulínom (odpoveď a). "
        "V roztokoch má najstabilnejšie oxidačné číslo +III, ktoré tvorí zelené alebo fialové hydratované komplexy (odpoveď c). "
        "V najvyššom oxidačnom stave +VI tvorí žlté chromany a oranžové dichrómany (Cr2O7 2-; odpoveď d), ktoré v kyslom prostredí pôsobia ako silné oxidačné činidlá (odpoveď h; b, e, f, g sú nepravdivé)."
    ),
    444: (
        "Mangán je esenciálny biogénny mikroprvok prítomný v ľudskom organizme, kde je kofaktorom enzýmov ako pyruvátkarboxyláza či Mn-SOD (odpovede a, d). "
        "Elementárny kov sa vyrába aluminotermickou redukciou svojich oxidov práškovým hliníkom (odpoveď b). "
        "Jeho soľ manganistan draselný (KMnO4, hypermangán) má silné oxidačné účinky a v medicíne sa používa ako antiseptikum a dezinfekcia (odpoveď e). "
        "V Beketovom rade leží naľavo od vodíka a tvorí viaceré stabilné oxidačné čísla od +II po +VII (c, f, g, h neplatia)."
    ),
    445: (
        "Najstabilnejšou podvojnou soľou Fe2+ je Mohrova soľ (NH4)2Fe(SO4)2 . 6 H2O, ktorá na vzduchu nepodlieha takej rýchlej samovoľnej oxidácii ako FeSO4 (odpoveď a). "
        "Ferrokyanid draselný K4[Fe(CN)6] je žltá krvná soľ (odpoveď e) a Uffelmannovo činidlo obsahuje komplexne viazané Fe3+ s fenolom na dôkaz kyseliny mliečnej (odpoveď f). "
        "Voľné katióny Fe3+ vo vode silne hydrolyzujú a už pri pH = 4 precipitujú ako nerozpustný hydratovaný oxid/hydroxid železitý (odpoveď g; b, c, d, h neplatia)."
    ),
    446: (
        "Meď je ušľachtilý kov (E° = +0,34 V) známy už od praveku v dobe bronzovej (bronz je zliatina medi a cínu; odpoveď d). "
        "Pre svoj kladný potenciál nereaguje s neoxidujúcimi kyselinami, ale rozpúšťa sa v koncentrovanej kyseline dusičnej, pričom ju redukuje na oxidy dusíka NOx a sama sa oxiduje na Cu2+ (odpoveď g). "
        "V biologických systémoch pôsobí ako esenciálny biogénny mikroprvok (cytochróm c oxidáza, ceruloplazmín) a so zinkom tvorí zliatinu mosadz (v oficiálnom kľúči správne možnosti a, c, d, g)."
    ),
    447: (
        "Striebro (Ag) je ušľachtilý kov s najvyššou elektrickou a tepelnou vodivosťou zo všetkých prvkov (odpoveď f). "
        "Využíva sa pri výrobe zrkadiel, kde sa redukciou strieborných komplexov (Tollensovo činidlo) vylučuje lesklé elementárne striebro priamo na sklo (odpoveď b). "
        "Ako ušľachtilý kov nereaguje s kyselinou chlorovodíkovou, ale rozpúšťa sa v koncentrovanej kyseline dusičnej za vzniku AgNO3 a vývoja oxidov dusíka (odpoveď h; v kľúči správne b, d, f, h)."
    ),
    448: (
        "Zlato je mimoriadne chemicky odolný, rýdzi ušľachtilý kov s vysokou hustotou (19,3 g/cm3), ktorý sa v náplavoch riek nachádza v elementárnej forme a dá sa ťažiť ryžovaním (odpoveď h). "
        "Čistota a obsah zlata v zliatinách sa tradične udáva v karátoch (24 karátov je rýdze zlato; odpoveď e). "
        "Rozpúšťa sa iba v silných oxidačných zmesiach (lúčavka kráľovská) a v roztokoch preferuje stabilné oxidačné číslo +III, pričom je mäkké a kujné (v kľúči správne a, c, e, h; d, f, g sú nesprávne)."
    ),
    449: (
        "Zinok je esenciálny biogénny mikroprvok tvoriaci aktívne centrum stoviek enzýmov vrátane karbonanhydrázy a alkoholdehydrogenázy (odpoveď a). "
        "Má jediné stále oxidačné číslo +II s plne zaplnenou konfiguráciou 3d10 (odpoveď d) a vo veľkom meradle sa využíva na galvanické pokovovanie železa na ochranu pred koróziou (odpoveď c). "
        "Na vzduchu horí jasným plameňom na biely oxid zinočnatý ZnO (odpoveď f). "
        "Ako neušľachtilý amfotérny kov reaguje s kyselinami aj hydroxidmi za vývoja vodíka (b, e, g, h sú nepravdivé)."
    ),
    450: (
        "Ortuť (Hg) je jediný kovový prvok, ktorý je za bežných laboratórnych podmienok kvapalný (odpoveď c). "
        "V Beketovom rade napätia kovov leží napravo od vodíka (E° = +0,85 V), patrí medzi ušľachtilé kovy a so zriedenými kyselinami nereaguje (odpoveď d). "
        "Vyznačuje sa schopnosťou rozpúšťať iné kovy za vzniku amalgámov (odpoveď g) a elementárna ortuť aj jej zlúčeniny sú pre človeka vysoko toxické, poškodzujúce najmä CNS a obličky (odpoveď f; a, b, e, h neplatia)."
    ),
}

# Načítanie batch_8.json
with open('scripts/chem_batches/batch_8.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions from batch_8.json")

# Aplikácia vysvetlení
updated_count = 0
for idx, q in enumerate(questions):
    q_num = 401 + idx
    if q_num in explanations:
        q['explanation'] = explanations[q_num]
        updated_count += 1
    else:
        print(f"Warning: Missing explanation for question {q_num}")

# Uloženie do batch_8_explained.json
output_path = 'scripts/chem_batches/batch_8_explained.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully wrote {len(questions)} questions ({updated_count} updated) to {output_path}")
