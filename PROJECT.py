import customtkinter as ctk
from tkinter.constants import END
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

FONT_LARGE = ("Arial", 20)
FONT_NORMAL = ("Arial", 17)

#Create a data directory to save all user lists
DATA_DIR = "user_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

USER_FILE = os.path.join(DATA_DIR, "users.txt")

#Initialize users.txt if it doesn't exist
if not os.path.exists(USER_FILE):
    open(USER_FILE, 'w').close()


class PackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dane Travel Packing Organizer")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.current_user = None
        self.create_login_ui()

    def center_window(self, window, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_login_ui(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Login", font=FONT_LARGE).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self.root, placeholder_text="Username",
                                           font=FONT_NORMAL, width=300, height=40)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.root, placeholder_text="Password",
                                           show="*", font=FONT_NORMAL, width=300, height=40)
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self.root, text="Login", command=self.login_user,
                      font=FONT_NORMAL, width=200, height=40).pack(pady=15)
        ctk.CTkButton(self.root, text="Register", command=self.create_register_ui,
                      font=FONT_NORMAL, width=200, height=40).pack()

    def create_register_ui(self):
        register_window = ctk.CTkToplevel(self.root)
        register_window.title("Register")
        register_window.resizable(False, False)
        self.center_window(register_window, 500, 500)

        register_window.transient(self.root)
        register_window.grab_set()
        register_window.focus_set()

        ctk.CTkLabel(register_window, text="Register New User", font=FONT_LARGE).pack(pady=20)
        entries = {}
        for label in ["First Name", "Last Name", "Username", "Password"]:
            ctk.CTkLabel(register_window, text=label, font=FONT_NORMAL).pack(pady=5)
            entries[label] = ctk.CTkEntry(register_window,
                                          show="*" if label == "Password" else None,
                                          font=FONT_NORMAL, width=300, height=40)
            entries[label].pack(pady=5)

        def submit():
            with open(USER_FILE, "a") as f:
                f.write(
                    f"{entries['First Name'].get()}|{entries['Last Name'].get()}|{entries['Username'].get()}|{entries['Password'].get()}\n")

            # Create a new file for user's list
            user_list_file = os.path.join(DATA_DIR, f"{entries['Username'].get()}_list.txt")
            open(user_list_file, 'w').close()

            register_window.destroy()
            success_popup = ctk.CTkToplevel(self.root)
            success_popup.title("Success")
            success_popup.resizable(False, False)
            self.center_window(success_popup, 400, 200)
            success_popup.transient(self.root)
            success_popup.grab_set()
            success_popup.focus_set()
            ctk.CTkLabel(success_popup, text="Successfully registered!", font=FONT_NORMAL).pack(pady=30)
            ctk.CTkButton(success_popup, text="OK", command=success_popup.destroy,
                          font=FONT_NORMAL, width=150, height=40).pack(pady=10)

        ctk.CTkButton(register_window, text="Submit", command=submit,
                      font=FONT_NORMAL, width=200, height=40).pack(pady=30)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open(USER_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) != 4:
                    continue
                _, _, u, p = parts
                if u == username and p == password:
                    self.current_user = username
                    # Create user's list file if it doesn't exist
                    user_list_file = os.path.join(DATA_DIR, f"{username}_list.txt")
                    if not os.path.exists(user_list_file):
                        open(user_list_file, 'w').close()
                    self.create_main_ui()
                    login_popup = ctk.CTkToplevel(self.root)
                    login_popup.title("Login Successful")
                    login_popup.resizable(False, False)
                    self.center_window(login_popup, 400, 200)
                    login_popup.transient(self.root)
                    login_popup.grab_set()
                    login_popup.focus_set()
                    ctk.CTkLabel(login_popup, text="Login successful!", font=FONT_NORMAL).pack(pady=30)
                    ctk.CTkButton(login_popup, text="OK", command=login_popup.destroy,
                                  font=FONT_NORMAL, width=150, height=40).pack(pady=10)
                    return
        ctk.CTkLabel(self.root, text="Invalid credentials!", text_color="red", font=FONT_NORMAL).pack()

    def create_main_ui(self):
        self.clear_window()

        header_frame = ctk.CTkFrame(self.root)
        header_frame.pack(fill='x', padx=20, pady=20)

        ctk.CTkLabel(header_frame, text=f"Welcome, {self.current_user}!",
                     font=FONT_LARGE).pack(side='left')

        ctk.CTkButton(header_frame, text="Logout",
                      command=self.create_login_ui,
                      font=FONT_NORMAL, width=100, height=40).pack(side='right')

        self.textbox = ctk.CTkTextbox(self.root, font=FONT_NORMAL, width=600, height=300)
        self.textbox.pack(pady=20)

        # Button Frame for better organization
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Load List",
                      command=self.load_list,
                      font=FONT_NORMAL, width=200, height=40).pack(pady=5)

        ctk.CTkButton(button_frame, text="Add Item",
                      command=self.add_item_popup,
                      font=FONT_NORMAL, width=200, height=40).pack(pady=5)

        ctk.CTkButton(button_frame, text="Delete Item",
                      command=self.delete_item_popup,
                      font=FONT_NORMAL, width=200, height=40).pack(pady=5)

        ctk.CTkButton(button_frame, text="Save List",
                      command=self.save_list,
                      font=FONT_NORMAL, width=200, height=40).pack(pady=5)

    def add_item_popup(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Add Item")
        popup.resizable(False, False)
        self.center_window(popup, 400, 250)
        popup.transient(self.root)
        popup.grab_set()
        popup.focus_set()

        ctk.CTkLabel(popup, text="Enter item:", font=FONT_NORMAL).pack(pady=20)
        item_entry = ctk.CTkEntry(popup, font=FONT_NORMAL, width=300, height=40)
        item_entry.pack(pady=10)

        def add():
            item = item_entry.get().strip()
            if item:
                current_text = self.textbox.get("1.0", END).strip()
                if current_text:
                    self.textbox.insert(END, f"\n{item}")
                else:
                    self.textbox.insert(END, item)
                popup.destroy()

                added_popup = ctk.CTkToplevel(self.root)
                added_popup.title("Item Added")
                added_popup.resizable(False, False)
                self.center_window(added_popup, 400, 200)
                added_popup.transient(self.root)
                added_popup.grab_set()
                added_popup.focus_set()
                ctk.CTkLabel(added_popup, text="Item added to the list!",
                             font=FONT_NORMAL).pack(pady=30)
                ctk.CTkButton(added_popup, text="OK",
                              command=added_popup.destroy,
                              font=FONT_NORMAL, width=150, height=40).pack(pady=10)

        ctk.CTkButton(popup, text="Add", command=add,
                      font=FONT_NORMAL, width=200, height=40).pack(pady=20)

    def delete_item_popup(self):
        items = [item.strip() for item in self.textbox.get("1.0", END).splitlines() if item.strip()]

        if not items:
            error_popup = ctk.CTkToplevel(self.root)
            error_popup.title("Error")
            error_popup.resizable(False, False)
            self.center_window(error_popup, 400, 200)
            error_popup.transient(self.root)
            error_popup.grab_set()
            error_popup.focus_set()

            ctk.CTkLabel(error_popup,
                         text="No items in the list to delete!",
                         font=FONT_NORMAL).pack(pady=30)

            ctk.CTkButton(error_popup,
                          text="OK",
                          command=error_popup.destroy,
                          font=FONT_NORMAL,
                          width=150,
                          height=40).pack(pady=10)
            return

        delete_window = ctk.CTkToplevel(self.root)
        delete_window.title("Delete Items")
        delete_window.resizable(False, False)
        self.center_window(delete_window, 600, 600)
        delete_window.transient(self.root)
        delete_window.grab_set()
        delete_window.focus_set()

        main_frame = ctk.CTkFrame(delete_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame,
                     text="Select items to delete:",
                     font=FONT_LARGE).pack(pady=20)

        scroll_frame = ctk.CTkScrollableFrame(main_frame,
                                              width=500,
                                              height=300)
        scroll_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        checkbox_vars = {}

        for item in items:
            var = ctk.BooleanVar()
            checkbox_vars[item] = var
            checkbox = ctk.CTkCheckBox(scroll_frame,
                                       text=item,
                                       variable=var,
                                       font=FONT_NORMAL,
                                       height=35,
                                       checkbox_width=25,
                                       checkbox_height=25)
            checkbox.pack(pady=5, anchor="w", padx=10)

        def delete_selected_items():
            items_to_delete = [item for item, var in checkbox_vars.items() if var.get()]

            if not items_to_delete:
                return

            current_items = [item.strip() for item in self.textbox.get("1.0", END).splitlines() if item.strip()]
            remaining_items = [item for item in current_items if item not in items_to_delete]

            self.textbox.delete("1.0", END)
            if remaining_items:
                self.textbox.insert(END, '\n'.join(remaining_items) + '\n')

            delete_window.destroy()

            success = ctk.CTkToplevel(self.root)
            success.title("Success")
            success.resizable(False, False)
            self.center_window(success, 400, 200)
            success.transient(self.root)
            success.grab_set()
            success.focus_set()

            msg = f"Successfully deleted {len(items_to_delete)} item{'s' if len(items_to_delete) > 1 else ''}!"
            ctk.CTkLabel(success,
                         text=msg,
                         font=FONT_NORMAL).pack(pady=30)

            ctk.CTkButton(success,
                          text="OK",
                          command=success.destroy,
                          font=FONT_NORMAL,
                          width=150,
                          height=40).pack(pady=10)

        button_container = ctk.CTkFrame(delete_window, fg_color="transparent")
        button_container.pack(fill="x", padx=20, pady=(0, 20))

        delete_button = ctk.CTkButton(
            button_container,
            text="Delete Selected",
            command=delete_selected_items,
            font=("Arial", 20),
            width=250,
            height=60,
            fg_color="#FF3B30",
            hover_color="#DC2626",
            border_width=2,
            border_color="#FF3B30",
            corner_radius=10
        )
        delete_button.pack(side="left", padx=20)

        cancel_button = ctk.CTkButton(
            button_container,
            text="Cancel",
            command=delete_window.destroy,
            font=("Arial", 20),
            width=250,
            height=60,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            border_width=2,
            border_color="#3B82F6",
            corner_radius=10
        )
        cancel_button.pack(side="right", padx=20)

    def save_list(self):
        if not self.current_user:
            return

        user_list_file = os.path.join(DATA_DIR, f"{self.current_user}_list.txt")
        with open(user_list_file, "w") as f:
            f.write(self.textbox.get("1.0", END).strip())

        save_popup = ctk.CTkToplevel(self.root)
        save_popup.title("Saved")
        save_popup.resizable(False, False)
        self.center_window(save_popup, 400, 200)
        save_popup.transient(self.root)
        save_popup.grab_set()
        save_popup.focus_set()
        ctk.CTkLabel(save_popup, text="Packing list saved!", font=FONT_NORMAL).pack(pady=30)
        ctk.CTkButton(save_popup, text="OK", command=save_popup.destroy,
                      font=FONT_NORMAL, width=150, height=40).pack(pady=10)

    def load_list(self):
        if not self.current_user:
            return

        user_list_file = os.path.join(DATA_DIR, f"{self.current_user}_list.txt")
        self.textbox.delete("1.0", END)

        if os.path.exists(user_list_file):
            with open(user_list_file, "r") as f:
                content = f.read().strip()
                if content:  # Only show popup if there's actual content
                    self.textbox.insert(END, content)

                    load_popup = ctk.CTkToplevel(self.root)
                    load_popup.title("Loaded")
                    load_popup.resizable(False, False)
                    self.center_window(load_popup, 400, 200)
                    load_popup.transient(self.root)
                    load_popup.grab_set()
                    load_popup.focus_set()
                    ctk.CTkLabel(load_popup, text="Packing list loaded!", font=FONT_NORMAL).pack(pady=30)
                    ctk.CTkButton(load_popup, text="OK", command=load_popup.destroy,
                                  font=FONT_NORMAL, width=150, height=40).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = PackingApp(root)
    root.mainloop()