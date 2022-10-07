import tkinter as tk
import customtkinter as ctk
import tkinter.font as font
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import webbrowser

from requests import delete
from backend.encryption import PasswordDatabase

db = PasswordDatabase()


"""
root = ctk.CTk()
root.geometry('450x576')
root.configure(bg='#212121')
"""


# CONSTANTS
FONT_INPUT = ('Poppins', 15, 'normal')
FONT_TITLE = ('Poppins', 27, 'bold')
FONT_CATEGORY_TITLE = ('Poppins', 24, 'bold')
FONT_DRAMA_TITLE = ('Poppins', 15, 'bold')
FONT_SUBTITLE = ('Poppins', 9, 'bold')
FONT_DESCRIPTION = ('Poppins', 7, 'normal')
FONT_BUTTON = ('Poppins', 15, 'normal')


class ScrollableFrame(tk.Frame):
    def __init__(self, container, orientation, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        if orientation == 'vertical': self.canvas = tk.Canvas(self, width=366, height=290)
        elif orientation == 'horizontal': self.canvas = tk.Canvas(self, width=366, height=210)
        #self.canvas = tk.Canvas(self, width=346, height=290, bg='#212121', bd=0, highlightthickness=0, relief='ridge') # <-- Iteration two
        self.scrollable_frame = tk.Frame(self.canvas)
        #self.scrollable_frame = tk.Frame(self.canvas, bg="#212121") # <-- Iteration two
        self.scrollable_frame.bind("<Configure>", lambda *args, **kwargs: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind("<Destroy>", lambda *args, **kwargs: self.unbind_all("<MouseWheel>"))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        if orientation == 'vertical':
            self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            #self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview, fg_color='#202020',scrollbar_color='#303030', scrollbar_hover_color='#404040', width=30, corner_radius=10) # <-- Iteration two
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky="nes")
        elif orientation == 'horizontal':
            self.scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.scrollbar.set)
            self.scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.grid(row=0, column=0, sticky="news")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * round(event.delta / 120), "units")

class WrappingLabel(ctk.CTkLabel):
    '''a type of Label that automatically adjusts the wrap to the size'''
    # https://stackoverflow.com/questions/62485520/how-to-wrap-the-text-in-a-tkinter-label-dynamically
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkLabel.__init__(self, master, *args, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

class Button(ctk.CTkButton):
    '''A custom-styled button class'''
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkButton.__init__(self, master, *args, **kwargs)
        self.bind(self.configure(fg_color="#48BB78",hover_color="#38A169",text_color="#FFFFFF",corner_radius=0))

class InputBox(ctk.CTkEntry):
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkEntry.__init__(self, master, border_width=2, corner_radius=0, bg_color='#212121', fg_color="#212121", text_color="#FFFFFF", placeholder_text_color="#FFFFFF", *args, **kwargs)
    
    def get_input(self):
        return self.get()

class DramaCard(ctk.CTkFrame):
    def __init__(self, master=None, cover_url=None, title=None, year=None, description=None, genres=None, drama_id=None, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, width=366, height=168*1.25, bg_color="#333333", fg_color="#333333",corner_radius=0, *args, **kwargs)
        self.grid_propagate(False)

        self.cover_frame = ctk.CTkFrame(self, width=112, height=168*1.25, fg_color="#333333")
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

        self.drama_id = drama_id

        self.initialize_cover(cover_url)
        self.initialize_content(title, year, description, genres)
        self.initialize_add_to_watchlist()

    def initialize_cover(self, cover_url=None):
        raw_cover = urllib.request.urlopen(cover_url).read()
        img = Image.open(BytesIO(raw_cover))
        baseheight = 210
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

    def initialize_add_to_watchlist(self):
        add_to_watchlist_frame = ctk.CTkFrame(self.content_frame, fg_color="#333333", bg_color="#333333")
        add_to_watchlist_frame.grid(row=5, column=0, sticky="nw")
        add_to_watchlist_frame.grid_propagate(False)
        self.watchlist_dropdown = ctk.CTkComboBox(add_to_watchlist_frame, values=["Select an option","Plan to watch","Currently watching","Completed","On hold","Dropped"], width=136, height=24, corner_radius=0, border_width=0, border_color="#212121", fg_color="#212121", bg_color="#212121", button_color="212121", button_hover_color="#212121", dropdown_color="#212121", dropdown_hover_color="#212121", text_color="#FFFFFF", text_font=FONT_DESCRIPTION, dropdown_text_font=FONT_DESCRIPTION, hover=False)
        self.watchlist_dropdown.grid(row=0, column=0, sticky="nw")
        self.watchlist_dropdown.set("Select an option")  # set initial value
        self.value = self.watchlist_dropdown.get()
        self.add_to_watchlist_button = Button(add_to_watchlist_frame, text='Add to Watchlist', width=80, height=24, text_font=FONT_DESCRIPTION)
        self.add_to_watchlist_button.grid(row=0, column=1, sticky="")
        self.success_label = ctk.CTkLabel(add_to_watchlist_frame, text="", text_font=FONT_DESCRIPTION, text_color="#FFFFFF", anchor="w")
        self.success_label.grid(row=1, column=0, sticky="nw")

class WatchlistDramaCard(ctk.CTkFrame):
    def __init__(self, master=None, cover_url=None, title=None, year=None, description=None, genres=None, drama_id=None, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, width=366, height=210, bg_color="#333333", fg_color="#333333",corner_radius=0, *args, **kwargs)
        self.grid_propagate(False)

        self.cover_frame = ctk.CTkFrame(self, width=112, height=210, fg_color="#333333")
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

        self.drama_id = drama_id

        self.initialize_cover(cover_url)
        self.initialize_content(title, year, description, genres)
        self.initialize_update_watchlist()

    def initialize_cover(self, cover_url=None):
        raw_cover = urllib.request.urlopen(cover_url).read()
        img = Image.open(BytesIO(raw_cover))
        baseheight = 210
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

    def initialize_update_watchlist(self):
        update_watchlist_frame = ctk.CTkFrame(self.content_frame, fg_color="#333333", bg_color="#333333")
        update_watchlist_frame.grid(row=5, column=0, sticky="nw")
        update_watchlist_frame.grid_propagate(False)

        self.watchlist_dropdown = ctk.CTkComboBox(update_watchlist_frame, values=["Select an option","Plan to watch","Currently watching","Completed","On hold","Dropped"], height=24, corner_radius=0, border_width=0, border_color="#212121", fg_color="#212121", bg_color="#212121", button_color="212121", button_hover_color="#212121", dropdown_color="#212121", dropdown_hover_color="#212121", text_color="#FFFFFF", text_font=FONT_DESCRIPTION, dropdown_text_font=FONT_DESCRIPTION, hover=False)
        self.watchlist_dropdown.grid(row=0, column=0, columnspan=2, sticky="nw") # <-- Iteration two: add 'news' sticky
        self.watchlist_dropdown.set("Select an option")  # set initial value
        self.value = self.watchlist_dropdown.get()

        self.update_watchlist_button = Button(update_watchlist_frame, text='Update', width=80, height=24, text_font=FONT_DESCRIPTION)
        self.update_watchlist_button.grid(row=1, column=0, sticky="")
        self.delete_watchlist_button = ctk.CTkButton(update_watchlist_frame, text='Delete', width=80, height=24, text_font=FONT_DESCRIPTION, fg_color="red", hover_color="#38A169", text_color="#FFFFFF", corner_radius=0)
        self.delete_watchlist_button.grid(row=1, column=1, sticky="")

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