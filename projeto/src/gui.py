import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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
        self.sensitivity = tk.DoubleVar(value=0.8)  # Sensibilidade padrão

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

        settings_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Set Sensitivity", command=self.set_sensitivity)

        # Adicionando uma barra de ferramentas
        toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
        open_button = tk.Button(toolbar, text="Open Template", command=self.load_template)
        open_button.pack(side=tk.LEFT, padx=2, pady=2)
        save_button = tk.Button(toolbar, text="Save Results", command=self.save_results)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Adicionando uma barra de status
        self.status = tk.StringVar()
        self.status.set("Ready")
        status_bar = tk.Label(root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

    def load_template(self):
        initial_dir = r"C:\Users\felip\Pictures\Screenshots"
        self.template_path = filedialog.askopenfilename(initialdir=initial_dir)
        if self.template_path:
            template_image = image_manager.load_image(self.template_path)
            self.template_image = ImageTk.PhotoImage(template_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.template_image)
            self.status.set(f"Template loaded: {self.template_path}")
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

        self.status.set("Screen captured")
        logging.info("Screen captured")

    def recognize(self):
        if self.template_path and self.screen_image is not None:
            template = cv2.imread(self.template_path)
            loc, val = image_recognition.match_template(self.screen_image, template)
            if val > self.sensitivity.get():  # Use the user-defined sensitivity
                self.canvas.create_rectangle(loc[0], loc[1], loc[0]+template.shape[1], loc[1]+template.shape[0], outline='red')
                self.draw_rectangle_on_image(loc, template.shape[1], template.shape[0])
                self.status.set(f"Template recognized at {loc} with confidence {val}")
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
                self.status.set(f"Results saved to {save_path}")
                logging.info(f"Results saved to {save_path}")
                messagebox.showinfo("Save Results", f"Imagem salva em: {save_path}")

    def set_sensitivity(self):
        sensitivity_window = tk.Toplevel(self.root)
        sensitivity_window.title("Set Sensitivity")

        tk.Label(sensitivity_window, text="Sensitivity:").pack(side=tk.LEFT)
        sensitivity_scale = tk.Scale(sensitivity_window, variable=self.sensitivity, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
        sensitivity_scale.pack(side=tk.LEFT)

        tk.Button(sensitivity_window, text="OK", command=sensitivity_window.destroy).pack(side=tk.LEFT)

    def show_about(self):
        messagebox.showinfo("About", "Image Recognition Tester\nVersion 1.0")
        self.status.set("Showing About dialog")
        logging.info("About dialog shown")
