import sys
import customtkinter as ctk
import widgets as w
from backend.tmdb import TMDB
import tkinter as tk
from tkinter import messagebox
from backend.encryption import PasswordDatabase
import ctypes

ctk.set_appearance_mode('dark')
db = PasswordDatabase()
tmdb = TMDB()
#ctk.deactivate_automatic_dpi_awareness()
ctypes.windll.shcore.SetProcessDpiAwareness(0)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HangukDramaList")
        self.geometry("450x576")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_rowconfigure(0, weight="1")
        self.grid_columnconfigure(0, weight="1")

        self.screens = {}
        self.LoginScreen = LoginScreen
        self.SignupScreen = SignupScreen
        self.HomeScreen = HomeScreen
        self.WatchListScreen = WatchListScreen

        for i in {LoginScreen, SignupScreen, HomeScreen, WatchListScreen}:
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

        self.configure(fg_color="#212121")
        content_frame = ctk.CTkFrame(self, fg_color="#212121")
        content_frame.grid(row=0, column=0, sticky="")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(content_frame, text="Welcome Back", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w").grid(sticky="nws", pady=(29,60))

        ctk.CTkLabel(content_frame, text="Username", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        username = w.InputBox(content_frame, placeholder_text="Enter your username", width=366, height=48)
        username.grid(pady=(0,27))

        ctk.CTkLabel(content_frame, text="Password", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        password = w.InputBox(content_frame, placeholder_text="Enter your password", width=366, height=48, show="*")
        password.grid(pady=(0,27))

        w.Button(content_frame, text="Sign In", width=366, height=48, text_font=w.FONT_BUTTON, command=lambda: self.sign_in(parent, username, password)).grid()

        signup_frame = ctk.CTkFrame(content_frame, fg_color="#212121")
        signup_frame.grid(sticky="", pady=(87,28))

        ctk.CTkLabel(signup_frame, text="Don't have an account?", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        ctk.CTkButton(signup_frame, text="Sign Up", text_font=w.FONT_INPUT, text_color="#48BB78", fg_color="#212121", hover_color="#212121", width=30, command=lambda: parent.show_screen(parent.SignupScreen)).grid(row=0, column=1,pady=0,padx=0)

        parent.bind('<Return>', lambda e: self.sign_in(parent, username, password))

    def sign_in(self, parent, username, password):
        self.user_data = db.login(str(username.get()), str(password.get()))
        print(f"username:{username.get()}, password:{password.get()}, {self.user_data}")
        if self.user_data == "User does not exist":
            messagebox.showwarning("User not found","Please enter the correct username")
        elif self.user_data and not self.user_data == "User does not exist":
            self.user_data = self.user_data[::len(self.user_data)-1]
            #parent.HomeScreen.title.configure(text=f"Search Drama, {user_data[0]}")
            parent.show_screen(parent.HomeScreen)
        else:
            messagebox.showwarning("Please try again","Please enter the correct username and/or password")

class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#212121")
        content_frame = ctk.CTkFrame(self, fg_color="#212121")
        content_frame.grid(row=0, column=0, sticky="")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(content_frame, text="Create an account", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w").grid(sticky="nws", pady=(29,60))

        ctk.CTkLabel(content_frame, text="Username", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        username = w.InputBox(content_frame, placeholder_text="Create a username", width=366, height=48)
        username.grid(pady=(0,27))

        ctk.CTkLabel(content_frame, text="Password", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        password = w.InputBox(content_frame, placeholder_text="Create a password ", width=366, height=48, show="*")
        password.grid(pady=(0,27))

        w.Button(content_frame, text="Sign Up", width=366, height=48, text_font=w.FONT_BUTTON, command=lambda: self.sign_up(parent, username, password)).grid()

        signup_frame = ctk.CTkFrame(content_frame, fg_color="#212121")
        signup_frame.grid(sticky="", pady=(87,28))

        ctk.CTkLabel(signup_frame, text="Already have an account?", text_font=w.FONT_INPUT, text_color="#FFFFFF", anchor="w").grid(sticky="nws")
        ctk.CTkButton(signup_frame, text="Sign in", text_font=w.FONT_INPUT, text_color="#48BB78", fg_color="#212121", hover_color="#212121", width=30, command=lambda: parent.show_screen(parent.LoginScreen)).grid(row=0, column=1,pady=0,padx=0)

        parent.bind('<Return>', lambda e: self.sign_in(parent, username, password))

    def sign_up(self, parent, username, password):
        self.user_data = db.register(user=str(username.get()), password=str(password.get()))
        print(f"nickname:, username:{username.get()}, password:{password.get()}, {self.user_data}")
        if self.user_data == "User already exists":
            print("hahahah")
            messagebox.showwarning("User already exists","Please go to the sign in")
        elif self.user_data == "paswword < 6":
            messagebox.showwarning("Password too short","Please enter a password with at least 6 characters")
        elif self.user_data and not self.user_data == "User already exists" and not self.user_data == "paswword < 6":
            self.user_data = self.user_data[::len(self.user_data)-1]
            #parent.HomeScreen.title.configure(text=f"Search Drama, {user_data[0]}")
            parent.show_screen(parent.HomeScreen)
        else:
            messagebox.showwarning("Please try again","Please enter the correct username and/or password")

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="#212121")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(self, fg_color="#212121", width=366, height=512, corner_radius=0)
        content_frame.grid(row=0, column=0, sticky="", pady=(0,0))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_propagate(False)
        
        self.title = ctk.CTkLabel(content_frame, text="Search Drama", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w")
        self.title.grid(row=1, sticky="nws", pady=(0,8))

        search_frame = ctk.CTkFrame(content_frame, fg_color="#212121")
        search_frame.grid(row=2, sticky="nws", pady=(0,0))
        search = w.InputBox(search_frame, placeholder_text="Search for a drama...", width=264, height=48)
        search.grid(row=0, column=0, sticky="nws", padx=(0,10))
        w.Button(search_frame, text="Search", width=96, height=48, text_font=w.FONT_BUTTON, command=lambda: self.search_drama(search, drama_card_frame)).grid(row=0, column=1, sticky="nes")

        drama_card_frame = ctk.CTkFrame(content_frame, fg_color="#212121", width=366, height=168*1.25, corner_radius=0)
        drama_card_frame.grid(row=3, sticky="nws", pady=(14,0))

        w.Button(content_frame, text="View current watchlist", width=366, height=48, text_font=w.FONT_BUTTON, command=lambda: parent.show_screen(parent.WatchListScreen)).grid(row=4,pady=(32,0))

        w.footer(content_frame).grid(row=5, sticky="", pady=(0,0))

    def search_drama(self, search, parent_frame):
        print(search.get())
        result = tmdb.search_drama(search.get())
        for widgets in parent_frame.winfo_children():
            widgets.destroy()
        drama_card = w.DramaCard(parent_frame, cover_url=result["poster_path"], title=result["name"], year=result["year"], description=result["description"], genres=result["genres"])
        drama_card.add_to_watchlist_button.configure(command=lambda: self.check_dropdown(drama_card.watchlist_dropdown.get(), result))
        drama_card.grid(sticky="news")
    
    def check_dropdown(self, dropdown, result):
        add_to_watchlist = db.add_to_watchlist(dropdown, result["id"])
        if add_to_watchlist:
            messagebox.showinfo("Successfully added to watchlist!",f"{result['name']} has been added to your watchlist")
        elif not add_to_watchlist:
            messagebox.showwarning("Select an option","Please chose one of the options in the dropdown")


class WatchListScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(fg_color="#212121")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(self, fg_color="#212121", width=366, height=512, corner_radius=0)
        content_frame.grid(row=0, column=0, sticky="")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_propagate(False) 

        title_frame = ctk.CTkFrame(content_frame, fg_color="#333333", bg_color="#333333", width=242, height=48, corner_radius=0)
        title_frame.grid(row=1, column=0, sticky="nws", pady=(0,8))
        ctk.CTkLabel(title_frame, text="My Watchlist", text_font=w.FONT_TITLE, text_color="#FFFFFF", anchor="w").grid(row=0, column=0, sticky="nws")
        ctk.CTkButton(title_frame, text="Reload", bg_color="#333333", fg_color="#333333", command=lambda: self.update_watchlist(self.drama_category_frames)).grid(row=0, column=1, sticky="nes")

        # Categories in watchlist_frame
        watchlist_frame = w.ScrollableFrame(content_frame, "vertical")
        watchlist_frame.grid(row=3, column=0, sticky="nws")
        self.categories= ["Plan to watch","Currently watching","Completed","On hold","Dropped"]
        self.drama_category_frames = []
        for i, category in enumerate(self.categories):
            title_index = [0,2,4,6,8]
            drama_index = [1,3,5,7,9]
            ctk.CTkLabel(watchlist_frame.scrollable_frame, text=category, text_font=w.FONT_CATEGORY_TITLE, fg_color="#404040", bg_color="#202020", anchor="w").grid(row=title_index[i], sticky="nws", pady=(0,0))
            drama_category_frame = w.ScrollableFrame(watchlist_frame.scrollable_frame, "horizontal")
            drama_category_frame.grid(row=drama_index[i], sticky="nws", pady=(10,10))
            self.drama_category_frames.append(drama_category_frame)
        
        #for i, category in enumerate(categories):
        #    drama_card = w.DramaCard(watchlist_frame.scrollable_frame, cover_url="https://image.tmdb.org/t/p/w500/6t6r1VGQTTQecN4V0sZeqsmdU9g.jpg", title="The King: Eternal Monarch", year="2020", description="A detective from the Joseon era is transported to present day South Korea where he must solve a series of gruesome murders.", genres=["Fantasy","Romance","Thriller"])
        #    drama_card.grid(row=i+1, sticky="news", pady=(0,10))

        # Footer
        w.Button(content_frame, text="Search Drama", width=366, height=48, text_font=w.FONT_BUTTON, command=lambda: parent.show_screen(parent.HomeScreen)).grid(row=4,pady=(22,0))
        w.footer(content_frame).grid(row=5, sticky="")
        #watchlist_scrollbar = ctk.CTkScrollbar(content_frame, orientation="vertical", command=watchlist_frame.yview)
        #watchlist_scrollbar.grid(row=3, column=1, sticky="ns")
        #watchlist_frame.configure(yscrollcommand=watchlist_scrollbar.set)
    
    def update_watchlist(self, parent_frames):
        watchlist = db.get_dramas()
        test_drama = tmdb.search_drama_by_id(129760)
        for frame in parent_frames:
            for widgets in frame.scrollable_frame.winfo_children():
                widgets.destroy()
        for category in watchlist:
            for i, id in enumerate(watchlist[category]):
                drama = tmdb.search_drama_by_id(id)
                w.WatchlistDramaCard(parent_frames[i].scrollable_frame, cover_url=drama["poster_path"], title=drama["name"], year=drama["year"], description=drama["description"], genres=drama["genres"]).grid(sticky="news", pady=(0,10))
        print(watchlist)

if __name__ == '__main__':
    app = App()
    app.mainloop()
