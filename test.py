import sys, io, re

from collections import deque



art = "AObptMCjcHxdDrzZsSXLTvYGfqkkglmnhhwyIyEU"
consonants = "bptjcxdrZsSfqkglmn"

lat = "SOZU"


convert = dict()
convert['A'] = ''
convert['O'] = 'O'
convert['M'] = 't'
convert['C'] = 'ss?'
convert['H'] = 'hh?'
for char in "DzLv":
	convert[char] = 'zz?'
convert['X'] = 'ss?'
convert['T'] = 'tt?'
convert['Y'] = 'U?'
convert['G'] = 'qq?'
convert['h'] = 'hh?|e$'
convert['w'] = '[wuo]|vv?'
convert['W'] = '[wuo]?|v?v?'
convert['y'] = 'yi|iy?|yy?'
convert['I'] = 'yi|iy?|yy?'
convert['E'] = 'U?'
convert['U'] = 'U?'
convert[','] = ','
for char in consonants:
	convert[char] = ''+ char + char + '?'
for char in art:
	if char not in convert:
		print char + " not found"

vowelre = '([aeo]?)'


memo = dict() 

def makegold(ac, gc, origc):
	gstr = ''
	if ac != gc:
		if ac == 'h':
			if gc == 'e':
				gstr += 'eh'
			else:
				gstr += 'h'
		elif ac in 'wW':
			if gc == '':
				gstr += 'W'
			elif 'u' in gc:
				gstr += 'uw'
			elif 'o' in gc:
				gstr += 'ow'
			else:
				gstr += 'w'
		elif ac in 'yI':
			if 'i' in gc:
				gstr += 'i' + ac
			else:
				gstr += ac
		else:
			gstr += origc
	else:
		gstr += origc
	if len(gc) == 2:
		if gc[0] == gc[1]:
			gstr+= 'Q'
	return gstr



count = 0
aline = "Agrnh , bA msElh I mwjwd knwnI rwbrw mySwym , yYnI wAZhAyI bA frAgwyShAI gwnAgwn kh bA yk jwr AmlA nwSth mySwnd , yA xwAnA nbwdn frAgwyShAI wAZh hAI nA OSnA"
lline = "agarna , bO masUaleye mowjude konuni ruberu miSavim , yaUni vOZehOyi bO farOguyeShOye gunOgun ke bO yek jur emlO neveSte miSavand , yO xOnO nabudane farOguyeShOye vOZehOye nOOSnO"
alpha = re.compile(r"[A-Za-z]+")




goldout = []
alist = deque(aline.strip().split())
llist = deque(lline.strip().split())
while True:
	
	aword = alist.popleft()
	lword = llist.popleft()
	while not alpha.match(aword):
		goldout.append(aword)
		if len(alist) != 0:
			aword = alist.popleft()
		else:
			break

	while not alpha.match(lword):
		if len(llist) != 0:
			lword = llist.popleft()
		else:
			break


  	#if memo
  	if not alpha.match(aword):
  		print "only punctuation"
  		#goldout.append(aword)
  		break
  	elif not alpha.match(lword):
  		print "only punctuation on l"
  		break
	elif len(aword) == 1:
		print "too short: " + aword + ', ' + lword + " on line " + str(count)
		if (aword, lword) in memo:
			goldout.append(memo[(aword, lword)])
		else:
			inshort = raw_input('correct string: ').strip()
			memo[(aword, lword)] = inshort
			goldout.append(inshort)

	else:
		print "merging " + aword + " and " + lword
		aw = (aword[0] + aword[1:].replace('A', 'O')).replace('xw', 'xW')

		exp = r''
		for char in aw:
			exp += '(' + convert[char] + ')'+ vowelre
		expr = re.match(exp+ '$', lword)

		if expr:

			goldstr = ''
			for i in range(0, len(aw)):
				achar = aw[i]
				g = 2*i+1
				gchar = expr.group(g)
				origchar = aword[i]
				goldstr += makegold(achar, gchar, origchar)
				goldstr += expr.group(g+1)
			goldout.append(goldstr)


				
		elif len(alist) != 0:
			print exp
			aword2 = alist.popleft()
			print "combining " + aword + " with " + aword2
			aw2 = aword2
			if len(aw2) > 1:
				aw2 = (aword2[0] + aword2[1:].replace('A', 'O')).replace('xw', 'xW')
			exp2 = r''
			for char in aw2:
				exp2 += '(' + convert[char] + ')'+ vowelre

			expr2 = re.match(exp.replace('$', '')+exp2 + '$', lword)

			if expr2:
				goldstr = ''
				for i in range(0, len(aw)):
					achar = aw[i]
					g = 2*i+1
					gchar = expr2.group(g)
					origchar = aword[i]
					goldstr += makegold(achar, gchar, origchar)
					goldstr += expr2.group(g+1)
				goldstr += '_'
				for i in range(0, len(aw2)):
					achar = aw2[i]
					g = 2*(len(aw)+i)+1
					print g
					print exp.replace('$', '')+exp2 
					gchar = expr2.group(g)
					origchar = aword2[i]
					goldstr += makegold(achar, gchar, origchar)
					goldstr += expr2.group(g+1)
				goldout.append(goldstr)
			
			else:
				print exp2
				alist.appendleft(aword2)
				lword2 = 'NONE'
				if len(llist) > 0:
					lword2 = llist[0]

				print "mismatch: " + aword + ' ' + alist[0] + ', ' + lword + ' ' + lword2
				intext = raw_input('a/l/n: ')
				if intext[0] == 'a':
					alist.popleft()
				elif intext[0] == 'l':
					llist.popleft()
				intext2 = raw_input('correct string: ')
				goldout.append(intext2.strip())
		else:
			print exp
			lword2 = 'NONE'
			if len(llist) > 0:
				lword2 = llist[0]
			print "mismatch: " + aword + ', ' + lword + ' ' + lword2
			intext = raw_input('l/n: ')

			if intext[0] == 'l':
				llist.popleft()
			intext2 = raw_input('correct string: ')
			goldout.append(intext2.strip())
	if len(alist) == 0:
		print "ending well"
		break
	if len(llist) == 0:
		print "ending early on line " + str(count)
		print alist

print ' '.join(goldout)




