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
        input_type_var = tk.StringVar(value="Turn angle (weak)")  # Default value
        input_type_dropdown = ttk.OptionMenu(
            input_frame, input_type_var, "Turn angle (weak)", 
            "Turn angle (weak)", "Turn angle (strong)", "Wave angle", "M1n"
        )
        input_type_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Third Input Value
        tk.Label(input_frame, text="Input Value:").grid(row=3, column=0, padx=5, pady=5)
        input_value_entry = tk.Entry(input_frame)
        input_value_entry.grid(row=3, column=1, padx=5, pady=5)

        # Result Output
        result_text = tk.Text(self, height=10, width=50)
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
                flow = ObliqueShock(gamma)

                if input_type == "Turn angle (weak)":
                    result = flow.calculate_turn_angle_weak(mach, input_value)
                elif input_type == "Turn angle (strong)":
                    result = flow.calculate_turn_angle_strong(mach, input_value)
                elif input_type == "Wave angle":
                    result = flow.calculate_wave_angle(mach, input_value)
                elif input_type == "M1n":
                    result = flow.calculate_m1n(mach, input_value)
                else:
                    raise ValueError("Invalid input type selected.")

                # Display results
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Mach Number: {mach}\n")
                result_text.insert(tk.END, f"Input Type: {input_type}\n")
                result_text.insert(tk.END, f"Input Value: {input_value}\n\n")
                result_text.insert(tk.END, f"Pressure Ratio (p2/p1): {result.p2_p1}\n")
                result_text.insert(tk.END, f"Density Ratio (rho2/rho1): {result.rho2_rho1}\n")
                result_text.insert(tk.END, f"Temperature Ratio (T2/T1): {result.T2_T1}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)
