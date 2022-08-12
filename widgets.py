import tkinter as tk
import customtkinter as ctk
import tkinter.font as font

# https://stackoverflow.com/questions/62485520/how-to-wrap-the-text-in-a-tkinter-label-dynamically
class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

class Button(ctk.CTkButton):
    '''A custom-styled button class'''
    def __init__(self, master=None, *args, **kwargs):
        ctk.CTkButton.__init__(self, master, text_font=button_font, *args, **kwargs)
        self.bind(self.configure(fg_color="#48BB78",hover_color="#38A169",text_color="#FFFFFF",command=lambda: print("hello")))

class InputBox(ctk.CTkEntry):
    '''A custom-styled button class'''
    def __init__(self, master=None, placeholder="PLACEHOLDER", *args, **kwargs):
        ctk.CTkEntry.__init__(self, master,placeholder_text=placeholder,placeholder_text_color="#FFFFFF",border_width=2,corner_radius=0,*args, **kwargs)
        self.input_text = tk.StringVar()
        self.bind(self.configure(bg_color='#212121',fg_color="#212121",font=input_font,text_color="#FFFFFF",relief=tk.FLAT,textvariable=self.input_text))
        
    def get_input(self):
        return self.input_text.get()

root = ctk.CTk()
root.geometry('450x576')
root.configure(bg='#212121')

input_font = font.Font(family='Poppins', size=8, weight='normal')
button_font = font.Font(family='Poppins', size=8, weight='normal')

my_input = InputBox(root, placeholder_text="Enter your name", width=183*2, height=48)
my_button = Button(root, text='Sign In', width=183*2, height=48)
my_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
my_input.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

root.mainloop()