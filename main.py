import sys
import customtkinter as ctk
import widgets as w
import tkinter as tk

ctk.set_appearance_mode('dark')
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
        self.login_screen = LoginScreen
        self.signup_screen = SignupScreen
        self.home_screen = HomeScreen

        for i in {LoginScreen, SignupScreen, HomeScreen}:
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

        self.configure(bg="#212121")
        content_frame = ctk.CTkFrame(self, bg="#212121")
        content_frame.grid(row=0, column=0, sticky="")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(content_frame, text="Welcome Back", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w").grid(sticky="nws", pady=(0,60))


        ctk.CTkLabel(content_frame, text="Email", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        username = w.InputBox(content_frame, placeholder_text="Enter your email", width=366, height=48)
        username.grid(pady=(0,27))

        ctk.CTkLabel(content_frame, text="Password", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        password = w.InputBox(content_frame, placeholder_text="Enter your password", width=366, height=48)
        password.grid(pady=(0,27))

        w.Button(content_frame, text="Sign In", width=366, height=48, command=lambda: parent.show_screen(SignupScreen)).grid()
        #ctk.CTkButton(content_frame, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

        signup_frame = ctk.CTkFrame(content_frame, bg="#212121")
        signup_frame.grid(sticky="s", pady=(87,0))

        ctk.CTkLabel(signup_frame, text="Don't have an account?", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        ctk.CTkButton(signup_frame, text="Sign Up", text_font=w.FONT_INPUT, text_color="#48BB78", fg_color="#212121", hover_color="#212121", width=30, command=lambda: parent.show_screen(SignupScreen)).grid(row=0, column=1,pady=0,padx=0)

class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Sign Up Page")
        label.grid(pady=0,padx=0)
        ctk.CTkButton(self, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Home Page")
        label.grid(pady=0,padx=0)
        ctk.CTkButton(self, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

if __name__ == '__main__':
    app = App()
    app.mainloop()
