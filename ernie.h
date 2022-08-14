typedef struct __attribute__((packed)) s_ernie_cmd {
    uint16_t id;
    uint8_t unk;
    uint16_t data_size;
    uint8_t data[64 - 5]; // last 2 bytes are the checksum
} s_ernie_cmd;

enum ERNIE_COMMANDS {
    ERNIE_CMD_UNK_x100 = 0x100,
    ERNIE_CMD_GET_INFO,
    ERNIE_CMD_UNLOCK_T1 = 0x103,
    ERNIE_CMD_LOCK_T1 = 0x104,
    ERNIE_CMD_GET_UNK_DATE = 0x107,
    ERNIE_CMD_UNLOCK_T8 = 0x110,
    ERNIE_CMD_UNLOCK_T4 = 0x900,
    ERNIE_CMD_LOCK_T4 = 0x901,
};

enum ERNIE_ERRORS {
    ERR_NO_ERR = 0, // command accepted/success
    ERR_UNKNOWN_CMD, // unknown, probably nonexisting command
    ERR_BAD_LENGTH,
    ERR_BAD_CHKSUM,
    ERR_NO_CRLF, // unsure, only trigger was no CRLF
    ERR_BAD_FORMAT, // unsure, only trigger was non-hex [0-9 | A-F] chars
    ERR_BLOCKED_T8 = 0x10, // blocked by command x 110
    ERR_BLOCKED_T8_2, // unknown, blocked by command x 110 ?
    ERR_BLOCKED_T1 = 0x20, // blocked by command pair x 103/104
    ERR_BAD_PARAMS = 0x32, // unknown, probably bad params
    ERR_UNKNOWN_x33, // unknown
    ERR_UNKNOWN_x40 = 0x40, // unknown
    ERR_UNKNOWN_x60 = 0x60, // unknown BUT gives payload (??)
    ERR_UNKNOWN_x92 = 0x92, // unknown
    ERR_UNKNOWN_x95 = 0x95, // unknown
    ERR_UNKNOWN_xA3 = 0xA3, // unknown
    ERR_UNKNOWN_xD0 = 0xD0, // unknown
    ERR_UNKNOWN_xD2 = 0xD2, // unknown
    ERR_UNKNOWN_xD8 = 0xD8, // unknown
    ERR_BLOCKED_T4 = 0xFF, // blocked by command pair x 900/901
};