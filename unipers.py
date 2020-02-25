#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, io, codecs, re
from nltk import wordpunct_tokenize as tokenize

unwanted = u"šâ٪žٌ ُ ً َ "
ar = u"اآبپتةثجچحخدذرزژسشصضطظعغفقكکگلمنهھویىيئء،؟؛۱۲۳۴۵۶۷۸۹۰"
art = "AObptMCjcHxdDrzZsSXLTvYGfqkkglmnhhwyIyEU,?;1234567890"
# aeiou, and Q means tanvin, and B means O written as I
la = u"šâž'"
lat = "SOZU"
nullchar = u'ـ'

upa = codecs.open('upa.txt', encoding='utf-8')
upl = codecs.open('upl.txt', encoding='utf-8')

upao = open('upa_ascii.txt', 'w+')
uplo = open('upl_ascii.txt', 'w+')
count = 0
aline = upa.readline()
lline = upl.readline()

while aline:
	aline = aline.replace(nullchar, u'')
	alineout = ''
	llineout = ''
	for char in aline.strip():
		if char not in ar:
			alineout += char.encode('ascii', 'ignore')
		else:
			alineout += art[ar.index(char)]
	for char in lline.strip().lower():
		if char not in la:
			llineout += char.encode('ascii', 'ignore')
		else:
			llineout += lat[la.index(char)]
	alines = re.split(r'[.?!]+', alineout.strip('.?!'))
	llines = re.split(r'[.?!]+', llineout.strip('.?!'))
	if len(alines) != len(llines):
		print len(llines)
		print alineout
		print llineout
		print alines
		print llines
		quit()
	else:
		for i in range(0, len(alines)):
			awrite = ' '.join(tokenize(alines[i]))
			if len(awrite) > 2:
				upao.write(awrite+ '\n')
				uplo.write(' '.join(tokenize(llines[i]))+ '\n')

	lline = upl.readline()
	aline = upa.readline()



upa.close()
upl.close()
upao.close()
uplo.close()