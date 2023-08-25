# JIG MULTI SWITCH
PCB for JIG for PCH-100x, VTE-100x and PCH-200x PSVITA

This is an alternative design to the MULTI board which should be closer to what the Sony official JIG may have been like.
Unlike the MULTI board design, this design requires a switch to change between PCH-100X and PCH-200X JIG detect circuits.

* Currently supprorts PCH-1XXX/PDEL-100x, VTE-100x and PCH-2xxx PSVITA at both 3.3V and 5V
* 5V design requires the use of 0 ohms resistors or solder bridges (recommended)
Throughhole design only.

* * CAUTION (5V circuit only) Be aware that some UART modules advertised as 5V or with a jumper to 5V do NOT shift the power levels for UART TX/RX which will operate at 3.3V, Please measure voltage using a multimeter on your UART module between TX and GND, if it runs at 3.3V Replace R1 to a 1K ohms resistor in the 5V design.

![image](https://github.com/SKGleba/bert/assets/203427/16c58465-e892-4835-aa79-84ebeac5ab7d)

