# pyEnigma

[![builds.sr.ht status](https://builds.sr.ht/~cedric/pyenigma.svg)](https://builds.sr.ht/~cedric/pyenigma)


[pyEnigma](https://sr.ht/~cedric/pyenigma) is a  Python Enigma cypher machine
simulator.

For reporting issues, visit the tracker here:
https://todo.sr.ht/~cedric/pyenigma


## Usage


### As a Python library

You can install pyEnigma with Poetry.

```bash
$ poetry install pyenigma
```

Then you can use it in your program:

```bash
$ poetry shell
(pyenigma-X0xzv6Ge-py3.8) $
(pyenigma-X0xzv6Ge-py3.8) $ python
```

```python
Python 3.8.0 (default, Dec 11 2019, 21:43:13)
[GCC 9.2.1 20191008] on linux
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
Qgqop Vyzxp
```

### As a program

Install pyEnigma system wide with pipx:

```bash
$ pipx install pyenigma
```

Then you can use the command line interface:

```bash
$ echo "Hello World" | enigma ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"
Qgqop Vyzxp

$ echo "Qgqop Vyzxp" | enigma ABC A  I II III "AV BS CG DL FU HZ IN KM OW RX"
Hello World
```

If you want to display the rotor output state:

```bash
$ echo "Hello World" | enigma ABC A I II III "AV BS CG DL FU HZ IN KM OW RX" --verbose
Qgqop Vyzxp
KBC A I II III "AV BS CG DL FU HZ IN KM OW RX"
```

The state is returned on ```stderr```, so you can still use the Unix pipe mechanism:

```bash
$ echo "Hello World" | enigma ABC A I II III "AV BS CG DL FU HZ IN KM OW RX" --verbose | enigma ABC A I II III "AV BS CG DL FU HZ IN KM OW RX"
KBC A I II III "AV BS CG DL FU HZ IN KM OW RX"
Hello World
```


## License

pyEnigma is licensed under
[GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.html)


## Author

* [Christophe Goessen](https://github.com/cgoessen) (initial author)
* [Cédric Bonhomme](https://www.cedricbonhomme.org)
