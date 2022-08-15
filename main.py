import customtkinter as ctk

ctk.set_appearance_mode('dark')

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login - HangukDramaList")
        self.geometry("500x300")
        self.configure(bg='#212121')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.destroy()

if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
