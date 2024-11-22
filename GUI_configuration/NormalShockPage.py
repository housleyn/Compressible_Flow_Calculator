import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.normal_shocks import NormalShock


class NormalShockPage(tk.Frame):
    """Improved standalone page for Normal Shock Calculations with Table Results."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Normal Shock Calculations", font=("Arial", 18, "bold")).pack(pady=15)

        # Input Section
        input_frame = tk.LabelFrame(self, text="Inputs", font=("Arial", 14, "bold"), bd=2, relief="solid", padx=10, pady=10, bg="#f9f9f9")
        input_frame.pack(padx=20, pady=10, fill="x")

        # Gamma Input
        tk.Label(input_frame, text="Gamma (γ):", font=("Arial", 12), bg="#f9f9f9").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        gamma_entry = ttk.Entry(input_frame, font=("Arial", 12))
        gamma_entry.grid(row=0, column=1, padx=5, pady=5)

        # Calculation Type Dropdown
        tk.Label(input_frame, text="Calculation Type:", font=("Arial", 12), bg="#f9f9f9").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        calc_type_var = tk.StringVar(value="Select Calculation Type")
        calc_type_dropdown = ttk.Combobox(
            input_frame, textvariable=calc_type_var, font=("Arial", 12), state="readonly",
            values=[
                "M1", "M2", "p02/p01", "p1/p02", "p2/p1", "rho2/rho1", "T2/T1"
            ]
        )
        calc_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Input Value
        tk.Label(input_frame, text="Input Value:", font=("Arial", 12), bg="#f9f9f9").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        value_entry = ttk.Entry(input_frame, font=("Arial", 12))
        value_entry.grid(row=2, column=1, padx=5, pady=5)

        # Calculate Button
        calculate_button = ttk.Button(input_frame, text="Calculate", command=lambda: self.calculate(gamma_entry, calc_type_var, value_entry))
        calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Error Display
        self.error_label = tk.Label(self, text="", font=("Arial", 12, "bold"), fg="red")
        self.error_label.pack()

        # Result Section
        result_frame = tk.LabelFrame(self, text="Results", font=("Arial", 14, "bold"), bd=2, relief="solid", padx=10, pady=10, bg="#f9f9f9")
        result_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Table for Results
        columns = ("Property", "Value")
        result_table = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)
        result_table.pack(padx=5, pady=5, fill="both", expand=True)

        # Configure Columns
        result_table.heading("Property", text="Property")
        result_table.heading("Value", text="Value")
        result_table.column("Property", anchor="center", width=200)
        result_table.column("Value", anchor="center", width=200)

        # Apply alternating row colors
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#d9d9d9", relief="solid")
        style.map("Treeview", background=[("selected", "#fffbcc")], foreground=[("selected", "black")], font=[("selected", ("Arial", 12, "bold"))])
        style.configure("TButton", font=("Arial", 12), padding=5)

        # Enable copying to clipboard
        result_table.bind("<Double-1>", self.copy_to_clipboard)

        # Save result_table for later use
        self.result_table = result_table

        # Copy Notification Label
        self.copy_label = tk.Label(self, text="", font=("Arial", 10), fg="green")
        self.copy_label.pack(pady=5)

        # Copy Button
        copy_button = ttk.Button(self, text="Copy Selected Value", command=self.copy_to_clipboard)
        copy_button.pack(pady=5)

    def calculate(self, gamma_entry, calc_type_var, value_entry):
        """Perform the calculation and display results in a table."""
        try:
            gamma = float(gamma_entry.get())
            if gamma <= 1.0:
                raise ValueError("Gamma (γ) must be greater than 1")

            calc_type = calc_type_var.get()
            if calc_type == "Select Calculation Type":
                raise ValueError("Please select a valid calculation type.")

            value = float(value_entry.get())

            # Perform the calculation
            shock = NormalShock(gamma)
            result = shock.calculate(calc_type, value)

            # Clear previous results
            for row in self.result_table.get_children():
                self.result_table.delete(row)

            # Clear error message
            self.error_label.config(text="")

            # Insert results into the table
            row_tags = ["odd", "even"]
            for index, (property, val) in enumerate([
                ("M1", round(result.mach_number1, 4)),
                ("M2", round(result.mach_number2, 4)),
                ("p2/p1", round(result.p2p1, 4)),
                ("p02/p01", round(result.p02p01, 4)),
                ("rho2/rho1", round(result.r2r1, 4)),
                ("T2/T1", round(result.t2t1, 4)),
                ("p1/p02", round(result.p1p02, 4)),
            ]):
                self.result_table.insert("", "end", values=(property, val), tags=(row_tags[index % 2],))

            # Configure alternating row colors
            self.result_table.tag_configure("odd", background="white")
            self.result_table.tag_configure("even", background="#f2f2f2")

        except ValueError as e:
            # Display error message
            self.error_label.config(text=str(e))
            for row in self.result_table.get_children():
                self.result_table.delete(row)

    def copy_to_clipboard(self, event=None):
        """Copy selected table value to the clipboard and show confirmation."""
        selected_item = self.result_table.selection()  # Get selected row
        if selected_item:
            selected_values = self.result_table.item(selected_item, "values")  # Get row values
            if len(selected_values) > 1:
                value_to_copy = selected_values[1]  # Copy the 'Value' column
                self.clipboard_clear()
                self.clipboard_append(value_to_copy)
                self.update()  # Ensures clipboard is updated
                
                # Show confirmation message
                self.copy_label.config(text="Value copied!")
                self.after(1500, lambda: self.copy_label.config(text=""))
