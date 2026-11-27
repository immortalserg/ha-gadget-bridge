"""Legacy Huami AES challenge-response packet codec.

Not a complete device driver. Newer authentication variants are not supported.
"""
AUTH_CHARACTERISTIC = "00000009-0000-3512-2118-0009af100700"


def challenge_request() -> bytes:
    return bytes((0x02, 0x00))


def challenge_response(packet: bytes, key: bytes, encrypt_block) -> bytes:
    """Build response using an injected AES-128 ECB single-block encryptor."""
    if len(key) != 16:
        raise ValueError("Expected a 16-byte authentication key")
    if len(packet) != 19 or packet[:3] != bytes((0x10, 0x02, 0x01)):
        raise ValueError("Invalid or unsuccessful challenge packet")
    encrypted = encrypt_block(key, packet[3:])
    if len(encrypted) != 16:
        raise ValueError("Expected a 16-byte encrypted challenge")
    return bytes((0x03, 0x00)) + encrypted


def authentication_succeeded(packet: bytes) -> bool:
    return packet == bytes((0x10, 0x03, 0x01))
