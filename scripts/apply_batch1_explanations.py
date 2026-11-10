import json
import os

# Explanations dictionary mapping question index (0 to 49) to Slovak explanation
explanations = {
    0: (
        "Suspenzia je heterogénna (rôznorodá) hrubodisperzná zmes nerozpustenej tuhej látky rozptýlenej v kvapaline, "
        "kde veľkosť častíc presahuje 100 nm (resp. 1 μm). Bežným príkladom je zmes piesku a vody alebo ovocný džús "
        "s nerozpustnou dužinou. Na rozdiel od pravých roztokov má suspenzia viacero fáz a nepatrí medzi aerosóly, "
        "pretože aerosóly majú plynné disperzné prostredie (napr. dym či hmla)."
    ),
    1: (
        "Emulzia je hrubodisperzná rôznorodá zmes dvoch vzájomne nemiešateľných (nerozpustných) kvapalín, v ktorej sú "
        "kvapôčky jednej kvapaliny rozptýlené v druhej. Typickými príkladmi emulzií sú mlieko, pleťové mlieka alebo zmes "
        "oleja a vody stabilizovaná emulgátorom. Možnosti uvádzajúce rovnorodú zmes, rozpustené kvapaliny či plynné zložky "
        "sú chybné, pretože emulzia je vždy heterogénna sústava kvapalín."
    ),
    2: (
        "Kvalitatívne a intenzívne vlastnosti látok (ako vzhľad, hustota či skupenstvo) sú charakteristické pre daný chemický "
        "druh a spravidla nezávisia od celkového množstva danej látky v sústave. Chemicky čisté látky (prvky a zlúčeniny) "
        "sa v prírode vyskytujú zriedka, keďže väčšina hmôt existuje vo forme zmesí. Tvrdenia predpokladajúce závislosť "
        "vlastností od množstva alebo vylučujúce senzorické vlastnosti (chuť, vôňa) sú nesprávne."
    ),
    3: (
        "Separačné metódy slúžia na rozdelenie zmesí na jednotlivé zložky na základe ich rozdielnych fyzikálnych vlastností "
        "(teplota varu, rozpustnosť, hustota) bez zmeny chemickej identity. Sedimentácia využíva rozdielne hustoty a gravitačné "
        "usadzovanie, destilácia je založená na odlišných teplotách varu kvapalín a filtrácia s kryštalizáciou patria medzi "
        "základné separačné techniky. Možnosti tvrdiace opak alebo považujúce destiláciu za neúčinnú sú nesprávne."
    ),
    4: (
        "Otázka vyžaduje vybrať nesprávne výroky: aerosóly v skutočnosti patria medzi koloidné roztoky (disperzie kvapaliny "
        "alebo tuhej látky v plyne), dym a hmla sú aerosóly (nie peny) a benzín vo vode tvorí emulziu dvoch kvapalín, "
        "nie suspenziu. Taktiež v rôznorodej zmesi spravidla vieme rozlíšiť prevládajúcu fázu (disperzné prostredie). "
        "Definície peny a hmly sú naopak pravdivé, preto nepatria k označeným nesprávnym možnostiam."
    ),
    5: (
        "Otázka vyžaduje označiť nesprávne tvrdenia: ionizačná energia je energia potrebná na odtrhnutie elektrónu od atómu, "
        "preto prvky ľahko tvoriace katióny majú nízku, nie vysokú ionizačnú energiu. Energia uvoľnená pri prijatí elektrónu "
        "je elektrónová afinita, nie ionizačná energia, a neudáva sa iba v kJ (ale v kJ/mol), pričom môže nadobúdať aj záporné hodnoty. "
        "Tieto chybné a navzájom zamenené definície presne zodpovedajú možnostiam b, c, e, f."
    ),
    6: (
        "Rozpustnosť látky v danom rozpúšťadle závisí od chemickej povahy oboch zložiek a teploty, pričom jej priebeh vyjadruje "
        "krivka rozpustnosti a možno ju vyjadriť koncentráciou nasýteného roztoku v mol·dm⁻³. V prípade plynov je rozpustnosť "
        "v kvapaline priamo závislá od tlaku podľa Henryho zákona. Nezávisí od objemu nádoby a neplatí, že s rastom teploty "
        "vždy rastie (pri plynoch naopak klesá), ani že tlak ovplyvňuje rozpustnosť tuhých látok."
    ),
    7: (
        "Jeden mól akejkoľvek plynnej látky obsahuje rovnaký počet molekúl rovný Avogadrovej konštante (NA = 6,022·10²³), čo nezávisí "
        "od tlaku, preto 1 mol O₂ aj 1 mol HCl obsahujú zhodný počet molekúl. Za rovnakých podmienok má 1 mol CO₂ rovnaký molový "
        "objem ako 1 mol O₂ (Vm = 22,4 dm³/mol pri s.t.p.). V 1 móle trojatómového CO₂ je celkovo 3 NA atómov, čo je viac než v 1 móle "
        "dvojatómového O₂ (2 NA atómov)."
    ),
    8: (
        "Pravé (analytické) roztoky sú homogénne disperzné sústavy, v ktorých sú rozpustené častice nízkomolekulové (jednotlivé "
        "solvatované ióny alebo malé neutrálne molekuly) s veľkosťou menšou ako 1 nm (1·10⁻⁹ m). Patria sem roztoky bežných solí "
        "a silných elektrolytov ako KCl či FeCl₂, ktoré vo vode úplne disociujú na voľné ióny. Roztoky bielkovín obsahujú makromolekuly "
        "s veľkosťou 1 až 100 nm, preto tvoria koloidné, nie pravé roztoky."
    ),
    9: (
        "Hmotnostný zlomok w(A) = m(A)/mr vyjadruje bezrozmerný podiel hmotnosti rozpustenej látky A k celkovej hmotnosti roztoku, "
        "pričom nadobúda hodnoty w(A) ≤ 1. Vynásobením číslom 100 získame koncentráciu v hmotnostných percentách, pričom vyššia hodnota "
        "w(A) znamená vyššiu koncentráciu roztoku. Možnosť uvádzajúca jednotku g·mol⁻¹ patrí molárnej hmotnosti a možnosť f definuje "
        "mólový zlomok, nie hmotnostný."
    ),
    10: (
        "V pravom roztoku musia mať rozpustené častice rozmer menší ako 1 nm, čo spĺňajú len nízkomolekulové zlúčeniny a jednoduché ióny. "
        "Makromolekuly prírodných polymérnych zlúčenín, akými sú škrob (polysacharid) a bielkoviny vrátane hemoglobínu, majú rozmery "
        "v rozmedzí 1 až 100 nm. Z tohto dôvodu tvoria výlučne koloidné roztoky a v pravom roztoku sa nikdy nemôžu vyskytovať."
    ),
    11: (
        "V perióde zľava doprava stúpa efektívny náboj jadra, čo spôsobuje nárast elektronegativity, nekovového charakteru a kyslosti "
        "tvorivých oxidov. Z toho logicky vyplýva, že nekovový charakter klesá opačným smerom (sprava doľava). Zároveň zľava doprava "
        "klesajú redukčné účinky prvkov, pretože atómy ťažšie odovzdávajú svoje valenčné elektróny. Možnosti a, c, f, g uvádzajú opačné trendy."
    ),
    12: (
        "V hlavných podskupinách periodickej tabuľky rastie počet elektrónových vrstiev, preto polomer atómov rastie s rastúcim Z a naopak "
        "sa zmenšuje s klesajúcim Z. V danej perióde sa zľava doprava zvyšuje kladný náboj jadra pri rovnakom počte vrstiev, čo vedie "
        "k silnejšiemu priťahovaniu vonkajších elektrónov a zmenšovaniu atómového polomeru (s výnimkou inertných plynov s uzavretým oktetom)."
    ),
    13: (
        "Odtrhnutím elektrónu pri vzniku katiónu prevládne príťažlivá sila jadra nad zmenšeným obalom, preto je polomer katiónu vždy "
        "menší než polomer neutrálneho atómu a ďalej sa zmenšuje s rastúcim kladným nábojom (napr. r(Fe³⁺) < r(Fe²⁺)). Naopak prijatím "
        "elektrónu do obalu pri vzniku aniónu sa zvýši medzi-elektrónové odpudzovanie a polomer aniónu je vždy väčší než pôvodného atómu. "
        "V perióde veľkosť aniónov s rastúcim Z klesá vďaka rastúcemu náboju jadra."
    ),
    14: (
        "Pre väčšinu prvkov hlavných podskupín zodpovedá maximálne kladné oxidačné číslo číslu podskupiny (počtu valenčných elektrónov), "
        "avšak pri prechodných kovoch môže byť aj vyššie (napr. Cu v skupine IB tvorí Cu²⁺). Maximálne záporné oxidačné číslo nekovov "
        "sa určuje podľa pravidla doplnenia oktetu vzťahom 8 mínus číslo podskupiny (so záporným znamienkom, napr. pre VI.A skupinu: 8 - 6 = 2, "
        "teda oxidačné číslo -II)."
    ),
    15: (
        "Táto otázka testuje základnú typológiu chemických sústav a disperzných systémov. Izolovaná sústava si s okolím nevymieňa hmotu "
        "ani energiu, homogénna sústava je jednofázová s rovnakými vlastnosťami v celom objeme, koloidný roztok predstavuje disperziu "
        "s časticami veľkosti 1–100 nm a heterogénna sústava pozostáva z viacerých fáz oddelených fázovým rozhraním. V oficiálnom kľúči "
        "sú ako správne definované možnosti c, d, e, f."
    ),
    16: (
        "Pravý roztok je homogénna sústava tvorená jednou fázou, ktorá vykazuje vo všetkých svojich častiach rovnaké fyzikálno-chemické "
        "vlastnosti. Izolovaná sústava je termodynamicky definovaná ako systém dokonale izolovaný od okolia, ktorý si s ním nevymieňa "
        "hmotu ani žiadnu formu energie. Možnosti a, c, d presne zodpovedajú týmto základným definíciám platným pre roztoky a sústavy."
    ),
    17: (
        "Otázka vyžaduje označiť nesprávne tvrdenia o chemických vzorcoch. Funkčný vzorec vyjadruje charakteristickú funkčnú skupinu "
        "(napr. -OH), nie priestorové usporiadanie atómov (to vyjadruje konfiguračný vzorec). Stechiometrický vzorec udáva najjednoduchší "
        "pomer atómov a pri mnohých zlúčeninách (napr. H₂O) je zhodný so sumárnym molekulovým vzorcom. Možnosti a a g sú navyše vecne chybné "
        "či skomolené formulácie v kontexte zadania."
    ),
    18: (
        "Vodný roztok chloridu sodného (NaCl) je pravý roztok, a teda rovnorodá (homogénna) zmes, pretože disociované hydratované ióny "
        "Na⁺ a Cl⁻ majú rozmery menšie ako 1 nm. Keďže NaCl je silný elektrolyt, prítomnosť voľne pohyblivých solvatovaných iónov robí "
        "roztok elektricky vodivým. Nejde o chemicky čistú látku ani chemické indivíduum, keďže pozostáva z dvoch odlišných zložiek (soli a vody)."
    ),
    19: (
        "Albumín je globulárna bielkovina tvoriaca lyofilnú koloidnú zmes s veľkosťou častíc v koloidnom rozmedzí (1 až 100 nm, t. j. 10⁻⁹ až 10⁻⁷ m). "
        "V roztoku je stabilizovaný solvatačným (hydratačným) obalom z molekúl vody a rovnakým elektrostatickým nábojom, čo zabraňuje zhlukovaniu. "
        "Nejde o pravý roztok, pretože makromolekuly bielkovín vykazujú typické vlastnosti koloidov vrátane Tyndallovho javu."
    ),
    20: (
        "Vriaca voda v otvorenej kadičke neustále vymieňa s okolím hmotu (paru) aj energiu (teplo), preto je otvorenou nerovnovážnou sústavou. "
        "Voda a chloroform v uzavretom lieviku tvoria dve oddelené kvapalné fázy bez výmeny hmoty s okolím (uzavretá heterogénna sústava). "
        "Koloidné sústavy majú veľkosť dispergovaných častíc od 1 nm do 100 nm (0,1 μm), kým častice s veľkosťou nad 1 μm tvoria hrubé "
        "heterogénne sústavy."
    ),
    21: (
        "Číra minerálna alebo pitná voda vyvierajúca z prameňa je rovnorodá (homogénna) zmes viacerých chemických látok – vody a v nej "
        "rozpustených anorganických solí a plynov. Keďže rozpustené látky sú rozptýlené vo forme jednotlivých iónov s rozmerom pod 1 nm, "
        "predstavuje pravý roztok. Nejde o chemicky čistú látku ani chemické indivíduum, keďže nepozostáva výhradne z molekúl H₂O."
    ),
    22: (
        "Chemické indivíduum (chemicky čistá látka) je látka so stálymi fyzikálno-chemickými vlastnosťami (teplota varu, hustota) a presným "
        "zložením, ktorou môže byť chemický prvok alebo chemická zlúčenina. Príkladom chemických indivíduí sú čistý etanol (CH₃-CH₂-OH) "
        "a disacharid laktóza. Naopak roztoky (ako KCl vo vode) sú zmesi dvoch a viacerých látok, a samotný atóm nie je látkou v makroskopickom zmysle."
    ),
    23: (
        "Zmes je sústava zložená z rôznych chemických častíc a delí sa podľa stupňa disperzity na homogénnu, koloidnú a heterogénnu. "
        "Zmesi existujú vo všetkých skupenstvách (vrátane pevných zliatin), pričom zmes plynov je za bežných podmienok vždy dokonale "
        "homogénna sústava. Možnosti tvrdiace identické vlastnosti zložiek alebo označujúce roztok KCl za heterogénny sú nesprávne."
    ),
    24: (
        "Chemické prvky sú chemické indivíduá (čisté látky), ktorých atómy majú zhodné protónové číslo Z, pričom sa môžu líšiť počtom neutrónov "
        "v jadre (izotopy). Molekuly jednoduchých látok tvorených daným prvkom sú zložené výlučne z atómov rovnakého druhu (napr. O₂, N₂). "
        "Ak by boli molekuly zložené z atómov rôznych prvkov (ako tvrdí možnosť h), išlo by o chemické zlúčeniny."
    ),
    25: (
        "Chemicky čistá látka pozostáva z jediného typu chemického indivídua s presne definovaným zložením, kam patria prvky (kvapalný dusík N₂) "
        "aj stechiometrické zlúčeniny (sóda bikarbóna NaHCO₃, síran zinočnatý ZnSO₄ a kryštalohydrát MgCl₂·6H₂O). Pitná voda, čistý vzduch, "
        "sklo a roztok HNO₃ predstavujú viaczložkové zmesi, a preto nie sú chemicky čistými látkami."
    ),
    26: (
        "Modrá skalica (pentahydrát síranu meďnatého, CuSO₄·5H₂O) sa vo vode úplne rozpúšťa a disociuje na hydratované katióny Cu²⁺ a anióny SO₄²⁻. "
        "Hydratované meďnaté ióny absorbujú svetlo v červenej oblasti spektra, čo dáva roztoku typickú modrú farbu. Vzniknutá sústava je "
        "pravým roztokom, a teda homogénnou jednofázovou zmesou bez fázových rozhraní či optickej aktivity."
    ),
    27: (
        "Koloidné roztoky (nepravé roztoky, soly) obsahujú rozptýlené častice s veľkosťou v intervale 1 až 100 nm (vrátane rozmedzia 1–50 nm). "
        "Vďaka tejto veľkosti častíc dochádza k optickému rozptylu svetla (Tyndallov jav), čo odlišuje koloidy od pravých roztokov. Medzi typické "
        "lyofilné koloidy patria roztoky makromolekulových bielkovín; suspenzie a emulzie naopak patria medzi hrubé disperzie."
    ),
    28: (
        "Skupenský stav látky je výsledkom rovnováhy medzi medzimolekulovými silami a tepelným pohybom častíc, a preto je priamo závislý "
        "od vonkajších podmienok (teploty a tlaku). Priamy prechod látky z tuhého skupenstva do plynného sa nazýva sublimácia. Plazma je vysoko "
        "ionizovaný stav hmoty tvorený zmesou voľných iónov, elektrónov a neutrálnych častíc, ktorý je navonok ako celok elektroneutrálny."
    ),
    29: (
        "V plynnom stave sú vzdialenosti medzi časticami mnohonásobne väčšie ako v kvapalinách a tepelný pohyb častíc je výrazne chaotickejší. "
        "Zväčšením medzimolekulových vzdialeností a prekonaním súdržných síl sa z kvapaliny stáva plyn. Sublimácia predstavuje priamy prechod "
        "z pevného skupenstva do plynného bez prechodu cez kvapalnú fázu. Alotropia naopak označuje existenciu prvku v rôznych štruktúrnych formách."
    ),
    30: (
        "Chemické zlúčeniny vznikajú chemickou reakciou z prvkov tvorbou nových chemických väzieb, pričom vlastnosti pôvodných prvkov "
        "nezostávajú zachované. Prvky sa v zlúčeninách viažu v stálych a celistvých násobných pomeroch podľa Daltonovho zákona. Na rozdiel "
        "od zmesí ich nemožno rozdeliť na pôvodné zložky fyzikálnymi metódami, ale výlučne chemickým rozkladom."
    ),
    31: (
        "Zmes vzniká jednoduchým fyzikálnym zmiešaním dvoch alebo viacerých čistých látok v ľubovoľnom hmotnostnom pomere bez priebehu "
        "chemickej reakcie, vďaka čomu si zložky zachovávajú svoje pôvodné vlastnosti. Jednotlivé čisté látky možno zo zmesi opäť izolovať "
        "pomocou fyzikálnych separačných metód (sedimentácia, filtrácia, destilácia či extrakcia). Možnosti vyžadujúce chemickú reakciu "
        "alebo pevný stechiometrický pomer platia pre zlúčeniny."
    ),
    32: (
        "Avogadrov zákon stanovuje, že rovnaké látkové množstvá ideálnych plynov zaberajú za rovnakých podmienok rovnaký objem, pričom za "
        "normálnych podmienok je to molový objem Vm = 22,4 dm³/mol. Daltonov zákon násobných pomerov dokazuje existencia oxidov chrómu "
        "(CrO₃ a Cr₂O₃), kde na rovnaké množstvo chrómu pripadá pomer kyslíka v pomere celých čísel. Zákon zachovania hmotnosti formuloval "
        "Lomonosov (spolu s Lavoisierom); v možnostiach c, d, h sú uvedené nesprávne vzťahy a veličiny."
    ),
    33: (
        "Chemická reakcia je proces, pri ktorom dochádza k premene reaktantov na produkty s odlišnou chemickou štruktúrou a vlastnosťami. "
        "Periodický zákon formuluje, že vlastnosti prvkov a ich zlúčenín sú periodickou funkciou ich protónového čísla Z. Molekuly "
        "vznikajú kovalentným spojením celistvých počtov atómov, zatiaľ čo fázové zmeny ako ohrev či topenie sú fyzikálne deje bez zmeny molekúl."
    ),
    34: (
        "Hmotnosť jedného mólu chemickej látky vyjadruje jej molárna hmotnosť M a jeden mól obsahuje presne 6,022·10²³ častíc (Avogadrova konštanta). "
        "Relatívna atómová hmotnosť Ar je bezrozmerná veličina definovaná ako pomer skutočnej hmotnosti atómu a atómovej hmotnostnej jednotky u "
        "(Ar = matómu / u). Možnosti c, f, g, h uvádzajú tieto fundamentálne stechiometrické vzťahy a veličiny v súlade s oficiálnym kľúčom."
    ),
    35: (
        "Atómová hmotnostná jednotka u zodpovedá 1/12 hmotnosti atómu uhlíka ¹²C (historicky približne hmotnosti atómu vodíka ¹H). Relatívna "
        "atómová hmotnosť Ar je bezrozmerný podiel strednej hmotnosti atómu a jednotky u, a analogicky relatívna molekulová hmotnosť je Mr = mmolekuly / u. "
        "Látkové množstvo n vyjadruje počet základných entít v súbore delený Avogadrovou konštantou podľa vzťahu n = N / NA."
    ),
    36: (
        "Látkové množstvo n je definované ako pomer celkového počtu častíc N a Avogadrovej konštanty NA (n = N / NA), alebo ako podiel "
        "hmotnosti vzorky m a molárnej hmotnosti M (n = m / M). Základnou jednotkou látkového množstva v sústave SI je mól (mol), prípadne "
        "odvodená jednotka milimól (mmol). Ostatné vzorce a jednotky uvedené v možnostiach sú dimenzionálne nesprávne."
    ),
    37: (
        "Otázka žiada identifikovať nesprávne tvrdenia: molárna hmotnosť má jednotku kg/mol alebo g/mol, nie mol/kg. Látkové množstvo má "
        "jednotku mol, nie mol/kg, a vyjadruje sa pomerom n = N / NA (nie NA / N). Predpona nano znamená 10⁻⁹, preto 1 nmol = 10⁻⁹ mol, "
        "nie 10⁻⁶ mol (čo je mikromól). Tieto jednoznačne chybné výroky zodpovedajú možnostiam c, d, f, h."
    ),
    38: (
        "Vzťahy pre výpočet koncentrácií vychádzajú z látkového množstva a Avogadrovho princípu. Látková koncentrácia sa vyjadruje ako "
        "c = n / V (s jednotkou mol·l⁻¹ alebo mmol/l) a po dosadení za látkové množstvo n = m / M dostávame vzťah c = m / (M·V) s jednotkou "
        "mol·cm⁻³. Možnosti a, b, d, g sú v oficiálnom kľúči testovnice UPJŠ LF označené ako správne odpovede na tento typ úloh."
    ),
    39: (
        "Látková koncentrácia c vyjadruje pomer látkového množstva n a objemu roztoku V (c = n / V). Po dosadení vzťahu n = m / M získame "
        "ekvivalentný vzorec c = m / (M·V). Medzi platné jednotky látkovej koncentrácie patria mol·l⁻¹, mol/dm³, mmol/l a mol·cm⁻³, "
        "zatiaľ čo vzorce so súčinom objemu či nesprávnymi exponentmi (napr. c = n·V) sú chybné."
    ),
    40: (
        "Hmotnostný zlomok w(A) látky v roztoku je pomer hmotnosti látky k celkovej hmotnosti roztoku: w(A) = m(A) / m. Keďže hmotnosť roztoku "
        "je súčinom hustoty a objemu (m = ρ·V), platí w(A) = m(A) / (ρ·V). Po vyjadrení hmotnosti látky cez látkové množstvo m(A) = n(A)·M(A) "
        "získavame ekvivalentné správne vyjadrenia w(A) = n(A)·M(A) / m a w(A) = n(A)·M(A) / (ρ·V)."
    ),
    41: (
        "Látková (molárna) koncentrácia udáva množstvo látky v jednotke objemu roztoku (c = n / V). Jej jednotkou v sústave SI je mol·m⁻³, "
        "v laboratórnej praxi sa však najčastejšie používajú jednotky mol·dm⁻³, mol/l, menšia jednotka mmol/l a pri malých objemoch mol·cm⁻³. "
        "Samotný mol je jednotkou látkového množstva a kg/mol je jednotkou molárnej hmotnosti."
    ),
    42: (
        "Jeden mól je základná jednotka látkového množstva, ktorá obsahuje presne toľko základných častíc, koľko atómov je v 12 g nuklidu ¹²C. "
        "Látkové množstvo látky v roztoku je rovné súčinu jej látkovej koncentrácie a objemu roztoku (n = c·V). Možnosti b, c, f, h "
        "sú označené ako správne podľa oficiálneho kľúča testovnice UPJŠ LF."
    ),
    43: (
        "Zloženie roztokov môžeme kvantitatívne vyjadriť mólovým zlomkom (xA = nA / ncelk), hmotnostnou koncentráciou v g/l (cm = mA / V), "
        "molalitou definovanou ako látkové množstvo na kilogram rozpúšťadla a látkovou (molovou) koncentráciou (c = nA / V). Možnosti d a e "
        "sú chybné, pretože zlomky sa vzťahujú k celému roztoku a nie k samotnému rozpúšťadlu."
    ),
    44: (
        "Objemový zlomok φ(A) vyjadruje podiel objemu zložky V(A) k celkovému objemu roztoku V, teda φ(A) = V(A) / V. Pretože celkový objem "
        "roztoku možno z hustoty a hmotnosti vyjadriť ako V = m / ρ, dosadením dostaneme vzťah φ(A) = V(A)·ρ / m. Ostatné uvedené vzorce "
        "rozmerovo a vecne nezodpovedajú definícii objemového zlomku."
    ),
    45: (
        "Látkovú koncentráciu c(A) = n(A)/V = m(A)/(M·V) možno vyjadriť dosadením za objem V = m/ρ, čím získame c(A) = n(A)·ρ / m "
        "a c(A) = m(A)·ρ / (M·m). Keďže hmotnostný zlomok je w = m(A)/m, úpravou dostaneme priamy prevodný vzťah medzi zlomkom a koncentráciou "
        "c(A) = w·ρ / M. Tieto odvodené tvary presne zodpovedajú možnostiam c, e, g, h."
    ),
    46: (
        "Zmiešavacia rovnica vychádza zo zákona zachovania hmotnosti: m₁w₁ + m₂w₂ = mw, kde výsledná hmotnosť je súčtom m = m₁ + m₂ "
        "(teda m₁ = m - m₂). Pri zrieďovaní roztoku čistým rozpúšťadlom je hmotnostný zlomok rozpustenej látky v pridanom rozpúšťadle w₂ = 0. "
        "Pri zahusťovaní pridaním čistej tuhej látky má táto pridaná zložka hmotnostný zlomok w₂ = 1."
    ),
    47: (
        "Rozpustnosť látky vyjadruje jej schopnosť tvoriť za daných podmienok nasýtený roztok a je kľúčová pri navrhovaní kryštalizácie, "
        "pri posudzovaní vstrebávania a toxicity liečiv v organizme a úzko súvisí s rozpúšťacím teplom (entalpiou rozpúšťania). Naopak, "
        "bežné prepočty koncentrácií a výpočty pH vychádzajú z molárnej hmotnosti a rovnovážnych disociačných konštánt, nie zo samotnej rozpustnosti."
    ),
    48: (
        "Vlastnosti a zloženie roztokov sa kvantifikujú látkovou koncentráciou v mol·dm⁻³ (c = n/V), ktorá presne udáva počet mólov častíc "
        "v jednotke objemu. Rozpustnosť mr udáva hmotnosť látky v gramoch rozpustnej v 100 g rozpúšťadla, pričom látky s 0,1 < mr < 1 g "
        "považujeme za málo rozpustné. Hustota má vzorec ρ = m/V (nie V/m) a molalita má jednotku mol/kg (nie mol/dm³)."
    ),
    49: (
        "Rozpustnosť mr je definovaná ako maximálna hmotnosť látky, ktorá sa rozpustí v 100 g rozpúšťadla pri danej teplote za vzniku nasýteného "
        "roztoku. Väčšina halogenidov je vo vode dobre rozpustná, zatiaľ čo fluoridy kovov alkalických zemín (napr. CaF₂) sú prakticky "
        "nerozpustné kvôli vysokej mriežkovej energii. Tvrdenia, že rozpustnosť nezávisí od teploty, alebo že všetky hydroxidy sú vo vode "
        "rozpustné, sú v rozpore so základnými chemickými faktami."
    )
}

input_path = "scripts/chem_batches/batch_1.json"
output_path = "scripts/chem_batches/batch_1_explained.json"

with open(input_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions from {input_path}")
assert len(questions) == 50, f"Expected 50 questions, found {len(questions)}"
assert len(explanations) == 50, f"Expected 50 explanations, found {len(explanations)}"

for idx, q in enumerate(questions):
    assert idx in explanations, f"Missing explanation for index {idx}"
    q["explanation"] = explanations[idx]

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(questions)} explained questions to {output_path}")
