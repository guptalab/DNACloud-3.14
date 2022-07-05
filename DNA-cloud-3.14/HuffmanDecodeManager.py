"""
##########################################################################################
Improvised Version: DNA Cloud 3.14
Developers: Mihir Gohel, Natvar Prajapati, Shashank Upadhyay, Shivam Madlani, Vandan Bhuva
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file implements Huffman decoding useful in Goldman Decoding .
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""
import huffman
import os


class HuffmanDecodeManager(object):
    tritString = []
    currLenOfTritString = 0
    totalLenOfTritString = 0
    fileFinal = None
    startIndex = 0
    maxRAMCapacity = 500000

    def addTrit(self, trit):
        self.tritString.append(trit)
        self.currLenOfTritString = self.currLenOfTritString + 1
        self.countOfTrits = self.countOfTrits + 1
        global percentageCompleted1
        global fileLength1
        percentageCompleted1 = 50 + (self.countOfTrits*1.00/fileLength1)*50
        if self.countOfTrits % 1000 == 0:
            self.signalStatus.emit(str(int(percentageCompleted1)))
        if self.currLenOfTritString == 6:
            self.updateManager()

    def addString(self, string1):
        # string1 is b'trits' so decoded it to normal string containing trits
        newstring1 = string1.decode("utf-8")
        self.totalLenOfTritString = len(newstring1)

        for trit in newstring1:
            self.addTrit(trit)


    def readFromFile(self, fileIn, len12, fileLength2):
        global fileLength1
        fileLength1 = fileLength2
        CHUNK_SIZE = 10000000000
        currLen = 0
        while True:
            toRead = min(len12-currLen, CHUNK_SIZE)
            if toRead == 0:
                break
            currLen = currLen + toRead
            tritString1 = fileIn.read(currLen)
            if tritString1 is None:
                break
            else:
                self.addString(tritString1)
                return


    def updateManager(self):
        trit1 = ''.join(self.tritString[self.startIndex:])
        num1 = huffman.decode(trit1)

        if num1 == -1:

            num1 = huffman.decode(trit1[:-1])
            self.startIndex = self.startIndex + 5
            self.currLenOfTritString = 1
            self.totalLenOfTritString = self.totalLenOfTritString - 5
        else:
            self.startIndex = self.startIndex + 6
            self.currLenOfTritString = 0
            self.totalLenOfTritString = self.totalLenOfTritString - 6
        tempList = []
        if (self.totalLenOfTritString - 20 >= 0):
            tempList.append(num1)
            self.fileFinal.write(bytearray(tempList))

        if self.startIndex >= self.maxRAMCapacity:
            if self.currLenOfTritString == 1:
                self.tritString = self.tritString[-1:]
            else:
                self.tritString = []
            self.startIndex = 0


    def close(self):
        if self.currLenOfTritString != 0:
            self.updateManager()
        self.fileFinal.close()
        self.signalStatus.emit('100')
        

    def __init__(self, fileFinal1, signalStatus):
        self.fileFinal = fileFinal1
        self.tritString = []
        self.currLenOfTritString = 0
        self.startIndex = 0
        self.maxRAMCapacity = 500000
        self.signalStatus = signalStatus
        self.countOfTrits = 0
        huffman.setReverseHuffman()


fileLength1 = 0
percentageCompleted1 = 0
