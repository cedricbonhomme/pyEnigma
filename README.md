pyEnigma
========

#### Python Enigma cypher machine simulator.

Presentation
------------
Python 2 -> Python 3

Installation
------------

    $ cd pyenigma
    $ sudo python setup.py install

Usage
-----

As a Python module:

    Python 3.2.3 (default, Oct 19 2012, 19:53:16) 
    [GCC 4.7.2] on linux2
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

pyEnigma is under license.

Author
------
* [Christophe Goessen](https://bitbucket.org/azmaeve) (main author)
* [Cédric Bonhomme](http://cedricbonhomme.org/)
