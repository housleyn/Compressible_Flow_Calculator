import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.normal_shocks import NormalShock



class NormalShockPage(tk.Frame):
    """Standalone page for Normal Shock Calculations."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Normal Shock Calculations", font=("Arial", 16)).pack(pady=20)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Gamma (γ):").grid(row=0, column=0, padx=5, pady=5)
        gamma_entry = tk.Entry(input_frame)
        gamma_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Mach Number (M):").grid(row=1, column=0, padx=5, pady=5)
        mach_entry = tk.Entry(input_frame)
        mach_entry.grid(row=1, column=1, padx=5, pady=5)

        result_text = tk.Text(self, height=10, width=50)
        result_text.pack(pady=10)

        def calculate():
            try:
                gamma = float(gamma_entry.get())
                mach = float(mach_entry.get())

                flow = NormalShock(gamma)
                result = flow.calculate(mach)

                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Mach Number: {mach}\n\n")
                result_text.insert(tk.END, f"Pressure Ratio (p2/p1): {result.p2_p1}\n")
                result_text.insert(tk.END, f"Density Ratio (rho2/rho1): {result.rho2_rho1}\n")
                result_text.insert(tk.END, f"Temperature Ratio (T2/T1): {result.T2_T1}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)


