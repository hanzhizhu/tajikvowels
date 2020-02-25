orig = open("copper.txt", 'r')
gold = open("goldall.txt", 'r')
line = orig.readline()
gline = gold.readline()
while line:
	comp = ''
	gl = gline.strip().replace('W', 'w')
	for char in gl:
		if char == '_':
			comp += ' '
		elif char not in 'aeiouQB':
			comp += char
	if comp != line.strip():
		print comp
		print line
		raw_input("cont")
	line = orig.readline()
	gline = gold.readline()


