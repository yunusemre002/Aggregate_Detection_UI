# import customtkinter as ctk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import numpy as np

# class ResultsPage(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)

#         label = ctk.CTkLabel(self, text="Analysis Results", font=ctk.CTkFont(size=20, weight="bold"))
#         label.pack(pady=20)

#         button_frame = ctk.CTkFrame(self)
#         button_frame.pack(pady=10)

#         ctk.CTkButton(button_frame, text="3D View", command=self.dummy).grid(row=0, column=0, padx=10)
#         ctk.CTkButton(button_frame, text="Download PDF", command=self.dummy).grid(row=0, column=1, padx=10)
#         ctk.CTkButton(button_frame, text="Download CSV", command=self.dummy).grid(row=0, column=2, padx=10)

#         # Matplotlib plot example
#         fig, ax = plt.subplots(figsize=(5, 4))
#         ax.imshow(np.random.rand(100, 100), cmap="gray")
#         ax.set_title("Detected Aggregates")

#         canvas = FigureCanvasTkAgg(fig, master=self)
#         canvas.draw()
#         canvas.get_tk_widget().pack(pady=10)

#     def dummy(self):
#         print("Action triggered")

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import napari
from skimage.measure import regionprops

class ResultsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Analysis Results", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        # Butonlar
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="3D View", command=self.show_napari).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Download PDF", command=self.download_pdf).grid(row=0, column=1, padx=10)
        ctk.CTkButton(button_frame, text="Download CSV", command=self.download_csv).grid(row=0, column=2, padx=10)

        # Placeholder görüntü
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.set_title("Detected Aggregates")

        # Eğer veri varsa göster
        try:
            img = self.controller.results["labeled_aggregates"]
            ax.imshow(img[0], cmap="gray")
        except:
            ax.text(0.5, 0.5, "No data", ha='center', va='center')

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def show_napari(self):
        results = self.controller.results
        img_cellbody = results["img_cellbody"]
        img_nuclei = results["img_nuclei"]
        labeled = results["labeled_aggregates"]

        regions = regionprops(labeled)
        points = []
        labels = []
        for region in regions:
            z, y, x = region.centroid
            points.append([z, y, x])
            labels.append(str(region.label))
        points = np.array(points)

        viewer = napari.Viewer(ndisplay=3)
        viewer.add_image(img_nuclei, name="Nucleus", colormap="blue", scale=(1,1,1))
        viewer.add_image(img_cellbody, name="Cell Body", colormap="gray", blending="additive", scale=(1,1,1))
        viewer.add_labels(labeled, name="Aggregates", opacity=0.9, scale=(1,1,1))
        viewer.add_points(points, name="Aggregate IDs", size=3, face_color="red", text=labels, scale=(1,1,1))

        napari.run()

    def download_pdf(self):
        print("PDF export coming soon...")

    def download_csv(self):
        print("CSV export coming soon...")
