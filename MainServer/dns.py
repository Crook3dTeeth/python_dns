import socket
import datetime
import select
import threading


# Global settings
ip = "192.168.2.51"
isRunning = 1 # best not to change, used for restarting and shutting down

# Debug
debug = True
errors = True
warnings = True
client_ip = True
website = True
cache_details = True
cache_entries = False

# Fileoutput (what to output)
file_output = True
file_errors = False
file_warnings = False
file_client = False
file_website = False
if file_output:
    date = datetime.datetime.now().strftime("%x-%X").replace(":", "-")
    file = open(date.replace("/", "-") + "logs.txt", "w")

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
    try:
        if file_output:
            file.write(datetime.datetime.now().strftime("X") + str(output) + "\n")
    except:
        print("ERROR: failed to write to output file")


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
                    current_count += 4
                    start_index += 4                    


        if headerData[1][0] & 128:
            current_count = 0
            while current_count < answers:
                # Name, type, class, TTL, length

                responseName = data[start_index: start_index + 2]
                responseType = data[start_index + 2: start_index + 4]
                responseClass = data[start_index + 4: start_index + 6]
                responseTTL = data[start_index + 6: start_index + 10]
                responseLength = data[start_index + 10: start_index + 12]

                answer = b''

                current_count += 1
                start_index += 12
                count = int(data[start_index])

                # small hack to fix start_index not actually being the start index

                if count == 0:
                    while count == 0 or count > int.from_bytes(responseLength, 'big'):
                        start_index += 1
                        count = int(data[start_index])

                while count > 0 and (start_index + count) < data_length:
                    start_index += 1
                    end_index = start_index

                    answer += data[start_index: start_index + count]

                    start_index += count
                    count = int(data[end_index + count])

                    if count != 0:
                        answer += b'.'
                    else:
                        responseData.append((answer, responseName, responseType, responseClass, responseTTL, responseLength))


        if file_output:
            if responseData != []:
                debugPrint(responseData)

        return (headerData, questionData, responseData)
    except:
        debugPrint("ERROR: failed to decode packet")


def recievePacket(data, addr, sock):
    """ Recieves info from the socket
    """

    if client_ip:
        debugPrint(addr)

    DNSData = DNSServerLookup(data, addr)
    decodedData = decode_packet(DNSData)
    decodedData2 = decode_packet(data)
    
    try:
        sock.sendto(DNSData, addr)
    except:
        if warnings:
            debugPrint("ERROR: failed to send to client")


def DNSServerLookup(data, addr, dns = '8.8.8.8'):
    """ Gets data from another dns server
    """
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        sock.sendto(data, (dns, 53))
        
        dnsResponse = select.select([sock], [], [], 5)
        
        if dnsResponse == []:
            if warnings:
                debugPrint("WARNING: DNS server query timeout")
        else:
            debugPrint("Successfully got DNS server response")
            DNSData, serverAddr = dnsResponse[0][0].recvfrom(512)
            
            return DNSData
            #print(DNSData.decode("hex"))
        
    except:
        debugPrint("ERROR: Failed to send request to dns server")


def commandLine(data):

    global isRunning

    while isRunning:
        keyPress = input("Press 'h' for commands")
        if keyPress == 'd':
            debugPrint(data.dns_table)
        elif keyPress == 'q':
            file.close()
            isRunning = False
        elif keyPress == 'r':
            isRunning = True
            debugPrint("restarting...")
        elif keyPress == 'h':
            pass

def main():
    """ Main loop"""
    global isRunning

    while isRunning > 0:
        isRunning = 2
        #cache
        dnsCache = dns_table()
        dnsServer = create_socket(ip)
        debugPrint("Socket Created")
        
        senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        debugPrint("Sender Socket Created")

        if debug:
            threading.Thread(target=commandLine, args=(dnsCache,)).start()

        debugPrint("Server Started")
        while isRunning == 2:
            recievedRequest = select.select([dnsServer], [], [])

            data, addr = dnsServer.recvfrom(1024)
            
            recievePacket(data, addr, dnsServer)

            # Threading later
            #threading.Thread(target=recievePacket, args=(data, addr)).start()
            #threading.Thread(target=mDNS, args=(ip)).start() # mDNS
            
        senderSocket.close()
        dnsServer.close()

        dnsCache.shutdown()


def test_func():
    pass
    data = b'`\x98\x81\x80\x00\x01\x00\x04\x00\x00\x00\x00\x04help\x05apple\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x05\x00\x01\x00\x00\x06\xa3\x00"\x04help\x0corigin-apple\x03com\x06akadns\x03net\x00\xc0,\x00\x05\x00\x01\x00\x00\x00\x1e\x00\x1c\x07help-ar\x05apple\x03com\x07edgekey\xc0I\xc0Z\x00\x05\x00\x01\x00\x00S\x8a\x00\x16\x06e11408\x01d\nakamaiedge\xc0I\xc0\x82\x00\x01\x00\x01\x00\x00\x00\x14\x00\x04hu\xf9K'
    data1 = b"\x0e8\x81\x80\x00\x01\x00\x03\x00\x00\x00\x00\x02xp\x0citunes-apple\x03com\x06akadns\x03net\x00\x00\x01\x00\x01\xc0\x0c\x00\x05\x00\x01\x00\x00\x00\xb8\x00\x17\x02xp\x05apple\x03com\x07edgekey\xc0'\xc0<\x00\x05\x00\x01\x00\x00L\x1a\x00\x19\x06e17437\x04dsct\nakamaiedge\xc0'\xc0_\x00\x01\x00\x01\x00\x00\x002\x00\x04hq\xba\xd9"
    decode_packet(data)

test_func()
#main()
