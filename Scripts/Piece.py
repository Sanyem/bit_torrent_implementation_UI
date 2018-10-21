

BLOCK_SIZE = 2 ** 14

class Piece(object):
    def __init__(self, pieceIndex, pieceSize, pieceHash):
        import math
        self.pieceIndex = pieceIndex
        self.pieceSize = pieceSize
        self.pieceHash = pieceHash
        self.finished = False
        self.files = []
        self.pieceData = b""
        self.num_blocks = int(math.ceil( float(pieceSize) / BLOCK_SIZE))
        self.blocks = []
        self.initBlocks()

    def initBlocks(self):
        self.blocks = []

        if self.num_blocks > 1:
            for i in range(self.num_blocks):
                    self.blocks.append(["Free", BLOCK_SIZE, b"",0])

            # Last block of last piece, the special block
            if (self.pieceSize % BLOCK_SIZE) > 0:
                self.blocks[self.num_blocks-1][1] = self.pieceSize % BLOCK_SIZE

        else:
            self.blocks.append(["Free", int(self.pieceSize), b"",0])

    def setBlock(self, offset, data):
        if not self.finished:
            if offset == 0:
                index = 0
            else:
                index = offset / BLOCK_SIZE

            self.blocks[index][2] = data
            self.blocks[index][0] = "Full"

            self.isComplete()

    def getBlock(self, block_offset,block_length):
        return self.pieceData[block_offset:block_length]

    def getEmptyBlock(self):
        import time
        if not self.finished:
            blockIndex = 0
            for block in self.blocks:
                if block[0] == "Free":
                    block[0] = "Pending"
                    block[3] = int(time.time())
                    return self.pieceIndex, blockIndex * BLOCK_SIZE, block[1]
                blockIndex+=1

        return False

    def freeBlockLeft(self):
        for block in self.blocks:
            if block[0] == "Free":
                return True
        return False

    def isComplete(self):
        from pubsub import pub
        # If there is at least one block Free|Pending -> Piece not complete -> return false
        for block in self.blocks:
            if block[0] == "Free" or block[0] == "Pending":
                return False

        # Before returning True, we must check if hashes match
        data = self.assembleData()
        if self.isHashPieceCorrect(data):
            self.finished = True
            self.pieceData = data
            self.writeFilesOnDisk()
            pub.sendMessage('PiecesManager.PieceCompleted',pieceIndex=self.pieceIndex)
            return True

        else:
            return False

    def writeFunction(self,pathFile,data,offset):
        try:
            f = open(pathFile,'r+b')
        except IOError:
            f = open(pathFile,'wb')
        f.seek(offset)
        f.write(data)
        f.close()

    def writeFilesOnDisk(self):
        for file in self.files:
            pathFile = file["path"]
            fileOffset = file["fileOffset"]
            pieceOffset = file["pieceOffset"]
            length = file["length"]

            self.writeFunction(pathFile,self.pieceData[pieceOffset:pieceOffset+length],fileOffset)


    def assembleData(self):
        buf = b""
        for block in self.blocks:
            buf+=block[2]
        return buf

    def isHashPieceCorrect(self,data):
        import logging
        from libs import utils
        if utils.sha1_hash(data) == self.pieceHash:
            return True
        else:
            logging.warning("Error Piece Hash")
            logging.debug("{} : {}".format(utils.sha1_hash(data),self.pieceHash))
            self.initBlocks()
            return False