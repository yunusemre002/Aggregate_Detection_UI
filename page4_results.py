import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class ResultsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Analysis Results", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="3D View", command=self.dummy).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Download PDF", command=self.dummy).grid(row=0, column=1, padx=10)
        ctk.CTkButton(button_frame, text="Download CSV", command=self.dummy).grid(row=0, column=2, padx=10)

        # Matplotlib plot example
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.imshow(np.random.rand(100, 100), cmap="gray")
        ax.set_title("Detected Aggregates")

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def dummy(self):
        print("Action triggered")