"""
##########################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file implementes some supplementary functions
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""

#global variables
diffEncDict = {'A' : ['C','G','T'] ,'C' : ['G','T','A'] ,'G' : ['T','A','C'] ,'T':['A','C','G'] }
complementDictionary = {'A':'T','T':'A','C':'G','G':'C'}

# Uses differential encoding
# Input : base 3 number
# Output A,T,C,G

def diffEncode(prevBase,currTrit):
   global diffEncDict
   currBase = diffEncDict[prevBase][int(currTrit)]
   return currBase


# differentialy encode whole string
# Input : trit string
# Output : Corresponding DNA Sequence
def encodeSTR(string1,prevBase):
   finalDNAString = []
   for trit in string1:
      currBase = diffEncode(prevBase,trit)
      finalDNAString.append(currBase)
      prevBase = currBase
   return ''.join(finalDNAString)

# converts decimal to base 3 string
# Input: A decimal that is base 10 number
# Output: Base 3 Numerical String of length equal to lengthOfOut
def intToBase3(num,lengthOfOut):
   output = ''
   for i in range(1,lengthOfOut+1):
      output = str((num%3)) + output
      num = int(num/3)      
   return output

# Converts base 3 number to decimal number
def base3ToInt(tritString):
   num = 0
   for trit in tritString:
      num = (num*3) + int(trit)
   return num

# Converts base b number to decimal number
def base256ToInt(byteList):
   num = 0
   mul1 = 1
   for byte in byteList:
      num = num + byte*mul1
      mul1=mul1*256
   return num

# Reverse complements the DNA Chunk
def reverseComplement(dnaStr):
   global complementDictionary
   outputStr = []
   i = len(dnaStr) - 1
   while i>=0 :
      outputStr.append(complementDictionary[dnaStr[i]])
      i = i - 1
   return ''.join(outputStr)

# converts DNA string to trits using differential decoding
def getTrits(dnaStr,prevBase):
   output = []
   for base in dnaStr:
      if prevBase!=base:
         output.append(str(diffEncDict[prevBase].index(base)))
      prevBase = base
   return ''.join(output)
