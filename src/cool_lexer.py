from cool_tokens import tokens, reserved
import ply.lex as lex
from ply.lex import TOKEN

class Cool_Lexer:
    # Methods for lexer
    def __init__(self, errors):
        self.reserved = reserved
        self.tokens = tokens
        self.lexer = lex.lex(module=self)
        self.errors = errors

    def input(self, data_input):
        self.lexer.input(data_input)

    def token(self):
        return self.lexer.token()   

    # Ignore rule for single line comments
    t_ignore_SINGLE_LINE_COMMENT = r"\-\-[^\n]*"
    # Ignore this characters
    t_ignore = ' \t\r\f\v'    

    # Regular expressions
    t_SEMICOLON = r'\;'
    t_OCURLY = r'\{'
    t_CCURLY = r'\}'
    t_OPAREN  = r'\('
    t_CPAREN  = r'\)'
    t_COMMA = r'\,'
    t_COLON = r'\:'
    t_ASSIGN = r'\<\-'
    t_AT = r'\@'
    t_DOT = r'\.'
    t_ARROW = r'\=\>'
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_STAR   = r'\*'
    t_DIVIDE  = r'/'
    t_COMPLEMENT = r'\~'
    t_LT = r'\<'
    t_LTEQ = r'\<\='
    t_EQUAL = r'\='

    def t_BOOL(self, t):
        r'(true|false)'
        t.value = True if t.value == 'true' else False
        return t

    def t_TYPE(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'TYPE')
        return t

    def t_ID(self, t):
        r'[a-z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'ID')    
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # def t_STRING(self, t):
    #     r'"[a-zA-Z_][a-zA-Z_0-9]*"'
    #     t.value = t.value[1:-1]
    #     return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    # LEXER STATES
    @property
    def states(self):
        return (
            ("STRING", "exclusive"),
            ("COMMENT", "exclusive")
        )
    
    # THE STRING STATE
    def t_start_string(self, t):
        r'\"'
        t.lexer.push_state("STRING")
        t.lexer.string_backslashed = False
        t.lexer.stringbuf = ""

    def t_STRING_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        if not t.lexer.string_backslashed:
            print("String newline not escaped")
            t.lexer.skip(1)
        else:
            t.lexer.string_backslashed = False

    def t_STRING_end(self, t):
        r'\"'
        if not t.lexer.string_backslashed:
            t.lexer.pop_state()
            t.value = t.lexer.stringbuf
            t.type = "STRING"
            return t
        else:
            t.lexer.stringbuf += '"'
            t.lexer.string_backslashed = False

    def t_STRING_anything(self, t):
        r'[^\n]'
        if t.lexer.string_backslashed:
            if t.value == 'b':
                t.lexer.stringbuf += '\b'
            elif t.value == 't':
                t.lexer.stringbuf += '\t'
            elif t.value == 'n':
                t.lexer.stringbuf += '\n'
            elif t.value == 'f':
                t.lexer.stringbuf += '\f'
            elif t.value == '\\':
                t.lexer.stringbuf += '\\'
            else:
                t.lexer.stringbuf += t.value
            t.lexer.string_backslashed = False
        else:
            if t.value != '\\':
                t.lexer.stringbuf += t.value
            else:
                t.lexer.string_backslashed = True

    # STRING ignored characters
    t_STRING_ignore = ''

    # STRING error handler
    def t_STRING_error(self, t):
        self.errors.append("({}, {}) - LexicographicError: Caracter ilegal!".format(t.lineno, t.lexpos))
        t.lexer.skip(1)

    # THE COMMENT STATE
    def t_start_comment(self, t):
        r'\(\*'
        t.lexer.push_state("COMMENT")
        t.lexer.comment_count = 0

    def t_COMMENT_startanother(self, t):
        r'\(\*'
        t.lexer.comment_count += 1

    def t_COMMENT_end(self, t):
        r'\*\)'
        if t.lexer.comment_count == 0:
            t.lexer.pop_state()
        else:
            t.lexer.comment_count -= 1

    # COMMENT ignored characters
    t_COMMENT_ignore = ''

    # COMMENT error handler
    def t_COMMENT_error(self, t):
        t.lexer.skip(1)

    # Error handling rule
    def t_error(self, t):
        self.errors.append("({}, {}) - LexicographicError: Caracter ilegal!".format(t.lineno, t.lexpos))
        t.lexer.skip(1) 