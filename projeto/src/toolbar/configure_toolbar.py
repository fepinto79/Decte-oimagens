import tkinter as tk

def configure_toolbar(app):
    toolbar = tk.Frame(app.root, bd=1, relief=tk.RAISED)
    
    open_button = tk.Button(toolbar, text='Open Template', command=app.load_template)
    open_button.pack(side=tk.LEFT, padx=2, pady=2)

    capture_button = tk.Button(toolbar, text='Capture Screen', command=app.capture_screen)
    capture_button.pack(side=tk.LEFT, padx=2, pady=2)

    recognize_button = tk.Button(toolbar, text='Recognize', command=app.recognize)
    recognize_button.pack(side=tk.LEFT, padx=2, pady=2)

    sensitivity_button = tk.Button(toolbar, text='Set Sensitivity', command=app.set_sensitivity)
    sensitivity_button.pack(side=tk.LEFT, padx=2, pady=2)

    save_button = tk.Button(toolbar, text='Save Results', command=app.save_results)
    save_button.pack(side=tk.LEFT, padx=2, pady=2)

    toolbar.pack(side=tk.TOP, fill=tk.X)
