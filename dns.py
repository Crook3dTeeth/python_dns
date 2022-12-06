import socket
import select
import threading

class hostname_table:
    def __init__(self, max_size):
        pass

    def find(self, item):
        pass

    def add(self, item):
        pass

    def delete(self, item):
        pass


def create_socket(UDP_IP, DNS_PORT = 43):
    """ Creates the socket for the DNS server
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, DNS_PORT))
    return sock

    
def decode_packet(data):
    """ Decodes the request packet
    """


def send_packet(sock, data):
    """ Sends data using the socket
    """


def table_lookup(query):
    """ Finds the lookup in the table
    """


def recievePacket(data, addr):
    """ Recieves info from the socket
    """

    print(addr)
    print(data)


def recieveLoop():
    """
    """


def sendLoop():
    """
    """


def main():
    """ Main recieve loop"""


    max_clients = 5

    dnsServer = create_socket("127.0.0.1")


    while True:
        recievedRequest = select.select([dnsServer], [], [])

        data, addr = dnsServer.recvfrom(1024)

        threading.Thread(target=recievePacket, args=(data, addr)).start()

main()