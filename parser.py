class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0
        self.errors = []
    def match(self, token_type):
        if self.current_token and self.current_token.type == token_type or self.current_token.value == token_type:
            self.consume()
        else:
            self.error(self.current_token, token_type)

    def consume(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token.type = "EOF"
            self.current_token.value = "EOF"

    def error(self, found_token=None, expected_type=None):
        if found_token and expected_type:
            self.errors.append(f"Error: Expected {expected_type} but found {found_token}")
        else:
            self.errors.append("Error: Invalid syntax")


    def var_declaration(self):
        self.match("specifier_type")
        self.match("ID")
        if self.current_token.value == "=":
            self.match("=")
            self.match("Num")
        if self.current_token.value == "[":
            self.match("[")
            self.match("Num")
            self.match("]")
        self.match("semicolon")

    def declaration(self):
        if self.current_token.type == "specifier_type":
            self.var_declaration()
        else:
            self.error()

    def parse(self):
        self.current_token = self.tokens[0]
        self.declaration()
        return self.errors
