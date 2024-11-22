import tkinter as tk
from tkinter import ttk
import sys
import os
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.shock_tube import ShockTube


class ShockTubePage(tk.Frame):
    """Page for Shock Tube calculations."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        # Scrollable Frame for the entire page
        outer_frame = tk.Frame(self)
        outer_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer_frame)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
         # Bind mouse wheel events for this canvas only
        self.bind_mouse_wheel(canvas)


        # Title
        tk.Label(scrollable_frame, text="Shock Tube Calculations", font=("Arial", 16, "bold")).pack(pady=10)

        # Input Section
        input_frame = tk.LabelFrame(scrollable_frame, text="Inputs", font=("Arial", 14, "bold"), padx=10, pady=10)
        input_frame.pack(padx=100, pady=10, fill="x")

        # Input Fields with Units
        inputs = [
            ("Gamma (Region 1)", "1.4", ""),
            ("Gamma (Region 4)", "1.4", ""),
            ("Gas Constant R (Region 1)", "287", "J/(kg·K)"),
            ("Gas Constant R (Region 4)", "287", "J/(kg·K)"),
            ("Driven Temperature (T1)", "289.6", "K"),
            ("Driver Temperature (T4)", "295.8", "K"),
            ("Driven Gage Pressure (p1gage)", "-80503.21", "Pa"),
            ("Driver Gage Pressure (p4gage)", "191726.18", "Pa"),
            ("Atmospheric Pressure (patm)", "86386.78", "Pa"),
            ("Driver Length", "3.1", "m"),
            ("Driven Length", "11.67", "m"),
        ]
        self.entries = {}
        for i, (label_text, default, unit) in enumerate(inputs):
            tk.Label(input_frame, text=label_text, font=("Arial", 12)).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(input_frame, font=("Arial", 12))
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[label_text] = entry
            if unit:
                tk.Label(input_frame, text=unit, font=("Arial", 12)).grid(row=i, column=2, padx=5, pady=5, sticky="w")

        # Calculate Button Inside Input Frame
        ttk.Button(input_frame, text="Calculate", command=self.calculate).grid(row=len(inputs), column=0, columnspan=3, pady=10)

        # Results Section
        result_frame = tk.LabelFrame(scrollable_frame, text="Results", font=("Arial", 14, "bold"), padx=10, pady=10)
        result_frame.pack(padx=100, pady=10, fill="both", expand=True)

        # Plot Section
        plot_frame = tk.LabelFrame(scrollable_frame, text="Shock Tube Diagram", font=("Arial", 14, "bold"), padx=10, pady=10)
        plot_frame.pack(padx=20, pady=10, fill="both", expand=True)

         # Matplotlib Figure
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Treeview with Scrollbar
        result_table_frame = tk.Frame(result_frame)
        result_table_frame.pack(fill="both", expand=True)

        columns = ("Property", "Value", "Unit")
        self.result_table = ttk.Treeview(result_table_frame, columns=columns, show="headings", height=15)
        self.result_table.pack(side="left", fill="both", expand=True)

        # Vertical Scrollbar for Treeview
        table_scrollbar = ttk.Scrollbar(result_table_frame, orient="vertical", command=self.result_table.yview)
        self.result_table.configure(yscroll=table_scrollbar.set)
        table_scrollbar.pack(side="right", fill="y")

        for col in columns:
            self.result_table.heading(col, text=col)
            self.result_table.column(col, anchor="center", width=200)

        # Alternating Row Colors
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#d9d9d9", relief="solid")
        style.map("Treeview", background=[("selected", "#fffbcc")], foreground=[("selected", "black")], font=[("selected", ("Arial", 12, "bold"))])
        self.result_table.tag_configure("odd", background="white")
        self.result_table.tag_configure("even", background="#f2f2f2")


        # Add the "Copy Value" button under the results table
        ttk.Button(result_frame, text="Copy Selected Value", command=self.copy_selected_value).pack(pady=10)
        

    def bind_mouse_wheel(self, canvas):
        """Bind mouse wheel events to scroll the canvas."""
        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")  # For Windows and MacOS
        def on_mouse_wheel_linux(event):
            canvas.yview_scroll(-1 if event.num == 4 else 1, "units")  # For Linux systems

        # Bind events only when the cursor is over the canvas
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        

        # For Linux (bind mouse buttons 4 and 5)
        canvas.bind( "<Button-4>", on_mouse_wheel_linux)
        canvas.bind( "<Button-5>", on_mouse_wheel_linux)
      

    def calculate(self):
        """Perform calculations and display results."""
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
            driver_length = float(self.entries["Driver Length"].get())
            driven_length = float(self.entries["Driven Length"].get())

            # Perform calculations
            shock_tube = ShockTube(gamma1, gamma4, R1, R4, T1, T4, p1gage, p4gage, patm)
            results = shock_tube.run_calculations()

            # Clear previous results
            for row in self.result_table.get_children():
                self.result_table.delete(row)

            # Insert new results
            properties = [
                # Region-specific properties
                ("T1", results["T1"], "K"),
                ("p1", results["p1"], "Pa"),
                ("rho1", results["rho1"], "kg/m³"),
                ("v1", results["v1"], "m/s"),
                ("a1", results["a1"], "m/s" ),
                ("T2", results["T2"], "K"),
                ("p2", results["p2"], "Pa"),
                ("rho2", results["rho2"], "kg/m³"),
                ("v2", results["v2"], "m/s"),
                ("a2", results["a2"], "m/s" ),
                ("T3", results["T3"], "K"),
                ("p3", results["p3"], "Pa"),
                ("rho3", results["rho3"], "kg/m³"),
                ("v3", results["v3"], "m/s"),
                ("a3", results["a3"], "m/s" ),
                ("T4", results["T4"], "K"),
                ("p4", results["p4"], "Pa"),
                ("rho4", results["rho4"], "kg/m³"),
                ("v4", results["v4"], "m/s"),
                ("a4", results["a4"], "m/s" ),
                ("T5", results["T5"], "K"),
                ("p5", results["p5"], "Pa"),
                ("rho5", results["rho5"], "kg/m³"),
                ("v5", results["v5"], "m/s"),
                ("a5", results["a5"], "m/s" ),
                # Key properties
                ("Si", results["Si"], "m/s"),
                ("Mi", results["Mi"], ""),
                ("Sr", results["Sr"], "m/s"),
                ("Mr", results["Mr"], ""),
                ("V_CS", results["v_CS"], "m/s"),
                ("V_EW", results["v_EW"], "m/s"),
            ]
            for i, (prop, val, unit) in enumerate(properties):
                tag = "odd" if i % 2 == 0 else "even"
                self.result_table.insert("", "end", values=(prop, f"{val:.2f}", unit), tags=(tag,))
            xS = [0.001, driven_length]
            tS = [0.001, driven_length / results["Si"]]

            xSR = [driven_length, driven_length - driver_length/2]
            tSR = [tS[1], tS[1] + driven_length*.25 / results["Sr"]]

            xCS = [0.001, driven_length]
            tCS = [0.001, xCS[1] / results["v2"]]


            # Plot
            self.ax.clear()
            self.ax.plot(xS, tS, 'r+-', label="Normal Shock Incident")
            self.ax.plot(xSR, tSR, 'b+-', label="Normal Shock Reflected")
            self.ax.plot(xCS, tCS, 'k+-', label="Contact Surface")

            # Labels, Legend, and Grid
            self.ax.set_xlabel("x (m)", fontsize=12, fontweight="bold")
            self.ax.set_ylabel("t (s)", fontsize=12, fontweight="bold")
            self.ax.legend()
            self.ax.grid(True)

            

            # Update the Canvas
            self.canvas.draw()

        except Exception as e:
            self.result_table.insert("", "end", values=("Error", str(e), ""))

    def copy_selected_value(self):
        """Copy the selected value from the table to the clipboard."""
        selected_item = self.result_table.selection()  # Get selected row
        if selected_item:
            value = self.result_table.item(selected_item, "values")[1]  # Get 'Value' column
            self.clipboard_clear()
            self.clipboard_append(value)
            self.update()  # Update clipboard
    