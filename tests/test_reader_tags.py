# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests TAGs parsing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core import cable_by_id
from cablemap.core.reader import parse_tags

_TEST_DATA = (
    ('TAGS: something', [u'SOMETHING']),
    ('TAGS: something\n', [u'SOMETHING']),
    ('TAGS: something\nhere', [u'SOMETHING']),
    ('TAGS: something, \nhere', [u'SOMETHING', u'HERE']),
    (u'TAGS: something,\nhere', [u'SOMETHING', u'HERE']),
    (u'TAGS something', [u'SOMETHING']),
    (u'TAGS something\n', [u'SOMETHING']),
    (u'TAGS something\nhere', [u'SOMETHING']),
    (u'TAGS something, \nhere', [u'SOMETHING', u'HERE']),
    (u'tAgs something', [u'SOMETHING']),
    ('tAgs something\n', [u'SOMETHING']),
    (u'tAgs something\nhere', [u'SOMETHING']),
    (u'tAgs something, \nhere', [u'SOMETHING', u'HERE']),
    (u'tAgs something,\nhere', [u'SOMETHING', u'HERE']),
    (u'tAgs: something', [u'SOMETHING']),
    (u'tAgs: something\n', [u'SOMETHING']),
    (u'tAgs: something\nhere', [u'SOMETHING']),
    (u'tAgs: something, \nhere', [u'SOMETHING', u'HERE']),
    (u'tAgs: something,\nhere', [u'SOMETHING', u'HERE']),
    (u'TAGS: PREL ECON EFIN ELAB PGOV FR',
     [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']),
    (u'TAGS PREL ECON EFIN ELAB PGOV FR',
     [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']),
    (u'tags PREL ECON EFIN ELAB PGOV FR',
     [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']),
    (u'tags: PREL ECON EFIN ELAB PGOV FR',
     [u'PREL', u'ECON', u'EFIN', u'ELAB', u'PGOV', u'FR']),
    (u'TAGS ECON, PGOV, EFIN, MOPS, PINR, UK',
     [u'ECON', u'PGOV', u'EFIN', u'MOPS', u'PINR', u'UK']),
    (u'TAG PTER, PGOV, ASEC, EFIN, ENRG, KCIP',
     [u'PTER', u'PGOV', u'ASEC', u'EFIN', u'ENRG', u'KCIP']),
    (u'E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu \nSubject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?\n\n(U) Classifi',
     [u'PREL', u'PGOV', u'PINS', u'TU']),
    (u"E.o. 12958: decl: after korean unification\nTags: ovip (steinberg, james b.), prel, parm, pgov, econ,\netra, mnuc, marr, ch, jp, kn, ks, ir\nSubject: deputy secretary steinberg's meeting with xxxxx\nforeign minister he yafei, september 29, 2009",
     [u'OVIP', u'STEINBERG, JAMES B.', u'PREL', u'PARM', u'PGOV', u'ECON', u'ETRA', u'MNUC', u'MARR', u'CH', u'JP', u'KN', u'KS', u'IR']),
    ('TAGS: ECON EINV ENRG PGOV PBTS MARR BR\n\nSUBJECT: AMBASSADOR SOBEL MEETS WITH KEY ENERGY ENTITIES IN RIO Ref(s): A) 08 RIO DE JAN 138; B) 08 RIO DE JAN 0044 and previous Sensitive But Unclassified - Please handle accordingly. This message has been approved by Ambassador Sobel. ',
     [u'ECON', u'EINV', u'ENRG', u'PGOV', u'PBTS', u'MARR', u'BR']),
    #02ROME1196
    ('\nEO 12958 DECL: 03/05/2007\nTAGS PHUM, OPRC, OPRC, OPRC, OPRC, IT, ITPHUM, ITPHUM, ITPHUM, HUMAN RIGHTS\nSUBJECT: AS PREDICTED, ITALY’S HUMAN RIGHTS REPORT\nGENERATES FODDER FOR DOMESTIC POLITICAL MILLS', 
     [u'PHUM', u'OPRC', u'IT', u'HUMAN RIGHTS']),
    # 09STATE11937
    ('E.O. 12958: DECL: 02/05/2019\nTAGS: OVIP CLINTON HILLARY PREL KPAL FR IR RS\nNATO, UK, CN\nSUBJECT: (U) Secreta',
    [u'OVIP', u'CLINTON, HILLARY', u'PREL', u'KPAL', u'FR', u'IR', u'RS', u'NATO', u'UK', u'CN']),
    #09BEIJING2964
    ('TAGS: OVIP STEINBERG JAMES PREL MNUC SN CH KN',
     [u'OVIP', u'STEINBERG, JAMES B.', u'PREL', u'MNUC', u'SN', u'CH', u'KN']),
    # 09SANTIAGO331
    ("E.O. 12958: DECL: 04/07/2019\nTAGS: OVIP BIDEN JOSEPH PREL ECON PGOV SOCI EU\nSUBJECT: VICE PRESIDENT BIDEN'S MARCH 28 MEETING WITH PRIME",
     [u'OVIP', u'BIDEN, JOSEPH', u'PREL', u'ECON', u'PGOV', u'SOCI', u'EU']),
    #08STATE100219
    ('E.O. 12958: DECL: 09/17/2018\nTAGS: OVIP RICE CONDOLEEZZA PREL PHSA SP KV CU\nBL, IS\nSUBJECT: Secretary Rice',
     [u'OVIP', u'RICE, CONDOLEEZZA', u'PREL', u'PHSA', u'SP', u'KV', u'CU', u'BL', u'IS']),
    # 04SANAA2346
    ('TAGS: MASS MOPS OVIP PARM PINR PREL PTER YM COUNTER TERRORISM',
     [u'MASS', u'MOPS', u'OVIP', u'PARM', u'PINR', u'PREL', u'PTER', u'YM', u'COUNTERTERRORISM']),
    # 05TELAVIV1580
    ('TAGS PGOV, PREL, KWBG, IR, IS, COUNTERTERRORISM, GOI EXTERNAL ',
     [u'PGOV', u'PREL', u'KWBG', u'IR', u'IS', u'COUNTERTERRORISM', u'GOI EXTERNAL']),
    ('TAGS PTER MARR, MOPPS',
     [u'PTER', u'MARR', u'MOPS']),
    ('TAGS: IS ISRAELI PALESTINIAN AFFAIRS GOI EXTERNAL',
     [u'IS', u'ISRAELI PALESTINIAN AFFAIRS', u'GOI EXTERNAL']),
    ('TAGS: IS GAZA DISENGAGEMENT ISRAELI PALESTINIAN AFFAIRS',
     [u'IS', u'GAZA DISENGAGEMENT', u'ISRAELI PALESTINIAN AFFAIRS']),
    # 05BRASILIA2675
    ('TAGS: PREL PGOV BR OVIP ZOELLICK ROBERT US',
     [u'PREL', u'PGOV', u'BR', u'OVIP', u'ZOELLICK, ROBERT', u'US']),
    # 07BUENOSAIRES1673
    ('DECL: 08/22/2017 AGS: PGOV, PREL, ECON, SOCI, AR',
     [u'PGOV', u'PREL', u'ECON', u'SOCI', u'AR']),
    # 04ANKARA348
    ('''E.o. 12958: decl: 01/07/2014 Tags: prel, pgov, pins, tu Subject: turkish p.m. Erdogan goes to washington: how strong a leader in the face of strong challenges?
''',
     [u'PREL', u'PGOV', u'PINS', u'TU']),
    # 08MANAMA492
    ('''SIPDIS 
 
STATE FOR G/TIP 
BAGHDAD FOR AMBASSADOR ERELI 
 
E.O. 12958: DECL: 07/24/2018 
TAGS: KCRM KWMN ASEC PHUM BA
SUBJECT: BAHRAIN SEEKS IOM'S ASSISTANCE TO COMBAT TIP 
 
REF: A. MANAMA''',
     [u'KCRM', u'KWMN', u'ASEC', u'PHUM', u'BA']),
    # 08ECTION01OF02MANAMA492 which is the malformed version of 08MANAMA492
    ('''
E.O. 1295: DECL: 07/24/2018 
TAGS: KCRM KWMN ASEC PHUMBA
SUBJECT: BAHRAIN SEEKS IOM'S ASSISTANCE TO COBAT TIP
''',
     [u'KCRM', u'KWMN', u'ASEC', u'PHUM', u'BA']),
    #
    ('''SIPDIS 
 
DEPT NEA/MAG (JOHNSON), INR (HOFSTATTER) 
 
E.O. 12958: DECL:  1/20/2019 
TAGS: PGOV PREL ECON EFIN SCUL EPET PHUM KDEM LY
SUBJECT: LIBYA POSTPONES GENERAL PEOPLE'S CONGRESS, WALKS BACK FROM WEALTH DISTRIBUTION AND PRIVATIZATION PLANS  
''',
    [u'PGOV', u'PREL', u'ECON', u'EFIN', u'SCUL', u'EPET', u'PHUM', u'KDEM', u'LY']),
    # 09CAIRO2205
    ('''POSTS FOR FRAUD PREVENTION UNITS E.O. 12958: N/A TAGS: KFRDKIRFCVISCMGTKOCIASECPHUMSMIGEG

SUBJECT: BLIND COPTIC GIRLS' CHOIR USED FOR ALIEN SMUGGLING REF: CAIRO 2178

1.(SBU) Summary:''',
     [u'KFRD', u'KIRF', u'CVIS', u'CMGT', u'KOCI', u'ASEC', u'PHUM', u'SMIG', u'EG']),
    # 05SANJOSE2199
    ('''E.O. 12958: N/A 
TAGS: PREL SCUL ETRD CS UNDESCO
SUBJECT: COSTA RICA: UNESCO DEMARCHE DELIVERED ''',
     [u'PREL', u'SCUL', u'ETRD', u'CS', u'UNESCO']),
    # 04PANAMA586
    ('''E.O. 12958: DECL: 03/10/2009 
TAGS: MARR PREL PINS EWWT MOPS PM LABOR HUMAN RIGHTSPOLMIL
SUBJECT: PANAMA OFFERS BETTER HIGH-VALUE TRANSIT GUARANTEE 
 
REF: A. 03 PANAMA 2201 
     ¶B. 03 PANAMA 470 ''',
     [u'MARR', u'PREL', u'PINS', u'EWWT', u'MOPS', u'PM', u'LABOR', u'HUMAN RIGHTS', u'POL', u'MIL']),
    # 06SANJOSE2802
    ('''E.O. 12958: N/A 
TAGS: ETRDEINVECINPGOVCS
SUBJECT: COSTA RICA'S INSURANCE MONOPOLY PREPARES FOR COMPETITION 
 
¶1. SUMMARY.''',
     [u'ETRD', u'EINV', u'ECIN', u'PGOV', u'CS']),
    # 09BRASILIA542
    ('''SIPDIS 
 
E.O. 12958: N/A 
TAGS: KFLU AEMR ASEC AMEDCASCKFLO TBIO KSAF KPAO PREL
PINR, AMGT, TF, BR 
SUBJECT: TFFLU01: H1N1 INFLUENZA OUTBREAK AND BRAZIL:  SITREP # 5''',
     [u'KFLU', u'AEMR', u'ASEC', u'AMED', u'CASC', u'KFLO', u'TBIO', u'KSAF', u'KPAO', u'PREL', u'PINR', u'AMGT', u'TF', u'BR']),
    # 02VATICAN5607
    ('''E.O. 12958: DECL: 11/19/2012 
TAGS: PREL PGOV PHUM VT PGOV PHUM VT VE VEPREL
SUBJECT: HOLY SEE URGES CHURCH TO PROMOTE VENEZUELAN 
DIALOGUE, AVOID POLITICAL ACTIVISM 
 
REF: A. A) CARACAS 328''',
     [u'PREL', u'PGOV', u'PHUM', u'VT', u'VE']),
    # 01VATICAN3507
    ('''EO 12958 DECL: 07/02/11 
TAGS PREL, PHUM, IS, EG, CH, ID, PHUM, IS, EG, CH, ID, PHUM, IS, EG, CH, ID, PHUM, IS, EG, CH, ID, VT, VTPREL, VTPREL, VTPREL 
SUBJECT:  THE VATIC''',
     [u'PREL', u'PHUM', u'IS', u'EG', u'CH', u'ID', u'VT']),
    # 04PANAMA2524
    ('''E.O. 12958: DECL: 10/05/2014 
TAGS: ECON ETRD EFIN PTER SNAR PM ECONOMIC AFFAIRS
SUBJECT: UNDERSTANDING PANAMA'S COLON FREE ZONE ''',
     [u'ECON', u'ETRD', u'EFIN', u'PTER', u'SNAR', u'PM', u'ECONOMIC AFFAIRS']),
    # 07SAOPAULO212
    ('''E.O. 12958: N/A 
TAGS: OVIP BUSH GEORGE PREL PGOV SOCI EPET KTIA BR
SUBJECT: VISIT OF PRESIDENT GEORGE W. BUSH TO SAO PAULO, BRAZIL ''',
     [u'OVIP', u'BUSH, GEORGE W.', u'PREL', u'PGOV', u'SOCI', u'EPET', u'KTIA', u'BR']),
    # 04PANAMA672
    ('''E.O. 12958:  N/A 
TAGS: CASC CJAN SNAR PHUM CU PM NOVO GUILLERMO REMON PEDRO JIMENEZ GASPAR CONSULAR AFFAIRS
SUBJECT:  FATE OF ANTI-CASTRO CUBAN AMERICANS IN THE HANDS 
OF JUDGE ''',
     [u'CASC', u'CJAN', u'SNAR', u'PHUM', u'CU', u'PM', u'NOVO, GUILLERMO', u'REMON, PEDRO', u'JIMENEZ, GASPAR', u'CONSULAR AFFAIRS']),
    # 04ROME3708
    ('''E.O. 12958: DECL: 06/01/2034 
TAGS: MARR PREL ETTC EIND IT GLOBAL DEFENSE
SUBJECT: (C)''',
     [u'MARR', u'PREL', u'ETTC', u'EIND', u'IT', u'GLOBAL DEFENSE']),
    # 06TELAVIV2787
    ('''E.O. 12958: DECL: 07/14/2016
TAGS: ECON ETRD PREL PGOV PTER KWBG JO IS ECONOMY AND FINANCE
SUBJECT: HERZOG LAMENTS TIMING OF SECURITY CRISES ON
TOURISM INDUSTRY''',
     [u'ECON', u'ETRD', u'PREL', u'PGOV', u'PTER', u'KWBG', u'JO', u'IS', u'ECONOMY AND FINANCE']),
    # 03ROME2045
    ('''E.O. 12958: DECL: 05/12/2013 
TAGS: PREL MARR MOPS IT MARR MOPS IT MARR MOPS IT MARR MOPS IT MARR MOPS IT MARR MOPS IT IZ IZPREL IZPREL IZPREL IZPREL IZPREL IRAQI FREEDOM



SUBJECT: RE''',
     [u'PREL', u'MARR', u'MOPS', u'IT', u'IZ', u'IRAQI FREEDOM']),
    # 05ROME3585
    ('''TAGS: PREL PGOV CVIS IT ITALY NATIONAL ELECTIONS ITALIAN POLITICS IRAQI FREEDOM
SUBJECT:''',
     [u'PREL', u'PGOV', u'CVIS', u'IT', u'ITALY NATIONAL ELECTIONS', u'ITALIAN POLITICS', u'IRAQI FREEDOM']),
    # No cable, just a collection of TAGs
    ('''TAGS: DOMESTIC POLITICS MASSMNUC KNNPMNUC MEETINGS WITH AMBASSADOR NEW ZEALAND ROOD JOHN CROS GERARD ZANU-PF COUNTRY CLEARANCE''',
     [u'DOMESTIC POLITICS', u'MASS', 'MNUC', u'KNNP', u'MEETINGS WITH AMBASSADOR', u'NEW ZEALAND', u'ROOD, JOHN', u'CROS, GERARD', u'ZANU-PF', u'COUNTRY CLEARANCE']),
    # 09LONDON2499
    ('''E.O. 12958: DECL: 09/22/2019 
TAGS: PREL PGOV KPAL ETRD KNNP PARM SENV MARR MNUC
ECON, PHUM, RS, IS, IR, GG, AF, UK SUBJECT: MILIBAND'S RUSSIA TRIP AIMS TO MOVE BILATERAL RELATIONSHIP FORWARD  REF: LONDON DAILY 11/3/09  Classified By: Deputy Chief of Mission Richard LeBaron, reasons 1.4 (b,d).  ''',
     [u'PREL', u'PGOV', u'KPAL', u'ETRD', u'KNNP', u'PARM', u'SENV', u'MARR', u'MNUC', u'ECON', u'PHUM', u'RS', u'IS', u'IR', u'GG', u'AF', u'UK']),
    # 05OTTAWA3726
    ('''E.O. 12958: N/A 
TAGS: ECON ETRD PGOV CA MX SIPDIS
SUBJECT: TRILATERAL REGULATORY COOPERATION MEETING UNDER 
SPP: INFORMATION SHARING ''',
     [u'ECON', u'ETRD', u'PGOV', u'CA', u'MX']),
    # 07KUWAIT624
    ('''E.O. 12958: N/A 
TAGS: OREP AMGT ASEC AFIN GM IZ IC KU COUNTRY
CLEARANCE 
SUBJECT: KUWAIT GRANTS COUNTRY CLEARANCE FOR CODEL BOND 
(MAY 3-7) ''',
     [u'OREP', u'AMGT', u'ASEC', u'AFIN', u'GM', u'IZ', u'IC', u'KU', u'COUNTRY CLEARANCE']),
    # 05PANAMA1818
    (u'''TAGS: PGOV PREL PM POL FOREIGN POL''',
     [u'PGOV', u'PREL', u'PM', u'POL', u'FOREIGN POL']),
    # 05PANAMA388
    (u'''TAGS: PGOV PREL PM POLITICS FOREIGN POLICY POL FOREIGN POL''',
     [u'PGOV', u'PREL', u'PM', u'POLITICS FOREIGN POLICY', u'POL', u'FOREIGN POL']),
    # 06TELAVIV344
    (u'''TAGS: IS KMDR MEDIA REACTION REPORT''',
     [u'IS', u'KMDR', u'MEDIA REACTION REPORT']),
    # 05ISTANBUL329
    (u'''TAGS: TU BO MD PHUM KCRM PGOV KJUS TIP IN TURKEY''',
     [u'TU', u'BO', u'MD', u'PHUM', u'KCRM', u'PGOV', u'KJUS', u'TIP IN TURKEY']),
    #
    (u'''E.O. 12958: N/A
TAGS: ECON EFIN ELAB ETRD KIPR PTER SOCI TBIO SP
EINV
SUBJECT: MADRID WEEKLY ECON/AG/COMMERCIAL UPDATE - NOVEMBER
12-16

''',
     [u'ECON', u'EFIN', u'ELAB', u'ETRD', u'KIPR', u'PTER', u'SOCI', u'TBIO', u'SP', u'EINV']),
    # 07VATICAN118
    (u'''E.O. 12958: N/A 
TAGS: PREL VT

(SBU) Charge d'affaires spoke to Monsignor Marcel Smejkal, the 
Holy See's directo...


SUBJECT: HOLY SEE:  INQUIRIES PENDING ON RADIO MARYJA ''',
     [u'PREL', u'VT']),
    # 92IZMIR819
    ('''E.O. 12356: DECL:  OADR 
TAGS;  PGOV, TU 
SUBJ: TERRORIST KILL FOUR POLICEMEN IN ANTALYA ''',
     [u'PGOV', u'TU']),
    # 10TELAVIV386
    ('''E.O. 12958: N/A 
TAS: ECON, ETRD, IS, JO 
SUBJECT: JORDAN/ISRAEL/QIZ QUARTE''',
     [u'ECON', u'ETRD', u'IS', u'JO']),
    # 04ABUDHABI1445
    ('''STATE FOR NEA/LMALENAS AND NP/ECC/KCROUCH 
USDOC FOR BIS/OUS/RCUPITT 
 
TAGS: ETTC PARM PREL PTER KSTC TC
E.O. 12958:N/A 
SUBJECT: EXBS NATIONAL CONTROL LIST WORKSHOP, APRIL 24- 
26, 2004, WELL RECEIVED IN THE UAE ''',
     [u'ETTC', u'PARM', u'PREL', u'PTER', u'KSTC', u'TC']),
    # 08PARAMARIBO219
    (u'''E.O. 12958: N/A 
TABS: EFIS, ECON, EPET, VE, NS 
 
SUBJECT:  DEPARTMENT OF FISHERIES TO SEEK FUEL SUBSIDY FOR FISHING 
FLEETS ''',
     [u'EFIS', u'ECON', u'EPET', u'VE', u'NS']),
    # 08ATHENS1536
    (u'''E.O.1295: NA 
TGS: GOV, PREL, GR 
SUBJECT: RLINGMAJOITY ACK TO ONE-VOTE MARGIN ''',
     [u'GOV', u'PREL', u'GR']),
    # 09LIMA54
    (u'''E.O. 12958: N/A 
TAGS, ASEC, APER, AMGT, PE 
SUBJECT: CORRECTED: ANNUAL OVERSEAS SECURITY ADVISORY COUNCIL (OSAC) 
CRIME AND SAFETY REPORT. ''',
     [u'ASEC', u'APER', u'AMGT', u'PE']),
    # 09AMMAN1518
    (u''' 
E.O. 12958: N/A 
TAGES:  OIIP, KPAO, PREL, JO 
SUBJECT:  JORDAN:  SPECIAL BBG TRAINING FOCUSES ON BROADCASTING 
SKILLS AT JRTV ''',
     [u'OIIP', u'KPAO', u'PREL', u'JO']),
    # 03VATICAN283
    (u'''E.O. 12958: N/A 
TAGS: PREL, PHUM, PREF, PGOV, EAGR, EAID, ECON, SMIG, TBIO, PHUM, PREF, PGOV, EAGR, EAID, ECON, SMIG, TBIO, PHUM, PREF, PGOV, EAGR, EAID, ECON, SMIG, TBIO, PHUM, PREF, PGOV, EAGR, EAID, ECON, SMIG, TBIO, UNCLASSIFIED    PAGE 02        VATICA  00283  01 OF 05  241033Z VTPREL, UNCLASSIFIED    PAGE 02        VATICA  00283  02 OF 05  241034Z VTPREL, UNCLASSIFIED    PAGE 02        VATICA  00283  04 OF 05  241035Z VTPREL, UNCLASSIFIED    PAGE 02        VATICA  00283  05 OF 05  241035Z VT 
SUBJECT: PARTNERS FOR PROGRESS - WORKING WITH VATICAN 
DEVELOPMENT AGENCIES 
 
REF: 02 VATICAN 4217 ''',
     [u'PREL', u'PHUM', u'PREF', u'PGOV', u'EAGR', u'EAID', u'ECON', u'SMIG', u'TBIO']),
    # 02ROME3067
    (u'''E.O. 12958: DECL: X1, X5 
TAGS: PREL, ETRD, ETTC, PARM, IT                          SECRET       PAGE 02        ROME  03067  211833Z 
SUBJECT: ITALY ON LIBYA: RABTA GATHERS STEAM ''',
     [u'PREL', u'ETRD', u'ETTC', u'PARM', u'IT']),
    # 00LIMA2475
    (u'''E.O. 12958: DECL: 4/24/05 
TAGS: PINR, PGOV, PREL, PGOV, PREL, PGOV, PREL, PE                          SECRET       PAGE 02        LIMA  02475  01 OF 03  251228Z PINR, PE                          SECRET       PAGE 02        LIMA  02475  02 OF 03  251229Z PINR, PE                          SECRET       PAGE 02        LIMA  02475  03 OF 03  251229Z 
SUBJECT:  ALEJANDRO TOLEDO BIOGRAPHY:  POLITICAL ASSETS AND 
LIABILITIES 
 
REFS:  (A) LIMA 1638 ''',
     [u'PINR', u'PGOV', u'PREL', u'PE']),
    # 02ROME1059
    (u'''E.O. 12958: N/A 
TAGS: ECON, EFIN, EFIN, EFIN, EFIN, IT                       UNCLASSIFIED    PAGE 02        ROME  01059  01 OF 04  281501Z ECON, IT                       UNCLASSIFIED    PAGE 02        ROME  01059  02 OF 04  281502Z ECON, IT                       UNCLASSIFIED    PAGE 02        ROME  01059  03 OF 04  281502Z ECON, IT                       UNCLASSIFIED    PAGE 02        ROME  01059  04 OF 04  281503Z 
SUBJECT:  THE EURO CHANGEOVER IN ITALY 
 
REF: (A) 2002 MILAN 14''',
     [u'ECON', u'EFIN', u'IT']),
    # 05MANAMA429
    (u'TAGS: EAID, ECON, EINV, PREL, BA, TAGS: EFIN ',
     [u'EAID', u'ECON', u'EINV', u'PREL', u'BA', u'TAGS', u'EFIN']),
    # 08USUNNEWYORK1092
    (u'''E.O. 12958: N/A
TAGS: PREL, UNGA/C-6
SUBJECT: UNGA/C-6: UNGA,S SIXTH (LEGAL) COMMITTEE DISCUSSES
THE NATIONALITY OF PERSONS
 ''',
    [u'PREL', u'UNGA/C-6']),
   
)


def test_tags():
    def check(content, expected):
        eq_(expected, parse_tags(content))
    for content, expected in _TEST_DATA:
        yield check, content, expected

_TEST_DATA_NO_C14N = (
    ('''TAGS: AMEDCASCKFLO TBIO KSAF KPAO PREL PINR, AMGT, TF, BR 
SUBJECT: XXXX''',
     [u'AMEDCASCKFLO', u'TBIO', u'KSAF', u'KPAO', u'PREL', u'PINR', u'AMGT', u'TF', u'BR']),
)


def test_c14n_disabled():
    def check(content, expected):
        eq_(expected, parse_tags(content, canonicalize=False))
    for content, expected in _TEST_DATA_NO_C14N:
        yield check, content, expected



_TEST_DATA_BY_ID = (
    (u'08BEIJING3662', [u'EFIN', u'ECON', u'EINV', u'PGOV', u'CH']),
    (u'08BRASILIA703', [u'EAID', u'ECON', u'EFIN', u'EINV', u'PGOV', u'PREL', u'BR', u'IZ']),
    (u'07MOSCOW5208', [u'PREL', u'PGOV', u'MARR']),
    (u'08TELAVIV1693', [u'OVIP', u'ROOD, JOHN', u'PREL', u'PTER', u'KNNP', u'MNUC', u'MCAP', u'KN', u'EG', u'UN', u'IS']),
    (u'07KABUL173', [u'PGOV', u'PREL', u'KJUS', u'PTER', u'KCRM', u'AF']),
    (u'06BRASILIA1193', [u'ETRD', u'ECON', u'KIPR', u'EINV', u'EPET', u'KTFN', u'BEXP', u'BR']),
    (u'09ANKARA1783', [u'PTER', u'PREL', u'KCIP', u'OSCE', u'TU']),
    (u'10PARIS159', [u'PREF', u'EAID', u'PHUM', u'CVIS', u'UN', u'FR', u'HA']),
)


def test_by_id():
    def check(cable, expected):
        eq_(expected, cable.tags)
    for ref_id, expected in _TEST_DATA_BY_ID:
        yield check, cable_by_id(ref_id), expected



if __name__ == '__main__':
    import nose
    nose.core.runmodule()
