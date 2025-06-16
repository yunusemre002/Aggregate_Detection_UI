import customtkinter as ctk
import threading
import time

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