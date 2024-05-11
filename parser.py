class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0
        self.errors = []

    def consume(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def match(self, expected_type):
        if self.current_token and self.current_token[0] == expected_type:
            self.consume()
        else:
            self.error()

    def error(self):
        if self.current_token:
            self.errors.append(f"Error: Unexpected token '{self.current_token[1]}'")
        else:
            self.errors.append("Error: Unexpected end of input")

    def declaration(self):
        if self.current_token[0] == "specifier_type":
            self.consume()
            self.match("ID")
            self.match("semicolon")
        else:
            self.error()

    def parse(self):
        self.current_token = self.tokens[0]
        self.declaration()
        return self.errors
