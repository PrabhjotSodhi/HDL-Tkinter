from ctypes import windll
from tkinter import ttk
import tkinter as tk
import widgets as w

import customtkinter as ctk

screen_w, screen_h = 800, 500

root_w = 800
root_h = 500
border = 20
lines = 8

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        #self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview, fg_color='#202020',scrollbar_color='#303030', scrollbar_hover_color='#404040', width=30, corner_radius=10)

        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda *args, **kwargs: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind("<Destroy>", lambda *args, **kwargs: self.unbind_all("<MouseWheel>"))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nw")

        self.scrollbar.grid(row=0, column=0, sticky="nes")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * round(event.delta / 120), "units")


# ininitialize the root window
root = ctk.CTk(fg_color='#202020')
root.title("Scrollbar")
# spawn window in center of the screen
root.geometry(f"{root_w}x{root_h}")
root.resizable(False, False)

root.configure(fg_color="#212121")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

content_frame = ctk.CTkFrame(root, fg_color="#212121", width=366, height=512, corner_radius=0)
content_frame.grid(row=0, column=0, sticky="")
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_propagate(False)

ctk.CTkLabel(content_frame, text="My Watchlist", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w").grid(row=1, sticky="nws", pady=(0,0))


scrollable_frame = ScrollableFrame(content_frame, width=root_w, height=root_h)
scrollable_frame.grid(row=3, column=0, sticky="nw")
for i in range(lines):
    ctk.CTkLabel(scrollable_frame.scrollable_frame, fg_color='#404040', bg_color='#202020', width=root_w / border, corner_radius=10, text=f"Line {i + 1}", text_font="Consolas 24 normal").grid(row=i,pady=(10, 0))
w.Button(content_frame, text="Search Drama", width=366, height=48, text_font=w.FONT_BUTTON, command=lambda: parent.show_screen(parent.HomeScreen)).grid(row=4,pady=(22,0))
w.footer(content_frame).grid(row=5, sticky="")

root.mainloop()