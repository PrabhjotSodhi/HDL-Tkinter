import sys
import customtkinter as ctk
import widgets as w
import tkinter as tk
from tkinter import messagebox
from backend.encryption import PasswordDatabase

ctk.set_appearance_mode('dark')
db = PasswordDatabase()
#ctk.deactivate_automatic_dpi_awareness()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HangukDramaList")
        self.geometry("450x576")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_rowconfigure(0, weight="1")
        self.grid_columnconfigure(0, weight="1")

        self.screens = {}
        self.LoginScreen = LoginScreen
        self.SignupScreen = SignupScreen
        self.HomeScreen = HomeScreen
        self.WatchListScreen = WatchListScreen

        for i in {LoginScreen, SignupScreen, HomeScreen, WatchListScreen}:
            frame = i(self)
            self.screens[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_screen(LoginScreen)
    
    def show_screen(self, screen):
        frame = self.screens[screen]
        frame.tkraise()
        
    def on_closing(self):
        self.destroy()
        sys.exit(0)

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#212121")
        content_frame = ctk.CTkFrame(self, fg_color="#212121")
        content_frame.grid(row=0, column=0, sticky="")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(content_frame, text="Welcome Back", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w").grid(sticky="nws", pady=(29,60))


        ctk.CTkLabel(content_frame, text="Email", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        username = w.InputBox(content_frame, placeholder_text="Enter your email", width=366, height=48)
        username.grid(pady=(0,27))

        ctk.CTkLabel(content_frame, text="Password", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        password = w.InputBox(content_frame, placeholder_text="Enter your password", width=366, height=48) # add show="*",
        password.grid(pady=(0,27))

        w.Button(content_frame, text="Sign In", width=366, height=48, command=lambda: self.sign_in(parent, username, password)).grid()
        #ctk.CTkButton(content_frame, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

        signup_frame = ctk.CTkFrame(content_frame, fg_color="#212121")
        signup_frame.grid(sticky="", pady=(87,28))

        ctk.CTkLabel(signup_frame, text="Don't have an account?", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        ctk.CTkButton(signup_frame, text="Sign Up", text_font=w.FONT_INPUT, text_color="#48BB78", fg_color="#212121", hover_color="#212121", width=30, command=lambda: parent.show_screen(parent.SignupScreen)).grid(row=0, column=1,pady=0,padx=0)

        parent.bind('<Return>', lambda e: self.sign_in(parent, username, password))

    def sign_in(self, parent, username, password):
        user_data = db.login(str(username.get()), str(password.get()))
        print(f"username:{username.get()}, password:{password.get()}, {user_data}")
        if user_data:
            user_data = user_data[::len(user_data)-1]
            #parent.HomeScreen.title.configure(text=f"Search Drama, {user_data[0]}")
            parent.show_screen(parent.HomeScreen)
        else:
            messagebox.showwarning("Please try again","Please enter the correct username and/or password") # TODO: Improve by saying different error if no user found 

class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#212121")
        content_frame = ctk.CTkFrame(self, fg_color="#212121")
        content_frame.grid(row=0, column=0, sticky="")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        entry_frame = ctk.CTkFrame(content_frame, fg_color="#212121")
        entry_frame.grid(row=1, column=0, sticky="")

        ctk.CTkLabel(content_frame, text="Create an account", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w").grid(row=0, sticky="nws", pady=(29,0))

        ctk.CTkLabel(entry_frame, text="Nickname", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        nickname = w.InputBox(entry_frame, placeholder_text="What should we call you?", width=366, height=48)
        nickname.grid()

        ctk.CTkLabel(entry_frame, text="Email", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        username = w.InputBox(entry_frame, placeholder_text="Enter your email", width=366, height=48)
        username.grid()

        ctk.CTkLabel(entry_frame, text="Password", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        password = w.InputBox(entry_frame, placeholder_text="Enter your password", width=366, height=48)
        password.grid()

        w.Button(content_frame, text="Sign Up", width=366, height=48, command=lambda: self.sign_up(parent, nickname, username, password)).grid(pady=(27,0))
        #ctk.CTkButton(content_frame, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

        signup_frame = ctk.CTkFrame(content_frame, fg_color="#212121")
        signup_frame.grid(sticky="", pady=(87,28))

        ctk.CTkLabel(signup_frame, text="Already have an account?", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        ctk.CTkButton(signup_frame, text="Sign in", text_font=w.FONT_INPUT, text_color="#48BB78", fg_color="#212121", hover_color="#212121", width=30, command=lambda: parent.show_screen(parent.LoginScreen)).grid(row=0, column=1,pady=0,padx=0)

        parent.bind('<Return>', lambda e: self.sign_in(parent, username, password))

    def sign_up(self, parent, nickname, username, password):
        success = db.register(str(nickname.get()), str(username.get()), str(password.get()))
        print(f"nickname:{nickname.get()}, username:{username.get()}, password:{password.get()}, {success}")
        if success:
            parent.show_screen(parent.HomeScreen)


class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#212121")
        content_frame = ctk.CTkFrame(self, fg_color="#212121")
        content_frame.grid(row=0, column=0, sticky="")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(content_frame, text="Search Drama, John", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w")
        self.title.grid(row=0, sticky="nws", pady=(0,14))

        search_frame = ctk.CTkFrame(content_frame, fg_color="#212121")
        search_frame.grid(row=1, sticky="nws")
        search = w.InputBox(search_frame, placeholder_text="Search for a drama...", width=264, height=48)
        search.grid(row=0, column=0, sticky="nws", padx=(0,6))
        w.Button(search_frame, text="Search", width=96, height=48, command="").grid(row=0, column=1)

        #ctk.CTkButton(content_frame, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

        w.Button(content_frame, text="View current watchlist", width=366, height=48, command=lambda: parent.show_screen(parent.WatchListScreen)).grid(row=3,pady=(266,14))

        w.footer(content_frame).grid(row=4, sticky="", pady=(0,28))
        #signup_frame = ctk.CTkFrame(content_frame, fg_color="#212121")
        #signup_frame.grid(sticky="", pady=(87,28))

        #ctk.CTkLabel(signup_frame, text="Designed & Built by", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        #ctk.CTkButton(signup_frame, text="Prabhjot Sodhi", text_font=w.FONT_INPUT, text_color="#48BB78", fg_color="#212121", hover_color="#212121", width=30, command=).grid(row=0, column=1,pady=0,padx=0)

class WatchListScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#212121")
        content_frame = ctk.CTkFrame(self, fg_color="#212121")
        content_frame.grid(row=0, column=0, sticky="")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(content_frame, text="Welcome Back", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w").grid(sticky="nws", pady=(29,60))


if __name__ == '__main__':
    app = App()
    app.mainloop()
