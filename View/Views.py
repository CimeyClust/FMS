from functools import partial
from tkinter.ttk import *
from email.mime import image
import tkinter
import tkinter.messagebox
from turtle import width
from webbrowser import BackgroundBrowser
import customtkinter
from tkinter import PhotoImage, ttk
import os

from Controller import Controller
from Controller.CallbackRegister import Callback

global QRIcon
global Bild1

# Each View (different Window) should have one own class.
# By instantiating the class of the view, the old view should close and the new one should appear


# The main class every other view is inheriting from
class View:
    def initView(self, control: Controller, values: list):
        pass

    def killView(self):
        pass

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class MainView(View, customtkinter.CTk):

    WIDTH = 1200
    HEIGHT = 600

    def initView(self, control: Controller, values: list):
        '''
        Values:
        Title: value.title.title
        isbn: value.title.isbn
        autor: value.title.author
        subject: value.title.subject.subjectTitle
        student: value.student.surName + " " + value.student.lastName
        
        Callbacks:
        
        '''

        global QRIcon
        global Bild1
        global style
        super().__init__()

        self.title("Fachwerk Management System")
        self.geometry(f"{MainView.WIDTH}x{MainView.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)
        QRIcon = PhotoImage(file=f"{os.getcwd()}\View\images\qriconsmall.png")
        Bild1 = PhotoImage(file=f"{os.getcwd()}\View\images\logo.png")
        # QRIcon=PhotoImage(file="images/qriconsmall.png")
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, image=Bild1)  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="CTkButton 1",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_event)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="CTkButton 2",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_event)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="CTkButton 3",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_event)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_left)
        self.switch_1.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=6, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        trv = ttk.Treeview(master=self.frame_info, columns=(1, 2, 3, 4), height=100)
        style = ttk.Style(trv)
        style.theme_use("clam")
        ttk.Style().map("Treeview.Heading", background=[('pressed', '!focus', "#1e1e1f"), ('active', "#2d2e2e"),
                                                        ('disabled', "#383838")])
        style.configure("Treeview.Heading", background="#383838", foreground="white")
        style.configure("Treeview", background="#383838", fieldbackground="#383838", foreground="#383838")
        trv.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)
        trv.column("#0", anchor="center", stretch="yes", width=1)
        trv.column("#1", anchor="center", stretch="yes", width=1)
        trv.column("#2", anchor="center", stretch="yes", width=1)
        trv.column("#3", anchor="center", stretch="yes", width=1)
        trv.column("#4", anchor="center", stretch="yes", width=1)
        trv.heading("#0", text="adad")
        trv.heading("#1", text="dadada")
        trv.heading("#2", text="fafafaf")
        trv.heading("#3", text="fafaf")
        trv.heading("#4", text="fafafaf")

        table_scroll = tkinter.Scrollbar(master=self.frame_info, orient='vertical', command=trv.yview)
        table_scroll.grid(row=0, column=1, sticky='ns')
        trv['yscrollcommand'] = table_scroll.set

        for book, index in zip(values, range(0, len(values) - 1)):
            student = "---------------"
            if book.student is not None:
                student = book.student.surName + " " + book.student.lastName
            trv.insert(parent='', index='end', iid=book.id, text=book.title.title,
                       values=(book.title.isbn, book.title.author, book.title.subject.subjectTitle, student))
            # command=partial(control.handleCallback, (Callback.ADD_BOOKS_BUTTON, book.id))

        # self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        # self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

        # ============ frame_right ============

        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
        #                                        from_=0,
        #                                        to=1,
        #                                        number_of_steps=3,
        #                                        command=self.progressbar.set)
        # self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        # self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
        #                                        command=self.progressbar.set)
        # self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.slider_button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                       height=25,
                                                       text="CTkButton",
                                                       command=self.button_event)
        self.slider_button_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                       height=25,
                                                       text="CTkButton",
                                                       command=self.button_event)
        self.slider_button_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.checkbox_button_1 = customtkinter.CTkButton(master=self.frame_right, height=25, text="QR-Code erstellen",
                                                         image=QRIcon, command=self.button_event, fg_color="#38FF88",
                                                         text_color="Black")
        self.checkbox_button_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="nur ausgeliehene")
        self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="nur abgelaufene")
        self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Suche")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right, text="QR-Code scannen", image=QRIcon,
                                                compound="left", command=self.button_event)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.radio_button_1.select()
        self.switch_2.select()
        # self.slider_1.set(0.2)
        # self.slider_2.set(0.7)
        # self.progressbar.set(0.5)
        # self.slider_button_1.configure(state=tkinter.DISABLED, text="Disabled Button")
        # self.radio_button_3.configure(state=tkinter.DISABLED)
        # self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        self.check_box_2.select()

        self.start()


    def button_event(self):
        print("Button pressed")


    def change_mode(self):
        global style
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
            style.configure("Treeview", background="#383838", fieldbackground="#383838", foreground="white")
            ttk.Style().map("Treeview.Heading",
                            background=[('pressed', '!focus', "#1e1e1f"), ('active', "#2d2e2e"), ('disabled', "#383838")])
            style.configure("Treeview.Heading", background="#383838", foreground="white")
        else:
            customtkinter.set_appearance_mode("light")
            style.configure("Treeview", background="#d6d6d6", fieldbackground="#d6d6d6", foreground="black")
            ttk.Style().map("Treeview.Heading",
                            background=[('pressed', '!focus', "#9a9b9c"), ('active', "#bdbebf"), ('disabled', "#383838")])
            style.configure("Treeview.Heading", background="white", foreground="black")

    def start(self):
        self.mainloop()

    # Hide the current view and disable it
    def killView(self):
        pass
