import tkinter as tk
from tkinter import ttk
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

        # Gamma Input
        tk.Label(input_frame, text="Gamma (γ):").grid(row=0, column=0, padx=5, pady=5)
        gamma_entry = tk.Entry(input_frame)
        gamma_entry.grid(row=0, column=1, padx=5, pady=5)

        # Input Type Dropdown
        tk.Label(input_frame, text="Select Input Type:").grid(row=1, column=0, padx=5, pady=5)
        input_type_var = tk.StringVar(value="Mach Number")  # Default value
        input_type_dropdown = ttk.OptionMenu(
            input_frame, input_type_var, "Mach Number",
            "Mach Number", "4fL*/D(subsonic)", "4fL*/D(supersonic)", 
            "p/p*", "p0/p0*(subsonic)", "p0/p0*(supersonic)", "rho/rho*", "T/T*"
        )
        input_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Input Value
        tk.Label(input_frame, text="Input Value:").grid(row=2, column=0, padx=5, pady=5)
        input_value_entry = tk.Entry(input_frame)
        input_value_entry.grid(row=2, column=1, padx=5, pady=5)

        # Result Output
        result_text = tk.Text(self, height=15, width=60)
        result_text.pack(pady=10)

        # Calculate Button
        def calculate():
            try:
                # Get input values
                gamma = float(gamma_entry.get())
                input_type = input_type_var.get()
                input_value = float(input_value_entry.get())

                # Perform calculation
                flow = FannoFlow(gamma)
                result = flow.calculate(input_type, input_value)

                # Display results
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Input Type: {input_type}\n")
                result_text.insert(tk.END, f"Input Value: {input_value}\n\n")
                result_text.insert(tk.END, "Calculated Properties:\n")
                result_text.insert(tk.END, f"  Mach Number (M): {result['M']:.4f}\n")
                result_text.insert(tk.END, f"  T/T*: {result['T/T*']:.4f}\n")
                result_text.insert(tk.END, f"  p/p*: {result['p/p*']:.4f}\n")
                result_text.insert(tk.END, f"  p0/p0*: {result['p0/p0*']:.4f}\n")
                result_text.insert(tk.END, f"  ρ/ρ*: {result['rho/rho*']:.4f}\n")
                result_text.insert(tk.END, f"  4fL*/D: {result['4fL*/D']:.4f}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)
