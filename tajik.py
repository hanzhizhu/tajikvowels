#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, io, codecs, re
from nltk import wordpunct_tokenize as tokenize

latin = 	  "abvgGGdeOZziIIykqqlmnoprstuwwfxhhcjjSYEUARRRR''''"
cyrillic =   u"абвгғѓдеёжзиӣїйкқќлмнопрстуӯўфхҳњчҷљшъэюяыцщь«»“”"
cyr = u"абвгғѓдеёжзиӣїйкқќлмнопрстуӯўфхҳњчҷљшъэюяыцщь"
punct = u"«»“”"



f = codecs.open('tajik_corpus.txt', encoding='utf-8')
tc = open('tajc.txt', 'w+')
tc2 = open('tajcheck.txt', 'w+')
tl = open('tajl.txt', 'w+')
te = open('tajr.txt', 'w+')

alpha = re.compile(r"[A-Za-z]+")
split = re.compile(r''+ '([' +cyr + latin + ']+)' + '([^' + cyr + latin + ']+)$')
translit = {}

for i in range(0, len(latin)):
	translit[cyrillic[i]] = latin[i]

for line in f:
	line = line.lower().strip().replace('__', ' __ ').replace('_', ' _ ')
	if u'³' in line or u'ј' in line or u'і' in line or u'û' in line:
		continue
	outlist = []
	for wd in tokenize(line):
		obj = split.match(wd)

		if len(wd) == 0:
			continue
		if wd[0] in cyr:
			word = wd
			if obj:
				word = obj.group(1)
				print "object", wd 

			# if wd != word:
			# 	print wd
			# 	raw_input("cont1")

			new_word = ''
			for char in word:
				if char in translit:
					new_word += translit[char]

				elif char == 'p':
					new_word += 'r'
				elif char in latin:
					new_word += char
				else: 
					print word
					raw_input("cont")
			outlist.append(new_word)
		elif not alpha.search(wd):
			new_word = ''
			for char in wd:
				if char in punct:
					new_word += translit[char]
				else:
					new_word += char.encode('ascii', 'ignore')
			outlist.append(new_word)
		if obj:
			obj2 = obj.group(2)
			if obj.group(2) != '':
				new_word = ''
				for char in obj2:
					if char in punct:
						new_word += translit[char]
					else:
						new_word += char.encode('ascii', 'ignore')
				outlist.append(new_word)


	outline = ' '.join(outlist)
	outline = outline.replace(' e', ' ye')
	outline = outline.replace('O', 'yo')
	outline = outline.replace('E', 'e')
	outline = outline.replace('U', 'yu')
	outline = outline.replace('A', 'ya')
	if re.search(u'[ғӣқӯҳҷ]', line):
		tc.write(outline + '\n')
	elif re.search(u'[ѓїќўњљ]', line):
		tc2.write(outline + '\n')
	elif re.search(u'[абвгдеёжзийклмнопрстуфхчшъэюяыцщь]', line):
		te.write(outline + '\n')
	else:
		tl.write(outline + '\n')

f.close()
tc.close()
tl.close()
te.close()