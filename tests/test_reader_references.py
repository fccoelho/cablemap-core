# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests references parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.reader import parse_references as reader_parse_references

def parse_references(content, year, reference_id=None):
    res = []
    for ref in reader_parse_references(content, year, reference_id):
        if not ref.is_cable():
            continue
        if ref.value not in res:
           res.append(ref.value)
    return res

_TEST_DATA = (
    # input string, year, optional reference_id, expected

    # 07TBILISI1732
    (r'\nREF: A. TBILISI 1605  B. TBILISI 1352  C. TBILISI 1100  D. 06 TBILISI 2601  E. 06 TBILISI 2590  F. 06 TBILISI 2425  G. 06 TBILISI 2390  H. 06 TBILISI 1532  I. 06 STATE 80908  J. 06 TBILISI 1064  K. 06 TBILISI 0619  L. 06 TBILISI 0397  M. 06 MOSCOW 0546  N. 06 TBILISI 0140  O. 05 TBILISI 3171',
     2007, [r'07TBILISI1605', r'07TBILISI1352', r'07TBILISI1100', r'06TBILISI2601', r'06TBILISI2590', r'06TBILISI2425', r'06TBILISI2390', r'06TBILISI1532', r'06STATE80908', r'06TBILISI1064', r'06TBILISI619', r'06TBILISI397', r'06MOSCOW546', r'06TBILISI140', r'05TBILISI3171']),
    # 08PARIS1698
    (u'''
REF: A. PARIS 1501
B. PARIS 1568
C. HOTR WASHINGTON DC//USDAO PARIS (SUBJ: IIR 6 832
0617 08)
D. HOTR WASHINGTON DC//USDAO PARIS (SUBJ: IIR 6 832
0626 08) ''', 2008,
     [r'08PARIS1501', r'08PARIS1568']),
    # 08PARIS1501
    (r'\nREF: A. 05 PARIS 5459 \nB. 06 PARIS 5733', 2008,
     [r'05PARIS5459', r'06PARIS5733']),
    # 07TALLINN375
    (r'\nREF: A) TALLINN 366 B) LEE-GOLDSTEIN EMAIL 05/11/07 \nB) TALLINN 347 ', 2007,
     [r'07TALLINN366', r'07TALLINN347']),
    # 07TRIPOLI943
    (r'\nREF: A) STATE 135205; B) STATE 127608; C) JOHNSON-STEVENS/GODFREY E-MAIL 10/15/07; D) TRIPOLI 797; E) TRIPOLI 723 AND PREVIOUS', 2007,
     [r'07STATE135205', r'07STATE127608', r'07TRIPOLI797', r'07TRIPOLI723']),
    # 07STATE156011
    (r'  REF: LA PAZ 2974', 2007, [r'07LAPAZ2974']),
    # 05PARIS7835
    (r'\nREF: A. (A) PARIS 7682 AND PREVIOUS ', 2005, [r'05PARIS7682']),
    # 05PARIS7835
    (r'\nREF: A. (A) PARIS 7682 AND PREVIOUS \n\nB. (B) EMBASSY PARIS DAILY REPORT FOR OCTOBER 28 - \nNOVEMBER 16 (PARIS SIPRNET SITE) \nC. (C) PARIS 7527 ', 2005,
     [r'05PARIS7682', r'05PARIS7527']),
    # 09MADRID869
    (r'\nSUBJECT: UPDATES IN SPAIN’S INVESTIGATIONS OF RUSSIAN MAFIA \nREF: A. OSC EUP20080707950031  B. OSC EUP20081019950022  C. OSC EUP20090608178005  D. MADRID 286  E. OSC EUP20050620950076  F. OSC EUP20080708950049  G. OSC EUP20081029950032  H. OSC EUP 20061127123001\nMADRID 00000869 001.2 OF 004\n', 2009,
     [r'09MADRID286']),
    # 07STATE152317
    (r'\nREF: (A)STATE 071143, (B)STATE 073601, (C)STATE 72896, (D)BEIJING \n5361, (E) STATE 148514', 2007,
     [r'07STATE71143', r'07STATE73601', r'07STATE72896', r'07BEIJING5361', r'07STATE148514']),
    # 08MANAGUA573
    (r'\nREF: A. MANAGUA 520 \nB. MANAGUA 500 \nC. MANAGUA 443 \nD. MANAGUA 340 \nE. MANAGUA 325 \nF. MANAGUA 289 \nG. MANAGUA 263 \nH. MANAGUA 130 \nI. 2007 MANAGUA 2135 \nJ. 2007 MANAGUA 1730 \nK. 2007 MANAGUA 964 \nL. 2006 MANAGUA 2611 ', 2008,
     [r'08MANAGUA520', r'08MANAGUA500', r'08MANAGUA443', r'08MANAGUA340', r'08MANAGUA325', r'08MANAGUA289', r'08MANAGUA263', r'08MANAGUA130', r'07MANAGUA2135', r'07MANAGUA1730', r'07MANAGUA964', r'06MANAGUA2611']),
    # 66BUENOSAIRES2481
    (r'\n REF: STATE 106206 CIRCULAR; STATE CA-3400 NOV 2, 1966 ', 1966, [r'66STATE106206']),
    #04MADRID4063
    (r'\nREF: EMBASSY MADRID E-MAIL TO EUR/WE OF OCTOBER 14\n', 2004, []),
    #08RIYADH1134
    (r'\nREF: A. SECSTATE 74879 \n     B. RIYADH 43 \n', 2008, [r'08STATE74879', r'08RIYADH43']),
    #08RIODEJANEIRO165
    (r'TAGS: ECON EINV ENRG PGOV PBTS MARR BR\n\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ', 2008,
     [r'08RIODEJANEIRO138', r'08RIODEJANEIRO44']),
    (r'\nREF: A. A) SECSTATE 54183 B. B) 07 BRASILIA 1868 C. C) STATE 57700 D. 07 STATE 17940 Classified By: DCM Phillip Chicola, Reason 1.5 (d) ', 2008,
    [r'08STATE54183', r'07BRASILIA1868', r'08STATE57700', r'07STATE17940']),
    # 08BRASILIA806
    (r'\nPROGRAM REF: A. A) SECSTATE 54183 B. B) 07 BRASILIA 1868 C. C) STATE 57700 D. 07 STATE 17940 Classified By: DCM Phillip Chicola, Reason 1.5 (d) ', 2008,
     [r'08STATE54183', r'07BRASILIA1868', r'08STATE57700', r'07STATE17940']),
    # 06SAOPAULO276
    (r'\nCARDINAL HUMMES DISCUSSES LULA GOVERNMENT, THE OPPOSITION, AND FTAA REF: (A) 05 SAO PAULO 405; (B) 05 SAO PAULO 402 (C) 02 BRASILIA 2670', 2006,
     [r'05SAOPAULO405', r'05SAOPAULO402', r'02BRASILIA2670']),
    # 08BERLIN1387
    (r'\nREF: A. BERLIN 1045\nB. SECDEF MSG DTG 301601z SEP 08', 2008, [r'08BERLIN1045']),
    #09NAIROBI1938
    (r'\nREF: A. 08 STATE 81854\n\n\nS e c r e t nairobi 001938', 2009, [r'08STATE81854']),
    # 02ROME1196
    (r'\nREF: A. STATE 40721\n CONFIDENTIAL\\nPAGE 02 ROME 01196 01 OF 02 082030Z  B. ROME 1098  C. ROME 894  D. MYRIAD POST-DEPARTMENT E-MAILS FROM 10/01-02/02  E. ROME 348\nCLASSIFIED BY: POL', 2002,
     [r'02STATE40721', r'02ROME1098', r'02ROME894', r'02ROME348']),
    # 10TRIPOLI167
    (r'\nREF: TRIPOLI 115\n\n1.(SBU) This is an action request; please see para 4.\n\n', 2010, [r'10TRIPOLI115']),
    # 06BRASILIA882
    (r'SUBJECT: ENERGY INSTALLATIONS REF: BRASILIA 861', 2006, [r'06BRASILIA861']),
    # 08MOSCOW864
    ("TAGS: EPET ENRG ECON PREL PGOV RS\nSUBJECT: WHAT'S BEHIND THE RAIDS ON TNK-BP AND BP REF: A. MOSCOW 816 B. MOSCOW 768 C. 07 MOSCOW 3054 Classified By: Ambassador William J. Burns for Reasons 1.4 (b/d)\n", 2008,
     [r'08MOSCOW816', r'08MOSCOW768', r'07MOSCOW3054']),
    # 08TRIPOLI402
    (r'REF: A) TRIPOLI 199, B) TRIPOLI 227 TRIPOLI 00000402 \n\n001.2 OF 003 ', 2008, '08TRIPOLI402',
      [r'08TRIPOLI199', r'08TRIPOLI227']),
    # 08LONDON2627
    (u'''
E.O. 12958: N/A TAGS: AMGT

SUBJECT: UK COUNTRY CLEARANCE IS GRANTED TO STAMILIO, LTC DODSON AND LTCOL HAVRANEK REF: SECDEF R162245Z OCT 08

1.Embassy London is pleased to grant country clearance to Mr. Mark Stamilio, LTCOL John Havranek, and LTC James Dodson to visit London October 19-20 to attend working level meetings on ISAF detention policies and practices.

2. ---------------- Visit Officer ---------------- 

XXXXXXXXXXXX If calling from within the UK replace 44 with 0, if calling from landline to landline within London, dial only the last eight digits.

3. Confirmed reservations are held for Stamilio, Havranek and Dodson at Marriott Grosvernor Square.The rate is within per diem. The confirmation number are: Stamilio - 84274267, Havranek, 84274449, and Dodson, 84274523. London Marriott Grosvenor Square, Grosvenor Square, London W1A 4AW. Telephone number is (44)(0)20 7493-1232 Fax number is (44)(0)20 7491-3201. If calling from within the UK replace 44 with 0; if calling from landline within London, dial only the last eight digits.

4.Carry
''', 2008, []),
    # 08BRASILIA429
    (u'''
SUBJECT: THOUGHTS ON THE VISIT OF DEFENSE MINISTER JOBIM TO WASHINGTON 

REF: A. A) BRASILIA 236 B. B) OSD REPORT DTG 251847Z MAR 08 C. C) BRASILIA 175 
Classified By: Ambassador Clifford Sobel. 
Reason: 1.5 d 
''', 2008, [r'08BRASILIA236', r'08BRASILIA175']),
    # 09PARIS1039
    (u'''
SUBJECT: FRANCE’S POSITION ON NUCLEAR ISSUES IN THE RUN-UP 
TO THE NPT REVCON

REF: A. PARIS POINTS JULY 15  B. PARIS POINTS JULY 6  C. PARIS POINTS APRIL 10  D. PARIS 1025

Classified By:
''', 2009, [r'09PARIS1025']),
    # 08BERLIN1387
    (u'''
SUBJECT: GERMANY: BUNDESTAG SET TO RENEW A BEEFED-UP ISAF
MANDATE AND A SCALED-DOWN OEF COUNTERPART

REF: A. BERLIN 1045 
¶B. SECDEF MSG DTG 301601z SEP 08

Classified By: CHARGE D'AFFAIRES''',
     2008,
     [r'08BERLIN1045']),
    # 08STATE15220
    (u'''
Subject: (s) further scheming by german firm to export
test chamber to iranian ballistic missile program

Ref: a. 05 state 201650

B. 05 berlin 3726
c. 05 state 211408
d. 05 berlin 3954
e. 06 state 36325
f. 06 berlin 674
g. 06 state 62278
h. 06 berlin 1123
i. 06 state 70328
j. 06 berlin 1229
k. 06 berlin 1550
l. Mtcr poc 201/2006 - may 16 2006
m. 07 state 75839
n. 07 berlin 1137
o. 07 state 108420
p. 07 berlin 002163
q. 07 state 166482
r. 07 berlin 2216

Classified By: ISN/MTR DIRECTOR PAM DURHAM
for reasons 1.4 (b), (d).
''', 2008,
     [r'05STATE201650', r'05BERLIN3726', r'05STATE211408', r'05BERLIN3954', r'06STATE36325', r'06BERLIN674', r'06STATE62278', r'06BERLIN1123', r'06STATE70328', r'06BERLIN1229', r'06BERLIN1550', r'07STATE75839', r'07BERLIN1137', r'07STATE108420', r'07BERLIN2163', r'07STATE166482', r'07BERLIN2216']),
    # 09PARIS504
    (u'''SUBJECT: DRC/ROC/NIGER: FRENCH PRESIDENCY'S READOUT OF 
SARKOZY'S MARCH 26-27 VISITS 

REF: A. PARIS 399 
B. KINSHASA 291 
C. BRAZZAVILLE 101 
D. NIAMEY 234 
E. 08 PARIS 1501 
F. 08 PARIS 1568 
G. 08 PARIS 1698 

Classified By: Political Minister-Counselor Kathleen Allegrone, 1.4 (b/ 
d). ''',
     2009,
     [r'09PARIS399', r'09KINSHASA291', r'09BRAZZAVILLE101', r'09NIAMEY234', r'08PARIS1501', r'08PARIS1568', r'08PARIS1698']),
    # 10THEHAGUE114
    (u'''SUBJECT: NETHERLANDS/AFGHANISTAN: A REDUCED ROLE LIKELY BUT
DETAILS WILL NOT COME QUICKLY
REF: A. THE HAGUE 109
B. THE HAGUE 108
C. THE HAGUE 097
D. 09 THE HAGUE 759
Classified By: Deput''',
     2010,
     [r'10THEHAGUE109', r'10THEHAGUE108', '10THEHAGUE97', '09THEHAGUE759']),
    # 03THEHAGUE2597
    (u'''REF: A. RICHARD-WITMER EMAIL 10/9 

B. WITMER-HOLLIDAY EMAILS 9-22 THRU 10-7 ''',
     2003,
     []),
    # 10STATE16220
    (u'''SUBJECT: IRISL'S UNINSURED FLEET AND EVASIVE ACTIONS NECESSITATE DENIAL OF PORT ENTRY WORLDWIDE 

REF A) LONDON 002351 B) STATE 069339 C) STATE 094723 D) STATE 104496 E) STATE 108151 F) HAMILTON 00014 G) STATE 125339 H) STATE 1760 I) STATE 52348 J) STATE 121818 K) STATE 115243 L) STATE 90303 STATE 00016220 001.2 OF 005 M) STATE 7877 N) SINGAPORE 00083 O) UNSCR 1737 SANCTIONS COMMITTEE IMPLEMENTATION ASSISTANCE NOTICE- 24 JULY 2009 P) UNSCR 1737 SANCTIONS COMMITTEE IMPLEMENTATION ASSISTANCE NOTICE- 20 JANUARY 2010

1. (U) This''',
     2010, '10STATE16220',
     [r'10LONDON2351', r'10STATE69339', r'10STATE94723', r'10STATE104496', r'10STATE108151', r'10HAMILTON14', r'10STATE125339', r'10STATE1760', r'10STATE52348', r'10STATE121818', r'10STATE115243', r'10STATE90303', r'10STATE7877', r'10SINGAPORE83']),
    # 10CAIRO177
    (u'''
SUBJECT: Sinai Update: Counter Smuggling and Floods 
 
REF: SECDEF 122723; CAIRO IIR 6 899 0149 10; 2009 CAIRO 2394 
2009 CAIRO 491 

CLASSIFIED BY:''',
    2010,
    [r'10SECDEF122723', r'09CAIRO2394', r'09CAIRO491']),
    # 08LONDON1991
    (u'''SUBJECT: (C/NF) WHO WOULD REPLACE GORDON BROWN AS UK PRIMEREF: A. LONDON 1939  B. LONDON 1704''',
     2008,
     [r'08LONDON1939', r'08LONDON1704']),
    # 06CAIRO941
    (u'''SUBJECT: FBI DIRECTOR MUELLER’S VISIT TO EGYPTREF: CAIRO 493

Classified by DCM Stua''',
     2006,
     [r'06CAIRO493']),
    # 04BRASILIA445
    (u'''E.O. 12958: N/A 
TAGS: KIPR ECON ETRD KCRM PGOV BR IPR

SUBJECT: BRAZIL - 2004 SPECIAL 301 RESPONSE 

Refs: A) State 29549 
B) Sao Paulo 276 
C) Rio de Janeiro 128 
D) Brasilia 313 
E) Brasilia 222 
F) Brasilia 202 
G) 2003 Sao Paulo 2199 
H) 2003 Brasilia 3868 
I) 2003 Brasilia 3138 
J) 2003 Brasilia 3122 
K) 2003 Brasilia 2943 
L) 2003 Sao Paulo 1186 
''',
     2004,
     [r'04STATE29549', r'04SAOPAULO276', r'04RIODEJANEIRO128', r'04BRASILIA313', r'04BRASILIA222', r'04BRASILIA202', r'03SAOPAULO2199', r'03BRASILIA3868', r'03BRASILIA3138', r'03BRASILIA3122', r'03BRASILIA2943', r'03SAOPAULO1186']),
    # 06SAOPAULO532
    (u'''
E.O. 12958: N/A TAGS: PGOV PHUM KCRM SOCI SNAR ASEC BR

REF: (A) Sao Paulo 526; 
(B) Sao Paulo 319; 
(C) Sao Paulo 42; 
(D) 05 Sao Paulo 975 

SENSITIVE BUT UNCLASSIFIED
''',
     2006,
     [r'06SAOPAULO526', r'06SAOPAULO319', r'06SAOPAULO42', r'05SAOPAULO975']),
    # 08LIMA480
    (u'''
E.O. 12958:DECL: 03/18/2018   TAGS: PGOV PREL PINR PE

REF: A. LIMA 0389        
B. LIMA 3853        
C. LIMA 0390      

Classified By: 
''',
     2008,
     [r'08LIMA389', r'08LIMA3853', r'08LIMA390']),
    # 08MANAMA117
    (u'''
UBJECT: BAHRAIN WILL FORMALLY REQUEST QATAR TO EXECUTE LEGAL JUDGMENT AGAINST KHALIFA AL SUBAIE REF: A. A) MANAMA 20 
B. B) 2/22/08 GRAY-ERELI E-MAIL 

Classified By''',
     2008,
     [r'08MANAMA20']),
    # 08MANAMA492 (08ECTION01OF02MANAMA492)
    (u'''SUBJECT: BAHRAIN SEEKS IOM'S ASSISTANCE TO COBAT TIP 
 
REF: A. MANAMA 165 B. MANAMA 320 C. MANAMA 363 D. MANAMA 486 Classiied By: CDA Chr''',
     2008,
     [r'08MANAMA165', r'08MANAMA320', r'08MANAMA363', r'08MANAMA486']),
    # 06GENEVA1673
    (r'''TAGS: PHUM UNHRC
SUBJECT: HRC: SPECIAL SESSION ON PALESTINE \
 \
REF: A. A) BERN 1253 \
 \
     B. B) GENEVA 1633 \
 \
Classified By: Pol''',
     2006,
     [r'06BERN1253', r'06GENEVA1633']),
    # 10UNESCOPARISFR197
    (u'''SUBJECT: HAITI EARTHQUAKE:  DISCUSSION WITH UNESCO DIRECTOR-GENERAL 
 
REF: (A) USUNESCO PARIS FR 000087, (B) USUNESCO PARIS FR 00187 
 
1.  Ambassador [...]''',
     2010,
     ['10UNESCOPARISFR87', '10UNESCOPARISFR187']),
    # 08PARISFR2202
    (u'''SUBJECT: UNESCO DIRECTOR GENERAL SUCCESSION:  CONVERSATIONS WITH 
MEXICO, SWEDEN, BRAZIL, FRANCE, AND TURKEY 
 
REF: (A) PARIS FR 2144 
     (B) PARIS FR 2153 
 
Classified by Amb[...]''',
     2008,
     [r'08UNESCOPARISFR2144', r'08UNESCOPARISFR2153']),
    # 10UNESCOPARISFR187
    (u'''SUBJECT: HAITI EARTHQUAKE:  UNESCO MEETING ON SAVING HAITI'S 
HERITAGE 
 
REF: UNESCO PARIS FR 000087 

1. Summary. UNESCO, ''',
     2010,
     [r'10UNESCOPARISFR87']),
    # 09UNVIEVIENNA553
    (u'''SUBJECT: AUSTRIAN AMBASSADOR TO IRAN DESCRIBES ELECTIONS AS 
DRIVING TEHRAN ENVIRONMENT 
 
REF: UNVIE 544 
 
Classified By: DCM''', 2010,
     [r'10UNVIEVIENNA544']),
    # 09UNVIEVIENNA322
    (u'''SUBJECT: IAEA LEADERSHIP TEAM TRANSITION AND U.S. INFLUENCE 
IN THE AGENCY 
 
REF: A. UNVIE 148 
     B. UNVIE 102 (NOTAL) 
     C. UNVIE 089 
     D. UNVIE 076 
 
Classified By:''',
     2009,
     [r'09UNVIEVIENNA148', r'09UNVIEVIENNA102', r'09UNVIEVIENNA89', r'09UNVIEVIENNA76']),
    # 09UNVIEVIENNA540
    (u'''SUBJECT: STAFFDEL KESSLER EXAMINES IRAN, SYRIA, AND 
MULTILATERAL VIENNA’S FRUSTRATING NAM DYNAMIC
REF: EMBASSY VIENNA 1450
Classified By: Mark''',
     2009,
     [r'09VIENNA1450']),
    # 08BRASILIA672
    (u'''SUBJECT: SOURCES OF GENERATION - ELECTRICITY SERIES #2 
 
SENSITIVE BUT UNCLASSIFED--PLEASE PROTECT ACCORDINGLY 
 
REF: A: Sao Paulo 0031; B: La Paz 0462; C: 06 Sao Paulo 1059 D: 
Brasilia 00593; E: Sao Paulo  F: Rio 0091 
 
 
1.(U)SUMMARY: As''',
     2008,
     [r'08SAOPAULO31', r'08LAPAZ462', r'06SAOPAULO1059', r'08BRASILIA593', r'08RIODEJANEIRO91']),
    # 04RIODEJANEIRO1105
    (u'''SUBJECT: BRZAIL'S MINAS GERAIS:  PT INCUMBENT COULD 
WIN A TIGHT RACE IN BRAZIL'S THIRD CITY 
 
Refs:  (A) Rio de Janeiro 00190  (B) Rio de Janeiro 
 
00723  (C) Brasilia 01392 
 
1.  (U)  SUMMARY''',
     2004,
     [r'04RIODEJANEIRO190', r'04RIODEJANEIRO723', r'04BRASILIA1392']),
    # 05RIODEJANEIRO19
    (u'''SUBJECT:  Brazil - Bahia State Growing Faster but Interior 
Still a Problem 
 
Ref:  2003 Rio de Janeiro 1773 
 
Summary 
------- ''',
     2005,
     [r'03RIODEJANEIRO1773']),
    # 05RIODEJANEIRO1120
    (u'''SUBJECT: MINAS GERAIS:  THE VIEW FROM BELO HORIZONTE 
 
Reftel:  Rio de Janeiro 1118 
 
SUMMARY 
------- ''',
     2005,
     [r'05RIODEJANEIRO1118']),
    # 08RIODEJANEIRO135
    (u'''SUBJECT: Petrobras Delays Some Subsalt Tests Due to Equipment 
Shortage 
 
REF: A) RIO DE JANEIRO 91, B) RIO DE JANEIRO 35, C) 07 SAO PAULO 
0953 
 
1. Summary. ''',
     2008,
     [r'08RIODEJANEIRO91', r'08RIODEJANEIRO35', r'07SAOPAULO953']),
    # 09RIODEJANEIRO357
    (u'''SUBJECT: (C) WAR BY ANY OTHER NAME: RIO'S "INTERNAL ARMED CONFLICT" 

REF: A. (A) RIO 329 
¶B. (B) RIO 346 Classified By: Principal Officer Dennis W. Hearne for reasons 1.4 (b, d ) 

¶1. (C) Summary: Rio Principal''',
     2009,
     [r'09RIODEJANEIRO329', r'09RIODEJANEIRO346']),
    # 05BOGOTA3726
    (u'''SUBJECT: PEACE PROCESS WITH ELN STALLS
 
REF: A. BOGOTA 1775
 
     ¶B. BOGOTA 3422
     ¶C. CARACAS 0951
 
Classified By: Ambassador Willia''',
     2005,
     [r'05BOGOTA1775', r'05BOGOTA3422', r'05CARACAS951']),
    # 09CAIRO2205
    (u'''POSTS FOR FRAUD PREVENTION UNITS E.O. 12958: N/A TAGS: KFRDKIRFCVISCMGTKOCIASECPHUMSMIGEG

SUBJECT: BLIND COPTIC GIRLS' CHOIR USED FOR ALIEN SMUGGLING REF: CAIRO 2178

1.(SBU) Summary:''',
     2009,
     [r'09CAIRO2178']),
    # 09BERLIN1116
    (u'''E.O. 12958: DECL: 09/10/2034 TAGS: ETTC PGOV PINR MCAP PREL TSPAM JP FR SP UK
REF: A. BERLIN 1080 B. BERLIN 1049 C. BERLIN 765 D. BERLIN 601 E. BERLIN 561 F. BERLIN 181 G. 08 BERLIN 1575

Classified By: Global Affairs''',
     2009,
     [r'09BERLIN1080', r'09BERLIN1049', r'09BERLIN765', r'09BERLIN601', r'09BERLIN561', r'09BERLIN181', r'08BERLIN1575']),
    # 09SAOPAULO558
    (u'''E.O. 12958: N/A 
TAGS: PINR PGOV PREL SNAR BR AVERY
SUBJECT: WHAT HAPPENED TO THE PCC? 
 
REF: A. ASUNCION 701 (08) 
     ¶B. ASUNCION 338 (07) 
     ¶C. INCSR BRAZIL 2008 
     ¶D. SAO PAULO 228 (08) 
     ¶E. SAO PAULO 66 (08) 
     ¶F. SAO PAULO 873 (07) 
     ¶G. SAO PAULO 447 (07) 
     ¶H. SAO PAULO 975 (06) 
     ¶I. SAO PAULO 526 (06) 
     ¶J. SAO PAULO 319 (06) 
 
¶1.  (SBU) Summary: For thre''',
     2009,
     [r'08ASUNCION701',
      r'07ASUNCION338',
      r'08SAOPAULO228',
      r'08SAOPAULO66',
      r'07SAOPAULO873',
      r'07SAOPAULO447',
      r'06SAOPAULO975',
      r'06SAOPAULO526',
      r'06SAOPAULO319']),
    # 07KINGSTON393
    (u'''SUBJECT: JAMAICA/VENEZUELA: OPPOSITION LEADER DEEPLY 
CONCERNED OVER CHAVEZ'S INFLUENCE 
 
REF: A. KINGSTON 89 (NOTAL) 
     ¶B. KINGSTON 215 (NOTAL) 
     ¶C. 06 KINGSTON 2021 (NOTAL) 
     ¶D. KINGSTON 342 (NOTAL) 
     ¶E. PORT-OF-SPAIN 220 (NOTAL) 
 
Classified By: Ambassador Brenda''',
     2007,
     [r'07KINGSTON89', r'07KINGSTON215', r'06KINGSTON2021', r'07KINGSTON342', r'07PORTOFSPAIN220']),
    # 06PORTAUPRINCE2230
    (u'''SUBJECT: COLLEAGUE CHRONICLES CORRUPTION OF YOURI LATORTUE REF: PORT AU PRINCE 01407 PORT AU PR 00002230 001.2 OF 002 Classified By:''',
     2006,
     [r'06PORTAUPRINCE1407']),
    # 06MONTREAL436
    (u'''SUBJECT: IPR in Montreal Part 2 - Music Fans and Industry Stakeholders Take IPR Into Their Own Hands Ref: A Montreal 365, B Ottawa 406, C 05 Ottawa 2970 This message is Sensitive but Unclassified ''',
     2006,
     [r'06MONTREAL365', r'06OTTAWA406', r'05OTTAWA2970']),
    # 06WELLINGTON725
    (u'''SUBJECT: DON BRASH NOT DOWN FOR THE COUNT - YET 
 
REF A WELLINGTON 721 B WELLINGTON 690 
 
Summary ''',
     2006,
     [r'06WELLINGTON721', r'06WELLINGTON690']),
    # 10QUITO33
    (u'''SUBJECT: New Foreign Minister Patino from Left Side of Correa's 
Circle 
 
REF: QUITO 5; 094 QUITO 841; 08 QUITO 1062; 07 QUITO 1607 
07 QUITO 290; 06 QUITO 2937 
 
CLASSIFIED BY''',
     2010,
     [r'10QUITO5', r'94QUITO841', r'08QUITO1062', r'07QUITO1607', r'07QUITO290', r'06QUITO2937']),
    # 10HAVANA9
    (u'''REF: A. REF A HAVANA 639 ("A SPLENDID LITTLE VISIT") ¶B. B HAVANA 772 (CONSULAR VISIT TO JAILED AMCIT) ¶C. C HAVANA 763 (CUBA PASSES UP ON REFORMS) ¶D. D HAVANA 739 (STRIDENT PROTEST) ¶E. E HAVANA 736 (HUMAN RIGHTS MARCHES TURN VIOLENT) ¶F. F HAVANA 755 (CUBAN FEATHERS RUFFLED BY USCG RESCUE) ''',
     2010,
     [r'10HAVANA639', r'10HAVANA772', r'10HAVANA763', r'10HAVANA739', r'10HAVANA736', r'10HAVANA755']),
    # 09NDJAMENA588
    (u'''REF: A. NDJAMENA 520 ¶B. N'DJAMENA 511 ¶C. N'DJAMENA 521''',
     2009,
     [r'09NDJAMENA520', r'09NDJAMENA511', r'09NDJAMENA521']),
    # 09LONDON2697
    (u'''REF: A. REF A STATE 122214 B. REF B LONDON 2649 C. REF C LONDON 2638 ''',
     2009,
     [r'09STATE122214', r'09LONDON2649', r'09LONDON2638']),
    # 04BRASILIA676
    (u'''REF: A. A. STATE 56282 ¶B. B. STATE 56666 ¶C. C. STATE 41252 AND 44603 ¶D. D. BRASILIA 616 ''',
     2004,
     [r'04STATE56282', r'04STATE56666', r'04STATE41252', r'04STATE44603', r'04BRASILIA616']),
    # 04BRASILIA2863
    (u'''REF: A. BRASILIA 2799 AND 2764 ¶B. PORT AU PRINCE 2325 ''',
     2004,
     [r'04BRASILIA2799', r'04BRASILIA2764', r'04PORTAUPRINCE2325']),
    # 02ROME1196
    (u'''SUBJECT: AS PREDICTED, ITALY'S HUMAN RIGHTS REPORT GENERATES FODDER FOR DOMESTIC POLITICAL MILLS REF: A. STATE 40721 CONFIDENTIAL PAGE 02 ROME 01196 01 OF 02 082030Z B. ROME 1098 C. ROME 894 D. MYRIAD POST-DEPARTMENT E-MAILS FROM 10/01-02/02 E. ROME 348 CLASSIFIED BY: POL''',
     2002,
     [r'02STATE40721', r'02ROME1098', r'02ROME894', r'02ROME348']),
    # 03HALIFAX308
    (u'''SUBJECT: THANKS A LOT, JUAN REF: HILL - OPS CENTER TELCONS 9/28 AND 29 ''',
     2003,
     []),
    # 05WELLINGTON489
    (u'''REF: SECSTATE 113408 AND SECSTATE 113635 ''',
     2005,
     [r'05STATE113408', r'05STATE113635']),
    # 05HELSINKI924
    (u'''REF: A. STATE 1531333 ¶B. STOCKHOLM 1498 ¶C. BISHTEK 1194 ¶D. SCHLAEFER/THOME-EUR/NB E-MAILS 22-24 AUG 05 ''',
     2005,
     [r'05STATE1531333', r'05STOCKHOLM1498', r'05BISHKEK1194']),
    # 05VATICAN514
    (u'''REF: A. A) ROME 2543, ¶B. 05 ROME 2543, 03 VAT 4859; 03 ROME 5205; 04 VAT 3810 ''',
     2005,
     [r'05ROME2543', r'03VATICAN4859', r'03ROME5205', r'04VATICAN3810']),
    # 07SAOPAULO161
    (u'''REF: A) 05 SAO PAUO 1106; B) 05 SAO PAULO 703; C) 05 SAO PAUL 614 SAO PAULO 00000161 001.3 OF 005 SENSITIVE BUT UNCLASSIFIED; PLEASE''',
     2007,
     [r'05SAOPAULO1106', r'05SAOPAULO703', r'05SAOPAULO614']),
    # 07PRISTINA102
    (u'''REF: SECTSTATE 14985 ''',
     2007,
     [r'07STATE14985']),
    # 09THEHAGUE264
    (u'''REF: A. 08 HAGUE 468 ¶B. 07 HAGUE 714 ¶C. 07 HAGUE 247 ¶D. 07 HAGUE 063''',
     2009,
     [r'08THEHAGUE468', r'07THEHAGUE714', r'07THEHAGUE247', r'07THEHAGUE63']),
    # 09PHNOMPENH564
    (u'''REF: A. PHNOM PENH 343 ¶B. PHNOM PEN 333 ¶C. PHNOM PENH 316 ¶D. PHNOM PENH 264 ''',
     2009,
     [r'09PHNOMPENH343', r'09PHNOMPENH333', r'09PHNOMPENH316', r'09PHNOMPENH264']),
    # 09TRIPOLI661
    (u'''REF: A) 07 TRIPOLI 656; B) 07 TRIPOLII 695 TRIPOLI 00000661 001.2 OF 002 CLASSIFIED BY: ''',
     2009,
     [r'07TRIPOLI656', r'07TRIPOLI695']),
    # 09BRASILIA1127
    (u'''REF: A. BRASILIA 1099 ¶B. BRASILA 931 ''',
     2009,
     [r'09BRASILIA1099', r'09BRASILIA931']),
    # 09MEXICO2701
    (u'''REF: A. MEXICO CITY 2636 ¶B. MEXICO CITY 2556 ¶C. MEXICO CITY 2675. ''',
     2009,
     [r'09MEXICO2636', r'09MEXICO2556', r'09MEXICO2675']),
    # 09USUNNEWYORK828
    (u'''REF: A. USUN NEW YORK 827 ¶B. USUN NEW YORK 634 ¶C. USUN NE YORK 609 ¶D. USUN NEW YORK 553 ¶E. USUN NEW YORK 432 ¶F. USUN NEW YORK 388 ¶G. USUN NEW YORK 345 ¶H. USUN NEW YORK 289 ¶I. USUN NEW YORK 230 ''',
     2009,
     [r'09USUNNEWYORK827', r'09USUNNEWYORK634', r'09USUNNEWYORK609', r'09USUNNEWYORK553', r'09USUNNEWYORK432', r'09USUNNEWYORK388', r'09USUNNEWYORK345', r'09USUNNEWYORK289', r'09USUNNEWYORK230']),
    # 09BRASILIA1314
    (u'''REF: A. SECSTATE 116264 ¶B. BRAZIL 1280 ''',
     2009,
     [r'09STATE116264', r'09BRASILIA1280']),
    # 06BUENOSAIRES1439
    (u'''REF: A. BA 1485 ¶B. BA 1062 ''',
     2006,
     [r'06BUENOSAIRES1485', r'06BUENOSAIRES1062']),
    # 01VATICAN5693
    (u'''SUBJECT:  SOUTH ASIA BUREAU AFGHANISTAN COORDINATOR 
BRIEFS VATICAN. 
 
REF. STATE 184178 
                       CONFIDENTIAL 
 
PAGE 02        VATICA  05693  01 OF 02  021700Z 
 
CLASSIFIED BY AMBASSADOR''',
     2001,
     [r'01STATE184178']),
    # 02VATICAN1975
    (u'''SUBJECT: ENGAGING CATHOLIC CHURCH IN VENEZUELA 
 
REF: STATE: 73097 
 
CLASSIFIED BY:''',
     2002,
     [r'02STATE73097']),
    # 01VATICAN5095
    (u'''SUBJECT: TFUS01: VATICAN POSITION ON RETALIATION AGAINST 
TERRORISTS 
 
REF: (99) ROME 2196 
 
                       CONFIDENTIAL 
 
PAGE 02        VATICA  05095  281347Z 
(U) CLASSIFIED BY DCM''',
     2001,
     [r'99ROME2196']),
    # 03OTTAWA700
    (u'''SUBJECT: G8 EXPERTS MEETING ON CRITICAL INFORMATION 
INFRASTRUCTURE PROTECTION: CANADIAN DELEGATION 
 
REF: REF: SECSTATE 58408 
 
 1. Following is th''',
     2003,
     [r'03STATE58408']),
    # 96ANKARA12278
    (u'''SUBJECT: GLIMPSES OF THE SHARIA IN TURKEY 
 
REF: A) ANKARA 11676;B) ANKARA 11279 
 
¶1.  CLASSIFIED BY ''',
     1996,
     [r'96ANKARA11676', r'96ANKARA11279']),
    # 03BRASILIA311
    (u'''REFS: 
 
¶A. RIO 0108 
¶B. 02 BRASILIA 3393 
¶C. 02 BRASILIA 1639 
D.01 BRASILIA 3714 
 
SENSITIVE BUT UNCLASSIFIED, PLEASE''',
     2003,
     [r'03RIODEJANEIRO108', r'02BRASILIA3393', r'02BRASILIA1639', r'01BRASILIA3714']),
    # 04PANAMA1963
    (u'''REF: Panama 01764 
 
 
C O R R E C T E D COPY OF PANAMA 1957 - TEXT
''',
     2004,
     [r'04PANAMA1764']),
    # 10CAIRO195
    (u'''SUBJECT: FOREIGN WORKER AND LABOR PROBLEMS IN QIZ FACTORY 
 
REF: 09CAIRO0561; 08CAIRO2528 
 
CLASSIFIED BY: ''',
     2010,
     [r'09CAIRO561', r'08CAIRO2528']),
    # 10OTTAWA79
    (u'''REF: 10-OTTAWA-57 ''',
     2010,
     [r'10OTTAWA57']),
    # 10RIYADH184
    (u'''REF: A. 09DHAHRAN 201 B. 09RIYADH 1302 C. 09RIYADH 1397 D. 09RIYADH 1492 E. 09RIYADH 1557 F. 09RIYADH 1642 G. RIYADH 103 H. SECSTATE 3080 I. SECSTATE 11182''',
     2010,
     [r'09DHAHRAN201', r'09RIYADH1302', r'09RIYADH1397', r'09RIYADH1492', r'09RIYADH1557', r'09RIYADH1642', r'10RIYADH103', r'10STATE3080', r'10STATE11182']),
    # 10PORTAUPRINCE112
    (u'''REF: PORT A 76; PORT A 100''',
     2010,
     [r'10PORTAUPRINCE76', r'10PORTAUPRINCE100']),
    # 09SOFIA508
    (u'''REF: A. REF A: 09 SOFIA 154
¶B. REF B: 05 SOFIA 1207
¶C. REF C: 05 SOFIA 1882
¶D. REF D: 08 SOFIA 192 ''',
     2009,
     [r'09SOFIA154', r'05SOFIA1207', r'05SOFIA1882', r'08SOFIA192']),
    # 09BUENOSAIRES66
    (u'''REF: A. '08 BUENOS AIRES 1491 
     ¶B. '08 BUENOS AIRES 1389 
     ¶C. '08 BUENOS AIRES 1398 ''',
     2009,
     [r'08BUENOSAIRES1491', r'08BUENOSAIRES1389', r'08BUENOSAIRES1398']),
    # 06BRASILIA578
    (u'''REFS: (1) 2005 RIO DE JANEIRO 1143, (2) 2005 BRASILIA 03242 ''',
     2006,
     [r'05RIODEJANEIRO1143', r'05BRASILIA3242']),
    # 06WELLINGTON538
    (u'''REF: A.) WELLINGTON 282 
     B.) WELLINGTON 283 
     C.) WELLINGTON 323 ''',
     2006,
     [r'06WELLINGTON282', r'06WELLINGTON283', r'06WELLINGTON323']),
    # 06PANAMA1518
    (u'''REF: A. PANAMA 651

     ¶B. PANAMA 1213
     ¶C. PANAMA 1293
     ¶D. 2005PANAMA2342''',
     2006,
     [r'06PANAMA651', r'06PANAMA1213', r'06PANAMA1293', r'05PANAMA2342']),
    # 06OTTAWA2420
    (u'''REF: A. OTTAWA 2258 
 
     ¶B. OTTAWA 1245 
     ¶C. 05 0TTAWA 3518 ''',
     2006,
     [r'06OTTAWA2258', r'06OTTAWA1245', r'05OTTAWA3518']),
    # 06CHENNAI1497
    (u'''REF: (A)05 CHENNAI 0121, (B)O4 CHENNAI 0944 ''',
     2006,
     [r'05CHENNAI121', r'04CHENNAI944']),
    # 04HANOI652
    (u'''SUBJECT:  INPUT FOR 2004 TIP REPORT - VIETNAM 
 
REFS:  A. STATE 7869 B. 03 HANOI 3232 C. 03 HANOI 3288 D. 03 
 
HANOI 2323 E. HANOI 336 F. HCMC 196 
 
¶1. Mission Viet ''',
     2004,
     [r'04STATE7869', r'03HANOI3232',
      r'03HANOI3288', r'03HANOI2323',
      r'04HANOI336', r'04HOCHIMINHCITY196']),
    # 08RIGA472
    (u'''E.O. 12958: DECL: 08/12/2018 
TAGS: PREL MOPS ENRG NATO EUN RS GG LG
SUBJECT: TFGG01: LATVIAN FM WANTS STRONG NATO AND EU 
STATEMENTS BUT NOT OPTIMISTIC 
 
REF: A) STATE 856708 B) STATE 86108 ...

C O N F I D E N T I A L RIGA 000472 SIPDIS E.O. 12958: DECL: 08/12/2018 TAGS: PREL MOPS ENRG NATO EUN RS GG LG
STATE 86108 Classified By:''',
     2008,
     [r'08STATE856708', r'08STATE86108']),
    # 09HANOI809
    (u'''SUBJECT: 2011 LEADERSHIP TRANSITION: LEADING CONTENDERS FOR GENERAL  SECRETARY AND PRIME MINISTER    

REF: HANOI 60 (FEW CHANGES AT THE 9TH PARTH PLENUM)  HANOI 330 (IDEOLOGY RESURGENT? THE GENERAL SECRETARY’S NEW CONCEPT  AND ITS IMPLICATIONS)  HANOI 413 (IN VIETNAM, CHINA AND BAUXITE DON’T MIX) HANOI 537 (BAUXITE CONTROVERSY SPURS LEADERSHIP DIVISIONS, VIBRANT NATIONAL ASSEMBLY DEBATE)  HANOI 672 (BEHIND VIETNAM’S LATEST CRACKDOWN)   

CLASSIFIED BY: Mi''',
     2009,
     [r'09HANOI60', r'09HANOI330', r'09HANOI413', r'09HANOI537', r'09HANOI672']),
    # 72TEHRAN1164
    (u'''REF: TEHRAN 1091: TEHRAN 263: MOSCOW 1603 ''',
     1972,
     [r'72TEHRAN1091', r'72TEHRAN263', r'72MOSCOW1603']),
    # 05OTTAWA2105
    (u'''Ref: [A] State 188314, 259032, [B] Ottawa 2285 ''',
     2005,
     [r'05STATE188314', r'05OTTAWA2285']),
    # 06SANTIAGO439
    (u'''REF: A. STATE 3836 
     ¶B. 05 SANTIAG0 465 
     ¶C. 05 SANTIAGO 466 
''',
     2006,
     [r'06STATE3836', r'05SANTIAGO465', r'05SANTIAGO466']),
    
)

def test_parse_references():
    def check(content, year, reference_id, expected):
        eq_(expected, parse_references(content, year, reference_id))
    for test in _TEST_DATA:
        reference_id = None
        if len(test) == 4:
           content, year, reference_id, expected = test
        else:
           content, year, expected = test
        yield check, content, year, reference_id, expected

_TRIPOLI_TESTS = {
'08TRIPOLI564': (
u"""
RESIGN SOON 
 
REF: TRIPOLI 227  TRIPOLI 00000564  001.2 OF 002   CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy - Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (S/NF)
""", 2008, [r'08TRIPOLI227']),
'08TRIPOLI494': (
"""
E.O. 12958: DECL:  6/18/2018 
TAGS: PGOV PREL PHUM PINR LY
SUBJECT: JOURNALIST JAILED FOR CRITICIZING GOVERNMENT'S 
POORLY-COORDINATED DEVELOPMENT PROJECTS  CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary:  A respected [...]"""
, 2008, []),
'08TRIPOLI574': (
u"""
SUBJECT: U.K. VISIT TO RABTA CHEMICAL WEAPONS PRODUCTION FACILITY 
 
REF: TRIPOLI 466  CLASSIFIED BY: John T. Godfrey, CDA, U.S. Embassy - Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary: T [...]
""", 2008, [r'08TRIPOLI466']),
'08TRIPOLI466': (
u"""
TAGS: PARM PREL CWC OPCW CBW CH JA IT LY
SUBJECT: CHEMICAL WEAPONS CONVENTION (CWC): CONVERSION OF THE RABTA CHEMICAL WEAPONS PRODUCTION FACILITY  REF: A) STATE 58476, B) THE HAGUE 482, C) TRIPOLI 119  CLASSIFIED BY: Chris Stevens, CDA, U.S. Embassy Tripoli, Dept of State. REASON: 1.4 (b), (d) 1. (C) Summary:  The"""
, 2008, [r'08STATE58476', r'08THEHAGUE482', r'08TRIPOLI119']),
}


def test_malformed_tripoli_cables():
    def check(content, year, reference_id, expected):
        eq_(expected, parse_references(content, year, reference_id))
    for ref_id, params in _TRIPOLI_TESTS.iteritems():
        content, year, result = params
        yield check, content, year, ref_id, result


if __name__ == '__main__':
    import nose
    nose.core.runmodule()