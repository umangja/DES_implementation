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
	
	def __init__(self, text, key, nRound = 16, blockSize = 64, seed = None):
		
		if len(key) != 8:
			raise Exception("Key length should be exactly 8")


		'''
		Hyperpameters
		'''
		self.nRound = nRound
		self._seed = seed
		self.blockSize = blockSize

		# seed to reproduce results 
		if seed is not None:
			np.random.seed(seed)
			random.seed(seed)


		if blockSize%8 != 0:
			raise Exception("blockSize should be a multiple of 8 but {} is not".format(blockSize))
		
		if blockSize < 16 or blockSize > 64:
			raise Exception("blockSize should be greater than 16  and less than 64 but {} is not".format(blockSize))


		#Matrix that determine the shift for each round of keys
		#Intiallized in des init 
		self.SHIFT = []
		for i in range(self.nRound):
			self.SHIFT.append(int(np.random.random()*2+1))


		self.textString = text
		self.keyString  = key

		self.addPadding()

		self.text = string_to_binary(self.textString)
		self.key  = string_to_binary(key)
		
		if len(self.key) != 64:
			raise Exception("Key length should be changed 64 but key length \
				is {}".format(len(self.key)))


		# Initial permutation for message
		self.initial_message_permutation = None
		
		# expansion used in round functions
		self.expansion_P_box = None

		# Final permutation for message which is inverse of initial permutaion
		self.final_message_permutation = None

		# final permutation in round function
		self.round_function_final_permutation = None
	
		#Initial permut made on the key
		self.initial_key_permutation = None;

		self.inner_key_permutaion = None;

		self.keys = self.generateKey(self.key)

		if len(self.keys) != self.nRound:
			raise Exception("Total {} keys should be generated. check generateKey\
				function".format(self.nRound))			

		if len(self.keys[0]) != 48:
			raise Exception("keys should be compressed to 48 length . check generateKey\
				function")
 	
 	# Add space padding for make size appropriate 
	def addPadding(self):
		div = self.blockSize/8 
		if div <= 0:
			raise Exception("Block Size should be positive multiple of 8 but {} is given".format(self.blockSize))
		while len(self.textString)%div != 0:
			self.textString+=" ";

	#permute the array according to the given permutation array
	def permute(self,text, permutationArray):

		return [text[x-1] for x in permutationArray]

	# circular left shift
	def shift(self, key, n):

		return key[n : ] + key[0 : n] 

	# Generate key for each round 
	def generateKey(self, key):
		if len(key) != 64: 
			raise Exception("Key length should be exactly 64 but \
				it is {}".format(len(key)))

		keys = []

		if self.initial_key_permutation is None:
			_, self.initial_key_permutation = self.getExpansionArray(56, 64) 

		if self.inner_key_permutaion is None:
			_, self.inner_key_permutaion = self.getExpansionArray(48, 56)

		key = self.permute(key, self.initial_key_permutation)
		Lkey = key[0:28]
		Rkey = key[28:56]
		for roundNo in range(self.nRound):
			Lkey = self.shift(Lkey, self.SHIFT[roundNo])
			Rkey = self.shift(Rkey, self.SHIFT[roundNo])

			compressedKey = self.permute(Lkey+Rkey, self.inner_key_permutaion)
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

	# return expansion and corresponding compression array for given sizes
	def getExpansionArray(self, fromSize, toSize):
		expand = []
		compress = [ 0 ]*fromSize
		for i  in range(toSize):
			cur = int(np.random.random()*fromSize + 1)
			expand.append(cur)
			compress[cur-1] = i + 1

		return (expand, compress)

	# self explanatory
	def getPermutaion(self, ofSize):
		res = [x+1 for x in range(ofSize)]
		np.random.shuffle(res)
		return res

	# self explanatory
	def getInversePermutation(self, perm) :
		res = [0] * len(perm)
		for i,x in enumerate(perm):
			res[x - 1] = i+1 
		return res

	# SBox of DES Algorithm
	def sBox(self, text):
		boxNo = 0
		res = ""
		bits = self.blockSize//16
		for i in range(0, 48, 6):
			curText = text[i: i+6]
			rowNo = binaryToDecimal(curText[0] + curText[5])
			colNo = binaryToDecimal(curText[1]+curText[2]+curText[3]+curText[4])
			temp = format(S_boxes[boxNo][rowNo][colNo], '04b') 
			temp = temp[ : bits]
			res+=temp
			boxNo+=1

		assert(len(res)==self.blockSize//2)
		return res

	# Each Round of Algorithm
	def roundFunction(self, text, roundNo):
		if len(text) != self.blockSize/2 :
			raise Exception("Inside Round Function, text length should\
				be {} but {} is given for {}".format(self.blockSize/2,len(text), text))

		if self.expansion_P_box is None:
			self.expansion_P_box,_ = self.getExpansionArray(len(text), 48)

		text = self.permute(text, self.expansion_P_box)
		assert(len(text) == 48)

		text = self.XOR(text, self.keys[roundNo])

		text = self.sBox(text)
		assert(len(text)==self.blockSize/2)

		if self.round_function_final_permutation is None:
			self.round_function_final_permutation = self.getPermutaion(self.blockSize//2)

		text = self.permute(text, self.round_function_final_permutation)
		return text

	def runForEachBlock(self, text, action):
		if len(text) != self.blockSize:
			raise Exception("text length should be exactly {} but \
				it is {}".format(self.blockSize, len(text)))

		if self.initial_message_permutation == None:
			self.initial_message_permutation = self.getPermutaion(self.blockSize) 
		
		text = self.permute(text, self.initial_message_permutation)

		textL = text[   : self.blockSize//2]
		textR = text[self.blockSize//2 :   ]

		for roundNo in range(self.nRound):
			if action == "encrypt":
				temp = self.roundFunction(textR, roundNo)
			else:
				temp = self.roundFunction(textR, self.nRound - roundNo -1)
			temp = self.XOR(temp, textL)			
			textL = textR
			textR = temp;

		if self.final_message_permutation is None:
			self.final_message_permutation = self.getInversePermutation(self.initial_message_permutation)
		
		encryptedText = self.permute(textR+textL, self.final_message_permutation)
		return encryptedText;

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

		if action == "encrypt":
			self.cipherText  = res
		else:
			assert(self.text == res)

		return binary_to_string(res)


if __name__ == '__main__':
    key = "ÿÿÿÿÿÿÿÿ"
    text= "umangjain"
    d = DES(text, key, 16, 16)
    a  = d.run("encrypt")
    print("encryption DONE")
    print("Ciphered: ", a)
    b = d.run("decrypt")
    print("Decryption Done")
    print("Deciphered: ", b)
    print("Round Keys are \n ")
    i = 1
    for x in d.keys : 
    	print("Key for round {} is \n {} \n".format(i,x))
    	i = i+1
    # print(binary_to_string("11111111"))

# if __name__ == '__main__':

# 	text = str(input("Enter message to encrypt\n(Note : text will be padded \
#  by ' ' to make its length appropriate)\n"))

# 	key = None
# 	while key is None or len(key)!=8:
# 		key = str(input("Enter key\n(Note : key length should be EXACTLY equals to 8)\n"))

# 	blockSize = int(input("Enter Block Size\n"))
# 	nRounds = int(input("Enter Number of rounds\n"))

# 	d = DES(text, key, nRounds, blockSize, 5000)
# 	a  = d.run("encrypt")
# 	print("encryption DONE")
# 	print("Ciphered: ", a)
# 	b = d.run("decrypt")
# 	print("Decryption Done")
# 	print("Deciphered: ", b)



