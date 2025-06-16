import customtkinter as ctk
from tkinter import filedialog
import os

class FileSelectPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_file = ""

        label = ctk.CTkLabel(self, text="Select a .tif File", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        self.file_button = ctk.CTkButton(self, text="Choose File", command=self.select_file)
        self.file_button.pack(pady=10)

        self.next_button = ctk.CTkButton(self, text="NEXT", command=self.next_page, state="disabled")
        self.next_button.pack(pady=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("TIF files", "*.tif")])
        if file_path.endswith(".tif"):
            self.selected_file = file_path
            self.file_button.configure(text=os.path.basename(file_path))
            self.controller.tif_path = file_path
            self.next_button.configure(state="normal")

    def next_page(self):
        self.controller.show_frame("ChannelInfoPage")