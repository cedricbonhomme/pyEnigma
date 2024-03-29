#!/usr/bin/env python
import sys

from pyenigma import enigma
from pyenigma import rotor

"""A trivial and minimaliste CLI.
"""


def usage():
    print("Usage:")
    print('\techo "Hello World" | enigma ABC ref rotor1 rotor2 rotor3 plugboard')
    print("\nExample:")
    print(
        '\t$ echo "Hello World" | enigma ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"'
    )
    print("\tQgqop Vyzxp")


def main():
    # Point of entry in execution mode
    try:
        key = sys.argv[1].upper()
        ref = sys.argv[2].upper()
        r1 = sys.argv[3].upper()
        r2 = sys.argv[4].upper()
        r3 = sys.argv[5].upper()
        plugs = sys.argv[6].upper()
        verbose = (sys.argv[7] if 7 < len(sys.argv) else "") in ["-v", "--verbose"]
    except Exception:
        usage()
        exit()
    raw = sys.stdin.read(-1)

    rotors = {
        "I": rotor.ROTOR_I,
        "II": rotor.ROTOR_II,
        "III": rotor.ROTOR_III,
        "IV": rotor.ROTOR_IV,
        "V": rotor.ROTOR_V,
        "VI": rotor.ROTOR_VI,
        "VII": rotor.ROTOR_VII,
    }
    reflectors = {
        "A": rotor.ROTOR_Reflector_A,
        "B": rotor.ROTOR_Reflector_B,
        "C": rotor.ROTOR_Reflector_C,
    }

    if len(key) == 3:  # add the default ringstellung
        key += "-AAA"

    engr = enigma.Enigma(
        reflectors[ref],
        rotors[r1],
        rotors[r2],
        rotors[r3],
        key=key[:3],
        plugs=plugs,
        ring=key[4:7],
    )
    res = engr.encipher(raw).strip()
    print(res)
    if verbose:
        print(
            '{}{}{} {} {} {} {} "{}"'.format(
                engr.rotor1.state,
                engr.rotor2.state,
                engr.rotor3.state,
                ref,
                r1,
                r2,
                r3,
                plugs,
            ),
            file=sys.stderr,
        )
