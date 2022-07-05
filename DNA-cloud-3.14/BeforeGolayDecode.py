"""
#######################################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file sorts out unsorted chunks according to their chunk ID. It also calculates chunk ID length(mu).
#######################################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
#######################################################################################################
"""

from functools import *
import functools
from importlib.metadata import files
from importlib.resources import read_binary
import io
import math
import ExtraModules
import os
import GolayDictionary

""" Number of irregular chunks dont exceed 4 in the worst case so we can sample some chunks until we get a chunklength which has occured at least 7 times. By this we will be able to calculate "mu" which is the chunkID size. """
""" Regular chunk consists: 1(Guard Trit) + 99(Payload Maximum) + TritForfileID(Depends on number of files but will be known probably written on the testtube) + muTrits(number of trits for chunkID, the only unknown before) + 1(parity) + 1(\n). """
""" If file size greater than 2000 then we can do this sampling heuristic to reduce time to find the GOD chunk, which is the largest otherwise do linear search to find the same till the end. This is the key to start decoding process further """
# Assumptions: We know the trits required for fileID as we know how many files are stored together.

fileIdTrits = 2  # default to support upto 9 files
regularChunkSize = 0
mulength = 0
#
#	Chunk architecture of GOD chunk:
#					 guard trit
#					 11 trits (1 byte) to get number of file name chunks
#					 2 trits to get maximum number of bytes which is required to store file size. (range =0 to 8, but interpretation 1 to 9)
#					 next trits ( no of bytes for filesize * 11 * x, x is the minimum no such that god chunk size becomes greater than regular chunk size)
#					 fileid trits
#					 parity trit
#					 guard trit


def getChunkId(string):
    global mulength
    # 1(newline) + 1(guard) + 1(parity) + chunkid
    beginningOfChunkIdFromEnd = 1+1+1+mulength
    te = ExtraModules.getTrits(string[-1*beginningOfChunkIdFromEnd:-3], string[-1 * (beginningOfChunkIdFromEnd + 1)])
    ans1 = ExtraModules.base3ToInt(te)
    return ans1


count1 = 0


def compare_chunks(a, b):
    global numberOfTimesComparatorCalled
    global estimatedTime
    global signalStatus

    numberOfTimesComparatorCalled = numberOfTimesComparatorCalled + 1
    numberOfTimesComparatorCalled = min(numberOfTimesComparatorCalled, estimatedTime)
    percentageCompleted = int((numberOfTimesComparatorCalled*1.00/(estimatedTime))*60)
    if numberOfTimesComparatorCalled % 100 == 0:
        signalStatus.emit(str(int(percentageCompleted)))

    global regularChunkSize
    if len(a) > regularChunkSize:  # can be Godchunk, remember it has no chunk id
        return -1
    if len(b) > regularChunkSize:  # can be Godchunk, remember it has no chunk id
        return 1

    if a[0] == 'G' or a[0] == 'C':
        a = ExtraModules.reverseComplement(a)
        if b[0] == 'G' or b[0] == 'C':
            b = ExtraModules.reverseComplement(b)

        a_chunkId = getChunkId(a)
        b_chunkId = getChunkId(b)

        return a_chunkId - b_chunkId
    return numberOfTimesComparatorCalled


def findChunkIdLength(fileToRead):
    fileSize = os.stat(fileToRead).st_size     # gives size of specified path
    inputFile = io.open(fileToRead, "r")       

    global mulength, fileIdTrits, regularChunkSize
    mulength = 0
    GodChunk = ''

    if fileSize >= 2000:  # Apply Heuristic only when fileSize is >= 2000 bytes
        sizeDictionary = dict()
        regularChunkSize = 0
        i=0  
        for chunk in inputFile:
            if i==0:   # chunk for i=0 is the "Number of Chunks:" line
                pass
            chunklength = len(chunk)
            if sizeDictionary.get(chunklength) == None:
                sizeDictionary[chunklength] = 1
                i=i+1
            else:
                sizeDictionary[chunklength] = sizeDictionary[chunklength] + 1
                i=i+1
            if sizeDictionary[chunklength] == 7:
                regularChunkSize1 = chunklength
                i=i+1
                break
        mulength = regularChunkSize1 - (1 + 99 + fileIdTrits + 1 + 1 + 1)
        regularChunkSize = regularChunkSize

    else:
        GodChunk = inputFile.readline()
        GodChunk = inputFile.readline() #Updated GodChunk to next line because first line contains number of chunks


        numberOfFileNameChunks = ExtraModules.base256ToInt(GolayDictionary.decodeSTR(ExtraModules.getTrits(GodChunk[1:12], 'A')))
        noOfBytesForSize = ExtraModules.base3ToInt((ExtraModules.getTrits(GodChunk[12:14], GodChunk[11]))) + 1
        readTrits = noOfBytesForSize*11
        tempR = ExtraModules.getTrits(GodChunk[14:14+readTrits], GodChunk[13])
        filelength = ExtraModules.base256ToInt(GolayDictionary.decodeSTR(tempR))
        # ceil apparently gives real number and not int
        numberOfChunks = int(math.ceil(filelength/9.0) + numberOfFileNameChunks + 1.0)
        # number of trits required to address chunk indices
        mulength = int(math.ceil(math.log(numberOfChunks, 3)))

    inputFile.close()
    return mulength


estimatedTime = 0
numberOfTimesComparatorCalled = 0
signalStatus = None


def refine(filename, signalStatus1):
    GolayDictionary.initDict()
    global regularChunkSize, mulength, fileIdTrits, signalStatus
    mulength = findChunkIdLength(filename)
    signalStatus = signalStatus1

    # new line character included
    regularChunkSize = mulength + (1 + 99 + fileIdTrits + 1 + 1 + 1)
    with io.open(filename, "r") as fileToRead, io.open(filename[:-5]+'.temp', "w") as OutputFile:
        fileToRead = io.open(filename, 'r')
        chunks = fileToRead.readlines()
        chunks = chunks[1:]   # to remove the first line of .dnac file 
        global estimatedTime
        estimatedTime = len(chunks)*math.ceil(math.log(len(chunks), 2))
        for chunk in chunks:
            if chunk[0] == 'G' or chunk[0] == 'C':
                chunk = ExtraModules.reverseComplement(chunk)
            OutputFile.write(chunk)
        return int((numberOfTimesComparatorCalled*1.00/(estimatedTime))*60)
