import tkinter as tk

def configure_menu(app):
    file_menu = tk.Menu(app.menu, tearoff=0)
    app.menu.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Open Template', command=app.load_template)
    file_menu.add_command(label='Capture Screen', command=app.capture_screen)
    file_menu.add_command(label='Recognize', command=app.recognize)
    file_menu.add_command(label='Save Results', command=app.save_results)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=app.root.quit)

    help_menu = tk.Menu(app.menu, tearoff=0)
    app.menu.add_cascade(label='Help', menu=help_menu)
    help_menu.add_command(label='About', command=app.show_about)

    settings_menu = tk.Menu(app.menu, tearoff=0)
    app.menu.add_cascade(label='Settings', menu=settings_menu)
    settings_menu.add_command(label='Set Sensitivity', command=app.set_sensitivity)

    app.root.config(menu=app.menu)
