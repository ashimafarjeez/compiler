import re
token_definition=[
    ('NUMBER', r'\d+'),
    ('ID', r'[a-zA-Z_]\w*'),
    ('ASSIGN', r'='),
    ('PLUS', r'\+'),
    ('MINUS',r'-'),
    ('TIMES', r'\*'),
    ('DIV', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMI',r';')
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.')
]

def tokenize(code):
    tokens = []
    #building one big regex
    token_regex='|'.join(
        f'(?P<{name}>{pattern})'
        for name, pattern in token_definition
    )
    #match patterns and update tokens
    for match in re.finditer(token_regex, code):
        kind=match.lastgroup #name of the group it got matched to
        value=match.group() #actual value
        if kind=='SKIP':
            continue
        elif kind=='MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        else:
            tokens.append((kind,value))
    return tokens
