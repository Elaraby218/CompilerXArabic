from gui import GUI
from tokenizer import Tokenizer
from parser import Parser

def tokenize_input():
    input_text = gui.get_input_text()
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(input_text)
    output_text = ""
    for token in tokens:
        output_text += f"{token[0]}: {token[1]}\n"
    gui.set_output_text(output_text)

def parse_input():
    input_text = gui.get_input_text()
    tokenizer = Tokenizer()
    parser = Parser(tokenizer.tokenize(input_text))
    errors = parser.parse()
    output_text = ""
    if errors:
        for error in errors:
            output_text += error + "\n"
    else:
        output_text += "Parsing successful\n"
    gui.set_output_text(output_text)

def clear_boxes():
    gui.clear_boxes()

gui = GUI(tokenize_command=tokenize_input, parse_command=parse_input, clear_command=clear_boxes)
gui.run()
