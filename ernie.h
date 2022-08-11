typedef struct __attribute__((packed)) s_ernie_cmd {
    uint16_t id;
    uint8_t unk;
    uint16_t data_size;
    uint8_t data[64 - 5]; // last 2 bytes are the checksum
} s_ernie_cmd;

enum ERNIE_COMMANDS {
    ERNIE_CMD_GET_INFO = 0x101,
    ERNIE_CMD_UNK_UNLOCK_CMDx110 = 0x103,
    ERNIE_CMD_UNK_LOCK_CMDx110 = 0x104,
    ERNIE_CMD_GET_UNK_x106 = 0x106,
    ERNIE_CMD_SET_KEYXCG = 0x110
};

enum ERNIE_ERRORS {
    ERR_NO_ERR = 0, // command accepted/success
    ERR_UNKNOWN_CMD, // unknown, probably nonexisting command
    ERR_BAD_LENGTH,
    ERR_BAD_CHKSUM,
    ERR_NO_CRLF, // unsure, only trigger was no CRLF
    ERR_BAD_FORMAT, // unsure, only trigger was non-hex [0-9 | A-F] chars
    ERR_UNKNOWN_x10 = 0x10, // unknown
    ERR_BLOCKED_T1 = 0x20, // blocked by command pair x 103/104
    ERR_BAD_PARAMS = 0x32, // unknown, probably bad params
    ERR_UNKNOWN_x33, // unknown
    ERR_UNKNOWN_x40 = 0x40, // unknown
    ERR_UNKNOWN_x95 = 0x95, // unknown
};

/* existing CMDs returns with size 0:
0x100 - 0x00
0x101 - 0x00 payload some syscon/console info
0x102 - 0x32
0x103 - 0x00 [UNBLOCKS 0x110,0x120-0x121,0x141-0x147,0x150-0x157,0x160-0x163]
0x104 - 0x00 [BLOCKS 0x110,0x120-0x121,0x141-0x147,0x150-0x157,0x160-0x163]
0x105 - 0x33
0x106 - 0x00 payload 0400 (0x4)
0x107 - 0x00 payload some date string in hex, ex. 201312131552
0x108 - 0x33
0x109 - 0x33
0x110 - 0x00 keyxchange, payload varies
0x120 - 0x40
0x121 - 0x40
0x140 - 0x00 payload 5800050058000400
0x141-0x147 - 0x10
0x150 - 0x00 payload 090001AA00000000
0x151 - 0x95
0x152-0x156 - 0x10
0x157 - 0x95
0x160-0x163 - 0x10
*/
