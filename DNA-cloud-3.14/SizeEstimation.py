"""
##########################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file implements memory estimation function for Goldman as well as Golay .
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""
import math

def extractFilenameFromPath(path):
	i = len(path) - 1
	while i>=0 :
		if path[i] == "\\" or path[i] =='/'  :
			break
		i = i - 1
	return path[i+1:]


def estimateNoOfDNABasesUsedForGolayEncoding(pathToFile,filesize):

	fileName = extractFilenameFromPath(pathToFile)
	fileName = fileName.split(".")[0]   #retriving file name from fileName + extension

	numberOfFileNameChunks = int(math.ceil(len(fileName)/9.0)) # divide by 9 because max 9 bytes in a chunk
	numberOfExtensionChunks = 1
	numberOfDataChunks = int( math.ceil(filesize/9.0) )
	totalNumberOfChunksExceptGodChunk = numberOfFileNameChunks + numberOfExtensionChunks + numberOfDataChunks

	chunkIDTrits = int( math.ceil( math.log(totalNumberOfChunksExceptGodChunk,3) ) ) #number of trits required to address chunk indices
	extraTrits = 5 + chunkIDTrits   # trits excluding payload trits  (2 flags + 1 parity + 2 file ID + chunkID length)
	payloadTrits = 99
	totalTritsInRegularChunks = payloadTrits+extraTrits
    
	godChunkSize = 11   # this 11 trits used for encoding number of filename chunks
	noOfBytesToStoreFileSize = int(math.ceil(math.log(filesize,256))) # file size is stored as base 256 string
	godChunkSize = godChunkSize + 2 # Used for telling how many next bytes used for storing filesize
	howMuchToRepeat = int(math.ceil((totalTritsInRegularChunks*1.0)/(noOfBytesToStoreFileSize*11)))  
	godChunkSize = godChunkSize + noOfBytesToStoreFileSize*11*howMuchToRepeat  #Repeatitions used to make god chunk larger than any regular chunk
	godChunkSize = godChunkSize + 5 # (2 flags + 1 parity + 2 file ID)
    
	return godChunkSize + totalNumberOfChunksExceptGodChunk*totalTritsInRegularChunks
    
def estimateNoOfDNABasesUsedForGoldmanEncoding(fileSize):
	totalBytesAfterHuffmanEncoding = fileSize*5 
	totalBytesAfterAddingExtraInfo = totalBytesAfterHuffmanEncoding + 20 + 25  # 20 -> encoding length of data, 25 -> upper limit used for padding
	numberOfChunksAfterFourFoldRedundancy = max(int(math.ceil(totalBytesAfterAddingExtraInfo/25.0)) - 3,1)
	return numberOfChunksAfterFourFoldRedundancy*117;  # 117 DNA bases used per chunk at max
    
def estimateNoOfDNABasesUsedForEncoding(encodingType,pathToFile,fileSize):
	if encodingType == "Goldman":
		return  estimateNoOfDNABasesUsedForGoldmanEncoding(fileSize)
	elif encodingType == "Golay":
		return  estimateNoOfDNABasesUsedForGolayEncoding(pathToFile,fileSize)  
