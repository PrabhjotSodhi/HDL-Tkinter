import tkinter as tk
import customtkinter as ctk
import tkinter.font as font
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO


"""
root = ctk.CTk()
root.geometry('450x576')
root.configure(bg='#212121')
"""


# CONSTANTS
FONT_INPUT = ('Poppins', 15, 'normal')
FONT_TITLE = ('Poppins', 27, 'bold')
FONT_SUBTITLE = ('Poppins', 5, 'bold')
FONT_BUTTON = ('Poppins', 15, 'normal')


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
        self.bind(self.configure(fg_color="#48BB78",hover_color="#38A169",text_color="#FFFFFF",corner_radius=0))

class InputBox(ctk.CTkEntry):
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkEntry.__init__(self, master, border_width=2, corner_radius=0, bg_color='#212121', fg_color="#212121", text_color="#FFFFFF", placeholder_text_color="#FFFFFF", *args, **kwargs)
    
    def get_input(self):
        return self.get()

class DramaCard(ctk.CTkFrame):
    def __init__(self, master=None, cover_url=None, title=None, year=None, description=None, genres=None, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, width=366, height=168, bg_color="#333333", fg_color="#333333",corner_radius=0, *args, **kwargs)
        self.grid_propagate(False)

        drama_frame = ctk.CTkFrame(self)
        drama_frame.grid(row=0, column=1)
        self.columnconfigure(1, weight=1)

        self.content_frame = ctk.CTkFrame(drama_frame)
        self.content_frame.grid(row=0, column=0, sticky="nesw")

        self.initialize_cover(cover_url)
        self.initialize_title(title)

    def initialize_cover(self, cover_url=None):
        raw_cover = urllib.request.urlopen(cover_url).read()
        img = Image.open(BytesIO(raw_cover))
        baseheight = 168
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        self.cover_img = ImageTk.PhotoImage(img.resize((wsize, baseheight), Image.ANTIALIAS))
        cover = ctk.CTkLabel(self, image=self.cover_img)
        cover.grid(row=0, column=0, sticky="nesw")

    def initialize_title(self, title=None):
        title_label = ctk.CTkLabel(self.content_frame, text=title, text_font=FONT_TITLE, text_color="#FFFFFF")
        title_label.grid(row=0, column=0, sticky="nesw")

'''
my_input = InputBox(root, placeholder_text="Enter your name", width=366, height=48)
my_button = Button(root, text='Sign In', width=366, height=48, command=lambda: print(my_input.get()))
my_drama_card = DramaCard(root, cover_url="http://image.tmdb.org/t/p/original/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg", title="Squid Game(2021)")

#my_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#my_input.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
my_drama_card.grid()

root.mainloop()
'''