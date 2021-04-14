import numpy as np
import random



def binaryToDecimal(n):
    return int(n,2)

def string_to_binary(text):
	res = ''.join(format(ord(i), '08b') for i in text)
	print("text is {} and its binary conversion is {}".format(text, res))
	return res

def binary_to_string(val):
	if len(val)% 8 != 0:
		raise Exception("Length of string {} should be multiple of 8".format(val))

	text = ""
	for idx in range(0, len(val), 8):
		curAlphabetInBinaryString = val[idx: idx+8]
		curAlphabetInAsciiValue = binaryToDecimal(curAlphabetInBinaryString)
		text = text + chr(curAlphabetInAsciiValue)

	return text


a = "umangjaa"
b = string_to_binary(a)
c = binary_to_string(b)

print(a)
print(b)
print(c)


def permute(text, permutationArray):
	if len(text) != len(permutationArray):
		raise Exception("length of text and permutaion array should be same\
			but they are not, text --> {}, array --> {}".format(len(text),len(permutationArray)))
	
	return [text[x-1] for x in permutationArray]

d = "0111"
c = [2, 3, 4, 1]

e = permute(d, c)
print(e)

f = "UMANGJAINY"
print(f[0:5])
print(f[5:10])


g = 10
k = 11
t = ""
t+=format(g, '04b')
print(t)

for i in reversed(range(4)):
	print(i)

assert("ok" in ["oki", "ok"])

f = [ 0 ]*20
print(len(f))


res = [x for x in range(10)]
np.random.shuffle(res)
print(res)

for i,x in enumerate(res):
	print(i,x)