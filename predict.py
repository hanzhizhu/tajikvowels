import cPickle as pickle
from sklearn import svm
from collections import deque
import re

art =   "ObptjcxdrzZsSYGfqkglmnhvy"
taj =   "abvgGdeZziIykqlmnoprstuwfxhcjSY"
cons  = "bvgGdZzykqlmnOprstfxhcjSY"
vow = "aeiJuF"
constaj = "bvgGdZzykqlmnOprstfxhcjSY P"

f = open('copper.txt', 'r')
out = open('25p2nb1.txt', 'w+')

clf = pickle.load(open('25p2nb1.p', 'r'))

alpha = re.compile(r"[A-Za-z]+$")

consdict = dict()
for i in range(0, len(constaj)):
	consdict[constaj[i]] = i

vowdict = dict()
for i in range(0, 7):
	vowdict[('N'+vow)[i]] = i

def vectorize_farsi(chars, lens):
	vectors = [[0.,]*len(constaj) for i in range(0,4)]
	for i in range(0,4):
		vectors[i][consdict[chars[i]]] = 1.
	
	flatvector = vectors[0] + vectors[1] + vectors[2] + vectors[3] + lens	
	#flatvector = vectors[1] + vectors[2] + lens
	return flatvector

def predict(vector, must = False):
	num = clf.predict(vector)[0]
	if must:
		best = clf.predict_proba(vector)
		num = best.argsort()[0][-2]
		return vow[num - 1]
	if num == 0:
		return ''
	else:
		return vow[num-1]

for line in f:

	outlist = []

	deck = line.strip().split()
	for origword in deck:
		word = origword
		if not alpha.match(word):
			outlist.append(word)
			continue

		for char in "DzLv":
			word = word.replace(char, 'z')
		word = word.replace('w', 'v')
		word = word.replace('M', 't')
		word = word.replace('T', 't')
		word = word.replace('C', 's')
		word = word.replace('X', 's')
		word = word.replace('H', 'h')
		word = word.replace('I', 'y')
		word = word.replace('E', 'Y')
		word = word.replace('U', 'Y')
		word = word[0] + word[1:].replace('A', 'O')

		pword = ''
		flag = False
		for i in range(0, len(word)):
			pword += origword[i]
			if flag:
				flag = False
				continue
			if word[i] == 'O':
				continue

			pre = ('  ' + word[:i+1]).replace('A', '')

			post = word[i+1:] + '  '
			if word[i] == 'h' and pre[-1] != 'O' and post[0] == ' ':
				continue
			if post[0] == 'h' and post[1] == ' ':
				post = post.replace('Oh', 'OH').replace('h ', ' ').replace('H', 'h')
				chars = pre[-2] + pre[-1] + post[0] + post[1]
				lens = [ len(pre)-2, len(post)- 2]

				vector = vectorize_farsi(chars, lens)
				pchar = predict(vector, must = True)
				pword += pchar
				continue
			post = post.replace('Oh', 'OH').replace('h ', ' ').replace('H', 'h')

			if post[0] in 'vy':
				vy = post[0]
				post = post[1:] + ' '
				chars = pre[-2] + pre[-1] + post[0] + post[1]
				lens = [ len(pre)-2, len(post)- 2]
				vector = vectorize_farsi(chars, lens)
				pred = predict(vector)
				if origword == 'cwn':
					print origword, word, i, pre, post, pred
				if len(pred) > 0 and pred in 'uw' and vy == 'v':
					pword += pred
					# print origword, word, i, pre, post, pred
					# raw_input ("cont")
					flag = True
					continue
				elif len(pred) > 0 and pred in 'eiI' and vy == 'y':
					pword += pred
					# print origword, word, i, pre, post, pred
					# raw_input ("cont")
					flag = True
					continue
				else:
					post = vy + post[:-1]
			
			chars = pre[-2] + pre[-1] + post[0] + post[1]
			lens = [ len(pre)-2, len(post)- 2]

			vector = vectorize_farsi(chars, lens)
			pword += predict(vector)
			# print origword, word, i, pre, post, predict(vector)
			# raw_input ("cont")

		outlist.append(pword)
	out.write(' '.join(outlist) + '\n')


f.close()
out.close()


