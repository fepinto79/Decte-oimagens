# -*- coding: utf-8 -*-
import sys
import os
import tkinter as tk

# Adiciona o diretório 'src' ao caminho de busca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import App

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
