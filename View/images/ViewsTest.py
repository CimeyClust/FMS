import sys
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import PhotoImage, ttk
from Controller import Controller
from Controller.CallbackRegister import Callback

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


class MainView(View, customtkinter.CTk):
    WIDTH = 1200
    HEIGHT = 600

    def initView(self, control: Controller, *values):
        '''
        Values:
        Title: values[0].title.title
        isbn: values[0].title.isbn
        autor: values[0].title.author
        subject: values[0].title.subject.subjectTitle
        student: values[0].student.name + " " + value.student.surName

        fachbereichsnamen: values[1]
        HatDatenbank?: values[2]

        Callbacks:

        '''

        self.control = control
        if values[0][2]:
            self.setupconnection()

        super().__init__()

        self.trigger1 = False
        self.trigger2 = False
        self.placeholder = "rüherei"
        self.values = values[0]
        self.title("Fachwerk Management System")
        self.geometry(f"{MainView.WIDTH}x{MainView.HEIGHT}")
        self.state("zoomed")
        self.minsize(MainView.WIDTH, MainView.HEIGHT)
        # self.minsize(App.WIDTH, App.HEIGHT)
        # Set icons
        self.iconbitmap(f"View\images\logo.ico")

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

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, image=Bild1,
                                              text="Willkommen! \nBeim Fachwerk Management System \nder Gustav-Heinemann Oberschule!",
                                              compound="top")  # font name and size in px
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

        self.trv = ttk.Treeview(master=self.frame_info, columns=(1, 2, 3, 4, 5, 6), height=100, selectmode="browse")
        style = ttk.Style(self.trv)
        style.theme_use("clam")
        ttk.Style().map("Treeview.Heading", background=[('pressed', '!focus', "#1e1e1f"), ('active', "#2d2e2e"),
                                                        ('disabled', "#383838")])
        style.configure("Treeview.Heading", background="#383838", foreground="white")
        style.configure("Treeview", background="#383838", fieldbackground="#383838", foreground="#383838")
        self.trv.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)
        self.trv.column("#0", anchor="center", stretch="yes", width=0)
        self.trv.column("#1", anchor="center", stretch="yes", width=1)
        self.trv.column("#2", anchor="center", stretch="yes", width=1)
        self.trv.column("#3", anchor="center", stretch="yes", width=1)
        self.trv.column("#4", anchor="center", stretch="yes", width=1)
        self.trv.column("#5", anchor="center", stretch="yes", width=1)
        self.trv.column("#6", anchor="center", stretch="yes", width=1)

        self.trv.heading("#0", text="Buch-ID")
        self.trv.heading("#1", text="Titel")
        self.trv.heading("#2", text="ISBN")
        self.trv.heading("#3", text="Autor")
        self.trv.heading("#4", text="Fach")
        self.trv.heading("#5", text="Schüler")
        self.trv.heading("#6", text="Klasse")

        table_scroll = tkinter.Scrollbar(master=self.frame_info, orient='vertical', command=self.trv.yview)
        table_scroll.grid(row=0, column=1, sticky='ns')
        self.trv['yscrollcommand'] = table_scroll.set

        for book, index in zip(values[0][0], range(1, len(values[0][0]) + 2)):
            student = ""
            group = ""
            if book.student is not None:
                student = book.student.name + " " + book.student.surname
                group = book.student.schoolClass
            self.trv.insert(parent='', index='end', iid=index, text=book.id,
                            values=(
                                book.title.title, book.title.isbn, book.title.author, book.title.subject.subjectTitle,
                                student, group))
            # command=partial(control.handleCallback, (Callback.ADD_BOOKS_BUTTON, book.id))

        self.trv.bind('<<TreeviewSelect>>', self.activate)
        self.trv.bind("<Double-1>", lambda x: self.control.handleCallback(Callback.TITLE_EDIT_INIT, self.trv))
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
                                                           command=lambda: self.control.handleCallback(
                                                               Callback.RELOAD_TABLE, "all"))
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="nw")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=1, text="Verfügbare",
                                                           command=lambda: self.control.handleCallback(
                                                               Callback.RELOAD_TABLE, "available"))
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="nw")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=2, text="Ausgeliehene",
                                                           command=lambda: self.control.handleCallback(
                                                               Callback.RELOAD_TABLE, "unavailable"))
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="nw")

        # command=partial(control.handleCallback, (Callback.SELECTION, (self.radio_var)))

        # self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
        #                                        from_=0,
        #                                        to=1,
        #                                        number_of_steps=3,
        #                                        command=self.progressbar.set)
        # self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        # self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
        #                                        command=self.progressbar.set)
        # self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.slider_button_1 = customtkinter.CTkButton(master=self.frame_right, text="Erstellen", command=self.create,
                                                       text_color=("Black", "#e3e3e3"), image=plusicon,
                                                       fg_color=("gray75", "gray30"), hover_color="#9c9a9a")
        self.slider_button_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_button_2 = customtkinter.CTkButton(master=self.frame_right, text="Bearbeiten",
                                                       command=lambda: self.control.handleCallback(
                                                           Callback.TITLE_EDIT_INIT, self.trv), state=tkinter.DISABLED,
                                                       fg_color="#737373", text_color=("Black", "#e3e3e3"),
                                                       image=editicon)
        self.slider_button_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.checkbox_button_1 = customtkinter.CTkButton(master=self.frame_right, text="QR-Code erstellen",
                                                         image=QRIcon, command=lambda: self.control.handleCallback(
                Callback.CREATE_QRCODE, self.trv), state=tkinter.DISABLED, text_color=("Black", "#e3e3e3"),
                                                         fg_color="#737373", hover_color="#9c9a9a")
        self.checkbox_button_1.grid(row=8, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.checkbox_button_3 = customtkinter.CTkButton(master=self.frame_right, text="Löschen", image=trashiconw,
                                                         command=lambda: self.control.handleCallback(
                                                             Callback.BOOK_DELETE, self.trv), state=tkinter.DISABLED,
                                                         text_color="Black", fg_color="#737373", hover_color="#9c9a9a")
        self.checkbox_button_3.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.checkbox_button_2 = customtkinter.CTkButton(master=self.frame_info, text="Ausleihen", command=self.leasing,
                                                         fg_color="#737373", text_color="Black", state=tkinter.DISABLED)
        self.checkbox_button_2.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="we")

        """self.searchLabel = customtkinter.CTkLabel(master=self.frame_right,
                                                  text="Suchen:", text_font='Arial 13 bold')
        self.searchLabel.grid(row=8, column=0, columnspan=1, pady=0, padx=0, sticky="es")"""

        self.sv = tkinter.StringVar()
        self.sv.trace("w", lambda name, index, mode, sv=self.sv: self.control.handleCallback(Callback.SEARCH, self.sv))
        self.entry = customtkinter.CTkEntry(master=self.frame_right, width=120, textvariable=self.sv,
                                            placeholder_text="Suchen")
        self.entry.grid(row=8, column=0, columnspan=2, pady=25, padx=20, sticky="we")

        '''self.button_5 = customtkinter.CTkButton(master=self.frame_right, text="Suchen", compound="left", text_color="Black", image=trashicon)
        self.button_5.grid(row=11, column=2, columnspan=1, pady=25, padx=20, sticky="we")'''

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

        self.protocol("WM_DELETE_WINDOW", self.killProgram)
        self.start()