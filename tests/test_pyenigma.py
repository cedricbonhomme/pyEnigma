#!/usr/bin/env python
# pyEnigma - Python Enigma cypher machine simulator.
# Copyright (C) 2010-2017
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2017/03/15 $"
__revision__ = "$Date: 2017/03/15 $"
__license__ = "GPLv3"

import unittest

from pyenigma.enigma import Enigma
from pyenigma.rotor import ROTOR_I
from pyenigma.rotor import ROTOR_II
from pyenigma.rotor import ROTOR_III
from pyenigma.rotor import ROTOR_IV
from pyenigma.rotor import ROTOR_Reflector_A
from pyenigma.rotor import ROTOR_Reflector_B
from pyenigma.rotor import ROTOR_Reflector_C
from pyenigma.rotor import ROTOR_V
from pyenigma.rotor import ROTOR_VI
from pyenigma.rotor import ROTOR_VII


class TestpyEnigma(unittest.TestCase):
    def setUp(self):
        self.rotors = {
            "I": ROTOR_I,
            "II": ROTOR_II,
            "III": ROTOR_III,
            "IV": ROTOR_IV,
            "V": ROTOR_V,
            "VI": ROTOR_VI,
            "VII": ROTOR_VII,
        }
        self.reflectors = {
            "A": ROTOR_Reflector_A,
            "B": ROTOR_Reflector_B,
            "C": ROTOR_Reflector_C,
        }

        self.key = "ABC"
        self.ref = "A"
        self.r1 = "I"
        self.r2 = "II"
        self.r3 = "III"
        self.plugs = "AV BS CG DL FU HZ IN KM OW RX"

    def test_encrypt(self):
        message = "Hello World"

        engr = Enigma(
            self.reflectors[self.ref],
            self.rotors[self.r1],
            self.rotors[self.r2],
            self.rotors[self.r3],
            key=self.key,
            plugs=self.plugs,
        )
        secret = engr.encipher(message)

        self.assertEqual(secret, "Qgqop Vyzxp")

    def test_turnover_matches_reference(self):
        # Regression for the rotor turnover timing (ticket #2): enciphering 26
        # 'A's with Walzenlage I-II-III (left to right), reflector B, ring AAA,
        # ground position AAA and no plugboard must match a standard Enigma.
        # This crosses the fast rotor's notch, which the old (off-by-one)
        # stepping mishandled.
        engr = Enigma(
            self.reflectors["B"],
            self.rotors["III"],  # rotor1 = fast / rightmost
            self.rotors["II"],  # rotor2 = middle
            self.rotors["I"],  # rotor3 = slow / leftmost
            key="AAA",
            plugs="",
        )
        secret = engr.encipher("A" * 26)

        self.assertEqual(secret, "BDZGOWCXLTKSBTMCDLPBMFQOFX")

    def test_double_step_matches_reference(self):
        # Regression for the double-stepping anomaly (ticket #2): when the
        # middle rotor sits on its notch, both the middle and the left rotor
        # advance. Ground position ADU drives the middle rotor (II, notch F)
        # through its notch within a 30-character message.
        engr = Enigma(
            self.reflectors["B"],
            self.rotors["III"],  # rotor1 = fast / rightmost, position U
            self.rotors["II"],  # rotor2 = middle, position D
            self.rotors["I"],  # rotor3 = slow / leftmost, position A
            key="UDA",
            plugs="",
        )
        secret = engr.encipher("A" * 30)

        self.assertEqual(secret, "EOEZIKERFPOZSVWHCCCKNEWZHKQQQC")

    def test_encrypt_length_changing_uppercase(self):
        # Regression: characters whose .upper() changes length (e.g. "ß" -> "SS")
        # used to raise IndexError / silently drop trailing enciphered characters
        # because case restoration assumed input and output had equal length.
        message = "Straße"

        engr = Enigma(
            self.reflectors[self.ref],
            self.rotors[self.r1],
            self.rotors[self.r2],
            self.rotors[self.r3],
            key=self.key,
            plugs=self.plugs,
        )
        secret = engr.encipher(message)

        # Output is full length (aligned with the uppercased input) and the
        # original case pattern is preserved across the expansion.
        self.assertEqual(secret, "Fphuagn")
        self.assertEqual(len(secret), len(message.upper()))
        self.assertEqual(secret[0], secret[0].upper())
        self.assertEqual(secret[1:], secret[1:].lower())


if __name__ == "__main__":
    unittest.main()
