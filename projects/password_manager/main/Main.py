import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import random
import string
import pyperclip

class PasswordManager:
    def __init__(self, master_password=None):
        self.master_password = master_password
        self.passwords_file = 'passwords.json'
        self.passwords = self.load_passwords()

    def load_passwords(self):
        try:
            with open(self.passwords_file, 'r') as file:
                passwords_data = json.load(file)
                master_passwords = passwords_data.get('master_passwords', [])
                return {'master_passwords': master_passwords, 'passwords': passwords_data.get('passwords', {})}
        except (FileNotFoundError, json.JSONDecodeError):
            return {'master_passwords': [], 'passwords': {}}

    def save_passwords(self):
        with open(self.passwords_file, 'w') as file:
            json.dump({'master_passwords': self.passwords['master_passwords'], 'passwords': self.passwords['passwords']}, file)

    def save_master_password(self, master_password):
        if master_password not in self.passwords['master_passwords']:
            self.passwords['master_passwords'].append(master_password)
            self.save_passwords()
            return True
        else:
            return False

    def set_active_master_password(self, master_password):
        self.master_password = master_password

    def save_password(self, service, username, password):
        if service not in self.passwords:
            self.passwords['passwords'][service] = {}
        self.passwords['passwords'][service][username] = password
        self.save_passwords()

    def get_password(self, service, username):
        if service in self.passwords['passwords'] and username in self.passwords['passwords'][service]:
            return self.passwords['passwords'][service][username]
        else:
            return None

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.password_manager = None

        self.create_widgets()

    def create_widgets(self):
        self.label_password = tk.Label(self.root, text="Master Password:")
        self.entry_password = tk.Entry(self.root, show="*")
        self.button_login = tk.Button(self.root, text="Login", command=self.login)

        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_login.pack(pady=10)

        # Always prompt to create a master password
        self.create_master_password()

    def create_master_password(self):
        response = messagebox.askyesno("Create Master Password", "Do you want to create a master password?")
        if response:
            master_password = simpledialog.askstring("Create Master Password", "Set your master password:")
            if master_password:
                self.password_manager = PasswordManager()
                if self.password_manager.save_master_password(master_password):
                    messagebox.showinfo("Password Manager", "Master password created successfully!")
                else:
                    messagebox.showwarning("Password Manager", "This master password already exists.")
            else:
                messagebox.showwarning("Password Manager", "Master password cannot be empty.")
        else:
            self.password_manager = PasswordManager()  # No master password

    def login(self):
        master_password = self.entry_password.get()

        if not self.password_manager:
            self.password_manager = PasswordManager()  # No master password

        if not self.password_manager.passwords['master_passwords'] or master_password in self.password_manager.passwords['master_passwords']:
            self.password_manager.set_active_master_password(master_password)
            self.root.destroy()  # Close the login window
            self.show_main_menu()
        else:
            messagebox.showwarning("Password Manager", "Incorrect master password. Please try again.")

    def show_main_menu(self):
        main_menu = tk.Tk()
        main_menu.title("Password Manager - Main Menu")

        label_info = tk.Label(main_menu, text="Choose an option:")
        button_save = tk.Button(main_menu, text="Save Password", command=self.save_password)
        button_retrieve = tk.Button(main_menu, text="Retrieve Password", command=self.retrieve_password)
        button_generate = tk.Button(main_menu, text="Generate Password", command=self.generate_password)
        button_exit = tk.Button(main_menu, text="Exit", command=main_menu.destroy)

        label_info.pack(pady=10)
        button_save.pack(pady=5)
        button_retrieve.pack(pady=5)
        button_generate.pack(pady=5)
        button_exit.pack(pady=5)

        main_menu.mainloop()

    def save_password(self):
        if self.password_manager:
            service = simpledialog.askstring("Save Password", "Enter the service name:")
            username = simpledialog.askstring("Save Password", "Enter the username:")
            password = simpledialog.askstring("Save Password", "Enter the password:")

            if service and username and password:
                self.password_manager.save_password(service, username, password)
                messagebox.showinfo("Password Manager", "Password saved successfully!")
            else:
                messagebox.showwarning("Password Manager", "Invalid input. Please try again.")
        else:
            messagebox.showwarning("Password Manager", "Login first.")

    def retrieve_password(self):
        if self.password_manager:
            service = simpledialog.askstring("Retrieve Password", "Enter the service name:")
            username = simpledialog.askstring("Retrieve Password", "Enter the username:")

            if service and username:
                retrieved_password = self.password_manager.get_password(service, username)
                if retrieved_password:
                    messagebox.showinfo("Password Manager", f"Retrieved Password for {service}/{username}: {retrieved_password}")
                else:
                    messagebox.showwarning("Password Manager", "Password not found.")
            else:
                messagebox.showwarning("Password Manager", "Invalid input. Please try again.")
        else:
            messagebox.showwarning("Password Manager", "Login first.")

    def generate_password(self):
        if self.password_manager:
            generated_password = self.password_manager.generate_password()
            self.show_copy_password_window(generated_password)
        else:
            messagebox.showwarning("Password Manager", "Login first.")

    def show_copy_password_window(self, password):
        copy_password_window = tk.Toplevel()
        copy_password_window.title("Generated Password")

        label_generated_password = tk.Label(copy_password_window, text="Generated Password:")
        label_generated_password.pack(pady=10)

        entry_generated_password = tk.Entry(copy_password_window, state='readonly', readonlybackground='white',
                                            width=30)
        entry_generated_password.insert(0, password)
        entry_generated_password.pack(pady=10)

        button_copy = tk.Button(copy_password_window, text="Copy to Clipboard",
                                command=lambda: self.copy_to_clipboard(password))
        button_copy.pack(pady=10)

        copy_password_window.protocol("WM_DELETE_WINDOW", lambda: copy_password_window.destroy())
        copy_password_window.mainloop()

    def copy_to_clipboard(self, data):
        pyperclip.copy(data)
        messagebox.showinfo("Password Manager", "Password copied to clipboard!")

# Example Usage:
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
