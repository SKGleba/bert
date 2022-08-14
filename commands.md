## Command list tested with a live unit
### 0x0100
 - response: 0x00
### 0x0101 - get console info
 - response: 0x00
 - output: 3850800011050301030175008040327F
   - last 4 bytes are variable
### 0x0102
 - response: 0x00
 - input: unknown, ascii size 8 bytes
### 0x0103 - lock T1
 - response: 0x00
### 0x0104 - unlock T1
 - response: 0x00
### 0x0105
 - response: 0x00
 - input: unknown, min ascii size 2 bytes
   - 00 : resp 0x50
   - 02 : resp 0x00
   - 03 : resp 0x50
### 0x0106
 - response: 0x00
 - output: 0400
### 0x0107 - get date string
 - response: 0x00
 - output: 32303133313231333135353207000000000000000000000000000000
 - output hex2ascii : 201312131552
### 0x0108
 - response: 0x00
 - output: 100001C20000000020008043000000003000A90016045300310020050208A90040FFFFFF00000000
 - input: unknown, min ascii size 4 bytes
### 0x0109
 - response: 0x00
 - output: 0900040000000000320000000000000000000000000000000000000000000000
 - input: unknown, min ascii size 2 bytes
   - 00 : output 0900040000000000320000000000000000000000000000000000000000000000
   - 01 : output 0802020000000200610009020400000004003200000000000000000000000000
### 0x0110 - unlock T8 or T2
 - response: 0x00
 - input: 3-step handshake, ascii size 80 bytes
### 0x0120
 - response: 0x40
### 0x0121
 - response: 0x40
### 0x0131
 - auth level: T2
 - response: 0xA3
### 0x0132
 - auth level: T2
 - response: 0xA3
### 0x0140
 - response: 0x00
 - output: 5800050058000400
### 0x0141
 - response: 0x00
 - input: unknown, min ascii size 6 bytes
### 0x0142
 - response: 0xD0
### 0x0143
 - response: 0x00
### 0x0144
 - response: 0x00
### 0x0145
 - response: 0xD0
### 0x0146
 - response: 0x00
### 0x0147
 - response: 0x00
### 0x0150
 - response: 0x00
 - output: 0900001100000000
### 0x0151
 - response: 0x00
### 0x0152
 - response: 0x00
 - unlocks 0x155,0x156
### 0x0153
 - response: 0x00
 - output: 01AA0900
 - input: unknown, min ascii size 4 bytes
### 0x0154
 - response: 0x00
 - input: unknown, min ascii size 6 bytes
### 0x0155
 - response: 0x00
 - input: unknown, min ascii size 4 bytes
### 0x0156
 - response: 0x00
### 0x0157
 - response: 0x00
 - unlocks 0x155,0x156
### 0x0160
 - response: 0x33
### 0x0161
 - response: 0x00
 - causes ?soft reset?, UUU is sent again
### 0x0162
 - response: 0x00
 - causes ?soft reset?, UUU is sent again, faster than 0x162
### 0x0163
 - response: 0x33
### 0x0168
 - response: 0x00
 - output: 70033737
### 0x0170
 - response: 0x00
 - output: 01420000250000001B0CFFFFF8000F00000000000018
### 0x0171
 - response: 0x00
 - output: 8040327FFFFF61EDF4
   - output is variable
### 0x0172
 - response: 0x00
 - output: CC640500FFFFFFFF00
   - output is variable
### 0x0180
 - response: 0x00
 - output: 8607B70FF200F70056000000
### 0x0181
 - response: 0x00
 - output: 110080016201000000000000
### 0x0182
 - response: 0x00
 - causes ?soft reset?, UUU is sent again after a longer period (~6 seconds)
### 0x0183
 - response: 0x00
 - unlocks 0x184,0x185,0x186,0x187,0x188,0x189
### 0x0184
 - response: 0x00
### 0x0185
 - response: 0x33
### 0x0186
 - response: 0x00
### 0x0187
 - response: 0x33
### 0x0188
 - response: 0x00
### 0x0189
 - response: 0x00
### 0x018A
 - response: 0x00
 - output: 40000000
### 0x018B
 - response: 0x00
 - output: 01
### 0x018C
 - response: 0x00
 - output: 0C
### 0x018D
 - response: 0x00
 - output: 00
### 0x018E
 - response: 0x00
 - output: 01
### 0x0190
 - response: 0x00
 - output: 0100000000010000
### 0x01A0
 - response: 0x40
### 0x01A1
 - response: 0x40
### 0x01B0
 - response: 0x00
 - output: 0000000000000000
### 0x01C0
 - response: 0x00
 - output: 01550000
### 0x01C1
 - response: 0x00
### 0x01C2
 - response: 0x00
### 0x01C3
 - response: 0x00
 - unlocks 0x1C1,0x1C4
### 0x01C4
 - response: 0x00
 - output: 36300301FF000400
 - input: unknown, min ascii size 4 bytes
### 0x01D0
 - response: 0x98
### 0x01D1
 - response: 0x98
### 0x01D2
 - response: 0x00
 - output: 0000000000010000
### 0x0300 write to shared jig-kermit buffer
 - response: 0x00
 - input: message to kermit, max ascii size 80 bytes
 - sets some key
### 0x0301 read from jig-kermit shared buffer
 - response: 0x00
 - output: message from kermit, ascii size 80 bytes
### 0x0900 - unlock T4
 - response: 0x00
 - input: password, ascii size 32 bytes
### 0x0901 - lock T4
 - response: 0x00
### 0x0910
 - response: 0x33
### 0x0911
 - response: 0x33
### 0x0912
 - response: 0x33
### 0x0913
 - response: 0x33
### 0x0914
 - response: 0x33
### 0x0915
 - response: 0x33
### 0x0916
 - response: 0x00
 - output: 1B010600035402010100010000000000
### 0x0917
 - response: 0x00
 - output: 2D3A0543
### 0x0930
 - response: 0x00
 - output: 01C2
### 0x0931
 - response: 0x00
 - output: 8043
### 0x0932
 - response: 0x00
 - output: 2005A900160453000208A900
### 0x0940
 - response: 0x00
 - output: 0300
 - input: unknown
   - : output 05A9 resp 0x60
   - 00-03,08-0D,24,25,33-35,37,41,44,48 : output 0300
   - 04-07,0F-1F,36,38-3F : output 0400
   - 0E : output 0600
   - 20-22,40,43,46,47,49-4F : output 0200
   - 23,26-32,90-9F : output 0100
   - 42,71,72 : output 0004
   - 45 : output 0404
   - 50 : output 5541
   - 51,54 : output 4105
   - 52,55 : output 1000
   - 53 : output AA81
   - 56-5F,80,A0-A3,A5-A7,AA-B2,F0-FF : output 0000
   - 60-70 : output FFF0
   - 73 : output 0005
   - 74-7F : output 0101
   - 81 : output 1500
   - 82-85 : output 1700
   - 86-8F : output 0F00
   - B3-BF : output F000
   - A9,C0-CF : output 8000
   - D0-EF : output 01C2
### 0x0941
 - response: 0x00
 - input: unknown, min ascii size 2 bytes
 - writes somewhere or sets some flag for 0x942
### 0x0942
 - response: 0x00
 - input: unknown, min ascii size 2 bytes
 - output: 0000 unless written with 0x941, mashed with input
### 0x0943
 - response: 0x00
 - input: unknown, min ascii size 2 bytes
### 0x0944
 - response: 0x00
 - output: 9801
### 0x0945
 - response: 0x00
 - input: unknown, min ascii size 2 bytes
### 0x0952
 - response: 0x00
 - causes ?soft reset?, UUU is sent again after around 3s
### 0x0953
 - response: 0x00
 - output: 1C000000A60BA30B
### 0x0961
 - response: 0x00
 - output: 8080808080808080
### 0x0962
 - response: 0x00
 - output: 0080008000800080
### 0x0963
 - response: 0x00
 - output: 00000000000000000000000000000000
### 0x0964
 - response: 0x00
 - output: 0080008000800000008000800080000000800080008000000080008000800000
### 0x0965
 - response: 0x00
 - output: 0000C0FF0000C0FF0000C0FF0000C0FF


## Command list from syscon
<ID, OFFSET, AUTH>
<100h, sub_1E814, 0>                   
<101h, sub_1E830, 0>                   
<102h, sub_1E8B5, 0>                   
<103h, sub_1EA0C, 0>                   
<104h, sub_1EA3D, 0>                   
<105h, sub_1EA6E, 1>                   
<106h, sub_1EC2F, 0>                   
<107h, sub_1EC84, 0>                   
<108h, sub_1F43C, 0>                   
<109h, sub_1F4B2, 0>                   
<110h, do_handshake_0_1_E, 1>          
<120h, sub_1ED5F, 1>                   
<121h, sub_1EE1C, 1>                   
<131h, sub_1EFE9, 3>                   
<132h, sub_1F091, 3>                   
<140h, sub_1F2CE, 0>                   
<141h, sub_1F317, 9>                   
<142h, sub_1F541, 9>                   
<143h, sub_1F5E3, 9>                   
<144h, sub_1F624, 9>                   
<145h, sub_1F665, 9>                   
<146h, sub_1F6A6, 9>                   
<147h, sub_1F753, 9>                   
<148h, sub_1F801, 9>                   
<150h, sub_1FA55, 1>                   
<151h, sub_1FAB6, 1>                   
<152h, sub_1FAF0, 9>                   
<153h, sub_1FB29, 9>                   
<154h, sub_1FBC1, 9>                   
<155h, sub_1FC7E, 9>                   
<156h, sub_1FCD0, 9>                   
<157h, sub_1FD04, 1>                   
<160h, sub_1FD3E, 9>                   
<161h, sub_1FECC, 9>                   
<162h, sub_1FF00, 9>                   
<163h, sub_1FF2D, 9>                   
<168h, sub_1F3C2, 1>                   
<170h, sub_1F127, 9>                   
<171h, sub_1F916, 9>                   
<172h, sub_1F9BD, 9>                   
<180h, sub_1FF8E, 1>                   
<181h, sub_1FFC5, 9>                   
<182h, sub_1FFFC, 9>                   
<183h, sub_200A6, 9>                   
<184h, sub_200EE, 9>                   
<185h, sub_20136, 9>                   
<186h, sub_2017E, 9>                   
<187h, sub_201C6, 9>                   
<188h, sub_2020E, 9>                   
<189h, sub_20256, 9>                   
<18Ah, sub_2029E, 9>                   
<18Bh, sub_202CC, 9>                   
<18Ch, sub_202FA, 9>                   
<18Dh, sub_20328, 9>                   
<18Eh, sub_20356, 9>                   
<18Fh, sub_20384, 9>                   
<190h, sub_20033, 9>                   
<191h, sub_203F6, 9>                   
<192h, sub_20447, 9>                   
<1A0h, sub_2064C, 1>                   
<1A1h, sub_206D9, 1>                   
<1B0h, sub_20743, 1>                   
<1B2h, sub_20788, 9>                   
<1C0h, sub_207FA, 1>                   
<1C1h, sub_20884, 1>                   
<1C2h, sub_208B6, 1>                   
<1C3h, sub_208E8, 1>                   
<1C4h, sub_2091A, 1>                   
<1D0h, sub_209BA, 9>                   
<1D1h, sub_209D8, 9>                   
<1D2h, sub_1F3FF, 1>                   
<1D3h, sub_210E0, 9>                   
<1D4h, sub_210FE, 1>                   
<1D5h, sub_2111C, 9>                   
<1E0h, sub_2113A, 1>                   
<1E1h, sub_21171, 1>                   
<1E2h, sub_211C2, 1>                   
<1E3h, sub_211F9, 1>                   
<300h, sub_1F1AA, 0>                   
<301h, sub_1F1FF, 0>                   
<900h, sub_20A05, 0>  Send Passphrase? passphrase is: 93CE8EBEDF7F69A96F35DDE3BECB97D5                 
<901h, sub_20A69, 0>                   
<910h, sub_20A96, 4>                   
<911h, sub_20B22, 4>                   
<912h, sub_20B5B, 4>                   
<913h, sub_20BE7, 4>                   
<914h, sub_20C6C, 4>                   
<915h, sub_20CF8, 4>                   
<916h, sub_20D7E, 4>                   
<917h, sub_20DCE, 0Ch>                 
<930h, sub_20E33, 4>                   
<931h, sub_20E33, 4>                   
<932h, sub_20E33, 4>                   
<940h, sub_20E92, 0Ch>                 
<941h, sub_20F0C, 0Ch>                 
<942h, sub_20E92, 0Ch>                 
<943h, sub_20F0C, 0Ch>                 
<944h, sub_20E92, 0Ch>                 
<945h, sub_20F0C, 0Ch>                 
<952h, sub_20FBE, 0Ch>                 
<953h, sub_21019, 4>                   
<954h, sub_21050, 4>                   
<955h, sub_21098, 4>                   
<961h, sub_21220, 4>                   
<962h, sub_21275, 4>                   
<963h, sub_212C0, 4>                   
<964h, sub_2130C, 4>                   
<965h, sub_2147A, 4>                   
<967h, sub_214C6, 0Ch>                 
<968h, sub_21501, 0Ch>                 
<969h, sub_2153D, 0Ch>              
