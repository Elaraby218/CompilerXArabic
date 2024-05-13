from gui import GUI
from tokenizer import Tokenizer
from parser import Parser

# Function to read tests from file and populate the global list
def read_tests_from_file():
    try:
        with open("Tests.txt", "r") as file:
            tests = file.read().split("###")
            tests = [test.strip() for test in tests if test.strip()]
            return tests
    except FileNotFoundError:
        print("Tests file not found.")
        return []

# Global variables
tests_list = read_tests_from_file()
current_test_index = 0

# Tokenize input function
def tokenize_input():
    global tests_list, current_test_index
    input_text = gui.get_input_text()
    tokens = Tokenizer().tokenize(input_text)
    output_text = "\n".join([f"{token.type}: {token.value}" for token in tokens])
    gui.set_output_text(output_text)
    update_test_list(input_text)
    update_current_index()

# Parse input function
def parse_input():
    global tests_list, current_test_index
    input_text = gui.get_input_text()
    parser = Parser(Tokenizer().tokenize(input_text))
    errors = parser.parse()
    output_text = "\n".join(errors) if errors else "Parsing successful"
    gui.set_output_text(output_text)
    update_test_list(input_text)
    update_current_index()

# Update test list function
def update_test_list(new_test):
    global tests_list
    if new_test not in tests_list:
        tests_list.append(new_test)
        with open("Tests.txt", "a") as file:
            file.write(f"{new_test}\n###\n")

# Update current index function
def update_current_index():
    global current_test_index
    current_test_index = len(tests_list) - 1

# Show next test function
def show_next_test():
    global current_test_index
    current_test_index = (current_test_index + 1) % len(tests_list)
    gui.set_input_text(tests_list[current_test_index])

# Show previous test function
def show_previous_test():
    global current_test_index
    current_test_index = (current_test_index - 1) % len(tests_list)
    gui.set_input_text(tests_list[current_test_index])

# Clear boxes function
def clear_boxes():
    gui.clear_boxes()

# Initialize GUI
gui = GUI(tokenize_command=tokenize_input, parse_command=parse_input, clear_command=clear_boxes,
          show_next_command=show_next_test, show_previous_command=show_previous_test)
gui.run()
