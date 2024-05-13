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

    def reco_stmt(self):
        if self.current_token.is_token("specifier_type"):
            self.declaration()
        if self.current_token.is_token("if_stmt"):
            self.if_condition()
            if self.current_token.is_token("else_stmt"):
                self.else_condition()

    def declaration(self):
        if self.current_token.is_token("specifier_type"):
            self.match("specifier_type")
            self.match("ID")
            if self.current_token.is_token("("):
                self.function_declaration()
            else:
                self.var_declaration()
        self.reco_stmt()

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

    def if_condition(self):
        if self.current_token.is_token("if_stmt"):
            self.match("if_stmt")
            self.match("(")
            # self.reco_stmt() need to implement expresion stmt
            self.match(")")
            self.match("{")
            self.reco_stmt()
            self.match("}")

    def else_condition(self):
        if self.current_token.is_token("else_stmt"):
            self.match("else_stmt")
            self.match("{")
            self.reco_stmt()
            self.match("}")

    def iteration_stmt(self):
        if self.current_token.is_token("iteration"):
            self.match("iteration")
            self.match("(")
            # we need to match expression here
            self.match(")")
            self.match("{")
            # reco
            self.match("}")

    def return_stmt(self):
        if self.current_token.is_token("return"):
            self.match("return")
            if self.current_token.is_token("semicolon"):
                self.match("semicolon")
            else:
                self.expression()
                self.match("semicolon")  # second error

    def expression(self):
        if self.current_token.is_token("ID"):
            self.var()
            if self.current_token.is_token("="):
                self.match("=")
                if self.current_token.is_token("ID"):
                    self.expression()
        else:
            self.simple_expression()

    def var(self):
        if self.current_token.is_token("ID"):
            self.match("ID")
            if self.current_token.is_token("["):
                self.match("[")
                self.expression()
                self.match("]")  # first error
        elif self.current_token.is_token("["):
            self.match("[")
            self.expression()
            self.match("]")

    def simple_expression(self):
        self.additive_expression()
        if self.current_token.is_token("relOp"):
            self.match("relOp")
            self.additive_expression()

    def additive_expression(self):
        self.term()
        if self.current_token.is_token("addOp"):
            self.match("addOp")
            self.additive_expression()

    def term(self):
        self.factor()
        if self.current_token.is_token("mulOp"):
            self.match("mulOp")
            self.term()

    def factor(self):
        if self.current_token.is_token("("):
            self.match("(")
            self.expression()
            self.match(")")
        elif self.current_token.is_token("Num"):
            self.match("Num")
        elif self.current_token.is_token("ID"):
            self.match("ID")
            if self.current_token.is_token("("):
                self.call()
            else:
                self.var()

    def call(self):
        if self.current_token.is_token("ID"):
            self.match("ID")
            self.match("(")
            self.args()
            self.match(")")

    def args(self):
        if not (self.current_token.is_token(")")):
            self.args_list()

    def args_list(self):
        self.expression()
        if self.current_token.is_token(","):
            self.match(",")
            self.args_list()

    def parse(self):
        if not self.tokens:
            self.errors.append("Error: No tokens to parse")
            return self.errors
        self.current_token = self.tokens[0]
        self.return_stmt()
        return self.errors