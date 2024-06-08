
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageDraw
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import image_manager
import image_recognition
import logging

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Recognition Tester")
        self.template_path = None
        self.screen_image = None

        # Configurando o logger
        logging.basicConfig(filename='app.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Adicionando a barra de menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Template", command=self.load_template)
        file_menu.add_command(label="Capture Screen", command=self.capture_screen)
        file_menu.add_command(label="Recognize", command=self.recognize)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

    def load_template(self):
        initial_dir = r"C:\Users\felip\Pictures\Screenshots"
        self.template_path = filedialog.askopenfilename(initialdir=initial_dir)
        if self.template_path:
            template_image = image_manager.load_image(self.template_path)
            self.template_image = ImageTk.PhotoImage(template_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.template_image)
            logging.info(f"Template loaded: {self.template_path}")

    def capture_screen(self):
        # Minimize the application window
        window = gw.getWindowsWithTitle("Image Recognition Tester")[0]
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

        logging.info("Screen captured")

    def recognize(self):
        if self.template_path and self.screen_image is not None:
            template = cv2.imread(self.template_path)
            loc, val = image_recognition.match_template(self.screen_image, template)
            if val > 0.8:  # Threshold for recognition
                self.canvas.create_rectangle(loc[0], loc[1], loc[0]+template.shape[1], loc[1]+template.shape[0], outline='red')
                self.draw_rectangle_on_image(loc, template.shape[1], template.shape[0])
                logging.info(f"Template recognized at {loc} with confidence {val}")

    def draw_rectangle_on_image(self, loc, width, height):
        # Desenha o retângulo na imagem PIL
        screen_image_pil = Image.fromarray(cv2.cvtColor(self.screen_image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(screen_image_pil)
        draw.rectangle([loc[0], loc[1], loc[0] + width, loc[1] + height], outline="red")
        self.screen_image_with_rect = screen_image_pil

    def save_results(self):
        if hasattr(self, 'screen_image_with_rect'):
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                self.screen_image_with_rect.save(save_path)
                logging.info(f"Results saved to {save_path}")
                messagebox.showinfo("Save Results", f"Imagem salva em: {save_path}")

    def show_about(self):
        messagebox.showinfo("About", "Image Recognition Tester\nVersion 1.0")
        logging.info("About dialog shown")
