import tkinter as tk

class HomePage(tk.Frame):
    """Home page with navigation buttons."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Compressible Flow Calculator", font=("Arial", 18)).pack(pady=20)

        # Navigation Buttons
        tk.Button(self, text="Isentropic Flow Calculations",
                  command=lambda: controller.show_frame("IsentropicFlowPage")).pack(pady=10)
        tk.Button(self, text="Normal Shock Calculations",
                  command=lambda: controller.show_frame("NormalShockPage")).pack(pady=10)
        tk.Button(self, text="Oblique Shocks Calculations",
                  command=lambda: controller.show_frame("ObliqueShocksPage")).pack(pady=10)
        tk.Button(self, text="Fanno Flow Calculations",
                  command=lambda: controller.show_frame("FannoFlowPage")).pack(pady=10)
        tk.Button(self, text="Rayleigh Flow Calculations",
                  command=lambda: controller.show_frame("RayleighFlowPage")).pack(pady=10)
        tk.Button(self, text="Shock Tubes Calculations",
                  command=lambda: controller.show_frame("ShockTubePage")).pack(pady=10)
        tk.Button(self, text="Normal Shock Locations",
                  command=lambda: controller.show_frame("NormalShockLocationsPage")).pack(pady=10)
