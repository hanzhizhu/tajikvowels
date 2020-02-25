#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kazakh Script Converter for Stanford Field Methods Class 2013
author: Hanzhi Zhu
created: January 24, 2013

Converts input text written in the provisional Kazakh orthography used for our class (see handout) into 4 scripts:
cyrillic (official in Kazakhstan)
latin (version proposed by Kazakh government)
ipa (according to handout, feel free to change as suited)
arabic (official in China)

usage:
python kazakh_script_converter.py (to input text on command line)
python kazakh_script_converter.py [input filename] (prints output to console)
python kazakh_script_converter.py [input filename] [output filename]
(creates new output file or updates existing file)

Notes:
reverse conversion not supported
added Russian <э> to our orthography
arabic frontness marker (ء) probably not 100% accurate

Updates:
2013/1/26 file output support
2013/1/27 bug fix (unicode command line input)
"""

import sys, io, codecs, re

in_text = ''
out_text = ''
class_orth = u"aäbcCdeéfgGhiïjklmnNoöpqrsStuUüvwxyzZ"
cyrillic =   u"аәбцчдеэфгғһиійклмнңоөпқрсштуұүвухызж"
latin =      u"aäbcçdeéfgğhïiyklmnñoöpqrsştwuüvwxızj"
#ipa =       u"aæbcCdeɛfgɣhiɪjklmnŋoɵpqrsʃtuʊʏvwxɯzʒ" 
ipa =        u"aæbcCdeɛfgʁhiɨjklmnŋoøpqrsʃtuʊyvwχɯzʒ"
arabic =     u"اابcچدەەفگعھيىيكلمنڭووپقرسشتۋۇۇۆۋحىزج"
    
if len(sys.argv) > 1:
    filename = sys.argv[1]
    try:
        f = codecs.open(filename, encoding='utf-8')
        in_text = f.read()
        f.close()
    except:
        print "Cannot find file."
        in_text = raw_input('input string: ').decode('utf-8')
else: in_text = raw_input('input string: ').decode('utf-8')
 
in_text = in_text.replace(u'uw', u'u') # corrects <uw> to <u> (not needed)
in_text = in_text.replace(u'ijï', u'iï') # corrects <ijï> to iï> (not needed)
in_text = in_text.replace(u'ije', u'ie')
#in_text = in_text.replace(u'je', u'e')

out_type = ''
while not re.match('[clia]$', out_type):
    out_type = raw_input('alphabet to output [c/l/i/a]: ')
    if len(out_type) >= 1: out_type = out_type[0]
    else: sys.exit()

abbrevs = dict(l=latin, c=cyrillic, i=ipa, a=arabic)
out_orth = abbrevs[out_type]

translit = {}
for i in range(0,len(class_orth)):
    translit[class_orth[i]] = out_orth[i]

#arabic-specific preprocessing
if out_type is 'a': 
    input_list = in_text.strip().split(' ')
    in_text = ''
    for word in input_list:
        if re.match(u'([^eïäöü]*(^|[^kge])[ïäöü][^eïäöü]*)+$', word):
            in_text = in_text + u'ء' + word + u' '
        elif re.match(u'[^aeyouU]*(^|[^kge])[i][^aeyouU]*', word):
            in_text = in_text + u'ء' + word + u' '
        else: in_text = in_text + word + u' '
    in_text = in_text.strip(' ')

for ch in in_text:
    new_ch = ch
    if ch in class_orth:
        new_ch = translit[ch]
    out_text += new_ch

if out_type is 'i':
    out_text = out_text.replace(u'c', u'ts') 
    out_text = out_text.replace(u'C', u'tʃ')

if out_type is 'c':
    #cyrillic-specific diphonemic graphs
    out_text = out_text.replace(u'йа', u'я')
    out_text = out_text.replace(u'йу', u'ю')
    out_text = out_text.replace(u'йо', u'ё')
    out_text = out_text.replace(u'шш', u'щ')

out_text = out_text.replace('-', '') #gets rid of <-> (not needed)

if len(sys.argv) > 2: 
    out_filename = sys.argv[2]
    try:
        f = codecs.open(out_filename,'a','utf-8')
        f.write(out_text)
        f.close()
    except:
        print "Error writing to output file."
        print out_text
else: print out_text
