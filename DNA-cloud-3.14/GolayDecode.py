"""
##########################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file implements Golay decoding.
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""
import io
import GolayDictionary
import ExtraModules
import math
import BeforeGolayDecode
import os
# header Chunk = FLAG(1) + noOfChunksForFileName(1*11) + fileSize(variable) + FILEID(2) + PARITY(1) + FLAG(1)


def getDirectory(fileName):
    i = len(fileName) - 1
    while i >= 0:
        if fileName[i] == "\\" or fileName[i] == '/':
            break
        i = i - 1
    if i == -1:
        return ''
    return fileName[:i+1]


def decodeGolay(fileToRead, signalStatus):
    perDone = BeforeGolayDecode.refine(fileToRead, signalStatus)
    perLeft = 100 - perDone
    countOfBytes = 0  # for calculating percentage
    global percentageCompleted
    global fileLength
    fileToRead = fileToRead[0:-5]+'.temp'
    GolayDictionary.initDict()
    inputFile = io.open(fileToRead, "r")   # file object for .dnac file
    headerChunk = inputFile.readline()    # main chunk of .dnac file
    countOfBytes = countOfBytes + len(headerChunk)
    extensionChunk = inputFile.readline()  # extension chunk for file
    countOfBytes = countOfBytes + len(extensionChunk)
    noOfChunksForFileName = getChunksForFilename(headerChunk)
    # 2 for FILE ID + 1 for PARITY + 1 FOR FLAG + CHUNK ID SIZE + 1 for \n
    extraTrits = 2 + 1 + 1 + getNumberOfTritsForChunkID(headerChunk) + 1
    extension = '.' + getString(extensionChunk[1:-1*extraTrits])
    fileNameList = []
    for i in range(1, noOfChunksForFileName+1):
        fileNameChunk = inputFile.readline()
        countOfBytes = countOfBytes + len(fileNameChunk)
        fileNameList.append(getString(fileNameChunk[1:-1*extraTrits]))

    fileName = ''.join(fileNameList)
    # finalFileName = fileName + extension
    outputFile = io.open(fileToRead[:-5], "wb")  # decoded FILE object

    percentageCompleted = (countOfBytes*1.00/fileLength)*100
    countOfChunks = 0
    # maintaning previous base for differential decoding
    prevBase = 'A'
    for chunk in inputFile:
        countOfChunks = countOfChunks + 1
        countOfBytes = countOfBytes + len(chunk)
        percentageCompleted = perDone + (countOfBytes*1.00/fileLength)*perLeft
        if countOfChunks % 1000 == 0:
            signalStatus.emit(str(int(percentageCompleted)))
        data = chunk[1:-1*extraTrits]
        trits = ExtraModules.getTrits(data, prevBase)
        o = len(data)
        if o != 0:
            prevBase = data[-1]
        
        outputFile.write(bytearray(GolayDictionary.decodeSTR(trits)))
        
    signalStatus.emit('100')  # task completed
    inputFile.close()
    os.remove(fileToRead)


def getNumberOfTritsForChunkID(str1):
    return BeforeGolayDecode.mulength
    # noOfChunks =  getChunksForFilename(str1) + 1   # 1 for extension + n chunks for file name
    # noOfChunksForData = int(math.ceil(getSize(str1)/9))  # n chunks for actual data ceil((size/9))
    # print 'WHY? ',getSize(str1)
    # return int(math.ceil(math.log(noOfChunks + noOfChunksForData,3))) # taking log base 3 and then taking ceiling and taking int of it.


def getSize(str1):
    return getBase256Int(str1[12:-5], str1[11])   # 1 extra for \n


def getChunksForFilename(str1):
    return int(GolayDictionary.decode(ExtraModules.getTrits(str1[1:12], 'A')))


def getBase256Int(dnaString, prevBase):
    return ExtraModules.base256ToInt(GolayDictionary.decodeSTR(ExtraModules.getTrits(dnaString, prevBase)))


def getString(str1):
    byteArr = GolayDictionary.decodeSTR(ExtraModules.getTrits(str1, 'A'))
    list1 = []
    for byte in byteArr:
        list1.append(chr(byte))
    return ''.join(list1)


def decodeFile(str1, signalStatus):
    global fileLength
    fileLength = os.path.getsize(str1)  # gives size of specified path
    decodeGolay(str1, signalStatus)

fileLength = 0
percentageCompleted = 0