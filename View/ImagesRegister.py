from enum import Enum
from tkinter import PhotoImage


class Image(Enum):
    Logo = PhotoImage(file=f"View\images\logo.png")
    QRIcon = PhotoImage(file=f"View\images\qriconsmall.png")
    editicon = PhotoImage(file=f"View\images\stifticon.png")
    trashicon = PhotoImage(file=f"View\images\\trashicon.png")
    plusicon = PhotoImage(file=f"View\images\plus.png")
    QRIconw = PhotoImage(file=f"View\images\qriconsmallw.png")
    editiconw = PhotoImage(file=f"View\images\stifticonw.png")
    trashiconw = PhotoImage(file=f"View\images\\trashiconw.png")
    plusiconw = PhotoImage(file=f"View\images\plusw.png")