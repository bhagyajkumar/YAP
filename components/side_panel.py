import tkinter as tk
from tkinter import ttk, simpledialog
from ttkbootstrap import Style
import json
import os
import uuid

REQUESTS_FILE = "requests.json"

class SidePanel(tk.Frame):
    """Side panel for managing collections and requests."""

    def __init__(self, parent):
        super().__init__(parent, width=250, bg="lightgray")
        self.pack_propagate(False)  # Prevent shrinking
        self.style = Style(theme="darkly")  # Apply Bootstrap theme
        self.create_treeview()
        self.create_context_menu()
        self.parent = parent

    def create_treeview(self):
        """Creates a Treeview widget for collections and requests."""
        self.tree = ttk.Treeview(self, style="Treeview")
        self.tree.pack(expand=True, fill="both", padx=5, pady=5)

        # Sample collections and requests
        self.collections = self.tree.insert("", "end", text="Collections", open=True)
        self.load_requests()

        # Bind right-click event
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.save_requests()

    def create_context_menu(self):
        """Creates a right-click context menu."""
        self.context_menu = tk.Menu(self, tearoff=0, bg="white", fg="black")
        self.context_menu.add_command(label="New Collection", command=self.new_collection)
        self.context_menu.add_command(label="New Request", command=self.new_request)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Rename", command=self.rename_item)
        self.context_menu.add_command(label="Delete", command=self.delete_item)

    def show_context_menu(self, event):
        """Displays the context menu at the cursor position."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.selected_item = item
            self.context_menu.post(event.x_root, event.y_root)

    def new_collection(self):
        """Creates a new collection."""
        name = simpledialog.askstring("New Collection", "Enter collection name:")
        if name:
            uid = str(uuid.uuid4())  # Generate UUID
            self.tree.insert(self.collections, "end", text=name, values=(uid,))
            self.save_requests()

    def new_request(self):
        """Creates a new request under a selected collection."""
        parent = self.tree.parent(self.selected_item)
        if parent == self.collections or self.selected_item == self.collections:
            name = simpledialog.askstring("New Request", "Enter request name:")
            if name:
                uid = str(uuid.uuid4())
                self.tree.insert(self.selected_item, "end", text=name, values=(uid,))
                self.save_requests()
        else:
            print("Select a collection to add a request.")

    def rename_item(self):
        """Handles renaming a collection or request."""
        name = simpledialog.askstring("Rename", "Enter new name:")
        if name:
            self.tree.item(self.selected_item, text=name)
            self.save_requests()

    def delete_item(self):
        """Handles deleting a collection or request."""
        self.tree.delete(self.selected_item)
        self.save_requests()


    def save_requests(self):
        """Saves the current requests and collections to a JSON file with UUIDs."""

        def get_children(parent):
            children = self.tree.get_children(parent)
            return [{"text": self.tree.item(child, "text"),
                     "uuid": self.tree.item(child, "values")[0],  # Get stored UUID
                     "children": get_children(child)} for child in children]

        requests = get_children(self.collections)

        with open(REQUESTS_FILE, "w") as f:
            json.dump(requests, f, indent=4)


    def load_requests(self):
        """Loads requests from JSON file and restores UUIDs."""
        if os.path.exists(REQUESTS_FILE):
            with open(REQUESTS_FILE, "r") as f:
                layout = json.load(f)
                self._load_tree(self.collections, layout)

    def _load_tree(self, parent, items):
        """Recursively loads items into the Treeview with UUIDs."""
        for item in items:
            node = self.tree.insert(parent, "end", text=item["text"], values=(item["uuid"],))
            if "children" in item:
                self._load_tree(node, item["children"])
