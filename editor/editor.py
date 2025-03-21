import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

from noise_generator.generator import NoiseGenerator
import noise_generator.register
from noise_generator.register import filetypes

# ------------------------- GUI -------------------------
class NoiseGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("2D Noise Texture Generator")
        
        # init component
        self.current_image = None
        self.preview_photo = None
        self._init_ui()
        
        # load noise types
        self.noise_types = NoiseGenerator.get_sorted_noise_types()
        self.noise_type_combobox['values'] = self.noise_types
        self.noise_type_combobox.set(self.noise_types[0]  if self.noise_types else "")
        self._update_parameters()

    def _init_ui(self):
        """init the editor layout"""
        # control oanel
        control_frame = ttk.LabelFrame(self.master, text="control panel", padding=10)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # base parameters
        self._create_basic_controls(control_frame)

        # select noise type
        ttk.Label(control_frame, text="noise type:").grid(row=3, column=0, sticky="e")
        self.noise_type_combobox = ttk.Combobox(
            control_frame,
            state="readonly",
            width=15
        )
        self.noise_type_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.noise_type_combobox.bind("<<ComboboxSelected>>", self._update_parameters)

        # dynamic parameters frame
        self.param_frame = ttk.Frame(control_frame)
        self.param_frame.grid(row=4, column=0, columnspan=2, pady=5)

        # button
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="generator", command=self.generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="save", command=self.save_image).pack(side=tk.LEFT, padx=5)

        # perview
        self.preview_label = ttk.Label(self.master)
        self.preview_label.grid(row=0, column=1, padx=10, pady=10)

    def _create_basic_controls(self, parent):
        """create the basic parameters"""
        ttk.Label(parent, text="width:").grid(row=0, column=0, sticky="e")
        self.width_entry = ttk.Entry(parent, width=8)
        self.width_entry.grid(row=0, column=1, padx=5, pady=2)
        self.width_entry.insert(0, "512")

        ttk.Label(parent, text="height:").grid(row=1, column=0, sticky="e")
        self.height_entry = ttk.Entry(parent, width=8)
        self.height_entry.grid(row=1, column=1, padx=5, pady=2)
        self.height_entry.insert(0, "512")

        # random seed
        ttk.Label(parent, text="seed:").grid(row=2, column=0, sticky="e")
        self.seed_entry = ttk.Entry(parent, width=8)
        self.seed_entry.grid(row=2, column=1, padx=5, pady=2)
        self.seed_entry.insert(0, "0")

    def _update_parameters(self, event=None):
        """update the parameters input component"""
        # clean
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.param_entries = {}

        # get current noise type parameters
        noise_type = self.noise_type_combobox.get()
        try:
            generator = NoiseGenerator.create(noise_type)
        except ValueError:
            return
        params = generator.get_parameters()

        # create new component
        self.param_entries = {}
        for row, (param, label, dtype, default) in enumerate(params):
            ttk.Label(self.param_frame, text=f"{label}:").grid(row=row, column=0, sticky="e")
            
            if dtype == 'int':
                entry = ttk.Spinbox(self.param_frame, from_=1, to=1000, width=8)
            elif dtype == 'float':
                entry = ttk.Entry(self.param_frame, width=10)
                entry.insert(0, str(default))
            elif dtype == 'choice':
                entry = ttk.Combobox(self.param_frame, values=default, state="readonly", width=10)
                entry.set(default[0])
            else:
                entry = ttk.Entry(self.param_frame, width=10)
            
            # clean
            entry.delete(0, tk.END)
            entry.insert(0, str(default))

            entry.grid(row=row, column=1, padx=5, pady=2)
            self.param_entries[param] = (entry, dtype)

    def _get_parameters(self):
        """get all parameters value"""
        try:
            params = {
                'width': int(self.width_entry.get()),
                'height': int(self.height_entry.get()),
                'seed': int(self.seed_entry.get()),
                'noise_type': self.noise_type_combobox.get()
            }

            # dynamic parameters
            for param, (entry, dtype) in self.param_entries.items():
                value = entry.get()
                if dtype == 'int':
                    params[param] = int(value)
                elif dtype == 'float':
                    params[param] = float(value)
                elif dtype == 'choice':
                    params[param] = value
                else:
                    params[param] = value

            return params
        except ValueError as e:
            messagebox.showerror("parameters error", f"invalid input value: {str(e)}")
            return None

    def generate(self):
        """generate noise"""
        params = self._get_parameters()
        if not params:
            return

        try:
            generator = NoiseGenerator.create(params['noise_type'])
            
            noise_params = {k:v for k,v in params.items() 
                          if k not in ['width', 'height', 'seed', 'noise_type']}
            array = generator.generate(
                width=params['width'],
                height=params['height'],
                seed=params['seed'],
                **noise_params
            )

            self.current_image = Image.fromarray(array.astype(np.uint8))
            
            preview_img = self.current_image.resize((params["width"], params["height"]), Image.Resampling.LANCZOS)
            self.preview_photo = ImageTk.PhotoImage(preview_img)
            self.preview_label.configure(image=self.preview_photo)
        except Exception as e:
            messagebox.showerror("generate error", str(e))

    def save_image(self):
        """save image to file"""
        if self.current_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension = ".png",
                filetype = filetypes
            )
            if file_path:
                self.current_image.save(file_path)
                messagebox.showinfo("save successful", f"the image has been saved to:\n{file_path}")