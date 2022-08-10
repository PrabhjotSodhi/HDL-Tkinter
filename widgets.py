import tkinter as tk
from turtle import width
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
        self.bind(self.configure(fg_color="#48BB78",hover_color="#38A169",text_color="#FFFFFF",corner_radius=0,command=lambda: print("hello")))

class InputBox(tk.Entry):
    '''A custom-styled button class'''
    def __init__(self, master=None, *args, **kwargs):
        tk.Entry.__init__(self, master, *args, **kwargs)
        self.input_text = tk.StringVar()
        self.bind(self.config(bg='#212121',fg="#FFFFFF",font=input_font,relief=tk.FLAT,textvariable=self.input_text))
    def get_input(self):
        return self.input_text.get()

root = ctk.CTk()
root.geometry('450x576')
root.configure(bg='#212121')

input_font = font.Font(family='Poppins', size=8, weight='normal')
button_font = font.Font(family='Poppins', size=8, weight='normal')

my_input = InputBox(root, text='Sign In')
my_button = Button(root, text='Sign In', width=183*2, height=48, )
my_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
my_input.pack(ipadx=10,ipady=10)

root.mainloop()