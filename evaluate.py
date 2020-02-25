import sys, io, codecs, re

othername = raw_input("filename?")
other = open(othername, 'r')
gold = open("goldall.txt", 'r')

oline = other.readline()
gline = gold.readline()

vowels = "aeiou"
cons = 'AObptMCjcHxdDrzZsSXLTvYGfqkkglmnhhwyIyEUW'

allvowels = 0
tp = 0
tn = 0
fp = 0
fn = 0

alpha = re.compile(r"[A-Za-z]+")


while gline:
	olist = oline.strip().replace('_', ' ').replace('F', 'u').replace('J', 'i').replace('e', 'i').replace('ah ', 'ih ').split()
	glist = gline.strip().replace('_', ' ').replace('e', 'i').split()

	assert len(olist) == len(glist), "same # words"
	for i in range(0, len(olist)):
		owd = olist[i]
		owd = owd.replace('uw', 'Rw').replace('u', 'o').replace('R', 'u')
		gwd = glist[i]
		vowelless = ''
		ow = ''
		gw = '' 

		if 'B' in gwd or not alpha.match(gwd):
			continue
		gwd = gwd.replace('Q', '')


		if 'B' in owd or not alpha.match(owd):
			continue
		owd = owd.replace('Q', '')

		for j in range(0, len(gwd)):

			gword = gwd + '$'
			if gword[j] in cons:
				vowelless += gword[j]
				if gword[j+1] in cons + '$':
					gw += gword[j] + 'V'
				else:
					gw += gword[j]
			else:
				gw += gword[j]
		for j in range(0, len(owd)):
			oword = owd + '$'
			if oword[j] in cons and oword[j+1] in cons + '$':
				ow += oword[j] + 'V'
			else:
				ow += oword[j]
		assert len(ow) == len(gw) , "same # chars" + ow + ' ' + gw
		assert len(vowelless)* 2 == len(ow), "double # chars "  + ow + ' ' + gw
	#	print ow, gw
	#	raw_input("cont")
		for j in range(0, len(gw)):
			if gw[j] in vowels:
				allvowels += 1
				if gw[j] == ow[j]:
					tp += 1
				else:
					fn += 1
			elif gw[j] == 'V':
				if gw[j] == ow[j]:
					tn += 1
				else:
					fp += 1


	oline = other.readline()
	gline = gold.readline()


print "precision", 1.*tp/(tp+fp+1)
print "recall", 1.*tp/(tp+fn)
print "accuracy", 1.*(tp+tn)/(tp+tn + fp + fn)


other.close()
gold.close()