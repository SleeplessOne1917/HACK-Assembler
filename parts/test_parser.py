from parts.parser import Parser
from tempfile import TemporaryFile
from pytest import mark, raises

comp_test_data = [('M=1', '1'),
                  ('AD=M', 'M'),
                  ('0;JMP', '0'),
                  ('D-D;JGE', 'D-D'),
                  ('MAD=D&A;JNE', 'D&A'),
                  ('A=!A', '!A'),
                  ('M|A;JLT', 'M|A'),
                  ('A=-1', '-1'),
                  ('D+M;JNE', 'D+M'),
                  ('M=D', 'D'),
                  ('A=!A', '!A'),
                  ('!D;JGE', '!D'),
                  ('M=D+1', 'D+1'),
                  ('A+1;JNE', 'A+1'),
                  ('D=D-1', 'D-1'),
                  ('M=A-1', 'A-1'),
                  ('D+A;JEQ', 'D+A'),
                  ('MD=D-A', 'D-A'),
                  ('A-D;JEQ', 'A-D'),
                  ('M=D|A', 'D|A'),
                  ('M=!M', '!M'),
                  ('D-M;JGT', 'D-M')]


@mark.parametrize('instruction,expected', comp_test_data)
def test_comp_when_input_is_valid_returns_comp(instruction, expected):
    parser = setup_parser(instruction)
    assert parser.comp == expected


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
def test_dest_when_input_is_valid_returns_dest(instruction, expected):
    parser = setup_parser(instruction)
    assert parser.dest == expected


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
def test_jump_when_input_is_valid_returns_jump(instruction, expected):
    parser = setup_parser(instruction)
    assert parser.jump == expected


symbol_test_data = [('@32767', '32767'),
                    ('@1234', '1234'),
                    ('@567', '567'),
                    ('@69', '69'),
                    ('@7', '7'),
                    ('@_420', '_420'),
                    ('@foo:bar', 'foo:bar'),
                    ('(YeEt$)', 'YeEt$'),
                    ('@...Kekarino', '...Kekarino'),
                    ('(B_ruh$:suh.)', 'B_ruh$:suh.'),
                    ('(SYMBOLTHATACTUALLYFOLLOWSCONVENTION)', 'SYMBOLTHATACTUALLYFOLLOWSCONVENTION'),
                     ('@1337', '1337'),
                    ('@symbol', 'symbol'),
                    ('(symbol)', 'symbol')]


@mark.parametrize('instruction,expected', symbol_test_data)
def test_symbol_when_input_is_valid_returns_symbol(instruction, expected):
    parser = setup_parser(instruction)
    assert parser.symbol == expected


non_c_instructions = [arg[0] for arg in symbol_test_data]


@mark.parametrize('instruction', non_c_instructions)
def test_comp_when_input_is_not_c_instruction_throws(instruction):
    parser = setup_parser(instruction)
    with raises(Exception):
        assert parser.comp


@mark.parametrize('instruction', non_c_instructions)
def test_dest_when_input_is_not_c_instruction_throws(instruction):
    parser = setup_parser(instruction)
    with raises(Exception):
        assert parser.dest


@mark.parametrize('instruction', non_c_instructions)
def test_jump_when_input_is_not_c_instruction_throws(instruction):
    parser = setup_parser(instruction)
    with raises(Exception):
        assert parser.jump


c_instrs = [arg[0] for arg in comp_test_data] + [arg[0] for arg in dest_test_data] + [arg[0] for arg in jump_test_data]


@mark.parametrize('instruction', c_instrs)
def test_symbol_when_input_is_c_instruction_throws(instruction):
    parser = setup_parser(instruction)
    with raises(Exception):
        assert parser.symbol


invalid_instrs = ['@3symbol',
                  '@ahoy^^m80',
                  '(Argg&stuff)',
                  '(24label)',
                  'yayayayeet',
                  '(-POOPER_SCOOPER)',
                  'L=1',
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


@mark.parametrize('instruction', invalid_instrs)
def test_parser_fails_when_syntax_is_illegal(instruction):
    with raises(RuntimeError):
        assert setup_parser(instruction)


out_of_bounds_numbers = [32768, -1, -12345, 123456789]


@mark.parametrize('constant', out_of_bounds_numbers)
def test_parser_when_constant_out_of_bounds_throws(constant):
    with raises(RuntimeError) as e:
        setup_parser(f'@{constant}')
    assert 'out of bounds' in str(e.value)


def test_parser_when_lines_contain_comments_and_whitespace_reports_line_number():
    contents = '''//Lines containing only comments and whitespace
    
              
    //invalid instruction
    BAD'''
    with raises(RuntimeError) as e:
        setup_parser(contents)
    assert 'Line 5' in str(e.value)


def setup_parser(instruction):
    file = TemporaryFile('w+')
    file.write(instruction)
    file.seek(0)
    parser = Parser(file)
    parser.advance()
    return parser
