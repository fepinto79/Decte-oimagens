import tkinter as tk

def configure_status_bar(app):
    status_bar = tk.Label(app.root, textvariable=app.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
