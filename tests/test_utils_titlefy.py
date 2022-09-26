# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2015 -- Lars Heuer <heuer[at]semagia.com>
# All rights reserved.
#
# License: BSD, see LICENSE.txt for more details.
#
"""\
Tests cablemap.core.utils.titlefy

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD license
"""
from nose.tools import eq_
from cablemap.core.utils import titlefy

_TEST_DATA = (
    ('MISSILE TECHNOLOGY CONTROL REGIME (MTCR): "BROKERING CONTROLS IN THE UNITED STATES ON DUAL-USE ITEMS"',
     u'Missile Technology Control Regime (MTCR): "Brokering Controls in the United States on Dual-Use Items"'),
    ('germany requests release of xxxxxxxxxxxx nonpaper to the german criminal customs office',
      u'Germany Requests Release of XXXXXXXXXXXX Nonpaper to the German Criminal Customs Office'),
    # 8TRIPOLI227
    ('BACK TO THE FUTURE? QADHAFI CALLS FOR DRAMATIC SOCIO-ECONOMIC CHANGE IN GPC SPEECH',
      u'Back to the Future? Qadhafi Calls for Dramatic Socio-Economic Change in GPC Speech'),
    ("WESTERWELLE'S SURGE CLINCHES BLACK-YELLOW IN GERMANY; MERKEL GAINS SECOND TERM",
      u"Westerwelle's Surge Clinches Black-Yellow in Germany; Merkel Gains Second Term"),
    ('COALITION TESTED AS US-EU TFTP/SWIFT AGREEMENT PASSES ON GERMAN ABSTENTION',
     u'Coalition Tested as US-EU TFTP/SWIFT Agreement Passes on German Abstention'),
    # 09BERLIN1393    
    ("GERMANY'S NEW INTERIOR MINISTER FACES STEEP LEARNING CURVE",
     u"Germany's New Interior Minister Faces Steep Learning Curve"),
    # 09BERLIN1360
    ("THE NEW GERMAN CABINET - AN OVERVIEW",
     u'The New German Cabinet - An Overview'),
    # 09BERLIN1162
    ("GERMANY'S NEXT FOREIGN MINISTER?: THE WORLD ACCORDING TO FDP CHAIRMAN GUIDO WESTERWELLE",
     u"Germany's Next Foreign Minister?: The World According to FDP Chairman Guido Westerwelle"),
    # 10MEXICO141
    (u'Mexico’s Latin American Unity Summit -- Back to the Future?',
     u'Mexico’s Latin American Unity Summit -- Back to the Future?'),
    # 09BAKU744
    ('"LORDS OF THE MOUNTAINS" WILL FIGHT NO MORE FOREVER',
     u'"Lords of the Mountains" Will Fight No More Forever'),
    # 06HAVANA8633
    ('''"IF YOU DON'T HAVE YOUR HEALTH..." (AILMENTS AMONG THE CASTRO CLAN)''',
     u'''"If You Don't Have Your Health..." (Ailments Among the Castro Clan)'''),
    # 08LONDON2899
    (u"COTE D'IVOIRE: UK ON ELECTIONS, DDR, AND RE-ENERGIZING THE PROCESS",
     u"Cote D'Ivoire: UK on Elections, DDR, and Re-Energizing the Process"),
    # 06PARIS5974
    (u'FRENCH ELECTION 2007: NICOLAS SARKOZY -- THE CANDIDATE WHO MIGHT CHANGE FRANCE',
     u'French Election 2007: Nicolas Sarkozy -- The Candidate Who Might Change France'),
    # 08LONDON2542
    (u'PM BROWN DOES THE UNEXPECTED IN ADDRESSING ECONOMIC PROBLEMS',
     u'PM Brown Does the Unexpected in Addressing Economic Problems'),
    # 06BERLIN2546
    ("SPD IN DRIVER'S SEAT FOR BERLIN ELECTION",
     u"SPD in Driver's Seat for Berlin Election"),
    # 07TRIPOLI949
    ('''SLOW PROGRESS ON ITALY-LIBYA COLONIAL COMPENSATION TREATY A SIGN OF GOL'S "CORSAIR MENTALITY"''',
     u'''Slow Progress on Italy-Libya Colonial Compensation Treaty a Sign of GOL's "Corsair Mentality"'''),
    # 09TRIPOLI363
    ('SLA/U CAN NEGOTIATE ONLY WITH ASSURANCES THAT JEM AND KHARTOUM WILL ALSO LAY DOWN ARMS',
     u'SLA/U Can Negotiate Only With Assurances That JEM and Khartoum Will Also Lay Down Arms'),
    # 09LONDON2569
    ('HMG STRESSES U.S.-UK COORDINATION ON AFGHANISTAN STRATEGY',
     u'HMG Stresses U.S.-UK Coordination on Afghanistan Strategy'),
    # 10LONDON76
    ("AFGHANISTAN/YEMEN/IRAN: SENIOR UK-BASED DIPLOMATS DISCUSS AT CHINESE AMB'S FAREWELL DINNER",
     u"Afghanistan/Yemen/Iran: Senior UK-Based Diplomats Discuss at Chinese Amb's Farewell Dinner"),
    # 09LONDON2237
    ("Economists Warn UK's Economic Recovery Is Fragile",
     u"Economists Warn UK's Economic Recovery Is Fragile"),
    # 01VATICAN1261
    ('DROC--VATICAN DEMARCHE',
     u'DROC--Vatican Demarche'),
    # 01STATE176819
    ("AFGHANISTAN'S POLITICAL FUTURE (CORRECTED COPY)",
     u"Afghanistan's Political Future (Corrected Copy)"),
    # 04TASHKENT3180
    ('FIRST DAUGHTER LOLA (KARIMOVA) CUTS LOSE',
     u'First Daughter Lola (Karimova) Cuts Lose'),
    # 07TUNIS1489
    ("THE PNG'ING OF SUHA ARAFAT: MANY RUMORS, FEW FACTS",
     u"The PNG'ing of Suha Arafat: Many Rumors, Few Facts"),
    # 08LONDON1761
    ('CWS/BWC: CLOSE ALLIES MEETING, JUNE 17-18, 2008',
      u'CWS/BWC: Close Allies Meeting, June 17-18, 2008'),
    # 08LONDON2822
    ('DRC: UK FOCUSING ON POLITICAL SOLUTION, MAKING MONUC MORE RESPONSIVE AND FLEXIBLE',
     u'DRC: UK Focusing on Political Solution, Making MONUC More Responsive and Flexible'),
    # 10SANSALVADOR85
    ('Scenesetter for DoD Visit to El Salvador, March 8-9',
     u'Scenesetter for DoD Visit to El Salvador, March 8-9'),
    # 06BRASILIA694
    ("VARIG'S DOWNWARD SPIRAL: WE'LL PAY YOU LATER",
     u"VARIG's Downward Spiral: We'll Pay You Later"),
    # 05SANAA923
    ("SALEH ON KANAAN: WE'VE GOT HIM!!",
     u"Saleh on Kanaan: We've Got Him!!"),
    # 09SEOUL59
    (u"ROK’S FOREIGN POLICY TOWARD THE NEIGHBORS: NORTH KOREA, JAPAN, CHINA AND RUSSIA",
     u"ROK’s Foreign Policy Toward the Neighbors: North Korea, Japan, China and Russia"),
    # 10MEXICO690
    (u'Scenesetter for Ex-IM Chairman Fred Hochberg',
     u'Scenesetter for Ex-IM Chairman Fred Hochberg'),
    # 09SAOPAULO558
    (u'WHAT HAPPENED TO THE PCC?',
     u'What Happened to the PCC?'),
    # 08BRASILIA1252
    (u'63RD UN GENERAL ASSEMBLY: BRAZILIAN PRIORITIES',
     u'63rd UN General Assembly: Brazilian Priorities'),
    # 08PARIS1561
    (u'WORKING WITH FRANCE TO ADVANCE A SOLUTION TO THE CONFLICT IN GEORGIA (UNSCR AND GAERC)',
     u'Working With France to Advance a Solution to the Conflict in Georgia (UNSCR and GAERC)'),
    # 05PANAMA1205
    (u'PANAMA AND CUBA: NSC-DIRECTED REVIEW REGARDING SUSPENSION OF TITLE III OF THE LIBERTAD ACT ',
     u'Panama and Cuba: NSC-Directed Review Regarding Suspension of Title III of the Libertad Act'),
)

def test_titlefy():
    def check(content, expected):
        eq_(expected, titlefy(content))
    for content, expected in _TEST_DATA:
        yield check, content, expected


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
