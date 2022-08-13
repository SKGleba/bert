#!/usr/bin/env python3
'''

PSVita v2 Syscon JIG Client by Proxima (R)

'''
import sys, os, struct, code, binascii
import serial, time, re, math
from Crypto.Cipher import AES
import random


secret1data = {
    0x0: "80996FBBC8B4EBA30595F4D379A23BD0",
    0x1: "8C20B6FABD2236F772AA283B8C82B13E",
    0xB: "CF2E93E9F94E28CCA48026134C7C77CE",
    0xE: "AD2F322F4256C49D1848818F0FDD81BE",
    0xF: "C86B51FB019A207F32118E55462D5008"
}

secret2data = {
    0xF: "B01103B0623832D62540B56333D6E11D"
}

key1table = {
    0x0: "EF685D2E33C7D029A1A2EE646BE39D41",
    0x1: "87DC6ECFF1CA5D709B01AEF69EA6B283",
    0xB: "BB644721CB4C55072E83177BEB3BBEE9",
    0xE: "4ACE3A668AAEBB11793C432FB8A4CE88",
    0xF: "50E4C3A77264167C409C72A9B57A8609"
}

key2table = {
    0x0: "CE7867DE57575C008D998281E8DA5912",
    0x1: "51EB8DD39B0585CE915F3BFF609C9563",
    0xB: "DC6B6EE0F457DF0E7BAD1C5EA338027F",
    0xE: "1CBAE93DE883557C8AA14886786BE227",
    0xF: "9E34087C48985B4B351A63572D9B481B"
}

key3table = {
    0xF: "EBE3460D84A41754AC441368CF0200D8"
}


def read_all(port, size):
    data = b''
    while len(data) < size:
        data += port.read(size - len(data))
    assert len(data) == size
    return data

class JIGClient(object):
    def __init__(self, uart_port):
        self._port = serial.Serial(uart_port, baudrate=38400, timeout=0)

    def read_all(self, size):
        return read_all(self._port, size)

    def read_line(self, terminator=b'\n'):
        data = []
        c = b''
        while c != terminator:
            c = self.read_all(1)
            data.append(c)
        return b''.join(data)
 
    def checksum(self,s):
        csum=0
        for x in s:
            csum = (csum + x) & 0xFFFF
        return bytearray(int((~csum) & 0xFFFF).to_bytes(2,"little"))

    def get_resp(self):
        x= bytes.fromhex(self.read_line().decode("ascii"))
        return x

    def send_cmd(self, cmd):

        #cmd = cmd.encode('ascii')
        bcmd = cmd + self.checksum(cmd)
        #bcmd += ':{0:02X}\r\n'.format(self.checksum(cmd)).encode('ascii')
        uartcmd = bcmd.hex().upper() + "\r\n"
        print("SEND: " + uartcmd[0:-2])
        #print('send: {0}'.format(cmd[:-1].decode('ascii')))
        self._port.write(uartcmd.encode("ascii"))


client = JIGClient('COM6')

cmd = sys.argv[1]
if cmd == "unlock1":
    c = bytearray.fromhex("0301000000")
    client.send_cmd(c)
    response = client.get_resp()
    print("RESP: " + response.hex().upper())
 
elif cmd == "lock1":
    c = bytearray.fromhex("0401000000")
    client.send_cmd(c)
    response = client.get_resp()
    print("RESP: " + response.hex().upper())
   
elif cmd == "handshake":
    #                      0 1 2 3 4 5 6 7 8 9 A B C D E F 101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D
    #                      10010050003001000E00000000BABEF00DBEEFBABE000000000000000000000000000000000000000000000000
    c = bytearray.fromhex("100100500030000000000000000000000000000000000000000000000000000000000000000000000000000000")
    c[8] = 0xE
    client.send_cmd(c)
    response =client.get_resp()
    print("RESP: " + response.hex().upper())
    if response[2] != 0:
        print("ERROR: Bad Response (" + response[2].hex() + ")")
        exit(0)
    c[6] = 1
    c[0xD:0x15] = random.randbytes(8)
    # Send step 1 challenge
    client.send_cmd(c)
    response =client.get_resp()
    print("RESP: " + response.hex().upper())
    if response[2] != 0 or response[7] !=0:
        print("ERROR: Bad Response (" + response[2].hex() + "-" + response[7].hex() + ")")
        exit(0)

    payload = response[0xD:0x2D]
    
    shared_secret = bytes.fromhex(secret1data[c[8]])
    key1 = bytes.fromhex(key1table[c[8]])
    key2 = bytes.fromhex(key2table[c[8]])
    iv = bytes(0x10)
    plain = AES.new(key1, AES.MODE_CBC, iv).decrypt(payload)
    if plain[0x10:0x20] == shared_secret:
        handplain = plain[8:0x10] + plain[0:8] + iv
        handcrypt = AES.new(key2, AES.MODE_CBC, iv).encrypt(handplain)
        c[6] = 3
        c[0xD:0x2D] = handcrypt
        client.send_cmd(c)
        response =client.get_resp()
        print("RESP: " + response.hex().upper())
        if response[7] == 0 and response[6] == 0xFF:
            print("Successful Auth")
        else:
            print("ERROR: Failed Auth (" + response[2].hex() + "-" + response[6].hex() + "-"+ response[7].hex() + ")")
            
                
    else:
        print("ERROR: Invalid Handshake secret")

        
else:
    client.send_cmd(bytearray.fromhex(cmd))            
    response =client.get_resp()
    print("RESP: " + response.hex().upper())

