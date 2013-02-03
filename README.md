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

As a Python module
~~~~~~~~~~~~~~~~~~

    Python 3.2.3 (default, Oct 19 2012, 19:53:16) 
    [GCC 4.7.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pyenigma import rotor
    >>> print(rotor.ROTOR_GR_III)

        Name: III
        Model: German Railway (Rocket)
        Date: 7 February 1941
        Wiring: JVIUBHTCDYAKEQZPOSGXNRMWFL
    >>>

Command line
~~~~~~~~~~~~

    $ echo "Hello World" | ./cypher_enigma_safe.py secret B  I II V 
    Vjpfw Ekdxj

    $ echo "Vjpfw Ekdxj" | ./cypher_enigma_safe.py secret B  I II V
    Hello World

License
-------

pyEnigma is under license.

Author
------
* [Christophe Goessen](https://bitbucket.org/azmaeve) (main author)
* [Cédric Bonhomme](http://cedricbonhomme.org/)
