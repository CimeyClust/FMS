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
import asyncio
from Controller import Controller
from Controller.CallbackRegister import Callback
import matplotlib

global QRIcon
global Bild1
global searchicon
global plusicon
global editicon


# Each View (different Window) should have one own class.
# By instantiating the class of the view, the old view should close and the new one should appear


# The main class every other view is inheriting from
class View:
    def initView(self, control: Controller, *values):
        pass

    def killView(self):
        pass

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
matplotlib.use('Agg')


class MainView(View, customtkinter.CTk):

    WIDTH = 1200
    HEIGHT = 600

    def initView(self, control: Controller, *values):
        '''
        Values:
        Title: value[0].title.title
        isbn: value[0].title.isbn
        autor: value[0].title.author
        subject: value[0].title.subject.subjectTitle
        student: value[0].student.name + " " + value.student.surName

        fachbreichsnamen: value[1]

        Callbacks:

        '''

        global QRIcon
        global Bild1
        global style
        global searchicon
        global plusicon
        global editicon

        super().__init__()



        self.trigger1 = False
        self.trigger2 = False
        self.placeholder = "rüherei"
        self.values = values[0]
        self.control = control
        self.title("Fachwerk Management System")
        self.geometry(f"{MainView.WIDTH}x{MainView.HEIGHT}")
        self.minsize(MainView.WIDTH, MainView.HEIGHT)
        # self.minsize(App.WIDTH, App.HEIGHT)
        QRIcon = PhotoImage(file=f"{os.getcwd()}\View\images\qriconsmall.png")
        Bild1 = PhotoImage(file=f"{os.getcwd()}\View\images\logo.png")
        editicon = PhotoImage(file=f"{os.getcwd()}\View\images\stifticon.png")
        searchicon = PhotoImage(file=f"{os.getcwd()}\View\images\searchicon.png")
        plusicon = PhotoImage(file=f"{os.getcwd()}\View\images\plus.png")
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

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, image=Bild1, text="Willkommen! \nBeim Fachwerk Management System \nder Gustav-Heinemann Oberschule!", compound="top")  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

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
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=7, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.trv = ttk.Treeview(master=self.frame_info, columns=(1, 2, 3, 4, 5), height=100, selectmode="browse")
        style = ttk.Style(self.trv)
        style.theme_use("clam")
        ttk.Style().map("Treeview.Heading", background=[('pressed', '!focus', "#1e1e1f"), ('active', "#2d2e2e"),
                                                        ('disabled', "#383838")])
        style.configure("Treeview.Heading", background="#383838", foreground="white")
        style.configure("Treeview", background="#383838", fieldbackground="#383838", foreground="#383838")
        self.trv.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)
        self.trv.column("#0", anchor="center", stretch="yes", width=1)
        self.trv.column("#1", anchor="center", stretch="yes", width=1)
        self.trv.column("#2", anchor="center", stretch="yes", width=1)
        self.trv.column("#3", anchor="center", stretch="yes", width=1)
        self.trv.column("#4", anchor="center", stretch="yes", width=1)
        self.trv.column("#5", anchor="center", stretch="yes", width=1)

        self.trv.heading("#0", text="Buch-ID")
        self.trv.heading("#1", text="Titel")
        self.trv.heading("#2", text="ISBN")
        self.trv.heading("#3", text="Autor")
        self.trv.heading("#4", text="Fach")
        self.trv.heading("#5", text="Schüler")

        table_scroll = tkinter.Scrollbar(master=self.frame_info, orient='vertical', command=self.trv.yview)
        table_scroll.grid(row=0, column=1, sticky='ns')
        self.trv['yscrollcommand'] = table_scroll.set

        for book, index in zip(values[0][0], range(0, len(values[0][0]) - 1)):
            student = ""
            if book.student is not None:
                student = book.student.name + " " + book.student.surname
            self.trv.insert(parent='', index='end', iid=book.id, text=book.id,
                       values=(book.title.title, book.title.isbn, book.title.author, book.title.subject.subjectTitle, student))
            # command=partial(control.handleCallback, (Callback.ADD_BOOKS_BUTTON, book.id))

        self.trv.bind('<<TreeviewSelect>>', self.activate)
        self.trv.bind("<Double-1>", self.editdouble)
        # self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        # self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

        # ============ frame_right ============

        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Anzeigen:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=0, text="Alle",
                                                           command=lambda: self.control.handleCallback(Callback.RELOAD_TABLE, "all"))
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="nw")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=1, text="Verfügbare",
                                                           command=lambda: self.control.handleCallback(Callback.RELOAD_TABLE, "available"))
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="nw")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=2, text="Ausgeliehene",
                                                           command=lambda: self.control.handleCallback(Callback.RELOAD_TABLE, "unavailable"))
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="nw")

        #command=partial(control.handleCallback, (Callback.SELECTION, (self.radio_var)))

        # self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
        #                                        from_=0,
        #                                        to=1,
        #                                        number_of_steps=3,
        #                                        command=self.progressbar.set)
        # self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        # self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
        #                                        command=self.progressbar.set)
        # self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.slider_button_1 = customtkinter.CTkButton(master=self.frame_right, text="Erstellen", command=self.create, text_color="Black", image=plusicon, fg_color=("gray75", "White"), hover_color="#9c9a9a")
        self.slider_button_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_button_2 = customtkinter.CTkButton(master=self.frame_right, text="Bearbeiten", command=self.edit, state=tkinter.DISABLED, fg_color="#737373", text_color="Black", image=editicon)
        self.slider_button_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.checkbox_button_1 = customtkinter.CTkButton(master=self.frame_right, text="QR-Code erstellen", image=QRIcon, command=self.button_event, text_color="Black", fg_color=("gray75", "White"), hover_color="#9c9a9a")
        self.checkbox_button_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.checkbox_button_2 = customtkinter.CTkButton(master=self.frame_info, text="Ausleihen", command=self.button_event, fg_color="#737373", text_color="Black", state=tkinter.DISABLED)
        self.checkbox_button_2.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="we")

        self.entry = customtkinter.CTkEntry(master=self.frame_right, width=120, placeholder_text="Suche")
        self.entry.grid(row=11, column=0, columnspan=2, pady=25, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right, text="Suchen", compound="left", text_color="Black", image=searchicon)
        self.button_5.grid(row=11, column=2, columnspan=1, pady=25, padx=20, sticky="we")


        ''', command=partial(control.handleCallback, (Callback.SEARCH, (self.entry.get())))'''
        # set default values
        self.radio_button_1.select()
        self.switch_2.select()
        # self.slider_1.set(0.2)
        # self.slider_2.set(0.7)
        # self.progressbar.set(0.5)
        # self.slider_button_1.configure(state=tkinter.DISABLED, text="Disabled Button")
        # self.radio_button_3.configure(state=tkinter.DISABLED)
        # self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        # self.check_box_2.select()

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

    def activate(self, placeholder):
        self.slider_button_2.configure(state=tkinter.NORMAL, fg_color=("gray75", "White"), hover_color="#9c9a9a")
        self.checkbox_button_2.configure(fg_color="#38FF88", hover_color="#30d973", state=tkinter.NORMAL)
        curItem = self.trv.focus()
        curDict = self.trv.item(curItem)
        value=curDict.get("values")
        if value[4]=="":
            self.checkbox_button_2.configure(fg_color="#38FF88", hover_color="#30d973", state=tkinter.NORMAL, text="Ausleihen", command=self.leasing)
        else:
            self.checkbox_button_2.configure(fg_color="#ff5e5e", hover_color="#c94949", state=tkinter.NORMAL, text="Zurückgeben", command=self.button_event)

    def editdouble(self, placeholder):
        self.edit()

    def edit(self):
        if self.trigger1: return
        curItemID = self.trv.focus()
        if not curItemID=="":
            curItem = self.trv.item(curItemID)
            curDict = curItem.get("values")
            self.trigger1=True
            self.editwindow=customtkinter.CTk()
            self.editwindow.title('Eintrag editieren')
            self.editwindow.geometry('1000x453')
            self.editwindow.resizable(0,0)
            self.frame_input = customtkinter.CTkFrame(master=self.editwindow)
            self.frame_input.grid(row=0, column=0, columnspan=4, rowspan=6, pady=20, padx=20, sticky="nsew")

            self.subject=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="Fach:", text_font='Arial 13').grid(row=0, column=0, columnspan=1, pady=20, padx=5, sticky="w")
            self.selected_subject = tkinter.StringVar()
            self.subject_cb = ttk.Combobox(master=self.frame_input, textvariable=self.selected_subject)
            self.subject_cb.grid(row=0, column=4, columnspan=3, pady=20, padx=20, sticky="nesw")
            self.subject_cb['state'] = 'readonly'
            self.subject_cb['values'] = self.values[1]
            #self.subject_cb['values'] = [book.title.author for book, index in zip(values, range(0, len(values)-1))]

            self.title=customtkinter.CTkLabel(master=self.frame_input,anchor=tkinter.W, justify=tkinter.LEFT, text="Titel:", text_font='Arial 13').grid(row=1, column=0, columnspan=1, pady=20, padx=0, sticky="w")
            self.titleentry = customtkinter.CTkEntry(master=self.frame_input, width=120)
            self.titleentry.grid(row=1, column=4, columnspan=3, pady=20, padx=20, sticky="nesw")

            self.isbn=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="ISBN:", text_font='Arial 13').grid(row=2, column=0, columnspan=1, pady=20, padx=0, sticky="w")
            self.isbnentry = customtkinter.CTkEntry(master=self.frame_input, width=120)
            self.isbnentry.grid(row=2, column=4, columnspan=3, pady=20, padx=20, sticky="nesw")

            self.autor=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="Autor:", text_font='Arial 13').grid(row=3, column=0, columnspan=1, pady=20, padx=0, sticky="w")
            self.autorentry = customtkinter.CTkEntry(master=self.frame_input, width=120)
            self.autorentry.grid(row=3, column=4, columnspan=3, pady=20, padx=20, sticky="nesw")

            self.amount=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="Anzahl", text_font='Arial 13').grid(row=4, column=0, columnspan=1, pady=20, padx=0, sticky="w")
            self.amountentry = customtkinter.CTkEntry(master=self.frame_input, width=790)
            self.amountentry.grid(row=4, column=4, columnspan=3, pady=20, padx=20, sticky="nesw")

            self.finish = customtkinter.CTkButton(self.editwindow, text="Fertig", fg_color="#38FF88", hover_color="#30d973", text_color="Black").grid(row=7, column=2, columnspan=1, pady=10, padx=20, sticky="nesw")
            self.stop = customtkinter.CTkButton(self.editwindow, text="Abbrechen",fg_color="#ff5e5e", hover_color="#c94949", text_color="Black", command=self.on_closing).grid(row=7, column=1, columnspan=1, pady=10, padx=20, sticky="nesw")
            self.titleentry.insert(0, curDict[0])
            self.isbnentry.insert(0, curDict[1])
            self.autorentry.insert(0, curDict[2])
            self.amountentry.insert(0, 5)
            self.editwindow.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.editwindow.mainloop()

    def leasing(self):
        if self.trigger1: return
        curItemID = self.trv.focus()
        curItem = self.trv.item(curItemID)
        curDict = curItem.get("values")
        self.trigger1=True
        self.editwindow=customtkinter.CTk()
        windowtitle=(curDict[0]+" ausleihen")
        self.editwindow.title(windowtitle)
        self.editwindow.geometry('780x250')
        self.editwindow.resizable(0,0)
        self.frame_input = customtkinter.CTkFrame(master=self.editwindow)
        self.frame_input.grid(row=0, column=0, columnspan=4, rowspan=6, pady=20, padx=20, sticky="nsew")

        self.title=customtkinter.CTkLabel(master=self.frame_input,anchor=tkinter.W, justify=tkinter.LEFT, text="Vorname des Schülers:", text_font='Arial 13').grid(row=0, column=0, columnspan=1, pady=20, padx=0, sticky="w")
        self.titleentry = customtkinter.CTkEntry(master=self.frame_input, width=120)
        self.titleentry.grid(row=0, column=4, columnspan=3, pady=20, padx=20, sticky="nesw")

        self.isbn=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="Nachname des Schülers:", text_font='Arial 13').grid(row=1, column=0, columnspan=1, pady=20, padx=0, sticky="w")
        self.isbnentry = customtkinter.CTkEntry(master=self.frame_input, width=500)
        self.isbnentry.grid(row=1, column=4, columnspan=3, pady=20, padx=20, sticky="nesw")

        self.finish = customtkinter.CTkButton(self.editwindow, text="Fertig", fg_color="#38FF88", hover_color="#30d973", text_color="Black").grid(row=7, column=2, columnspan=1, pady=10, padx=20, sticky="nesw")
        self.stop = customtkinter.CTkButton(self.editwindow, text="Abbrechen",fg_color="#ff5e5e", hover_color="#c94949", text_color="Black", command=self.on_closing).grid(row=7, column=1, columnspan=1, pady=10, padx=20, sticky="nesw")
        self.editwindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.editwindow.mainloop()

    def create(self):
        if self.trigger1: return
        self.trigger1=True
        self.editwindow=customtkinter.CTk()
        self.editwindow.title('Fachwerk Managment System')
        self.editwindow.geometry('1000x520')
        self.editwindow.resizable(0,0)

        self.frame_input = customtkinter.CTkFrame(master=self.editwindow)
        self.frame_input.grid(row=0, column=0, columnspan=4, rowspan=7, pady=20, padx=20, sticky="nsew")

        self.createsubjectbutton = customtkinter.CTkButton(master=self.frame_input, text="Fachbereich erstellen/löschen", text_color="Black", width=30, command=self.createsubject).grid(row=0, column=10, columnspan=1, pady=20, padx=40, sticky="nesw")
        self.titleheading=customtkinter.CTkLabel(master=self.frame_input,anchor=tkinter.W, justify=tkinter.LEFT, text="Titel erstellen:", text_font='Arial 17').grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="w")

        self.subject=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="Fach:", text_font='Arial 13').grid(row=1, column=0, columnspan=1, pady=20, padx=5, sticky="w")
        self.selected_subject = tkinter.StringVar()
        self.subject_cb = ttk.Combobox(master=self.frame_input, textvariable=self.selected_subject)
        self.subject_cb.grid(row=1, column=1, columnspan=10, pady=20, padx=20, sticky="nesw")
        self.subject_cb['state'] = 'readonly'
        self.subject_cb['values'] = self.values[1]
        #self.subject_cb['values'] = [book.title.author for book, index in zip(values, range(0, len(values)-1))]

        self.title=customtkinter.CTkLabel(master=self.frame_input,anchor=tkinter.W, justify=tkinter.LEFT, text="Titel:", text_font='Arial 13').grid(row=2, column=0, columnspan=1, pady=20, padx=0, sticky="w")
        self.titleentry = customtkinter.CTkEntry(master=self.frame_input, width=120)
        self.titleentry.grid(row=2, column=1, columnspan=10, pady=20, padx=20, sticky="nesw")

        self.isbn=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="ISBN:", text_font='Arial 13').grid(row=3, column=0, columnspan=1, pady=20, padx=0, sticky="w")
        self.isbnentry = customtkinter.CTkEntry(master=self.frame_input, width=120)
        self.isbnentry.grid(row=3, column=1, columnspan=10, pady=20, padx=20, sticky="nesw")

        self.autor=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="Autor:", text_font='Arial 13').grid(row=4, column=0, columnspan=1, pady=20, padx=0, sticky="w")
        self.autorentry = customtkinter.CTkEntry(master=self.frame_input, width=120)
        self.autorentry.grid(row=4, column=1, columnspan=10, pady=20, padx=20, sticky="nesw")

        self.amount=customtkinter.CTkLabel(master=self.frame_input, anchor=tkinter.W, justify=tkinter.LEFT, text="Anzahl", text_font='Arial 13').grid(row=5, column=0, columnspan=1, pady=20, padx=0, sticky="w")
        self.amountentry = customtkinter.CTkEntry(master=self.frame_input, width=790)
        self.amountentry.grid(row=5, column=1, columnspan=10, pady=20, padx=20, sticky="nesw")

        self.finish = customtkinter.CTkButton(self.editwindow, text="Fertig",fg_color="#38FF88", hover_color="#30d973", text_color="Black").grid(row=7, column=2, columnspan=1, pady=10, padx=20, sticky="nesw")
        self.stop = customtkinter.CTkButton(self.editwindow, text="Abbrechen",fg_color="#ff5e5e", hover_color="#c94949", text_color="Black", command=self.on_closing).grid(row=7, column=1, columnspan=1, pady=10, padx=20, sticky="nesw")

        self.editwindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.editwindow.mainloop()

    def createsubject(self):
        if self.trigger2: return
        curItemID = self.trv.focus()
        curItem = self.trv.item(curItemID)
        curDict = curItem.get("values")
        self.trigger2=True
        self.subjectwindow=customtkinter.CTk()
        self.subjectwindow.title('Fachbereich erstellen/löschen')
        self.subjectwindow.geometry('1000x315')
        self.subjectwindow.resizable(0,0)
        self.frame_input1 = customtkinter.CTkFrame(master=self.subjectwindow)
        self.frame_input1.grid(row=0, column=0, columnspan=4, rowspan=6, pady=20, padx=20, sticky="nsew")

        self.createtitle=customtkinter.CTkLabel(master=self.frame_input1, anchor=tkinter.W, justify=tkinter.LEFT, text="Erstellen:", text_font='Arial 13').grid(row=0, column=0, columnspan=1, pady=(20, 10), padx=(10, 10), sticky="w")
        self.titleentry = customtkinter.CTkEntry(master=self.frame_input1, width=735)
        self.titleentry.grid(row=1, column=0, columnspan=3, pady=10, padx=(30, 10), sticky="nesw")
        self.createbut = customtkinter.CTkButton(master=self.frame_input1, text="Fachbereich erstellen", text_color="Black", width=10, command=lambda: self.control.handleCallback(Callback.ADD_SUBJECT, self.titleentry)).grid(row=1, column=4, columnspan=1, pady=10, padx=(10, 30), sticky="nesw")

        self.deletetitle=customtkinter.CTkLabel(master=self.frame_input1, anchor=tkinter.W, justify=tkinter.LEFT, text="Löschen:", text_font='Arial 13').grid(row=2, column=0, columnspan=1, pady=10, padx=10, sticky="w")
        self.selected_subject1 = tkinter.StringVar()
        self.subject_cb1 = ttk.Combobox(master=self.frame_input1, textvariable=self.selected_subject)
        self.subject_cb1.grid(row=3, column=0, columnspan=3, pady=(10, 20), padx=(30, 10), sticky="nesw")
        self.subject_cb1['state'] = 'readonly'
        self.subject_cb1['values'] = self.values[1]
        self.createbut = customtkinter.CTkButton(master=self.frame_input1, text="Fachbereich löschen", text_color="Black", command=lambda: self.control.handleCallback(Callback.DELETE_SUBJECT, self.selected_subject1)).grid(row=3, column=4, columnspan=1, pady=(10, 20), padx=(10, 30), sticky="nesw")

        self.finish = customtkinter.CTkButton(self.subjectwindow, text="Fertig", fg_color="#38FF88", hover_color="#30d973", text_color="Black", command=self.on_closing2).grid(row=7, column=1, columnspan=2, pady=10, padx=20, sticky="nesw")

        self.subjectwindow.protocol("WM_DELETE_WINDOW", self.on_closing2)
        self.subjectwindow.mainloop()

    def reloadTable(self, books):
        for row in self.trv.get_children():
            self.trv.delete(row)

        for book, index in zip(books, range(0, len(books) - 1)):
            student = ""
            if book.student is not None:
                student = book.student.name + " " + book.student.surname
            self.trv.insert(parent='', index='end', iid=book.id, text=book.id,
                            values=(book.title.title, book.title.isbn, book.title.author, book.title.subject.subjectTitle, student))


    def on_closing(self, event=0):
        self.trigger1=False
        self.editwindow.destroy()

    def on_closing2(self, event=0):
        self.trigger2=False
        self.subjectwindow.destroy()

    # Hide the current view and disable it
    def killView(self):
        pass
