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

        # Gamma input
        tk.Label(input_frame, text="Gamma (γ):").grid(row=0, column=0, padx=5, pady=5)
        gamma_entry = tk.Entry(input_frame)
        gamma_entry.grid(row=0, column=1, padx=5, pady=5)

        # Dropdown for calculation type
        tk.Label(input_frame, text="Calculation Type:").grid(row=1, column=0, padx=5, pady=5)
        calc_type_var = tk.StringVar(value="M1")
        calc_type_dropdown = tk.OptionMenu(
            input_frame, calc_type_var,
            "M1", "M2", "p02/p01", "p1/p02", "p2/p1", "rho2/rho1", "T2/T1"
        )
        calc_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Input value field
        tk.Label(input_frame, text="Input Value:").grid(row=2, column=0, padx=5, pady=5)
        value_entry = tk.Entry(input_frame)
        value_entry.grid(row=2, column=1, padx=5, pady=5)

        # Result text box
        result_text = tk.Text(self, height=20, width=60)
        result_text.pack(pady=10)

        def calculate():
            try:
                # Get inputs
                gamma = float(gamma_entry.get())
                calc_type = calc_type_var.get()
                input_value = float(value_entry.get())

                # Perform calculation
                shock = NormalShock(gamma)
                result = shock.calculate(calc_type, input_value)

                # Display all calculated results
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Input Type: {calc_type}\n")
                result_text.insert(tk.END, f"Input Value: {input_value}\n\n")
                result_text.insert(tk.END, "Calculated Properties:\n")
                result_text.insert(tk.END, f"  M1: {result.mach_number1:.4f}\n")
                result_text.insert(tk.END, f"  M2: {result.mach_number2:.4f}\n")
                result_text.insert(tk.END, f"  p2/p1: {result.p2p1:.4f}\n")
                result_text.insert(tk.END, f"  p02/p01: {result.p02p01:.4f}\n")
                result_text.insert(tk.END, f"  rho2/rho1: {result.r2r1:.4f}\n")
                result_text.insert(tk.END, f"  T2/T1: {result.t2t1:.4f}\n")
                result_text.insert(tk.END, f"  p1/p02: {result.p1p02:.4f}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        # Calculate button
        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)
