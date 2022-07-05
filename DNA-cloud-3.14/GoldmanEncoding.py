"""
##########################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file implements Goldman Encoding.
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""

import huffman
import ChunkManager1
import ExtraModules
import io
import os

# Binary files to DNA String Convertor
# Input : fileName and fileID to be used
# Output : file converted to it's DNA string. To be later converted into chunks to get 4 fold redundancy
# Limitation: 3GB is the limitation


def file2DNA(fileName, fileId, signalStatus):
    totalLen = 0
    myFile = io.open(fileName, "rb")
    outFile = io.open(fileName+'.dnac', "w")
    outFile.write("                                              \n")  # writing a blank line in .dnac file so that .seek() function does not over-write the DNA string while writing number of chunks
    chunkManager = ChunkManager1.ChunkManager(outFile, fileId)
    prevBase = 'A'
    countOfBytes = 0
    while True:
        byte = myFile.read(1)
        countOfBytes = countOfBytes + 1
        global percentageCompleted
        global fileLength
        percentageCompleted = (countOfBytes*1.00/fileLength)*100
        if countOfBytes % 1000 == 0:
            signalStatus.emit(str(int(percentageCompleted)))
        if (not byte):
            break
        tritString = str(huffman.encode(byte))
        totalLen = totalLen + len(tritString)
        dnaString = ExtraModules.encodeSTR(tritString, prevBase)
        prevBase = dnaString[-1]

        chunkManager.addString(dnaString)
        

    S2 = ExtraModules.intToBase3(totalLen, 20)
    currLen = 20 + totalLen
    lenOfS3 = 25 - (currLen % 25)
    S3 = '0'*lenOfS3
    dnaString1 = ExtraModules.encodeSTR(S3+S2, prevBase)
    chunkManager.addString(dnaString1)
    chunkManager.close()
    signalStatus.emit('100')


def encodeFile(str1, signalStatus):
    global fileLength
    fileLength = os.path.getsize(str1)
    file2DNA(str1, '10', signalStatus)


fileLength = 0
percentageCompleted = 0
