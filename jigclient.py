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

STATUS_CODES = {
    0x0 : "OK",
    0x1 : "UNK_CMD",
    0x2 : "BAD_LEN",
    0x3 : "BAD_CHKSUM",
    0x4 : "NO_CRLF",
    0x5 : "BAD_CMD_FORMAT",
    0x10 : "LOCKED_HANDSHAKE",
    0x20 : "LOCKED_T1",
    0x32 : "BAD_ARG_SIZE",
    0x33 : "BAD_ARG",
    0x40 : "WRONG_STATE",
}

def read_all(port, size):
    data = b''
    while len(data) < size:
        data += port.read(size - len(data))
    assert len(data) == size
    return data
    
silent_mode = 0
def print_packet(pinfo, cmdp, outbound):
    if silent_mode == 0:
        print(pinfo + ": 0x" + cmdp[2:4] + cmdp[0:2] + " 0x" + cmdp[8:10] + cmdp[6:8] + " [ " + cmdp[10:-4] + " ] 0x" + cmdp[-2:] + cmdp[-4:-2], end="")
    elif silent_mode == 1:
        if not outbound:
            print("-", end="")
        if cmdp[10:-4] != "":
            print(" [ " + cmdp[10:-4] + " ]", end="")
        else:
            print(" [ ]", end="")
    if silent_mode != 2:
        if not outbound:
            cv_status = int(cmdp[4:6], 16)
            if cv_status in STATUS_CODES:
                print(" <" + STATUS_CODES[cv_status] + ">", end="")
            else:
                print(" <0x" + "{:02X}".format(cv_status) + ">", end="")
        print("")
        

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
        if loglevel != 0 and silent_mode == 1:
            print("+", end="")
        if loglevel == 2:
            print_packet("SEND", uartcmd[:-2], True)
        elif loglevel == 1 and silent_mode != 2:
            if silent_mode == 1:
                print(uartcmd[0:-2])
            else:
                print("SEND: " + uartcmd[0:-2])
        self._port.reset_input_buffer()
        self._port.reset_output_buffer()
        self._port.write(uartcmd.encode("ascii"))
        

client = JIGClient()

def cmd_x110(keyv):
    if silent_mode != 2:
        print("Starting 3Auth")
    #                      0 1 2 3 4 5 6 7 8 9 A B C D E F 101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D
    #                      10010050003001000E00000000BABEF00DBEEFBABE000000000000000000000000000000000000000000000000
    c = bytearray.fromhex("100100500030000000000000000000000000000000000000000000000000000000000000000000000000000000")
    c[8] = keyv
    client.send_cmd(c, 2)
    response =client.get_resp()
    print_packet("RESP", response.hex().upper(), False)
    if response[2] != 0:
        if silent_mode != 2:
            print("ERROR: Bad Response (" + response[2].hex() + ")")
        exit(0)
    c[6] = 1
    c[0xD:0x15] = random.randbytes(8)
    # Send step 1 challenge
    client.send_cmd(c, 2)
    response =client.get_resp()
    print_packet("RESP", response.hex().upper(), False)
    if response[2] != 0 or response[7] !=0:
        if silent_mode != 2:
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
        print_packet("RESP", response.hex().upper(), False)
        if silent_mode != 2:
            if response[7] == 0 and response[6] == 0xFF:
                print("Successful 3Auth")
            else:
                print("ERROR: Failed 3Auth (" + response[2].hex() + "-" + response[6].hex() + "-"+ response[7].hex() + ")")
    elif silent_mode != 2:
        print("ERROR: Invalid Handshake secret")

def send_simple_cmd(cmd_ascii):
    c = bytearray.fromhex(cmd_ascii)
    client.send_cmd(c, 2)
    response = client.get_resp()
    print_packet("RESP", response.hex().upper(), False)
    

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
            if silent_mode == 0:
                print("RESP: " + response.hex().upper())
            elif silent_mode == 1:
                print("-" + response.hex().upper())
        case "test":
            test()
        case "nop":
            send_simple_cmd("0001000000")
        case "info":
            send_simple_cmd("0101000000")
        case "mode":
            send_simple_cmd("0201000800" + ("01" if argv[2] == "true" else "00") + ("01" if argv[3] == "true" else "00") + "0000")
        case "unlock-1":
            send_simple_cmd("0301000000")
        case "lock-1":
            send_simple_cmd("0401000000")
        case "power-off":
            send_simple_cmd("050100020000")
        case "power-on":
            send_simple_cmd("050100020002")
        case "power-fsm":
            send_simple_cmd("050100020003")
        case "get-power":
            client.send_cmd(bytearray.fromhex("0601000000"), 0)
            response =client.get_resp()
            if silent_mode != 2:
                match response.hex()[10:-4].upper():
                    case "0400":
                        print("STATE_OFF")
                    case "0800":
                        print("STATE_SUSPEND")
                    case "2000":
                        print("STATE_ON")
                    case _:
                        print("UNK STATE : " + response.hex()[10:-4].upper())
        case "handshake-0":
            cmd_x110(0x0)
        case "handshake-1":
            cmd_x110(0x1)
        case "handshake-E":
            cmd_x110(0xE)
        case "get-kr600":
            send_simple_cmd("2001000000")
        case "maika-0":
            send_simple_cmd("2101000400" + argv[2][4:6] + argv[2][2:4])
        case "nvs-read":
            cv_off = "0x{:04X}".format(int(argv[2][2:], 16))
            cv_sz = "0x{:02X}".format(int(argv[3][2:], 16))
            cv_cmd = "3101000600" + cv_off[4:6] + cv_off[2:4] + cv_sz[2:4]
            send_simple_cmd(cv_cmd)
        case "nvs-read-range":
            cv_bsz = int(argv[4][2:], 16)
            for x in range(int(argv[2][2:], 16), int(argv[3][2:], 16), cv_bsz):
                cv_off = "0x" + "{:04X}".format(x)
                cv_cmd = "3101000600" + cv_off[4:6] + cv_off[2:4] + "{:02X}".format(cv_bsz)
                client.send_cmd(bytearray.fromhex(cv_cmd), 0)
                response =client.get_resp()
                if silent_mode != 2:
                    print(response.hex()[10:-4].upper())
        case "nvs-write":
            cv_off = "0x{:04X}".format(int(argv[2][2:], 16))
            cv_sz = "0x{:02X}".format(int(argv[3][2:], 16))
            cv_cmd = "320100" + "{:02X}".format((int(cv_sz[2:4], 16) * 2) + 6) + "00" + cv_off[4:6] + cv_off[2:4] + cv_sz[2:4] + argv[4]
            send_simple_cmd(cv_cmd)
        case "confzz-read":
            cv_off = "0x{:04X}".format(int(argv[2][2:], 16))
            cv_sz = "0x{:02X}".format(int(argv[3][2:], 16))
            cv_cmd = "4101000600" + cv_off[4:6] + cv_off[2:4] + cv_sz[2:4]
            send_simple_cmd(cv_cmd)
        case "confzz-read-range":
            cv_bsz = int(argv[4][2:], 16)
            for x in range(int(argv[2][2:], 16), int(argv[3][2:], 16), cv_bsz):
                cv_off = "0x" + "{:04X}".format(x)
                cv_cmd = "4101000600" + cv_off[4:6] + cv_off[2:4] + "{:02X}".format(cv_bsz)
                client.send_cmd(bytearray.fromhex(cv_cmd), 0)
                response =client.get_resp()
                if silent_mode != 2:
                    print(response.hex()[10:-4].upper())
        case "confzz-write":
            cv_off = "0x{:04X}".format(int(argv[2][2:], 16))
            cv_sz = "0x{:02X}".format(int(argv[3][2:], 16))
            cv_cmd = "420100" + "{:02X}".format((int(cv_sz[2:4], 16) * 2) + 6) + "00" + cv_off[4:6] + cv_off[2:4] + cv_sz[2:4] + argv[4]
            client.send_cmd(bytearray.fromhex(cv_cmd), 0)
            response =client.get_resp()
            send_simple_cmd(cv_cmd)
        case "confzz-rw":
            send_simple_cmd("4301000000")
        case "confzz-ro":
            send_simple_cmd("4401000000")
        case "confzz-apply":
            send_simple_cmd("4501000000")
        case "invs-read-id":
            cv_id = "0x{:02X}".format(int(argv[2][2:], 16))
            cv_cmd = "5301000200" + cv_id[2:4] + "00"
            send_simple_cmd(cv_cmd)
        case "invs-read":
            cv_off = "0x{:04X}".format(int(argv[2][2:], 16))
            cv_sz = "0x{:02X}".format(int(argv[3][2:], 16))
            cv_cmd = "5401000600" + cv_off[4:6] + cv_off[2:4] + cv_sz[2:4]
            send_simple_cmd(cv_cmd)
        case "invs-read-range":
            cv_bsz = int(argv[4][2:], 16)
            for x in range(int(argv[2][2:], 16), int(argv[3][2:], 16), cv_bsz):
                cv_off = "0x" + "{:04X}".format(x)
                cv_cmd = "5401000600" + cv_off[4:6] + cv_off[2:4] + "{:02X}".format(cv_bsz)
                client.send_cmd(bytearray.fromhex(cv_cmd), 0)
                response =client.get_resp()
                if silent_mode != 2:
                    print(response.hex()[10:-4].upper())
        case "wipe-nvs":
            send_simple_cmd("600100020002")
        case "reset":
            send_simple_cmd("6101000000")
        case "reset-hard":
            send_simple_cmd("6201000000")
        case "kill":
            send_simple_cmd("63010002005A")
        case "reset-bic":
            send_simple_cmd("8201000000")
        case "unlock-4":
            send_simple_cmd("0009002000" + CMD900_PWD)
        case "lock-4":
            send_simple_cmd("0109000000")
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
        case _:
            if user_cmd[:2] == "0x":
                cv_user_cmd = "0x{:04X}".format(int(user_cmd[2:], 16))
                if len(argv) > 2:
                    cv_user_cmd_size = "0x{:04X}".format(int(argv[2][2:], 16))
                else:
                    cv_user_cmd_size = "0x0000"
                cv_cmd = cv_user_cmd[4:6] + cv_user_cmd[2:4] + "00" + cv_user_cmd_size[4:6] + cv_user_cmd_size[2:4]
                if len(argv) > 3:
                    cv_cmd += argv[3]
                return handle_cmd(cv_cmd, argv)
            else:
                try:
                    send_simple_cmd(user_cmd)
                except KeyboardInterrupt:
                    pass
                except:
                    print("command not found and/or malformed input")

def interactive():
    global silent_mode
    print("\nWelcome to interactive mode")
    print("use !help to display usage info")
    while 1:
        print("")
        uinput = input('> ')
        uinput_argv = uinput.split()
        uinput_argv.insert(0, "interactive")
        cmd = uinput_argv[1]
        match cmd:
            case "!help":
                helper(True, ">")
            case "!exit":
                break
            case "!open":
                try:
                    client.open(uinput_argv[2], int(uinput_argv[3]))
                except Exception as e:
                    print(e)
            case "!close":
                client.close()
            case "!wait":
                if client.is_open == True:
                    try:
                        line = client.get_resp()
                        if len(uinput_argv) > 2:
                            print_packet("ERNIE", line.hex().upper())
                        elif silent_mode != 2:
                            print("ERNIE: " + line.hex().upper())
                    except Exception as e:
                        print(e)
                    except KeyboardInterrupt:
                        pass
                else:
                    print("port not open!")
            case "!silent":
                if len(uinput_argv) == 2:
                    silent_mode = not silent_mode
                else:
                    silent_mode = int(uinput_argv[2])
            case _:
                try:
                    handle_cmd(cmd, uinput_argv)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print(e)
                
def helper(in_interactive, caller):
    print("ernie commands:")
    print(caller + " raw [COMMAND]                               : send a raw command, only adds checksum           : -----")
    print(caller + " nop                                         : ping ernie                                       : 0x100")
    print(caller + " mode [USE_FAST?] [USE_BIN?]                 : [true/false] 115200 and binary uart modes        : 0x102")
    print(caller + " info                                        : get hardware & ernie info                        : 0x101")
    print(caller + " get-date-string                             : get ernie firmware date string                   : 0x107")
    print(caller + " power-off / power-on / power-fsm            : set new power state                              : 0x105")
    print(caller + " get-power                                   : get current power state                          : 0x106")
    print(caller + " get-kr600                                   : read some ID with maika command 4, off 0x120     : 0x120")
    print(caller + " maika-0 [OFFu16]                            : read some data with maika command 0              : 0x121")
    print(caller + " nvs-read [OFFu16] [SIZEu8]                  : read nvs                                         : 0x131")
    print(caller + " nvs-read-range [OFFu16] [ENDu16] [STEPu8]   : read and print nvs in STEP-sized blocks          : -----")
    print(caller + " nvs-write [OFFu16] [SIZEu8] [DATA]          : write nvs                                        : 0x132")
    print(caller + " confzz-ro / confzz-rw                       : block/allow confzz writes                        : 0x144 / 0x143")
    print(caller + " confzz-read [OFFu16] [SIZEu8]               : read confzz                                      : 0x141")
    print(caller + " confzz-read-range [OFFu16] [ENDu16] [STEPu8]: read and print confzz in STEP-sized blocks       : -----")
    print(caller + " confzz-write [OFFu16] [SIZEu8] [DATA]       : write backup confzz                              : 0x142")
    print(caller + " confzz-apply                                : write backup confzz to main confzz               : 0x145")
    print(caller + " invs-read [OFFu16] [SIZEu8]                 : read internal nvs                                : 0x154")
    print(caller + " invs-read-id [IDu8]                         : read internal nvs by id                          : 0x153")
    print(caller + " invs-read-range [OFFu16] [ENDu16] [STEPu8]  : read and print internal nvs in STEP-sized blocks : -----")
    print(caller + " wipe-nvs                                    : wipe NVS with 0xFF                               : 0x160")
    print(caller + " reset / reset-hard                          : soft-reset / hard reset ernie                    : 0x161 / 0x162")
    print(caller + " kill                                        : full, hard shutdown of all components            : 0x163")
    print(caller + " reset-bic                                   : reset the battery controller                     : 0x182")
    print(caller + " unlock-1 / lock-1                           : un/lock the T1 lock                              : 0x104 / 0x103")
    print(caller + " unlock-4 / lock-4                           : un/lock the T4 lock with a passcode              : 0x900 / 0x901")
    print(caller + " handshake-0 / handshake-1 / handshake-E     : authenticate with the selected keyset            : 0x110")
    print(caller + " unlock-qa                                   : unlock the T1 and T8 locks                       : 0x103 + 0x110 (E)")
    print(caller + " unlock-nvs                                  : unlock the T1 and T2 locks                       : 0x103 + 0x110 (1)")
    print(caller + " unlock-sdboot                               : unlock the T1 lock and boot into SD mode         : 0x103 + 0x110 (0)")
    print(caller + " unlock-all                                  : unlock 1,4,qa,nvs,sdboot                         : -----")
    print(caller + " [COMMANDu16] <SIZEu16> <DATA>               : execute a command, e.g. '0x105 0x2 03'           : -----")
    
    print("")
    if in_interactive:
        print("client commands:")
        print(caller + " !exit                                       : exit the client")
        print(caller + " !open [PORT] [BAUDRATE]                     : open & use PORT")
        print(caller + " !close                                      : close currently used port")
        print(caller + " !wait                                       : wait for ernie to send something")
        print(caller + " !silent                                     : toggle verbose level, argument '2' sets level to none")
    else:
        print("client commands:")
        print(caller + " !i                                          : enter an interactive session")

uinput_argv = sys.argv

if len(uinput_argv) == 1:
    helper(False, uinput_argv[0])
    exit(0)
       
cmd = uinput_argv[1]

if cmd[:1] == "!":
    interactive()
else:
    try:
        handle_cmd(cmd, uinput_argv)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    
client.close()
    

#client.send_cmd(cmd)
#response = client.read_line()
#print(response.decode("ascii"), end ='')