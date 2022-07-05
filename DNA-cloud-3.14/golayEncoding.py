"""
##########################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This module encodes a file into DNA strands using Golay encoding.
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachiya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""

import io
import math
import os
import random

import GolayDictionary
import ExtraModules

# Input : Absolute Path Of A File
# Output : Name Of The File With Extension
def getFileNameWithExtensionFromPath(path):
    i = len(path) - 1
    while i>=0 :
        if path[i] == "\\" or path[i] =='/'  :
            break
        i = i - 1
    return path[i+1:]

# Input : File Name with extension eg. example.txt
# Output : Pair of fileName and its extension. eg ['example','txt']
# If no extension present then extension is set default to txt
def getFileNameAndExtension(fileNameWithExtension) :
    i = len(fileNameWithExtension) - 1
    while i>=0 :
      if fileNameWithExtension[i] == '.' :
        break
      i = i - 1
    if i==-1 :
      return fileNameWithExtension,'.txt'
    return fileNameWithExtension[:i],fileNameWithExtension[i+1:]

# Input : DNA Chunk
# Output : DNA Chunk with guard bases added to its beginning and end
def addGuardBases(chunk):
    if chunk[0] == 'A' :
        startBase = 'T'
    elif chunk[0] == 'T' :
        startBase = 'A'
    else :
        randomNum = random.random()
        if randomNum > 0.5:
          startBase = 'A'
        else:
          startBase = 'T'

    if chunk[-1] == 'C' :
        endBase = 'G'
    elif chunk[-1] == 'G' :
        endBase = 'C'
    else :
        randomNum = random.random()
        if randomNum > 0.5 :
          endBase = 'C'
        else:
          endBase = 'G'

    return startBase + chunk + endBase

# Input : String data for which parity trit to be generated
# Output : Sum of all odd trits modulo 3
def getParityTrit(data):
    lengthOfData = len(data)
    parity = 0
    for i in range(0,lengthOfData,2):
       parity = parity + int(data[i])
    parity = parity % 3
    return str(parity)

# fileIDInTrits : File ID that is to be encoded
# chunkIdInTrits : Chunk ID to identify the chunk
# prevBase : Used in relative encoding from trits to DNA bases
# Output : DNA Bases which encodes extra info needed for processing during decoding
def getExtraInfoInDNABases(fileIDInTrits,chunkIDInTrits,prevBase):
   parityInTrits = getParityTrit(chunkIDInTrits+fileIDInTrits)
   extraInfo = fileIDInTrits + chunkIDInTrits + parityInTrits
   return ExtraModules.encodeSTR(extraInfo,prevBase)

# Input : Size of the file  
# Output : The encoded trits for file size
def encodeFileSize(sizeOfTheFile):
    output = []
    while sizeOfTheFile!=0:
        output.append(GolayDictionary.encodeDirect((sizeOfTheFile%256)))
        sizeOfTheFile = sizeOfTheFile//256             
    return ''.join(output) 

maxNoOfFilesToBeEncodedInSingleFile = 9

# filePath : Absolute Path Of The File to be encoded
# fileId : ID of the file (to be used when two files are encoded into a single file)
# signalStatus : To be notified constantly about the progress of the encoding prodecure
def encode(filePath,fileId,signalStatus):
    global inputFiletemp, numberOfChunks
    inputFile = io.open(filePath,"rb")
    inputFiletemp = io.open(filePath, "rb")
    outputFile = io.open(filePath+'.dnac',"w")

    fileNameWithExtension = getFileNameWithExtensionFromPath(filePath)
    fileName,fileExtension = getFileNameAndExtension(fileNameWithExtension)
    
    global maxNoOfFilesToBeEncodedInSingleFile
    fileIdInTrits=ExtraModules.intToBase3(fileId, int(math.ceil( math.log(maxNoOfFilesToBeEncodedInSingleFile,3) )) )
    
    # calculating no of trits required for chunk ID (mu)
    fileLength= os.path.getsize(filePath)
    numberOfFileNameChunks = int(math.ceil(len(fileName) /9.0)) #divide by 9 because max 9 bytes in a chunk
    numberOfExtensionChunks = 1
    numberOfFileDataChunks = int(math.ceil(fileLength/9.0))
    numberOfChunks = numberOfFileNameChunks + numberOfExtensionChunks + numberOfFileDataChunks
    outputFile.write(str('Number of Chunks = ' + str(numberOfChunks) + '\n'))
    mu=int( math.ceil( math.log(numberOfChunks,3) ) ) #number of trits required to address chunk indices
   
    # creating the god chunk 
    noOfFileNameChunksInTrits = GolayDictionary.encodeDirect(numberOfFileNameChunks)
    noOfFileNameChunksInDNABases = ExtraModules.encodeSTR(noOfFileNameChunksInTrits,'A') 

    fileSizeInTrits = encodeFileSize(fileLength)
    noOfFileSizeTritsInTrits = ExtraModules.intToBase3(len(fileSizeInTrits)//11-1,2)
    noOfFileSizeTritsInDNABases = ExtraModules.encodeSTR(noOfFileSizeTritsInTrits,noOfFileNameChunksInDNABases[-1])

    maxRegularChunkSize = 1+99+len(fileIdInTrits)+mu+1+1
    howMuchToRepeat = int(math.ceil((maxRegularChunkSize*1.0)/len(fileSizeInTrits)))
    repeatedFileSizeTritsInDNABases = ExtraModules.encodeSTR(fileSizeInTrits*howMuchToRepeat ,noOfFileSizeTritsInDNABases[-1])
    godDataInDNABases = noOfFileNameChunksInDNABases + noOfFileSizeTritsInDNABases + repeatedFileSizeTritsInDNABases
    godChunk = addGuardBases(godDataInDNABases+getExtraInfoInDNABases(fileIdInTrits,"",godDataInDNABases[-1]))
    outputFile.write(str(godChunk+'\n'))
    
    # creating file extension chunk. There cannot be more than 9 characters in extension
    extensionInTrits = GolayDictionary.encodeSTR(fileExtension)
    extensionInDNABases = ExtraModules.encodeSTR(extensionInTrits,'A')
    chunkIDInTrits = '0'*mu
    extensionChunk = addGuardBases(extensionInDNABases+getExtraInfoInDNABases(fileIdInTrits,chunkIDInTrits,extensionInDNABases[-1]))
    outputFile.write(str(extensionChunk+'\n'))
    
    # creating file name chunks. 9 characters of file name in each file name chunk
    chunkIndex = 1
    for i in range(0,len(fileName),9):
        chunkIdinTrits = ExtraModules.intToBase3(chunkIndex,mu)
        fileNameInTrits = GolayDictionary.encodeSTR(fileName[i:i+9])
        fileNameInDNABases = ExtraModules.encodeSTR(fileNameInTrits,'A')
        fileNameChunk = addGuardBases(fileNameInDNABases+getExtraInfoInDNABases(fileIdInTrits,chunkIdinTrits,fileNameInDNABases[-1]))
        outputFile.write(str(fileNameChunk+'\n'))
        chunkIndex = chunkIndex + 1
    
    # creating chunks for actual file data
    prevBase = 'A'
    numberOfBytesEncoded = 0 # used for calculating percentage of work done to indicate progress via signal status
    numberOfChunksEncoded = 0

    while True:
        data = inputFile.read(9)
        if (not data):   # There are no bytes left in the file
            break
        # dataInTrits1 = GolayDictionary.encodeSTR(data)   #ORIGINAL
        dataInTrits = GolayDictionary.encodeSTRtemp()
        dataInDNABases = ExtraModules.encodeSTR(dataInTrits,prevBase) 
        prevBase = dataInDNABases[-1]

        chunkIndexInTrits = ExtraModules.intToBase3(chunkIndex,mu)
        payloadChunk = addGuardBases(dataInDNABases+getExtraInfoInDNABases(fileIdInTrits,chunkIndexInTrits,dataInDNABases[-1]))
        outputFile.write(str(payloadChunk+'\n'))

        chunkIndex = chunkIndex + 1
        numberOfBytesEncoded+=len(data)
        numberOfChunksEncoded = numberOfChunksEncoded + 1

        percentageCompleted = (numberOfBytesEncoded*1.00/fileLength)*100
        if(numberOfChunksEncoded%1000==0) :  # Send progress signal after every 1000 chunks encoded
           signalStatus.emit(str(int(percentageCompleted)))

    signalStatus.emit('100')  # completion of task signal.
    inputFile.close()
    inputFiletemp.close()

        
def encodeFile(filePath,signalStatus):
    fileID = 1
    encode(filePath,fileID,signalStatus)
