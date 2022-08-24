import tkinter as tk
import customtkinter as ctk
import tkinter.font as font
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import webbrowser


"""
root = ctk.CTk()
root.geometry('450x576')
root.configure(bg='#212121')
"""


# CONSTANTS
FONT_INPUT = ('Poppins', 15, 'normal')
FONT_TITLE = ('Poppins', 27, 'bold')
FONT_DRAMA_TITLE = ('Poppins', 15, 'bold')
FONT_SUBTITLE = ('Poppins', 9, 'bold')
FONT_DESCRIPTION = ('Poppins', 7, 'normal')
FONT_BUTTON = ('Poppins', 15, 'normal')


class WrappingLabel(ctk.CTkLabel):
    '''a type of Label that automatically adjusts the wrap to the size'''
    # https://stackoverflow.com/questions/62485520/how-to-wrap-the-text-in-a-tkinter-label-dynamically
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkLabel.__init__(self, master, *args, **kwargs)
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

        self.cover_frame = ctk.CTkFrame(self, width=112, height=168, fg_color="#333333")
        self.cover_frame.grid(row=0, column=0)
        self.cover_frame.grid_propagate(False)

        drama_frame = ctk.CTkFrame(self, fg_color="#333333")
        drama_frame.grid(row=0, column=1, columnspan=2, sticky="news")
        drama_frame.grid_propagate(False)
        drama_frame.grid_rowconfigure(0, weight=1)
        drama_frame.grid_columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.content_frame = ctk.CTkFrame(drama_frame, width=229, height=136, fg_color="#333333")
        self.content_frame.grid(row=0, column=0, sticky="ns")
        self.content_frame.grid_propagate(False)

        self.initialize_cover(cover_url)
        self.initialize_content(title, year, description, genres)

    def initialize_cover(self, cover_url=None):
        raw_cover = urllib.request.urlopen(cover_url).read()
        img = Image.open(BytesIO(raw_cover))
        baseheight = 168
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        self.cover_img = ImageTk.PhotoImage(img.resize((wsize, baseheight), Image.ANTIALIAS))
        cover = ctk.CTkLabel(self.cover_frame, image=self.cover_img)
        cover.grid(row=0, column=0, sticky="news")

    def initialize_content(self, title=None, year="YYYY", description=None, genres=None):
        ctk.CTkLabel(self.content_frame, text=f"{title}({year})", text_font=FONT_DRAMA_TITLE, text_color="#FFFFFF", anchor="w").grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(self.content_frame, text="Description", text_font=FONT_SUBTITLE, text_color="#FFFFFF", anchor="w").grid(row=1, column=0, sticky="nw")
        ctk.CTkLabel(self.content_frame, text=description, text_font=FONT_DESCRIPTION, text_color="#FFFFFF", anchor="w", justify="left", wraplength=300).grid(row=2, column=0, sticky="n")
        
        ctk.CTkLabel(self.content_frame, text="Genres", text_font=FONT_SUBTITLE, text_color="#FFFFFF", anchor="w").grid(row=3, column=0, sticky="nw")
        ctk.CTkLabel(self.content_frame, text=str(genres), text_font=FONT_DESCRIPTION, text_color="#FFFFFF", anchor="w").grid(row=4, column=0, sticky="nw")

        add_to_watchlist_frame = ctk.CTkFrame(self.content_frame).grid(row=5, column=0, sticky="")
        watchlist_dropdown = ctk.CTkComboBox(add_to_watchlist_frame, values=["Select an option","Plan to watch","Currently watching","Completed","On hold","Dropped"], width=136, height=24, corner_radius=0, border_width=0, border_color="#212121", fg_color="#212121", button_color="212121", button_hover_color="#212121", dropdown_color="#212121", dropdown_hover_color="#212121", text_color="#FFFFFF", text_font=FONT_DESCRIPTION, dropdown_text_font=FONT_DESCRIPTION, hover=False)
        watchlist_dropdown.grid(row=0, column=0, sticky="")
        watchlist_dropdown.set("Select an option")  # set initial value
        Button(add_to_watchlist_frame, text='Add to Watchlist', width=80, height=24, command=lambda: print(watchlist_dropdown.get())).grid(row=0, column=1, sticky="")
        #ctk.CTkButton(add_to_watchlist_frame, text="Add to Watchlist", text_font=FONT_BUTTON, command=lambda: print("Add to Watchlist")).grid(row=0, column=1, sticky="")
        

class footer(ctk.CTkFrame):
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, width=366, height=100, bg_color="#212121", fg_color="#212121",corner_radius=0, *args, **kwargs)
        self.grid_propagate(False)

        github_url = "http://github.com/PrabhjotSodhi"
        tmdb_url = "http://www.themoviedb.org/"

        top_frame=ctk.CTkFrame(self, fg_color="#212121")
        bottom_frame=ctk.CTkFrame(self, fg_color="#212121")
        top_frame.grid(row=0, column=0, sticky="")
        bottom_frame.grid(row=1, column=0, sticky="")

        ctk.CTkLabel(top_frame, text="Designed & Built by", text_font=FONT_INPUT, text_color="#FFFFFF", anchor="e").grid(row=0, sticky="nws")
        ctk.CTkButton(top_frame, text="Prabhjot Sodhi", text_font=FONT_INPUT, text_color="#48BB78", fg_color="#212121", hover_color="#212121", width=30, command=lambda aurl=github_url:webbrowser.open_new(github_url)).grid(row=0, column=1,pady=0,padx=0)

        ctk.CTkLabel(bottom_frame, text="Powered by", text_font=FONT_INPUT, text_color="#FFFFFF", anchor="e").grid(row=0, sticky="nws")
        ctk.CTkButton(bottom_frame, text="TMDB API", text_font=FONT_INPUT, text_color="#48BB78", fg_color="#212121", hover_color="#212121", width=30, command=lambda aurl=tmdb_url:webbrowser.open_new(tmdb_url)).grid(row=0, column=1,pady=0,padx=0, sticky="nws")



'''
my_input = InputBox(root, placeholder_text="Enter your name", width=366, height=48)
my_button = Button(root, text='Sign In', width=366, height=48, command=lambda: print(my_input.get()))
my_drama_card = DramaCard(root, cover_url="http://image.tmdb.org/t/p/original/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg", title="Squid Game(2021)")

#my_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#my_input.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
my_drama_card.grid()

root.mainloop()
'''