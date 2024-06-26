﻿import tkinter as tk
from tkinter import filedialog, messagebox
from src.menu.configure_menu import configure_menu
from src.toolbar.configure_toolbar import configure_toolbar
from src.status_bar.configure_status_bar import configure_status_bar
from PIL import ImageTk, Image, ImageDraw
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import src.image_manager as image_manager
import src.image_recognition as image_recognition
import logging

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Recognition Tester')
        self.template_path = None
        self.screen_image = None
        self.sensitivity = tk.DoubleVar(value=0.8)  # Sensibilidade padrão

        # Configurando o logger
        logging.basicConfig(filename='app.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Configurando o menu
        self.menu = tk.Menu(self.root)
        configure_menu(self)

        # Configurando a barra de ferramentas
        configure_toolbar(self)

        # Configurando a barra de status
        self.status = tk.StringVar()
        self.status.set('Ready')
        configure_status_bar(self)

        # Ajustando o layout
        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=800, height=600, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def load_template(self):
        initial_dir = r'C:\\Users\\felip\\Pictures\\Screenshots'
        self.template_path = filedialog.askopenfilename(initialdir=initial_dir)
        if self.template_path:
            template_image = image_manager.load_image(self.template_path)
            self.template_image = ImageTk.PhotoImage(template_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.template_image)
            self.status.set(f'Template loaded: {self.template_path}')
            logging.info(f'Template loaded: {self.template_path}')

    def capture_screen(self):
        # Minimize the application window
        window = gw.getWindowsWithTitle('Image Recognition Tester')[0]
        window.minimize()
        # Wait a moment to ensure the window is minimized
        pyautogui.sleep(1)

        # Capture the entire screen
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        self.screen_image = screenshot

        # Restore the application window
        window.restore()
        pyautogui.sleep(1)

        # Redimensiona o canvas para o tamanho da captura de tela
        self.canvas.config(width=self.screen_image.shape[1], height=self.screen_image.shape[0])

        # Exibe a captura de tela no canvas
        screen_image_pil = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        self.screen_image_tk = ImageTk.PhotoImage(screen_image_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.screen_image_tk)

        self.status.set('Screen captured')
        logging.info('Screen captured')

    def recognize(self):
        if self.template_path and self.screen_image is not None:
            template = cv2.imread(self.template_path, 0)
            screen_gray = cv2.cvtColor(self.screen_image, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = self.sensitivity.get()
            loc = np.where(res >= threshold)

            # Marcar todas as ocorrências
            for pt in zip(*loc[::-1]):
                self.canvas.create_rectangle(pt[0], pt[1], pt[0] + template.shape[1], pt[1] + template.shape[0], outline='red')
                self.draw_rectangle_on_image(pt, template.shape[1], template.shape[0])

            self.status.set(f'Template recognized in multiple locations')
            logging.info(f'Template recognized in multiple locations')

    def draw_rectangle_on_image(self, loc, width, height):
        # Desenha o retângulo na imagem PIL
        screen_image_pil = Image.fromarray(cv2.cvtColor(self.screen_image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(screen_image_pil)
        draw.rectangle([loc[0], loc[1], loc[0] + width, loc[1] + height], outline='red')
        self.screen_image_with_rect = screen_image_pil

    def save_results(self):
        if hasattr(self, 'screen_image_with_rect'):
            save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
            if save_path:
                self.screen_image_with_rect.save(save_path)
                self.status.set(f'Results saved to {save_path}')
                logging.info(f'Results saved to {save_path}')
                messagebox.showinfo('Save Results', f'Imagem salva em: {save_path}')

    def set_sensitivity(self):
        sensitivity_window = tk.Toplevel(self.root)
        sensitivity_window.title('Set Sensitivity')

        tk.Label(sensitivity_window, text='Sensitivity:').pack(side=tk.LEFT)
        sensitivity_scale = tk.Scale(sensitivity_window, variable=self.sensitivity, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
        sensitivity_scale.pack(side=tk.LEFT)

        tk.Button(sensitivity_window, text='OK', command=sensitivity_window.destroy).pack(side=tk.LEFT)

    def show_about(self):
        messagebox.showinfo('About', 'Image Recognition Tester\\nVersion 1.0')
        self.status.set('Showing About dialog')
        logging.info('About dialog shown')
