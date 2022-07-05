"""
##########################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file does four fold redundancy of chunks effectively managing the RAM.
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""

import random

from pkg_resources import FileMetadata
import ExtraModules

# Object that effectively manages RAM by addding bases to the file as soon as chunk is detected
# dnaBaseStr ---> our DNA encoded string
# currLenOfDNA ---> present length of DNA encoded
# chunkIndex ---> present chunkIndex
# fileID ---> represents ID of the file
# fileFinal ---> file Object for writing the final output
# startIndex ---> actual DNA encoded string is from startIndex to end of dnaBaseStr
# maxRamCapacity ---> as soon as dnaBaseStr length is more than maxRamCapacity it empties strings and adjust startIndex accordingly


class ChunkManager(object):
    dnaBaseStr = []
    currLenOfDNA = 0
    chunkIndex = 0
    fileID = ''
    fileFinal = None
    startIndex = 0
    maxRAMCapacity = 500000
    filedata = ''

    def addBase(self, base1):
        self.dnaBaseStr.append(base1)
        self.currLenOfDNA = self.currLenOfDNA + 1

        if self.currLenOfDNA == 100:
            self.updateManager()
            

    def addString(self, string1):
        for base in string1:
            self.addBase(base)


    def updateManager(self):
        currChunk = ''.join(self.dnaBaseStr[self.startIndex:])
        if (self.chunkIndex) % 2 != 0:
            currChunk = ExtraModules.reverseComplement(currChunk)

        i3 = ExtraModules.intToBase3(self.chunkIndex, 12)
        P = int(self.fileID[0]) + int(i3[0]) + int(i3[2]) + int(i3[4]) + int(i3[6]) + int(i3[8]) + int(i3[10])
        P = P % 3
        indexingInfo = self.fileID + i3 + str(P)
        encodedIndexInfo = ExtraModules.encodeSTR(indexingInfo, currChunk[-1])

        if currChunk[0] == 'A':
            startBase = 'T'
        elif currChunk[0] == 'T':
            startBase = 'A'
        else:
            randomNum = random.random()
            if randomNum > 0.5:
                startBase = 'A'
            else:
                startBase = 'T'

        if encodedIndexInfo[-1] == 'C':
            endBase = 'G'
        elif encodedIndexInfo[-1] == 'G':
            endBase = 'C'
        else:
            randomNum = random.random()
            if randomNum > 0.5:
                endBase = 'C'
            else:
                endBase = 'G'

        currChunk = startBase + currChunk + encodedIndexInfo + endBase

        self.chunkIndex = self.chunkIndex + 1
        self.startIndex = self.startIndex + 25
        self.currLenOfDNA = 75
        if self.startIndex >= self.maxRAMCapacity:
            self.dnaBaseStr = self.dnaBaseStr[self.startIndex:]
            self.startIndex = 0
        self.fileFinal.write(str(currChunk+'\n'))


    def close(self):
        if self.currLenOfDNA > 0:
            self.updateManager()
        if self.fileFinal is not None:
            self.fileFinal.seek(0,0)  # takes the cursor to the first column of first line
            self.fileFinal.write(str("Number of Chunks = " + str(self.chunkIndex + 1)))
            self.fileFinal.flush()
            self.fileFinal.close()


    def __init__(self, fileFinal1, fileID1):
        self.fileFinal = fileFinal1
        self.fileID = fileID1
        self.dnaBaseStr = []
        self.currLenOfDNA = 0
        self.chunkIndex = 0
        self.startIndex = 0
        self.maxRAMCapacity = 500000
