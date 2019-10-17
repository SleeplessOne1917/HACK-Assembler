from re import sub, match

A_COMMAND = 'A_COMMAND'
C_COMMAND = 'C_COMMAND'
L_COMMAND = 'L_COMMAND'


class Parser:
    def __init__(self, file):
        self._instructions = list(self._read_instr_lines(file))
        self._cur_instr_index = -1

    def advance(self):
        self._cur_instr_index += 1

    def has_more_cmds(self):
        return self._cur_instr_index < len(self._instructions) - 1

    def _cur_instr(self):
        return self._instructions[self._cur_instr_index]

    def cmd_type(self):
        determining_char = self._cur_instr()[0]
        if determining_char == '@':
            return A_COMMAND
        elif determining_char == '(':
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        if self.cmd_type() == C_COMMAND:
            raise RuntimeError('Instruction must be an A command or label')
        elif self.cmd_type() == A_COMMAND:
            return self._cur_instr()[1:]
        else:
            return self._cur_instr()[1:-1]

    def dest(self):
        if not self.cmd_type() == C_COMMAND:
            raise RuntimeError('Only C commands have dests')
        return self._extract_group_from_c_command(self._cur_instr(), 0)

    def comp(self):
        if not self.cmd_type() == C_COMMAND:
            raise RuntimeError('Only C commands have comps')
        return self._extract_group_from_c_command(self._cur_instr(), 3)

    def jump(self):
        if not self.cmd_type() == C_COMMAND:
            raise RuntimeError('Only C commands have jumps')
        return self._extract_group_from_c_command(self._cur_instr(), 4)

    @staticmethod
    def _extract_group_from_c_command(c_command, group_index):
        registers = 'ADM'
        jumps = ['JMP', 'JNE', 'JEQ', 'JGT', 'JLT', 'JLE', 'JGE']
        unary_operators = r'\!\-'
        binary_operators = r'\+\-\|&'

        dest_group = fr'(?:(([{registers}])(?!\2)([{registers}])?(?!\2|\3)[{registers}]?)=)'
        comp_group = ('(0|'
                      r'\-?1|'
                      fr'[{unary_operators}]?[{registers}]|'
                      fr'(?:(?:1|[{registers}])[{binary_operators}](?:1|[{registers}])))')
        jump_group = f'(?:;({"|".join(jumps)}))'

        pattern = f'^{dest_group}?{comp_group}{jump_group}?$'
        groups = match(pattern, c_command).groups()
        return groups[group_index]

    @staticmethod
    def _read_instr_lines(file):
        def remove_comments_and_whitespace():
            return sub(r'[/]{2}.*\n|\s+', '', line)

        for line in file.readlines():
            line = remove_comments_and_whitespace()
            if not line:
                continue
            yield line
