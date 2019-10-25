from bitstring import BitArray


def dest(mnemonic):
    return BitArray(b'').join([bin(reg in mnemonic) for reg in 'ADM']) if mnemonic else BitArray(bin='000')
