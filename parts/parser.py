from re import sub, match

A_COMMAND = 'A_COMMAND'
C_COMMAND = 'C_COMMAND'
L_COMMAND = 'L_COMMAND'

_sym_pat = r'[A-Za-z\$_\.:][A-Za-z\$_\.:\d]*'
_const_pat = r'0*(?:[1-2][0-9]{4}|3[0-1][0-9]{3}|32[0-6][0-9]{2}|327[0-5][0-9]|3276[0-7]|[0-9]{1,4})'
_a_instr_pat = f'^@({_sym_pat}|{_const_pat})$'
_l_instr_pat = fr'^\(({_sym_pat})\)$'

_regs = 'ADM'
_jumps = ['JMP', 'JNE', 'JEQ', 'JGT', 'JLT', 'JLE', 'JGE']
_unary_ops = r'\!\-'
_binary_ops = r'\+\-\|&'

_dest_group = fr'(?:(([{_regs}])(?!\2)([{_regs}])?(?!\2|\3)[{_regs}]?)=)'
_comp_group = ('(0|'
               r'\-?1|'
               fr'[{_unary_ops}]?[{_regs}]|'
               fr'(?:(?:1|[{_regs}])[{_binary_ops}](?:1|[{_regs}])))')
_jump_group = f'(?:;({"|".join(_jumps)}))'
_c_instr_pat = f'^{_dest_group}?{_comp_group}{_jump_group}?$'

_MAX_CONST_SIZE = 32767


class Parser:
    def __init__(self, file):
        self._line_map = {}
        self._instrs = list(self._read_instr_lines(file))
        self._cur_instr_index = -1
        self._cur_instr_type = None
        self._cur_instr_match = None

    def advance(self):
        self._cur_instr_index += 1
        self._set_cmd_type_and_match()

    @property
    def has_more_cmds(self):
        return self._cur_instr_index < len(self._instrs) - 1

    @property
    def cmd_type(self):
        return self._cur_instr_type

    @property
    def symbol(self):
        if self._cur_instr_type == C_COMMAND:
            raise RuntimeError(f'Line {self._cur_line}: "{self._cur_instr}" does not have a symbol because it is a C instruction')
        else:
            return self._cur_instr_match.group(1)

    @property
    def dest(self):
        return self._c_cmd(1, "dest")

    @property
    def comp(self):
        return self._c_cmd(4, 'comp')

    @property
    def jump(self):
        return self._c_cmd(5, 'jump')

    @property
    def _cur_instr(self):
        return self._instrs[self._cur_instr_index]

    @property
    def _cur_line(self):
        return self._line_map[self._cur_instr_index]

    def _c_cmd(self, grp, part):
        if not self._cur_instr_type == C_COMMAND:
            raise RuntimeError(f'Line {self._cur_line}: "{self._cur_instr}" does not have a {part} because it is not a C instruction')
        return self._cur_instr_match.group(grp)

    def _set_cmd_type_and_match(self):
        def match_instr(pat):
            return match(pat, self._cur_instr)

        def do_set(cmd_type):
            self._cur_instr_type = cmd_type
            self._cur_instr_match = m
            return cmd_type

        if m := match_instr(_l_instr_pat):
            do_set(L_COMMAND)
        elif m := match_instr(_c_instr_pat):
            do_set(C_COMMAND)
        elif m := match_instr(_a_instr_pat):
            do_set(A_COMMAND)
        elif match_instr(r'^@\-?\d+$'):
            raise RuntimeError(f'Line {self._cur_line}: constant in "{self._cur_instr}" is out of bounds. Please enter an integer between 0 and {_MAX_CONST_SIZE}.')
        else:
            raise RuntimeError(f'Line {self._cur_line}: invalid instruction: {self._cur_instr}')

    def _read_instr_lines(self, file):
        def rm_comments_and_whtspc():
            return sub(r'[/]{2}.*\n|\s+', '', line)

        lineno = 0
        line_index = -1
        for line in file.readlines():
            lineno += 1
            line = rm_comments_and_whtspc()
            if not line:
                continue
            line_index += 1
            self._line_map[line_index] = lineno
            yield line
