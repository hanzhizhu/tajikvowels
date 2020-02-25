f = open('goldall.txt', 'r')

counts = dict()
for ch in 'aeiou':
	counts[ch] = 0


for line in f:
	for char in line:
		if char in 'aeiou':
			counts[char] += 1

print counts
