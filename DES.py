import numpy as np
import random
import utils

'''
Practical Assignment 1
 

Write a program with a nice UI to implement and study DEA with different hyper parameters. 

Number of rounds n=1,8,16,32; 
half width of data block w=16,32,64. 
Pick suitable entries for P- and S- boxes.

(a) Demonstrate the avalanche effect with different hyper parameter choices.

(b) Demonstrate how weak keys supplied by the user affect the round keys. 
'''


# Initial permutation for message 
initial_message_permutation = [
		58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4,
		62, 54, 46, 38, 30, 22, 14, 6,
		64, 56, 48, 40, 32, 24, 16, 8,
		57, 49, 41, 33, 25, 17, 9, 1,
		59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5,
		63, 55, 47, 39, 31, 23, 15, 7
		]

# Final permutation for message which is inverse of initial permutaion
final_message_permutation = [
		40, 8, 48, 16, 56, 24, 64, 32,
		39, 7, 47, 15, 55, 23, 63, 31,
		38, 6, 46, 14, 54, 22, 62, 30,
		37, 5, 45, 13, 53, 21, 61, 29,
		36, 4, 44, 12, 52, 20, 60, 28,
		35, 3, 43, 11, 51, 19, 59, 27,
		34, 2, 42, 10, 50, 18, 58, 26,
		33, 1, 41, 9, 49, 17, 57, 25
		]

# expansion used in round functions
expansion_P_box = [
		32,  1,  2,  3,  4,  5,
		4,  5,  6,  7,  8,  9,
		8,  9, 10, 11, 12, 13,
		12, 13, 14, 15, 16, 17,
		16, 17, 18, 19, 20, 21,
		20, 21, 22, 23, 24, 25,
		24, 25, 26, 27, 28, 29,
		28, 29, 30, 31, 32,  1
		]


# S boxes to compression in round function
S_boxes = [
[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
],

[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
],

[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
],

[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
],  

[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
],

[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
], 

[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
],
   
[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]
]

# final permutation in round function
round_function_final_permutation =    [
		16,  7, 20, 21,
		29, 12, 28, 17,
		1, 15, 23, 26,
		5, 18, 31, 10,
		2,  8, 24, 14,
		32, 27,  3,  9,
		19, 13, 30,  6,
		22, 11,  4, 25
		]


#Initial permut made on the key
initial_key_permutation = [
		57, 49, 41, 33, 25, 17, 9,
		1, 58, 50, 42, 34, 26, 18,
		10, 2, 59, 51, 43, 35, 27,
		19, 11, 3, 60, 52, 44, 36,
		63, 55, 47, 39, 31, 23, 15,
		7, 62, 54, 46, 38, 30, 22,
		14, 6, 61, 53, 45, 37, 29,
		21, 13, 5, 28, 20, 12, 4]

#Permut applied on shifted key to get Ki+1
inner_key_permutaion = [
		14, 17, 11, 24, 1, 5, 3, 28,
		15, 6, 21, 10, 23, 19, 12, 4,
		26, 8, 16, 7, 27, 20, 13, 2,
		41, 52, 31, 37, 47, 55, 30, 40,
		51, 45, 33, 48, 44, 49, 39, 56,
		34, 53, 46, 42, 50, 36, 29, 32]


#Matrix that determine the shift for each round of keys
#Intiallized in des init 
SHIFT = []




'''
convert binary string to its decimal representation
'''
def binaryToDecimal(n):
    return int(n,2)

'''
converts string to binary
By converting each character to its ASCII value 
and then converting that value to binary with exactly 8 bit
''' 
def string_to_binary(text):
	res = ''.join(format(ord(i), '08b') for i in text)
	# print("text is {} and its binary conversion is {}".format(text, res))
	return res

'''
converts binary string to string
By taking each 8 character and converting then to their decimal form 
and then taking this decimal value as its ASCII value, finding the character 
'''
def binary_to_string(val):
	if len(val)%8 != 0:
		raise Exception("Length of string {} should be multiple of 8".format(val))

	text = ""
	for idx in range(0, len(val), 8):
		curAlphabetInBinaryString = val[idx: idx+8]
		curAlphabetInAsciiValue = binaryToDecimal(curAlphabetInBinaryString)
		text = text + chr(curAlphabetInAsciiValue)

	return text




class DES(): 

	#private member
	__cipherText = None	
	
	'''
	Hyperpameters
	nRounds --> No of rounds in DES algorithm
	seed    --> seed value to reproduce
	text    --> text to encrypt, will be padded with ' ' if size of not multiple of 8 
	key     --> key, size should be exactly 8
	'''
	def __init__(self, text, key, nRound = 16, blockSize = 64, seed = None):
		
		if len(key) != 8:
			raise Exception("Key length should be exactly 8")


		self.nRound = nRound
		self._seed = seed
		self.blockSize = blockSize

		if self.blockSize != 64:
			assert("This implementation only works with 64 bit block sizes")

		if seed is not None:
			np.random.seed(seed)
			random.seed(seed)

		for i in range(self.nRound):
			SHIFT.append(int(np.random.random()*2+1))

		# print(SHIFT)

		self.textString = text
		self.keyString  = key

		self.addPadding()
		# print(self.textString)

		self.text = string_to_binary(self.textString)
		# print(len(self.text))
		
		self.key  = string_to_binary(key)
		
		if len(self.key) != 64:
			raise Exception("Key length should be changed 64 but key length \
				is {}".format(len(self.key)))

		self.keys = self.generateKey(self.key)
		if len(self.keys) != self.nRound:
			raise Exception("Total 16 keys should be generated. check generateKey\
				function")			

		if len(self.keys[0]) != 48:
			raise Exception("keys should be compressed to 48 length . check generateKey\
				function")


	# self explanatory
	def permute(self,text, permutationArray):

		return [text[x-1] for x in permutationArray]

	# circular left shift
	def shift(self, key, n):

		return key[n : ] + key[0 : n] 

	# generate keys required for each round
	def generateKey(self, key):
		if len(key) != 64: 
			raise Exception("Key length should be exactly 64 but \
				it is {}".format(len(key)))

		keys = []
		key = self.permute(key, initial_key_permutation)
		Lkey = key[0:28]
		Rkey = key[28:56]
		for roundNo in range(self.nRound):
			Lkey = self.shift(Lkey, SHIFT[roundNo])
			Rkey = self.shift(Rkey, SHIFT[roundNo])

			compressedKey = self.permute(Lkey+Rkey, inner_key_permutaion)
			if len(compressedKey) != 48:
				raise Exception("keys should be compressed to 48 length . check generateKey\
					function")	
			keys.append(compressedKey)

		return keys

	# self explanatory
	def XOR(self, arr1, arr2):
		if len(arr1) != len(arr2):
			raise Exception("arr1 and arr2 should have equal length. \
				\n But arr1 is {} \n \
				\n arr2 is {}".format(arr1, arr2));

		return [str(int(x)^int(y)) for x,y in zip(arr1, arr2)];

	# self explanatory
	def sBox(self, text):
		boxNo = 0
		res = ""
		for i in range(0, 48, 6):
			curText = text[i: i+6]
			rowNo = binaryToDecimal(curText[0] + curText[5])
			colNo = binaryToDecimal(curText[1]+curText[2]+curText[3]+curText[4])
			res += format(S_boxes[boxNo][rowNo][colNo], '04b')
			boxNo+=1

		assert(len(res)==32)
		return res

	# self explanatory
	def roundFunction(self, text, roundNo):
		if len(text) != 32 :
			raise Exception("Inside Round Function, text length should\
				be 32 but {} is given for {}".format(len(text), text))

		text = self.permute(text, expansion_P_box)
		assert(len(text) == 48)

		text = self.XOR(text, self.keys[roundNo])

		text = self.sBox(text)
		assert(len(text)==32)

		text = self.permute(text, round_function_final_permutation)
		return text

	'''
		NOT USED, THIS FUNCTION CAN BE DELETED
	'''
	def findExpansionAndCompressionArray(self, fromSize, toSize):
		expand = []
		compress = [ 0 ]*fromSize
		for i  in range(toSize):
			cur = int(np.random.random()*fromSize + 1)
			expand.append(cur)
			compress[cur-1] = i + 1

		# print(expand)
		# print(compress)
		return (expand, compress)


	'''
		RUNNING DES ON A BLOCK OF 64 BITS
	'''
	def runForEachBlock(self, text, action):
		if len(text) != 64:
			raise Exception("text length should be exactly 64 but \
				it is {}".format(len(text)))

		text = self.permute(text, initial_message_permutation)

		textL = text[   : 32]
		textR = text[32 :   ]

		for roundNo in range(self.nRound):
			if action == "encrypt":
				temp = self.roundFunction(textR, roundNo)
			else:
				temp = self.roundFunction(textR, self.nRound - roundNo -1)
			temp = self.XOR(temp, textL)			
			textL = textR
			textR = temp;

		encryptedText = self.permute(textR+textL, final_message_permutation)
		return encryptedText;

	# self explanatory
	def addPadding(self):
		while len(self.textString)%8 != 0:
			self.textString+=" ";

	'''
		BREAKING TEXT INTO BLOCKS OF SIZE 64 BITS AND RUNNING DES ON EACH BLOCK
	'''
	def run(self, action):
		assert(action in ["encrypt", "decrypt"])

		if action == "encrypt":
			text = self.text
		else :
			text = self.cipherText

		res = ""
		for i in range(0, len(text), self.blockSize):
			curText = text[i:i+self.blockSize]
			temp = self.runForEachBlock(curText, action)
			for ch in temp:
				res+=ch

		# print("action is ", action)
		# print("text is ", text)
		# print("res is ", res)
		# print(binary_to_string(res))
		if action == "encrypt":
			self.cipherText  = res
		else:
			assert(self.text == res)

		return binary_to_string(res)



if __name__ == '__main__':
    key = "umbngjai"
    text= "umangjainisagoodboyokbyebyeanythingyouwantotypehere"
    d = DES(text, key, 128, 64, 12)
    a  = d.run("encrypt")
    print("encryption DONE")
    print("Ciphered: ", a)
    b = d.run("decrypt")
    print("Decryption Done")
    print("Deciphered: ", b)

