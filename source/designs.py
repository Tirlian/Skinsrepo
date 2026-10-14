"""Authored character-specific masks. Each string is drawn directly at native resolution.
Not an image downsampling pipeline. Names/IDs are read from the user's V4 package.
"""
from dataclasses import dataclass, field

@dataclass
class Design:
    id: str
    main: str
    second: str
    accent: str
    hair: str
    skin: str
    fringe: tuple
    front: str
    back: str
    sleeves: str = 'jacket'
    pants: str = '263041'
    boots: str = '1d2330'
    eyes: str = '458f87'
    hair_style: str = 'short'
    feature: str = ''
    leg_style: str = 'trousers'
    note: str = ''

D=[]
def add(id,main,second,accent,hair,skin,fringe,front,back,**kw):
    D.append(Design(id,main,second,accent,hair,skin,tuple(fringe),front,back,**kw))

# Token map: a primary cloth, b secondary cloth, c accent, w ivory, k undershirt,
# s skin, l leather, m metal, p trousers, x dark seam. Slash separates native pixel rows.
add('freya','277f76','f2dfbd','e99457','934525','e8b190',(3,3,2,1,2,3,4,5),
    'aawsswaa/aaawwaa a/aalwkwaa/aaalwwaa/acwalwaa/aaawalwa/aawwwall/aawwwaal/lllmmlll/pppappap/pppppppp/pppppppp'.replace(' ',''),
    'aahhhhaa/aahhhhaa/aaahhaaa/aaaahhaa/aaalhaaa/aalaaala/aalbaala/aallllla/aaalllaa/pppppppp/pppppppp/pppppppp',
    hair_style='braid',feature='clip',sleeves='bomber',pants='314958',eyes='2d877b',note='Kupferfarbener Seitenzopf; türkis-cremefarbene Kurzjacke, orange Haarspange und braune Umhängetasche.')
add('kian','303b51','a9323e','72a65e','382d32','c99776',(4,2,3,2,1,2,3,4),
    'bbassaaa/bbakkbaa/bbakkbaa/baakkbaa/bcckkbaa/aaakkbaa/aaakkbaa/aakkkbaa/aabbbbaa/pppppppp/pbpppppp/pbpppppp',
    'bbkkkkbb/abbkkbba/abbbbbba/aaaaaaba/aaaaaaba/aaaccaab/aaaccaaa/aaaaaaaa/aabbbbaa/pppppppp/pbpppppp/pbpppppp',
    hair_style='spiky',feature='earstud',sleeves='racing',pants='202a3c',eyes='579346',leg_style='sneakers',note='Dunkle wilde Haare; diagonal geteilte rote Sportjacke, grünes Geckarbor-Abzeichen, hohe Sneakers.')
add('gym_fire','292936','962b38','ee6927','c12d32','d99a78',(3,4,3,2,1,2,3,4),
    'aaassaaa/acaskbaa/abckkbaa/abbckbaa/abbckbaa/abkkcbaa/abmkkcba/abkkkmca/lllcmlll/aappppaa/pppppppp/pppppppp',
    'abaaaaba/aabbbbaa/aaabbaaa/aaaaacaa/aaaaccaa/aaacccaa/aacbcaaa/aacccaaa/aaaaacaa/abaaaaba/pppppppp/pppppppp',
    hair_style='flame',feature='brow',sleeves='fire',pants='232734',boots='252331',eyes='b74028',leg_style='strapboots',note='Scharlachroter asymmetrischer Haarschopf, orange Spitzen auf beiden Ebenen. Anthrazit-Bikerjacke mit Kupferzipper, ein roter Ärmel, schwere Stiefel.')
add('gym_normal','947b65','4d655f','be9252','614637','e0b090',(2,2,2,2,3,3,4,3),
    'wwassaww/wawwwwaa/aaawwaaa/aabwbaaa/aabbbaaa/aaabaaaa/aaawaaaa/aambamma/aaaawaaa/lllmmlll/pppppppp/pppppppp',
    'aaaaaaaa/aaaawaaa/aaaaaaaa/aaaaaaaa/aaabaaaa/aaaaaaaa/aaaxaaaa/aaaxaaaa/aaaawaaa/lllmmlll/pppppppp/pppppppp',
    hair_style='bob',feature='glasses',sleeves='rolled',pants='51443c',eyes='397569',leg_style='loafers',note='Kastanienbrauner Bob, eckige Lesebrille, salbeifarbene Weste unter beigefarbenem Cardigan und Loafer.')
add('gym_water','e0e8df','275770','4bb6bc','3f9fa9','dfac94',(2,3,3,2,2,3,4,5),
    'ccassacc/abassaba/aabbbbaa/abwbbwba/abbwwbba/abbwbbaa/abbbbbba/abmmmbba/abbbbbba/abppppba/abppppba/abppppba',
    'aahhhhaa/aaahhhaa/aaaaahha/abbbaaha/abbbwbaa/abbwbbba/abwbwbba/abbbbbba/abmmmbba/abppppba/abppppba/abppppba',
    hair_style='long_side',feature='pearl',sleeves='nautical',pants='28475d',eyes='295fa4',leg_style='tallboots',note='Meeresgrünes seitliches langes Haar. Elfenbeinfarbener Hafenmantel, marineblaues Oberteil und ein einzelner Perlenohrring.')
add('gym_electric','292943','d6a538','65c7d2','644092','b68161',(1,1,2,2,3,4,4,3),
    'bbakkabb/bbakkkab/baakkkab/bmmakkab/baakkcab/aacckcab/aacakcab/aacakkab/aaakkkab/lllmmbll/pppppbpp/pppppbpp',
    'bbbbbbaa/aaxaaaab/aaxccaaa/aaxacaaa/aaxaccca/aaxaaaac/aaxxacca/aaaaccaa/aaakkkab/lllmmbll/pppppbpp/pppppbpp',
    hair_style='undercut',feature='headphones',sleeves='tech',pants='343544',eyes='4eabb1',leg_style='sneakers',note='Violetter Undercut und einseitiger Kopfhörer; kurze gelbe Techjacke mit anthrazitfarbenem Rumpf, türkisfarbene Leitermotive.')
add('gym_grass','52764c','a1ae6b','dcc37e','425438','c38c67',(3,2,2,1,2,3,4,5),
    'bbassabb/bbbaabbb/bbaaaabb/bbaaacbb/bbaaacbb/baacccab/baacaaab/aaacaaaa/baaaabab/ppbabbpp/pppppppp/pppppppp',
    'bbahhabb/bbbhhbbb/bbahhabb/bbaaahbb/bbaabhbb/bbaachbb/baabcabb/aaaacaaa/baaaabab/ppbabbpp/pppppppp/pppppppp',
    hair_style='braid_left',feature='leaf',sleeves='linen',pants='63594a',eyes='756638',leg_style='hiking',note='Moosgrüner Flechtzopf und Blattspange, kurzer geometrischer Poncho über Leinenärmeln, Wanderstiefel.')
add('gym_ice','bad7de','364968','f1eee2','a5c4d9','e6bbad',(3,3,2,2,1,2,3,5),
    'cccssccc/cccccccc/acccccca/aaakkbaa/aaakkbaa/aaackbaa/aaackbaa/abackbba/aaaakbaa/ccackccc/aappppaa/aappppaa',
    'ccchhhcc/ccchhhcc/acchhcca/aaahhaaa/aaaahhaa/aaaahaaa/aaacaaaa/aaacaaaa/aaaaaaaa/cccccccc/aappppaa/aappppaa',
    hair_style='long',feature='snowclip',sleeves='fur',pants='293951',eyes='5a84ad',leg_style='winter',note='Eisblaues langes Haar, breite helle Fellkante und gestrickte Ärmel. Kurze Winterjacke über schmalen dunklen Hosen.')
add('gym_fighting','ded4b7','ad463a','5e8b86','272b31','bf8564',(2,1,1,2,2,2,1,2),
    'ssassass/ssaassas/saaaassa/saaaaaaa/aaaabaaa/aaaabaaa/aaaabaaa/bbbbcbbb/bbbbcbbb/aaaaaaba/aaaaaaba/aaaaaaba',
    'ssaaaass/ssaaaass/saaaaaas/saaaaaas/aaaaaaaa/aaaaaaaa/aaaaxaaa/bbbbcbbb/bbbbcbbb/aaaaaaba/aaaaaaba/aaaaaaba',
    hair_style='topknot',feature='headband',sleeves='wraps',pants='cfc4a7',boots='423932',eyes='815237',leg_style='martial',note='Dunkler Haarknoten mit rostrotem Stirnband, ärmelloser cremefarbener Gi, grüne Gürtelmarke und Unterarmbandagen.')
add('gym_poison','362c4c','7854a4','a3d865','b59ad0','d8a387',(1,1,2,3,4,4,5,5),
    'abassabb/abakkkbb/ababkkbb/abbbmkbb/abbbbmbb/aabbkkbb/aaackkbb/amccmkbb/lllmmlll/pppppppp/ppppbppp/ppppbppp',
    'aaaaabbb/aaaabbbb/aaabbbbb/aabbbabb/abbbaabb/bbbbaabb/bbbaabbb/bbaaabbb/lllmmlll/pppppppp/ppppbppp/ppppbppp',
    hair_style='undercut_long',feature='earrings',sleeves='poison',pants='282d34',eyes='788f43',leg_style='strapboots',note='Lila Seitenscheitel über einem Auge, rasierte Gegenseite, kurzer urbaner Mantel mit grünen Reagenzgläsern am Gürtel.')
add('gym_ground','9c704c','d4bd86','679796','a5532e','be8561',(2,3,2,2,1,2,2,3),
    'bba ssabb/bbbssbbb/ablbblla/aaallbaa/ababllaa/ababalaa/aaaaalll/aaamaala/lllmmlll/aaapppaa/aaapppaa/pppppppp'.replace(' ',''),
    'bbbbbbbb/aaaaaaal/aaalllla/aallbbll/aallbbll/aalllbll/aaalllll/aaaaaala/lllmmlll/aaapppaa/aaapppaa/pppppppp',
    hair_style='cropped',feature='goggles',sleeves='expedition',pants='69513e',boots='453b32',eyes='627d68',leg_style='cargo',note='Kurzer kupferfarbener Haarschnitt und hochgeschobene Schutzbrille. Staubmantel, gekreuzte Ledergurte, Kompass und Cargohose.')
add('gym_flying','46687b','d5c7a9','c98345','c39a5d','d7a185',(3,2,1,2,3,4,3,2),
    'bbassabb/bbbssbbb/abbbbbaa/abkkkbaa/abkkkbaa/ackkkbaa/aaakkbaa/aaakkbma/aabbbbaa/lllmmlll/pppppppp/pppppppp',
    'bbbbbbbb/abbbbbba/aaaabaaa/aaabbaaa/aaaabaaa/aaacacaa/aaccccc a/aaaacaaa/aabbbbaa/lllmmlll/pppppppp/pppppppp'.replace(' ',''),
    hair_style='windswept',feature='aviator',sleeves='bomber',pants='344858',boots='463d38',eyes='50869a',leg_style='hiking',note='Sandblonder windzerzauster Pony, Pilotenbrille auf der Stirn und cremefarbener Schal; blaue Fliegerjacke mit Flügelnaht.')
add('gym_psychic','604b83','aa6c9b','e4b675','70449a','d6a58b',(3,3,3,2,2,3,3,3),
    'baassabb/baassbba/abaaabaa/aaabaaab/aaaabaaa/aaaabaaa/cccccccc/aabbbaaa/aaabbaaa/aaaabaaa/aaaabaaa/aaaabaaa',
    'bahhhhab/bahhhhab/aahhhhaa/aahhhhaa/aaahhaaa/aaaahaaa/cccccccc/aaaacaaa/aaacacaa/aaaacaaa/aaaaaaaa/aaaaaaaa',
    hair_style='long_straight',feature='diadem',sleeves='wide',pants='47355e',boots='2c293e',eyes='bd718d',leg_style='robe',note='Amethystfarbener gerader Pony, schmale Sternspange und asymmetrisch geschlossener violetter Mantel mit breiter Schärpe.')
add('gym_bug','688157','d0b271','657eae','ab863f','ddb18d',(3,3,3,4,3,3,4,3),
    'bbassabb/babssbab/babwa bab/baa a aaab/baaaa aab/baacaaab/bammm aab/baaaaaab/aaaaxaaa/aaaaxaaa/pppppppp/pppppppp'.replace(' ',''),
    'bbbbbbbb/babbbbab/bbab babb/bbaaaabb/bbaaaabb/bbaaaabb/bbaaaabb/bbaaaabb/aaaaxaaa/aaaaxaaa/pppppppp/pppppppp'.replace(' ',''),
    hair_style='bowl',feature='roundglasses',sleeves='short',pants='526448',boots='4e4634',eyes='6c955a',leg_style='shorts',note='Ockerfarbener Pilzkopf, runde Feldbrille und grüne Latzhose über hellen kurzen Ärmeln; kleiner Probenrucksack.')
add('gym_rock','636e77','a88d69','dfb554','555b65','bc9072',(1,2,1,1,2,2,1,2),
    'bbassabb/abassaba/aaallaaa/aallalaa/aalkala a/aalkaaaa/aaamaaaa/aalkaaaa/lllmllll/aapp p paa/pppppppp/pppppppp'.replace(' ',''),
    'aaaaaaaa/aaalllaa/aaalllaa/aallblla/aallblla/aallblla/aaalllaa/aaaaaaaa/lllmllll/aappppaa/pppppppp/pppppppp',
    hair_style='short',feature='beard',sleeves='rolled',pants='4c514d',boots='413b34',eyes='698790',leg_style='hiking',note='Schiefergraues kurzes Haar, kantiger Bart, robuste Feldweste, Klettergurt und gelbe Karabiner.')
add('gym_ghost','302d45','585577','aea2bc','222638','dfb6ac',(4,5,4,3,2,2,3,4),
    'aaassaaa/aaacaaaa/aawkkwaa/aaakkbaa/aaakkbaa/aaakkbaa/aamkkbaa/aaakkbaa/aaakkbaa/aaappaaa/aaappaaa/aaappaaa',
    'aahhhhaa/aahhhhaa/aaahhaaa/aaaaaaba/aaaccaaa/aaccccaa/aaacccaa/aaaacaaa/aaaaaaaa/aaaxaaaa/aaaxaaaa/aaaxaaaa',
    hair_style='fringe',feature='monocle',sleeves='coat',pants='252638',boots='242335',eyes='8d74ba',leg_style='coat',note='Tiefdunkler asymmetrischer Pony, ein blasses Monokel, langer auberginefarbener Mantel, schmale silberne Schließe.')
add('gym_dragon','39485c','728495','c79354','24394c','b67c62',(2,3,4,3,2,1,2,4),
    'bbbssbbb/bbcsscbb/abkkkkba/abkkkkba/abckkcba/abkcckba/aabkkbaa/aabbbaaa/lllmllll/abppppba/abppppba/abppppba',
    'bbbbbbbb/bbaaaabb/abacabba/abaccbba/abccccba/abaccbba/abacabba/abbbbbba/lllmllll/abppppba/abppppba/abppppba',
    hair_style='swept_back',feature='scar',sleeves='bracer',pants='30303f',boots='33313b',eyes='ac8152',leg_style='coat',note='Dunkelblau zurückgelegtes Haar, kupferner Schuppenverschluss und wetterfester Reisemantel; eine verstärkte Schulter.')
add('gym_dark','252e3d','695a65','b8bfc6','d5d7d8','c78f7c',(2,2,3,4,5,5,4,3),
    'abassaaa/abassaaa/abkkkaaa/abbkkaa a/abckcaaa/abkkkaaa/abkmkaaa/abbkkaaa/lllmmlll/aappppaa/pppppppp/pppppppp'.replace(' ',''),
    'aaaaaaaa/aaaabaaa/aaabbbaa/aabbbbaa/aabbbbaa/aaaabaaa/aaaaaaam/aaaaaamm/lllmmlll/aappppaa/pppppppp/pppppppp',
    hair_style='fringe_right',feature='earrings',sleeves='asym',pants='373039',boots='212936',eyes='946276',leg_style='strapboots',note='Weißer schräger Pony über einem Auge, dunkle kurze Jacke mit asymmetrischer Weste, silberne Kette und ein offener Ärmel.')
add('gym_steel','4a6270','929ea0','d2a65c','697780','c58f73',(1,1,2,3,3,2,2,1),
    'bbassabb/abassaba/abbbbbba/abammaba/abakkaba/abakkaba/aabbbbaa/aackkcaa/lllmmlll/aappppaa/aappppaa/pppppppp',
    'bbbbbbbb/bbaaaabb/abaaaaba/abammaba/abak kaba/abakkaba/aabbbbaa/aaacca aa/lllmmlll/aappppaa/aappppaa/pppppppp'.replace(' ',''),
    hair_style='undercut',feature='visor_up',sleeves='mechanic',pants='354551',boots='28323d',eyes='527f87',leg_style='workboots',note='Stahlgrauer Undercut, hochgeklapptes Schutzvisier, blaue Arbeitsschürze, matte Metallbeschläge und verstärkte Handschuhe.')
add('gym_fairy','c48caa','e8d7c8','8ac4b8','b85d80','e7b19b',(2,3,2,3,3,2,3,4),
    'bbassabb/bbassabb/bbbccbbb/abcb bcba/aaabb aaa/aaaabaaa/aaaabaaa/cccccccc/abbbbbba/babbbbab/bbbaabbb/aaaaaaaa'.replace(' ',''),
    'bbahhabb/bbbhhbbb/bbbhhbbb/aaahhaaa/aaahhaaa/aaaahaaa/aaaaaaaa/cccccccc/abbbbbba/babbbbab/bbbaabbb/aaaaaaaa',
    hair_style='twintail',feature='ribbon',sleeves='puff',pants='756878',boots='6a4c62',eyes='7e8f6c',leg_style='skirt',note='Rosenfarbene Zöpfe, mintfarbene Schleife, roséfarbene Cape-Jacke über Faltenrock und cremefarbenen Ärmeln.')

# Liga: independent silhouettes, not five copies of a suit.
add('league_tirlian','292f3d','685431','deb663','1f2938','d4a080',(3,2,2,3,4,3,2,3),
    'aaassaaa/abassaba/abkcckba/abkc ckba/abkcckba/abkkkkba/abkkkkba/abckkcba/lllcc lll/abppppba/abppppba/abppppba'.replace(' ',''),
    'abaaaaba/aaabbaaa/aaaacaaa/aaccccc a/aa caccaa/aaacacaa/aaaacaaa/aaaaaaaa/lllcclll/abppppba/abppppba/abppppba'.replace(' ',''),
    hair_style='windswept',feature='goldstud',sleeves='formal',pants='303340',eyes='687d96',leg_style='coat',note='Fiktiver Top-4-Trainer: dunkles Haar, anthrazitfarbener langer Trainerrock und zurückhaltendes goldenes Sonnenprisma. Keine Porträtbehauptung.')
add('league_cassia','674052','be929f','c7a667','692d47','c99183',(3,3,3,3,2,3,3,4),
    'bbassabb/bbssabba/abbbabaa/aabbab aa/aaabaaaa/aaabaaaa/cccccccc/baaaaabb/aabbbbba/aaabbbba/aaaaabba/aaaaaaba'.replace(' ',''),
    'bahhhhab/bahhhhab/aahhhhaa/aahhhhaa/aaahhaaa/aaaahaaa/cccccccc/baaaaaab/aabbbbaa/aaabbaaa/aaaabaaa/aaaaaaaa',
    hair_style='long_straight',feature='hairpin',sleeves='wide',pants='4d3549',eyes='b58b69',leg_style='robe',note='Weinrotes langes Haar, goldene Haarnadel, überkreuzter Seidenmantel und breite perlmuttfarbene Schärpe.')
add('league_orion','354d69','69869b','bdc9cd','9baebe','af7d65',(1,2,2,1,1,2,3,2),
    'bbassabb/abassaba/abbccbaa/abbbbbba/abmkkbba/abkkkkba/abmkkbba/abkkkkba/cccccccc/abppppba/abppppba/abppppba',
    'bbbbbbbb/abbcc bba/aabbbbaa/aaaaaaaa/aaacaaaa/aaacaaaa/aaaacaaa/aaaacaaa/cccccccc/abppppba/abppppba/abppppba'.replace(' ',''),
    hair_style='short',feature='beard_trim',sleeves='formal',pants='273a50',eyes='547f9d',leg_style='tallboots',note='Silberblauer kurzer Schopf und schmaler Bart, zweireihige dunkelblaue Uniform mit hellen Metallknöpfen.')
add('league_lys','496c6a','bac8ab','d3b866','455b42','cda886',(3,2,3,4,3,2,3,4),
    'bbassabb/bbbssbbb/babbbbab/abaaaa ba/aaabaaaa/aabacaaa/abacacaa/aaacaaaa/cccccccc/abppppba/abppppba/abppppba'.replace(' ',''),
    'bbahhabb/bbbhhbbb/babhhbab/abahaaaa/aaahaaaa/aaahaaaa/aaahaaaa/aaaacaaa/cccccccc/abppppba/abppppba/abppppba',
    hair_style='braid_left',feature='leafpin',sleeves='linen',pants='354a47',eyes='816e41',leg_style='coat',note='Moosgrüner Zopf, salbeifarbene einseitige Schultercape, lange petrolfarbene Weste und botanische Metallspange.')
add('league_champion','e6d9b8','263b51','c59745','d7ceba','d19a79',(3,2,1,2,3,2,3,4),
    'bbassabb/abassaba/abcccaba/abbcbbca/abbbcbca/abbbbcba/abbbbbca/abbbbbaa/cccmcccc/aappppaa/aappppaa/aappppaa',
    'bbaaaabb/abbbbbba/abbbbbba/abcccbba/abcbcbba/abcbcbba/abbbbbba/abbbbbba/cccmcccc/aappppaa/aappppaa/aappppaa',
    hair_style='swept_back',feature='laurel',sleeves='champion',pants='2d3d53',boots='2b3040',eyes='947445',leg_style='coat',note='Platinblonder schwungvoller Scheitel, elfenbeinfarbener Frack, tiefblaue Weste und goldene diagonal geführte Siegerschärpe.')
# Team Nova: black/charcoal base, restrained magenta, rank marks.
add('nova_aster','292734','464254','c13f84','c7cbd3','ddb4a1',(2,2,1,1,2,3,3,3),
    'bbassabb/abbssbba/abccccba/abkkkkba/abkcckba/abkkkkba/abkkkkba/abmkkmba/bbbbbbbb/aacppcaa/aacppcaa/aacppcaa',
    'bbbbbbbb/abbbbbba/aaacacca/aaaccaca/aaaccaca/aaacacca/aaaaaaaa/aaaaaaaa/bbbbbbbb/aacppcaa/aacppcaa/aacppcaa',
    hair_style='part',feature='temple',sleeves='aster',pants='252633',eyes='985578',leg_style='coat',note='Kühlsilberner exakter Seitenscheitel, schwarzer langer Uniformmantel, scharfe Schultern und magentafarbene Innensäume.')
add('nova_lyra','302b40','645064','d25d9d','d0ccd8','c99287',(3,4,5,4,3,2,2,3),
    'baassabb/abassbba/abkbbbba/abbbkkba/abbkkkba/abkkkkba/aacckcba/aaakkbaa/mmmccmmm/aaappaaa/aaappaaa/aaappaaa',
    'bbahhhbb/abahhhba/aaahhhaa/aaaahhaa/aaaahaaa/aaacacca/aaaccaca/aaacacca/mmmccmmm/aaappaaa/aaappaaa/aaappaaa',
    hair_style='long_side',feature='nova_clip',sleeves='lyra',pants='3b3046',eyes='8d4166',leg_style='tallboots',note='Weißsilberner scharfer Seitenpony, taillierte asymmetrische Offiziersjacke, hohe dunkle Stiefel und Nova-Haarspange.')
add('nova_varek','b6b6bf','353142','b4488d','646577','ccab96',(1,1,2,3,3,4,3,2),
    'aaassaaa/abassaba/abbccbba/abkbbkba/abkkbcba/abmkccba/abkkbcba/abkkbkba/abkkbkba/abppppba/abppppba/abppppba',
    'aaaaaaaa/abbccbba/aaaabaaa/aaaabaaa/aaacacca/aaaccaca/aaacacca/aaaabaaa/aaaabaaa/abppppba/abppppba/abppppba',
    hair_style='undercut',feature='goggles_face',sleeves='lab_nova',pants='3c374a',eyes='88778c',leg_style='coat',note='Schieferhaar und rechteckige Forschungsbrille; heller Labormantel über schwarzer Nova-Weste, violette Handschuhe und Probenhalter.')
add('nova_korr','33313d','55505e','ae4b7b','30313b','9a6a57',(1,1,1,1,1,2,2,1),
    'bbassabb/bbassabb/abbbbbba/abbcc bba/abab baba/abab baba/abab baba/abbbbbba/mmmccmmm/pppppppp/pbpppbpp/pbpppbpp'.replace(' ',''),
    'bbbbbbbb/bbaaaabb/abbbbbba/abaa aaba/abacacca/abaccaca/abacacca/abbbbbba/mmmccmmm/pppppppp/pbpppbpp/pbpppbpp'.replace(' ',''),
    hair_style='buzz',feature='scar',sleeves='armor',pants='34313c',eyes='916244',leg_style='workboots',note='Dunkler Bürstenschnitt und kleine Brauennarbe; gepanzerte Einsatzweste, breite Handschuhe und schwere Kommandantenstiefel.')
add('nova_grunt_01','353342','565161','ba4d90','252c3e','c2967b',(2,2,2,2,2,2,2,2),
    'bbassabb/abbssbba/abccccba/abkkkkba/abkkkkba/abkkkkba/abkkkkba/abmkkmba/mmmccmmm/pppppppp/pppppppp/pppppppp',
    'bbbbbbbb/abbbbbba/aaacacca/aaaccaca/aaaccaca/aaacacca/aaaaaaaa/aaaaaaaa/mmmccmmm/pppppppp/pppppppp/pppppppp',
    hair_style='short',feature='nova_cap',sleeves='uniform',pants='30303e',eyes='6b7484',leg_style='workboots',note='Dunkle Schirmmütze, geschlossenes schwarzes Diensthemd mit magentafarbenem Bruststreifen und Nova-Rückenabzeichen.')
add('nova_grunt_02','3a3144','645062','bc4d91','733e53','deae98',(3,3,3,2,3,3,4,3),
    'bbassabb/abassbba/abccccba/abkkkkba/abkkkkba/abkkkcba/abkkkcba/abmkkmba/mmmccmmm/aaappaaa/aaappaaa/pppppppp',
    'bbahhhbb/abahhhba/aaacacca/aaaccaca/aaaccaca/aaacacca/aaaaaaaa/aaaaaaaa/mmmccmmm/aaappaaa/aaappaaa/pppppppp',
    hair_style='bob',feature='earstud',sleeves='uniform_short',pants='302c3a',eyes='71875c',leg_style='tallboots',note='Weinroter Bob, kurzärmlige Nova-Uniform, kurzer Uniformrock über dunklen Beinen und hohe Stiefel.')
add('nova_grunt_03','34343f','575763','ad4a8b','687382','a7745e',(3,4,5,4,3,2,1,2),
    'bbassabb/bbakkabb/abccccba/abkkkkba/abkkkkba/abmkkkba/abkkkkba/abmkkmba/mmmccmmm/pppppppp/ppbppbpp/ppbppbpp',
    'bbbbbbbb/abbkkbba/aaacacca/aaaccaca/aaaccaca/aaacacca/aaaaaaaa/aaaaaaaa/mmmccmmm/pppppppp/ppbppbpp/ppbppbpp',
    hair_style='fringe',feature='earpiece',sleeves='uniform',pants='313440',eyes='688e99',leg_style='cargo',note='Schieferblauer Pony, Funkhörer und Nova-Kapuzenjacke; funktionale Cargohose statt langem Mantel.')
add('nova_grunt_04','35303e','685967','c55496','d4ccd1','b27e6b',(2,1,2,1,2,2,1,2),
    'bbassabb/abassaba/abccccba/abkkkkba/abkkkkba/abkkmkba/abkkkkba/abmkkmba/mmmccmmm/pppppppp/pppppppp/pppppppp',
    'bbahhabb/abahhaba/aaacacca/aaaccaca/aaaccaca/aaacacca/aaaaaaaa/aaaaaaaa/mmmccmmm/pppppppp/pppppppp/pppppppp',
    hair_style='topknot',feature='eyeline',sleeves='uniform_rolled',pants='302b36',eyes='9d6979',leg_style='sneakers',note='Platinfarbener kleiner Knoten, hochgekrempelte Uniformärmel und schmale Handschuhmanschetten; leichtes Erkundungsoutfit.')
# Forschende and everyday cast.
add('research_elian','e2dfce','488789','bc8f58','6d4c39','dfb08b',(2,2,1,2,3,4,3,3),
    'aaassaaa/abassaba/abbwwbba/abbbbbaa/abbbbmba/abbbbbaa/abmbbbba/abbbbbaa/abbbbbaa/abppppba/abppppba/abppppba',
    'aaaaaaaa/aaabbaaa/aaaaaaaa/aaaaaaaa/aaaaxaaa/aaaaxaaa/aaaaxaaa/aaaaxaaa/aaaaaaaa/abppppba/abppppba/abppppba',
    hair_style='messy',feature='glasses',sleeves='lab',pants='485c61',eyes='51857c',leg_style='coat',note='Walnussbraunes unordentliches Haar, Brille auf der Nase, elfenbeinfarbener Laborkittel mit Notizkarten und Petrolhemd.')
add('research_mira','5a6477','c6aa86','b27443','a35635','dfae90',(2,2,3,3,2,3,4,4),
    'bbassabb/abwsswba/abbwwbba/aaawwaaa/aabbbbaa/aaabbaaa/aaaabaaa/aaamaaaa/lllmmlll/aaaxaaaa/aaaxaaaa/aaaxaaaa',
    'aaahhaaa/aaahhaaa/aaahhaaa/aaaahaaa/aaaaahaa/aaaaahaa/aaaahaaa/aaahaaaa/lllmmlll/aaaxaaaa/aaaxaaaa/aaaxaaaa',
    hair_style='braid',feature='roundglasses',sleeves='cardigan',pants='59556a',eyes='708d73',leg_style='skirt',note='Kupferroter Zopf, schmale runde Brille, tintenblauer Cardigan, hoher Stehkragen und langer Archivrock.')
add('research_rhea','68714c','b1a077','b65b39','88432c','bb855f',(3,2,4,3,2,2,3,4),
    'bbassabb/bbbssbbb/abbbblaa/aabklbaa/abmllbaa/abbl kbaa/aallkbaa/aalbkbaa/lllmmlll/aappppaa/pppppppp/pppppppp'.replace(' ',''),
    'bbbbbbbb/aallaall/aallbbll/aallbbll/aallbbll/aallbbll/aallll ll/aaaaaaaa/lllmmlll/aappppaa/pppppppp/pppppppp'.replace(' ',''),
    hair_style='messy',feature='bandana',sleeves='rolled',pants='68523c',boots='40392f',eyes='688254',leg_style='cargo',note='Kastanienrotes wildes Haar mit rostfarbigem Bandana, offene Expeditionsweste, Rucksack, Feldgurte und robuste Stiefel.')
add('research_fossil','d8c8a6','596d7a','d3984c','b99758','e1b495',(2,2,2,2,3,3,2,2),
    'aaassaaa/abassaba/abwbwbba/abbbbbba/abmmmbba/abbbbbba/abbbmbba/abbbbbba/lllmmlll/aappppaa/aappppaa/pppppppp',
    'aaaaaaaa/abb bbbba/abbbbbba/abbbcbba/abbcc bba/abbbcbba/abbbbbba/aaaaaaaa/lllmmlll/aappppaa/aappppaa/pppppppp'.replace(' ',''),
    hair_style='short',feature='goggles',sleeves='rolled',pants='6a7071',eyes='708b91',leg_style='workboots',note='Sandfarbenes Haar und Feldbrille, heller Ausgrabungskittel mit Schürze, Pinsel und kleines Fossilabzeichen.')
add('quest_healer','dba6b0','f0e4d6','618f95','b56a83','edbea7',(3,3,2,3,3,2,3,3),
    'bbassabb/abbssbba/aabbbbaa/aaaaacaa/aaaaccca/aaaaacaa/aabbbbaa/aabbbbaa/bbbbbbbb/aaaxaaaa/aaaxaaaa/aaaxaaaa',
    'aaaaaaaa/aaaabaaa/aaaaaaaa/aaaaaaaa/aaaaaaaa/aaaaaaaa/aabbbbaa/aaaaaaaa/bbbbbbbb/aaaxaaaa/aaaxaaaa/aaaxaaaa',
    hair_style='bob',feature='nurseclip',sleeves='short',pants='d2c6ba',eyes='70849a',leg_style='skirt',note='Roséfarbener Bob, helle medizinische Tunika mit petrolfarbenem Plus statt rotem Kreuz, flache weiße Schuhe.')
add('quest_guide','577b93','d2c1a1','ce8650','77503a','cc9b79',(2,2,1,2,2,3,2,2),
    'bbassabb/bbbssbbb/aaaabaaa/aaalb aaa/abblbaaa/abllbmaa/aallbaaa/aaalbbaa/lllmmlll/pppppppp/pppppppp/pppppppp'.replace(' ',''),
    'bbbbbbbb/aaaaaaal/aaaaalla/aaaallaa/aaallaaa/aallaaaa/allaaaaa/llaaaaaa/lllmmlll/pppppppp/pppppppp/pppppppp',
    hair_style='topknot',feature='beret',sleeves='cardigan',pants='485b66',eyes='57858b',leg_style='hiking',note='Kastanienbrauner Knoten unter schräger blauer Baskenmütze, Halstuch, Umhänge-Kartentasche und Wanderhose.')
add('quest_merchant','806144','c5a06b','4c807c','614831','ab7b5d',(2,2,1,1,2,2,3,2),
    'bbassabb/abassaba/abbwwbba/abbbbbba/abbbmbba/abbbbbba/ablllbba/ablllbba/lllmmlll/aappppaa/pppppppp/pppppppp',
    'aaaaaaaa/aaaabaaa/aaaaaaaa/aaaabaaa/aaaaaaaa/aaaabaaa/aaaaaaaa/aaaaaaaa/lllmmlll/aappppaa/pppppppp/pppppppp',
    hair_style='part',feature='moustache',sleeves='linen',pants='514737',eyes='6c7950',leg_style='loafers',note='Walnussbrauner Seitenscheitel, Schnurrbart, gemusterte Kaufmannsweste über cremefarbenem Hemd und schwere Ledertaschen.')
add('quest_historian','778594','ded7c0','87683f','a0b6c3','d5ae95',(1,1,2,3,3,2,1,1),
    'aaassaaa/abassaba/abwwwbba/abbbb bba/abbbbbba/abbbmbba/abbbbbba/abbbmbba/abbbbbba/abppppba/abppppba/abppppba'.replace(' ',''),
    'aahhhhaa/aahhhhaa/aaahhaaa/aaaabaaa/aaaabaaa/aaaabaaa/aaaabaaa/aaaabaaa/aaaabaaa/abppppba/abppppba/abppppba',
    hair_style='receding',feature='beard_long',sleeves='coat',pants='515d69',eyes='647b86',leg_style='coat',note='Zurückweichender silbergrauer Haaransatz und heller Bart, blauer Gehrock, elfenbeinfarbener Schal und Taschenuhr.')
add('quest_miner','847058','4c595b','d2a556','a25832','b98667',(2,2,2,2,3,2,2,2),
    'bbassabb/bbassabb/baabbaab/baaabaaa/baaaa aab/baam maab/baaaaaab/baaaaaab/aaaaxaaa/aaaaxaaa/pppppppp/pppppppp'.replace(' ',''),
    'bbbbbbbb/babbbbab/bbaa aabb/bbaaaabb/bbaaaabb/bbaaaabb/bbaaaabb/bbaaaabb/aaaaxaaa/aaaaxaaa/pppppppp/pppppppp'.replace(' ',''),
    hair_style='cropped',feature='hardhat',sleeves='work',pants='5c5550',boots='433b36',eyes='648776',leg_style='workboots',note='Kupferhaar unter ockerfarbenem Grubenhelm mit Stirnlampe, abgewetzte Latzhose, graugrünes Hemd und Stiefelkappen.')
add('quest_ranger','466751','a4ae77','bd8750','475a3b','ba8b68',(3,4,3,2,2,3,3,2),
    'bbassabb/abassaba/abbbblaa/abkklbaa/abl lkbba/abllkbba/aalbkbba/aalbkbba/lllmmlll/aappppaa/pppppppp/pppppppp'.replace(' ',''),
    'bbbbbbbb/abbaabba/abbaabba/abbcc bba/abccccba/abccbcba/abbbbbba/aaaaaaaa/lllmmlll/aappppaa/pppppppp/pppppppp'.replace(' ',''),
    hair_style='fringe',feature='ranger_hat',sleeves='rolled',pants='5a5d43',boots='3e3b2c',eyes='847844',leg_style='cargo',note='Moosgrünes Haar und flacher Rangerhut, dunkle Waldjacke, salbeifarbene Schulterpartie, Lederriemen und Kartenfach.')
add('quest_engineer','d4b76c','485d66','63b3b4','ad873d','d6a687',(1,1,2,3,4,3,3,2),
    'bbassabb/baassbab/baabwaab/baaaa aab/baam maab/baaaacaa/baaaacaa/baaaamaa/mmmccmmm/aaaaxaaa/pppppppp/pppppppp'.replace(' ',''),
    'bbbbbbbb/babbbbab/bbaa aabb/bbaaacbb/bbbaacbb/bbbbccbb/bbaaacbb/bbaaaabb/mmmccmmm/aaaaxaaa/pppppppp/pppppppp'.replace(' ',''),
    hair_style='undercut',feature='goggles',sleeves='engineer',pants='495c61',boots='323c41',eyes='42868f',leg_style='cargo',note='Ockerfarbener Undercut, Schutzbrille, goldfarbene Arbeitsschürze, aufgekrempelte Ärmel und türkisfarbiges Messgerät.')
add('quest_traveler','788a9d','d0c0a4','a6653f','c5a266','d6a184',(3,2,1,2,3,4,3,2),
    'bbassabb/bbbssbbb/abbbblaa/abkkllaa/abl lklba/abllklba/aallklba/aalkklba/lllmmlll/aappppaa/pppppppp/pppppppp'.replace(' ',''),
    'bbbbbbbb/allaalla/allbbbll/allbbbll/allbb bll/allbcbll/allbbbll/alllllll/lllmmlll/aappppaa/pppppppp/pppppppp'.replace(' ',''),
    hair_style='windswept',feature='bandana_low',sleeves='expedition',pants='4d5670',boots='584738',eyes='69889d',leg_style='hiking',note='Sandblonder Pony, cremefarbenes Halstuch, verwaschene Reiseweste, großer zweifarbiger Rucksack und braune Stiefel.')

# Shared faction emblem is intentional; each coat/collar remains individually authored.
for design in D:
    if design.id.startswith('nova_'):
        rows=design.back.split('/')
        rows[3:7]=['aacaacaa','aaccacaa','aacaccaa','aacaacaa']
        design.back='/'.join(rows)
