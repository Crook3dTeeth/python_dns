import socket
import datetime
import select
import threading


# Global settings
ip = "192.168.2.51"

# Debug
debug = True
errors = True
warnings = True
client_ip = True
website = True
cache_details = True
cache_entries = False

# Fileoutput (what to output)
file_output = False
file_errors = False
file_warnings = False
file_client = False
file_website = False

# Cahce settings
cache_output = True # saves the cache
cache_file_name = "" # File to save cache to
max_age = 10000 # seconds since last request
update_time = 100 #


class dns_table:
    def __init__(self):
        
        self.dns_table = {}

        # load data from file

    def find(self, name, data_type):
        if self.__contains_data__(name, data_type):
            data = self.dns_table[name][data_type]
            return data[0], data[1], data[2]
        else:
            return None

    def add(self, name, data_type, value, ttl):
        now = datetime.datetime.now()
        if not self.__contains_data__(name, data_type):
            if not self.__contains_name__(name):
                self.dns_table[name] = {}
                self.dns_table[name][data_type] = [value, ttl, now]
            else:
                self.dns_table[name][data_type] = [value, ttl, now]
        else:
            if self.dns_table[name][data_type][:2] != [value, ttl]:
                self.dns_table[name][data_type] = [value, ttl, now]

    def remove(self, name, data_type):
        self.dns_table.pop()

    def shutdown(self):
        pass

    def __contains_name__(self, name):
        if name in self.dns_table:
            return True
        else:
            return False

    def __contains_data__(self, name, data_type):
        if data_type in self.dns_table.get(name, {}):
            return True
        else:
            return False


def debugPrint(output):
    print(output)
    if file_output:
        pass


def create_socket(UDP_IP, DNS_PORT = 53):
    """ Creates the socket for the DNS server
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, DNS_PORT))
    return sock

    
def decode_packet(data):
    """ Decodes the request packet and creates a tuple of (identification, flags)
    """

    #packet info 
    
    # Identification, flags, # questions, # answers RRs, # authority RRs, # additional RRs
    try:
        questions = int.from_bytes(data[4:6], "big")
        answers = int.from_bytes(data[6:8], "big")
        authorityRR = int.from_bytes(data[8:10], "big")
        additionalRR = int.from_bytes(data[8:10], "big")

        headerData = [data[0:2], data[2:4], data[4:6], data[6:8], data[8:10], data[10:12]]
        questionData = []
        responseData = []

        # Queries 
        data_length = len(data)

        current_count = 0
        start_index = 13
        while current_count < questions:    
            count = int(data[12])
            query = b''

            while count > 0 and (start_index + count) < data_length:
                query += data[start_index: start_index + count]

                end_index = start_index
                start_index += count + 1
                count = int(data[end_index + count])
                if count != 0:
                    query += b'.'
                else:
                    # type and class 2 bytes
                    dataType = data[start_index: start_index + 2]
                    classData = data[start_index + 2: start_index + 4]

                    questionData.append((query, dataType, classData))
                    current_count += 1                    

        if headerData[1] & 128:
            current_count = 0
            while current_count < answers:
                # Name, type, class, TTL, length

                responseName = data[start_index: start_index + 2]
                responseType = data[start_index + 2: start_index + 4]
                responseClass = data[start_index + 4: start_index + 6]
                responseTTL = data[start_index + 6: start_index + 10]
                responseLength = data[start_index + 10: start_index + 12]



    
        

        return (headerData, questionData, responseData)
    except:
        print("ERROR: failed to decode packet")


def table_lookup(Name, Type):
    """ Finds the lookup in the table
    """

    dnsTable = ()

def recievePacket(data, addr, sock):
    """ Recieves info from the socket
    """

    if client_ip:
        print(addr)

    DNSData = DNSServerLookup(data, addr)
    decodedData = decode_packet(DNSData)
    
    try:
        sock.sendto(DNSData, addr)
    except:
        if warnings:
            print("ERROR: failed to send to client")


def DNSServerLookup(data, addr, dns = '8.8.8.8'):
    """ Gets data from another dns server
    """
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        sock.sendto(data, (dns, 53))
        
        dnsResponse = select.select([sock], [], [], 5)
        
        if dnsResponse == []:
            if warnings:
                print("WARNING: DNS server query timeout")
        else:
            print("Successfully got DNS server response")
            DNSData, serverAddr = dnsResponse[0][0].recvfrom(512)
            
            return DNSData
            #print(DNSData.decode("hex"))
        
    except:
        print("ERROR: Failed to send request to dns server")

def mDNS(ip):
    """ Used for mDNS
    """
    
    mDNSSock = create_socket(ip, 5353)


def cachePrint(data):

    while True:
        input("Press any key")

        print(data.dns_table)


def main():
    """ Main loop"""
    #cache
    dnsCache = dns_table()
    dnsServer = create_socket(ip)
    print("Socket Created")
    
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sender Socket Created")

    if debug:
        threading.Thread(target=cachePrint, args=(dnsCache,)).start()

    print("Server Started")
    while True:
        recievedRequest = select.select([dnsServer], [], [])

        data, addr = dnsServer.recvfrom(1024)
        
        recievePacket(data, addr, dnsServer)



        # Threading later
        #threading.Thread(target=recievePacket, args=(data, addr)).start()
        #threading.Thread(target=mDNS, args=(ip)).start() # mDNS
        

main()