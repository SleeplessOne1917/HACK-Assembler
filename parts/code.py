from bitstring import BitArray


def dest(mnemonic):
    if not mnemonic:
        return BitArray(bin='000')
    return BitArray(b'').join([bin(reg in mnemonic) for reg in 'ADM'])
