import datetime
import socket
import threading
import select
import time

class hostname_table:
    def __init__(self):
        self.data = 0


    def add(self):
        self.data = self.data + 1

    def printItem(self):
        print(str(self.data))



def main():

    test = b'0\xfc\x81\x80\x00\x01\x00\x03\x00\x00\x00\x00\x03www\tinstagram\x03com\x00\x00\x1c\x00\x01\xc0\x0c\x00\x05\x00\x01\x00\x00\r\x94\x00\n\x07geo-p42\xc0\x10\xc0/\x00\x05\x00\x01\x00\x00\r\x94\x00\x17\x0fz-p42-instagram\x04c10r\xc0\x10\xc0E\x00\x1c\x00\x01\x00\x00\x00\xb0\x00\x10*\x03(\x80\xf2a\x00\xe6\xfa\xce\xb0\x0c\x00\x00D '

    # Identification, flags, # questions, # answers RRs, # authority RRs, # additional RRs
    header_data = []
    # questions, answers, authority, additional information
    data = []

    

main()