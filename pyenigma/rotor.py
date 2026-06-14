#!/usr/bin/env python
"""Rotor and reflector components for the Enigma cipher machine.

This module defines the Rotor and Reflector classes that implement
the core substitution cipher mechanics of the Enigma machine, along
with all historical rotor and reflector definitions.
"""
# Alphabet constants
_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_ALPHABET_SIZE = 26
_ORD_A = ord("A")


def _build_reverse_wiring(wiring):
    """Build the reverse (left-to-right) wiring from a forward wiring string.

    Given a forward wiring like "EKMFLGDQVZNTOWYHXUSPAIBRCJ" (Rotor I),
    computes the inverse mapping so that if A->E in forward, then E->A
    in reverse. This is needed for the signal's return path through the
    rotors after hitting the reflector.

    Args:
        wiring: A 26-character string representing the forward wiring,
            where position i maps letter chr(_ORD_A + i) to wiring[i].

    Returns:
        A list of 26 characters representing the reverse wiring.
    """
    reverse = [""] * _ALPHABET_SIZE
    for position, wired_letter in enumerate(wiring):
        reverse[ord(wired_letter) - _ORD_A] = chr(_ORD_A + position)
    return reverse


class Reflector:
    """Represents an Enigma reflector (UKW = Umkehrwalze).

    The reflector sits to the left of the leftmost rotor. It receives
    the signal from the rotors, swaps paired letters, and sends the
    signal back through the rotors in the opposite direction. This
    reciprocal property is what makes Enigma self-reciprocal: the same
    machine both encrypts and decrypts with identical settings.

    Unlike rotors, the reflector never rotates during operation.

    Attributes:
        wiring: The 26-character substitution wiring string.
        name: Human-readable identifier (e.g., "Reflector B").
        model: The Enigma model this reflector belongs to.
        date: The date this reflector was introduced.
    """

    _DEFAULT_WIRING = _ALPHABET

    def __init__(self, wiring=None, name=None, model=None, date=None):
        """Initialize a reflector with the given wiring configuration.

        Args:
            wiring: 26-character wiring string. Defaults to identity (A->A, B->B, ...).
            name: Human-readable name for this reflector.
            model: Enigma model designation.
            date: Historical introduction date.
        """
        self.wiring = wiring if wiring is not None else self._DEFAULT_WIRING
        self.name = name
        self.model = model
        self.date = date

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def encipher(self, key):
        """Transform a letter through the reflector's wiring.

        The signal passes through the reflector with the current
        state offset applied, then the result is adjusted back.

        Args:
            key: A single uppercase letter to transform.

        Returns:
            The transformed uppercase letter.
        """
        shift = ord(self.state) - _ORD_A
        connector_index = (ord(key) - _ORD_A + shift) % _ALPHABET_SIZE
        wired_letter = self.wiring[connector_index]
        output = chr(
            _ORD_A
            + (ord(wired_letter) - _ORD_A + _ALPHABET_SIZE - shift) % _ALPHABET_SIZE
        )
        return output

    def __eq__(self, other):
        """Two reflectors are equal if they have the same name."""
        return self.name == other.name

    def __str__(self):
        """Pretty display."""
        return """
        Name: {}
        Model: {}
        Date: {}
        Wiring: {}""".format(
            self.name, self.model, self.date, self.wiring
        )


class Rotor:
    """Represents an Enigma rotor (Walze).

    Each rotor implements a substitution cipher with a 26-letter wiring.
    The rotor can be in different rotational positions (state) and has
    a configurable ring setting (Ringstellung) that offsets the internal
    wiring relative to the outer alphabet ring.

    Rotors also have turnover notches: when the rotor reaches a notch
    position, it causes the next rotor to advance (mechanical stepping).

    The double-stepping anomaly is handled by the Enigma class: when
    the middle rotor is in its notch position, both the middle and
    left rotors advance.

    Attributes:
        wiring: The 26-character forward substitution wiring.
        rwiring: The computed reverse wiring (for signal return path).
        notchs: String of turnover notch letters (e.g., "R" for Rotor I).
        name: Human-readable identifier (e.g., "I", "II", "III").
        model: The Enigma model this rotor belongs to.
        date: Historical introduction date.
        state: Current rotational position (A-Z).
        ring: Ring setting offset (A-Z, also called Ringstellung).
    """

    _DEFAULT_WIRING = _ALPHABET

    def __init__(
        self,
        wiring=None,
        notchs=None,
        name=None,
        model=None,
        date=None,
        state="A",
        ring="A",
    ):
        """Initialize a rotor with the given wiring and configuration.

        Args:
            wiring: 26-character forward wiring string. Defaults to identity.
            notchs: Turnover notch letters (e.g., "R" or "AN"). Defaults to empty.
            name: Human-readable rotor name.
            model: Enigma model designation.
            date: Historical introduction date.
            state: Initial rotational position (A-Z). Defaults to "A".
            ring: Ring setting / Ringstellung (A-Z). Defaults to "A".
        """
        self.wiring = wiring if wiring is not None else self._DEFAULT_WIRING
        self.rwiring = _build_reverse_wiring(self.wiring)
        self.notchs = notchs if notchs is not None else ""
        self.name = name
        self.model = model
        self.date = date
        self.state = state
        self.ring = ring

    def __setattr__(self, name, value):
        """Override to rebuild reverse wiring when forward wiring changes."""
        self.__dict__[name] = value
        if name == "wiring":
            self.rwiring = _build_reverse_wiring(self.wiring)

    def encipher_right(self, key):
        """Transform a letter through the rotor in the right-to-left direction.

        This is the forward path: the signal enters from the right side
        of the rotor (keyboard side) and exits to the left (reflector side).

        The transformation accounts for the current rotational state and
        ring setting offset.

        Args:
            key: A single uppercase letter to transform.

        Returns:
            The transformed uppercase letter.
        """
        shift = ord(self.state) - ord(self.ring)
        connector_index = (ord(key) - _ORD_A + shift) % _ALPHABET_SIZE
        wired_letter = self.wiring[connector_index]
        output = chr(
            _ORD_A
            + (ord(wired_letter) - _ORD_A + _ALPHABET_SIZE - shift) % _ALPHABET_SIZE
        )
        return output

    def encipher_left(self, key):
        """Transform a letter through the rotor in the left-to-right direction.

        This is the return path: after the signal bounces off the reflector,
        it passes back through the rotors from left to right, using the
        reverse wiring.

        Args:
            key: A single uppercase letter to transform.

        Returns:
            The transformed uppercase letter.
        """
        shift = ord(self.state) - ord(self.ring)
        connector_index = (ord(key) - _ORD_A + shift) % _ALPHABET_SIZE
        wired_letter = self.rwiring[connector_index]
        output = chr(
            _ORD_A
            + (ord(wired_letter) - _ORD_A + _ALPHABET_SIZE - shift) % _ALPHABET_SIZE
        )
        return output

    def notch(self, offset=1):
        """Advance the rotor by the given offset (default: 1 position).

        This simulates the mechanical stepping of the rotor. After each
        keypress, the rightmost rotor (fast rotor) advances by one position.
        Other rotors advance when triggered by turnover notches.

        Args:
            offset: Number of positions to advance. Defaults to 1.
        """
        self.state = chr((ord(self.state) + offset - _ORD_A) % _ALPHABET_SIZE + _ORD_A)

    def is_in_turnover_pos(self):
        """Check if the rotor is currently sitting on a turnover notch.

        A real Enigma rotor carries the next rotor as it *leaves* its notch
        letter (e.g. Rotor I turns the rotor to its left as it steps from R
        to S). So the turnover is triggered by the keypress that occurs while
        the notch letter is showing — i.e. when the *current* position is a
        notch position.

        Returns:
            True if the current position is a turnover notch, False otherwise.
        """
        return self.state in self.notchs

    def __eq__(self, other):
        """Two rotors are equal if they have the same name."""
        return self.name == other.name

    def __str__(self):
        """Pretty display."""
        return """
        Name: {}
        Model: {}
        Date: {}
        Wiring: {}
        State: {}""".format(
            self.name, self.model, self.date, self.wiring, self.state
        )


# ─── Historical Rotor Definitions ──────────────────────────────────────────
#
# Each rotor is defined by its unique wiring (the substitution cipher it
# implements), its turnover notch position(s), and its historical metadata.
# The wiring strings define the signal path: position i in the string is
# where letter chr(65+i) maps to.

# 1924 Commercial Enigma A, B Rotors
ROTOR_IC = Rotor(
    wiring="DMTWSILRUYQNKFEJCAZBPGXOHV",
    name="IC",
    model="Commercial Enigma A, B",
    date="1924",
)
ROTOR_IIC = Rotor(
    wiring="HQZGPJTMOBLNCIFDYAWVEUSRKX",
    name="IIC",
    model="Commercial Enigma A, B",
    date="1924",
)
ROTOR_IIIC = Rotor(
    wiring="UQNTLSZFMREHDPXKIBVYGJCWOA",
    name="IIIC",
    model="Commercial Enigma A, B",
    date="1924",
)


# German Railway (Rocket) Rotors — introduced 7 February 1941
ROTOR_GR_I = Rotor(
    wiring="JGDQOXUSCAMIFRVTPNEWKBLZYH",
    name="I",
    model="German Railway (Rocket)",
    date="7 February 1941",
)
ROTOR_GR_II = Rotor(
    wiring="NTZPSFBOKMWRCJDIVLAEYUXHGQ",
    name="II",
    model="German Railway (Rocket)",
    date="7 February 1941",
)
ROTOR_GR_III = Rotor(
    wiring="JVIUBHTCDYAKEQZPOSGXNRMWFL",
    name="III",
    model="German Railway (Rocket)",
    date="7 February 1941",
)
ROTOR_GR_UKW = Reflector(
    wiring="QYHOGNECVPUZTFDJAXWMKISRBL",
    name="UTKW",
    model="German Railway (Rocket)",
    date="7 February 1941",
)
ROTOR_GR_ETW = Rotor(
    wiring="QWERTZUIOASDFGHJKPYXCVBNML",
    name="ETW",
    model="German Railway (Rocket)",
    date="7 February 1941",
)

# Swiss K Rotors — introduced February 1939
ROTOR_I_K = Rotor(
    wiring="PEZUOHXSCVFMTBGLRINQJWAYDK",
    name="I-K",
    model="Swiss K",
    date="February 1939",
)
ROTOR_II_K = Rotor(
    wiring="ZOUESYDKFWPCIQXHMVBLGNJRAT",
    name="II-K",
    model="Swiss K",
    date="February 1939",
)
ROTOR_III_K = Rotor(
    wiring="EHRVXGAOBQUSIMZFLYNWKTPDJC",
    name="III-K",
    model="Swiss K",
    date="February 1939",
)
ROTOR_UKW_K = Reflector(
    wiring="IMETCGFRAYSQBZXWLHKDVUPOJN",
    name="UKW-K",
    model="Swiss K",
    date="February 1939",
)
ROTOR_ETW_K = Rotor(
    wiring="QWERTZUIOASDFGHJKPYXCVBNML",
    name="ETW-K",
    model="Swiss K",
    date="February 1939",
)

# Enigma 1 Rotors — introduced 1930
ROTOR_I = Rotor(
    wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    notchs="R",
    name="I",
    model="Enigma 1",
    date="1930",
)
ROTOR_II = Rotor(
    wiring="AJDKSIRUXBLHWTMCQGZNPYFVOE",
    notchs="F",
    name="II",
    model="Enigma 1",
    date="1930",
)
ROTOR_III = Rotor(
    wiring="BDFHJLCPRTXVZNYEIWGAKMUSQO",
    notchs="W",
    name="III",
    model="Enigma 1",
    date="1930",
)

# M3 Army Rotors — introduced December 1938
ROTOR_IV = Rotor(
    wiring="ESOVPZJAYQUIRHXLNFTGKDCMWB",
    notchs="K",
    name="IV",
    model="M3 Army",
    date="December 1938",
)
ROTOR_V = Rotor(
    wiring="VZBRGITYUPSDNHLXAWMJQOFECK",
    notchs="A",
    name="V",
    model="M3 Army",
    date="December 1938",
)

# M3 & M4 Naval Rotors — introduced 1939, deployed February 1942
ROTOR_VI = Rotor(
    wiring="JPGVOUMFYQBENHZRDKASXLICTW",
    notchs="AN",
    name="VI",
    model="M3 & M4 Naval(February 1942)",
    date="1939",
)
ROTOR_VII = Rotor(
    wiring="NZJHGRCXMYSWBOUFAIVLPEKQDT",
    notchs="AN",
    name="VII",
    model="M3 & M4 Naval(February 1942)",
    date="1939",
)
ROTOR_VIII = Rotor(
    wiring="FKQHTLXOCBJSPDZRAMEWNIUYGV",
    notchs="AN",
    name="VIII",
    model="M3 & M4 Naval(February 1942)",
    date="1939",
)

# M4 R2 (Thin) Rotors — introduced Spring 1941
ROTOR_Beta = Rotor(
    wiring="LEYJVCNIXWPBQMDRTAKZGFUHOS", name="Beta", model="M4 R2", date="Spring 1941"
)
ROTOR_Gamma = Rotor(
    wiring="FSOKANUERHMBTIYCWLQPZXVGJD", name="Gamma", model="M4 R2", date="Spring 1941"
)

# Reflectors
ROTOR_Reflector_A = Reflector(wiring="EJMZALYXVBWFCRQUONTSPIKHGD", name="Reflector A")
ROTOR_Reflector_B = Reflector(wiring="YRUHQSLDPXNGOKMIEBFZCWVJAT", name="Reflector B")
ROTOR_Reflector_C = Reflector(wiring="FVPJIAOYEDRZXWGCTKUQSBNMHL", name="Reflector C")
ROTOR_Reflector_B_Thin = Reflector(
    wiring="ENKQAUYWJICOPBLMDXZVFTHRGS",
    name="Reflector_B_Thin",
    model="M4 R1 (M3 + Thin)",
    date="1940",
)
ROTOR_Reflector_C_Thin = Reflector(
    wiring="RDOBJNTKVEHMLFCWZAXGYIPSUQ",
    name="Reflector_C_Thin",
    model="M4 R1 (M3 + Thin)",
    date="1940",
)

# Entry wheel (ETW = Eintrittswalze) — identity wiring
ROTOR_ETW = Rotor(wiring=_ALPHABET, name="ETW", model="Enigma 1")
