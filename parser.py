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

    # 8 - params-list -> params-list , param | param
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

    # 12 - statement -> expression-statement | compound-statement | selection-statement | iteration-statement | return-statement
    def statement(self):
        if self.current_token.is_token("specifier_type"):
            self.declaration()
        elif self.current_token.is_token("if_stmt"):
            self.if_condition()
            if self.current_token.is_token("else_stmt"):
                self.else_condition()
        elif self.current_token.is_token("iteration"):
            self.iteration_stmt()
        elif self.current_token.is_token("return"):
            self.return_stmt()
        elif self.is_factor() or self.current_token.is_token("semicolon"):
            self.expression_stmt()

    # 3 - declaration -> var-declaration | function-declaration
    def declaration(self):
        if self.current_token.is_token("specifier_type"):
            self.match("specifier_type")
            self.match("ID")
            if self.current_token.is_token("("):
                self.function_declaration()
            else:
                self.var_declaration()
        self.statement()

    # 6 - function-declaration -> compound-stmt ( params ) ID specifier-type
    def function_declaration(self):
        self.parameter_list()

    # 4 - var-declaration -> var-declaration | fun-declaration
    def var_declaration(self):
        if self.current_token.is_token("="):
            self.match("=")
            self.match("Num")
        if self.current_token.is_token("["):
            self.match("[")
            self.match("Num")
            self.match("]")
        self.match("semicolon")

    # 13 - statement -> selection-statement
    # 15 - selection-statement -> if ( expression ) statement | if ( expression ) statement else statement
    def if_condition(self):
        if self.current_token.is_token("if_stmt"):
            self.match("if_stmt")
            self.match("(")
            self.expression()
            self.match(")")
            self.match("{")
            self.statement()
            self.match("}")
        self.statement()

    # 13 - statement -> selection-statement
    #      selection-statement -> else-stmt
    def else_condition(self):
        if self.current_token.is_token("else_stmt"):
            self.match("else_stmt")
            self.match("{")
            self.statement()
            self.match("}")
        self.statement()

    # 13 - statement -> iteration-statement
    # 16 - iteration-statement -> while ( expression ) statement
    def iteration_stmt(self):
        if self.current_token.is_token("iteration"):
            self.match("iteration")
            self.match("(")
            self.expression()
            self.match(")")
            self.match("{")
            self.statement()
            self.match("}")
        self.statement()

    # 13 - statement -> return-statement
    # 17 - return-statement -> return ; | return expression ;
    def return_stmt(self):
        self.match("return")
        if self.current_token.is_token("semicolon"):
            self.match("semicolon")
        else:
            self.expression()
            self.match("semicolon")  # second error
            # match semicolon could be called one here
        self.statement()

    # 14 - expression-stmt -> expression ; | ;
    def expression_stmt(self):
        if self.current_token.is_token("semicolon"):
            self.match("semicolon")
        else:
            self.expression()
            self.match("semicolon")
        self.statement()

    # 18 - expression -> var = expression | simple-expression
    def expression(self):
        if self.current_token.is_token("ID") and self.tokens[self.index + 1].is_token("="):
            self.var()
            self.match("=")
            self.expression()
        else:
            self.simple_expression()

    # 19 - var -> ID [ expression ] | ID
    def var(self):
        self.match("ID")
        if self.current_token.is_token("["):
            self.match("[")
            self.expression()
            self.match("]")
            # self.match("=")

    # 20 - simple-expression -> additive-expression relop additive-expression | additive-expression
    def simple_expression(self):
        self.additive_expression()
        if self.current_token.is_token("relOp"):
            self.match("relOp")
            self.additive_expression()

    # 22 - additive-expression -> term addOp additive-expression | term
    def additive_expression(self):
        self.term()
        if self.current_token.is_token("addOp"):
            self.match("addOp")
            self.additive_expression()

    # 24 - term -> factor mulOp term | factor
    def term(self):
        self.factor()
        if self.current_token.is_token("mulOp"):
            self.match("mulOp")
            self.term()

    # 26 - factor -> ( expression ) | Num | call | var
    def factor(self):
        if self.current_token.is_token("("):
            self.match("(")
            self.expression()
            self.match(")")
        elif self.current_token.is_token("Num"):
            self.match("Num")
        elif self.current_token.is_token("ID") and self.tokens[self.index + 1].is_token("("):
            self.call()
        else:
            self.var()

    # if the current token is factor then it supposed to be an expression-stmt
    def is_factor(self):
        return (
                self.current_token.is_token("(") or
                self.current_token.is_token("Num") or
                (self.current_token.is_token("ID"))
        )

    # 28 - call -> ID ( args )
    def call(self):
        # if self.current_token.is_token("ID"): from the function that called me i know that the current token is ID
        self.match("ID")
        self.match("(")
        self.args()
        self.match(")")

    # 28 - args -> arg-list | empty
    def args(self):
        if not (self.current_token.is_token(")")):
            self.args_list()

    # 29 - arg-list -> expression , arg-list | expression
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
       # while not self.current_token.is_token("EOF"): # do not remove it, it is important
        self.statement()
        return self.errors
    # this is my branch
