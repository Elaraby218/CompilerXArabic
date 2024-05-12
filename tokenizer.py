import re


class Token:
    def __init__(self, token_type, token_value, line=None):
        self.type = token_type
        self.value = token_value
        self.line = line

    def __str__(self):
        return f"{self.type}: {self.value} at line {self.line}"

class Tokenizer:
    def __init__(self):
        self.token_patterns = {
            'specifier_type': r'صحيح|حقیقى|خالى',
            'keyword': r'ارجع|بينما|اخر|اذا|خالي|حقيقي|صحيح',
            'relOp': r'==|=!|=<|=>|<|>|=',
            'addOp': r'\+|-',
            'mulOp': r'\*|\\',
            'openBracket': r'[\(\[\{]',
            'closeBracket': r'[\)\]\}]',
            'ID': r'[اإبتثجحخدذرزسشصضطظعغفقكلمنهوى]+[\da-zA-Z]*|[\da-zA-Z]+[اإبتثجحخدذرزسشصضطظعغفقكلمنهوى]+',
            'Num': r'(-?\d+(?:,\d+)?|-?\d*\.\d+)',
            'semicolon': r'؛',
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
