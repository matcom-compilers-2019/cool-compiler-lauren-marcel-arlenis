# List of token names.   This is always required
tokens = [
'SEMICOLON',
'TYPE',
'OCURLY',
'CCURLY',
'ID',
'OPAREN',
'CPAREN',
'COMMA',
'COLON',
'ASSIGN',
'AT',
'DOT',
'ARROW',
'PLUS',
'MINUS',
'STAR',
'DIVIDE',
'COMPLEMENT',
'LT',
'LTEQ',
'EQUAL',
'INTEGER',
'STRING',
'BOOL'
]

reserved = {
    'class' : 'CLASS',
    'else' : 'ELSE',
    'fi' : 'FI',
    'if' : 'IF',
    'in' : 'IN',
    'inherits' : 'INHERITS',
    'isvoid' : 'ISVOID',
    'let' : 'LET',
    'loop' : 'LOOP',
    'pool' : 'POOL',
    'then' : 'THEN',
    'while' : 'WHILE',
    'case' : 'CASE',
    'esac' : 'ESAC',
    'new' : 'NEW',
    'of' : 'OF',
    'not' : 'NOT'
}

tokens += list(reserved.values())