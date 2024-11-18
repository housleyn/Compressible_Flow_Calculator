import tkinter as tk

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
        tk.Label(input_frame, text="Mach Number:").grid(row=0, column=0, padx=5, pady=5)
        mach_entry = tk.Entry(input_frame)
        mach_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Shock Angle (degrees):").grid(row=1, column=0, padx=5, pady=5)
        angle_entry = tk.Entry(input_frame)
        angle_entry.grid(row=1, column=1, padx=5, pady=5)

        # Output
        output_var = tk.StringVar(value="Result will be displayed here")
        tk.Label(self, textvariable=output_var, fg="blue", font=("Arial", 12)).pack(pady=10)

        # Calculate Button
        def calculate():
            try:
                mach = float(mach_entry.get())
                angle = float(angle_entry.get())
                # Placeholder calculation
                result = f"Oblique shock result for Mach {mach}, angle {angle}°"
                output_var.set(result)
            except ValueError:
                output_var.set("Invalid input. Please enter valid numbers.")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)

        # Back to Home Button
        tk.Button(self, text="Back to Home",
                  command=lambda: controller.show_frame("HomePage")).pack(pady=20)
