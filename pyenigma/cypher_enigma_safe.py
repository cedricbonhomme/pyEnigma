#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys

from rotor import *
from enigma import *

"""A trivial and minimaliste CLI.
"""

def usage():
    print("Usage:")
    print('\techo "Hello World" | ./cypher_enigma_safe.py ABC ref rotor1 rotor2 rotor3 plugboard')
    print("\nExample:")
    print('\t$ echo "Hello World" | ./cypher_enigma_safe.py ABC B  I II IV')
    print("\tIajfb Sqguz")

if __name__ == "__main__":
    # Point of entry in execution mode
    try:
        key = sys.argv[1]
        ref = sys.argv[2]
        r1 = sys.argv[3]
        r2 = sys.argv[4]
        r3 = sys.argv[5]
        plugs = sys.argv[6]
    except:
        usage()
        exit()
    raw = sys.stdin.read(-1)

    rotors = { \
          "I":ROTOR_I,"II":ROTOR_II,"III":ROTOR_III,"IV":ROTOR_IV, \
          "V":ROTOR_V,"VI":ROTOR_VI,"VII":ROTOR_VII \
          }
    reflectors = { \
          "A":ROTOR_Reflector_A,"B":ROTOR_Reflector_B, \
          "C":ROTOR_Reflector_C \
          }

    engr = Enigma(reflectors[ref], rotors[r1], rotors[r2], rotors[r3], key=key, plugs=plugs)
    res = engr.encipher(raw)
    print(res)
