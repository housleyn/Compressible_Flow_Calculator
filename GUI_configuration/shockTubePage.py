import tkinter as tk

class ShockTubesPage(tk.Frame):
    """Page for shock tubes calculations."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Shock Tubes Calculations", font=("Arial", 16)).pack(pady=20)

        # Back to Home Button
        tk.Button(self, text="Back to Home",
                  command=lambda: controller.show_frame("HomePage")).pack(pady=20)
