import re
import numpy as np
import cPickle as pickle
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB

tajfile = open("tajc.txt", 'r')

art = "AObptMCjcHxdDrzZsSXLTvYGfqkkglmnhhwWyIyEU"
taj =   "abvgGdeZziIykqlmnoprstuwfxhcjSY"
cons  = "bvgGdZzykqlmnOprstfxhcjSY P"
vow = "aeiIuw"


alpha = re.compile(r"[abvgGdeZziIykqlmnoprstuwfxhcjSY]+$")

count = 0

consdict = dict()
for i in range(0, len(cons)):
	consdict[cons[i]] = i

vowdict = dict()
for i in range(0, 7):
	vowdict[('N'+vow)[i]] = i

def vectorize_tajik(chars, lens):

	vectors = [[0.,]*len(cons) for i in range(0,4)]
	for i in range(0,4):
		if chars[i] in vow:
			vectors[i][consdict['P']] = 1.
			if chars[i] in 'eiI':
				vectors[i][consdict['y']] = 1.
			elif chars[i] == 'a':
				vectors[i][consdict['Y']] = 1.
			elif chars[i] == 'w':
				vectors[i][consdict['v']] = 1.
		else:
			vectors[i][consdict[chars[i]]] = 1.
	flatvector = vectors[0] + vectors[1] + vectors[2] + vectors[3] + lens
	#flatvector = vectors[1] + vectors[2]  + lens
	return flatvector

X_taj = []
y_taj = []

for line in tajfile:
	count += 1 
	if count == 25000:
		break
	tokens = line.strip().split()
	for word in tokens:
		if alpha.match(word):
			word = word.replace('o','O')
			hasvow = ''
			novow = ''
			for i in range(0, len(word)):
				word += ' '
				if word[i] in vow:
					hasvow += word[i]
					novow += 'V'
				 	if word[i+1] in vow:
						hasvow += 'P'
						novow += 'P'
				elif word[i] != word[i+1]:
					hasvow += word[i]
					novow += word[i]
					if word[i+1] not in vow:
						hasvow += 'N'
						novow += 'V'


			for i in range(0, len(hasvow)):
				if hasvow[i] in vow+ 'N':
					pre = ('  ' + novow[:i]).replace('V', '')
					post = (novow[i+1:] + '  ').replace('V', '')
					chars = [ pre[-2], pre[-1], post[0], post[1] ]
					lens = [ len(pre)-2, len(post)- 2]

					prevow = hasvow[:i]
					postvow = hasvow[i+1:]
					if chars[0] == 'P':
						if chars[1] == 'P':
							chars[0] = prevow[prevow.rindex('P')-1]
						else:
							chars[0] = prevow[prevow.rindex('P')+1]
					if chars[1] == 'P':
						chars[1] = prevow[prevow.rindex('P')-1]
					if chars[3] == 'P':
						if chars[2] == 'P':
							chars[3] = postvow[postvow.index('P')+1]
						else:
							chars[3] = postvow[postvow.index('P')-1]

					if chars[2] == 'P':
						chars[2] = postvow[postvow.index('P')+1]

					if 'N' in chars:
						print hasvow, hasvow[i], postvow, postvow.index('P')
						print chars
						raw_input("cont")
					X_taj.append(vectorize_tajik(chars, lens))
					y_taj.append(('N'+vow).index(hasvow[i]))


print len(X_taj), len(X_taj[0])
print len(y_taj)

X_taj_scaled = preprocessing.scale(np.array(X_taj))
y_taj = np.array(y_taj)

clfs = [
    #KNeighborsClassifier(3),
    MultinomialNB(),
    #DecisionTreeClassifier(max_depth=5),
    #RandomForestClassifier(n_estimators=10),
    #SVC(kernel="linear", C=0.025)
    ]
count = 0
for clf in clfs:
	count += 1
	clf.fit(X_taj, y_taj)
	print "done clf", count
	pickle.dump(clf, open('25p2nb' + str(count) + '.p', 'wb'))
#pickle.dump(np.array(X_taj), open('X_taj.p', 'wb'))
#pickle.dump(np.array(y_taj), open('y_taj.p', 'wb'))
					# print hasvow
					# print chars
					# print lens

