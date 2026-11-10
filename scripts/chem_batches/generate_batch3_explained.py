# -*- coding: utf-8 -*-
import json

explanations = {
    101: "Alkalické kovy (prvky 1. skupiny: Li, Na, K, Rb, Cs, Fr) tvoria významné prírodné minerály ako sylvín (KCl), halit alias kamenná soľ (NaCl) a čilský liadok (NaNO3) (a, c, d, e). Naopak, kalcit a aragonit (CaCO3) spolu s magnezitom (MgCO3) sú minerály kovov alkalických zemín (b, f, h) a cinabarit (HgS) je sulfidový minerál prechodného kovu ortuti (g).",

    102: "V užšom zmysle sa v anorganickej chémii medzi kovy alkalických zemín zaraďujú iba prvky Ca, Sr, Ba a Ra, ktorých zlúčeniny sú prítomné v dolomite (CaCO3·MgCO3), baryte (BaSO4), apatite (Ca5(PO4)3(F,Cl,OH)) a kazivci (CaF2) (b, d, f, h). Minerály magnezit (MgCO3), beryl (Be3Al2Si6O18), sylvín (KCl) a bauxit (Al2O3·xH2O) kovy alkalických zemín v tomto zmysle neobsahujú (a, c, e, g), keďže obsahujú horčík, berýlium, draslík alebo hliník.",

    103: "Správne systematické názvy podvojných a komplexných zlúčenín sú uvedené v možnostiach b, c, e a f: dodekahydrát síranu draselno-hlinitého (kamenec) AlK(SO4)2·12H2O, dihydroxid-uhličitan meďnatý (malachit) Cu2CO3(OH)2, tetrachloroželezitan draselný K[FeCl4] a hexahydrát síranu diamónno-železnatého (Mohrova soľ) Fe(NH4)2(SO4)2·6H2O. V možnosti a nesedí stechiometria (Na3[AlF6] je hexafluorohlinitan trisodný), v d je uvedený nesprávny názov pre koordinačný komplex a v g chýba označenie kryštalického hydrátu.",

    104: "Dural je ľahká a pevná zliatina hliníka s meďou a horčíkom (Al, Cu, Mg), literina (písmovina) je tvorená antimónom, cínom a olovom (Sb, Sn, Pb), konštantán obsahuje meď, nikel a mangán (Cu, Ni, Mn) a mäkká spájka je eutektická zliatina olova a cínu (Pb, Sn) (a, b, e, h). Mosadz je zliatina medi so zinkom (nie cínom, c) a bronz je zliatina medi s cínom (nie niklom a zinkom, d).",

    105: "Korektné chemické vzorce minerálov a technických látok sú: kyanid draselný cyankáli (KCN), kryolit (hexafluorohlinitan trisodný Na3[AlF6]), kaolinit (hlinitokremičitan Al2(OH)4Si2O5) a sylvín (chlorid draselný KCl) (a, b, c, f). Baryt je síran bárnatý BaSO4, kazivec fluorid vápenatý CaF2, beryl hlinitokremičitan berýlnatý a bauxit hydratovaný oxid hlinitý.",

    106: "Amalgámy sú špecifické zliatiny kovov s kvapalnou ortuťou, pričom zubný amalgám vzniká zmiešaním ortuti s práškom Ag, Sn a Cu a sodíkový amalgám (Na-Hg) sa využíva v chémii ako silné redukčné činidlo (b, c, f). Ortuť netvorí amalgámy s prechodnými kovmi železnej triády (Fe, Co, Ni), preto sa ortuť bezpečne transportuje a skladuje v oceľových či železných nádobách (h); ortuť teda netvorí amalgámy so všetkými kovmi bez výnimky a amalgámy môžu byť za bežnej teploty aj tuhé (a, d, g).",

    107: "Správne vzorce a systematické názvy hydridov sú: KH – hydrid draselný, PH3 – fosfán, H2S – sulfán a SiH4 – silán (d, f, g, h). Možnosti a, b, c a e obsahujú hrubé chyby: azán je NH3 (nie AlH3, čo je alán), hydrid horečnatý má stechiometriu MgH2 (nie Mg2H), borán je BH3 resp. B2H6 (nie BrH, čo je bromovodík) a hydrid sodný je NaH (nie NaH2).",

    108: "Koordinačná zlúčenina tetrachloroplatnatan tetraammín-dichloroplatičitý má vzorec [PtCl2(NH3)4][PtCl4], kde katión s centrálnym atómom Pt(+IV) a nábojom +2 obsahuje 4 elektroneutrálne ligandy NH3 a 2 ligandy Cl-, kým komplexný anión s Pt(+II) a koordinačným číslom 4 obsahuje štyri ligandy Cl- (b, e, f). V celej molekule sa nachádza celkovo 6 atómov chlóru (g), neutrálne ligandy sú iba štyri (nie 10, a) a katión sa v zápise vzorca uvádza vždy pred aniónom (h).",

    109: "V komplexe [Co(H2O)(NH3)3]2(SO4)3 vystupujú ako ligandy neutrálne molekuly vody a amoniaku, takže náboj troch vonkajších síranových aniónov ((SO4)3^(6-)) vyrovnávajú dva trojmocné katióny [Co(H2O)(NH3)3]^(3+); centrálnym atómom je kobalt s oxidačným číslom +III a systematický názov je síran akva-triamminkobaltitý (a, f, g). Molekula obsahuje celkovo 14 atómov kyslíka (2×1 z vody + 3×4 zo síranov) (h), voda je viazaná koordinačne vo vnútornej sfére (nie kryštalicky, e) a centrálny kobalt viaže iba 4 ligandy (c).",

    110: "Hydrát chloridu pentaakva-chlorochromitého má racionálny vzorec [CrCl(H2O)5]Cl2·H2O, kde chromitý katión Cr^(3+) viaže päť neutrálnych akva-ligandov a jeden chlorido-ligand Cl-, čím tvorí komplexný katión s nábojom +2 (d, g, h). Vo vonkajšej sfére vystupujú dva chloridové anióny Cl- s oxidačným číslom -I (f) a jedna kryštalicky viazaná molekula vody; celkové koordinačné číslo chrómu je 6, nie 3 (c).",

    111: "Atómové jadro sústreďuje viac ako 99,9 % hmotnosti celého atómu, hoci jeho priemer (~10^(-15) m) je zhruba 100 000-krát menší než priemer celého elektrónového obalu (~10^(-10) m) (c, f). Nukleóny (protóny a neutróny) sú zložené z kvarkov prvej generácie (u a d) a jadrová stabilita je podmienená optimálnym pomerom neutrónov k protónom N/Z (e, g). Nukleónové číslo A udáva súčet nukleónov, kým Z je protónové číslo (d).",

    112: "Podľa štandardného modelu časticovej fyziky je bežná látka tvorená 12 základnými elementárnymi fermiónmi: 6 kvarkami (u, d, c, s, t, b) a 6 leptónmi (elektrón, mión, tauón a tri neutrína) (a, b). Pozitrón je antičasticou elektrónu s opačným kladným nábojom a interakcie medzi časticami sprostredkúvajú štyri základné sily (gravitačná, elektromagnetická, silná a slabá) (e, f). Elektrón je leptón (nie kvark, c), antičasticou protónu je antiprotón (d) a elektromagnetickú interakciu prenášajú fotóny, nie gluóny (g).",

    113: "Rádionuklidy sú nestabilné jadrá podliehajúce rádioaktívnemu rozpadu na stabilnejšie dcérske nuklidy sprevádzanému emisiou jadrového žiarenia, pričom ich základnou charakteristikou je polčas rozpadu (b, d). V prírode sa vyskytuje približne 50 prírodných rádionuklidov vrátane stopových prvkov zemskej kôry, akými sú astát a francium z rozpadových radov (c, h). Umelo pripravených rádionuklidov však existuje niekoľko tisíc (nie 50, g) a pojem rádionuklid zahŕňa rádioaktívne izotopy všetkých prvkov, nielen rádia či transuránov (a, e).",

    114: "Polčas rozpadu (doba polpremeny, T1/2) je prísna konštanta rádioaktívneho rozpadu charakteristická pre konkrétny nuklid, ktorá nezávisí od vonkajších fyzikálnych podmienok (teplota, tlak, chemická väzba) ani od východiskového množstva nuklidu (c, f). V závislosti od druhu rádionuklidu sa môže pohybovať od zlomkov sekúnd až po miliardy rokov (e, h). Žiadne bežné zahrievanie ani zmena tlaku rýchlosť jadrového rozpadu nemení (b, g).",

    115: "Veľkosť elementárneho náboja je e = 1,602·10^(-19) C; protón nesie kladný náboj (+e), elektrón rovnaký záporný náboj (-e) a neutrón má elektrický náboj nulový (a, c, e). V neutrálnom atóme sa počet protónov rovná počtu elektrónov, preto sa súčet nábojov jadra v absolútnej hodnote presne rovná celkovému zápornému náboju obalu (g). Voľné neutrálne atómy majú celkový náboj nulový, kladný a záporný náboj sú v dokonalej rovnováhe (h).",

    116: "Hlavné kvantové číslo n určuje celkovú energiu elektrónu v atóme vodíka (podľa vzťahu En = -B/n^2, kde B = 13,6 eV), určuje veľkosť a priestorové ohraničenie orbitálu a pre valenčnú vrstvu sa zhoduje s číslom periódy (b, d, f, g). Nadobúda iba kladné celé čísla n = 1, 2, 3... (nikdy nie n = 0, c), tvar orbitálu je primárne daný vedľajším kvantovým číslom l (a) a počet protónov definuje protónové číslo Z (h).",

    117: "Vedľajšie kvantové číslo l nadobúda hodnoty od 0 do n - 1 (tradične označované písmenami s, p, d, f) a určuje priestorový tvar orbitálu a jeho príspevok k energii elektrónu vo viacelktrónovom atóme (a, e, g). Pre degenerované orbitály v rámci rovnakej podvrstvy (napr. 2px, 2py, 2pz) má identickú hodnotu (c). Veľkosť orbitálu je riadená číslom n (b) a hodnoty ±1/2 patria spinovému kvantovému číslu s (d).",

    118: "Magnetické kvantové číslo m určuje priestorovú orientáciu orbitálu v magnetickom poli a môže nadobúdať celočíselné hodnoty od -l cez 0 až po +l, čo predstavuje celkovo (2l + 1) hodnôt zodpovedajúcich počtu degenerovaných orbitálov danej podvrstvy (a, b, c). Pre podvrstvu f (l = 3) nadobúda presne 7 hodnôt: -3, -2, -1, 0, 1, 2, 3 (h). Neudáva počet valenčných elektrónov ani celkovú energiu elektrónu (e, g).",

    119: "Protónové číslo Z definuje počet protónov v atómovom jadre, určuje identitu chemického prvku a jeho postavenie v periodickej sústave (f). Pri rádioaktívnej premene beta mínus (β-) sa neutrón mení na protón a Z vzrastá na Z + 1, kým pri premene beta plus (β+) sa protón mení na neutrón a Z klesá na Z - 1 (b, e); pri vyžiarení gama kvanta zostáva Z nezmenené (g). Celkový počet nukleónov (protónov a neutrónov) udáva nukleónové číslo A (h).",

    120: "Počet elektrónov v elektrónovom obale je daný vzťahom Ne = Z - q: neutrálny neón 10Ne má 10 elektrónov, anióny O^(2-) (8 + 2) a F^(-) (9 + 1) majú 10 elektrónov a katión Na^(+) (11 - 1) má rovnako 10 elektrónov, čím tvoria izoelektrónový rad s konfiguráciou [Ne] (a, b, f, h). Chloridový anión Cl- a draselný katión K+ majú 18 elektrónov ([Ar], d, g) a stroncíum Sr^(2+) má 36 elektrónov (c).",

    121: "Elektrónová vrstva L zodpovedá hlavnému kvantovému číslu n = 2, takže obsahuje iba podvrstvy s (l = 0) a p (l = 1), zložené z jedného orbitálu s a troch orbitálov p (a). Maximálna elektrónová kapacita každej vrstvy je daná univerzálnym vzorcom 2n^2, čo pre hladinu L činí presne 2·(2^2) = 8 elektrónov (b, g). Orbitály d sa energeticky vyskytujú až od tretej hladiny M (n = 3, kapacita 18 elektrónov) (c, e).",

    122: "Nuklid je chemická látka zložená z atómov s identickým protónovým (Z) aj nukleónovým (A) číslom, napríklad kyslík 17_8O, bór 12_5B či kadmium 112_48Cd (c, f). Rôzne nuklidy toho istého prvku s rovnakým Z, ale odlišným A (napr. izotopy vodíka 1H, 2H a 3H) sú izotopmi (g). Nuklidy s rovnakým A a rôznym Z sú izobary (e) a mnohé nuklidy sú úplne stabilné, takže termín nuklid nie je synonymom pre rádioaktívny prvok (b).",

    123: "Neutrón je elektroneutrálna častica jadra atómu patriaca spolu s protónom medzi nukleóny s relatívnou hmotnosťou približne 1 u (b, c, f). V nestabilných jadrách s nadbytkom protónov môže neutrón vznikať procesom beta plus premeny (p -> n + e+ + νe) (e). Neutrón nemá záporný elektrický náboj (a) a jeho hmotnosť je len nepatrne vyššia než hmotnosť protónu, rozhodne nie dvojnásobná (h).",

    124: "Z kompletného zápisu nuklidu A_Z X vyplýva, že hliník 27_13Al obsahuje 13 protónov, 13 elektrónov a 14 neutrónov (27 - 13) a dusík 14_7N má zhodne 7 protónov aj 7 neutrónov (a, f). Nuklidy s rovnakým Z a rôznym A sú izotopy (58Co a 60Co) a nuklidy s rovnakým A a rôznym Z sú izobary (40K a 40Ca) (c, d). Horné číslo je nukleónové číslo A (pre Ti je A = 48, nie 26, e) a horečnatý katión Mg^(2+) má po odovzdaní dvoch elektrónov len 10 elektrónov (h).",

    125: "Základný stav atómu je stav s najnižšou možnou vnútornou energiou, kedy atóm neabsorboval excitačnú energiu a nie je excitovaný (f, h). Elektróny v ňom obsadzujú jednotlivé energetické hladiny a orbitály od najnižšej energie v súlade s výstavbovým princípom, Pauliho princípom a Hundovým pravidlom (c). Vyššie energetické stavy po prijatí kvanta energie predstavujú excitované stavy (b, e).",

    126: "Pre vedľajšie kvantové číslo l = 2 (orbitály d) nadobúda magnetické kvantové číslo m celočíselné hodnoty v intervale od -l do +l, teda kompletnú množinu -2, -1, 0, 1, 2 (d). Možnosti b, c a h predstavujú dovolené podmnožiny alebo jednotlivé platné hodnoty z tohto intervalu (0; -1, 0, 1; 0, 1, 2). Hodnoty ±3 patria až podvrstve f (l = 3, f) a neceločíselné hodnoty ±1/2 charakterizujú spinové kvantové číslo s (g).",

    127: "V perióde s rastúcim protónovým číslom Z rastie náboj jadra, čo vedie ku kontrakcii obalu (zmenšeniu atómového polomeru) a nárastu ionizačnej energie (f), kým v skupine s rastúcim Z rastie počet vrstiev a klesá elektrónová afinita (g). Katióny majú vždy menší polomer než neutrálny atóm v dôsledku prevahy náboja jadra a anióny majú väčší polomer v dôsledku medzielektrónového odpudzovania (b, c). Elektronegativita je schopnosť atómu priťahovať väzbové elektróny, nie ich odpudzovať (e).",

    128: "Chloridový anión Cl- prijatím elektrónu dosahuje konfiguráciu vzácneho plynu argónu [Ar] a neutrálny fluór 9F má v základnom stave konfiguráciu 1s2 2s2 2p5 (c, h). Chalkogény (16. skupina) majú valenčnú konfiguráciu ns2 np4 (d) a pri vanáde po obsadení 4s orbitálu klesá energia 3d orbitálov pod úroveň 4s (f). Prvá sféra (n = 1) obsahuje iba orbitál 1s (a), katión Ca^(2+) má orbitál 4s prázdny (b) a podvrstva d pojme maximálne 10 elektrónov (g).",

    129: "Elektrón sa pohybuje v príťažlivom elektrickom poli kladného jadra a vykazuje vlnovo-korpuskulárny dualizmus ako častica s nepatrnou pokojovou hmotnosťou (~9,11·10^(-31) kg) a vlnovými vlastnosťami (a, e, f). Sodík má veľmi nízku prvú ionizačnú energiu, takže ochotne odovzdáva svoj valenčný 3s elektrón za vzniku stabilného katiónu Na+ (c). Odtrhnutím elektrónu vzniká kladný katión, nie anión (b) a stav elektrónu je popísaný štyrmi kvantovými číslami (d).",

    130: "Medzi nesprávne tvrdenia patrí b, pretože podľa Hundovho pravidla sa dva valenčné p-elektróny uhlíka rozmiestňujú s paralelným spinom do dvoch degenerovaných orbitálov (2px1 2py1), nie do jedného orbitálu px (b). Orbitály f (l = 3) sú sedemkrát degenerované (2l + 1 = 7), nie trikrát (g). Možnosti a a e rovnako obsahujú chybné formulácie výstavby a zápisu, zatiaľ čo konfigurácie O^(2-) (1s2 2s2 2p6) a halogénov (ns2 np5) sú správne (d, f).",

    131: "Správne konfigurácie podľa pravidiel výstavby a Hundovho pravidla sú: bór 5B: [He] 2s2 2px1 a dusík 7N s tromi nespárovanými elektrónmi v degenerovaných orbitáloch 1s2 2s2 2px1 2py1 2pz1 (a, g). Katióny Ca^(2+) a K^(+) stratou valenčných 4s elektrónov nadobúdajú stabilnú konfiguráciu argónu 1s2 2s2 2p6 3s2 3p6 alias [Ar] (b, d). Anión O^(2-) má konfiguráciu [Ne] bez elektrónov v 3s (f) a neutrálne lítium má iba tri elektróny 1s2 2s1 (h).",

    132: "Pri ionizácii prechodných kovov sa elektróny odštepujú prednostne z vonkajšieho orbitálu 4s: Zn^(2+) má preto konfiguráciu [Ar] 3d10 a Fe^(2+) má [Ar] 3d6 (a, d). Tretí excitovaný stav chlóru Cl*** zahŕňa rozštiepenie troch elektrónových párov do 3d orbitálov ([Ne] 3s1 3p3 3d3) a excitovaný bór B* má konfiguráciu 1s2 2s1 2p2 (b, f). Katión Mn^(2+) má konfiguráciu [Ar] 3d5, nie 4s2 3d3 (c).",

    133: "Podľa kvantovej mechaniky je vedľajšie kvantové číslo ohraničené podmienkou l ≤ n - 1: pre n = 1 môže existovať iba l = 0 (orbitál 1s, orbitál 1p neexistuje) (a). Pre n = 2 existujú len stavy s a p (l = 0, 1), takže orbitál 2d je fyzikálne nemožný (h) a orbitály f (l = 3) sa objavujú až od štvrtej vrstvy (n = 4), zápis 3f je teda neplatný (d). Ostatné orbitály (2s, 2p, 3d, 4d, 5s) sú dovolené.",

    134: "Správne zápisy konfigurácií neutrálnych atómov v základnom stave sú: neón 10Ne: 1s2 2s2 2p6, kremík 14Si: [Ne] 3s2 3p2, vápnik 20Ca: [Ar] 4s2 a zinok 30Zn: [Ar] 3d10 4s2 (a, c, f, g). Chlór má v základnom stave konfiguráciu [Ne] 3s2 3p5 (b), hliník [Ne] 3s2 3p1 (d) a neutrálny chróm vykazuje v dôsledku mimoriadnej stability polozaplneného 3d orbitálu anomálnu konfiguráciu [Ar] 3d5 4s1, nie 3d4 4s2 (h).",

    135: "Excitovaný stav atómu vzniká dodaním energie, kedy dochádza k rozštiepeniu valenčného elektrónového páru a preskoku elektrónu do voľného orbitálu: uhlík v excitovanom stave C* prechádza na štvorväzbovú konfiguráciu [He] 2s1 2p3 (d), síra S** na šesťväzbovú konfiguráciu [Ne] 3s1 3p3 3d2 (h) a bróm Br** na [Ar] 3d10 4s2 4p3 4d2 (a, e). Konfigurácia medi [Ar] 3d10 4s1 je jej stabilným základným stavom, nie excitovaným (f).",

    136: "Orbitály v izolovanom atóme, ktoré majú rovnaké hlavné aj vedľajšie kvantové číslo (rovnaké n a l), sú energeticky rovnocenné (degenerované) a ich energetická hladina nezávisí od hodnoty m (b). Hodnote l = 3 zodpovedajú orbitály typu f (f) a so vzrastajúcim hlavným kvantovým číslom n sa zväčšuje efektívny polomer a veľkosť orbitálov daného typu (g). Orbitál 4p je vždy väčší než 3p (c) a pre m od -3 po +3 (7 orbitálov f) je maximálna kapacita 14 elektrónov, nie 10 (e).",

    137: "Počet degenerovaných orbitálov v danej podvrstve je striktne určený vzťahom (2l + 1): podvrstva s má vždy 1 orbitál, podvrstva p má 3 orbitály a podvrstva d má 5 orbitálov (b, c, g, h). Hladina L (n = 2) teda obsahuje 1 orbitál typu s a 3 orbitály typu p (c) a hladina M (n = 3) obsahuje 1 orbitál s, 3 orbitály p a 5 orbitálov d (g). V žiadnej vrstve nemôže existovať viac ako jeden orbitál typu s (d, f).",

    138: "Hydridový anión H- prijatím elektrónu dosahuje stabilnú konfiguráciu hélia (1s2), zatiaľ čo katióny Na+ a Al3+ odovzdaním valenčných elektrónov a fluoridový anión F- prijatím elektrónu dosahujú stabilný oktet neónu [Ne] (a, d, e, g). Naopak, ióny prechodných kovov ako Ti2+ ([Ar] 3d2), Cu2+ ([Ar] 3d9), Zn2+ ([Ar] 3d10) a Ag2+ ([Kr] 4d9) si zachovávajú elektróny v d-orbitáloch a nemajú konfiguráciu vzácneho plynu (b, c, f, h).",

    139: "Medzi nesprávne tvrdenia patria a, e, f a g: pre hlavné kvantové číslo n = 3 môže vedľajšie číslo l nadobúdať iba hodnoty 0, 1 a 2, takže stav l = 3 (orbitál f) na hladine M nemôže existovať (a). Veľkosť orbitálov rastie s rastúcim číslom n, takže orbitály 3d a 4d, resp. 1s až 4s rozhodne nie sú rovnako veľké (e, g). Dva elektróny s odlišným magnetickým číslom m (-2 vs +2) sa nachádzajú v dvoch rôznych priestorovo orientovaných orbitáloch (f).",

    140: "Pri excitácii elektrónu dochádza k jeho preskoku do voľného orbitálu vyššej podvrstvy v rámci valenčnej sféry, napríklad z 3p (l = 1) do 3d (l = 2) (d). Pri excitácii atómu uhlíka C* prechádza jeden 2s elektrón do voľného orbitálu 2p, takže tri elektróny majú l = 1 (f), a pri atóme brómu vedie excitácia k presunu elektrónov z orbitálov 4p do 4d, čím ich počet v p-orbitáloch klesá (g). Prvky od 3. periódy môžu vďaka prítomnosti d-orbitálov tvoriť viacero po sebe idúcich excitovaných stavov (h).",

    141: "Výstavbový princíp určuje, že elektróny najprv obsadzujú orbitály s nižšou energiou, riadené pravidlom najnižšieho súčtu (n + l) (c, e). Podľa Hundovho pravidla sa v súbore (2l + 1) degenerovaných orbitálov tvoria elektrónové páry až po tom, čo je každý orbitál obsadený jedným elektrónom s paralelným spinom (d, g). Degenerované orbitály sa líšia hodnotou magnetického kvantového čísla m (a) a pri rovnakom súčte (n + l) sa skôr zapĺňa orbitál s nižším n (f).",

    142: "K nesprávnym tvrdeniam patria c, e, f a h: ionizačná energia je energia potrebná na odtrhnutie elektrónu z atómu (energia spotrebovaná, nie uvoľnená pri prijatí elektrónu – čo je definícia elektrónovej afinity) (e). Pri atómoch K a Ca sa v súlade s pravidlom (n + l) najprv zapĺňa orbitál 4s (4 + 0 = 4) a až po ňom orbitál 3d (3 + 2 = 5) (f). Rotáciu a vlastný moment hybnosti elektrónu vyjadruje spinové kvantové číslo s (ms), nie magnetické kvantové číslo m (h).",

    143: "Chróm vykazuje v dôsledku vysokej stability polozaplnenej d-podvrstvy anomálnu konfiguráciu [Ar] 3d5 4s1 (a), neutrálne železo má konfiguráciu [Ar] 3d6 4s2 (c) a hydridový ión H- má stabilnú konfiguráciu hélia 1s2 alias [He] (b). Katión Cu2+ vzniká odtrhnutím 4s elektrónu a jedného 3d elektrónu z atómu medi, čím vzniká stabilný stav [Ar] 3d9 (d). Zápisy s 3d4 4s2 pre chróm (h) a 4s2 3d3 pre Mn2+ (f) sú chybné.",

    144: "Ionizačná energia predstavuje energiu potrebnú na odtrhnutie valenčného elektrónu od atómu v základnom plynnom stave (b). Pri tvorbe valenčných excitovaných stavov sa elektrónové páry valenčnej sféry štiepia a elektróny preskakujú do energeticky najbližších prázdnych orbitálov s rovnakým n (napr. 3s/3p -> 3d), čo priamo podmieňuje väzbovosť prvkov v zlúčeninách (c, g, h). Štiepia sa väzbové páry s najvyššou (nie najnižšou) energiou (a) a nízka ionizačná energia znamená vysokú elektropozitivitu a reaktivitu, nie stabilitu prvku (e).",

    145: "K nesprávnym tvrdeniam patria: hlavné kvantové číslo n nadobúda iba kladné celé čísla n ≥ 1, hodnota n = 0 neexistuje (a). Magnetické kvantové číslo m je priamo závislé od vedľajšieho čísla l (m ∈ <-l; +l>) (b) a nespárované elektróny v degenerovaných orbitáloch musia mať podľa Hundovho pravidla rovnaký paralelný spin (h). Súčasné presné stanovenie polohy aj hybnosti (rýchlosti) mikroskopických častíc striktne vylučuje Heisenbergov princíp neurčitosti (e).",

    146: "Nuklid uhlíka 11_6C má pomer N/Z = 5/6, čo predstavuje jadro s nadbytkom protónov oproti stabilnému izotopu 12_6C (c, f). Stabilizuje sa rádioaktívnou beta plus (β+) premenou, pri ktorej sa jadrový protón premieňa na neutrón za vyžiarenia pozitrónu (1_1p -> 1_0n + e+) a elektrónového neutrína (d). V dôsledku tejto premeny klesá protónové číslo o jednotku (Z -> Z - 1, zo 6 na 5 za vzniku bóru 11_5B), zatiaľ čo nukleónové číslo A = 11 zostáva zachované (g).",

    147: "Prechod metastabilného jadra 80m_35Br do základného stavu 80_35Br predstavuje izomérny prechod (jadrovú deexcitáciu) sprevádzaný uvoľnením gama (γ) žiarenia (d). Pri emisii gama fotónu sa nemení protónové číslo Z = 35 ani nukleónové číslo A = 80 (f). Žiarenie gama je vysokofrekvenčné elektromagnetické žiarenie bez elektrického náboja, ktoré sa nevychyľuje v elektrickom ani magnetickom poli a spomedzi bežných rádioaktívnych žiarení je najprenikavejšie (g, h).",

    148: "Podstatou beta mínus (β-) rádioaktivity je samovoľná jadrová premena prebytočného neutrónu na protón za vyžiarenia rýchleho elektrónu a antineutrína (1_0n -> 1_1p + e-) (h). Vyžiarený prúd elektrónov tvorí korpuskulárne ionizujúce žiarenie so záporným elementárnym nábojom, ktoré je možné odchýliť elektrickým aj magnetickým poľom (e, f). Príkladom je prirodzená premena draslíka 40_19K na vápnik 40_20Ca (a); beta žiarenie nie je elektromagnetickej povahy (g) a najvyššiu prenikavosť vykazuje gama žiarenie (d).",

    149: "Izotopy sú nuklidy rovnakého prvku, ktorých atómové jadrá majú zhodný počet protónov (rovnaké Z), no líšia sa počtom neutrónov (rôzne nukleónové číslo A) (g). Typickým príkladom sú izotopy vodíka prócium (1H), deutérium (2H) a trícium (3H) (e). Keďže majú rovnakú elektrónovú konfiguráciu, vykazujú prakticky identické chemické vlastnosti, no kvôli rozdielnej hmotnosti jadier sa mierne líšia fyzikálnymi vlastnosťami (h). Atómy s rovnakým A a rôznym Z sú izobary (c).",

    150: "Izobary sú nuklidy rôznych chemických prvkov, ktoré majú zhodné nukleónové číslo A (rovnaký celkový počet nukleónov), ale odlišné protónové číslo Z (d, h). Bežne vznikajú pri beta rádioaktívnych premenách (β- aj β+), pri ktorých sa protónové číslo mení o ±1, kým celkový počet nukleónov A zostáva konštantný (c). Príkladom izobárických dvojíc a trojíc sú nuklidy 112_48Cd a 112_50Sn, resp. 12_5B, 12_6C a 12_7N (f, h)."
}

# Load batch_3.json
with open('scripts/chem_batches/batch_3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} questions from batch_3.json")
assert len(data) == 50, f"Expected 50 questions, found {len(data)}"
assert len(explanations) == 50, f"Expected 50 explanations, found {len(explanations)}"

# Check each question and assign explanation
for idx, q in enumerate(data):
    q_num = 101 + idx
    assert q_num in explanations, f"Missing explanation for question {q_num}"
    new_exp = explanations[q_num].strip()
    assert len(new_exp) > 50, f"Explanation too short for question {q_num}"
    q['explanation'] = new_exp

# Save to scripts/chem_batches/batch_3_explained.json
output_path = 'scripts/chem_batches/batch_3_explained.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved explained batch to {output_path}")

# Verification
with open(output_path, 'r', encoding='utf-8') as f:
    verified_data = json.load(f)

print(f"Verification: {len(verified_data)} questions in {output_path}")
for i, q in enumerate(verified_data):
    assert 'explanation' in q and len(q['explanation']) > 50
    assert not q['explanation'].startswith("Správne odpovede podľa oficiálneho kľúča")

print("All verifications passed successfully!")
print("\n--- SAMPLE Q101 ---")
print("Content:", verified_data[0]['content'])
print("Explanation:", verified_data[0]['explanation'])
print("\n--- SAMPLE Q102 ---")
print("Content:", verified_data[1]['content'])
print("Explanation:", verified_data[1]['explanation'])
