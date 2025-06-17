import customtkinter as ctk
import numpy as np
import tifffile
from PIL import Image, ImageTk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from customtkinter import CTkImage


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
        return CTkImage(light_image=im, size=im.size)

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

        print("▶️ Image shape:", img.shape)
        Z, C, Y, X = img.shape
        C = img.shape[1] if img.ndim == 4 else 1  # Handle (Z, C, Y, X) or (Z, Y, X)
        mid = Z // 2

        def array_to_ctkimage_safe(img_slice, cmap_name='magma', target_size=(200, 200)):
            # Normalize
            img = img_slice.astype(np.float32)
            img -= img.min()
            if img.max() > 0:
                img /= img.max()

            # Colormap uygula
            cmap = cm.get_cmap(cmap_name)
            colored = (cmap(img)[:, :, :3] * 255).astype(np.uint8)

            # CTkImage oluştur
            pil_img = Image.fromarray(colored).resize(target_size)
            return CTkImage(light_image=pil_img, size=target_size)


        for c in range(C):
            img_slice = img[mid, c]
            photo = array_to_ctkimage_safe(img_slice)

            frame = ctk.CTkFrame(self.image_frame)
            frame.grid(row=0, column=c, padx=10)

            label = ctk.CTkLabel(frame, image=photo, text=f"Channel {c}")
            label.image = photo
            label.pack()

            menu_var = ctk.StringVar(value="Select")
            menu = ctk.CTkOptionMenu(frame, variable=menu_var, values=self.choices)
            menu.pack(pady=5)

            self.image_labels.append(label)
            self.option_menus.append(menu)
            self.selections.append(menu_var)
  
    def validate_and_proceed(self):
        selected = [s.get() for s in self.selections]
        if "Select" in selected:
            messagebox.showerror("Error", "Please select a type for each channel.")
            return
        self.controller.show_frame("ProcessingPage")