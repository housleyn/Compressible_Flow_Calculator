import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.fanno_flow import FannoFlow

class FannoFlowPage(tk.Frame):
    """Standalone page for Fanno Flow Calculations."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Fanno Flow Calculations", font=("Arial", 16)).pack(pady=20)

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

                flow = FannoFlow(gamma)
                result = flow.calculate(mach)

                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Mach Number: {mach}\n\n")
                result_text.insert(tk.END, f"Friction Factor (fL/D): {result.friction_factor}\n")
                result_text.insert(tk.END, f"Pressure Ratio (p/p*): {result.p_p_star}\n")
                result_text.insert(tk.END, f"Temperature Ratio (T/T*): {result.T_T_star}\n")
                result_text.insert(tk.END, f"Density Ratio (ρ/ρ*): {result.rho_rho_star}\n")
                result_text.insert(tk.END, f"Stagnation Pressure Ratio (p0/p0*): {result.p0_p0_star}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)
