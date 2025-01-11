import re
import bisect

class Token:
    def __init__(self, type_, text, pos, line, column):
        self.type = type_
        self.text = text
        self.pos = pos
        self.line = line
        self.column = column

class Lexer:
    def __init__(self):
        self.rules = [
            ('WHITESPACE', r'\s+'),
            ('MULTILINE_COMMENT', r'--\[(=*)\[(.*?)\]\1\]'),
            ('COMMENT', r'--[^\n]*'),
            ('STRING_DBL', r'"(?:\\.|[^\\"])*"'),
            ('STRING_SGL', r"'(?:\\.|[^\\'])*'"),
            ('MULTILINE_STRING', r'\[(=*)\[(.*?)\]\1\]'),
            ('VARARGS', r'\.\.\.(?!\.)'),
            ('CONCAT', r'\.\.'),
            ('METHOD_ACCESS', r':'),
            ('LSHIFT_EQ', r'<<='),
            ('RSHIFT_EQ', r'>>='),
            ('LSHIFT', r'<<'),
            ('RSHIFT', r'>>'),
            ('EQ', r'=='),
            ('NEQ', r'~='),
            ('LE', r'<='),
            ('GE', r'>='),
            ('OP', r'[+\-*/%^#=<>|&~]'),
            ('HEX_NUM', r'0x[0-9a-fA-F]+(?:\.[0-9a-fA-F]+)?(?:[pP][+\-]?\d+)?'),
            ('BIN_NUM', r'0b[01]+'),
            ('OCT_NUM', r'0o[0-7]+'),
            ('FLOAT_NUM', r'-?\d*\.\d+(?:[eE][+\-]?\d+)?'),
            ('INT_NUM', r'-?\d+'),
            ('KEYWORD', r'\b(?:local|if|then|else|elseif|end|function|return|for|while|do|repeat|until|break|continue|not|and|or|in|self|import|export|type|interface|class|extends|implements|nilable|constructor|new)\b'),
            ('BOOL', r'\b(?:true|false)\b'),
            ('NIL', r'\bnil\b'),
            ('METHOD', r'\b(?:WaitForChild|InvokeServer|Connect|Fire)\b'),
            ('IDENT', r'\b[_a-zA-Z][_a-zA-Z0-9]*\b'),
            ('DELIM', r'[(){}\[\],;.]'),
            ('NEWLINE', r'\n'),
            ('UNKNOWN', r'.'),
        ]
        pattern = '|'.join(f'(?P<{name}>{regex})' for name, regex in self.rules)
        self.regex = re.compile(pattern, re.DOTALL)

    def tokenize(self, code):
        lines = [0]
        for idx, char in enumerate(code):
            if char == '\n':
                lines.append(idx + 1)

        def get_position(pos):
            line = bisect.bisect_right(lines, pos) - 1
            return line + 1, pos - lines[line] + 1

        tokens = []
        for match in self.regex.finditer(code):
            kind = match.lastgroup
            start = match.start()
            line, col = get_position(start)
            if kind in ('WHITESPACE', 'COMMENT', 'MULTILINE_COMMENT', 'NEWLINE'):
                continue
            text = match.group()
            tokens.append(Token(kind, text, start, line, col))
        return tokens

def tokenize_luau(code):
    lexer = Lexer()
    tokens = lexer.tokenize(code)
    return tokens
