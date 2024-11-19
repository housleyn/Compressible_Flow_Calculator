import tkinter as tk
from tkinter import ttk
import sys
import os
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.oblique_shocks import ObliqueShock


class ObliqueShocksPage(tk.Frame):
    """Page for oblique shocks calculations."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Oblique Shocks Calculations", font=("Arial", 16)).pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Gamma Input
        tk.Label(input_frame, text="Gamma:").grid(row=0, column=0, padx=5, pady=5)
        gamma_entry = tk.Entry(input_frame)
        gamma_entry.insert(0, "1.4")  # Default value
        gamma_entry.grid(row=0, column=1, padx=5, pady=5)

        # Mach Number Input
        tk.Label(input_frame, text="Mach Number 1:").grid(row=1, column=0, padx=5, pady=5)
        mach_entry = tk.Entry(input_frame)
        mach_entry.grid(row=1, column=1, padx=5, pady=5)

        # Angle Input with Unit Dropdown
        
        input_frame_angle = tk.Frame(input_frame)
        input_frame_angle.grid(row=2, column=1, padx=5, pady=5)

        # Calculation Type Dropdown
        calc_type_var = tk.StringVar(value="Turn angle (weak shock)")
        calc_type_dropdown = ttk.Combobox(input_frame, textvariable=calc_type_var, state="readonly")
        calc_type_dropdown['values'] = [
            "Turn angle (weak shock)",
            "Turn angle (strong shock)",
            "Wave angle",
            "M1n"
        ]
        calc_type_dropdown.grid(row=2, column=0, padx=5, pady=5)
        angle_entry = tk.Entry(input_frame_angle)  # Entry field for the angle value
        angle_entry.pack(side=tk.LEFT, padx=5)

        # Output
        output_frame = tk.Frame(self)
        output_frame.pack(pady=10)
        output_var = tk.StringVar(value="Results will be displayed here")
        output_label = tk.Label(output_frame, textvariable=output_var, fg="blue", font=("Arial", 12), wraplength=400, justify="left")
        output_label.pack()

        # Calculate Button
        def calculate():
            try:
                gamma = float(gamma_entry.get())
                mach = float(mach_entry.get())
                angle = float(angle_entry.get())
                calc_type = calc_type_var.get()


                # Perform calculation
                shock = ObliqueShock(gamma)
                results = shock.calculate(calc_type, mach, angle)

                # Format and display results
                result_text = "\n".join([f"{key}: {value}" for key, value in results.items()])
                output_var.set(result_text)
            except ValueError as e:
                output_var.set(f"Error: {str(e)}")
            except Exception as e:
                output_var.set(f"Unexpected error: {str(e)}")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)

        # Back to Home Button
        tk.Button(self, text="Back to Home",
                  command=lambda: controller.show_frame("HomePage")).pack(pady=20)
