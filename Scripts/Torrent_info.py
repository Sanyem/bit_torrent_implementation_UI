import logging
class torrent_info(object):
    def __init__(self, path):
        import bencode
        from libs.utils import sha1_hash 
        with open(path, 'r') as file:
            contents = file.read()

        self.torrentFile = bencode.bdecode(contents)
        file1 = open("torrent_info.txt","w")
        file1.write(str(self.torrentFile))
        self.totalLength = 0
        self.pieceLength = self.torrentFile['info']['piece length']
        self.pieces = self.torrentFile['info']['pieces']
        self.info_hash = sha1_hash(str(
            bencode.bencode(self.torrentFile['info'])
        ))
        self.peer_id = self.generatePeerId()
        self.announceList = self.getTrackers()
        self.fileNames = []

        self.getFiles()

        if self.totalLength % self.pieceLength == 0:
            self.numberOfPieces = self.totalLength / self.pieceLength
        else:
            self.numberOfPieces = (self.totalLength / self.pieceLength) + 1

        logging.debug(self.announceList)
        logging.debug(self.fileNames)

        assert(self.totalLength > 0)
        assert(len(self.fileNames) > 0)

    def getFiles(self):
        import os
        root = self.torrentFile['info']['name']

        if 'files' in self.torrentFile['info']:
            if not os.path.exists(root):
                os.mkdir(root, 0766 )

            for file in self.torrentFile['info']['files']:
                pathFile = os.path.join(root, *file["path"])

                if not os.path.exists(os.path.dirname(pathFile)):
                    os.makedirs(os.path.dirname(pathFile))

                self.fileNames.append({"path": pathFile , "length": file["length"]})
                self.totalLength += file["length"]

        else:
            self.fileNames.append({"path": root , "length": self.torrentFile['info']['length']})
            self.totalLength = self.torrentFile['info']['length']

    def getTrackers(self):
        if 'announce-list' in self.torrentFile:
            return self.torrentFile['announce-list']
        else:
            return [[ self.torrentFile['announce'] ]]

    def generatePeerId(self):
        import time
        from libs.utils import sha1_hash 
        seed = str(time.time())
        return sha1_hash(seed)
