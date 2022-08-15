import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO


root = ctk.CTk()
root.geometry('450x576')
root.configure(bg='#212121')

class DramaCard(ctk.CTkFrame):
    def __init__(self, master=None, cover_url="https://image.tmdb.org/t/p/original/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg", title=None, year=None, description=None, genres=None, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master, width=366, height=168, bg_color="#333333", fg_color="#333333",corner_radius=0, *args, **kwargs)
        self.image = []
        self.raw_cover = urllib.request.urlopen(cover_url).read()
        self.cover_img = ImageTk.PhotoImage(Image.open(BytesIO(self.raw_cover)).resize((112, 168)))
        label1 = ctk.CTkLabel(self, image=self.cover_img)
        label1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.image.append(label1)


my_drama_card = DramaCard(root, cover_url="https://image.tmdb.org/t/p/original/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg")
my_drama_card.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

root.mainloop()