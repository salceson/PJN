# coding: utf-8
import re

__author__ = "Michał Ciołczyk"

_SUBSTITUTIONS = [
    ('&', ' AND '),
    ("INTL", 'INTERNATIONAL'),
    ("INTN'L", "INTERNATIONAL")
]

_PREFIXES = [
    'SAME AS CONSIGNEE',
    'AGENCJA CELNA',
    'AGENCJA TRANSPORTOWA',
    'OOO',
    'BY ORDER OF',
    'BY ORDER TO',
    'BY ORDER',
    'FHU',
    'F H U',
    'LLC',
    'OY',
    'PPHU',
    'P P H U',
    'ZAO',
    'TC',
    'TO THE ORDER OF',
    'TO THE ORDER BY',
    'TO THE ORDER',
    'TO ORDER OF',
    'TO ORDER BY',
    'TO ORDER',
    'AS AGENT OF ',
    'BRANCH OF'
]

_SUFFIXES = [
    ' CO',
    'GROUP CORP',
    'HONG KONG',
    'HONGKONG',
    'POLSKA',
    ' OY',
    'POLAND',
    'CHINA',
    'A S',
    'S A',
    'SP J',
    'SHANGHAI',
    'DEUTSCHLAND',
    'BANGLADESH',
    'BV',
    'COMPANY',
    ' H K',
    'MOSCOW',
    'S C',
    'KOREA',
    'LLC',
    'GDYNIA',
    'IMP AND EXP',
    'IMPORT EXPORT',
    'IMPORT AND EXPORT',
    'IMP EXP',
    'INTERNATIONAL',
    'INTL',
    'SHENZHEN',
    'CAMBODIA',
    'RUS',
    'RUSSIA',
    'FINLAND',
    'PRC',
    'JAPAN'
]

_SPLITTERS = (
    ',',
    'SP Z O O',
    'SP ZOO',
    'SP Z OO',
    'SP ZO O',
    'S Z O O',
    'SPOLKA ZOO',
    'LIMITED',
    'LTD',
    ' LLC ',
    'P O BOX',
    'PO BOX',
    ' SA ',
    ' AB ',
    'PVT',
    ' PRIVATE ',
    ' CO ',
    ' S A ',
    ' A S ',
    ' AS ',
    ' ZAO ',
    ' UL ',
    ' INTL ',
    ' SP J ',
    ' OY ',
    'GMBH',
    'SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA',
    ' SP K ',
    'OOO',
    '"',
    'SPOLKA AKCYJNA',
    ' TEL ',
    ' FAX ',
    ' B V ',
    'S KA Z O O',
    'SDN BDH',
    'SPOLKA JAWNA',
    'S P A',
    'SPOLKA Z O O',
    'SDN BHD',
    ' C O ',
    'HQ ',
    ' INC ',
    ' ZIP ',
    'OYKATRIINANTIE',
    'SPZ O O',
    ' AG ',
    ' SP K ',
    ' SP KOM ',
    'SPOLKA KOMANDYTOWA',
    ' SP K ',
    ' SP Z O ',
    'S P Z O O',
    'BRANCH OF',
    'BRANCHOF',
    ' AND ',
    'SP KOMANDYTOWA',
    'POLSKA',
    'S R O',
    'STREET',
    ' STR ',
    'OYKOIVUHAANTIE',
)

_SUBSTRINGS = (
    'LOGISTICS',
    'LOGISTIC',
    'INTERNATIONAL TRADING',
    'INTERNATIONAL TRADE',
    'SERVICE CONTRACT',
    'CITY',
    'OFFICE',
    'INDUSTRIAL',
    'MANUFACTURING',
    'INTERNATIONAL',
    'SHIPPING',
    'FORWARDING',
    'SERVICE',
    'TRADE',
    'IMP EXP',
    'IMPORT EXPORT',
    'IMP AND EXP',
    'IMPORT AND EXPORT',
    'TRADING',
    'INDUSTRY',
    ' AND ',
    'GLOBAL',
    'HOLDINGS',
    'TRANSPORT',
    'ENTERPRISES',
    'SHANGHAI',
    'SHENZHEN',
    'VIETNAM',
    'POLSKA',
    'TECHNOLOGY',
    'FURNITURE',
    'GROUP',
    'CARGO',
    'POLAND',
    'POLLAND',
    'INDUSTRIES',
    'ELECTRONICS',
    'SPOLKA KOMANDYTOWA',
    ' SP K ',
    'SP KOMANDYTOWA',
    'CORPORATION',
    'SPOLKAKOMANDYTOWA',
)

_TO_DELETE = re.compile('[^A-Z,"\']+')
_SPACES = re.compile(' {2,}')
_TO_STRIP = ',"\' '


def process(line):
    line = line.upper().split('2.', 1)[0]
    for (s_from, s_to) in _SUBSTITUTIONS:
        line = line.replace(s_from, s_to)
    line = _TO_DELETE.sub(' ', line).lstrip(_TO_STRIP)
    for prefix in _PREFIXES:
        if line.startswith(prefix):
            line = line[len(prefix):]
        line = _SPACES.sub(' ', line.lstrip(_TO_STRIP))
    for splitter in _SPLITTERS:
        line = line.split(splitter, 1)[0]
        line = _SPACES.sub(' ', line.rstrip(_TO_STRIP))
    for suffix in _SUFFIXES:
        if line.endswith(suffix):
            line = line[:-len(suffix)]
        line = _SPACES.sub(' ', line.rstrip(_TO_STRIP))
    for substring in _SUBSTRINGS:
        line = line.replace(substring, '').strip(_TO_STRIP)
        line = _SPACES.sub(' ', line)
    return line
