import tkinter as tk
from tkinter import ttk
import json
import re

class RequestBodyFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Configure grid layout for resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a scrollable Text widget
        self.text = tk.Text(self, wrap="word", undo=True, font=("Courier", 12))
        self.text.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, command=self.text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 10))
        self.text.config(yscrollcommand=scrollbar.set)

        # Configure syntax highlighting tags
        self.text.tag_configure("key", foreground="blue")
        self.text.tag_configure("string", foreground="green")
        self.text.tag_configure("number", foreground="purple")
        self.text.tag_configure("boolean", foreground="red")
        self.text.tag_configure("null", foreground="orange")

        # Bracket matching colors (alternating for depth levels)
        self.bracket_colors = ["blue", "purple", "orange", "green", "red"]
        for i, color in enumerate(self.bracket_colors):
            self.text.tag_configure(f"bracket_{i}", foreground=color)

        # Bind event to trigger highlighting
        self.text.bind("<KeyRelease>", lambda event: self.highlight_json())

    def highlight_json(self):
        """ Apply syntax highlighting to JSON text and bracket matching """
        text = self.text.get("1.0", "end-1c")

        try:
            json.loads(text)  # Validate JSON
        except json.JSONDecodeError:
            return  # Skip highlighting if JSON is invalid

        # Remove existing highlights
        for tag in ["key", "string", "number", "boolean", "null"]:
            self.text.tag_remove(tag, "1.0", "end")

        # Remove old bracket highlights
        for i in range(len(self.bracket_colors)):
            self.text.tag_remove(f"bracket_{i}", "1.0", "end")

        # Regex patterns for JSON elements
        patterns = {
            "key": r'(?P<key>"[^"]*")\s*:',   # Matches keys: `"key":`
            "string": r'(:\s*)(?P<string>"[^"]*")',  # Matches values: `: "value"`
            "number": r'(:\s*)(?P<number>-?\d+(\.\d+)?)',  # Matches numbers: `: 123, -12.5`
            "boolean": r'(:\s*)(?P<boolean>true|false)',  # Matches true/false
            "null": r'(:\s*)(?P<null>null)'  # Matches null
        }

        # Apply highlighting for JSON syntax
        for tag, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                if tag in match.groupdict():
                    start, end = match.span(tag)
                    self.text.tag_add(tag, f"1.0+{start}c", f"1.0+{end}c")

        # Apply bracket highlighting
        self.highlight_brackets(text)

    def highlight_brackets(self, text):
        """ Highlight matching brackets `{}` and `[]` with alternating colors """
        stack = []  # Stack to keep track of bracket depth

        for i, char in enumerate(text):
            if char in "{}[]":
                if char in "{[":
                    stack.append((i, char))  # Push opening bracket with position
                elif char in "}]":
                    if stack:
                        start_idx, opening_bracket = stack.pop()
                        depth = len(stack) % len(self.bracket_colors)  # Cycle colors
                        color_tag = f"bracket_{depth}"

                        # Highlight opening and closing brackets
                        self.text.tag_add(color_tag, f"1.0+{start_idx}c", f"1.0+{start_idx+1}c")
                        self.text.tag_add(color_tag, f"1.0+{i}c", f"1.0+{i+1}c")
