"venv/Scripts/pyinstaller.exe" -y --icon="View/images/logo.ico" --noconsole --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" --add-data "View/images/*.png;View/images" --add-data "View/images/*.ico;View/images" --paths "venv/Lib/site-packages/" FMS.py