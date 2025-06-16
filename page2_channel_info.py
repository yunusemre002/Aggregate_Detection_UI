import customtkinter as ctk
import numpy as np
import tifffile
from PIL import Image, ImageTk
import os
from tkinter import messagebox

class ChannelInfoPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.image_labels = []
        self.option_menus = []
        self.selections = []
        self.choices = ["Select", "cell body", "nuclei", "aggregate", "other"]

        self.title = ctk.CTkLabel(self, text="Channel Assignment", font=ctk.CTkFont(size=20, weight="bold"))
        self.title.pack(pady=10)

        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.pack(pady=10)

        self.param_frame = ctk.CTkFrame(self)
        self.param_frame.pack(pady=10)

        # Params
        self.cell_diam = ctk.CTkEntry(self.param_frame, placeholder_text="Cell Body Diameter (default: 100)")
        self.cell_diam.insert(0, "100")
        self.cell_diam.grid(row=0, column=0, padx=10, pady=5)

        self.nuclei_diam = ctk.CTkEntry(self.param_frame, placeholder_text="Nuclei Diameter (default: 25)")
        self.nuclei_diam.insert(0, "25")
        self.nuclei_diam.grid(row=0, column=1, padx=10, pady=5)

        self.threshold = ctk.CTkEntry(self.param_frame, placeholder_text="Aggregate Threshold (default: 0.5)")
        self.threshold.insert(0, "0.5")
        self.threshold.grid(row=0, column=2, padx=10, pady=5)

        self.start_btn = ctk.CTkButton(self, text="Start Analyze", command=self.validate_and_proceed)
        self.start_btn.pack(pady=20)

    def tk_image_from_array(self, arr):
        im = Image.fromarray(arr).resize((150, 150))
        return ImageTk.PhotoImage(im)

    def tkraise(self):
        super().tkraise()
        self.load_images()

def load_images(self):
    for widget in self.image_frame.winfo_children():
        widget.destroy()
    self.image_labels.clear()
    self.option_menus.clear()
    self.selections.clear()

    tif_path = self.controller.tif_path
    img = tifffile.imread(tif_path)

    # Transpose to (Z, C, Y, X) for consistency
    if img.ndim == 5:  # (T, C, Z, Y, X)
        img = img[0]  # take first T
    if img.ndim == 4:  # (C, Z, Y, X)
        img = np.transpose(img, (1, 0, 2, 3))  # (Z, C, Y, X)

    Z, C, Y, X = img.shape
    mid = Z // 2

    for c in range(C):
        img_slice = img[mid, c]
        img_slice = ((img_slice - img_slice.min()) / (img_slice.ptp()) * 255).astype(np.uint8)

        photo = self.tk_image_from_array(img_slice)
        label = ctk.CTkLabel(self.image_frame, image=photo, text=f"Channel {c}")
        label.image = photo
        label.grid(row=0, column=c, padx=5)
        self.image_labels.append(label)

        var = ctk.StringVar(value=self.choices[0])
        option = ctk.CTkOptionMenu(self.image_frame, values=self.choices, variable=var)
        option.grid(row=1, column=c, padx=5, pady=5)
        self.option_menus.append(option)
        self.sele


    def validate_and_proceed(self):
        selected = [s.get() for s in self.selections]
        if "Select" in selected:
            messagebox.showerror("Error", "Please select a type for each channel.")
            return
        self.controller.show_frame("ProcessingPage")