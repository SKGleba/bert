### ernie.h
c-style docs of ernie's side of things

### commands.md
jig->ernie commands docs

### bert.py
 - client for ernie via jig uart
 - requires pyserial, pycryptodome, python 3.10

### PCBs

Various JIGkick PCBs required to interface Ernie JIG interface. 
 - Supported models: Late DEM-3000/CEM-3000/PDEL-100X/PCH-1XXX/PCH-2XXX/VTE-1XXX
 - Use model specific 'Nano' design for a small footprint or to integrate into a cradle
 - Use MULTI (recommended) or SWITCH designs to support all existing models with a single board.
