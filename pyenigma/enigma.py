#!/usr/bin/env python
"""Enigma cipher machine simulator.

This module implements the Enigma class, which simulates the WWII German
Enigma cipher machine. The machine uses a series of rotating substitution
ciphers (rotors), a reflector, and an optional plugboard (Steckerbrett)
to encrypt and decrypt messages.

The Enigma is self-reciprocal: with identical settings, enciphering an
already-enciphered message returns the original plaintext. This property
is fundamental to how Enigma operated — the sender and receiver used the
same machine settings to encrypt and decrypt respectively.
"""

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_ORD_A = ord("A")


def _build_plugboard_table(plugs_str):
    """Build a translation table from a plugboard configuration string.

    The plugboard (Steckerbrett) swaps pairs of letters before and after
    the rotor encryption. Each pair in the configuration string represents
    two letters that are wired together on the plugboard.

    Args:
        plugs_str: Space-separated letter pairs (e.g., "AV BS CG DL").
            An empty string means no plugboard connections.

    Returns:
        A str.maketrans translation table for the plugboard swaps.
    """
    if not plugs_str:
        return str.maketrans(_ALPHABET, _ALPHABET)

    plug_pairs = [(pair[0], pair[1]) for pair in plugs_str.split()]
    output_letters = list(_ALPHABET)

    for letter_a, letter_b in plug_pairs:
        output_letters[ord(letter_a) - _ORD_A] = letter_b
        output_letters[ord(letter_b) - _ORD_A] = letter_a

    return str.maketrans(_ALPHABET, "".join(output_letters))


def _process_single_char(enigma, char):
    """Process a single character through the Enigma machine's signal path.

    This implements the complete electrical signal path for one character:
    1. Advance the rotors (with double-stepping logic)
    2. Signal passes right-to-left through rotors 1→2→3
    3. Signal hits the reflector
    4. Signal passes left-to-right through rotors 3→2→1

    Args:
        enigma: The Enigma instance (needed for rotor access).
        char: A single uppercase alphabetic character.

    Returns:
        The encrypted/decrypted uppercase letter.
    """
    # Double-stepping anomaly: when both rotor1 and rotor2 are in
    # turnover positions, rotor3 also advances
    if enigma.rotor1.is_in_turnover_pos() and enigma.rotor2.is_in_turnover_pos():
        enigma.rotor3.notch()
    if enigma.rotor1.is_in_turnover_pos():
        enigma.rotor2.notch()

    # Always advance the fast rotor (rightmost)
    enigma.rotor1.notch()

    # Signal path: right → reflector → left
    signal = enigma.rotor1.encipher_right(char)
    signal = enigma.rotor2.encipher_right(signal)
    signal = enigma.rotor3.encipher_right(signal)
    signal = enigma.reflector.encipher(signal)
    signal = enigma.rotor3.encipher_left(signal)
    signal = enigma.rotor2.encipher_left(signal)
    signal = enigma.rotor1.encipher_left(signal)

    return signal


def _restore_case(lower_flags, ciphertext):
    """Restore the original case pattern onto the ciphertext.

    The Enigma machine operates on uppercase letters, but the input
    may contain lowercase characters. This function preserves the
    original case: positions that were lowercase in the input produce
    lowercase output, and uppercase positions stay uppercase.

    ``lower_flags`` must be aligned with ``ciphertext`` position-for-position
    (see :meth:`Enigma.encipher`). They can be built directly from the
    input string only when uppercasing preserves length; some characters
    expand when uppercased (e.g. ``ß`` -> ``SS``), so the flags are
    computed against that expansion rather than the raw input.

    Args:
        lower_flags: Per-position booleans, True where the output should
            be lowercased. Same length as ``ciphertext``.
        ciphertext: The encrypted string (all uppercase for alpha chars).

    Returns:
        The ciphertext with case restored to match the original input.
    """
    result = []
    for is_lower, cipher_char in zip(lower_flags, ciphertext):
        result.append(cipher_char.lower() if is_lower else cipher_char)
    return "".join(result)


class Enigma:
    """Represents an Enigma cipher machine.

    The Enigma machine encrypts text through a series of substitution
    ciphers implemented by rotating wheels (rotors), a reflector that
    reverses the signal path, and an optional plugboard that swaps
    letter pairs.

    The machine is self-reciprocal: enciphering the same text twice
    with identical settings returns the original plaintext.

    Attributes:
        reflector: The reflector component (Umkehrwalze).
        rotor1: The rightmost (fast) rotor.
        rotor2: The middle rotor.
        rotor3: The leftmost (slow) rotor.
        transtab: The plugboard translation table.
    """

    def __init__(self, ref, r1, r2, r3, key="AAA", plugs="", ring="AAA"):
        """Initialize an Enigma machine with the given configuration.

        Args:
            ref: Reflector instance (e.g., ROTOR_Reflector_B).
            r1: Rightmost rotor (fast rotor, advances every keypress).
            r2: Middle rotor (advances when r1 hits turnover).
            r3: Leftmost rotor (slow rotor, advances when r2 hits turnover).
            key: 3-letter initial rotor position (e.g., "AAA"). Defaults to "AAA".
            plugs: Plugboard configuration as space-separated pairs
                (e.g., "AV BS CG"). Defaults to empty (no plugs).
            ring: 3-letter ring setting / Ringstellung (e.g., "AAA").
                Defaults to "AAA".
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
        self.reflector.state = "A"

        self.transtab = _build_plugboard_table(plugs)

    def encipher(self, plaintext_in):
        """Encrypt or decrypt a message using the Enigma machine.

        The method processes each alphabetic character through the
        complete Enigma signal path, including plugboard, rotors,
        and reflector. Non-alphabetic characters (spaces, numbers,
        punctuation) pass through unchanged.

        Case is preserved: lowercase input produces lowercase output,
        and uppercase input produces uppercase output. The internal
        processing is always done in uppercase.

        Args:
            plaintext_in: The message to encrypt or decrypt.

        Returns:
            The enciphered text, with original case preserved and
            non-alphabetic characters unchanged.
        """
        plaintext_upper = plaintext_in.upper()
        plugboard_applied = plaintext_upper.translate(self.transtab)

        # Track case per output position. Uppercasing can change length
        # (e.g. "ß" -> "SS"), so flags are aligned with the uppercased
        # string rather than the raw input to keep the case mask in sync
        # with the enciphered characters.
        lower_flags = []
        for original_char in plaintext_in:
            expansion_len = len(original_char.upper())
            lower_flags.extend([original_char.islower()] * expansion_len)

        cipher_chars = []
        for char in plugboard_applied:
            if not char.isalpha():
                cipher_chars.append(char)
                continue
            cipher_chars.append(_process_single_char(self, char))

        ciphertext = "".join(cipher_chars)
        plugboard_reversed = ciphertext.translate(self.transtab)

        return _restore_case(lower_flags, plugboard_reversed)

    def __str__(self):
        """Pretty display of the machine's current rotor configuration."""
        return """
        Reflector: {}

        Rotor 1: {}

        Rotor 2: {}

        Rotor 3: {}""".format(
            self.reflector, self.rotor1, self.rotor2, self.rotor3
        )
