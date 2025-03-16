import customtkinter as ctk

from components.request_body import RequestBodyFrame
from components.request_headers import HeadersTab

class RequestTabs(ctk.CTkTabview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Add tabs
        self.headers_tab = self.add("Headers")
        self.body_tab = self.add("Body")
        self.params_tab = self.add("Params")
        self.auth_tab = self.add("Auth")

        # Initialize content
        self.create_headers_tab()
        self.create_body_tab()
        self.create_params_tab()
        self.create_auth_tab()

    def create_headers_tab(self):

        self.headers_component = HeadersTab(self.headers_tab)
        self.headers_component.pack(fill="both", expand=True, padx=10, pady=10)

        # ctk.CTkLabel(self.headers_tab, text="Key:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # self.headers_key = ctk.CTkEntry(self.headers_tab, width=200)
        # self.headers_key.grid(row=0, column=1, padx=10, pady=5)

        # ctk.CTkLabel(self.headers_tab, text="Value:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        # self.headers_value = ctk.CTkEntry(self.headers_tab, width=200)
        # self.headers_value.grid(row=1, column=1, padx=10, pady=5)

    def create_body_tab(self):
        self.body = RequestBodyFrame(self.body_tab)
        self.body.pack(pady=10, padx=10, fill="both", expand=True)

    def create_params_tab(self):
        ctk.CTkLabel(self.params_tab, text="Param Key:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.params_key = ctk.CTkEntry(self.params_tab, width=200)
        self.params_key.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.params_tab, text="Param Value:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.params_value = ctk.CTkEntry(self.params_tab, width=200)
        self.params_value.grid(row=1, column=1, padx=10, pady=5)

    def create_auth_tab(self):
        ctk.CTkLabel(self.auth_tab, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.auth_username = ctk.CTkEntry(self.auth_tab, width=200)
        self.auth_username.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.auth_tab, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.auth_password = ctk.CTkEntry(self.auth_tab, width=200, show="*")  # Mask password
        self.auth_password.grid(row=1, column=1, padx=10, pady=5)

# Example usage
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("600x400")

    tabs = RequestTabs(root)
    tabs.pack(fill="both", expand=True, padx=20, pady=20)

    root.mainloop()
