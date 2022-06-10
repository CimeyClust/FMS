###########################################################################
#
# CallbackRegister.py
# Program made by Jan, Sinan and Leon for the FMS project.
#
###########################################################################

from enum import Enum


class Callback(Enum):
    ADD_SUBJECT = 1,
    DELETE_SUBJECT = 2,
    RELOAD_TABLE = 3,
    CREATE_QRCODE = 4,
    BORROW_BOOK = 5,
    RETURN_BOOK = 6,
    SEARCH = 7,
    TITLE_CREATE = 8,
    TITLE_EDIT_INIT = 9,
    BOOK_DELETE = 10,
    TITLE_EDIT = 11,
    ADD_DB_CONNECTION = 12
