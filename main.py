import customtkinter as ctk
from tkinter import *

ctk.set_appearance_mode('dark')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HangukDramaList")
        self.geometry("450x576")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        root = ctk.CTkFrame(self, bg="#212121")
        root.pack(side="top", fill="both", expand=True)
        root.grid_rowconfigure(0, weight="1")
        root.grid_columnconfigure(0, weight="1")

        self.screens = {}
        self.login_screen = LoginScreen
        self.signup_screen = SignupScreen
        self.home_screen = HomeScreen

        for i in {LoginScreen, SignupScreen, HomeScreen}:
            frame = i(self, root)
            self.screens[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_screen(LoginScreen)
    
    def show_screen(self, screen):
        frame = self.screens[screen]
        frame.tkraise()
        
    def on_closing(self):
        self.destroy()

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = ctk.CTkLabel(self, text="Login Page")
        label.pack(pady=0,padx=0)
        ctk.CTkButton(self, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).pack(pady=0,padx=0)

class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = ctk.CTkLabel(self, text="Sign Up Page")
        label.pack(pady=0,padx=0)
        ctk.CTkButton(self, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).pack(pady=0,padx=0)

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = ctk.CTkLabel(self, text="Home Page")
        label.pack(pady=0,padx=0)
        ctk.CTkButton(self, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).pack(pady=0,padx=0)

if __name__ == '__main__':
    app = App()
    app.mainloop()
