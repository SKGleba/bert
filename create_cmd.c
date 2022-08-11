#include <stdio.h>
#include <stdint.h>
#include <string.h>
// #include "ernie.h" // comment for onlinegdb

typedef struct __attribute__((packed)) s_ernie_cmd {
    uint16_t id;
    uint8_t unk;
    uint16_t data_size;
    uint8_t data[64 - 5]; // last 2 bytes are the checksum
} s_ernie_cmd;

#define CMD_ID 0x110 // command id
#define DATA_LEN 40 // max 57
#define UNK_BYTE 0x00 // unknown third byte

// COMMAND_DATA
static uint8_t cmd_data[64 - 7] = {
    0x30,
    0x00,
    0x00,
    0x0E
};

int main() {
    uint8_t cmd[64];
    memset(cmd, 0, 64);

    s_ernie_cmd* ernie_cmd = (s_ernie_cmd*)cmd;

    ernie_cmd->id = CMD_ID; // called command
    ernie_cmd->unk = UNK_BYTE;
    ernie_cmd->data_size = (DATA_LEN * 2); // payload size * 2 (hex2ascii)

    memcpy(ernie_cmd->data, cmd_data, DATA_LEN); // payload

    // calculate the command checksum
    uint16_t chksum = 0;
    for (int i = 0; i < (5 + DATA_LEN); i++)
        chksum -= -cmd[i];
    *(uint16_t*)(ernie_cmd->data + DATA_LEN) = ~chksum;

    // print out the command
    for (int i = 0; i < DATA_LEN + 7; i++)
        printf("%02X", cmd[i]);

    return 0;
}

