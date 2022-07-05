# -*- coding: utf-8 -*-

"""
##########################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file implements Goldman decoding.
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""

import ExtraModules
import huffman
import io
import os
import HuffmanDecodeManager


def decode(filename, signalStatus):
    generateTrits(filename, signalStatus)
    huffmanDecode(filename, signalStatus)

    # first generate dna string out of the encoded file input


def generateTrits(filename, signalStatus):

    countOfBytes = 0
    chunkCount = 0
    with io.open(filename, "r") as fileToRead, io.open(filename[:-5]+'.temp', "w") as OutputFile:
        firstline = fileToRead.readline()    # reading the first line containing "Number of Chunks:" before reading DNA string
        first = True
        prevBase = 'A'
        rc = 1
        for chunk in fileToRead:
            chunkCount = chunkCount + 1
            countOfBytes = countOfBytes + len(chunk)
            global percentageCompleted
            global fileLength
            percentageCompleted = (countOfBytes*1.00/fileLength)*50
            if chunkCount % 1000 == 0:
                signalStatus.emit(str(int(percentageCompleted)))
            if chunk[0] == 'G' or chunk[0] == 'C':
                chunk = ExtraModules.reverseComplement(chunk)

            end = 25
            lengthOfChunk = len(chunk)

            if lengthOfChunk <= 117:
                end = (lengthOfChunk-18) % 25
                if end == 0:
                    end = 25
            temp = chunk[1:lengthOfChunk-17]

            if rc == 0:
                temp = ExtraModules.reverseComplement(temp)
            rc = rc ^ 1

            if first is False:
                OutputFile.write(str(getTrits(temp[-1*end:], prevBase)))
            else:
                first = False
                OutputFile.write(str(getTrits(temp, prevBase)))
            prevBase = temp[-1]


def getTrits(payload, prevBase):
    outputList = []

    for base in payload:
        if(prevBase != base):
            outputList.append(str(ExtraModules.diffEncDict[prevBase].index(base)))
        prevBase = base

    return ''.join(outputList)


def huffmanDecode(filename, signalStatus):
    tempfile = filename[:-5]+'.temp'
    with io.open(filename[:-5], "wb") as OutputFile, io.open(tempfile, "rb") as tempFileToRead:
        y = HuffmanDecodeManager.HuffmanDecodeManager(OutputFile, signalStatus)
        y.readFromFile(tempFileToRead, lengthfromS2(tempFileToRead), os.path.getsize(tempfile))
        y.close()
    os.remove(tempfile)


def lengthfromS2(tempFileToRead):
    tempFileToRead.seek(-20, os.SEEK_END)
    lenghtOfS1 = ExtraModules.base3ToInt(tempFileToRead.read())
    tempFileToRead.seek(0)
    return lenghtOfS1


def decodeFile(str1, signalStatus):
    global fileLength
    fileLength = os.path.getsize(str1)
    decode(str1, signalStatus)


fileLength = 0
percentageCompleted = 0
