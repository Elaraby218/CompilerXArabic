import tkinter as tk

class GUI:
    def __init__(self, tokenize_command, parse_command, clear_command, show_next_command, show_previous_command):
        self.root = tk.Tk()
        self.root.title("Token Parser")
        self.root.geometry("600x600")  # Set initial window size

        # Buttons for Next and Previous
        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(pady=5)
        self.next_button = tk.Button(self.navigation_frame, text="Next", command=show_next_command)
        self.next_button.pack(side="left", padx=(5, 0), anchor="w")  # Anchored to the west (leftmost)
        self.previous_button = tk.Button(self.navigation_frame, text="Previous", command=show_previous_command)
        self.previous_button.pack(side="right", padx=(0, 5), anchor="e")  # Anchored to the east (rightmost)

        # Input Box
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5, padx=10, fill="both")
        self.input_label = tk.Label(self.input_frame, text="Input:")
        self.input_label.pack(side="left", padx=(0, 10))
        self.input_box = tk.Text(self.input_frame, height=5, width=50)  # Adjusted size
        self.input_box.pack(fill="both", expand=False)

        # Output Box
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=5, padx=10, fill="both", expand=True)
        self.output_label = tk.Label(self.output_frame, text="Output:")
        self.output_label.pack(side="left", padx=(0, 10))
        self.output_box = tk.Text(self.output_frame, height=20, width=50)  # Adjusted size
        self.output_box.pack(fill="both", expand=True)

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)
        self.tokenize_button = tk.Button(self.button_frame, text="Tokenize", command=tokenize_command)
        self.tokenize_button.pack(side="left", padx=5)
        self.parse_button = tk.Button(self.button_frame, text="Parse", command=parse_command)
        self.parse_button.pack(side="left", padx=5)
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=clear_command)
        self.clear_button.pack(side="left", padx=5)

    def get_input_text(self):
        return self.input_box.get("1.0", "end-1c")

    def set_input_text(self, text):
        self.input_box.delete("1.0", "end")
        self.input_box.insert("end", text)

    def set_output_text(self, text):
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", text)

    def clear_boxes(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")

    def run(self):
        self.root.mainloop()
