# -*- coding: utf-8 -*-
import json

explanations = {
    51: "Správne pomenovania kyselín síry sú: H2S2O8 je kyselina peroxodisírová (c), H2S2O7 je kyselina disírová (d), H2SO6 je kyselina diperoxosírová (f) a H2S2O9 je kyselina diperoxodisírová (h). Vzorec H2SO5 patrí kyseline peroxosírovej (Caroovej kyseline), nie peroxosiričitej (a), vzorec H2SO je neúplný (b) a H2S2O7 je disírová a nie peroxodisiričitá (e).",

    52: "Správne systematické názvy a vzorce hydridov p-prvkov sú AsH3 – arzán (c), GeH4 – germán (d), H2Se – selán (e) a PH3 – fosfán (f). Vzorec fosfánu sa štandardne zapisuje ako PH3 a nie H3P (a), alan má vzorec AlH3 (b), pre selán je správny vzorec H2Se a nie SeH2 (g) a sulfán má stechiometriu H2S, nie HS2 (h).",

    53: "Vzorce neodpovedajú zadaným názvom v možnostiach a, c, d, h. Nitrid kremičitý má stechiometrický vzorec Si3N4, nie SiN4 (a); arzenid lítny pozostáva z katiónov Li+ a aniónu As3-, teda Li3As, nie LiAs3 (c); azid olovnatý obsahuje azidový anión N3-, preto má vzorec Pb(N3)2, kým Pb3N2 je nitrid olovnatý (d); a antimonid hlinitý má pomer prvkov 1:1, teda AlSb (h). Zlúčeniny GaAs, Mg3P2, CaC2 a Si3N4 sú zapísané správne.",

    54: "Vzorce neodpovedajú uvedeným zlúčeninám v možnostiach d, f, g, h. Hydroxid draselno-chromitý KCr(OH)4 vyžaduje štyri hydroxidové anióny na kompenzáciu nábojov K+ a Cr3+, vzorec KCr(OH)2 nie je elektroneutrálny (d); Cs3CoCl6 nevychádza nábojovo pre kobaltnatý katión Co2+ (f); oxid-sulfid uhličitý má vzorec COS, nie COS2 (g); chlorid-oxid fosforečný má vzorec POCl3, zatiaľ čo PCl5O by prekračoval maximálnu väzbovosť fosforu (h). Možnosti a, b, c, e uvádzajú korektné podvojné a zmiešané soli.",

    55: "Správne pomenovania a vzorce kyselín sú: HOCN – kyselina kyanatá (a), H6Si2O7 – kyselina heptaoxodikremičitá (b), H3BO3 – kyselina trioxoboritá (c) a H2S2O5 – kyselina dihydrogendisiričitá (d). Kyselina HBrO4 je tetraoxobromistá, nie brómična (e); H6TeO6 je kyselina hexaoxotelúrová s Te(VI), nie telúričitá (f); kyselina tetraoxokremičitá má vzorec H4SiO4, nie HSiO4 (g); a kyselina tetrahydrogendifosforitá je H4P2O5 (h).",

    56: "Správne vzorce a názvy hydrátov solí sú v možnostiach a, e, g, h: Na2SO4·10H2O (dekahydrát síranu sodného), (NH4)2Fe(SO4)2·6H2O (hexahydrát síranu amónno-železnatého – Mohrova soľ), CaSO4·1/2H2O (hemihydrát síranu vápenatého – pálená sadra) a Na2Mg(CO3)2·10H2O (dekahydrát uhličitanu horečnato-sodného). V možnosti b predpona undeka- označuje 11 (pričom vzorec má 12 H2O – dodekahydrát), v d predpona dodeka- nezodpovedá 11 molekulám vody a vo f chýba správny pomer pre chloristan bárnatý Ba(ClO4)2·3H2O.",

    57: "Vzorce neodpovedajú uvedeným názvom v možnostiach b, c, d, f. V K2[PtBr6] má platina oxidačné číslo +IV, preto ide o hexabromoplatičitan draselný (nie platnatan) a predpona „didraselný“ je v anorganickom názvosloví nesprávna (b); vzorec v c nezodpovedá dikyano-hydroxozlatitanu sodnému (nábojové pomery nevychádzajú); komplex v d nezodpovedá hexahydroxo-karbonylciničitanu; v f má mangán v anióne [MnF6]2- oxidačné číslo +IV, ide teda o hexafluoromanganičitan, nie manganičnan (+V) (f).",

    58: "Správne pomenované kyslé soli (hydrogénsoli) sú Sr(H2PO3)2 – dihydrogenfosforitan strontnatý (c), CsHMoO4 – hydrogenmolybdenan cézny (d), Li2HVO4 – hydrogenvanadičnan lítny (e) a Ag2HIO5 – hydrogenjodistan strieborný (g). Hydrogensulfid vápenatý má vzorec Ca(HS)2, pretože vápnik tvorí dvojmocný katión Ca2+ (a); v b je neúplný vzorec tetraboritanu; v f nie je zlúčenina elektroneutrálna (K+ a Fe3+ vyžadujú 4 anióny HCO3-); v h je anión H2AsO4- dihydrogenarzeničnanový, nie arzenitanový.",

    59: "Tetrachloro-paladnatan amónny má sumárny vzorec (NH4)2[PdCl4], kde centrálnym atómom je paládium Pd(II) a koordinačné číslo je 4 dané štyrmi monodentátnymi chloridovými ligandomi Cl- (e, f, g, h). Komplexný anión [PdCl4]2- nesie nábojové číslo -2. Centrálny atóm je akceptorom (nie donorom) voľných elektrónových párov (b), amónny katión NH4+ patrí do vonkajšej sféry a nie je ligandom (c), a vzorec v d uvádza platinu namiesto paládia.",

    60: "Hexakyanochromitan hexaamminkobaltitý je koordinačná zlúčenina zložená z komplexného katiónu [Co(NH3)6]3+ a komplexného aniónu [Cr(CN)6]3-, jej vzorec je preto [Co(NH3)6][Cr(CN)6] (f). Komplexný anión nesie nábojové číslo -3 (b), koordinačné čísla oboch komplexných iónov sú rovnaké a rovnajú sa 6 (c) a oba centrálne atómy Co i Cr majú zhodné oxidačné číslo +III (g). Ligandy CN- nie sú elektroneutrálne ale aniónové (e) a centrálnym atómom katiónu je Co, nie Cr (d).",

    61: "Vzorce neodpovedajú zadaným názvom v možnostiach a, b, c, e. Zápis NiCO3·6H2O predstavuje hydrát uhličitanu nikelnatého a nie koordinačný komplex [Ni(H2O)6]CO3 (a); vzorec Zn(SiO3)2 obsahuje zinok a nie zirkón, takže ide o kremičitan zinočnatý (b); v c vzorec nezodpovedá triammin-trichloronikelnatému komplexu; v e vzorec Ba(TlO4)2 obsahuje tálium a nie telúr (telúran bárnatý je BaTeO4). Zlúčeniny SrWO4, Na2S2O8, Pb2P2O7 a NH4[IrCl5] zodpovedajú svojim názvom (d, f, g, h).",

    62: "Chróm dosahuje oxidačné číslo +VI v chromanoch, dichromanoch a oxide chrómovom: PbCrO4 (chróman olovnatý, a), CrO3 (oxid chrómový, c), Na2CrO4 (chróman sodný, d) a K2Cr2O7 (dichróman draselný, f). V K2CrO3 a (NH4)2CrO3 má chróm oxidačné číslo +IV (b, h), neutrálny oxid Cr2O7 neexistuje (e) a vo Fe(CrO2)3 (chromitan železitý) má chróm oxidačné číslo +III (g).",

    63: "Fosfor má oxidačné číslo +III v bromide fosforitom PBr3 (a), v hydrogenfosforitanoch odvodených od dvojsýtnej kyseliny fosforitej H2(HPO3): (NH4)2HPO3 (c) a CaHPO3 (e), a v kyanide fosforitom P(CN)3 (g). V KH2PO2 (fosfornan) má fosfor oxidačné číslo +I (b), vo FePO4 a HPO3 (fosforečnany) má +V (d, f) a vo fosfáne PH3 má -III (h).",

    64: "Vodík má vo väčšine kovalentných a iónových zlúčenín oxidačné číslo +I, napríklad v hydrogenuhličitane NaHCO3 (b) alebo v amoniaku NH3 (f, kde je dusík elektronegatívnejší). V hydridoch alkalických kovov (LiH) vystupuje ako hydridový anión H- s oxidačným číslom -I (d), a ako voľný dvojatómový plyn H2 v elementárnom stave má oxidačné číslo 0 (g). Oxidačné číslo -III vodík netvorí (v PH3 má +I, a), v H2O2 má +I (c) a trícium je iba rádioaktívny izotop vodíka 3H (h).",

    65: "Kyslík sa v zlúčeninách najčastejšie vyskytuje v oxidačnom čísle -II, ako napríklad v bežných oxidoch vrátane oxidu fosforečného P2O5 (f). V peroxidoch obsahujúcich peroxydickú väzbu -O-O- (napr. Na2O2) má oxidačné číslo -I (d) a vo väzbe s elektronegatívnejším fluórom v difluoride kyslíka OF2 dosahuje kladné oxidačné číslo +II (c). Hodnoty -III, +I, +IV či +VI kyslík v uvedených zlúčeninách nenadobúda (napr. vo Fe2O3 má -II a v hydróniovom katióne H3O+ má taktiež -II).",

    66: "Bróm môže nadobúdať rôzne oxidačné čísla v rozsahu od -I do +VII: +I v oxide brónnom Br2O (b), +V v kyseline bromičnej HBrO3 (c), -I v bromovodíku HBr (e), +VII v bromistane draselnom KBrO4 (f) a 0 v elementárnom kvapalnom bróme Br2 (g). V KBrO3 má bróm oxidačné číslo +V, nie +III (a), a v bromidoch kovov ako CuBr2 či PbBr4 má bróm vždy oxidačné číslo -I (d, h).",

    67: "Chlór vystupuje v oxidačnom čísle +VII v chloristanoch ako NaClO4·H2O (a), +I v oxide chlórnom Cl2O (b), -I v chloridoch kovov ako MnCl2 (d) a +IV v oxide chloričitom ClO2 (f). V NaClO má chlór oxidačné číslo +I, nie +III (e); v AlCl3 má chlór -I, nie -III (h); záporné oxidačné čísla -II a -III chlór v bežných anorganických zlúčeninách netvorí (c, g).",

    68: "Železo má oxidačné číslo +III v oxide-hydroxide železitom FeO(OH) (a), v komplexe hexaaquaželezitého chloridu [Fe(H2O)6]Cl3 (c), vo fosforečnane železitom FePO4 (e) a v podvojnom oxide FeO·Fe2O3 (magnetit, Fe3O4), kde sú dva z troch atómov Fe v oxidačnom stave +III (g). V zlúčeninách K4[Fe(CN)6], Fe(HCO3)2, Fe(ClO4)2 a Fe(NO3)2 má železo oxidačné číslo +II (b, d, f, h).",

    69: "Prvok s oxidačným číslom +III sa nachádza v Bi(OH)2NO3 (bizmut Bi+III, a), v oxide fosforitom P4O6 (fosfor P+III, b), v komplexe [CrBr2(H2O)4]NO2 (chróm Cr+III kompenzovaný dvoma Br- a jedným NO2-, e) a v kyseline metaboritej HBO2 (bór B+III, h). V NH3 má dusík oxidačné číslo -III (c), v Na4[CoF6] má kobalt +II (d), v tioarzeničnane Na3[AsS4] má arzén +V (f) a v H2PtCl6 má platina +IV (g).",

    70: "Fosfor má oxidačné číslo +V v kyselinách fosforečných: HPO3 (kyselina metafosforečná, b), H4P2O7 (kyselina difosforečná, g) a H3PO4 (kyselina trihydrogenfosforečná, v texte preklep HsPO4, h). Vzorec chlórnanu sodného je NaClO a nitrid hlinitý je AlN (katión Al3+ a nitridový anión N3-). Možnosti a, c, d, e, f obsahujú nesprávne stechiometrické vzorce týchto látok ako Na2ClO, Na2ClO2, AlN3 či neexistujúce kyseliny fosforu.",

    71: "Pri postupnej neutralizácii trojsýtnej kyseliny fosforečnej H3PO4 hydroxidom vápenatým Ca(OH)2 vznikajú podľa látkového pomeru reaktantov tri rôzne soli: dihydrogenfosforečnan vápenatý Ca(H2PO4)2 (c), hydrogenfosforečnan vápenatý CaHPO4 (b) a terciárny fosforečnan vápenatý Ca3(PO4)2 (g). Ostatné kombinácie vzorcov (a, d, e, f, h) nezodpovedajú oxidačným číslam iónov Ca2+, H2PO4-, HPO4(2-) a PO4(3-).",

    72: "Správne pomenovania a vzorce oxidov dusíka sú: N2O4 je dimér oxidu dusičitého NO2 (a), N2O5 je oxid dusičný (b), N2O je oxid dusný (c) a NO2 je oxid dusičitý (f). V možnosti d je NO2 chybne označený ako dioxid dusnatý, N2O3 je oxid dusitý a nie dusnatý (e), a N2O4 je dimérom oxidu dusičitého, nie dusnatého (h).",

    73: "Oxidačné číslo +II má zinok v zinočnatanovom anióne [ZnO2]2- (b), železo v kyanokomplexe (c), meď v komplexe [Cu(CN)4]2- (f) a bárium ako katión Ba2+ v peroxide bárnatom BaO2 (g). V mangananovom anióne [MnO4]2- a chrómanovom [CrO4]2- majú centrálne kovy oxidačné číslo +VI (a, e), a vo fosforečnanoch má fosfor oxidačné číslo +V (h).",

    74: "Správny vzorec a názov majú BiClO – chlorid-oxid bizmutitý (a), H3PO2 – kyselina trihydrogenfosforná (v staršom názvosloví, b), Mg(BO2)2 – boritan horečnatý (metaboritan, d) a TeF6 – fluorid telúrový (h). Fosforečnan horečnato-amónny má vzorec MgNH4PO4 bez atómu vodíka (c), tetrachloropaladnatan amónny vyžaduje dva katióny amónne (NH4)2[PdCl4] (e), H4SiO4 je kyselina kremičitá a nie kremičná (f) a SiC je karbid kremičitý (g).",

    75: "Správne pomenovania a vzorce kyselín sú H3AsO3 – kyselina trioxoarzenitá (b), H2TeO3 – kyselina telúričitá (c), H5IO6 – kyselina pentahydrogenjodistá (e) a H4P2O7 – kyselina tetrahydrogendifosforečná (g). HPO3 je kyselina metafosforečná a nie fosforitá (d), HClO4 je kyselina chloristá a nie chlorečná (f), a kyselina disírová má vzorec H2S2O7, nie H2S2O5 (h).",

    76: "Správne pomenované soli sú Mg3(PO4)2 – fosforečnan trihorečnatý (c), KClO2 – chloritan draselný (d), Cu(ClO4)2 – chloristan meďnatý (g) a Ag2Se – selenid strieborný (h). Dichróman cézny má vzorec Cs2Cr2O7 (a), anión BrO- je chlórnanový analóg (brómnan draselný by bol KBrO, nie K2BrO, b), disíran amónny je (NH4)2S2O7 (e) a manganistan sodný je NaMnO4 s oxidačným číslom Mn(VII), nie Na3MnO4 (f).",

    77: "Podľa kľúča testovnice UPJŠ LF sú označené možnosti b, c, e, g. Zlúčeniny FeCl(OH)2 (b) a K[Au(OH)4] (g) obsahujú hydroxidové anióny OH-, [Cu(NH3)4]SO4·H2O je hydrát amminokomplexu medi (c) a NaTl(NO3)2 predstavuje podvojnú soľ (e). Tieto možnosti boli v danom testovom zadaní vyhodnotené ako správne podľa autorizovaného kľúča.",

    78: "Zmiešané a podvojné soli obsahujú viac ako jeden druh katiónu alebo aniónu: (NH4)2Pb(SO4)2 je podvojná soľ s dvoma rôznymi katiónmi (a), FeCl(OH)2 je zásaditá zmiešaná soľ s chloridovými a hydroxidovými aniónmi (b), NaTl(NO3)2 (e) a KCr(SO4)2 (chrómovo-draselný kamenec, f) sú podvojné soli dvoch kovov. Možnosti c a g sú koordinačné zlúčeniny, d je hydrogensoli KHS a h je oxid-chlorid bizmutitý.",

    79: "Zlúčeniny, ktoré nepatria medzi oxidy, sú Cs2H2SiO4 (hydrogénkremičitan, b), Ca(H2PO2)2 (fosfornan, c), BeHSe (hydrogenselenid, g) a (NH4)2ClO3 (h). Zlúčeniny v možnostiach a, d, e, f nesú názvy oxokyselín a ich solí s oxo-názvoslovím, kým možnosti b, c, g, h predstavujú iné typy anorganických solí a hydridov.",

    80: "Správne priradenie vzorca a názvu tej istej zlúčeniny predstavujú: Ca(H2PO2)2 – dihydrogenfosfornan vápenatý (c), Al(HSiO3)3 – hydrogentrioxokremičitan hlinitý (d), Mg(H2PO4)2 – dihydrogentetraoxofosforečnan horečnatý (e) a Ca(AsO2)2 – bis(arzenitan) vápenatý (f). V a nesedí oxidačné číslo a stechiometria (dioxofosforitan), v b je vzorec Cs2H2SiO4 skomolený, v g hydrogenselenid berýlnatý vyžaduje Be(HSe)2 a v h chlorečnan amónny má vzorec NH4ClO3, nie (NH4)2ClO3.",

    81: "Správne tvrdenia sú: K3PO4 je fosforečnan draselný (a), H2Si2O5 je kyselina dihydrogendikremičitá (d), Ca2Al(OH)7·H2O je hydrát heptahydroxidu divápenato-hlinitého (f) a Ca5F(PO4)3 je fluoroapatit – fluorid-tris(fosforečnan) pentavápenatý (h). V b je Pb(NO3)2 dusičnan olovnatý (nie dusitan), v c má chlorečnan strieborný vzorec AgClO3 (nie Ag2ClO3), v e je Fe(SCN)2 tiokyanatan železnatý (nie železitý) a v g je BaMnO4 mangánan bárnatý s Mn(VI), nie manganistan (MnVII).",

    82: "Nesprávne (chybné) tvrdenia sú v možnostiach a, b, e, g. Vzorec dusičnanu sodno-draselného vyžaduje dva dusičnanové anióny: NaK(NO3)2 (a); HgCl je chlorid ortuťný, nie dichlorid (b); K[Cr(OH)4] je tetrahydroxochromitan draselný, nie „hydroxid chromito-draselný“ (e); a BaO2 je peroxid bárnatý, nie oxid baričitý (g). Tvrdenia c, d, f, h uvádzajú správne pomenované zlúčeniny.",

    83: "Nesprávne pomenované zlúčeniny sú v možnostiach c, d, f, h. Zlúčenina CaHPO3 je hydrogenfosforitan vápenatý, nie hydrogenfosfornan (c); Na2S2O7 je disíran sodný, nie peroxosíran (d); KCr(SO4)2·12H2O je dodekahydrát síranu draselno-chromitého, nie dekahydrát (f); a Na2S2O3 je tiosíran sodný, nie disíran (h). Možnosti a, b, e, g uvádzajú správne názvy a vzorce.",

    84: "Vzorce nezodpovedajú uvedeným názvom v možnostiach a, d, e, g. V HAuCl4 má zlato oxidačné číslo +III, preto ide o kyselinu tetrachlorozlatitú (nie zlatnatú, a); Na2B4O7·10H2O je dekahydrát tetraboritanu sodného (bórax), nie dodekahydrát (d); vzorec H5IO6 patrí kyseline jodistej s I(VII), nie jodičnej (e); a SiC je karbid kremičitý (karborundum), pričom silán má vzorec SiH4 (g). Možnosti b, c, f, h uvádzajú správne vzorce.",

    85: "Správne pomenovania a vzorce komplexných zlúčenín sú: [Ni(NH3)6]Cl2 – chlorid hexaamminnikelnatý (a), [Ni(H2O)6](ClO4)2 – chloristan hexaakvanikelnatý (d), [CuCl2(H2O)2] – diakva-dichloromeďnatý komplex (f) a [Al(H2O)3(OH)3] – triakva-trihydroxohlinitý komplex / hydroxid (g). V b je NO3- dusičnan, nie dusitan; v c je (NH4)3[Co(NO2)6] hexanitrokobaltitan amónny, nie amónno-; a v h je HAuCl4 kyselina tetrachlorozlatitá s Au(III), nie zlatitá vo forme HAuCl4 s iným zápisom.",

    86: "Správne pomenované zlúčeniny a vzorce sú: BN – nitrid boritý (b), H5IO6 – kyselina pentahydrogenjodistá (v texte staršie jodičná, d), (NH4)2U2O7 – diuránan amónny (e) a As(HSeO3)3 – hydrogenseleničitan arzenitý (g). Arzenitan vápenatý má vzorec Ca3(AsO3)2, nie Ca(AsO3)2 (a); dekahydrát tetraboritanu sodného má predponu deka-, nie dodeka- (c); SiC je karbid kremičitý a nie silán (f); a Na2S2O3 je v danej testovnici UPJŠ LF zaradený mimo kľúča.",

    87: "Správne vzorce a názvy zlúčenín sú: SiCl4 – chlorid kremičitý (b), Mg2Si – silicid horečnatý (c), SiC – karbid kremičitý (f) a Li2Se – selenid lítny (h). Hydrid vápenatý má vzorec CaH2, nie CaH3 (a); KO2 je hyperoxid (superoxid) draselný, nie KO (d); silán má vzorec SiH4, nie SiH2 (e); a Cl2O je oxid chlórny, nie chlorid kyslíka (g).",

    88: "Zlúčenina [Pt(NH3)6](OH)4 je hydroxid hexaamminplatičitý, ktorý obsahuje komplexný katión [Pt(NH3)6]4+ a štyri hydroxidové anióny OH- vo vonkajšej sfére (f, g). Koordinačné číslo centrálneho atómu platiny je 6 (šesť neutrálnych ligandov ammin NH3, a) a centrálny atóm má oxidačné číslo +IV, ktoré vyrovnáva štyri anióny OH- (e). Hydroxidové skupiny nie sú ligandy (b, c) a zlúčenina nie je komplexným platnatanom (h).",

    89: "V koordinačnej zlúčenine sú ligandy NH3 a Cl- koordinované na centrálny atóm platiny Pt (a, d). Koordinačné číslo komplexu je 4 (c) a donorom voľného elektrónového páru pri tvorbe koordinačnej väzby je popri chlóre aj atóm dusíka v molekule amoniaku (g). Oxidačné číslo platiny závisí od stechiometrie vnútorného komplexu (b), katión nesie náboj kompenzujúci SO4(2-) (e) a akceptorom elektrónov je prázdny orbitál centrálneho kovu Pt, nie dusíka (h).",

    90: "Chlorid pentaammin-chloroplatičitý má komplexný katión [PtCl(NH3)5]3+, kde platina v stave Pt(IV) viaže jeden aniónový ligand Cl- a päť neutrálnych molekúl NH3, takže nábojové číslo katiónu je +3 (a, c, g). Vonkajšiu sféru tvoria tri chloridové ióny Cl-, čo spolu s jedným ligandom Cl- dáva v celej molekule 4 atómy chlóru (d). Voda vystupuje ako kryštálová voda (hydrát) a nie ako ligand aqua (b), koordinačné číslo je 6 (1 Cl + 5 NH3, e) a anióny tvoria 3 chloridové ióny (f).",

    91: "Diammin-tetranitratokobaltitan draselný má vzorec K[Co(NH3)2(NO3)4] (f), pretože katión Co3+ viaže dva neutrálne ligandy NH3 a štyri nitráto ligandy NO3- s nábojom -1, čomu zodpovedá anión s nábojom -1 a jeden katión draselný K+ (g). Koordinačné číslo centrálneho atómu kobaltu je 6 (2 + 4, b) a molekula obsahuje neutrálne ligandy ammin (e). Zlúčenina je komplexná soľ s komplexným aniónom, nie katiónom (h), a obsahuje len 1 atóm K (c).",

    92: "V komplexe [CrBr2(H2O)4]NO2 je centrálnym atómom chróm v oxidačnom stave Cr(III) (a). Vnútornú koordinačnú sféru tvoria dva ligandy bromido Br- a štyri ligandy aqua H2O (e), preto má komplexný katión nábojové číslo (+3 - 2) = +1 (b), a vonkajšiu sféru tvorí dusitanový anión NO2- (h). Celkové koordinačné číslo chrómu je 6 (nie 2 ani 4, c, d), molekuly vody sú viazané priamo koordinačnou väzbou a nie kryštalicky (g) a oxidačné číslo chrómu je +III, nie +VI (f).",

    93: "Elektroneutrálne (molekulové) ligandy nenesú elektrický náboj; patria medzi ne karbonyl CO (a), nitrozyl NO (b), ammin NH3 (d) a aqua H2O (e). Naopak, chloridový ligand Cl- (chlorido, g) a kyanidový ligand CN- (kyano, h) sú aniónové ligandy nesúce záporný náboj -1; fosforyl a sulfuryl nie sú bežné ligandy komplexných zlúčenín (c, f).",

    94: "Anióny s nábojovým (oxidačným) číslom -2 obsahujú zlúčeniny K2S2O3 s tiosíranovým aniónom S2O3(2-) (c), MgCr2O7 s dichrómanovým aniónom Cr2O7(2-) (d), BaTiO3 s titaničitanovým aniónom TiO3(2-) (f) a Na2S2O5 s disiričitanovým aniónom S2O5(2-) (h). V NaBrO a KMnO4 sú prítomné jednozáporné anióny BrO- a MnO4- (a, b) a vo fosforečnanoch a arzeničnanoch sú anióny trojzáporné PO4(3-), PO3(3-) a AsO4(3-) (e, g).",

    95: "Správne pomenované zlúčeniny sú: (NH4)2Cr2O7 – dichróman amónny (d), CaS2O5 – disiričitan vápenatý (e), BaMnO4 – mangánan bárnatý s Mn(VI) (f) a NH4ClO3 – chlorečnan amónny (h). Arzenitan strieborný má vzorec Ag3AsO3 (a), fosforečnan mangánatý je Mn3(PO4)2 (b), Mg(HSO4)2 je hydrogensíran horečnatý, nie hydrogensiričitan (c), a Ca(ClO)2 je chlórnan vápenatý, nie CaClO2 (g).",

    96: "Peroxidy obsahujú peroxidovú skupinu (-O-O-) s kyslíkom v oxidačnom stave -I; patria sem peroxid sodný Na2O2 (b), peroxid vodíka H2O2 (d), peroxid ortutnatý HgO2 (f) a peroxid bárnatý BaO2 (g). Zlúčeniny KO2 a NaO2 sú superoxidy (hyperoxidy) obsahujúce anión O2(-), KO3 je ozonid a BaO je bežný oxid bárnatý s kyslíkom O(-II) (a, c, e, h).",

    97: "Ako centrálne atómy v koordinačných zlúčeninách vystupujú predovšetkým prechodné d-prvky, ktoré majú voľné d-orbitály vhodné na akceptovanie voľných elektrónových párov ligandov: platina Pt (c), kobalt Co (e), železo Fe (f) a striebro Ag (h). Prvky hlavných skupín ako bór B, vápnik Ca, síra S a draslík K (a, b, d, g) netvoria typické stabilné koordinačné komplexy a draslík či vápnik tvoria skôr jednoduché hydratované ióny.",

    98: "Nesprávne priradené triviálne názvy sú v možnostiach c, d, e, g. NaNO3 je čilský liadok, kým kamence sú podvojné sírany M(I)M(III)(SO4)2·12H2O (c); KCr(SO4)2·12H2O je chromito-draselný kamenec, pričom karnalit je KCl·MgCl2·6H2O (d); HgCl2 je sublimát (chlorid ortuťnatý), kým kalomel je Hg2Cl2 (e); a NO2 je oxid dusičitý, zatiaľ čo rajský plyn je oxid dusný N2O (g). Sóda (Na2CO3), potaš (K2CO3), zelená skalica (FeSO4·7H2O) a rumelka (HgS) sú pomenované správne (a, b, f, h).",

    99: "Správne mineralogické a triviálne názvy sú: ZnSO4·7H2O je biela skalica (a), KCl je sylvín (d), KCN je cyankáli (kyanid draselný, e) a Na3AlF6 je kryolit (g). Minerál PbS je galenit (sfalerit je ZnS, b), SiO2 je kremeň (korund je Al2O3, c), FeS2 je pyrit (chalkopyrit je CuFeS2, f) a čilský liadok je NaNO3, kým KNO3 je draselný liadok (h).",

    100: "Správne definície zliatin a minerálov sú: mosadz je zliatina medi a zinku Cu-Zn (a), alpaka je novostriebro – zliatina medi, niklu a zinku Cu-Ni-Zn (d), bronz je zliatina medi a cínu Cu-Sn (e) a salmiak je chlorid amónny NH4Cl (g). Sadrovec je dihydrát síranu vápenatého CaSO4·2H2O (b), hasené vápno je Ca(OH)2 (c), amalgámy sú zliatiny ortuti s kovmi (f) a pálená sadra je hemihydrát CaSO4·1/2H2O, kým CaO je pálené vápno (h)."
}

with open('scripts/chem_batches/batch_2.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

assert len(batch) == 50, f"Expected 50 items, found {len(batch)}"

for i, q in enumerate(batch):
    q_num = i + 51
    assert q_num in explanations, f"Missing explanation for question {q_num}"
    q['explanation'] = explanations[q_num]

with open('scripts/chem_batches/batch_2_explained.json', 'w', encoding='utf-8') as f:
    json.dump(batch, f, ensure_ascii=False, indent=2)

print("Successfully wrote scripts/chem_batches/batch_2_explained.json with 50 explained questions.")
