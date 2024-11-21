import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.oblique_shocks import ObliqueShock


class ObliqueShockPage(tk.Frame):
    """Standalone page for Oblique Shock Calculations."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Oblique Shock Calculations", font=("Arial", 16)).pack(pady=20)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Gamma Input
        tk.Label(input_frame, text="Gamma (γ):").grid(row=0, column=0, padx=5, pady=5)
        gamma_entry = tk.Entry(input_frame)
        gamma_entry.grid(row=0, column=1, padx=5, pady=5)

        # Mach Number Input
        tk.Label(input_frame, text="Mach Number (M):").grid(row=1, column=0, padx=5, pady=5)
        mach_entry = tk.Entry(input_frame)
        mach_entry.grid(row=1, column=1, padx=5, pady=5)

        # Third Input Type Selection
        tk.Label(input_frame, text="Select Input Type:").grid(row=2, column=0, padx=5, pady=5)
        input_type_var = tk.StringVar(value="Turn angle (weak shock)")  # Default value
        input_type_dropdown = ttk.OptionMenu(
            input_frame, input_type_var, "Turn angle (weak shock)", 
            "Turn angle (weak shock)", "Turn angle (strong shock)", "Wave angle", "M1n"
        )
        input_type_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Third Input Value
        tk.Label(input_frame, text="Input Value:").grid(row=3, column=0, padx=5, pady=5)
        input_value_entry = tk.Entry(input_frame)
        input_value_entry.grid(row=3, column=1, padx=5, pady=5)

        # Result Output
        result_text = tk.Text(self, height=15, width=60)
        result_text.pack(pady=10)

        # Calculate Button
        def calculate():
            try:
                # Get input values
                gamma = float(gamma_entry.get())
                mach = float(mach_entry.get())
                input_type = input_type_var.get()
                input_value = float(input_value_entry.get())

                # Perform calculation
                shock = ObliqueShock(gamma)
                result = shock.calculate(input_type, mach, input_value)

                # Display results
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Mach Number: {mach}\n")
                result_text.insert(tk.END, f"Input Type: {input_type}\n")
                result_text.insert(tk.END, f"Input Value: {input_value}\n\n")
                result_text.insert(tk.END, "Calculated Properties:\n")
                result_text.insert(tk.END, f"  Wave Angle (β): {result['Wave Angle']:.4f}°\n")
                result_text.insert(tk.END, f"  Turn Angle (δ): {result['Turn Angle']:.4f}°\n")
                result_text.insert(tk.END, f"  M1n: {result['M1n']:.4f}\n")
                result_text.insert(tk.END, f"  M2n: {result['M2n']:.4f}\n")
                result_text.insert(tk.END, f"  M2: {result['M2']:.4f}\n")
                result_text.insert(tk.END, f"  p2/p1: {result['p2/p1']:.4f}\n")
                result_text.insert(tk.END, f"  p02/p01: {result['p02/p01']:.4f}\n")
                result_text.insert(tk.END, f"  rho2/rho1: {result['rho2/rho1']:.4f}\n")
                result_text.insert(tk.END, f"  T2/T1: {result['T2/T1']:.4f}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)
