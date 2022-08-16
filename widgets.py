import tkinter as tk
import customtkinter as ctk
import tkinter.font as font
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO

root = ctk.CTk()
root.geometry('450x576')
root.configure(bg='#212121')


# CONSTANTS
FONT_INPUT = font.Font(family='Poppins', size=15, weight='normal')
FONT_TITLE = font.Font(family='Poppins', size=8, weight='bold')
FONT_SUBTITLE = font.Font(family='Poppins', size=5, weight='bold')
FONT_BUTTON = font.Font(family='Poppins', size=15, weight='normal')


class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    # https://stackoverflow.com/questions/62485520/how-to-wrap-the-text-in-a-tkinter-label-dynamically
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

class Button(ctk.CTkButton):
    '''A custom-styled button class'''
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkButton.__init__(self, master, text_font=FONT_BUTTON, *args, **kwargs)
        self.bind(self.configure(fg_color="#48BB78",hover_color="#38A169",text_color="#FFFFFF"))

class InputBox(ctk.CTkEntry):
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkEntry.__init__(self, master, border_width=2, corner_radius=0, bg_color='#212121', fg_color="#212121", text_color="#FFFFFF", placeholder_text_color="#FFFFFF", *args, **kwargs)
    
    def get_input(self):
        return self.get()

class DramaCard(ctk.CTkFrame):
    def __init__(self, master=None, cover_url=None, title=None, year=None, description=None, genres=None, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, width=366, height=168, bg_color="#333333", fg_color="#333333",corner_radius=0, *args, **kwargs)
        self.initialize_cover(cover_url)
        self.initialize_title(title)

    def initialize_cover(self, cover_url=None):
        raw_cover = urllib.request.urlopen(cover_url).read()
        self.cover_img = ImageTk.PhotoImage(Image.open(BytesIO(raw_cover)).resize((112*2, 168*2)))
        cover = ctk.CTkLabel(self, image=self.cover_img)
        cover.place(relx=0.17, rely=0.5, anchor=tk.CENTER)

    def initialize_title(self, title=None):
        title_label = ctk.CTkLabel(self, text=title, text_font=FONT_TITLE, text_color="#FFFFFF")
        title_label.place(relx=0.55, rely=0.15, anchor=tk.CENTER)


my_input = InputBox(root, placeholder_text="Enter your name", width=366, height=48)
my_button = Button(root, text='Sign In', width=366, height=48, command=lambda: print(my_input.get()))
my_drama_card = DramaCard(root, cover_url="https://image.tmdb.org/t/p/original/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg", title="Squid Game(2021)")

my_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
my_input.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
my_drama_card.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

root.mainloop()