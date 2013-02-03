#! /usr/bin/env python
#-*- coding: utf-8 -*-

from rotor import *

class Enigma(object):
    """
    Represents an Enigma machine.
    """
    def __init__(self, ref, r3, r2, r1, setting='AAA', plugs = [], ringset=1):
        """
        Initialization of the Enigma machine.
        """
        self.reflector = ref
        self.rotor1 = r1
        self.rotor2 = r2
        self.rotor3 = r3

        self.rotor1.state = setting[0]
        self.rotor2.state = setting[1]
        self.rotor3.state = setting[2]
        self.reflector.state = 'A'
        self.ringset = ringset

        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alpha_out = [" "] * 26
        for i in range(len(alpha)):
            alpha_out[i] = alpha[i]
        for k,v in plugs:
            alpha_out[ord(k)-ord('A')] = v
            alpha_out[ord(v)-ord('A')] = k

        try:
            self.transtab = str.maketrans(alpha, "".join(alpha_out))
        except:
            # Python 2
            from string import maketrans
            self.transtab = maketrans(alpha,"".join(alpha_out))

    def encipher(self, plaintext_in):
        """
        Encrypt 'plaintext_in'.
        """
        ciphertext = ''
        plaintext_in_upper = plaintext_in.upper()
        plaintext = plaintext_in_upper.translate(self.transtab)
        for c in plaintext:
            if self.rotor2.is_in_turnover_pos():
                self.rotor2.notch()
                self.rotor3.notch()
            if self.rotor1.is_in_turnover_pos():
                self.rotor2.notch()

            self.rotor1.notch()

            if not c.isalpha():
                ciphertext += c
                continue
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
        """
        Pretty display.
        """
        return """
        Reflector: %s
        Rotor 1: %s
        Rotor 2: %s
        Rotor 3: %s""" % (self.reflector, self.r1, self.r2, self.r3)