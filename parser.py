class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0
        self.errors = []
        self.rules_called = []

    def track_function(func):
        def wrapper(self, *args, **kwargs):
            self.rules_called.append(func.__name__)
            return func(self, *args, **kwargs)  # Call the original method

        return wrapper

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







    # 1 - program -> declaration-list
    @track_function
    def program(self):
        self.declaration_list()

    # 2 - declaration-list -> declaration-list declaration | declaration
    @track_function
    def declaration_list(self):
        while not self.current_token.is_token("EOF"):
            self.declaration()

    # 3 - declaration -> var-declaration | function-declaration
    @track_function
    def declaration(self):
        if self.current_token.is_token("specifier_type"):
            self.match("specifier_type")
            self.match("ID")
            if self.current_token.is_token("("):
                self.fun_declaration()
            else:
                self.var_declaration()
        else:
            self.errors.append(
                f"Error: Expected specifier type but found {self.current_token.value} at line {self.current_token.line}")
            self.consume()
        #  self.statement()

    # 4 - var-declaration -> type-specifier ID ; | type-specifier ID [ Num ] ;
    # Accepted Test Cases:
    # صحيح س؛
    # صحيح س[5];
    @track_function
    def var_declaration(self):
        if self.current_token.is_token("="):
            self.match("=")
            self.match("Num")
        elif self.current_token.is_token("["):
            self.match("[")
            self.match("Num")
            self.match("]")
        self.match("semicolon")

    # 6 - function-declaration -> compound-stmt ( params ) ID specifier-type
    @track_function
    def fun_declaration(self):
        self.match("(")
        self.params()
        self.match(")")
        self.compound_stmt()

    # 7 - params -> params-list | void
    @track_function
    def params(self):
        if self.current_token.is_token("specifier_type"):
            self.parameter_list()
        else:
            self.void_till_end_of_line()

    @track_function
    def void_till_end_of_line(self):
        line = self.current_token.line
        not_void_list = []
        while self.current_token.line == line and not self.current_token.is_token(
                ")") and not self.current_token.is_token("EOF"):
            not_void_list.append(self.current_token.value)
            self.consume()

        if not_void_list:
            not_void_list = " ".join(not_void_list)
            self.errors.append(f"Error: Expected params or empty but found {not_void_list} at line {line}")

    # 8 - params-list -> params-list , param | param
    @track_function
    def parameter_list(self):
        self.param()
        if self.current_token.is_token(","):  # if it is not comma it should be close bract
            self.match(",")
            self.parameter_list()

    # 9 - param -> type-specifier ID | type-specifier ID [ ]
    @track_function
    def param(self):
        self.match("specifier_type")
        self.match("ID")
        if self.current_token.is_token("["):
            self.match("[")
            self.match("]")

    # 10 - compound-stmt -> { local-declarations statement-list }
    @track_function
    def compound_stmt(self):
        self.match("{")
        if self.current_token.is_token("specifier_type"):
            self.local_declarations()
        elif not self.current_token.is_token("}"):
            self.statement_list()
        self.match("}")
        self.statement()

    # 11 - local-declarations -> local-declarations var-declaration | empty
    @track_function
    def local_declarations(self):
        while self.current_token.is_token("specifier_type"):
            self.match("specifier_type")
            self.match("ID")
            self.var_declaration()

    # 12 - stmt-list -> stmt-list statement | empty
    def statement_list(self):
        while not self.current_token.is_token("}") and not self.current_token.is_token("EOF"):
            self.statement()

    # 13 - statement -> expression-statement | compound-statement | selection-statement | iteration-statement | return-statement
    @track_function
    def statement(self):
        if self.current_token.is_token("{"):
            self.compound_stmt()
            return
        elif self.current_token.is_token("if_stmt"):
            self.if_condition()
            return
        elif self.current_token.is_token("iteration"):
            self.iteration_stmt()
            return
        elif self.current_token.is_token("return"):
            self.return_stmt()
            return
        elif self.is_factor() or self.current_token.is_token("semicolon"):
            self.expression_stmt()
            return
        elif self.current_token.is_token("else_stmt"):
            self.errors.append(f"Else statement can not be without IF stmt {self.current_token.line} .. ")
            self.consume()

    # 13 - statement -> selection-statement
    # 15 - selection-statement -> if ( expression ) statement | if ( expression ) statement else statement
    @track_function
    def if_condition(self):
        if self.current_token.is_token("if_stmt"):
            self.match("if_stmt")
            self.match("(")
            self.expression()
            self.match(")")
            self.match("{")
            self.statement()
            self.match("}")
            if self.current_token.is_token("else_stmt"):
                self.match("else_stmt")
                self.match("{")
                self.statement()
                self.match("}")
            else:
                self.statement()
        self.statement()

    # 13 - statement -> selection-statement
    #      selection-statement -> else-stmt

    # 13 - statement -> iteration-statement
    # 16 - iteration-statement -> while ( expression ) statement
    @track_function
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
    @track_function
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
    @track_function
    def expression_stmt(self):
        if self.current_token.is_token("semicolon"):
            self.match("semicolon")
        else:
            self.expression()
            self.match("semicolon")
        self.statement()

    # 18 - expression -> var = expression | simple-expression
    @track_function
    def expression(self):
        if self.current_token.is_token("ID") and self.tokens[self.index + 1].is_token("="):
            self.var()
            self.match("=")
            self.expression()
        else:
            self.simple_expression()

    # 19 - var -> ID [ expression ] | ID
    @track_function
    def var(self):
        self.match("ID")
        if self.current_token.is_token("["):
            self.match("[")
            self.expression()
            self.match("]")
            # self.match("=")

    # 20 - simple-expression -> additive-expression relop additive-expression | additive-expression
    @track_function
    def simple_expression(self):
        self.additive_expression()
        if self.current_token.is_token("relOp"):
            self.match("relOp")
            self.additive_expression()

    # 22 - additive-expression -> term addOp additive-expression | term
    @track_function
    def additive_expression(self):
        self.term()
        if self.current_token.is_token("addOp"):
            self.match("addOp")
            self.additive_expression()

    # 24 - term -> factor mulOp term | factor
    @track_function
    def term(self):
        self.factor()
        if self.current_token.is_token("mulOp"):
            self.match("mulOp")
            self.term()

    # 26 - factor -> ( expression ) | Num | call | var
    @track_function
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
    @track_function
    def is_factor(self):
        return (
                self.current_token.is_token("(") or
                self.current_token.is_token("Num") or
                (self.current_token.is_token("ID"))
        )

    # 28 - call -> ID ( args )
    @track_function
    def call(self):
        # if self.current_token.is_token("ID"): from the function that called me i know that the current token is ID
        self.match("ID")
        self.match("(")
        self.args()
        self.match(")")

    # 28 - args -> arg-list | empty
    @track_function
    def args(self):
        if not (self.current_token.is_token(")")):
            self.args_list()

    # 29 - arg-list -> expression , arg-list | expression
    @track_function
    def args_list(self):
        self.expression()
        if self.current_token.is_token(","):
            self.match(",")
            self.args_list()

    @track_function
    def parse(self):
        if not self.tokens:
            self.errors.append("Error: No tokens to parse")
            return (self.errors, self.rules_called)
        self.current_token = self.tokens[0]
        # while not self.current_token.is_token("EOF"): # do not remove it, it is important
        self.program()
        return (self.errors, self.rules_called)
