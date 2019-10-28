from bitstring import BitArray


def dest(mnemonic):
    return BitArray(b'').join([bin(reg in mnemonic) for reg in 'ADM']) if mnemonic else BitArray(bin='000')


def jump(mnemoic):
    jump_bits = {None: '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110',
     'JMP': '111'}
    return BitArray(bin=jump_bits[mnemoic])
