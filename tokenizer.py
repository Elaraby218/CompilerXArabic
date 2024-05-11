import re

class Tokenizer:
    def __init__(self):
        self.token_patterns = {
            'specifier_type': r'صحيح|حقیقى|خالى',
            'keyword': r'ارجع|بينما|اخر|اذا|خالي|حقيقي|صحيح',
            'relOp': r'==|=!|=<|=>|<|>|=',
            'addOp': r'\+|-',
            'mulOp': r'\*|\\',
            'ID': r'[اإبتثجحخدذرزسشصضطظعغفقكلمنهوى]+[\da-zA-Z]*|[\da-zA-Z]+[اإبتثجحخدذرزسشصضطظعغفقكلمنهوى]+',
            'Num': r'(-?\d+(?:,\d+)?|-?\d*\.\d+)',
            'semicolon': r'؛',
        }

    def tokenize(self, text):
        output_tokens = []
        for match in re.finditer('|'.join('(?P<%s>%s)' % pair for pair in self.token_patterns.items()), text):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            output_tokens.append((token_type, token_value.strip()))
        return output_tokens
