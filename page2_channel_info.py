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
        self.choices = ["Select", "Cell body", "Nuclei", "Aggregate", "Other"]

        self.title = ctk.CTkLabel(self, text="Channel Assignment", font=ctk.CTkFont(size=20, weight="bold"))
        self.title.pack(pady=10)

        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.pack(pady=10)

        self.param_frame = ctk.CTkFrame(self)
        self.param_frame.pack(pady=10)

        # Params
        # self.cell_diam = ctk.CTkEntry(self.param_frame, placeholder_text="Cell Body Diameter (default: 100)")
        # self.cell_diam.insert(0, "100")
        # self.cell_diam.grid(row=0, column=0, padx=10, pady=5)

        # self.nuclei_diam = ctk.CTkEntry(self.param_frame, placeholder_text="Nuclei Diameter (default: 25)")
        # self.nuclei_diam.insert(0, "25")
        # self.nuclei_diam.grid(row=0, column=1, padx=10, pady=5)

        # self.threshold = ctk.CTkEntry(self.param_frame, placeholder_text="Aggregate Threshold (default: 0.5)")
        # self.threshold.insert(0, "0.5")
        # self.threshold.grid(row=0, column=2, padx=10, pady=5)
        
        # === Parametre Başlığı ===
        self.param_title = ctk.CTkLabel(self.param_frame, text="Model Parameters", font=ctk.CTkFont(size=16, weight="bold"))
        self.param_title.grid(row=0, column=0, columnspan=2, pady=(5, 0))

        # === Açıklama ===
        self.param_desc = ctk.CTkLabel(self.param_frame, text="These are default values. You can change them if needed.", font=ctk.CTkFont(size=12), text_color="gray")
        self.param_desc.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # === Parametreler ===
        self.cell_diam_label = ctk.CTkLabel(self.param_frame, text="Diameter (Cell Body)")
        self.cell_diam_label.grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.cell_diam = ctk.CTkEntry(self.param_frame)
        self.cell_diam.insert(0, "100")
        self.cell_diam.grid(row=2, column=1, padx=5, pady=3)

        self.nuclei_diam_label = ctk.CTkLabel(self.param_frame, text="Diameter (Nuclei)")
        self.nuclei_diam_label.grid(row=3, column=0, sticky="e", padx=5, pady=3)
        self.nuclei_diam = ctk.CTkEntry(self.param_frame)
        self.nuclei_diam.insert(0, "25")
        self.nuclei_diam.grid(row=3, column=1, padx=5, pady=3)

        self.threshold_label = ctk.CTkLabel(self.param_frame, text="Aggregate Threshold")
        self.threshold_label.grid(row=4, column=0, sticky="e", padx=5, pady=3)
        self.threshold = ctk.CTkEntry(self.param_frame)
        self.threshold.insert(0, "0.5")
        self.threshold.grid(row=4, column=1, padx=5, pady=3)


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

            # Kanal başlığı
            ch_label = ctk.CTkLabel(frame, text=f"Channel {c}", font=ctk.CTkFont(size=14))
            ch_label.pack(pady=(0, 5))

            # Görsel
            img_label = ctk.CTkLabel(frame, image=photo, text="")
            img_label.image = photo
            img_label.pack()

            menu_var = ctk.StringVar(value="Select")
            menu = ctk.CTkOptionMenu(frame, variable=menu_var, values=self.choices)
            menu.pack(pady=5)

            self.image_labels.append(img_label)
            self.option_menus.append(menu)
            self.selections.append(menu_var)
  
    def validate_and_proceed(self):
        selected = [s.get() for s in self.selections]
        if "Select" in selected:
            messagebox.showerror("Error", "Please select a type for each channel.")
            return
        self.controller.show_frame("ProcessingPage")