"venv/Scripts/pyinstaller.exe" -y --noconsole --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" --onefile -- --add-data "View/images/*.png;View/images" --paths "venv/Lib/site-packages/" FMS.py