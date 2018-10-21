import time
import Peer
from threading import Thread
from pubsub import pub


class Seek_torrent_peers(Thread):
    def __init__(self, queue_of_new_peers, torrent):
        Thread.__init__(self)
        self.queue_of_new_peers = queue_of_new_peers
        self.torrent_information = torrent
        self.peerFailed = [("","")]

    def run(self):
        while True:
            # TODO : if peerConnected == 50 sleep 50 seconds by adding new event, start,stop,slow ...
            peer = self.queue_of_new_peers.get()
            if not (peer[0],peer[1]) in self.peerFailed:
                p = Peer.Peer(self.torrent_information,peer[0],peer[1])
                if not p.connectToPeer(3):
                    self.peerFailed.append((peer[0],peer[1]))
                else:
                    pub.sendMessage('PeersManager.newPeer',peer=p)