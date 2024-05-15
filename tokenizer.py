import re


class Token:
    def __init__(self, token_type, token_value, line=None):
        self.type = token_type
        self.value = token_value
        self.line = line

    def __str__(self):
        return f"{self.type}: {self.value} at line {self.line}"

    def __repr__(self):
        return f"{self.type}: {self.value} at line {self.line}"

    def is_token(self, token_type):
        return self.type == token_type or self.value == token_type


class Tokenizer:
    def __init__(self):
        self.token_patterns = {
            'specifier_type': r'صحيح(?![^\s])|حقيقي(?![^\s])|خالى(?![^\s])',
            'if_stmt': r'اذا(?![^\s])',
            'else_stmt': r'اخر(?![^\s])',
            'return': r'ارجع(?![^\s])',
            'iteration': r'بينما(?![^\s])',

            # 'if_stmt': r'اذا',
            # 'else_stmt': r'اخر',
            # 'return': r'ارجع',
            # 'iteration': r'بينما',
            # 'keyword': r'ارجع|بينما|اخر|اذا|خالي|حقيقي|صحيح',
            'relOp': r'==|=!|=<|=>|<|>',
            'assign': r'=',
            'addOp': r'\+|-',
            'mulOp': r'\*|\\',
            'openBracket': r'[\(\[\{]',
            'closeBracket': r'[\)\]\}]',
            'ID': r'[_اإبتثجحخدذرزسشصضطظعغفقكلمنهويى]+[\da-zA-Z]*|[\da-zA-Z]+[ايإبتثجحخدذرزسشصضطظعغفقكلمنهوى_]+',
            'Num': r'(-?\d+(?:,\d+)?|-?\d*\.\d+)',
            'semicolon': r'؛',
            'comma': r',',
        }

    def tokenize(self, text):
        output_tokens = []
        # split on  \n to get the line number
        lines = text.split('\n')
        for i, line in enumerate(lines):
            for match in re.finditer('|'.join('(?P<%s>%s)' % pair for pair in self.token_patterns.items()), line):
                token_type = match.lastgroup
                token_value = match.group(token_type)
                output_tokens.append(Token(token_type, token_value, i + 1))
        return output_tokens
