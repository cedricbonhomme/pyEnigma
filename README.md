pyEnigma
========

[![Build](https://img.shields.io/travis/cedricbonhomme/pyEnigma/master.svg?style=flat-square)](https://travis-ci.org/cedricbonhomme/pyEnigma)
[![Coverage](https://img.shields.io/coveralls/cedricbonhomme/pyEnigma/master.svg?style=flat-square)](https://coveralls.io/github/cedricbonhomme/pyEnigma?branch=master)


#### Python Enigma cypher machine simulator.

Presentation
------------
[pyEnigma](https://github.com/cedricbonhomme/pyEnigma) has been tested with Python 2 -> Python 3.3.


Installation
------------

    $ cd pyenigma
    $ sudo python setup.py install


Usage
-----

As a Python module:

    Python 3.5.2 (default, Oct 20 2016, 10:10:10)
    [GCC 6.2.0 20161005] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pyenigma import enigma
    >>> from pyenigma import rotor
    >>> print(rotor.ROTOR_GR_III)

        Name: III
        Model: German Railway (Rocket)
        Date: 7 February 1941
        Wiring: JVIUBHTCDYAKEQZPOSGXNRMWFL
    >>>
    >>> engr = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I, rotor.ROTOR_II, rotor.ROTOR_III, key="ABC", plugs="AV BS CG DL FU HZ IN KM OW RX")
    >>> print(engr)

        Reflector:
        Name: Reflector A
        Model: None
        Date: None
        Wiring: EJMZALYXVBWFCRQUONTSPIKHGD

        Rotor 1:
        Name: I
        Model: Enigma 1
        Date: 1930
        Wiring: EKMFLGDQVZNTOWYHXUSPAIBRCJ
        State: A

        Rotor 2:
        Name: II
        Model: Enigma 1
        Date: 1930
        Wiring: AJDKSIRUXBLHWTMCQGZNPYFVOE
        State: B

        Rotor 3:
        Name: III
        Model: Enigma 1
        Date: 1930
        Wiring: BDFHJLCPRTXVZNYEIWGAKMUSQO
        State: C
    >>> res = engr.encipher("Hello World")
    >>> print res
    Qgqop Vwoxn


Command line:

    $ echo "Hello World" | ./cypher_enigma_safe.py ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"
    Qgqop Vwoxn

    $ echo "Qgqop Vwoxn" | ./cypher_enigma_safe.py ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"
    Hello World


License
-------

pyEnigma is under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt) license.


Author
------

* [Christophe Goessen](https://bitbucket.org/azmaeve) (main author)
* [Cédric Bonhomme](https://www.cedricbonhomme.org)
