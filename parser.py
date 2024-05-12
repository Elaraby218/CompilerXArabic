class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0
        self.errors = []

    def match(self, token_type):
        if self.current_token and self.current_token.is_token(token_type):
            self.consume()
        else:
            self.error(self.current_token, token_type)

    def consume(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token.type = "EOF"
            self.current_token.value = ""

    def error(self, found_token=None, expected_type=None):
        if found_token and expected_type:
            self.errors.append(f"Error: Expected {expected_type} but found {found_token}")
        else:
            self.errors.append("Error: Invalid syntax")

    def parameter_list(self):
        if self.current_token.is_token("("):
            self.match("(")
            while not self.current_token.is_token(")") and not self.current_token.is_token("EOF"):
                self.match("specifier_type")
                self.match("ID")
                if self.current_token.is_token("["):
                    self.match("[")
                    if self.current_token.is_token("Num"):
                        self.match("Num")
                    self.match("]")
                if self.current_token.is_token(","):
                    self.match(",")
                    if self.current_token.is_token(")"):
                        self.error(self.current_token, "specifier_type")
                else:
                    break
            self.match(")")
        else:
            self.error()

    def function_declaration(self):
        self.parameter_list()

    def var_declaration(self):
        if self.current_token.is_token("="):
            self.match("=")
            self.match("Num")
        if self.current_token.is_token("["):
            self.match("[")
            self.match("Num")
            self.match("]")
        self.match("semicolon")

    def declaration(self):
        if self.current_token.is_token("specifier_type"):
            self.match("specifier_type")
            self.match("ID")
            if self.current_token.is_token("("):
                self.function_declaration()
            else:
                self.var_declaration()

    def parse(self):
        self.current_token = self.tokens[0]
        self.declaration()
        return self.errors
