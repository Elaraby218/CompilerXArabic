import time
from gui import GUI
from tokenizer import Tokenizer
from parser import Parser
import requests
import threading

# Function to read tests from file and populate the global list
def read_tests_from_file():
    try:
        with open("Tests.txt", "r", encoding="UTF-8") as file:
            tests = file.read().split("###")
            tests = [test.strip() for test in tests if test.strip()]
            return tests
    except FileNotFoundError:
        print("Tests file not found.")
        return []

# Global variables
tests_list = read_tests_from_file()
current_test_index = 0

SentMessages = []
def formate_message(inputText, outputTokens, outputSyntax):
    if not inputText: inputText = "Empty input\n"
    if not outputTokens: outputTokens = "No tokens\n"
    if not outputSyntax: outputSyntax = "No syntax\n"
    if inputText not in SentMessages:
        SentMessages.append(inputText)
        return f"\n\nInput:\n```{inputText}\n```\nTokens:\n```\n{outputTokens}\n```\nSyntax:\n```\n{outputSyntax}\n```\n═════════════════════════════════════════════════════════════════════════════════════════════════"




def run_with_timeout(func):
    result = [None]  # Using a list to store the result as it's mutable

    def target():
        result[0] = func()

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout=3)  # Wait for 3 seconds

    return result[0] if not thread.is_alive() else "Exceeded 3 seconds"


def main_output(inputText):
    tokens = run_with_timeout(lambda: Tokenizer().tokenize(inputText))
    outputTokens = "\n".join([f"{token.type}: {token.value}" for token in tokens])
    syntax = run_with_timeout(lambda: Parser(tokens).parse())
    outputSyntax = "\n".join(syntax) if syntax else "Parsing successful"
    return (outputTokens, outputSyntax)

# Tokenize input function
def tokenize_input():
    global tests_list, current_test_index
    input_text = gui.get_input_text()
    tokens_output, syntax_output = main_output(input_text)

    gui.set_output_text(tokens_output)

    update_test_list(input_text)
    update_current_index()

    send_message_to_bot(formate_message(input_text, tokens_output, syntax_output))

# Parse input function
def parse_input():
    global tests_list, current_test_index
    input_text = gui.get_input_text()

    tokens_output, syntax_output = main_output(input_text)

    gui.set_output_text(syntax_output)
    update_test_list(input_text)
    update_current_index()

    send_message_to_bot(formate_message(input_text, tokens_output, syntax_output))


def send_message_to_bot(message):
    url = 'http://ro05.pylex.me:10337/send-message'
    data = {'message': message}

    # Define a function to send the request in a separate thread
    def send_request():
        requests.post(url, json=data)

    # Start a new thread to send the request
    threading.Thread(target=send_request).start()

# Update test list function
def update_test_list(new_test):
    if new_test == "": return
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
    if not tests_list: return
    current_test_index = (current_test_index + 1) % len(tests_list)
    gui.set_input_text(tests_list[current_test_index])

# Show previous test function
def show_previous_test():
    global current_test_index
    if not tests_list: return
    current_test_index = (current_test_index - 1) % len(tests_list)
    gui.set_input_text(tests_list[current_test_index])

# Clear boxes function
def clear_boxes():
    gui.clear_boxes()

# Initialize GUI
gui = GUI(tokenize_command=tokenize_input, parse_command=parse_input, clear_command=clear_boxes,
          show_next_command=show_next_test, show_previous_command=show_previous_test)
gui.run()
