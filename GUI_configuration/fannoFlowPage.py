import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.fanno_flow import FannoFlow

class FannoFlowPage(tk.Frame):
    """Page for Fanno Flow calculations."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Fanno Flow Calculations", font=("Arial", 16)).pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Gamma Input
        tk.Label(input_frame, text="Gamma (γ):").grid(row=0, column=0, padx=5, pady=5)
        gamma_entry = tk.Entry(input_frame)
        gamma_entry.grid(row=0, column=1, padx=5, pady=5)

        # Calculation Type Dropdown
        tk.Label(input_frame, text="Calculation Type:").grid(row=1, column=0, padx=5, pady=5)
        calc_type_var = tk.StringVar()
        calc_type_dropdown = tk.OptionMenu(input_frame, calc_type_var,
                                           "4fL*/D(subsonic)", "4fL*/D(supersonic)", "T/T*", "p/p*", "rho/rho*", "p0/p0*(subsonic)", "p0/p0*(supersonic)", "Mach Number")
        calc_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Input Value
        tk.Label(input_frame, text="Input Value:").grid(row=2, column=0, padx=5, pady=5)
        value_entry = tk.Entry(input_frame)
        value_entry.grid(row=2, column=1, padx=5, pady=5)

        # Output Area
        result_text = tk.Text(self, height=12, width=60)
        result_text.pack(pady=10)

        # Calculate Button
        def calculate():
            try:
                # Get gamma and validate
                gamma = float(gamma_entry.get())
                if gamma <= 1.0:
                    raise ValueError("Gamma (γ) must be greater than 1")

                # Get calculation type and input value
                calc_type = calc_type_var.get()
                value = float(value_entry.get())

                # Perform the calculation
                fanno = FannoFlow(gamma)
                result = fanno.calculate(calc_type, value)

                # Display the results
                result_text.delete(1.0, tk.END)  # Clear previous results
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Calculation Type: {calc_type}\n")
                result_text.insert(tk.END, f"Input Value: {value}\n\n")
                result_text.insert(tk.END, f"Mach Number (M): {result['M']}\n")
                result_text.insert(tk.END, f"T/T*: {result['T/T*']}\n")
                result_text.insert(tk.END, f"p/p*: {result['p/p*']}\n")
                result_text.insert(tk.END, f"p0/p0*: {result['p0/p0*']}\n")
                result_text.insert(tk.END, f"rho/rho*: {result['rho/rho*']}\n")
                result_text.insert(tk.END, f"4fL*/D: {result['4fL*/D']}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)  # Clear previous results
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        # Add Calculate Button
        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)

        # Back to Home Button
        tk.Button(self, text="Back to Home",
                  command=lambda: controller.show_frame("HomePage")).pack(pady=20)
