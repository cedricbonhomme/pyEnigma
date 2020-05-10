#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pyenigma.rotor import *

class Enigma(object):
    """Represents an Enigma machine.
    Initializes an Enigma machine with these arguments:
    - ref: reflector;
    - r1, r2, r3: rotors;
    - key: initial state of rotors;
    - plus: plugboard settings.
    """
    def __init__(self, ref, r1, r2, r3, key="AAA", plugs="", ring="AAA"):
        """Initialization of the Enigma machine.
        """
        self.reflector = ref
        self.rotor1 = r1
        self.rotor2 = r2
        self.rotor3 = r3

        self.rotor1.state = key[0]
        self.rotor2.state = key[1]
        self.rotor3.state = key[2]
        self.rotor1.ring = ring[0]
        self.rotor2.ring = ring[1]
        self.rotor3.ring = ring[2]
        self.reflector.state = 'A'

        plugboard_settings= [(elem[0], elem[1]) for elem in plugs.split()]

        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alpha_out = [" "] * 26
        for i in range(len(alpha)):
            alpha_out[i] = alpha[i]
        for k, v in plugboard_settings:
            alpha_out[ord(k)-ord('A')] = v
            alpha_out[ord(v)-ord('A')] = k

        try:
            self.transtab = str.maketrans(alpha, "".join(alpha_out))
        except:
            # Python 2
            from string import maketrans
            self.transtab = maketrans(alpha,"".join(alpha_out))

    def encipher(self, plaintext_in):
        """Encrypt 'plaintext_in'.
        """
        ciphertext = ''
        plaintext_in_upper = plaintext_in.upper()
        plaintext = plaintext_in_upper.translate(self.transtab)
        for c in plaintext:

            # ignore non alphabetic char
            if not c.isalpha():
                ciphertext += c
                continue

            if self.rotor2.is_in_turnover_pos():
                self.rotor2.notch()
                self.rotor3.notch()
            if self.rotor1.is_in_turnover_pos():
                self.rotor2.notch()

            self.rotor1.notch()

            t = self.rotor1.encipher_right(c)
            t = self.rotor2.encipher_right(t)
            t = self.rotor3.encipher_right(t)
            t = self.reflector.encipher(t)
            t = self.rotor3.encipher_left(t)
            t = self.rotor2.encipher_left(t)
            t = self.rotor1.encipher_left(t)
            ciphertext += t

        res = ciphertext.translate(self.transtab)

        fres = ""
        for idx, char in enumerate(res):
            if plaintext_in[idx].islower():
                fres += char.lower()
            else:
                fres += char
        return fres

    def __str__(self):
        """Pretty display.
        """
        return """
        Reflector: %s

        Rotor 1: %s

        Rotor 2: %s

        Rotor 3: %s""" % (self.reflector, self.rotor1, self.rotor2, self.rotor3)
