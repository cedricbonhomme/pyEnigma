#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

from pyenigma.rotor import *
from pyenigma.enigma import *

class TestpyEnigma(unittest.TestCase):

    def setUp(self):
        self.rotors = { \
              "I":ROTOR_I,"II":ROTOR_II,"III":ROTOR_III,"IV":ROTOR_IV, \
              "V":ROTOR_V,"VI":ROTOR_VI,"VII":ROTOR_VII \
              }
        self.reflectors = { \
              "A":ROTOR_Reflector_A,"B":ROTOR_Reflector_B, \
              "C":ROTOR_Reflector_C \
              }

        self.key = 'ABC'
        self.ref = 'A'
        self.r1 = 'I'
        self.r2 = 'II'
        self.r3 = 'III'
        self.plugs = 'AV BS CG DL FU HZ IN KM OW RX'

    def test_encrypt(self):
        message = 'Hello World'

        engr = Enigma(self.reflectors[self.ref], self.rotors[self.r1],
                        self.rotors[self.r2], self.rotors[self.r3],
                        key=self.key, plugs=self.plugs)
        secret = engr.encipher(message)

        self.assertEqual(secret, 'Qgqop Vyzxp')


if __name__ == '__main__':
    unittest.main()
