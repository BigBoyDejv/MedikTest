# -*- coding: utf-8 -*-
import json

explanations = [
    # 151
    "Prúd rýchlo letiacich jadier hélia (4_2He2+) predstavuje rádioaktívne žiarenie alfa (e). Vzhľadom na svoju relatívne veľkú hmotnosť a kladný náboj +2 má silné ionizačné účinky (b), vychyľuje sa v elektrickom a magnetickom poli (g) a po jeho vyžiarení z jadra klesne nukleónové číslo o 4 a protónové číslo o 2 (f). Nejde o elektromagnetické ani infračervené žiarenie (a, d) a jeho prenikavosť je najnižšia spomedzi všetkých druhov rádioaktívneho žiarenia (c, h).",

    # 152
    "Alfa žiarenie je prúdom jadier hélia 4_2He (g), ktoré sa uvoľňuje napríklad pri rozpade rádia 226_88Ra -> 222_86Rn + 4_2He (a). Pre veľký prierez a hmotnosť častíc má nízku schopnosť prieniku materiálom a zadrží ho už list papiera alebo tenká vrstva vzduchu (e, f). V elektromagnetickom poli sa vychyľuje kvôli kladnému náboju (h), uvoľňuje sa aj pri rozpadoch uránu či tória (b), možno ho spoľahlivo dokázať ionizačnými komorami (c) a protónové číslo po emisii klesá o 2, nie rastie (d).",

    # 153
    "Polčas rozpadu T_1/2 je definovaný ako čas potrebný na rozpad práve polovice počiatočného množstva (hmotnosti alebo počtu jadier) daného rádionuklidu (c). Pre každý izotop je charakteristickou konštantou: pre trícium 3_1H predstavuje približne 12,3 roka (f) a pre urán 238_92U približne 4,5 miliardy rokov, teda výrazne viac ako milión rokov (g). Nezávisí od počiatočného množstva (preto nie fixný 1 mol či 1 g, a, h), u rôznych prvkov je odlišný (e) a po jednom polčase sa rozpadne iba 50 %, nie celá vzorka (d).",

    # 154
    "Prírodné rádioaktívne rozpadové rady (uránovo-rádiový, uránovo-aktíniový a tóriový) zahŕňajú postupný rozpad nestabilných nuklidov prirodzene sa vyskytujúcich v prírode za vyžarovania neviditeľného ionizujúceho žiarenia (a, h). Všetky tri prírodné rady končia stabilnými izotopmi olova (206Pb, 207Pb, 208Pb) (c) a obsahujú plynné rádioaktívne izotopy radónu, ktorý je najťažším vzácnym plynom (e). Neptúniový rad je umelo vytvorený a končí bizmutom 209Bi (b, g), pričom žiadny rad nekončí tríciom ani uhlíkom 14C (d, f).",

    # 155
    "Izotopy sú nuklidy toho istého chemického prvku, ktoré majú zhodné protónové číslo Z (rovnaký počet protónov a elektrónov v neutrálnom atóme), ale líšia sa počtom neutrónov, a teda aj nukleónovým číslom A a relatívnou atómovou hmotnosťou (f, g, h). Typickým príkladom sú izotopy kobaltu 58_27Co a 60_27Co (e). Nuklidy s rovnakým nukleónovým a rôznym protónovým číslom sa nazývajú izobary (a), a nukleóny sú samotné častice jadra (protóny a neutróny), nie druhy atómov (c, d).",

    # 156
    "Gama žiarenie (γ) je vysokofrekvenčné elektromagnetické žiarenie tvorené fotónmi s vysokou energiou, ktoré vykazuje najvyššiu prenikavosť spomedzi jadrových žiarení (a, f). Keďže nenesie náboj ani pokojovú hmotnosť, uvoľňuje sa pri deexcitácii vzbudeného jadra (napríklad pri izomérnom prechode 99m_49In -> 99_49In) a nemení protónové ani nukleónové číslo jadra (c, d). Najsilnejšie ionizačné schopnosti má žiarenie alfa (e), vyžiarením gama nedochádza k zmene Z o -1 (b) a nejde o tok neutrónov (h).",

    # 157
    "Uránový rozpadový rad začína nuklidom 238_92U a končí stabilným izotopom olova 206_82Pb (a), pričom celá premena zahŕňa 8 alfa premien a 6 beta- premien (d). Po štyroch rozpadoch alfa (pokles hmotnosti o 16 na 222) a dvoch rozpadoch beta- (zvýšenie protónového čísla o 2 po poklese o 8: 92 - 8 + 2 = 86) vzniká izotop radónu 222_86Rn (b). Podľa oficiálneho kľúča testovnice UPJŠ LF sú označené možnosti a, b, d a h ako správne (pričom konečným produktom nie je bizmut 212Bi, c, ani rádium, f).",

    # 158
    "V uránovo-rádiovom rade je východiskovým nuklidom urán 238_92U (a), ktorého prvým alfa rozpadom vzniká tórium 234_90Th (g). Rad zahŕňa celkovo 8 premien alfa a 6 premien beta- (d), pričom po 4 alfa a 2 beta- premenách vzniká medziprodukt radón 222_86Rn (b). Možnosti e a h sú nesprávne, pretože počet premien nezodpovedá 6 alfa/4 beta a rad neobsahuje výlučne alfa premeny.",

    # 159
    "Počet neutrónov v jadre sa rovná rozdielu A - Z; atómy 14_7N aj 13_6C majú zhodne 7 neutrónov (a). Dvojice 12C, 13C a 32S, 34S predstavujú izotopy daných prvkov (c), a nuklidy 12_6C (6p, 6n), 32_16S (16p, 16n) a 14_7N (7p, 7n) majú rovnaký počet protónov a neutrónov (d). Podľa oficiálneho kľúča UPJŠ LF je označená aj možnosť h; izotopy uhlíka 13C a 12C sa však v skutočnosti líšia počtom neutrónov (7 vs. 6, pričom h je v kľúči zahrnutá).",

    # 160
    "Nuklidy 14_7N (14 - 7 = 7) a 13_6C (13 - 6 = 7) majú zhodne po 7 neutrónov (a), 12C/13C a 32S/34S sú izotopické páry (c) a jadrá 12_6C, 32_16S a 14_7N obsahujú zhodný počet protónov a neutrónov (d). Jadrovou reakciou ostreľovania stabilného fosforu 31P deuterónmi (jadrami 2H) vzniká rádioaktívny fosfor 32P podľa rovnice 31P + 2H -> 32P + 1H (e). Hliník 27Al má 14 neutrónov a fosfor 31P má 16 neutrónov (b), a izotop 32P je rádioaktívny (g).",

    # 161
    "Kovová väzba sa tvorí medzi atómami kovov v tuhom skupenstve (h) a možno ju popísať ako delokalizovanú kovalentnú väzbu (f). Je charakterizovaná mriežkou katiónov kovu obklopených spoločne zdieľaným voľne pohyblivým elektrónovým plynom (a), ktorý je priamou príčinou vysokej elektrickej a tepelnej vodivosti kovov (d). Vzniká medzi prvkami s nízkou elektronegativitou (b), nemá smerový charakter (e) a netvorí násobné väzby (c).",

    # 162
    "Medzimolekulové interakcie (van der Waalsove sily a vodíkové mostíky) sú rádovo slabšie než kovalentné väzby (g), no rozhodujúcim spôsobom určujú skupenstvo látok a ich fyzikálne konštanty, ako sú body topenia a varu (b, c). Vo farmakológii a biochémii sprostredkúvajú špecifickú väzbu liečiv na bunkové receptory a enzýmy (f). Zahŕňajú nielen van der Waalsove sily, ale aj vodíkové väzby (e, h) a pri prílišnom priblížení molekúl vykazujú aj odpudivú zložku (a).",

    # 163
    "V oxide sírovom (SO3) má centrálny atóm síry sterické číslo 3 bez voľného elektrónového páru, čo zodpovedá sp2 hybridizácii a planárnej trigonálnej geometrii s väzbovými uhlami 120° (b, h). Kostru molekuly tvoria tri σ väzby medzi sírou a kyslíkmi (c) a delokalizovaný π systém vznikajúci bočným prekrytím orbitálov (g). Molekula preto nie je lineárna (f) ani tetraedrická/sp3 (a).",

    # 164
    "Rovinné (planárne) usporiadanie molekúl sa typicky vysvetľuje sp2 hybridizáciou centrálneho atómu, ktorej tri hybridné orbitály zvierajú väzbové uhly 120° (a, h). Molekuly tak môžu mať tvar rovnostranného trojuholníka (napr. BF3, SO3) (f) alebo planárneho kruhu, ako je to pri aromatickom benzéne C6H6 (g). Molekula vody je lomená s hybridizáciou sp3 (b) a hybridné orbitály sp2 vznikajú zmiešaním jedného s a dvoch p orbitálov, nie naopak (e).",

    # 165
    "Iónová väzba je extrémne polárna interakcia medzi prvkami s veľkým rozdielom elektronegativít (Δχ > 1,7), založená na všesmerovom elektrostatickom priťahovaní opačne nabitých iónov, a preto nemá smerový charakter (d, h). Vyznačuje sa mimoriadnou pevnosťou v kryštálovej mriežke (b), no mechanický posun vrstiev spôsobí odpudzovanie súhlasných nábojov, čo je príčinou krehkosti iónových zlúčenín (a). Iónová väzba zásadne ovplyvňuje rozpustnosť v polárnych rozpúšťadlách (g).",

    # 166
    "Pre kryštalické látky neplatí, že ich geometrický tvar závisí od veľkosti, pretože vnútorné uhly kryštálu sú konštantné a dané kryštálovou sústavou bez ohľadu na veľkosť kryštálu (b). Chemické väzby medzi časticami priamo určujú vlastnosti kryštálu (c) a zďaleka nie všetky kryštály vedú elektrický prúd – mnohé molekulové a iónové v tuhom stave sú izolantmi (d, h). Naopak platí, že sú tvorené periodicky sa opakujúcou základnou bunkou, majú súmernosť a rozdeľujú sa na iónové, atómové a molekulové (a, e, f, g).",

    # 167
    "Molekulové kryštály sú tvorené samostatnými molekulami alebo atómami viazanými v uzloch mriežky slabými medzimolekulovými silami (van der Waals, vodíkové mostíky): patria sem tuhé vzácne plyny (c), chlór Cl2 (d), azán/amoniak NH3 (e) a metán CH4 (h). Naopak kamenná soľ NaCl (f) a KBr (g) tvoria typické iónové kryštály, a aragonit CaCO3 (a) i zafír Al2O3 (b) majú iónovo-koordinačnú pevnú štruktúru.",

    # 168
    "Atómové (kovalentné sieťové) kryštály sú tvorené sieťou atómov prepojených pevnými kovalentnými väzbami v celom objeme: príkladom je kremeň SiO2 a jeho odroda ametyst (a, e), sfalerit ZnS (h) a v klasifikácii testovnice UPJŠ aj rubín/korund Al2O3 (b). Naopak suchý ľad CO2 tvorí molekulový kryštál (f) a kalcit CaCO3 (c), modrá skalica (d) a KCl (g) sú kryštály iónové.",

    # 169
    "Iónové kryštály pozostávajú z pravidelne usporiadaných katiónov a aniónov viazaných elektrostatickou iónovou väzbou: kamenná soľ NaCl (c), kalcit CaCO3 (d), síran draselný K2SO4 (e) a fluorit CaF2 (f). Voda H2O v podobe ľadu (g) a vodík H2 (h) vytvárajú kryštály molekulové, a korund Al2O3 (a, b) patrí medzi kovalentné atómové mriežky.",

    # 170
    "Osovým prekrytím dvoch p orbitálov (orientovaných pozdĺž spojnice jadier) vzniká pevná kovalentná σ väzba (a). V komplexných zlúčeninách sa ligandy viažu na centrálny atóm koordinačnou (donorno-akceptorovou) väzbou (d), pričom soli s komplexnými iónmi vytvárajú iónové kryštály (e). Prítomnosť konjugovaných násobných väzieb v organických zlúčeninách umožňuje absorpciu viditeľného svetla a podmieňuje ich farebnosť (g). Vodíkové mostíky sú pre život kľúčové (b) a molekula s polárnymi väzbami môže byť vďaka symetrii nepolárna (h).",

    # 171
    "Dipólový moment väzby μ vzniká v dôsledku asymetrického rozloženia elektrónovej hustoty pri rozdielnej elektronegativite atómov (a), inhibícia predstavuje zníženie rýchlosti reakcie pôsobením inhibítorov (b) a ionizačná energia je energia nutná na odtrhnutie elektrónu z neutrálneho plynného atómu (c). Prijatím elektrónu nekovovým atómom za vzniku aniónu sa spravidla uvoľňuje energia (f). Katalyzátory ovplyvňujú rýchlosť reakcie, nie polohu chemickej rovnováhy (d), a prvky s nízkou ionizačnou energiou (s-prvky) sú najreaktívnejšie (e).",

    # 172
    "Vodíková väzba môže prepájať dve rôzne molekuly (intermolekulárna) alebo časti tej istej makromolekuly (intramolekulárna) (a). Tvorí sa medzi vodíkom viazaným na silne elektronegatívny atóm a voľným párom iného fluóru, kyslíka či dusíka, ako v HF, H2O a NH3 (d). V bielkovinách stabilizuje sekundárnu štruktúru (alfa-hélix a beta-skladaný list) (f) a významne zvyšuje teploty topenia a varu (g). Je podstatne slabšia než kovalentná väzba (c) a vzniká v silne polárnych, nie nepolárnych látkach (b).",

    # 173
    "Hybridizácia sp zahŕňa dva ekvivalentné hybridné orbitály zvierajúce uhol 180°, čo vedie k lineárnej geometrii molekúl (a) – takto hybridizovaný uhlík spôsobuje linearitu kyanovodíka H-C≡N (g). Všetky atómy uhlíka v alkánoch majú zhodnú tetraedrickú hybridizáciu sp3 (d), zatiaľ čo sp2 hybridizácia uhlíka v karbonylovej skupine (>C=O) podmieňuje jej rovinné usporiadanie (h). Hybridizácie sp2 a sp3 neposkytujú lineárnu geometriu (b, c, e).",

    # 174
    "Väzba π vzniká bočným prekrytím orbitálov (p-p, d-d alebo p-d) lokalizovaných kolmo na spojnicu jadier viazaných atómov (b, h). Na rozdiel od osovo symetrickej väzby σ nemá rotačnú symetriu okolo väzbovej osi, preto bráni voľnej rotácii (f). Bežne sa vyskytuje pri sp2 hybridizovaných atómoch uhlíka v alkénoch a arénoch ako zložka dvojitej väzby (g). Osovým prekrytím na spojnici jadier vzniká väzba σ, nie π (a).",

    # 175
    "Medzi slabé väzbové interakcie patria van der Waalsove sily (dipól-dipól, dipól-indukovaný dipól, disperzné sily) a vodíkové mostíky (c). Tieto interakcie determinujú vzájomné priťahovanie molekúl, umožňujú tvorbu supramolekulových komplexov (h) a dipólové sily vysvetľujú rozpustnosť polárnych látok v polárnych rozpúšťadlách podľa princípu 'podobné sa rozpúšťa v podobnom' (d, e). Disperzné a hydrofóbne sily k slabým interakciám patria (a) a uplatňujú sa aj pri kontakte polárnych a nepolárnych molekúl (g).",

    # 176
    "Vodíkový mostík vzniká elektrostatickou interakciou kladne polarizovaného atómu vodíka s voľným elektrónovým párom silne elektronegatívneho malého atómu (O, F, N) a označuje sa bodkovanou čiarou (...): O...H, F...H a N...H (b, e, h). Zápisy s plnou čiarou ako F-H, C-H či N-H predstavujú intramolekulárne kovalentné väzby, nie medzimolekulové vodíkové mostíky (a, c, d).",

    # 177
    "Väzbová energia je energia, ktorá sa uvoľní pri vzniku väzby z izolovaných atómov (resp. potrebná na jej rozštiepenie), a je priamou mierou pevnosti chemickej väzby – čím je vyššia, tým je väzba pevnejšia (a, e). S rastúcou násobnosťou väzby jej hodnota stúpa, preto v uvedenom rade rastie od jednoduchej väzby v Cl-Cl (~242 kJ/mol) cez dvojitú v O=O (~498 kJ/mol) až po trojitú v N≡N (~945 kJ/mol) (g). Väzbová energia sa nerovná elektronegativite (f) a pre danú dvojatómovú molekulu zodpovedá disociačnej energii (c, d).",

    # 178
    "Van der Waalsove sily patria medzi slabé medzimolekulové interakcie elektrostatickej podstaty pôsobiace medzi neutrálnymi molekulami, polárnymi časticami aj iónmi vo všetkých troch skupenstvách látok (a, b, c). Najslabšou zložkou sú disperzné (Londonove) sily vyvolané fluktuáciami elektrónovej hustoty a vznikom okamžitých indukovaných dipólov (d). Nepatria sem iónové väzby medzi aniónmi a katiónmi (e) ani koordinačné väzby (f), a primárnu štruktúru bielkovín udržiavajú pevné kovalentné peptidové väzby (g).",

    # 179
    "Koordinačná (donorno-akceptorová) väzba vzniká tak, že obidva väzbové elektróny poskytuje jeden atóm (donor) s voľným elektrónovým párom a druhý atóm (akceptor) poskytuje prázdny (vakantný) orbitál (g, h). Typickým príkladom je vznik amónneho katiónu NH4+ interakciou voľného páru dusíka v NH3 s protónom H+ (d) a tvorba komplexného katiónu [Al(H2O)6]3+ (b). Hoci má kovalentný charakter, líši sa mechanizmom vzniku (a), nevyskytuje sa v uhľovodíkoch (f) a bór ako prvok druhej periódy nemôže vytvoriť komplex [BF6]3- kvôli absencii d-orbitálov (c, e).",

    # 180
    "Molekula je polárna, ak má v dôsledku prítomnosti polárnych väzieb a asymetrického geometrického tvaru nenulový celkový dipólový moment: patria sem karboxylové kyseliny s vysoko polárnou skupinou -COOH (a), dusíkaté bázy DNA (d), amoniak NH3 s trigonálne pyramídovou štruktúrou (e) a etanol CH3-CH2-OH s lomenou polárnou väzbou C-O-H (g). Metán CH4 je nepolárny tetraéder (f), a oficiálny kľúč UPJŠ LF pri tejto otázke špecificky vymedzuje možnosti a, d, e, g.",

    # 181
    "Vodíkové mostíky medzi vlastnými molekulami sa môžu tvoriť len vtedy, ak zlúčenina obsahuje vodík viazaný na silne elektronegatívny heteroatóm (O, N, F): to spĺňajú karboxylové kyseliny (a), voda H2O (b), dusíkaté bázy nukleových kyselín (d), amoniak NH3 (e) a etanol (g). Dimetyléter (c) ani acetón (h) nemajú vodík na kyslíku (chýba donor protónu), takže medzi sebou vodíkové mostíky netvoria, a metán CH4 (f) je nepolárny uhľovodík.",

    # 182
    "Halogény v halogénvodíkoch majú 7 valenčných elektrónov – jeden tvoriaci jednoduchú kovalentnú väzbu s vodíkom a tri nezdieľané (voľné) elektrónové páry, čo platí pre HBr (b) aj chlorovodík HCl (d), a v kontexte testovnice sem spadá aj halogenid NaCl (g). Voda má 2 voľné páry na kyslíku (c), amoniak a fosfán majú po 1 voľnom páre na centrálnom atóme (a, e), dusík N2 má 2 voľné páry celkovo (f) a molekula H2 nemá žiadny voľný pár (h).",

    # 183
    "Iónové zlúčeniny sú tvorené pevnou kryštálovou mriežkou opačne nabitých iónov, čo podmieňuje ich vysoké teploty topenia a varu (e) a dobrú rozpustnosť v polárnych rozpúšťadlách, ako je voda, vďaka hydratácii iónov (d). Pri mechanickom tlaku dochádza k posunu vrstiev a odpudzovaniu súhlasných nábojov, čo spôsobuje ich krehkosť a štiepateľnosť (f). V roztokoch a taveninách sú ióny voľne pohyblivé, vďaka čomu výborne vedú elektrický prúd ako elektrolyty (h). Nízke teploty topenia (b) ani nevodivosť roztokov (g) pre ne neplatia.",

    # 184
    "V kyanovodíku H-C≡N sa atóm uhlíka nachádza v stave sp hybridizácie (f), čo určuje lineárnu geometriu celej molekuly s väzbovým uhlom 180° (d). Väzba C-H je jednoduchá σ väzba a trojitá väzba C≡N pozostáva z jednej σ a dvoch kolmých π väzieb, molekula teda celkovo obsahuje dve σ a dve π väzby (b). Uhlík nie je sp2 hybridizovaný (a), nemá rovinný trojuholníkový tvar (h) a jednotlivé väzby nie sú energeticky rovnocenné (g).",

    # 185
    "Nepolárna kovalentná väzba vzniká medzi atómami s nulovým alebo zanedbateľným rozdielom elektronegativít (Δχ < 0,4): v homonukleárnych molekulách Cl2 (c), H2 (d) a O2 (g) je Δχ = 0, a vo fosfáne PH3 je väzba nepolárna, pretože elektronegativita fosforu (2,19) a vodíka (2,20) je prakticky identická (h). V molekulách NH3, H2O a HCl je rozdiel elektronegativít vyšší, takže väzby sú polárne (a, b, e), a v NaCl je väzba iónová (f).",

    # 186
    "Väzba π sa nevyskytuje v nasýtených molekulách obsahujúcich výlučne jednoduché σ väzby: amoniak NH3 (d), sulfán H2S (f), metán CH4 (g) a bróm Br2 (h). Naopak molekuly CO2 (O=C=O) (a), CO (C≡O) (b), kyanovodík HCN (H-C≡N) (c) a dusík N2 (N≡N) (e) obsahujú násobné väzby, ktorých neoddeliteľnou súčasťou sú práve π väzby.",

    # 187
    "Iónová väzba vzniká medzi elektropozitívnymi kovmi s nízkou elektronegativitou a nekovmi s vysokou elektronegativitou, kde rozdiel Δχ presahuje hodnotu 1,7: patrí sem oxid bárnatý BaO (a), fluorid lítny LiF (c), oxid vápenatý CaO (e) a bromid draselný KBr (f). Karbid kremíka SiC (b) a nitrid bóru BN (g) sú kovalentné atómové látky s pevnou sieťovou štruktúrou, Br2 je homonukleárna nepolárna molekula (d) a jodovodík HI je polárna kovalentná zlúčenina (h).",

    # 188
    "Centrálny atóm dusíka v amoniaku NH3 podlieha neekvivalentnej sp3 hybridizácii, pri ktorej jeden zo štyroch hybridných orbitálov obsadzuje voľný elektrónový pár (a, h). Tento voľný pár odpudzuje väzbové elektrónové páry väzieb N-H, čím molekula nadobúda tvar trigonálnej pyramídy (e). Vďaka tejto asymetrickej priestorovej geometrii sa dipólové momenty jednotlivých väzieb N-H v priestore neanulujú a amoniak vykazuje výrazný permanentný dipól.",

    # 189
    "Molekula nie je polárna, ak je homonukleárna (O2, b) alebo ak je vysoko symetrická, takže sa dipólové momenty jednotlivých polárnych väzieb vektorovo navzájom rušia: lineárny acetylén H-C≡C-H (c), tetraedrický tetrachlórmetán CCl4 (f) a lineárny oxid uhličitý O=C=O (g). Naopak chlorovodík HCl (a), trichlórmetán CHCl3 (e) a lomená molekula vody H2O (h) sú asymetrické a majú stály dipólový moment.",

    # 190
    "Kovalentná chemická väzba je založená na vytvorení a zdieľaní spoločného elektrónového páru medzi dvoma atómami (c), pričom jednoduchá kovalentná väzba je typická pre nasýtené uhľovodíky – alkány (h). Dvojité väzby môžu byť v reťazci konjugované, čo znamená, že sa pravidelne striedajú s jednoduchými väzbami (b), a väzba spájajúca aminokyseliny v reťazcoch peptidov a bielkovín je kovalentná peptidová väzba -CO-NH- (g). Väzba nevzniká pôsobením gravitačných ani magnetických síl (e, f) a na jej tvorbe sa bežne podieľajú aj orbitály p a d (d).",

    # 191
    "Vznik vodíkových mostíkov nemožno očakávať pri nepolárnych uhľovodíkoch, ako sú metán CH4 (c) a propán (h), pretože uhlík nemá dostatočnú elektronegativitu. Pri dietyléteri (f) chýba donor vodíka (vodík priamo viazaný na kyslík) a pri plynnom HCl (e) je atóm chlóru príliš objemný s rozptýleným nábojom na tvorbu klasických silných vodíkových mostíkov. Naopak etanol (a), HF (b), NH3 (d) aj bielkovina inzulín (g) tvoria intenzívne vodíkové väzby.",

    # 192
    "S narastajúcou násobnosťou kovalentnej väzby sa vzdialenosť medzi jadrami zmenšuje (dĺžka väzby klesá) (b) a väzbová energia úmerne rastie (c). Pre väzby medzi atómami dusíka to presne dokumentujú hodnoty: disociačná energia trojitej väzby N≡N je vysoká (cca 941 kJ/mol) oproti jednoduchej N-N (cca 167 kJ/mol) (g), a dvojitá väzba N=N vykazuje strednú hodnotu okolo 376 kJ/mol v porovnaní so 167 kJ/mol pri jednoduchej väzbe (h).",

    # 193
    "Atómové (kovalentné sieťové) kryštály sú charakterizované trojrozmernou sieťou pevných kovalentných väzieb medzi atómami v celej mriežke (a), príkladom čoho je diamant, karbid kremíka SiC, sfalerit ZnS či CuCl (c). V dôsledku vysokej mriežkovej energie existujú za bežných podmienok (laboratórna teplota a tlak) výhradne v tuhom stave, rovnako ako iónové kryštály (d, f). Látky ako CO2, Br2 či I2 vytvárajú molekulové kryštály (h) a vzácne plyny majú molekulovú, nie sieťovú kovalentnú štruktúru (e).",

    # 194
    "V tejto testovej otázke možnostiam zodpovedá teória hybridizácie orbitálov: zmiešaním jedného orbitálu s a jedného orbitálu p vznikajú dva hybridné orbitály sp s lineárnym usporiadaním (a). Hybridizáciou jedného s a dvoch p orbitálov vznikajú tri hybridné orbitály sp2 s rovinným usporiadaním (d), a kombináciou jedného s a troch p orbitálov vznikajú štyri hybridné orbitály sp3 s priestorovým tetraedrickým usporiadaním (e). Podľa oficiálneho kľúča UPJŠ LF sú označené možnosti a, c, d, e.",

    # 195
    "Lineárnou kombináciou jedného orbitálu s a jedného p vznikajú dva sp orbitály s lineárnym tvarom (180°) (a), zmiešaním jedného s a dvoch p vznikajú tri sp2 orbitály s rovinným usporiadaním (120°) (d) a kombináciou jedného s a troch p vznikajú štyri priestorovo tetraedricky orientované orbitály sp3 (109,5°) (e). Hybridizácia s a p orbitálov je základným modelom vysvetľujúcim tvar a rovnocennosť väzieb v organických zlúčeninách; oficiálny kľúč UPJŠ LF pri tejto otázke zahŕňa možnosti a, d, e, h.",

    # 196
    "Lineárne molekuly majú atómy usporiadané v priamke a ich väzbový uhol je presne 180° (g), čo sa pri viacatómových molekulách vysvetľuje sp hybridizáciou centrálneho atómu (c). Lineárny tvar majú všetky dvojatómové molekuly (napr. Cl2, HI, CO) a vybrané viacatómové molekuly s sp hybridizáciou bez voľných elektrónových párov na centrálnom atóme, ako sú BeCl2 a CO2 (b, f). Voda H2O a amoniak NH3 sú nelineárne (lomená a pyramídová geometria) s hybridizáciou sp3 (a, d).",

    # 197
    "Hybridné orbitály vznikajú matematickým miešaním energeticky blízkych atómových orbitálov (napr. s a p), pričom od pôvodných orbitálov sa líšia tvarom (majú jeden lalok výrazne zväčšený) (a), priestorovou orientáciou (c), spriemerovanou energetickou hladinou (d) a asymetriou vzhľadom na jadro (g). Ich celkový počet sa však vždy rovná počtu pôvodných atómových orbitálov vstupujúcich do hybridizácie (b).",

    # 198
    "Molekula BF3 je vďaka sp2 hybridizácii bóru planárna a dokonale symetrická s uhlami 120°, takže jej celkový dipólový moment je nulový (a). Molekula H2S má lomený tvar s dvoma voľnými pármi na síre analogicky ako molekula vody (b). V molekulách metánu (CH4) aj amoniaku (NH3) je elektrónová hustota usporiadaná do tetraédra (sp3), avšak prítomnosť voľného elektrónového páru na dusíku v NH3 deformuje väzbové uhly na cca 107° v porovnaní so 109,5° pri CH4 (e). Karbonylová skupina má sp2 hybridizovaný uhlík, čo určuje jej rovinný tvar (f).",

    # 199
    "Pri dvojatómových molekulách je dipólový moment priamym ukazovateľom polarity väzby (a). Pri vysoko symetrických molekulách ako CS2, CH4, CO2 a BF3 sa väzbové dipóly vektorovo rušia, takže celkový dipólový moment CO2 aj BF3 je nulový (rovnaký) (c, g). Z fyzikálneho hľadiska ide o vektorovú veličinu charakterizujúcu asymetriu náboja v molekule (h), pričom viacatómová molekula je vektorovým súčtom, nie rozdielom, dipólových momentov všetkých väzieb (b).",

    # 200
    "Rozdiel elektronegativít medzi chlórom a vodíkom je Δχ = 3,0 - 2,1 = 0,9, čo leží v intervale 0,4 až 1,7 charakteristickom pre polárnu kovalentnú väzbu, ktorá je jednoduchá a sprostredkovaná jedným spoločným elektrónovým párom (b, d, f, h). Väzba v molekule chlorovodíka preto určite nie je nepolárna kovalentná (a), iónová (c), vodíková (e) ani kovová (g)."
]

# Load batch_4.json
with open('scripts/chem_batches/batch_4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} questions from batch_4.json")
print(f"Number of explanations prepared: {len(explanations)}")
assert len(data) == len(explanations), "Mismatch in questions and explanations count!"

for i, q in enumerate(data):
    q['explanation'] = explanations[i]

# Save to scripts/chem_batches/batch_4_explained.json
with open('scripts/chem_batches/batch_4_explained.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved scripts/chem_batches/batch_4_explained.json successfully.")

# Verification
with open('scripts/chem_batches/batch_4_explained.json', 'r', encoding='utf-8') as f:
    saved = json.load(f)

print(f"Verification: {len(saved)} items loaded.")
assert len(saved) == 50

for idx, item in enumerate(saved):
    exp = item.get('explanation', '')
    assert exp and len(exp) > 50, f"Question {idx+1} has invalid explanation!"
    assert not exp.startswith("Správne odpovede podľa oficiálneho kľúča"), f"Question {idx+1} explanation was not replaced!"

print("All 50 questions have verified new explanations!")
print("\n--- Sample Question 151 ---")
print("Content:", saved[0]['content'])
print("Explanation:", saved[0]['explanation'])
print("\n--- Sample Question 152 ---")
print("Content:", saved[1]['content'])
print("Explanation:", saved[1]['explanation'])
