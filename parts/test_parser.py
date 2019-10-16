from parts.parser import Parser
from tempfile import TemporaryFile
from pytest import mark, raises

invalid_test_data = ['L=1',
                    'AD=G',
                    '0;KEK',
                    'D-FoO;JGE',
                    'REEEEEEEEEEEEEEEEEEEE',
                    '42=!D',
                    'LRFRF|RERF:JLT',
                    'M|A;JUMP',
                    'BRUH=-1',
                    'FOO+BAR;JNE',
                    'A+D;YEET']

comp_test_data = [('M=1', '1'),
                  ('AD=M', 'M'),
                  ('0;JMP', '0'),
                  ('D-D;JGE', 'D-D'),
                  ('MAD=D&A;JNE', 'D&A'),
                  ('A=!A', '!A'),
                  ('M|A;JLT', 'M|A'),
                  ('A=-1', '-1'),
                  ('D+M;JNE', 'D+M')]


@mark.parametrize('instruction,expected', comp_test_data)
def test_comp_when_input_is_valid(instruction, expected):
    parser = setup_parser(instruction)
    assert parser.comp() == expected


@mark.parametrize('instruction', invalid_test_data)
def test_when_input_is_invalid_comp_throws(instruction):
    parser = setup_parser(instruction)
    with raises(Exception):
        assert parser.comp()


dest_test_data = [('M=1', 'M'),
                  ('AD=M', 'AD'),
                  ('0;JMP', None),
                  ('D-D;JGE', None),
                  ('MAD=D&A;JNE', 'MAD'),
                  ('A=!A', 'A'),
                  ('M|A;JLT', None),
                  ('A=-1', 'A'),
                  ('D+M;JNE', None)]


@mark.parametrize('instruction,expected', dest_test_data)
def test_dest_when_input_is_valid(instruction, expected):
    parser = setup_parser(instruction)
    assert parser.dest() == expected


@mark.parametrize('instruction', invalid_test_data)
def test_when_input_is_invalid_dest_throws(instruction):
    parser = setup_parser(instruction)
    with raises(Exception):
        assert parser.dest()


jump_test_data = [('M=1', None),
                  ('AD=M', None),
                  ('0;JMP', 'JMP'),
                  ('D-D;JGE', 'JGE'),
                  ('MAD=D&A;JNE', 'JNE'),
                  ('A=!A', None),
                  ('M|A;JLT', 'JLT'),
                  ('A=-1', None),
                  ('D+M;JNE', 'JNE')]


@mark.parametrize('instruction,expected', jump_test_data)
def test_jump_when_input_is_valid(instruction, expected):
    parser = setup_parser(instruction)
    assert parser.jump() == expected


@mark.parametrize('instruction', invalid_test_data)
def test_when_input_is_invalid_jump_throws(instruction):
    parser = setup_parser(instruction)
    with raises(Exception):
        assert parser.jump()


def setup_parser(instruction):
    file = TemporaryFile('w+')
    file.write(instruction)
    file.seek(0)
    parser = Parser(file)
    parser.advance()
    return parser
