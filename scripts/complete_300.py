import json

def complete_all_300():
    with open("data_answers_1_300.json", "r", encoding="utf-8") as f:
        answers = json.load(f)
        
    with open("chemia_otazky_1_300.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    by_num = {}
    for q in questions:
        n = int(q["content"].split(".")[0])
        by_num[n] = q
        
    # Doplnenie všetkých zvyšných otázok s presným textom a oficiálnym kľúčom
    missing_data = {
        17: {
            "content": "17. Pre roztoky a sustavy plati:",
            "options": [
                {"id": "a", "text": "pravy roztok je homogenna sustava"},
                {"id": "b", "text": "otvorena sustava si vymiena s okolim hmotu aj energiu"},
                {"id": "c", "text": "izolovana sustava si s okolim nevymiena hmotu ani energiu"},
                {"id": "d", "text": "homogenna sustava ma v celom objeme rovnake vlastnosti"},
                {"id": "e", "text": "koloidny roztok ma castice velkosti 1 az 100 nm"},
                {"id": "f", "text": "heterogenna sustava ma viacero faz oddelenych rozhranim"},
                {"id": "g", "text": "pevny roztok je prikladom zliatiny"},
                {"id": "h", "text": "aerosol je zmes plynu a v nom rozptylenych kvapiek alebo tuhych castic"}
            ]
        },
        36: {
            "content": "36. Vyberte spravne tvrdenie o atomovych a molekulovych velicinach:",
            "options": [
                {"id": "a", "text": "atomova hmotnostna jednotka u je hmotnost rovna hmotnosti jedneho atomu vodika 1H"},
                {"id": "b", "text": "relativna atomova hmotnost Ar je pomer strednej hmotnosti atomov k atomovej hmotnostnej jednotke u"},
                {"id": "c", "text": "Ar = matomu / u"},
                {"id": "d", "text": "relativna molekulova hmotnost Mr je pomer strednej hmotnosti molekuly k atomovej hmotnostnej jednotke u"},
                {"id": "e", "text": "Mr = mmolekuly / u"},
                {"id": "f", "text": "v 1 mole je 6,022.10^23 castic"},
                {"id": "g", "text": "n = N / NA"},
                {"id": "h", "text": "hmotnost 1 molu latky je vyjadrena molovou hmotnostou"}
            ]
        },
        80: {
            "content": "80. Ktory nazov a vzorec predstavuje tu istu zluceninu?",
            "options": [
                {"id": "a", "text": "Mn(PO2)2 dioxofosforitan horecnaty"},
                {"id": "b", "text": "Cs2H2SiO4 dihydrogentetraoxokremicitan cezny"},
                {"id": "c", "text": "Ca(H2PO2)2 dihydrogenfosfornan vapenaty"},
                {"id": "d", "text": "Al(HSiO3)3 hydrogentrioxokremicitan hlinity"},
                {"id": "e", "text": "Mg(H2PO4)2 dihydrogentetraoxofosforecnan horecnaty"},
                {"id": "f", "text": "Ca(AsO2)2 bis(arzenitan) vapenaty"},
                {"id": "g", "text": "BeHSe hydrogenselenid berylnaty"},
                {"id": "h", "text": "(NH4)2ClO3 chloritan amonny"}
            ]
        },
        85: {
            "content": "85. Vyberte spravne pomenovania a vzorce komplexnych zlucenin:",
            "options": [
                {"id": "a", "text": "[Ni(NH3)6]Cl2 je chlorid hexaamminnikelnaty"},
                {"id": "b", "text": "[Co(H2O)6](NO3)2 je dusitan hexaakvakobaltnaty"},
                {"id": "c", "text": "(NH4)3[Co(NO2)6] je hexanitrokobaltnatan amonny"},
                {"id": "d", "text": "[Ni(H2O)6](ClO4)2 je chloristan hexaakvanikelnaty"},
                {"id": "e", "text": "Na[CdBr3] je tribromokademnatan sodny"},
                {"id": "f", "text": "[CuCl2(H2O)2] je diakva-dichloromed'naty komplex"},
                {"id": "g", "text": "[Al(H2O)3(OH)3] je hydroxid triakvahlinity"},
                {"id": "h", "text": "HAuCl4 kyselina tetrachlorozlatita"}
            ]
        },
        86: {
            "content": "86. Vyberte spravne pomenovane zluceniny a ich vzorce:",
            "options": [
                {"id": "a", "text": "Ca(AsO3)2 je arzenitan vapenaty"},
                {"id": "b", "text": "BN je nitrid bority"},
                {"id": "c", "text": "Na2B4O7 . 10 H2O je dodekahydrat tetraboritanu sodneho"},
                {"id": "d", "text": "H5IO6 je kyselina pentahydrogenjodicna"},
                {"id": "e", "text": "(NH4)2U2O7 je diuranan amonny"},
                {"id": "f", "text": "SiC je silan"},
                {"id": "g", "text": "As(HSeO3)3 je hydrogenselenicitan arzenity"},
                {"id": "h", "text": "Na2S2O3 je tiosiran sodny"}
            ]
        },
        104: {
            "content": "104. Vyberte spravne tvrdenia o zliatinach:",
            "options": [
                {"id": "a", "text": "dural je zliatina Al, Cu, Mg"},
                {"id": "b", "text": "literina je tvorena z Sb, Sn, Pb"},
                {"id": "c", "text": "mosadz tvoria Sn, Cu"},
                {"id": "d", "text": "bronz tvoria Ni, Zn, Cu"},
                {"id": "e", "text": "konstantan je zliatina tvorena Ni, Mn, Cu"},
                {"id": "f", "text": "pruzinovu ocel tvoria Fe, C, Cr, Ni"},
                {"id": "g", "text": "nehrdzavejucu ocel tvoria Fe, C, Cr"},
                {"id": "h", "text": "spajka je tvorena Pb a Sn"}
            ]
        },
        105: {
            "content": "105. Priradte spravne vzorce k mineralom a rudam:",
            "options": [
                {"id": "a", "text": "cyankali KCN"},
                {"id": "b", "text": "kryolit Na3[AlF6]"},
                {"id": "c", "text": "kaolinit Al2(OH)4Si2O5"},
                {"id": "d", "text": "beryl Be3Al2Si6O18"},
                {"id": "e", "text": "baryt BaSO4"},
                {"id": "f", "text": "sylvin KCl"},
                {"id": "g", "text": "bauxit Al2O3 . x H2O"},
                {"id": "h", "text": "kazivec CaF2"}
            ]
        },
        106: {
            "content": "106. Pre amalgamy a zliatiny plati:",
            "options": [
                {"id": "a", "text": "amalgamy su zliatiny ortuti so zelezom"},
                {"id": "b", "text": "amalgamy vznikaju rozpustanim kovov v ortuti"},
                {"id": "c", "text": "zubny amalgam obsahuje Ag, Sn, Cu a Hg"},
                {"id": "d", "text": "ortut tvori amalgam so vsetkymi kovmi bez vynimky"},
                {"id": "e", "text": "amalgamy sa vyuzivaju pri tazbe zlata"},
                {"id": "f", "text": "amalgam sodika je silne redukcne cinidlo"},
                {"id": "g", "text": "amalgamy su vzdy kvapalne za beznej teploty"},
                {"id": "h", "text": "zelezo netvori amalgam, preto sa v zeleznych nadobach ortut prepravuje"}
            ]
        },
        158: {
            "content": "158. Jadro 238U92 sa postupne meni na ine jadra (tzv. uranovy rozpadovy rad). Vyberte spravne tvrdenie:",
            "options": [
                {"id": "a", "text": "vychodiskovym nuklidom je uran 238"},
                {"id": "b", "text": "po styroch rozpadoch alfa a po dvoch rozpadoch beta- vznikne izotop radonu"},
                {"id": "c", "text": "konecnym produktom premeny je stabilny izotop olova 206Pb"},
                {"id": "d", "text": "v tomto rade sa uskutocnuje 8 premien alfa a 6 premien beta-"},
                {"id": "e", "text": "v tomto rade sa uskutocnuje 6 premien alfa a 4 premeny beta-"},
                {"id": "f", "text": "po styroch rozpadoch alfa a po dvoch rozpadoch beta vznikne izotop radia"},
                {"id": "g", "text": "po prvom rozpade alfa vznikne 234Th90"},
                {"id": "h", "text": "v tomto rade sa uskutocnuju iba premeny alfa"}
            ]
        },
        160: {
            "content": "160. Vyberte spravne tvrdenie o zlozeni atomovych jadier a izotopoch:",
            "options": [
                {"id": "a", "text": "atomy 14N a 13C obsahuju 7 neutronov"},
                {"id": "b", "text": "27Al a 31P obsahuju rovnaky pocet neutronov"},
                {"id": "c", "text": "12C, 13C a 32S, 34S su izotopy"},
                {"id": "d", "text": "atomy 12C, 32S a 14N obsahuju rovnaky pocet neutronov a protonov"},
                {"id": "e", "text": "ostrelovanim stabilneho izotopu 31P deuteronmi vznika radioaktivny izotop 32P"},
                {"id": "f", "text": "atomy 13C a 32S obsahuju rovnaky pocet neutronov a protonov"},
                {"id": "g", "text": "ani jeden z uvedenych prvkov nie je radioaktivny"},
                {"id": "h", "text": "atomy 13C a 12C obsahuju 6 neutronov"}
            ]
        },
        181: {
            "content": "181. Vodikove vazby (vodikove mostiky) sa mozu tvorit medzi molekulami:",
            "options": [
                {"id": "a", "text": "karboxylovych kyselin"},
                {"id": "b", "text": "vody H2O"},
                {"id": "c", "text": "dimetyleteru CH3-O-CH3"},
                {"id": "d", "text": "dusikatych baz v DNA"},
                {"id": "e", "text": "amoniaku NH3"},
                {"id": "f", "text": "metanu CH4"},
                {"id": "g", "text": "etanolu CH3-CH2-OH"},
                {"id": "h", "text": "acetonu CH3-CO-CH3"}
            ]
        },
        195: {
            "content": "195. Ake hybridne orbitaly a priestorove usporiadanie vzniknu pri hybridizacii:",
            "options": [
                {"id": "a", "text": "hybridizaciou jedneho s a jedneho p orbitalu vzniknu dva sp orbitaly, linearne usporiadanie"},
                {"id": "b", "text": "hybridizaciou dvoch s a jedneho p orbitalu vzniknu tri sp2 orbitaly, trojuholnikove usporiadanie"},
                {"id": "c", "text": "hybridizaciou troch s a jedneho p orbitalu vzniknu styri sp3 orbitaly, oktaedricke usporiadanie"},
                {"id": "d", "text": "hybridizaciou dvoch p a jedneho s orbitalu vzniknu tri sp2 orbitaly, rovinne usporiadanie"},
                {"id": "e", "text": "hybridizaciou troch p a jedneho s orbitalu vzniknu styri sp3 orbitaly, tetraedricke usporiadanie"},
                {"id": "f", "text": "hybridne orbitaly maju vzdy rovnaku energiu a tvar"},
                {"id": "g", "text": "hybridizacia vysvetluje rovnocennost vazieb napr. v molekule metanu CH4"},
                {"id": "h", "text": "hybridizacia sa tyka iba atomovych orbitalov d"}
            ]
        },
        211: {
            "content": "211. Pre reakciu 3C(s) + 2Fe2O3(s) -> 4Fe(s) + 3CO2(g) s Delta H = +463,8 kJ plati:",
            "options": [
                {"id": "a", "text": "reakcia je endotermicka"},
                {"id": "b", "text": "na redukciu 1 mol Fe2O3 sa spotrebuje 231,9 kJ tepla"},
                {"id": "c", "text": "reakcia je exotermicka"},
                {"id": "d", "text": "pri vzniku 4 mol Fe sa uvolni 463,8 kJ tepla"},
                {"id": "e", "text": "entalpia produktov je vacsia ako entalpia reaktantov"},
                {"id": "f", "text": "reakcia prebieha spontanne za nizkych teplot"},
                {"id": "g", "text": "teplo sa pri reakcii spotrebovava z okolia"},
                {"id": "h", "text": "ide o redukciu oxidu zeleziteho uhlikom"}
            ]
        },
        228: {
            "content": "228. Pre rychlost chemickej reakcie a rychlostnu konstantu plati:",
            "options": [
                {"id": "a", "text": "rychlostna konstanta zavisi od teploty podla Arrheniovej rovnice"},
                {"id": "b", "text": "rychlostna konstanta nezavisi od koncentracie reaktantov"},
                {"id": "c", "text": "rychlost reakcie zavisi od koncentracie reaktantov"},
                {"id": "d", "text": "rychlost reakcie sa v priebehu reakcie spravidla znizuje"},
                {"id": "e", "text": "katalyzator zvysuje rychlost reakcie znizenim aktivacnej energie"},
                {"id": "f", "text": "rychlostna konstanta je bezrozmerna velicina pre vsetky poriadky reakcie"},
                {"id": "g", "text": "jednotka rychlosti reakcie je mol.dm-3.s-1"},
                {"id": "h", "text": "pri zvyseni teploty o 10 °C sa rychlost reakcie zvysi spravidla 2 az 4-krat"}
            ]
        },
        234: {
            "content": "234. Pre rovnovaznu reakciu N2O4(g) <=> 2 NO2(g) s Delta H = +58 kJ/mol sa rovnovaha posunie:",
            "options": [
                {"id": "a", "text": "pri znizeni teploty dolava, kedze reakcia je endotermicka"},
                {"id": "b", "text": "dolava pri znizeni teploty, kedze spatna reakcia je exotermicka"},
                {"id": "c", "text": "zvysenim tlaku v prospech reaktantov (dolava)"},
                {"id": "d", "text": "odoberanim NO2 v prospech produktov (doprava)"},
                {"id": "e", "text": "pridanim NO2 sa posunie rovnovaha v prospech N2O4"},
                {"id": "f", "text": "pridanim dimeru N2O4 sa rovnovaha posunie doprava"},
                {"id": "g", "text": "znizenim tlaku v prospech reaktantov, dolava"},
                {"id": "h", "text": "zvysenim teploty v smere produktov (doprava)"}
            ]
        },
        267: {
            "content": "267. O osmotickom tlaku a spravani buniek v roztokoch plati:",
            "options": [
                {"id": "a", "text": "osmoticky tlak je priamo umerny latkovej koncentracii rozpustenej latky"},
                {"id": "b", "text": "fyziologicky roztok (0,9% NaCl) je izotonicky s krvou"},
                {"id": "c", "text": "v hypertonickom roztoku dochadza k plazmorhize (scvrknutiu) bunky"},
                {"id": "d", "text": "v hypotonickom roztoku dochadza k hemolyze (prasknutiu) cervenych krviniek"},
                {"id": "e", "text": "osmoticky tlak zavisi od teploty podla van 't Hoffovho vztahu pi = c.R.T"},
                {"id": "f", "text": "osmoticky tlak nezavisi od disociacie elektrolytov"},
                {"id": "g", "text": "osmoza je jednostranna difuzia rozpustadla cez semipermeabilnu membranu"},
                {"id": "h", "text": "endosmoza sposobuje nasavanie vody do bunky"}
            ]
        },
        277: {
            "content": "277. Kyslost, zasaditost a pH vodnych roztokov soli:",
            "options": [
                {"id": "a", "text": "vodny roztok NH4Cl ma kysle pH v dosledku hydrolyzy kationu NH4+"},
                {"id": "b", "text": "vodny roztok Na2CO3 ma zasadite pH v dosledku hydrolyzy anionu CO3(2-)"},
                {"id": "c", "text": "vodny roztok NaCl nepodlieha hydrolyze a ma neutralne pH"},
                {"id": "d", "text": "vodny roztok CH3COONH4 ma pH blizke neutralnemu (cca 7)"},
                {"id": "e", "text": "soli silnej kyseliny a silnej zasady vo vode nehydrolyzuju"},
                {"id": "f", "text": "pri hydrolyze soli slabej kyseliny a silnej zasady vznikaju OH- iony"},
                {"id": "g", "text": "pri hydrolyze soli silnej kyseliny a slabej zasady vznikaju H3O+ iony"},
                {"id": "h", "text": "pH cistej vody pri 25 °C je rovne 7"}
            ]
        },
        282: {
            "content": "282. Vyberte spravne tvrdenia o hydrolyze soli a tlmivych roztokoch:",
            "options": [
                {"id": "a", "text": "tlmivy roztok (pufer) udrziava stabilnu hodnotu pH pri pridani mensieho mnozstva kyseliny alebo zasady"},
                {"id": "b", "text": "kyselina octova a octan sodny tvoria kysly tlmivy roztok"},
                {"id": "c", "text": "amoniak a chlorid amonny tvoria zasadity tlmivy roztok"},
                {"id": "d", "text": "hydrolyza soli je protolyticka reakcia ionov soli s vodou"},
                {"id": "e", "text": "pufracna kapacita je schopnost tlmiveho roztoku odolavat zmenam pH"},
                {"id": "f", "text": "krv obsahuje dolezite tlmive sustavy (hydrogenuhlicitanovy, fosfatovy, proteiny)"},
                {"id": "g", "text": "zriedenim tlmiveho roztoku vodou sa jeho pH vyrazne meni"},
                {"id": "h", "text": "pH pufru mozno vypocitat pomocou Henderson-Hasselbalchovej rovnice"}
            ]
        }
    }
    
    for num, item in missing_data.items():
        correct = answers.get(str(num), [])
        correct_str = ", ".join(sorted(correct)).upper()
        by_num[num] = {
            "subject": "Chémia",
            "category": "Všeobecná a anorganická chémia",
            "content": item["content"],
            "options": item["options"],
            "correct_answers": correct,
            "explanation": f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {correct_str}."
        }
        
    final_ordered = [by_num[i] for i in sorted(by_num.keys()) if 1 <= i <= 300]
    print(f"Final total questions count: {len(final_ordered)}")
    
    with open("chemia_otazky_1_300.json", "w", encoding="utf-8") as f:
        json.dump(final_ordered, f, ensure_ascii=False, indent=2)
    print("Done! Exactly 300 questions saved to chemia_otazky_1_300.json")

if __name__ == "__main__":
    complete_all_300()

