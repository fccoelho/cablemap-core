# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests classificationist parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_, ok_
from cablemap.core import cable_by_id
from cablemap.core.reader import parse_classified_by

_TEST_DATA = (
    ('10TOKYO397', 'Marc Wall', u'''FIELD

REF: STATE 015541

Classified By: Acting Deputy Chief of Mission Marc Wall for Reasons 1.4
 (b) and (d)

¶1. (C) SUM'''),
    ('10GENEVA249', 'Rose E. Gottemoeller', u'''REF: 10 GENEVA 231 (SFO-GVA-VIII-088) CLASSIFIED BY: Rose E. Gottemoeller, Assistant Secretary, Department of State, VCI; REASON: 1.4(B), (D) '''),
    ('10GENEVA247', 'Rose E. Gottemoeller', u'''REF: 10 GENEVA 245 (SFO-GVA-VIII-086) CLASSIFIED BY: Rose E. Gottemoeller, Assistant Secretary, Department of State, VCI; REASON: 1.4(B), (D) ¶1. (U) This '''),
    ('10UNVIEVIENNA77', 'Glyn T. Davies', u'''\nClassified By: Ambassador Glyn T. Davies for reasons 1.4 b and d '''),
    ('10WARSAW117', 'F. Daniel Sainz', u'''\nClassified By: Political Counselor F. Daniel Sainz for Reasons 1.4 (b) and (d) '''),
    ('10STATE16019', 'Karin L. Look', u'''\nClassified By: Karin L. Look, Acting ASSISTANT SECRETARY, VCI. Reason: 1.4 (b) and (d).'''),
    ('10LILONGWE59', 'Bodde Peter', u'''\nCLASSIFIED BY: Bodde Peter, Ambassador; REASON: 1.4(B) '''),
    ('95ZAGREB4339', 'ROBERT P. FINN', u'''
1.  (U)  CLASSIFIED BY ROBERT P. FINN, DEPUTY CHIEF OF
MISSION.  REASON: 1.5 (D)
 '''),
    ('95DAMASCUS5748', 'CHRISTOPHER W.S. ROSS', u'''SUBJECT:  HAFIZ AL-ASAD: LAST DEFENDER OF ARABS

1. CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY:
CHRISTOPHER W.S. ROSS, AMBASSADOR.  REASON: 1.5 (D) .

2. SUMMAR'''),
    ('95TELAVIV17504', (), u'''
1.  CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY SECTION 1.5 (B)
AND (D).  NIACT PRECEDENCE BECAUSE OF GOVERNMENT CRISIS IN
ISRAEL.

2.  SU'''),
    ('95RIYADH5221', 'THEODORE KATTOUF', u'''
1.  CONFIDENTIAL - ENTIRE TEXT.  CLASSIFIED BY DCM
THEODORE KATTOUF - 1.5 B,D.

2.  (C)'''),
    ('96ADDISABABA1545', 'JEFFREY JACOBS', u'''
1.  (U)  CLASSIFIED BY POLOFF JEFFREY JACOBS, 1.5 (D).

2.  (C)'''),
    ('96AMMAN2094', 'ROBERT BEECROFT', u'''
1. (U)  CLASSIFIED BY CHARGE ROBERT BEECROFT; REASON 1.5 (D).

2. (C) '''),
    ('96STATE86789', 'MARY BETH LEONARD', u'''
1.  CLASSIFIED BY AF/C - MARY BETH LEONARD, REASON 1.5
(D). '''),
    ('96NAIROBI6573', 'TIMOTHY CARNEY', u'''
1.  CLASSIFIED BY AMBASSADOR TO SUDAN TIMOTHY CARNEY.
REASON 1.5(D).
 '''),
    ('96RIYADH2406', 'THEODORE KATTOUF', u'''SUBJECT:  CROWN PRINCE ABDULLAH THE DIPLOMAT

1.  (U) CLASSIFIED BY CDA THEODORE KATTOUF, REASON 1.5.D.

2. '''),
    ('96RIYADH2696', 'THEODORE KATTOUF', u'''
1.  (U)  CLASSIFIED BY CHARGE D'AFFAIRES THEODORE
KATTOUF: 1.5 B, D.
 '''),
    ('96ISLAMABAD5972', 'THOMAS W. SIMONS, JR.', u'''
1.  (U) CLASSIFIED BY THOMAS W. SIMONS, JR., AMBASSADOR.
REASON:  1.5 (B), (C) AND (D).
 '''),
    ('96ISLAMABAD5972', 'Thomas W. Simons, Jr.', u'''
1.  (U) CLASSIFIED BY THOMAS W. SIMONS, JR., AMBASSADOR.
REASON:  1.5 (B), (C) AND (D).
 ''', True),
    ('96STATE183372', 'LEE 0. COLDREN', u''' 
1.  (U) CLASSIFIED BY LEE 0. COLDREN, DIRECTOR, SA/PAB, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 '''),
    ('96STATE183372', 'Lee O. Coldren', u''' 
1.  (U) CLASSIFIED BY LEE 0. COLDREN, DIRECTOR, SA/PAB, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 ''', True),
    ('96ASHGABAT2612', 'TATIANA C. GFOELLER', u''' 
1.  (U) CLASSIFIED BY CHARGE TATIANA C. GFOELLER. 
REASON:  1.5 D. 
 '''),
    ('96BOGOTA8773', 'S.K. ABEYTA', u''' 
1.  CLASSIFIED BY POL/ECONOFF. S.K. ABEYTA.  REASON:  1.5(D) 
 '''),
    ('96STATE194868', 'E. GIBSON LANPHER, JR.', u''' 
1.   (U) CLASSIFIED BY E. GIBSON LANPHER, JR., ACTING 
ASSISTANT SECRETARY OF STATE FOR SOUTH ASIAN AFFAIRS, 
DEPARTMENT OF STATE. REASON: 1.5(D). 
 '''),
    ('96JAKARTA7841', 'ED MCWILLIAMS', u''' 
1.  (U) CLASSIFIED BY POL COUNSELOR ED MCWILLIAMS; 
REASON 1.5(D) 
 '''),
    ('96JERUSALEM3094', 'EDWARD G. ABINGTON, JR.', u''' 
1.  CLASSIFIED BY CONSUL GENERAL EDWARD G. ABINGTON, JR.  REASON 
1.5 (B) AND (D). 
 '''),
    ('96BOGOTA10967', 'S.K. ABEYTA', u''' 
1.  (U)  CLASSIFIED BY POL/ECONOFF S.K. ABEYTA.  REASON 1.5(D). 
 '''),
    ('04MUSCAT2112', 'Richard L. Baltimore, III', u''' 
Classified By: Ambassador Richard L. Baltimore, III. 
Reasons: 1.4 (b) and (d). 
 '''),
    ('04MUSCAT2112', 'Richard L. Baltimore, III', u''' 
Classified By: Ambassador Richard L. Baltimore, III. 
Reasons: 1.4 (b) and (d). 
 ''', True),
    ('05OTTAWA1975', 'Patricia Kim-Scott', u''' 
Classified By: Pol/Mil Officer Patricia Kim-Scott.  Reason E.O. 12958, 
1.4 (b) and (d). 
 '''),
    ('05BOGOTA6208', 'William B. Wood', u''' 
Classified By: Ambassador William B. Wood; reasons 1.4 
(b) and (d) 
 '''),
    ('05TAIPEI2839', 'Douglas Paal', u''' 
Classified By: AIT Director Douglas Paal, Reason(s): 1.4 (B/D). 
 '''),
    ('05DHAKA3073', 'D.C. McCullough', u''' 
Classified By: A/DCM D.C. McCullough, reason para 1.4 (b) 
 '''),
    ('09NAIROBI1132', 'Jessica Davis Ba', u''' 
Classified By: Pol/Econ Officer Jessica Davis Ba for reasons 1.4(b) and 
 (d) 
 '''),
    ('08ROME1541', 'Liz Dibble', u''' 
Classified By: Classified by DCM Liz Dibble for reasons 1.4 (b) and 
(d). 
 '''),
    ('06BAGHDAD2082', 'DANIEL SPECKHARD', r''' 
Classified By: CHARGE D\'AFFAIRES DANIEL SPECKHARD FOR REASONS 1.4 (A), 
(B) AND (D) 
 '''),
    ('05ANKARA4653', 'Nancy McEldowney', u''' 
Classified By: (U) CDA Nancy McEldowney; E.O. 12958, reasons 1.4 (b,d) 
 '''),
    ('05QUITO2057', 'LARRY L. MEMMOTT', u''' 
Classified By: ECON LARRY L. MEMMOTT, REASONS 1.4 (B,D) 
 '''),
    ('06HONGKONG3559', 'LAURENT CHARBONNET', u''' 
CLASSIFIED BY: ACTING DEPUTY PRINCIPAL OFFICER LAURENT CHARBONNET.  REA 
SONS: 1.4 (B,D) 
 '''),
    ('09BAGHDAD791', 'Patricia Butenis', u''' 
Classified By: Charge d\' Affairs Patricia Butenis for reasons 1.4 (b) a 
nd (d) 
 '''),
    ('06OSLO19', 'Christopher W. Webster', u''' 
Classified By: Charge d\'Affaires a.i. Christopher W. Webster, 
reason 1.4 (b) and (d) 
 '''),
    ('08BEIJING3386', 'Aubrey Carlson', u''' 
Classified By: Political Section Minister Counselor Aubrey Carlson.  Re 
asons 1.4 (b/d). 
 '''),
    ('09MOSCOW2393', 'Susan M. Elliott', u''' 
Classified By: Political Minister Counselor Susan M. Elliott for reason 
s:  1.4 (b), (d). 
 '''),
    ('10BRUSSELS66', 'Christopher R. Davis', u''' 
Classified By: Political Minister-Counselor Christopher R. Davis for re 
ason 1.4 (b/d) 
 '''),
    ('06BEIJING22125', 'ROBERT LUKE', u''' 
Classified By: (C) CLASSIFIED BY MINISTER COUNSELOR FOR ECONOMIC AFFAIR 
S ROBERT LUKE; REASON 1.4 (B) AND (D). 
 '''),
    ('07CAIRO622', 'William R. Stewart', u''' 
Classified by:  Minister Counselor for Economic and 
Political Affairs William R. Stewart for reasons 1.4(b) and 
(d). 
 '''),
    ('07BAGHDAD1188', 'Daniel Speckhard', u''' 
Classified By: Charge Affaires Daniel Speckhard.  Reasons: 1.4 (b) and 
(d). 
 '''),
    ('08PARIS1131', 'STUART DWYER', u''' 
Classified By: ECONCOUNS STUART DWYER FOR REASONS 1.4 B AND D 
 '''),
    ('08ATHENS985', 'Jeff Hovenier', u''' 
Classified By: A/Political Counselor Jeff Hovenier for 
1.4 (b) and (d) 
 '''),
    ('09BEIJING2690', 'William Weinstein', u''' 
Classified By: This message classified by Econ Minister Counselor 
William Weinstein for reasons 1.4 (b), (d) and (e). 
 '''),
    ('06VILNIUS945', 'Rebecca Dunham', u''' 
Classified By: Political and Economic Section Chief Rebecca Dunham for 
reasons 1.4 (b) and (d) 
 '''),
    ('07BAGHDAD2781', 'Howard Keegan', u''' 
Classified By: Kirkuk PRT Team Leader Howard Keegan for reason 1.4 (b) 
and(d). 
 '''),
    ('09HARARE864', 'Donald Petterson', u''' 
Classified By: Charge d\'affaires, a.i. Donald Petterson for reason 1.4 
(b). 
 '''),
    ('04MANAMA525', 'Robert S. Ford', u''' 
Classified By: Charge de Affaires Robert S. Ford for reasons 
1.4 (b) and (d). 
 '''),
    ('08STATE56778', 'Patricia A. McNerney', u''' 
Classified By: ISN Acting Assistant Secretary 
Patricia A. McNerney, Reasons 1.4 b, c, and d 
 '''),
    ('07BRUSSELS1462', 'Larry Wohlers', u''' 
Classified By: USEU Political Minister Counselor Larry Wohlers 
for reasons 1.4 (b) and (d). 
 '''),
    ('09KABUL2261', 'Hoyt Yee', u''' 
Classified By: Interagency Provincial Affairs Deputy Coordinator Hoyt Y 
ee for reasons 1.4 (b) and (d) 
 '''),
    ('09KABUL1233', 'Patricia A McNerney', u''' 
Classified By: PRT and Sub-National Governance Acting Director Patricia 
 A McNerney for reasons 1.4 (b) and (d) 
 '''),
    ('09BRUSSELS1288', 'CHRISTOPHER DAVIS', u''' 
Classified By: CLASSIFIED BY USEU MCOUNSELOR CHRISTOPHER DAVIS, FOR REA 
 
SONS 1.4 (B) AND (D) 
 '''),
    ('06TAIPEI3165', 'Stephen M. Young', u''' 
Classified By: Classified by AIT DIR Stephen M. Young. 
Reasons:  1.4 b, d. 
 '''),
    ('07BRUSSELS1208', 'Courtney Nemroff', u''' 
Classified By: Institutional Affairs Unit Chief Courtney Nemroff for re 
asons 1.4 (b) & (d) 
 '''),
    ('05CAIRO8602', 'Michael Corbin', u''' 
Classified by ECPO Minister-Counselour Michael Corbin for 
reasons 1.4 (b) and (d). 
 '''),
    ('09MADRID1210', 'Arnold A. Chacon', u''' 
Classified By: Charge d'Affaires, a.i., Arnold A. Chacon 
 
1.(C) Summary:  In his meetings with Spanish officials, 
Special Envoy for Eurasian Energy'''),
    ('05SINGAPORE887', 'Laurent Charbonnet', u''' 
Classified By: E/P Counselor Laurent Charbonnet, Reasons 1.4(b)(d) 
 '''),
    ('09SINGAPORE677', 'Dan Jassem', u''' 
Classified By: Acting E/P Counselor Dan Jassem for reasons 1.4 (b) and 
(d) 
 '''),
    ('08BELGRADE1189', 'Thatcher Scharpf', u''' 
Classified By: Acting Deputy Chief of Mission Thatcher Scharpf for reas 
ons 1.4(b/d). 
 '''),
    ('09BAGHDAD3319', 'Rachna Korhonen', u''' 
Classified By: PRT Kirkuk Governance Section Head Rachna Korhonen for r 
easons 1.4 (b) and (d). 
 '''),
    ('04ANKARA5897', 'Thomas Goldberger', u''' 
Classified By: (U) Classified by Economic Counselor Thomas Goldberger f 
or reasons 1.4 b,d. 
 '''),
    ('00HARARE3759', 'TOM MCDONALD', u''' 
CLASSIFIED BY AMBASSADOR TOM MCDONALD. 
                       CONFIDENTIAL 
 
PAGE 02        HARARE  03759  01 OF 03  111533Z 
REASONS: 1.5 (B) AND (D). 
 
1.  (C)  SUMMARY:  ALTHOUGH WIDESPREAD FEARS OF A 
SPIKE'''),
    ('07STATE156455', 'Glyn T. Davies', u''' 
Classified By: Glyn T. Davies 
 
SUMMARY 
------- 
 '''),
    ('03GUATEMALA1727', 'Erik Hall', u''' 
Classified By: Labor Attache Erik Hall.  Reason 1.5 (d). 
 '''),
    ('05VILNIUS503', 'LARRY BEISEL', u''' 
Classified By: DEFENSE ATTACHE LTC LARRY BEISEL FOR REASONS 1.4 (B) AND 
 (D). 
 '''),
    ('08USUNNEWYORK729', 'Carolyn L. Willson', u''' 
Classified By: USUN Legal Adviser Carolyn L. Willson, for reasons 
1.4(b) and (d) 
 '''),
    ('04BRUSSELS4688', 'Jeremy Brenner', u''' 
Classified By: USEU polmil officer Jeremy Brenner for reasons 1.4 (b) a 
nd (d) 
 '''),
    ('08GUATEMALA1416', 'Drew G. Blakeney', u''' 
Classified By: Pol/Econ Couns Drew G. Blakeney for reasons 1.4 (b&d). 
 '''),
    ('08STATE77798', 'Brian H. Hook', u''' 
Classified By: IO Acting A/S Brian H. Hook, E.O. 12958, 
Reasons: 1.4(b) and (d) 
 
 '''),
    ('05ANKARA1071', 'Margaret H. Nardi', u''' 
Classified By: Acting Counselor for Political-Military Affiars Margaret 
 H. Nardi for reasons 1.4 (b) and (d). 
 '''),
    ('08MOSCOW3655', 'David Kostelancik', u''' 
Classified By: Deputy Political M/C David Kostelancik.  Reasons 1.4 (b) 
 and (d). 
 '''),
    ('09STATE75025', 'Richard C. Holbrooke', u''' 
Classified By: Special Representative for Afghanistan and Pakistan 
Richard C. Holbrooke 
 
1.  (U)  This is an action request; see paragraph 4. 
 '''),
    ('10KABUL688', 'Joseph Mussomeli', u''' 
Classified By: Assistant Chief of Mission Joseph Mussomeli for Reasons 
1.4 (b) and (d) 
 '''),
    ('98USUNNEWYORK1638', 'HOWARD STOFFER', u''' 
CLASSIFIED BY DEPUTY POLITICAL COUNSEL0R HOWARD STOFFER 
PER 1.5 (B) AND (D).  ACTION REQUEST IN PARA 10 BELOW. 
 '''),
    ('02ROME3119', 'PIERRE-RICHARD PROSPER', u''' 
CLASSIFIED BY: AMBASSADOR-AT-LARGE PIERRE-RICHARD PROSPER 
FOR REASONS 1.5 (B) AND (D) 
 '''),
    ('02ANKARA8447', 'Greta C. Holtz', u''' 
 
Classified by Consul Greta C. Holtz for reasons 1.5 (b) & (d). 
 '''),
    ('09USUNNEWYORK282', 'SUSAN RICE', u''' 
Classified By: U.S. PERMANENT REPRESENATIVE AMBASSADOR SUSAN RICE 
FOR REASONS 1.4 B/D 
 '''),
    ('09DHAKA339', 'Geeta Pasi', u''' 
Classified By: Charge d'Affaires, a.i. Geeta Pasi.  Reasons 1.4 (b) and 
 (d) 
 '''),
    ('06USUNNEWYORK2273', 'Alejandro D. Wolff', u''' 
Classified By: Acting Permanent Representative Alejandro D. Wolff 
 per reasons 1.4 (b) and (d) 
 '''),
    ('08ISLAMABAD1494', 'Anne W. Patterson', u''' 
Classified By: Ambassador Anne W. Patterson for reaons 1.4 (b) and (d). 
 
1. (C) Summary: During'''),
    ('08BERLIN1150', 'Robert Pollard', u''' 
Classified By: Classified by Economic Minister-Counsellor 
Robert Pollard for reasons 1.4 (b) and (d) 
 '''),
    ('08STATE104902', 'DAVID WELCH', u''' 
Classified By: 1. CLASSIFIED BY NEA ASSISTANT SECRETARY DAVID WELCH 
REASONS: 1.4 (B) AND (D) 
 '''),
    ('07VIENTIANE454', 'Mary Grace McGeehan', u''' 
Classified By: Charge de'Affairs ai. Mary Grace McGeehan for reasons 1. 
4 (b) and (d) 
 '''),
    ('07ROME1948', 'William Meara', u''' 
Classified By: Acting Ecmin William Meara for reasons 1.4 (b) and (d) 
 '''),
    ('07USUNNEWYORK545', 'Jackie Sanders', u''' 
Classified By: Amb. Jackie Sanders. E.O 12958. Reasons 1.4 (B&D). 
 '''),
    ('06USOSCE113', 'Bruce Connuck', u''' 
Classified By: Classified by Political Counselor Bruce Connuck for Reas 
(b) and (d). 
 '''),
    ('09DOHA404', 'Joseph LeBaron', u''' 
Classified By: Ambassaor Joseph LeBaron for reasons 1.4 (b and d). 
 '''),
    ('09DOHA404', 'Joseph LeBaron', u''' 
Classified By: Ambassaor Joseph LeBaron for reasons 1.4 (b and d). 
 ''', True),
    ('09RANGOON575', 'Thomas Vajda', u''' 
Classified By: Charge d'Afairs (AI) Thomas Vajda for Reasons 1.4 (b) & 
 (d 
 '''),
    ('03ROME3107', 'TOM COUNTRYMAN', u''' 
Classified By: POL MIN COUN TOM COUNTRYMAN, REASON 1.5(B)&(D). 
 '''),
    ('06USUNNEWYORK732', 'Molly Phee', u''' 
Classified By: Deputy Political Counselor Molly Phee, 
for Reasons 1.4 (B and D) 
 '''),
    ('06BAGHDAD1552', 'David M. Satterfield', u''' 
Classified By: Charge d'Affaires David M. Satterfield for reasons 1.4 ( 
b) and (d) 
 '''),
    ('06ABUJA232', 'Erin Y. Tariot', u''' 
Classified By: USDEL Member Erin Y. Tariot, reasons 1.4 (b,d) 
 '''),
    ('09ASTANA184', 'RICAHRD E. HOAGLAND', u''' 
Classified By: AMBASSADOR RICAHRD E. HOAGLAND: 1.2 (B), (D) 
 '''),
    ('09ASTANA184', 'Richard E. Hoagland', u''' 
Classified By: AMBASSADOR RICAHRD E. HOAGLAND: 1.2 (B), (D) 
 ''', True),
    ('09CANBERRA428', 'John W. Crowley', u''' 
Classified By: Deputy Political Counselor: John W. Crowley, for reasons 
 1.4 (b) and (d) 
 '''),
    ('08TASHKENT706', 'Molly Stephenson', u''' 
Classified By: Classfied By: IO Molly Stephenson for reasons 1.4 (b) a 
nd (d). 
 '''),
    ('08CONAKRY348', 'T. SCOTT BROWN', u''' 
Classified By: ECONOFF T. SCOTT BROWN FOR REASONS 1.4 (B) and (D) 
 '''),
    ('07STATE125576', 'Margaret McKelvey', u''' 
Classified By: PRM/AFR Dir. Margaret McKelvey-reasons 1.4(b/d) 
 '''),
    ('09BUDAPEST372', 'Steve Weston', u''' 
Classified By: Acting Pol/Econ Counselor:Steve Weston, 
reasons 1.4 (b and d) 
 '''),
    ('04TAIPEI3162', 'David J. Keegan', u'''' 
Classified By: AIT Deputy Director David J. Keegan, Reason: 1.4 (B/D) 
 '''),
    ('04TAIPEI3521', 'David J. Keegan', u''' 
Classified By: AIT Acting Director David J. Keegan, Reason: 1.4 (B/D) 
 '''),
    ('04TAIPEI3919', 'David J. Keegan', u''' 
Classified By: AIT Director David J. Keegan, Reason 1.4 (B/D) 
 '''),
    ('08JAKARTA1142', 'Stanley A. Harsha', u''' 
Classified By: Acting Pol/C Stanley A. Harsha for reasons 1.4 (b+d). 
 '''),
    ('06ISLAMABAD16739', 'MARY TOWNSWICK', u''' 
Classified By: DOS CLASSIFICATION GUIDE BY MARY TOWNSWICK 
 
1.  (C)  Summary.  With limited government support, Islamic 
banking has gained momentum in Pakistan in the past three 
years.  The State Bank of Pakistan (SBP) reports that the 
capital base of the Islamic banking system has more than 
doubled since 2003 as the number of Islamic banks operating 
in Pakistan rose from one to four.  A media analysis of 
Islamic banking in Pakistan cites an increase in the number 
of conventional banks'''),
    ('05DJIBOUTI802', 'JEFFREY PURSELL', u''' 
 (U) CLASSIFIED BY TDY RSO JEFFREY PURSELL FOR REASON 1.5 C. 
 '''),
    ('09STATE82567', 'Eliot Kang', u''' 
Classified By: Acting DAS for ISN Eliot Kang. Reasons 1.4 (b) and (d) 
 
 '''),
    ('04ANKARA5764', 'Charles O. Blaha', u''' 
Classified By: Classified by Deputy Political Counselor Charles O. Blah 
a, E.O. 12958, reasons 1.4 (b) and (d). 
 '''),
    ('04ANKARA5764', 'Charles O. Blaha', u''' 
Classified By: Classified by Deputy Political Counselor Charles O. Blah 
a, E.O. 12958, reasons 1.4 (b) and (d). 
 ''', True),
    ('10VIENNA195', 'J. Dean Yap', u''' 
Classified by: DCM J. Dean Yap (acting) for reasons 1.4 (b) 
and (d). 
 '''),
    ('03HARARE175', 'JOHN S. DICARLO', u''' 
Classified By: RSO - JOHN S. DICARLO. REASON 1.5(D) 
 '''),
    ('08LONDON2968', 'Greg Berry', u''' 
Classified By: PolMinCons Greg Berry, reasons 1.4 (b/d). 
 '''),
    ('08HAVANA956', 'Jonathan Farrar', u''' 
Classified By: COM Jonathan Farrar for reasons 1.5 (b) and (d) 
 '''),
    ('09BAGHDAD253', 'Robert Ford', u''' 
Classified By: Acting Deputy Robert Ford.  Reasons 1.4 (b) and (d) 
 '''),
    ('09TIRANA81', 'JOHN L. WITHERS II', u''' 
Classified By: AMBASSADOR JOHN L. WITHERS II FR REASONS 1.4 (b) AND (d 
). 
 '''),
    ('05HARARE383', 'Eric T. Schultz', u''' 
Classified By: Charge d'Affaires a.i. Eric T. Schultz under Section 1.4 
 b/d 
 '''),
    ('07LISBON2591', 'Jenifer Neidhart', u''' 
Classified By: Pol/Econ Off Jenifer Neidhart for reasons 1.4 (b) and (d 
) 
 '''),
    ('07STATE171234', 'Lawrence E. Butler', u''' 
Classified By:  NEA Lawrence E. Butler for reasons EO 12958 
1.4(b),(d), and (e). 
 '''),
    ('04AMMAN8544', 'David Hale', u''' 
Classified By: Charge d'Affaries David Hale for Reasons 1.4 (b), (d) 
 '''),
    ('07NEWDELHI5334', 'Ted Osius', u''' 
Classified By: Acting DCM/Ted Osius for reasons 1.4 (b and d) 
 '''),
    ('04JAKARTA5072', 'ANTHONY C. WOODS', u''' 
Classified By: EST&H OFFICER ANTHONY C. WOODS FOR REASON 1.5 (b, d) 
 '''),
    ('03AMMAN2822', 'Edward W. Gnehm', u''' 
Classified By: Ambassador Edward W. Gnehm.  Resons 1.5 (B) and (D) 
 '''),
    ('08CANBERRA1335', 'Daniel A. Clune', u''' 
Classified By: Deputy Chief of Mission: Daniel A. Clune: Reason: 1.4 (c 
) and (d) 
 '''),
    ('09HAVANA665', 'Charles Barclay', u''' 
Classified By: CDA: Charles Barclay for reQ#8$UQ8ML#C may choke oQhQGTzovisional\" controls, such as 
price caps and limits on the amount any one person could buy. 
 
 
3.  (SBU) Furthering speculation that the private markets 
were under the gun, official reports have resurfaced in 
recent months accusing private markets of artificially 
maintaining higher'''),
    ('08STATE8993', 'Gregory B. Starr', u''' 
1. (U) Classified by Acting Assistant Secretary for Diplomatic 
Security Gregory B. Starr for E.O. 12958 reasons 1.4 (c) and 
(d). 
 '''),
    ('09ISTANBUL137', 'Sandra Oudkirk', u''' 
Classified By: ConGen Istanbul DPO Sandra Oudkirk; Reason 1.5 (d) 
 '''),
 ('08BANGKOK1778', 'James F. Entwistle', u''' 
Classified By: Charge, d,Affaires a. i. James F. Entwistle, reason 1.4 
(b) and (d). 
 '''),
 ('08MANAMA301', 'Christopher Henzel', u''' 
Classified By: Charge d,Affaires a.i. Christopher Henzel, reasons 1.4(b 
) and (d). 
 
 '''),
    ('06COLOMBO123', 'Robert O. Blake, Jr.', u''' 
Classified By: Abassador Robert O. Blake, Jr. for reasons 
1.4 (b and (d). 
 '''),
    ('08YEREVAN907', 'Marie Yovanovitch', u''' 
Classified By: Amabassador Marie Yovanovitch.  Reason 1.4 (B/D) 
 '''),
    ('09QUITO329', 'Heather M. Hodges', u''' 
Classified By: AMB Heather M. Hodges for reason 1.4 (D) 
 '''),
    ('09STATE38028', ('KARL WYCOFF', 'SHARI VILLAROSA'), u''' 
CLASSIFIED BY AF KARL WYCOFF, ACTING AND S/CT DAS SHARI 
VILLAROSA ; E.O. 12958 REASON: 1.4 (B) AND (D) 
 '''),
    ('04ABUJA2060', 'BRUCE EHRNMAN', u''' 
Classified By: AF SPECIAL ADVISOR BRUCE EHRNMAN FOR REASONS 1.5 (B) AND 
 (D) 
 '''),
    ('06ISLAMABAD3684', 'RCROCKER', u''' 
Classified By: AMB:RCROCKER, Reasons 1.4 (b) and (c) 
 '''),
    ('06MANAMA184', 'William T.Monroe', u''' 
Classified By: Classified by Ambassadior William T.Monroe.  Reasons: 1. 
4 (b)(d) 
 '''),
    ('07SANSALVADOR263', 'Charles Glazer', u''' 
Classified By: Ambasasdor Charles Glazer, Reasons 
1.4 (b) and (d) 
 '''),
    ('05BRUSSELS1549', 'Michael Ranneberger', u''' 
Classified By: AF PDAS Michael Ranneberger.  Reasons 1.5 (b) and (d). 
 '''),
    ('09STATE14163', 'Mark Boulware', u''' 
Classified By: AF Acting DAS Mark Boulware,  Reasons 1.4 (b) and (d). 
 '''),
    ('06AITTAIPEI1142', 'Michael R. Wheeler', u''' 
Classified By: IPO Michael R. Wheeler for reason 1.4(G)(E) 
 '''),
    ('08TAIPEI1038', 'Stephen M. Young', u''' 
Classified By: AIT Chairman Stephen M. Young, 
Reasons: 1.4 (b/d) 
 '''),
    ('09STATE96519', 'Ellen O. Tauscher', u''' 
Classified By: T U/S Ellen O. Tauscher for Reasons 1.4 a,b,and d. 
 '''),
    ('08NAIROBI232', 'JOHN M. YATES', u''' 
Classified By: SPECIAL ENVOY JOHN M. YATES 
 
1.  (C) '''),
    ('07COLOMBO769', 'Robert O. Blake, Jr.', u''' 
Classified By: Ambassodor Robert O. Blake, Jr. for reasons 1.4 (b, d). 
 '''),
    ('04DJIBOUTI1541', 'MARGUERITA D. RAGSDALE', u''' 
Classified By: AMBASSSADOR MARGUERITA D. RAGSDALE. 
REASONS 1.4 (B) AND (D). 
 '''),
    ('08MOSCOW3202', 'David Kostelancik', u''' 
Classified By: Acting Political MC David Kostelancik for reasons 1.4(b) 
 and (d). 
 '''),
    ('09BEIJING939', 'Ben Moeling', u''' 
Classified By: Acting Political Minister-Couselor 
Ben Moeling, reasons 1.4 (b/d). 
 '''),
    ('09HAVANA689', 'Jonathan Farrar', u''' 
Classified By: Principal Office Jonathan Farrar for reasons 1.4 (b) and 
 (d) 
 '''),
    ('07VIENNA2687', 'J. Dean Yap', u''' 
Classified By: Political Economic Counselr J. Dean Yap for reasons 1.4 
 (b) and (d) 
 '''),
    ('08LONDON1485', 'Maura Connelly', u''' 
Classified By: Political Minister Counsel Maura Connelly for reasons 1. 
4 (b/d). 
 '''),
    ('07LONDON3228', 'JOHN MCNAMARA', u''' 
Classified By: A E/MIN COUNS. JOHN MCNAMARA, REASONS 1.4(B) AND (D) 
 '''),
    ('05ABUJA2031', 'Rich Verrier', u''' 
Classified By: ARSO Rich Verrier for reason 1.4 (d) 
 '''),
    ('09USOSCE235', 'Chris Ellis', u''' 
Classified By: Acting Chief Arms Control Delegate Chris Ellis, 
for reasons 1.4(b) and (d). 
 '''),
    ('06RANGOON1542', 'Walter Parrs III', u''' 
Classified By: Conoff Walter Parrs III for Reasons 1.4 (b) and (d) 
 '''),
    ('08STATE109148', 'Pam Durham', u''' 
Classified By: ISN/MTR Direcotr Pam Durham. 
Reason:  1.4 (B), (D). 
 '''),
    ('08STATE3581', 'AFriedt', u''' 
Classified By: EUR/PRA, Dir. AFriedt, Reason 1.4 (b/d) 
 '''),
    ('06HONGKONG3109', 'JEFF ZAISER', u''' 
CLASSIFIED BY: ACTING E/P CIEF JEFF ZAISER.  REASONS: 1.4(B,D). 
 '''),
    ('07LAPAZ123', 'Brian Quigley', u''' 
Classified By: Acting Ecopol Councilor Brian Quigley for reasons 1.4 (d 
) and (e). 
 '''),
    ('08BAGHDAD3818', 'Michael Dodman', u''' 
Classified By: A/EMIN Michael Dodman, Reasons 1.4 (b,d). 
 '''),
    ('09BAGHDAD565', 'Michael Dodman', u''' 
Classified By: Acting EMIN Michael Dodman, reasons 1.4 (b,d). 
 '''),
    ('09BUDAPEST198', 'Jon Martinson', u''' 
Classified By: Acting P/E Counseor Jon Martinson, reasons 1.4 (b,d) 
 '''),
    ('09BUDAPEST276', 'Jon Martinson', u''' 
Classified By: Acting P/E Counsleor Jon Martinson, reasons 1.4 (b,d) 
 '''),
    ('08STATE67468', 'George Krol', u''' 
Classified By: SCA/DAS for Central Asia George Krol 
 
 1.  (C) '''),
    ('09STATE24316', 'GEORGE KROL', u''' 
Classified By: DEPUTY ASSISTANT SECRETARY OF STATE FOR 
CENTRAL ASIA GEORGE KROL FOR REASONS 1.4 (B) AND (D) 
 '''),
    ('08STATE82744', 'BRIAN HOOK', u''' 
Classified By: CLASSIFIED BY IO A/S ACTING BRIAN HOOK 
FOR REASONS 1.4(B) AND (D). 
 '''),
    ('09SINGAPORE773', 'Daniel Shields', u''' 
Classified By: Charge d'Affaires (CDA) Daniel Shields for Reasons 1.4 ( 
b/b) 
 '''),
    ('07ASHGABAT350', 'Richard Hoagland', u''' 
Classified By: Classified by Acting Charge d\'Affaires, Ambassador Richa 
rd Hoagland, for reasons 1.4(B) and (D). 
 '''),
    ('05NEWDELHI8162', 'Bob Blake', u''' 
Classified By: Charge' Bob Blake for Reasons 1.4 (B, D) 
 '''),
    ('07RIYADH1028', 'BOB SILVERMAN', u''' 
Classified By: ECONOMIC COUNSELOR BOB SILVERMAN 
 FOR 12958 1.4 B, D, AND E 
 '''),
    ('05ROME3781', 'ANNA BORG', u''' 
Classified By: DCM ANNA BORG BASED ON E.O.12958 REASONS 1.4 (b) and (d) 
 '''),
    ('09STATE2508', 'PATRICIA A. MCNERNEA', u''' 
CLASSIFIED BY: ISN ? PATRICIA A. MCNERNEA, ACTING 
ASSISTANT SECRETARY, REASON 1.4 (B) AND (D) 
 '''),
    ('03OTTAWA2182', 'Mary Witt', u''' 
Classified By: A/ Pol Min Mary Witt for reasons 1.5(b) and (d) 
 '''),
    ('03KUWAIT3762', 'FRANK URBANCIC', u''' 
Classified By: CDA FRANK URBANCIC BASED UPON REASONS 1.5 (B) AND (D) 
 '''),
    ('07DAKAR1464', 'GARY SCHAAF', u''' 
Classified By: A/LEGATT GARY SCHAAF FOR RASONS 1.4 (B) AND (D). 
 '''),
    ('07HARARE680', 'Glenn Warren', u''' 
Classified By: Pol/Econ Chief Glenn Warren under 1.4 b/d 
 '''),
    ('09DHAKA775', 'James Moriarty', u''' 
Classified By: Ambassador James Moriarty for for reasons 1.4 b and d. 
 '''),
    (u'', 'Kelly A. Keiderling', u'''
Classified By: CDA Kelly A. Keiderling under 1.4 (b) and (d)
'''),
    ('04HARARE1722', 'Paul Weisenfeld', u''' 
Classified By: Classified by Charge d'Affaires Paul Weisenfeld under Se 
ction 1.5 b/d 
 '''),
    ('05SANTIAGO2540', 'SEAN MURPHY', u''' 
Classified By: CONSUL GENERAL SEAN MURPHY 
 
1. In a December 19 m'''),
    ('04HELSINKI1420', 'Earle I. Mack', u''' 
Classified By: Ambassador Earle I. Mack for reasons 1.5(B) and (D) 
 
Summary 
------- 
 '''),
    ('08PORTAUPRINCE520', 'Janet A. Sanderson', u''' 
Classified By: Ambassado Janet A. Sanderson for reasons 1.4 (b) and (d 
) 
 '''),
    ('97SOFIA3097', 'B0HLEN', u''' 
1.(U)  CLASSIFIED BY AMBASSAD0R B0HLEN.  REAS0N: 
1.5(B,D). 
 '''),
    ('99TUNIS2120', 'R0BIN L. RAPHEL', u''' 
(U)  CLASSIFIED BY AMBASSAD0R R0BIN L. RAPHEL BASED 0N 1.5 (B) 
AND (D). 
 '''),
    ('08TBILISI1121', 'John F. Tefft', u''' 
Classified By: Ambassadot John F. Tefft for reason 1.4 (b) and (d). 
 '''),
    ('07ANKARA2522', 'ROSS WILSON', u''' 
Classified By: AMBASSADR ROSS WILSON FOR REASONS 1.4 (B) AND (D) 
 '''),
    ('09UNVIEVIENNA531', 'Glyn T. Davies', u''' 
Classified By: Ambassadro Glyn T. Davies, reasons 1.4 (b) and (d) 
 '''),
    ('09TBILISI463', 'JOHN F. TEFFT', u''' 
Classified By: AMBSSADOR JOHN F. TEFFT.  REASONS:  1.4 (B) AND (D). 
 '''),
    ('09LUSAKA523', 'Donald E. Booth', u''' 
Classified By: Classified By: Ambbassador Donald E. Booth for 
Reasons 1.4 (b) and (d) 
 
 '''),
    ('07BAKU486', 'Anne E. Derse', u''' 
Classified By: Ambssador Anne E. Derse, Reasons 1.4 (b,d) 
 '''),
    ('09ANKARA63', 'A.F. Godfrey', u''' 
Classified By: Pol-Mil Counselor A.F. Godfrey 
 
Will Not Break Silence... 
------------------------- 
 
1. (C) I'''),
    ('03SANAA1319', 'ALAN MISENHEIMER', u''' 
Classified By: CHARGE ALAN MISENHEIMER F0R REASONS 1.5 (B) AND (D) 
 '''),
    ('08BAKU668', 'Alan Eyre', u''' 
Classified By: Acting Pol/Econ Chief Alan Eyre 
 
(S) In '''),
    ('07SINGAPORE285', 'Ike Reed', u''' 
Classified By: Economical and Political Chief Ike Reed; 
reasons 1.4 (b) and (d) 
 '''),
    ('07KHARTOUM832', 'Roberto Powers', r'''
Classified By: CDA Roberto Powers a.y., Sea3on: Sectaons 9.Q (b+`ald$hd 
)Q 
Q,----/-Qswmmfrq 
=,=--=HQ(@(RBF!&}ioSQB3wktf0r,vu qDWTel$1` \ulQlQO~jcvq>&Mw~ifw(U= ;QGM?QQx7Ab8QQ@@)\Minawi suggested that 
intelligence chief Salah Ghosh was the sole interlocutor with 
the "statesmanship" and influence within the regime to defuse 
tensions with the international community.  Embassy officials 
told Minawi that the NCP would need to demonstrate its 
genuine desire for better relations by agreeing to an 
effective UN peace-keeping operation, which could then lay 
the basis for future discussions.  Minawi also commented on 
Chad's obstruction of the Darfur peace process and an 
upcoming visit of Darfurian officials to Arab capitals.  End 
summary. 
 
-------------'''),
    ('05ANKARA7671', 'Nancy McEldowney', u''' 
Classified By: ADANA 222 
ADANA 216 
ADANA 207 
ANKARA 6772 
 
Classified by DCM Nancy McEldowney; reasons 1.4 b and d. 
 '''),
    ('04HARARE766', 'ROBERT E. WHITEHEAD', u''' 
Classified By: DCM ROBERT E. WHITEHEAD DUE TO 1,4 (C) AND (D). 
 '''),
    ('00TELAVIV4462', 'PSIMONS', u'''C O N F I D E N T I A L TEL AVIV 004462 
 
- - C O R R E C T E D  C O P Y - - CLASSIFIED BY LINE ADDED 
 
E.O. 12958: DECL: 08/24/05 
TAGS: KWBG, PTER, PGOV, PREL, IS 
SUBJECT: BIN LADIN CONNECTION IN GAZA FOUND PUZZLING; 
CONNECTION TO HAMAS QUESTIONED 
 
CLASSIFIED BY DCM PSIMONS PER 1.5 (B) AND (D) 
 
 '''),
)


_TEST_CABLES = (
    ('10BANGKOK468', ()),
    ('08STATE110079', ()),
    ('05VILNIUS1093', 'Derrick Hogan'),
    ('08STATE20184', ()),
    ('08STATE20332', ()),
    ('09ANKARA63', 'A.F. Godfrey'),
    ('03COLOMBO1348', 'Alex Moore'),
    ('03COLOMBO1810', 'Alex Moore'),
    ('66BUENOSAIRES2481', ()),
    ('05TAIPEI153', ()),
    ('09TELAVIV2643', ()),
    ('09BOGOTA2917',()),
    ('07TOKYO5202', ()),
    ('07USUNNEWYORK319', ()),
    ('07VIENNA1239', ()),
    ('09HONGKONG2247', ()),
    ('07TOKYO3205', ()),
    ('09HONGKONG2249', ()),
    ('07BELGRADE533', 'Ian Campbell'),
    ('05AMMAN646', ()),
    ('08BAGHDAD1451', 'Jess Baily'),
    ('08BAGHDAD1650', 'Jess Baily'),
    ('98STATE145892', 'Jeff Millington'),
    ('07TOKYO1414', ()),
    ('06COPENHAGEN1020', 'Bill Mozdzierz'),
    ('07ANKARA1581', 'Eric Green'),
    ('08ANKARA266', 'Eric Green'),
    ('08CHISINAU933', 'Daria Fane'),
    ('10RIGA27', 'Brian Phipps'),
    ('09WARSAW433', 'Jackson McDonald'),
    ('09BAGHDAD2784', 'Anbar'),
    ('05PARIS8353', 'Andrew, C. Koss'),
    ('05ANKARA581', 'John Kunstadter'),
    ('08RANGOON951', 'Drake Weisert'),
    ('10BAGHDAD488', 'John Underriner'),
    ('08STATE2004', 'Gordon Gray'),
    ('10BAGHDAD370', ()),
    ('09BEIJING951', 'Ben Moeling'),
    ('09TOKYO1878', 'Ray Hotz'),
    ('07OTTAWA100', 'Brian Mohler'),
    ('07BAMAKO1322', ()),
    ('09PRISTINA336', 'Michael J. Murphy'),
    ('09PRISTINA345', 'Michael J. Murphy'),
    ('06BAGHDAD4604', 'L. Hatton'),
    ('05ROME178', ('Castellano', 'Anna della Croce', 'Giovanni Brauzzi')),
    ('08USNATO348', 'W.S. Reid III'),
    ('09KHARTOUM107', 'Alberto M. Fernandez'),
    ('09ABUDHABI901', 'Douglas Greene'),
    ('03KUWAIT2352', 'Frank C. Urbancic'),
    ('09BUENOSAIRES849', 'Tom Kelly'),
    ('08BAGHDAD358', 'Todd Schwartz'),
    ('09BAGHDAD419', 'Michael Dodman'),
    ('10ADDISABABA186', ()),
    ('10ADDISABABA195', ()),
    ('10ASHGABAT178', 'Sylvia Reed Curran'),
    ('09MEXICO2309', 'Charles Barclay'),
    ('09MEXICO2339', 'Charles Barclay'),
    ('05ATHENS1903', 'Charles Ries'),
    ('02VATICAN25', 'Joseph Merante'),
    ('07ATHENS2029', 'Robin'),
    ('09HONGKONG934', ()),
    ('03KATHMANDU1044', 'Robert Boggs'),
    ('08CARACAS420', 'Robert Richard Downes'),
    ('08DHAKA812', 'Geeta Pasi'),
    ('09ULAANBAATAR87', ()),
    ('96JEDDAH948', 'Douglas Neumann'),
    ('09KABUL3161', 'Hoyt Yee'),
    ('03OTTAWA202', 'Brian Flora'),
    ('10GUATEMALA25', 'Drew G. Blakeney'),
    ('07CARACAS2254', 'Robert Downes'),
    ('09BUCHAREST115', 'Jeri Guthrie-Corn'),
    ('09BUCHAREST166', 'Jeri Guthrie-Corn'),
    ('06PANAMA2357', 'Luis Arreaga'),
    ('09JAKARTA1580', 'Ted Osius'),
    ('09JAKARTA1581', 'Ted Osius'),
    ('07ATHENS2219', 'Thomas Countryman'),
    ('09ANKARA1084', u"Daniel O'Grady"),
    ('10ANKARA173', u"Daniel O'Grady"),
    ('10ANKARA215', u"Daniel O'Grady"),
    ('10ANKARA224', u"Daniel O'Grady"),
    ('07BAGHDAD1513', 'Daniel V. Speckhard'),
    ('08TASHKENT1089', 'Jeff Hartman'),
    ('07HELSINKI636', 'Joy Shasteen'),
    ('09STATE57323', 'James Townsend'),
    ('09STATE59436', 'James Townsend'),
    ('07TASHKENT2064', ('Jeff Hartman', 'Steven Prohaska')),
    ('07DUSHANBE337', 'David Froman'),
    ('07DUSHANBE1589', 'David Froman'),
    ('08SANJOSE762', 'David E. Henifin'),
    ('05BAGHDAD3037', 'David M. Satterfield'),
    ('04AMMAN4133', 'D.Hale'),
    ('06YEREVAN237', 'A.F. Godfrey'),
    ('07DHAKA909', 'Dcmccullough'),
    ('07DHAKA1057', 'DCMcCullough'),
    ('07BAKU1017', 'Donald Lu'),
    ('07USNATO92', 'Clarence Juhl'),
    ('09KAMPALA272', 'Dcronin'),
    ('06LAGOS12', 'Sam Gaye'),
    ('07USNATO548', 'Clarence Juhl'),
    ('07TOKYO436', 'Carol T. Reynolds'),
    ('08STATE116100', 'Theresa L. Rusch'),
    ('07NEWDELHI5334', 'Ted Osius'),
    ('06BAGHDAD4350', 'Zalmay Khalilzad'),
    ('07STATE141771', 'Scott Marciel'),
    ('08STATE66299', 'David J. Kramer'),
    ('09STATE29700', 'Karen Stewart'),
    ('07NAIROBI4569', 'Jeffrey M. Roberts'),
    ('02HARARE2628', 'Rewhitehead'),
    ('04HARARE766', 'Robert E. Whitehead'),
    ('04ANKARA7050', 'John Kunstadter'),
    ('04ANKARA6368', 'Charles O. Blaha'),
    ('09BAGHDAD280', ()),
    ('05ABUJA1323', ()),
    ('07MONROVIA1375', 'Donald E. Booth'),
    ('03SANAA2434', 'Austin G. Gilreath'),
    ('07BRUSSELS3482', 'Maria Metcalf'),
    ('02KATHMANDU1201', 'Pete Fowler'),
    ('09STATE2522', 'Donald A. Camp'),
    ('09STATE100197', 'Roblake'),
    ('08COLOMBO213', 'Robert O. Blake, Jr.'),
    ('07MEXICO2653', 'Charles V. Barclay'),
    ('09SOFIA89', 'Mceldowney'),
    ('09ADDISABABA2168', 'Kirk McBride'),
    ('06MINSK338', 'George Krol'),
    ('10ADDISABABA195', ()),
    ('04AMMAN9411', 'Christopher Henzel'),
    ('06CAIRO4258', 'Catherine Hill-Herndon'),
    ('08NAIROBI233', 'John M. Yates'),
    ('06MADRID2993', ()),
    ('08AMMAN1821', ()),
    ('09KABUL1290', 'Patricia A. McNerney'),
    ('06JEDDAH765', 'Tatiana C. Gfoeller'),
    ('07BAGHDAD2045', 'Stephen Buckler'),
    ('07BAGHDAD2499', 'Steven Buckler'),
    ('04THEHAGUE1778', 'Liseli Mundie'),
    ('04THEHAGUE2020', 'John Hucke'),
    ('03HARARE1511', 'R.E. Whitehead'),
    ('03BRUSSELS4518', 'Van Reidhead'),
    ('02ROME4724', 'Douglas Feith'),
    ('08BRUSSELS1149', 'Chris Davis'),
    ('04BRUSSELS862', 'Frank Kerber'),
    ('08BRUSSELS1245', 'Chris Davis'),
    ('08BRUSSELS1458', 'Chris Davis'),
    ('07ISLAMABAD2316', 'Peter Bodde'),
    ('04MADRID764', 'Kathleen Fitzpatrick'),
    ('06BELGRADE1092', 'Ian Campbell'),
    ('07JERUSALEM1523', 'Jake Walles'),
    ('09PANAMA518', 'Barbar J. Stephenson'),
    ('06ABUDHABI409', 'Michelle J Sison'),
    ('07DOHA594', ()),
    ('07LAPAZ3136', 'Mike Hammer'),
    ('08BOGOTA4462', 'John S. Creamer'),
    ('09ATHENS1515', 'Deborah McCarthy'),
    ('09LONDON2347', 'Robin Quinville'),
    ('08LONDON821', 'Richard Mills, Jr.'),
    ('06BUENOSAIRES497', 'Line Gutierrez'),
    ('06BUENOSAIRES596', 'Line Gutierrez'),
    ('06BUENOSAIRES1243', 'Line Gutierrez'),
    ('05BAGHDAD3919', 'Robert Heine'),
    ('06RIYADH8836', 'Mgfoeller'),
    ('06BAGHDAD4422', 'Margaret Scobey'),
    ('08STATE129873', 'David Welch'),
    ('09BAGHDAD2299', 'Patricia Haslach'),
    ('09BAGHDAD2256', 'Phaslach'),
    ('09BAGHDAD2632', 'Phaslach'),
    ('04BAGHDAD697', 'Matthew Goshko'),
    ('05CAIRO8812', 'John Desrocher'),
    ('06HONGKONG4299', ()),
    ('06QUITO646', 'Vanessa Schulz'),
    ('08RIYADH1616', 'Scott McGehee'),
    ('08RIYADH1659', 'Scott McGehee'),
    ('10BAGHDAD481', 'W.S. Reid'),
    ('02KATHMANDU485', 'Pmahoney'),
    ('09BAGHDAD990', 'Robert Ford'),
    ('08BAGHDAD3023', 'Robert Ford'),
    ('09USNATO530', 'Kelly Degnan'),
    ('07LISBON2305', 'Lclifton'),
    ('08BAGHDAD4004', 'John Fox'),
    ('04THEHAGUE2346', 'A. Schofer'),
    ('07TALLINN173', 'Jessica Adkins'),
    ('09BAKU80', 'Rob Garverick'),
    ('06PHNOMPENH1757', 'Jennifer Spande'),
    ('06QUITO1401', 'Ned Kelly'),
    ('05ZAGREB724', 'Justin Friedman'),
    ('05TOKYO1351', 'David B. Shear'),
    ('07KIGALI73', 'G Learned'),
    ('08ZAGREB554', u"Peter D'Amico"),
    ('07TASHKENT1950', ('R. Fitzmaurice', 'T. Buckley')),
    ('07TASHKENT1679', ('Richard Fitzmaurice', 'Steven Prohaska')),
    ('07TASHKENT1894', ('Steven Prohaska', 'Richard Fitzmaurice')),
    ('08STATE68478', 'Margaret McKelvey'),
    ('04BRUSSELS416', 'Marc J. Meznar'),
    ('07BAGHDAD777', 'Jim Soriano'),
    ('05ALMATY3450', 'John Ordway'),
    ('05ACCRA2548', 'Nate Bluhm'),
    ('07ADDISABABA2523', 'Kent Healy'),
    ('09USUNNEWYORK746', 'Bruce C. Rashkow'),
    ('09STATE108370', 'Daniel Fried'),
    ('09BAGHDAD3120', 'Mark Storella'),
    ('09STATE64621', 'Richard C Holbrooke'),
    ('05NAIROBI4757', 'Chris Padilla'),
    ('05CAIRO5945', 'Stuart E. Jones'),
    ('07BAGHDAD1544', 'Steven R. Buckler'),
    ('07BAGHDAD1632', 'Steven R. Buckler'),
    ('02HARARE555', 'Aaron Tarver'),
    ('06BAGHDAD1021', 'Robert S. Ford'),
    ('06PRISTINA280', 'Philip S. Goldberg'),
    ('06SANSALVADOR849', 'Michael A. Butler'),
    ('06SUVA123', 'Larry M. Dinger'),
    ('06AITTAIPEI1142', 'Michael R. Wheeler'),
    ('08BEIRUT471', 'Michele J. Sison'),
    ('08MOSCOW937', 'Eric T. Schultz'),
    ('02HANOI2951', 'Emi Yamauchi'),
    ('08ROME525', 'Tom Delare',),
    ('01HARARE1632', 'Earl M. Irving'),
    ('06DUBAI5421', 'Timothy M. Brys'),
)


def test_parse_classified_by():
    def check(expected, content, normalize):
        if not isinstance(expected, tuple):
            expected = (expected,)
        eq_(expected, tuple(parse_classified_by(content, normalize)))
    for testcase in _TEST_DATA:
        if len(testcase) == 3:
            ref_id, expected, content = testcase
            normalize = False
        else:
            ref_id, expected, content, normalize = testcase
        yield check, expected, content, normalize


def test_cable_classified_by():
    def check(cable_id, expected):
        if not isinstance(expected, tuple):
            expected = (expected,)
        cable = cable_by_id(cable_id)
        ok_(cable, 'Cable "%s" not found' % cable_id)
        eq_(expected, tuple(cable.classified_by))
    for cable_id, expected in _TEST_CABLES:
        yield check, cable_id, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
