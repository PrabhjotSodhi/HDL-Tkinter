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

        content_frame = ctk.CTkFrame(self, bg="#212121")
        content_frame.grid(row=0, column=0, sticky="")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(content_frame, text="Welcome Back", text_font=w.FONT_TITLE, text_color="#FFFFFF").grid(sticky="nws")

        ctk.CTkLabel(content_frame, text="Email", text_font=w.FONT_BUTTON, text_color="#FFFFFF").grid(sticky="nws")
        username = w.InputBox(content_frame, placeholder_text="Enter your email", width=366, height=48)
        username.grid()

        ctk.CTkLabel(content_frame, text="Password", text_color="#FFFFFF").grid(sticky="nws")
        password = w.InputBox(content_frame, placeholder_text="Enter your password", width=366, height=48)


        ctk.CTkButton(content_frame, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = ctk.CTkLabel(self, text="Sign Up Page")
        label.grid(pady=0,padx=0)
        ctk.CTkButton(self, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = ctk.CTkLabel(self, text="Home Page")
        label.grid(pady=0,padx=0)
        ctk.CTkButton(self, text="Sign In", command=lambda: parent.show_screen(SignupScreen)).grid(pady=0,padx=0)

if __name__ == '__main__':
    app = App()
    app.mainloop()
