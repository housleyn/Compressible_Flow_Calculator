import tkinter as tk

class NormalShockLocationsPage(tk.Frame):
    """Page for normal shock locations calculations."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Normal Shock Locations Calculations", font=("Arial", 16)).pack(pady=20)

        # Back to Home Button
        tk.Button(self, text="Back to Home",
                  command=lambda: controller.show_frame("HomePage")).pack(pady=20)
