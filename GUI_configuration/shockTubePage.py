import tkinter as tk
from tkinter import ttk
import sys
import os
from tabulate import tabulate
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.shock_tube import ShockTube

class ShockTubePage(tk.Frame):
    """Page for Shock Tube calculations."""
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Shock Tube Calculations", font=("Arial", 16)).pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Input Fields
        inputs = [
            ("Gamma (Region 1)", ""),  # Default value for gamma1
            ("Gamma (Region 4)", ""),  # Default value for gamma4
            ("Gas Constant R (Region 1)", ""),  # Default value for R1
            ("Gas Constant R (Region 4)", ""),  # Default value for R4
            ("Driven Temperature (T1)", ""),  # Default value for T1
            ("Driver Temperature (T4)", ""),  # Default value for T4
            ("Driven Gage Pressure (p1gage)", ""),  # Default value for p1gage
            ("Driver Gage Pressure (p4gage)", ""),  # Default value for p4gage
            ("Atmospheric Pressure (patm)", ""),  # Default value for patm
        ]

        self.entries = {}
        for i, (label_text, default) in enumerate(inputs):
            tk.Label(input_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(input_frame)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label_text] = entry

        # Output Frame
        output_frame = tk.Frame(self)
        output_frame.pack(pady=20)
        self.output_var = tk.StringVar(value="Results will be displayed here.")
        output_label = tk.Label(output_frame, textvariable=self.output_var, font=("Arial", 12), fg="blue", wraplength=600, justify="left")
        output_label.pack()

        # Calculate Button
        def calculate():
            try:
                # Retrieve inputs
                gamma1 = float(self.entries["Gamma (Region 1)"].get())
                gamma4 = float(self.entries["Gamma (Region 4)"].get())
                R1 = float(self.entries["Gas Constant R (Region 1)"].get())
                R4 = float(self.entries["Gas Constant R (Region 4)"].get())
                T1 = float(self.entries["Driven Temperature (T1)"].get())
                T4 = float(self.entries["Driver Temperature (T4)"].get())
                p1gage = float(self.entries["Driven Gage Pressure (p1gage)"].get())
                p4gage = float(self.entries["Driver Gage Pressure (p4gage)"].get())
                patm = float(self.entries["Atmospheric Pressure (patm)"].get())

                # Perform calculations
                shock_tube = ShockTube(gamma1, gamma4, R1, R4, T1, T4, p1gage, p4gage, patm)
                results = shock_tube.run_calculations()

                
                formatted_table = format_results_as_table(results)
                self.output_var.set(formatted_table)

                
            except Exception as e:
                self.output_var.set(f"Error: {e}")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)

        # Back to Home Button
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack(pady=10)


def format_results_as_table(results):
    # Zone properties table
    zone_headers = ["Zone", "T (K)", "P (Pa)", "Rho (kg/m³)", "V (m/s)"]
    zone_data = [
        ["1", f"{results['T1']:.2f}", f"{results['p1']:.2f}", f"{results['rho1']:.2f}", f"{results['v1']:.2f}"],
        ["2", f"{results['T2']:.2f}", f"{results['p2']:.2f}", f"{results['rho2']:.2f}", f"{results['v2']:.2f}"],
        ["3", f"{results['T3']:.2f}", f"{results['p3']:.2f}", f"{results['rho3']:.2f}", f"{results['v3']:.2f}"],
        ["4", f"{results['T4']:.2f}", f"{results['p4']:.2f}", f"{results['rho4']:.2f}", f"{results['v4']:.2f}"],
        ["5", f"{results['T5']:.2f}", f"{results['p5']:.2f}", f"{results['rho5']:.2f}", f"{results['v5']:.2f}"],
    ]
    zone_table = tabulate(zone_data, headers=zone_headers, tablefmt="grid")

    # Key properties table
    key_headers = ["Property", "Value"]
    key_data = [
        ["Incident Shock Speed (Si)", f"{results['Si']:.2f} m/s"],
        ["Reflected Shock Speed (Sr)", f"{results['Sr']:.2f} m/s"],
        ["Incident Mach Number (Mi)", f"{results['Mi']:.2f}"],
        ["Reflected Mach Number (Mr)", f"{results['Mr']:.2f}"],
        ["Control Surface Velocity (Vel_CS)", f"{results['v_CS']:.2f} m/s"],
        ["Expansion Wave Velocity (Vel_EW)", f"{results['v_EW']:.2f} m/s"],
    ]
    key_table = tabulate(key_data, headers=key_headers, tablefmt="grid")

    # Combine both tables
    formatted_output = f"Zone Properties:\n{zone_table}\n\nKey Properties:\n{key_table}"
    return formatted_output
