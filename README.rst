pyEnigma
========

.. image:: https://img.shields.io/pypi/pyversions/pyenigma.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pyenigma

.. image:: https://img.shields.io/pypi/v/pyenigma.svg?style=flat-square
    :target: https://github.com/cedricbonhomme/pyenigma/releases/latest

.. image:: https://img.shields.io/pypi/l/pyenigma.svg?style=flat-square
    :target: https://www.gnu.org/licenses/gpl-3.0.html

.. image:: https://img.shields.io/travis/cedricbonhomme/pyEnigma/master.svg?style=flat-square
    :target: https://travis-ci.org/cedricbonhomme/pyEnigma

.. image:: https://img.shields.io/coveralls/cedricbonhomme/pyEnigma/master.svg?style=flat-square
   :target: https://coveralls.io/github/cedricbonhomme/pyEnigma?branch=master


`pyEnigma <https://github.com/cedricbonhomme/pyEnigma>`_, a  Python Enigma
cypher machine simulator.


Usage
-----

As a Python library
'''''''''''''''''''

.. code:: bash

    $ pipenv install pyenigma
    ✨ 🐍✨


.. code:: python

    Python 3.6.4 (default, Feb 23 2018, 13:45:58)
    [GCC 7.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pyenigma import enigma
    >>> from pyenigma import rotor
    >>> print(rotor.ROTOR_GR_III)

        Name: III
        Model: German Railway (Rocket)
        Date: 7 February 1941
        Wiring: JVIUBHTCDYAKEQZPOSGXNRMWFL
    >>>
    >>> engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                                    rotor.ROTOR_II, rotor.ROTOR_III, key="ABC",
                                    plugs="AV BS CG DL FU HZ IN KM OW RX")
    >>> print(engine)

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
    >>> secret = engine.encipher("Hello World")
    >>> print(secret)
    Qgqop Vwoxn


As a program
''''''''''''

.. code:: bash

    $ pipsi install pyenigma
    ✨ 🍰✨


.. code:: bash

    $ echo "Hello World" | enigma ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"
    Qgqop Vwoxn

    $ echo "Qgqop Vwoxn" | enigma ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"
    Hello World


License
-------

pyEnigma is under `GPLv3 <http://www.gnu.org/licenses/gpl-3.0.txt>`_ license.


Author
------

* `Christophe Goessen <https://github.com/cgoessen>`_ (initial author)
* `Cédric Bonhomme <https://www.cedricbonhomme.org>`_
