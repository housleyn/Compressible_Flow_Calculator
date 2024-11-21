import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.rayleigh_flow import RayleighFlow

class RayleighFlowPage(tk.Frame):
    """Page for Rayleigh flow calculations."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Rayleigh Flow Calculations", font=("Arial", 16)).pack(pady=20)

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
                                           "Mach Number",
                                           "T0/T0*(subsonic)", "T0/T0*(supersonic)",
                                           "T/T* (below T_max)", "T/T* (above T_max)",
                                           "p/p*", "p0/p0*(subsonic)", "p0/p0*(supersonic)")
        calc_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Input Value
        tk.Label(input_frame, text="Input Value:").grid(row=2, column=0, padx=5, pady=5)
        value_entry = tk.Entry(input_frame)
        value_entry.grid(row=2, column=1, padx=5, pady=5)

        # Output Area
        result_text = tk.Text(self, height=15, width=60)
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

                # Initialize RayleighFlow class
                flow = RayleighFlow(gamma)

                # Perform calculations
                if calc_type == "Mach Number":
                    M = value
                elif calc_type == "T0/T0*(subsonic)":
                    M = flow.calculate_mach_from_T0_T0s(value, solution_type="subsonic")
                elif calc_type == "T0/T0*(supersonic)":
                    M = flow.calculate_mach_from_T0_T0s(value, solution_type="supersonic")
                elif calc_type == "T/T* (below T_max)":
                    M = flow.calculate_mach_from_T_Ts(value, solution_type="below T_max")
                elif calc_type == "T/T* (above T_max)":
                    M = flow.calculate_mach_from_T_Ts(value, solution_type="above T_max")
                elif calc_type == "p/p*":
                    M = flow.calculate_mach_number_p_ps(value)  
                elif calc_type == "p0/p0*(subsonic)":
                    M = flow.calculate_mach_number(value, solution_type="subsonic")
                elif calc_type == "p0/p0*(supersonic)":
                    M = flow.calculate_mach_number(value, solution_type="supersonic")
                else:
                    raise ValueError("Invalid calculation type selected")

                # Calculate all properties based on Mach number
                p_ps = flow.calculate_p_ps(M)
                T_Ts = flow.calculate_T_Ts(M)
                T0_T0s = flow.calculate_T0_T0s(M)
                p0_p0s = flow.calculate_p0_p0s(M)

                # Display the results
                result_text.delete(1.0, tk.END)  # Clear previous results
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Calculation Type: {calc_type}\n")
                result_text.insert(tk.END, f"Input Value: {value}\n\n")
                result_text.insert(tk.END, f"Mach Number: {M:.6f}\n")
                result_text.insert(tk.END, f"p/ps: {p_ps:.6f}\n")
                result_text.insert(tk.END, f"T/Ts: {T_Ts:.6f}\n")
                result_text.insert(tk.END, f"T0/T0s: {T0_T0s:.6f}\n")
                result_text.insert(tk.END, f"p0/p0s: {p0_p0s:.6f}\n")

            except ValueError as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        # Add Calculate Button
        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)

        # Back to Home Button
        tk.Button(self, text="Back to Home",
                  command=lambda: controller.show_frame("HomePage")).pack(pady=20)
