from gui import GUI
from tokenizer import Tokenizer
from parser import Parser
import requests
import threading
import os
import time
import git # pip install GitPython

# Global variables
update_result = "Not checked yet"
tests_list = []
current_test_index = 0
SentMessages = []

def formate_message(inputText, outputTokens, outputSyntax):
    if not inputText: inputText = "Empty input\n"
    if not outputTokens: outputTokens = "No tokens\n"
    if not outputSyntax: outputSyntax = "No syntax\n"
    return f"\n\nInput from {os.getenv("USERNAME")}: `Update-Status: {update_result}`\n```{inputText}\n```\nTokens:\n```\n{outputTokens}\n```\nSyntax:\n```\n{outputSyntax}\n```\n═════════════════════════════════════════════════════════════════════════════════════════════════"

def send_message_to_bot(message):
    if message in  SentMessages: return
    SentMessages.append(message)
    url = 'http://ro05.pylex.me:10337/send-message'
    data = {'message': message}

    # Define a function to send the request in a separate thread
    def send_request():
        requests.post(url, json=data)

    # Start a new thread to send the request
    threading.Thread(target=send_request).start()

def run_with_timeout(func):
    result = [None]  # Using a list to store the result as it's mutable

    def target():
        result[0] = func()

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout=3)  # Wait for 3 seconds

    if thread.is_alive():
        print(f"Function {func.__name__} exceeded 3 seconds")

    return result[0] if not thread.is_alive() else "Exceeded 3 seconds"

def main_output(inputText):
    tokens = run_with_timeout(lambda: Tokenizer().tokenize(inputText))
    outputTokens = "\n".join([f"{token.type}: {token.value}" for token in tokens])
    syntax = run_with_timeout(lambda: Parser(tokens).parse())
    outputSyntax = "\n".join(syntax) if syntax else "Parsing successful"
    return (outputTokens, outputSyntax)

# Parse input function
def parse_input():
    global tests_list, current_test_index
    input_text = gui.get_input_text()
    tokens_output, syntax_output = main_output(input_text)
    gui.set_output_text(syntax_output)
    update_test_list(input_text)
    send_message_to_bot(formate_message(input_text, tokens_output, syntax_output))

# Tokenize input function
def tokenize_input():
    global tests_list, current_test_index
    input_text = gui.get_input_text()
    tokens_output, syntax_output = main_output(input_text)
    gui.set_output_text(tokens_output)
    update_test_list(input_text)
    send_message_to_bot(formate_message(input_text, tokens_output, syntax_output))

# Show next test function
def show_next_test():
    if not tests_list: return
    global current_test_index
    current_test_index = (current_test_index + 1) % len(tests_list)
    gui.set_input_text(tests_list[current_test_index])


# Show previous test function
def show_previous_test():
    if not tests_list: return
    global current_test_index
    current_test_index = (current_test_index - 1) % len(tests_list)
    gui.set_input_text(tests_list[current_test_index])

# Clear boxes function
def clear_boxes():
    gui.clear_boxes()

def check_for_updates_async():
    # Define a function to be executed in the new thread
    def check_updates():
        global update_result
        repo = git.Repo('.')
        origin = repo.remotes.origin
        origin.fetch()
        current_commit = repo.head.commit
        latest_remote_commit = origin.refs.master.commit  # Assuming you are checking the 'master' branch, change if necessary
        if current_commit == latest_remote_commit:
            update_result = "Up to date ✅"
        else:
            update_result = "Warning: Outdated 🟥"

    # Create a new thread and start it
    update_thread = threading.Thread(target=check_updates)
    update_thread.start()

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


# Update test list function
def update_test_list(new_test):
    if new_test == "": return
    global tests_list
    global current_test_index
    if new_test not in tests_list:
        tests_list.append(new_test)
        with open("Tests.txt", "a" , encoding="UTF-8") as file:
            file.write(f"{new_test}\n###\n")
    current_test_index = len(tests_list) - 1


check_for_updates_async()
tests_list = read_tests_from_file()


# Initialize GUI
gui = GUI(tokenize_command=tokenize_input, parse_command=parse_input, clear_command=clear_boxes,
          show_next_command=show_next_test, show_previous_command=show_previous_test)
gui.run()