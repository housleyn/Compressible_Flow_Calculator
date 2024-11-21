import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.rayleigh_flow import RayleighFlow


class RayleighFlowPage(tk.Frame):
    """Standalone page for Rayleigh Flow Calculations."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Rayleigh Flow Calculations", font=("Arial", 16)).pack(pady=20)

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
            "Mach Number", "p/p*", "T/T*", "T0/T0*(subsonic)", "T0/T0*(supersonic)", "p0/p0*(subsonic)", "p0/p0*(supersonic)"
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
                flow = RayleighFlow(gamma)
                if input_type == "Mach Number":
                    mach = input_value
                elif input_type == "p/p*":
                    mach = flow.calculate_mach_number_p_ps(input_value)
                elif input_type == "T/T*":
                    mach = flow.calculate_mach_from_T_Ts(input_value, solution_type='below T_max')
                elif input_type == "T0/T0*(subsonic)":
                    mach = flow.calculate_mach_from_T0_T0s(input_value, solution_type='subsonic')
                elif input_type == "T0/T0*(supersonic)":
                    mach = flow.calculate_mach_from_T0_T0s(input_value, solution_type='supersonic')
                elif input_type == "p0/p0*(subsonic)":
                    mach = flow.calculate_mach_number(input_value, solution_type='subsonic')
                elif input_type == "p0/p0*(supersonic)":
                    mach = flow.calculate_mach_number(input_value, solution_type='supersonic')
                else:
                    raise ValueError("Invalid input type selected.")

                # Compute all flow properties using Mach number
                p_p_star = flow.calculate_p_ps(mach)
                T_T_star = flow.calculate_T_Ts(mach)
                T0_T0_star = flow.calculate_T0_T0s(mach)
                p0_p0_star = flow.calculate_p0_p0s(mach)

                # Display results
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Input Type: {input_type}\n")
                result_text.insert(tk.END, f"Input Value: {input_value}\n\n")
                result_text.insert(tk.END, f"Calculated Mach Number: {mach:.4f}\n")
                result_text.insert(tk.END, f"p/p*: {p_p_star:.4f}\n")
                result_text.insert(tk.END, f"T/T*: {T_T_star:.4f}\n")
                result_text.insert(tk.END, f"T0/T0*: {T0_T0_star:.4f}\n")
                result_text.insert(tk.END, f"p0/p0*: {p0_p0_star:.4f}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)
