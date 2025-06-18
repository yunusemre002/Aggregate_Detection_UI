import customtkinter as ctk

class NapariPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title = ctk.CTkLabel(self, text="3D View Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.title.pack(pady=20)

        self.description = ctk.CTkLabel(
            self,
            text="Adjust the parameters below to visualize the 3D aggregates.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.description.pack(pady=5)

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=20)

        # Threshold Ratio
        threshold_label = ctk.CTkLabel(form_frame, text="Threshold Ratio (0-1):")
        threshold_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.threshold_entry = ctk.CTkEntry(form_frame, width=120)
        self.threshold_entry.insert(0, "0.6")
        self.threshold_entry.grid(row=0, column=1, padx=10, pady=10)

        # Min Size
        min_size_label = ctk.CTkLabel(form_frame, text="Minimum Size (voxels):")
        min_size_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.min_size_entry = ctk.CTkEntry(form_frame, width=120)
        self.min_size_entry.insert(0, "10")
        self.min_size_entry.grid(row=1, column=1, padx=10, pady=10)

        # Back button
        back_button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("ChannelInfoPage"))
        back_button.pack(pady=30)

    def get_settings(self):
        try:
            threshold = float(self.threshold_entry.get())
            min_size = int(self.min_size_entry.get())
            return threshold, min_size
        except ValueError:
            return None, None
