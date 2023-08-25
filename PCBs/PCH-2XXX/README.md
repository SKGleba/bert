# PCH-2xxx-JIG-PCB
PCB for JIG on PCH-2xxx PSVITA


Nano 0805 footprint 

3.3V Version (on the 3.3V Version VCC on the vita side is left floating so you cannot charge the Vita while JIG is in use)
3.3V Version does not seem to work with FTDI UART when using the FTDI 3.3V module as a voltage input because it appears to output 3.172v rather than a true 3.3v
![image](https://github.com/SKGleba/bert/assets/203427/aff9ae14-e484-4940-955e-5edb9749dca3)


5V Version (a VCC line has been added for charging, I do not know if it works, it has not been tested; connecting VCC is optional)
Tested on FTDI UART module, resistor values still work when using the UART 5V as a power source despite only outputing 4.930v

![image](https://github.com/SKGleba/bert/assets/203427/8ee600c5-e941-4e15-a111-497439a45842)
