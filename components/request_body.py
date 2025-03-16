import customtkinter as ctk
import json
import re

class RequestBodyFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Configure grid layout (Fixed Side Panel)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Content is resizable
        self.grid_columnconfigure(1, weight=0)  # Fixed side panel

        # Create a scrollable Textbox
        self.text = ctk.CTkTextbox(self, wrap="word", font=("Courier", 12))
        self.text.grid(row=0, column=0, sticky="nsew", padx=(0, 0), pady=0)

        # Disable side panel resizing
        self.columnconfigure(1, weight=0)

        # Configure syntax highlighting colors
        self.colors = {
            "key": "#56B6C2",
            "string": "#98C379",
            "number": "#D19A66",
            "boolean": "#E06C75",
            "null": "#C678DD"
        }

        # Bracket colors
        self.bracket_colors = ["#56B6C2", "#D19A66", "#C678DD", "#98C379", "#E06C75"]

        # Bind event for highlighting
        self.text.bind("<KeyRelease>", lambda event: self.highlight_json())

    def highlight_json(self):
        """ Apply syntax highlighting to JSON text """
        text = self.text.get("1.0", "end-1c")

        try:
            json.loads(text)  # Validate JSON
        except json.JSONDecodeError:
            return  # Skip highlighting if JSON is invalid

        # Clear previous formatting
        self.text.configure(state="normal")
        self.text.tag_remove("all", "1.0", "end")

        # Regex patterns for JSON elements
        patterns = {
            "key": r'(?P<key>"[^"]*")\s*:',
            "string": r'(:\s*)(?P<string>"[^"]*")',
            "number": r'(:\s*)(?P<number>-?\d+(\.\d+)?)',
            "boolean": r'(:\s*)(?P<boolean>true|false)',
            "null": r'(:\s*)(?P<null>null)'
        }

        # Apply syntax highlighting
        for tag, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                if tag in match.groupdict():
                    start, end = match.span(tag)
                    self.text.tag_add(tag, f"1.0+{start}c", f"1.0+{end}c")
                    self.text.tag_config(tag, foreground=self.colors[tag])

        # Apply bracket highlighting
        self.highlight_brackets(text)

    def highlight_brackets(self, text):
        """ Highlight matching brackets `{}` and `[]` """
        stack = []

        for i, char in enumerate(text):
            if char in "{}[]":
                if char in "{[":
                    stack.append((i, char))
                elif char in "}]":
                    if stack:
                        start_idx, _ = stack.pop()
                        depth = len(stack) % len(self.bracket_colors)
                        color = self.bracket_colors[depth]

                        # Highlight both opening and closing brackets
                        self.text.tag_add(f"bracket_{depth}", f"1.0+{start_idx}c", f"1.0+{start_idx+1}c")
                        self.text.tag_add(f"bracket_{depth}", f"1.0+{i}c", f"1.0+{i+1}c")
                        self.text.tag_config(f"bracket_{depth}", foreground=color)
