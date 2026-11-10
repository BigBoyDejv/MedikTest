import json

explanations = {
    251: (
        "Základný biogenetický zákon sformuloval nemecký biológ Ernst Haeckel v znení, že ontogenéza "
        "je skrátenou a zrýchlenou rekapituláciou fylogenézy. Ostatní uvedení vedci pôsobili v iných oblastiach: "
        "Charles Darwin položil základy evolučnej teórie prírodným výberom, Karl Linné zaviedol binomickú nomenklatúru "
        "a J. B. Lamarck vytvoril prvú ucelenú evolučnú hypotézu založenú na dedení získaných znakov."
    ),
    252: (
        "Homologické orgány majú rovnaký fylogenetický a embryonálny pôvod, no v dôsledku adaptácie na odlišné funkcie "
        "môžu mať rozličný tvar a funkciu (divergentná evolúcia). Príkladom sú modifikácie končatín cicavcov, krídla vtákov "
        "a ruky človeka, či perie vtákov a šupiny plazov. Orgány s rovnakou funkciou, ale odlišným pôvodom "
        "(napr. krídla vtákov a hmyzu) sú orgány analogické, vzniknuté konvergenciou."
    ),
    253: (
        "Analogické orgány vznikajú konvergentným vývojom – majú rôzny fylogenetický pôvod, no v dôsledku adaptácie na rovnaké podmienky "
        "majú podobný tvar a vykonávajú zhodnú funkciu. Typickým príkladom sú krídla vtákov (premenená predná končatina stavovca) "
        "a krídla hmyzu (vychlípeniny chitínovej kutikuly), alebo pľúcne vaky pavúkovcov a pľúca stavovcov. "
        "Orgány s rovnakým pôvodom (napr. ruka človeka a krídlo vtáka) sú naproti tomu homologické."
    ),
    254: (
        "Gastruláciou sa jednovrstvový zárodok (blastula) premieňa na dvojvrstvovú alebo trojvrstvovú gastrulu formovaním zárodočných listov. "
        "Pri dvojvrstvových živočíchoch (Diblastica) vznikajú ektoderm a endoderm, zatiaľ čo pri trojvrstvových (Triblastica) "
        "sa vytvára ektoderm, endoderm a stredný zárodočný list – mezoderm. Mezenchým je embryonálne väzivo a blastocel s celómom sú telové dutiny, "
        "nie samotné zárodočné vrstvy."
    ),
    255: (
        "Z mezodermu (stredného zárodočného listu) sa vyvíja kardiovaskulárny systém vrátane srdca a ciev, celá svalová sústava "
        "(kostrové, hladké aj srdcové svalstvo) a vnútorná oporná sústava stavovcov (kosti, chrupky a väzivá). "
        "Pokožka, zmyslové orgány a nervová sústava sú naopak ektodermového pôvodu, zatiaľ čo epitelová výstelka "
        "väčšiny tráviacej sústavy pochádza z endodermu."
    ),
    256: (
        "Ektoderm (vonkajší zárodočný list) dáva vznik pokožke (epidermis) a jej derivátom (srsť cicavcov, perie, rohovina, vonkajšia kostra článkonožcov), "
        "celej nervovej sústave a tiež okrajovým ektodermovým častiam tráviacej trubice (predná a koncová časť). "
        "Pečeň a stredné črevo sú endodermového pôvodu, zatiaľ čo cievna sústava a vnútorná kostra stavovcov "
        "sa diferencujú z mezodermu."
    ),
    257: (
        "Z endodermu (vnútorného zárodočného listu) vzniká epitelová výstelka strednej časti tráviacej rúry vrátane tenkého čreva "
        "a veľké tráviace žľazy, ako sú pečeň a pankreas, ako aj výstelka dýchacích ciest. Pokožka, nervová sústava "
        "a análny otvor sú ektodermové štruktúry, kým cievna sústava a kostra majú pôvod v mezoderme."
    ),
    258: (
        "Hlavnými energetickými a zásobnými látkami živočíšnych buniek sú lipidy (triacylglyceroly ukladané v tukovom tkanive) "
        "a zásobný polysacharid glykogén (ukladaný najmä v pečeni a kostrovom svale). Škrob a celulóza sú polysacharidy rastlinného pôvodu, "
        "ktoré živočíšne bunky nesyntetizujú. Bielkoviny a enzýmy plnia primárne funkciu stavebnú a katalytickú, nie zásobnú."
    ),
    259: (
        "Homeostáza je schopnosť organizmu udržiavať dynamickú stálosť vnútorného prostredia (napr. teploty, pH, glykémie či osmolarity) "
        "napriek neustálym výkyvom vonkajšieho prostredia. Zabezpečujú ju zložité neurohumorálne regulačné mechanizmy využívajúce negatívnu spätnú väzbu. "
        "Porucha zrážania krvi je hemofília, nerozlíšená pohlavnosť je hermafroditizmus a nervová regulácia je iba jednou zo zložiek riadenia."
    ),
    260: (
        "Epitely (výstelkové tkanivá) pokrývajú vonkajšie povrchy tela a vystielajú vnútorné dutiny; podľa funkcie ich delíme "
        "na krycí, žľazový, resorpčný (vstrebávací), zmyslový a obrvený (riaskový) epitel. Väzivo a chrupka patria medzi spojivové "
        "(podporné) tkanivá s bohatou medzibunkovou hmotou. Kutikula nie je bunkové tkanivo, ale nebunková vrstvička vylučovaná epidermálnymi bunkami."
    ),
    261: (
        "Žľazový epitel tvoria bunky vysoko špecializované na syntézu, sekréciu a vylučovanie špecifických látok (enzýmov, hormónov, hlienu), "
        "pričom predstavuje základný funkčný parenchým exokrinných aj endokrinných žliaz. Pokryv povrchu tela zaisťuje krycí epitel "
        "a zachytávanie zmyslových podnetov sprostredkúva zmyslový epitel. Žľazové bunky sú plnohodnotné jadrové bunky s rozvinutým proteosyntetickým aparátom."
    ),
    262: (
        "Epitelové tkanivá sú tvorené tesne k sebe priliehajúcimi bunkami usporiadanými do jednej alebo viacerých vrstiev, pričom nemajú vlastné cievne zásobenie "
        "a výživu prijímajú difúziou z ciev podkladového spojiva. Vyznačujú sa vysokou regeneračnou schopnosťou a zabezpečujú ochranu, sekréciu aj absorpciu látok. "
        "Hojná medzibunková hmota a mineralizácia sú naopak charakteristickým znakom spojivových tkanív (kostí a chrupky)."
    ),
    263: (
        "Deriváty pokožky (epidermis) cicavcov sú útvary vznikajúce rohovatením epidermálnych buniek bohatých na keratín, "
        "medzi ktoré patria nechty, kopytá, pazúry, rohy, srsť a modifikované chlpy – ostne (napr. u ježka). Šupiny rýb "
        "sú mezodermového pôvodu, perie je typickým derivátom pokožky vtákov a chitínová kutikula chráni bezstavovce."
    ),
    264: (
        "Základnou morfologickou a funkčnou jednotkou hladkého svalu je jednojadrová vretenovitá svalová bunka (myocyt / svalové vlákno tvorené jednou bunkou), "
        "ktorej kontraktilným aparátom v cytoplazme sú myofibrily. Viacjadrové svalové vlákna tvoria priečne pruhované kostrové svalstvo. "
        "Aktín a myozín sú jednotlivé kontraktilné myofilamenty, nie komplexné morfologicko-funkčné jednotky svalu."
    ),
    265: (
        "Spojivové tkanivá (spojivá) zabezpečujú oporu tela, spájanie a ochranu orgánov a metabolickú výmenu; tvoria ich väzivo, chrupka a kostné tkanivo, "
        "pričom z funkčného hľadiska sem patrí aj krv ako tekuté trofické spojivo. V oficiálnych testových podkladoch sú vyznačené možnosti zahŕňajúce väzivo, "
        "chrupku a kosti. Svaly, nervy a epitely predstavujú tri samostatné základné kategórie živočíšnych tkanív."
    ),
    266: (
        "Nervové tkanivo sa skladá z dvoch funkčne prepojených bunkových populácií: z neurónov (nervových buniek), ktoré tvoria a vedú nervové vzruchy, "
        "a z neuroglií (gliových buniek). Gliové bunky zabezpečujú štrukturálnu oporu, myelinizáciu, ochranu a metabolickú výživu neurónov. "
        "Neuróny sú vysoko diferencované jednojadrové bunky s dendritmi a neuritom (axónom), nie bunky bezjadrové či vakuolizované."
    ),
    267: (
        "Vnútorné oplodnenie nastáva splynutím spermie a vajíčka vo vnútri pohlavných ciest samice, spravidla po párení (kopulácii), "
        "čo chráni gaméty pred vyschnutím a je kľúčovou adaptáciou suchozemských živočíchov (plazov, vtákov, cicavcov, hmyzu). "
        "Pre väčšinu rýb a obojživelníkov je naopak typické vonkajšie oplodnenie vo vode. Vývin jedinca z neoplodneného vajíčka sa označuje ako partenogenéza."
    ),
    268: (
        "Vonkajšie oplodnenie prebieha mimo tela rodičovských organizmov vo vodnom prostredí, kde samice kladú vajíčka a samce ich zalievajú spermiami, "
        "čo je typické pre vodné organizmy (väčšinu rýb, obojživelníky) a primitívne bezstavovce. Pre suchozemské stavovce je nevyhnutné vnútorné oplodnenie, "
        "ktoré bráni dehydratácii gamét. Vývin vajíčka bez účasti spermie sa nazýva partenogenéza."
    ),
    269: (
        "Samčie gaméty živočíchov (spermie / spermatozoidy) vznikajú spermatogenézou v samčích pohlavných žľazách – semenníkoch (testes). "
        "Sú to malé, vysoko špecializované a aktívne pohyblivé haploidné bunky, ktorých hlavička je takmer celá vyplnená kondenzovaným jadrom nesúcim otcovskú DNA. "
        "Veľkými plazmatickými bunkami s bohatou zásobou živín sú naopak vajíčka, ktoré jediné môžu podliehať partenogenetickému vývinu."
    ),
    270: (
        "Nepohlavné (vegetatívne) rozmnožovanie prebieha mitotickým delením somatických (telových) buniek jediného rodičovského organizmu "
        "bez účasti pohlavných buniek, takže vzniknuté potomstvo tvorí geneticky identický klon. Ide o typický spôsob množenia jednobunkovcov (delenie) "
        "a primitívnych bezstavovcov (pučanie). Partenogenéza na rozdiel od neho patrí k pohlavnému rozmnožovaniu, pretože nový jedinec vzniká z gaméty (vajíčka)."
    ),
    271: (
        "Celóm (coeloma) je pravá druhotná telová dutina trojvrstvových živočíchov (Triblastica - Coelomata), ktorá je kompletne uzavretá "
        "a vystlaná mezodermálnym epitelom (peritoneom). Prvotná telová dutina (blastocel / pseudocel) naproti tomu nemá vlastnú mezodermovú výstelku. "
        "Celóm sa nevytvára už v blastule, ale vzniká až po gastrulácii v procese diferenciácie mezodermu."
    ),
    272: (
        "Hermafroditizmus (obojpohlavnosť) je stav, pri ktorom má ten istý jedinec vyvinuté samčie aj samičie gonády a tvorí oba typy gamét. "
        "Vyskytuje sa najmä u pomaly sa pohybujúcich alebo parazitických živočíchov (ploskavce ako motolice a pásomnice, suchozemské ulitníky, máloštetinavce), "
        "kde maximalizuje šancu na úspešné rozmnoženie. Rozdelenie populácie na samčích a samičích jedincov sa označuje ako gonochorizmus."
    ),
    273: (
        "Gonochorizmus (oddelené pohlavie) znamená diferencovanú pohlavnosť, pri ktorej sú samčí a samičí jedinci striktne oddelení. "
        "Jedinci sa odlišujú primárnymi pohlavnými znakmi (prítomnosťou samčích alebo samičích pohlavných žliaz a príslušných gamét). "
        "Stav, keď má jeden organizmus oba typy funkčných pohlavných orgánov súčasne, je hermafroditizmus."
    ),
    274: (
        "Sexuálny dimorfizmus (pohlavná dvojtvarosť) je morfologická a funkčná odlišnosť samčích a samičích jedincov toho istého druhu, "
        "ktorá sa prejavuje v primárnych (gonády) aj sekundárnych pohlavných znakoch (veľkosť tela, sfarbenie, parohy, hlas). "
        "Vyskytuje sa výlučne u druhov s oddeleným pohlavím (gonochoristov), napríklad u hmyzu, vtákov a cicavcov. "
        "Hermafrodity (napr. pásomnice) majú obe pohlavia v jednom tele, takže nevykazujú pohlavnú dvojtvarosť."
    ),
    275: (
        "Partenogenéza je osobitná forma pohlavného rozmnožovania, pri ktorej dochádza k vývinu nového plnohodnotného jedinca "
        "z neoplodneného vajíčka bez účasti spermie. Bežne sa vyskytuje u hmyzu (napr. vznik trúdov u včiel), vošiek, perloočiek či niektorých plazov. "
        "Vývin jedinca zo somatických buniek predstavuje nepohlavné rozmnožovanie, zatiaľ čo vývin oplodneného vajíčka je štandardné amfimiktické rozmnožovanie."
    ),
    276: (
        "Oogamia je najrozšírenejší a evolučne najpokročilejší typ heterogamie mnohobunkových živočíchov, pri ktorom dochádza "
        "k splynutiu veľkej, bohatej na živiny a nepohyblivej samičej gaméty (vajíčka) s malou, aktívne pohyblivou samčou gamétou (spermiou). "
        "Tento spôsob oplodnenia je typický pre mnohobunkovce. Vývin bez oplodnenia je partenogenéza a výmena jadier u nálevníkov je konjugácia."
    ),
    277: (
        "Samooplodnenie (autogamia) je u hermafroditov zriedkavý fenomén a slúži ako núdzový mechanizmus pri absencii partnera, "
        "bežný je však u solitérnych endoparazitov, akými sú pásomnice. Väčšina voľne žijúcich hermafroditov (napr. dážďovky a slimáky) preferuje "
        "vzájomné krížové oplodnenie, pričom samooplodneniu bráni morfologická stavba alebo časový posun v dozrievaní spermií a vajíčok (proterandria)."
    ),
    278: (
        "Vajcoživorodosť (ovoviviparia) spočíva v tom, že oplodnené vajíčka sa vyvíjajú v tele samice bez placenty (zárodok vyživuje žĺtok) "
        "a mláďatá sa liahnu priamo počas kladenia vajíčok alebo bezprostredne po ňom. Vyskytuje sa u gonochoristov, napr. u niektorých obojživelníkov (mlokov), "
        "plazov (vretenica) a klepietkavcov (škorpióny). Vtáky sú striktne vajcorodé (oviparné) a kladú vajíčka vyžadujúce inkubáciu."
    ),
    279: (
        "Vajíčka cicavcov sú alecitálne (obsahujú minimum žĺtka), pretože výživu zárodku zabezpečuje materský organizmus cez placentu. "
        "Vajíčka obojživelníkov majú ochranné rôsolovité obaly a u obrúčkavcov bielkovinové sekréty opasku obklopujú viacero vajíčok v kokóne. "
        "Spermie (nie vajíčka) majú stavbu s hlavičkou a bičíkom a vajíčka hlavonožcov obsahujú veľké množstvo žĺtka."
    ),
    280: (
        "Ontogenéza (individuálny vývin jedinca) zahŕňa celý životný cyklus organizmu od momentu oplodnenia (vzniku zygoty) až po jeho smrť. "
        "Ide o geneticky naprogramovaný proces, ktorý sa delí na embryonálnu etapu (ryhovanie, gastrulácia, organogenéza) "
        "a postembryonálnu etapu (rast, dospievanie, reprodukcia, starnutie). Ontogenéza sa teda nekončí vyliahnutím ani produkciou potomstva, ale až zánikom jedinca."
    ),
    281: (
        "Embryonálny vývin zahŕňa všetky procesy od vzniku zygoty po narodenie alebo vyliahnutie: brázdenie (ryhovanie) vajíčka "
        "(aj neoplodneného pri partenogenéze), vznik blastuly a gastruláciu, diferenciáciu troch zárodočných vrstiev "
        "a následnú organogenézu s bunkovou diferenciáciou. Spermie sú konečne diferencované gaméty, ktoré sa nebrázdia, "
        "a partenogenéza prebieha zásadne z vajíčka neoplodneného."
    ),
    282: (
        "Spermatozoidy sú pohyblivé samčie gaméty nesúce haploidnú sadu chromozómov, ktoré vznikajú meiózou pri spermatogenéze. "
        "Ich telo sa skladá z hlavičky s kondenzovaným genetickým materiálom a akrozómom, krčka s mitochondriami dodávajúcimi energiu "
        "a bičíka zabezpečujúceho aktívny pohyb. Zásobné látky a organely pre počiatočný vývin embrya poskytuje takmer výlučne vajíčko."
    ),
    283: (
        "Samičie gaméty (vajíčka) vznikajú v samičích pohlavných žľazách – vaječníkoch (ováriách) meiotickým redukčným delením, "
        "preto sú haploidné. U živočíchov sú vajíčka vždy nepohyblivé veľké bunky obsahujúce zásoby žĺtka pre vývin zygoty. "
        "Vznikajú z prapohlavných buniek procesom oogenézy, nie mitózou somatických buniek. V oficiálnych testových podkladoch sú vyznačené možnosti a, b, d."
    ),
    284: (
        "Vajíčka sú samičie haploidné gaméty vznikajúce meiózou z diploidných primárnych oocytov vo vaječníkoch. "
        "Obsahujú bunkové jadro a zásobu živín (žĺtok) v cytoplazme, pričom ide o nepohyblivé bunky prispôsobené na oplodnenie spermiou. "
        "Sú chránené rôznymi typmi obalov (rôsolovité, blanité, vápenaté), pričom v semenníkoch sa tvoria výhradne samčie gaméty."
    ),
    285: (
        "Vonkajšie schránky jednobunkovcov (napr. dierkavcov a mrežovcov) slúžia ako ochranná a oporná schránka bunky. "
        "Sú mineralizované a chemicky tvorené najčastejšie uhličitanom vápenatým (CaCO3 u Foraminifera) alebo oxidom kremičitým (SiO2 u Radiolaria). "
        "Neplnia funkciu lokomócie (tú zaisťujú panôžky, bičíky či brvy), neobsahujú celulózu a nenahrádzajú cytoplazmatickú membránu."
    ),
    286: (
        "Pokožka (epidermis) mnohobunkových živočíchov je povrchová vrstva tela ektodermového pôvodu, ktorá chráni organizmus pred vonkajším prostredím. "
        "Môže byť tvorená jednovrstvovým epitelom (často obrveným, napr. u ploskulíc) alebo viacvrstvovým epitelom (u stavovcov) a obsahuje krycie aj žľazové bunky. "
        "Jednobunkovce tkanivovú pokožku nemajú a mezoderm tvorí hlbšie uloženú zamšu a svalovinu."
    ),
    287: (
        "Koža stavovcov obsahuje rôzne typy exokrinných žliaz epidermálneho pôvodu: slizové a jedové žľazy u obojživelníkov a rýb, "
        "a mazové, potné, pachové a mliečne žľazy u cicavcov. Slinné žľazy ústia výhradne do dutiny úst a pohlavné žľazy (gonády) "
        "sú vnútorné orgány mezodermového pôvodu, takže v koži sa nenachádzajú."
    ),
    288: (
        "Koža cicavcov pozostáva z troch základných vrstiev: pokožky (epidermis), zamše (dermis / corium) a podkožného väziva (subcutis). "
        "Pokožka je tvorená viacvrstvovým dlaždicovým zrohovateným epitelom ektodermového pôvodu, zatiaľ čo zamša a podkožie sú mezodermové väzivové vrstvy. "
        "Kutikula je povrchovou vrstvou bezstavovcov a perie je derivátom pokožky vtákov."
    ),
    289: (
        "Celý vonkajší povrch kosti, s výnimkou kĺbových plôch krytých hyalínovou chrupkou, pokrýva okostica (periost). "
        "Okostica je tuhá, bohato cievne a nervovo zásobená väzivová blana, ktorej vnútorná vrstva osteoblastov zabezpečuje rast kosti do hrúbky a regeneráciu po zlomeninách. "
        "Spongiózne tkanivo a kostná dreň sa nachádzajú vo vnútri kosti, nie na jej povrchu."
    ),
    290: (
        "Kostru trupu stavovcov tvorí chrbtica (columna vertebralis) a kostra hrudníka tvorená hrudnými stavcami, rebrami a hrudnou kosťou. "
        "Celá táto kostra je vybudovaná z pevných spojivových tkanív – z kostného tkaniva, chrupky (rebrové chrupky, medzistavcové platničky) a spevňujúceho väziva. "
        "Lebka tvorí samostatnú kostru hlavy, končatiny patria do apendikulárnej kostry a svaly sú súčasťou pohybovej, nie opornej sústavy."
    ),
    291: (
        "Fylogenetickým aj embryonálnym základom vnútornej kostry chordátov a stavovcov je chrbtová struna (chorda dorsalis). "
        "Ide o pružný osový povrazec buniek bohatých na vakuoly a glykogén, ktorý sa zakladá odštiepením zo strechy prvočreva (v testovom ponímaní endodermového pôvodu). "
        "U dospelých stavovcov je chorda zatlačená a funkčne nahradená chrbticou tvorenou mezodermovými stavcami."
    ),
    292: (
        "Väzivo je mäkké spojivové (podporné a výplňové) tkanivo charakteristické hojnou medzibunkovou hmotou s kolagénovými a elastickými vláknami. "
        "Tvorí šľachy, väzy kĺbov a puzdrá orgánov a vypĺňa medziorgánové priestory v tele. "
        "Medzistavcové platničky a kostra drsnokožcov sú z chrupkového tkaniva, a mineralizovanú pevnú štruktúru vytvára kostné tkanivo."
    ),
    293: (
        "Povrch tela článkonožcov je tvorený jednovrstvovým epitelom pokožky (hypodermis), ktorý smerom von secernuje pevnú nebunkovú vrstvu – chitínovú kutikulu. "
        "Kutikula slúži ako vonkajšia kostra (exoskelet) spevnená inkrustáciou a sklerotizáciou a bráni strate vody. "
        "Viacvrstvový epitel pokožky majú stavovce, spongín tvorí oporu tiel hubiek a pelikula je povrchovou štruktúrou prvokov."
    ),
    294: (
        "Celá kostra stavovcov sa skladá z troch hlavných anatomických a funkčných celkov: kostry lebky (mozgová a tvárová časť), "
        "kostry trupu (chrbtica a hrudník s rebrami) a kostry končatín (predné a zadné, resp. horné a dolné končatiny vrátane pletencov). "
        "Jednotlivé možnosti ako iba lebka alebo trup s končatinami predstavujú len čiastkové komponenty celkovej kostry."
    ),
    295: (
        "Jednobunkové organizmy sa pohybujú pomocou špecializovaných pohybových organel: panôžok (pseudopódií u meňaviek), "
        "bičíkov (u bičíkovcov) a bŕv (u nálevníkov). Pohyb bŕv a bičíkov je založený na usporiadaní mikrotubulárnych štruktúr (axonéma 9+2) "
        "a motorových proteínoch (dyneín). Svalové tkanivá a kožnosvalový vak sú štruktúry mnohobunkovcov a pulzujúca vakuola slúži na osmoreguláciu."
    ),
    296: (
        "Kinéza je nedisponovaný (nesmerovaný) lokomočný pohyb primitívnych organizmov alebo jednobunkovcov v reakcii na podnet, "
        "pri ktorom stimul vyvoláva zrýchlenie alebo spomalenie pohybovej aktivity či zmenu frekvencie obratov, nie však priamu orientáciu k zdroju. "
        "Smerovaný pohyb k podnetu alebo od neho sa označuje ako taxia. Znížená aktivita v nepriaznivých podmienkach je anabióza."
    ),
    297: (
        "Kostrové svalové vlákna stavovcov sa delia na pomalé červené vlákna a rýchle biele vlákna. Červené vlákna obsahujú veľa myoglobínu "
        "a mitochondrií, kontrahujú sa pomalšie, pracujú aeróbne a sú prispôsobené na dlhodobú vytrvalú prácu bez rýchlej únavy. "
        "Biele vlákna majú menej myoglobínu, sťahujú sa rýchlo a silno pomocou anaeróbnej glykolýzy, no rýchlo sa unavia a tvoria kyslíkový dlh."
    ),
    298: (
        "Pomalé svalové vlákna kostrových svalov (červené vlákna, typ I) obsahujú veľké množstvo myoglobínu, cievnych kapilár a mitochondrií, "
        "vďaka čomu pracujú prevažne aeróbnym metabolizmom. Sú mimoriadne odolné voči únave a uspôsobené na dlhodobú vytrvalostnú prácu "
        "(napr. v lietacích svaloch vytrvalých vtákov a posturálnych svaloch človeka). Ako všetky kostrové svalové vlákna ide o mnohojadrové útvary."
    ),
    299: (
        "Hladké svalové tkanivo je tvorené jednojadrovými vretenovitými bunkami (myocytmi) a zabezpečuje pomalé, mimovôľové kontrakcie. "
        "U stavovcov tvorí svalovú vrstvu stien dutých vnútorných orgánov (tráviaci trakt, cievy, maternica) riadenú autonómnym nervovým systémom a hormónmi, "
        "pričom u nižších bezstavovcov (napr. červov) zabezpečuje celkový pohyb tela. Kostrové svaly stavovcov sú naopak tvorené priečne pruhovaným svalstvom."
    ),
    300: (
        "Hladké svaly zabezpečujú tonické kontrakcie s nízkou spotrebou energie, preto sú takmer neunaviteľné, hoci sa kontrahujú pomalšie a menšou silou "
        "než priečne pruhované svaly. Tvoria svalovinu stien tráviacej rúry aj ciev a ich aktivita je regulovaná látkovo (hormónmi), vegetatívnym nervstvom "
        "aj fyzikálnymi vplyvmi (napr. teplotou). Nepodliehajú vôľovému riadeniu somatickým nervovým systémom, ktorý ovláda výhradne kostrové svaly."
    ),
}

with open('scripts/bio_batches/batch_6.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions from batch_6.json")
assert len(questions) == 50

# Apply explanations
for i, q in enumerate(questions):
    q_num = 251 + i
    assert q_num in explanations, f"Missing explanation for question {q_num}"
    q['explanation'] = explanations[q_num]

# Save to batch_6_explained.json
output_path = 'scripts/bio_batches/batch_6_explained.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(questions)} explained questions to {output_path}")
