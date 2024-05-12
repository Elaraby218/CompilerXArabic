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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.errors = []

        # Define grammar rules
        self.rules = {
            "program": [("declaration_list",)],
            "declaration_list": [("declaration", "declaration_list"), ("declaration",)],
            "declaration": [("var_declaration",), ("function_declaration",)],
            "var_declaration": [("ID",), ("ID", "[", "Num", "]")],
            "function_declaration": [("ID", "(", "parameter_list", ")", "specifier_type")],
            "parameter_list": [("specifier_type", "ID", "[", "Num", "]", "param_rest"), ("specifier_type", "ID", "param_rest")],
            "param_rest": [(",", "specifier_type", "ID", "[", "Num", "]", "param_rest"), ()]
        }

    def match(self, expected_type):
        if self.index < len(self.tokens) and self.tokens[self.index].is_token(expected_type):
            self.index += 1
        else:
            self.error(expected_type)

    def error(self, expected_type):
        if self.index < len(self.tokens):
            found_token = self.tokens[self.index]
        else:
            found_token = Token("EOF", "")
        self.errors.append(f"Error: Expected {expected_type} but found {found_token}")

    def parse_symbol(self, symbol):
        for production in self.rules[symbol]:
            for token in production:
                if token in self.rules:
                    self.parse_symbol(token)
                else:
                    self.match(token)

    def parse(self):
        if self.tokens:
            self.parse_symbol("program")
        else:
            self.errors.append("Error: No tokens to parse")
        return self.errors


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
