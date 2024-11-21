import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.isentropic_flow import isentropicFlow

class IsentropicFlowPage(tk.Frame):
    """Standalone page for Isentropic Flow Calculations."""
    
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Isentropic Flow Calculations", font=("Arial", 16)).pack(pady=20)

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
                                           "T/T0", "p/p0", "rho/rho0", "A/A*(subsonic)", "A/A*(supersonic)",
                                           "Mach Angle(deg.)", "PM Angle(deg.)", "Mach Number")
        calc_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Input Value
        tk.Label(input_frame, text="Input Value:").grid(row=2, column=0, padx=5, pady=5)
        value_entry = tk.Entry(input_frame)
        value_entry.grid(row=2, column=1, padx=5, pady=5)

        # Output Area
        result_text = tk.Text(self, height=10, width=50)
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
                flow = isentropicFlow(gamma)
                result = flow.calculate(calc_type, value)

                # Display the results
                result_text.delete(1.0, tk.END)  # Clear previous results
                result_text.insert(tk.END, f"Gamma (γ): {gamma}\n")
                result_text.insert(tk.END, f"Calculation Type: {calc_type}\n")
                result_text.insert(tk.END, f"Input Value: {value}\n\n")
                result_text.insert(tk.END, f"Mach Number: {result.mach_number}\n")
                result_text.insert(tk.END, f"Mach Angle: {result.mach_angle}\n")
                result_text.insert(tk.END, f"PM Angle: {result.pm_angle}\n")
                result_text.insert(tk.END, f"T/T0: {result.t_t0}\n")
                result_text.insert(tk.END, f"p/p0: {result.p_p0}\n")
                result_text.insert(tk.END, f"rho/rho0: {result.rho_rho0}\n")
                result_text.insert(tk.END, f"T/Ts: {result.t_ts}\n")
                result_text.insert(tk.END, f"p/ps: {result.p_ps}\n")
                result_text.insert(tk.END, f"rho/rhos: {result.rho_rhos}\n")
                result_text.insert(tk.END, f"A/A*: {result.a_as}\n")
            except ValueError as e:
                result_text.delete(1.0, tk.END)  # Clear previous results
                result_text.insert(tk.END, f"Error: {str(e)}\n")

        # Add Calculate Button
        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)
