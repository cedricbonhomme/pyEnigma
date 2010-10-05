from rotor import *
from enigma import *
import sys
"""
 A trivial and minimaliste CLI
"""

if __name__ == "__main__":
    key = sys.argv[1]
    ref = sys.argv[2]
    r1 = sys.argv[3]
    r2 = sys.argv[4]
    r3 = sys.argv[5]
    plugs_s = sys.argv[6]
    raw = sys.stdin.read(-1)
    seq = raw.upper()
    
    ct = 0
    a = None
    b = None
    plugs = []
    for c in plugs:
        if not c.isalpha():
            continue
        if ct == 0:
            a = c.upper()
            ct = 1
        else:
            b = c.upper()
            ct =0
            plugs.append((a,b))
            
    rotors = {"I":ROTOR_I,"II":ROTOR_II,"III":ROTOR_III,"IV":ROTOR_IV,"V":ROTOR_V,"VI":ROTOR_VI,"VII":ROTOR_VII}
    reflectors = {"A":ROTOR_Reflector_A,"B":ROTOR_Reflector_B,"C":ROTOR_Reflector_C}
    
    engr = Enigma(reflectors[ref], rotors[r1], rotors[r2], rotors[r3],key,plugs)
    res = engr.encipher(seq)
    i = 0
    fres = ""
    while i < len(res):
        if raw[i].islower():
            fres += res[i].lower()
        else:
            fres += res[i]
        
        i += 1
    print fres
