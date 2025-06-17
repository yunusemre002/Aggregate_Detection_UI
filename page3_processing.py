import customtkinter as ctk
import threading
import time
from skimage import morphology
from skimage.measure import label
import numpy as np
import tifffile



class ProcessingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="AI-based detection in progress...", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="Initializing...", text_color="gray")
        self.status.pack(pady=10)

        self.spinner = ctk.CTkProgressBar(self, mode="indeterminate")
        self.spinner.pack(pady=10, fill="x", padx=100)
        self.spinner.start()

    def tkraise(self):
        super().tkraise()
        threading.Thread(target=self.process).start()

    def process(self):
        steps = ["Detecting Cell Bodies", "Detecting Nuclei", "Detecting Aggregates"]
        for step in steps:
            self.status.configure(text=step, text_color="orange")
            time.sleep(2)
            self.status.configure(text=f"{step} - Done", text_color="green")
        time.sleep(1)
        self.controller.show_frame("ResultsPage")
    

    def process(self):
        try:
            self.status.configure(text="Fetching parameters...", text_color="orange")

            # img ve kullanıcı seçimleri
            img = tifffile.imread(self.controller.tif_path)
            selections = self.controller.frames["ChannelInfoPage"].selections
            roles = [s.get() for s in selections]

            # Hangi kanal hangi görevde?
            cell_idx = roles.index("Cell body")
            nuc_idx = roles.index("Nuclei")
            agg_idx = roles.index("Aggregate")

            # Parametreler
            cell_diam = float(self.controller.frames["ChannelInfoPage"].cell_diam.get())
            nuc_diam = float(self.controller.frames["ChannelInfoPage"].nuclei_diam.get())
            agg_thresh = float(self.controller.frames["ChannelInfoPage"].threshold.get())

            # Cell body tespiti (placeholder)
            self.status.configure(text="Detecting Cell Bodies...", text_color="orange")
            img_cellbody = img[:, cell_idx]
            time.sleep(1)

            # Nuclei tespiti (placeholder)
            self.status.configure(text="Detecting Nuclei...", text_color="orange")
            img_nuclei = img[:, nuc_idx]
            time.sleep(1)

            def process_aggregates(img, channel_index, threshold_ratio=0.6):
                aggregate_masks = []
                for z_slice in range(img.shape[0]):
                    slice_img = img[z_slice, channel_index, :, :]
                    threshold = threshold_ratio * np.max(slice_img)
                    bright_spots = slice_img > threshold
                    clean_mask = morphology.remove_small_objects(bright_spots, min_size=10)
                    aggregate_masks.append(clean_mask)
                return np.stack(aggregate_masks, axis=0)
            

            # Aggregate tespiti
            self.status.configure(text="Detecting Aggregates...", text_color="orange")
            aggregate_stack = process_aggregates(img, agg_idx, agg_thresh)
            labeled_aggregates, _ = label(aggregate_stack, return_num=True)
            time.sleep(1)

            # Sonuçları kaydet
            self.controller.results = {
                "img_cellbody": img_cellbody,
                "img_nuclei": img_nuclei,
                "labeled_aggregates": labeled_aggregates
            }

            self.status.configure(text="Done!", text_color="green")
            time.sleep(1)
            self.controller.show_frame("ResultsPage")

        except Exception as e:
            self.status.configure(text=f"Error: {str(e)}", text_color="red")

