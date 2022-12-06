import datetime
import socket
import select

class hostname_table:
    def __init__(self, fileOutput, max_size, max_load = 0.5):
        self.data = []
        self.length = 0
        self.max_size = max_size
        self.fileOutput = fileOutput

    def find(self, item):
        pass

    def add(self, item):
        pass

    def delete(self, item):
        pass


def simple_proxy():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((234, "127.0.0.1"))


def main():
    size = 10000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 4353))

    sock.sendto(b'test', ("103.20.139.207", 234))
    #dtResponse = select.select([sock], [], [])

    #data, adr = dtResponse[0][0].recvfrom(1024)



    print()

main()