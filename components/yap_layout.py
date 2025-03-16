import tkinter as tk
from .side_panel import SidePanel
from .request_body import RequestBodyFrame
from tkinter import ttk

class YapLayout(tk.Tk):
    def __init__(self):
        super().__init__()

        self.state = {}

        self.title("Modular Side Panel Example")
        self.geometry("800x500")

        # Create a PanedWindow for resizable layout
        self.paned_window = tk.PanedWindow(self, orient="horizontal")
        self.paned_window.pack(fill="both", expand=True)

        # Create and add the Side Panel
        self.side_panel = SidePanel(self.paned_window)
        self.paned_window.add(self.side_panel)

        # Create and add the Main Content Area
        self.create_main_area()

        # Set minimum sizes for resizable effect
        self.paned_window.paneconfig(self.side_panel, minsize=100)

    def create_main_area(self):
        """Creates the main content area."""
        self.main_area = tk.Frame(self.paned_window, bg="white")
        self.paned_window.add(self.main_area)

        input_area = tk.Frame(self.main_area)
        input_area.pack(fill="x", padx=10, pady=(0, 10))  # Placed below main_area

        # Configure grid columns for input_area
        input_area.columnconfigure(0, weight=0)  # Dropdown stays fixed
        input_area.columnconfigure(1, weight=1)  # Entry expands
        input_area.columnconfigure(2, weight=0)  # Button stays fixed

        # Dropdown for HTTP methods
        options = ["GET", "POST", "PUT", "DELETE"]
        method_var = tk.StringVar(value=options[0])  # Default to GET
        dropdown = ttk.Combobox(input_area, textvariable=method_var, values=options, state="readonly", width=7)
        dropdown.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        # Entry field
        entry = tk.Entry(input_area)
        entry.grid(row=0, column=1, padx=(0, 5), sticky="ew")

        # Submit button
        button = tk.Button(input_area, text="Submit")
        button.grid(row=0, column=2, sticky="ew")

        # Request Body Frame (Make sure to pack it)
        self.request_area = RequestBodyFrame(self.main_area)
        self.request_area.pack(fill="both", padx=10, pady=2)

        self.paned_window.paneconfig(self.main_area, minsize=200)
