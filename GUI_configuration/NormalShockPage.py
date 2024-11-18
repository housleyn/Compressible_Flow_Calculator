import tkinter as tk

class NormalShockPage(tk.Frame):
    """Page for normal shock calculations."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Normal Shock Calculations", font=("Arial", 16)).pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Mach Number:").grid(row=0, column=0, padx=5, pady=5)
        mach_entry = tk.Entry(input_frame)
        mach_entry.grid(row=0, column=1, padx=5, pady=5)

        # Output
        output_var = tk.StringVar(value="Result will be displayed here")
        tk.Label(self, textvariable=output_var, fg="blue", font=("Arial", 12)).pack(pady=10)

        # Calculate Button
        def calculate():
            try:
                mach = float(mach_entry.get())
                # Placeholder calculation
                result = f"Normal shock calculation result for Mach {mach}"
                output_var.set(result)
            except ValueError:
                output_var.set("Invalid input. Please enter a valid Mach number.")

        tk.Button(self, text="Calculate", command=calculate).pack(pady=10)

        # Back to Home Button
        tk.Button(self, text="Back to Home",
                  command=lambda: controller.show_frame("HomePage")).pack(pady=20)
