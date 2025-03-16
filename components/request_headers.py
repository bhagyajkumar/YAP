import customtkinter as ctk

class HeadersTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.headers = []  # List to store header rows

        # Frame to hold header fields
        self.headers_frame = ctk.CTkFrame(self)
        self.headers_frame.pack(fill="x", padx=10, pady=5)

        self.add_header_fields()  # Add an initial header row

        # "Add Header" button positioned properly
        self.add_button = ctk.CTkButton(self, text="Add Header", command=self.add_header_fields)
        self.add_button.pack(pady=5, padx=10, anchor="w")

    def add_header_fields(self):
        """Adds a new row of key-value input fields for headers with a delete button."""
        row = len(self.headers)

        key_entry = ctk.CTkEntry(self.headers_frame, width=150)
        key_entry.grid(row=row, column=0, padx=5, pady=2)

        value_entry = ctk.CTkEntry(self.headers_frame, width=150)
        value_entry.grid(row=row, column=1, padx=5, pady=2)

        delete_button = ctk.CTkButton(self.headers_frame, text="X", width=30, fg_color="red", command=lambda: self.delete_header(row))
        delete_button.grid(row=row, column=2, padx=5, pady=2)

        self.headers.append((key_entry, value_entry, delete_button))

    def delete_header(self, row):
        """Deletes the selected header row."""
        if row < len(self.headers):
            key_entry, value_entry, delete_button = self.headers.pop(row)

            # Remove widgets
            key_entry.destroy()
            value_entry.destroy()
            delete_button.destroy()

            # Reorder the remaining rows
            self.reorder_headers()

    def reorder_headers(self):
        """Reorders the header rows after deletion."""
        for i, (key_entry, value_entry, delete_button) in enumerate(self.headers):
            key_entry.grid(row=i, column=0, padx=5, pady=2)
            value_entry.grid(row=i, column=1, padx=5, pady=2)
            delete_button.grid(row=i, column=2, padx=5, pady=2, sticky="w")

    def get_headers(self):
        """Returns a dictionary of headers."""
        return {key.get(): value.get() for key, value, _ in self.headers if key.get()}

# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Optional: Set theme
    root = ctk.CTk()
    root.title("Headers Tab Example")
    root.geometry("500x300")

    headers_tab = HeadersTab(root)
    headers_tab.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()
