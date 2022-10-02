#!/usr/bin/env python3
'''

PSVita v2 Syscon JIG Client by Proxima (R)

'''
import sys, os, struct, code, binascii
import serial, time, re, math
from Crypto.Cipher import AES
import random

DEFAULT_PORT = 'COM14'

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

CMD900_PWD = "93CE8EBEDF7F69A96F35DDE3BECB97D5"

def read_all(port, size):
    data = b''
    while len(data) < size:
        data += port.read(size - len(data))
    assert len(data) == size
    return data
    
def print_packet(pinfo, cmdp):
    print(pinfo + ": 0x" + cmdp[2:4] + cmdp[0:2] + " 0x" + cmdp[4:6] + " 0x" + cmdp[8:10] + cmdp[6:8] + " [ " + cmdp[10:-4] + " ] 0x" + cmdp[-2:] + cmdp[-4:-2])

class JIGClient(object):
    def __init__(self):
        self.is_open = False
        
    def open(self, uart_port, baud):
        if self.is_open == False:
            self._port = serial.Serial(uart_port, baudrate=baud, timeout=0)
            self.is_open = True
        
    def close(self):
        if self.is_open == True:
            self._port.close()
            self.is_open = False

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

    def send_cmd(self, cmd, loglevel):
        bcmd = cmd + self.checksum(cmd)
        uartcmd = bcmd.hex().upper() + "\r\n"
        if loglevel == 2:
            print_packet("SEND", uartcmd[:-2])
        elif loglevel == 1:
            print("SEND: " + uartcmd[0:-2])
        self._port.reset_input_buffer()
        self._port.reset_output_buffer()
        self._port.write(uartcmd.encode("ascii"))
        

client = JIGClient()

def cmd_x110(keyv):
    print("Starting 3Auth")
    #                      0 1 2 3 4 5 6 7 8 9 A B C D E F 101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D
    #                      10010050003001000E00000000BABEF00DBEEFBABE000000000000000000000000000000000000000000000000
    c = bytearray.fromhex("100100500030000000000000000000000000000000000000000000000000000000000000000000000000000000")
    c[8] = keyv
    client.send_cmd(c, 2)
    response =client.get_resp()
    print_packet("RESP", response.hex().upper())
    if response[2] != 0:
        print("ERROR: Bad Response (" + response[2].hex() + ")")
        exit(0)
    c[6] = 1
    c[0xD:0x15] = random.randbytes(8)
    # Send step 1 challenge
    client.send_cmd(c, 2)
    response =client.get_resp()
    print_packet("RESP", response.hex().upper())
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
        client.send_cmd(c, 2)
        response =client.get_resp()
        print_packet("RESP", response.hex().upper())
        if response[7] == 0 and response[6] == 0xFF:
            print("Successful 3Auth")
        else:
            print("ERROR: Failed 3Auth (" + response[2].hex() + "-" + response[6].hex() + "-"+ response[7].hex() + ")")
    else:
        print("ERROR: Invalid Handshake secret")

def send_simple_cmd(cmd_ascii):
    c = bytearray.fromhex(cmd_ascii)
    client.send_cmd(c, 2)
    response = client.get_resp()
    print_packet("RESP", response.hex().upper())
    

def test():
    for x in range(0, 0xB60, 0x20):
        cv_cmd = "3101000600" + "{:02X}".format(x & 0xFF) + "{:02X}".format((x & 0xFF00) // 0x100) + "20"
        client.send_cmd(bytearray.fromhex(cv_cmd), 0)
        response =client.get_resp()
        print(response.hex()[10:-4].upper())

def handle_cmd(user_cmd, argv):
    if client.is_open == False:
        client.open(DEFAULT_PORT, 38400)
    match user_cmd:
        case "raw":
            client.send_cmd(bytearray.fromhex(argv[2]), 1)           
            response = client.get_resp()
            print("RESP: " + response.hex().upper())
        case "test":
            test()
        case "nop":
            send_simple_cmd("0001000000")
        case "info":
            send_simple_cmd("0101000000")
        case "unlock-1":
            send_simple_cmd("0301000000")
        case "lock-1":
            send_simple_cmd("0401000000")
        case "power-get":
            send_simple_cmd("0601000000")
        case "power-off":
            send_simple_cmd("050100020000")
        case "power-on":
            send_simple_cmd("050100020002")
        case "power-sus":
            send_simple_cmd("050100020003")
        case "reset":
            client.send_cmd(bytearray.fromhex("6201000000"), 2)
        case "unlock-4":
            send_simple_cmd("0009002000" + CMD900_PWD)
        case "lock-4":
            send_simple_cmd("0109000000")
        case "handshake-E":
            cmd_x110(0xE)
        case "handshake-0":
            cmd_x110(0x0)
        case "handshake-1":
            cmd_x110(0x1)
        case "unlock-qa":
            handle_cmd("unlock-1", argv)
            handle_cmd("handshake-E", argv)
        case "unlock-nvs":
            handle_cmd("unlock-1", argv)
            handle_cmd("handshake-1", argv)
        case "unlock-sdboot":
            handle_cmd("unlock-1", argv)
            handle_cmd("handshake-0", argv)
        case "unlock-all":
            handle_cmd("unlock-1", argv)
            handle_cmd("handshake-E", argv)
            handle_cmd("handshake-1", argv)
            handle_cmd("handshake-0", argv)
            handle_cmd("unlock-4", argv)
        case "nvs-read":
            cv_cmd = "3101000600" + argv[2][4:6] + argv[2][2:4] + argv[3][2:4]
            client.send_cmd(bytearray.fromhex(cv_cmd), 0)
            response =client.get_resp()
            print(response.hex()[10:-4].upper())
        case "nvs-read-range":
            cv_bsz = int(argv[4][2:], 16)
            cv_argv = [""] * 4
            for x in range(int(argv[2][2:], 16), int(argv[3][2:], 16), cv_bsz):
                cv_argv[0] = "nvs-read-range"
                cv_argv[1] = "nvs-read"
                cv_argv[2] = "0x" + "{:04X}".format(x)
                cv_argv[3] = "0x" + "{:02X}".format(cv_bsz)
                handle_cmd(cv_argv[1], cv_argv)
        case "nvs-write":
            cv_cmd = "320100" + "{:02X}".format((int(argv[3][2:4], 16) * 2) + 6) + "00" + argv[2][4:6] + argv[2][2:4] + argv[3][2:4] + argv[4]
            client.send_cmd(bytearray.fromhex(cv_cmd), 0)
            response =client.get_resp()
            print(response.hex()[4:6].upper())
        case _:
            if user_cmd[:2] == "0x":
                cv_cmd = argv[1][4:6] + argv[1][2:4] + argv[2][2:4] + argv[3][4:6] + argv[3][2:4]
                if len(argv) >= 5:
                    cv_cmd += argv[4]
                return handle_cmd(cv_cmd, argv)
            else:
                send_simple_cmd(user_cmd)

def interactive():
    print("\nWelcome to interactive mode")
    print("use !help to display usage info")
    while 1:
        print("")
        uinput = input('> ')
        uinput_argv = uinput.split()
        uinput_argv.insert(0, "interactive")
        cmd = uinput_argv[1]
        match cmd:
            case "!exit":
                break
            case "!open":
                client.open(uinput_argv[2], int(uinput_argv[3]))
            case "!close":
                client.close()
            case "!wait":
                if client.is_open == True:
                    line = client.get_resp()
                    if len(uinput_argv) > 2:
                        print_packet("ERNIE", line.hex().upper())
                    else:
                        print("ERNIE: " + line.hex().upper())
                else:
                    print("port not open!")
            case _:
                handle_cmd(cmd, uinput_argv)
                

uinput_argv = sys.argv           
cmd = uinput_argv[1]

if cmd[:1] == "!":
    interactive()
else:
    handle_cmd(cmd, uinput_argv)
    
client.close()
    

#client.send_cmd(cmd)
#response = client.read_line()
#print(response.decode("ascii"), end ='')