from parts.code import dest
from bitstring import BitArray
from pytest import mark

dest_test_data = [(None, '000'),
                  ('M', '001'),
                  ('D', '010'),
                  ('A', '100'),
                  ('MD', '011'),
                  ('AM', '101'),
                  ('AD', '110'),
                  ('MAD', '111')]


@mark.parametrize('mnemonic,bits', dest_test_data)
def test_dest_when_mnemonic_has_registers_returns_bits(mnemonic, bits):
    assert dest(mnemonic) == BitArray(bin=bits)
