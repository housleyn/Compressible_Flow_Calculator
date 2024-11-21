import tkinter as tk
from tkinter import ttk
from GUI_configuration.IsentropicFlowPage import IsentropicFlowPage
from GUI_configuration.NormalShockPage import NormalShockPage
from GUI_configuration.obliqueShockPage import ObliqueShockPage
from GUI_configuration.fannoFlowPage import FannoFlowPage
from GUI_configuration.rayleighFlowPage import RayleighFlowPage
from GUI_configuration.shockTubePage import ShockTubePage  
from GUI_configuration.superAirfoil import SupersonicAirfoilPage 


class DynamicFlowCalculatorApp(tk.Tk):
    """Main app for the dynamic flow calculator with tabs."""
    
    def __init__(self):
        super().__init__()
        self.title("Dynamic Flow Calculator with Tabs")
        self.geometry("800x600")

        # Create the Notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Add the dynamic flow calculator tab
        self.dynamic_calculator_tab = tk.Frame(self.notebook)
        self.notebook.add(self.dynamic_calculator_tab, text="Flow Calculator")
        self.init_dynamic_calculator_tab()

        # Add the shock tube page tab
        self.shock_tube_tab = ShockTubePage(self.notebook)
        self.notebook.add(self.shock_tube_tab, text="Shock Tube")

        # Add the supersonic airfoil page tab
        self.supersonic_airfoil_tab = SupersonicAirfoilPage(self.notebook)
        self.notebook.add(self.supersonic_airfoil_tab, text="Supersonic Airfoil")

        # Future tabs can be added here as needed

    def init_dynamic_calculator_tab(self):
        """Initialize the dynamic calculator tab."""
        # Scrollable container for calculators
        container = tk.Frame(self.dynamic_calculator_tab)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling
        self.bind_mouse_wheel(self.canvas)

        # Track the number of calculators dynamically
        self.calculator_count = 0
        self.scrollable_frame = scrollable_frame

        # Dictionary to track calculators by ID
        self.calculator_frames = {}

        # Start with the first dropdown menu
        self.add_calculator_dropdown(scrollable_frame)

    def bind_mouse_wheel(self, canvas):
        """Bind mouse wheel events to scroll the canvas."""
        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")  # For Windows
        def on_mouse_wheel_linux(event):
            canvas.yview_scroll(-1 if event.num == 4 else 1, "units")  # For Linux systems

        self.bind_all("<MouseWheel>", on_mouse_wheel)
        self.bind_all("<Button-4>", on_mouse_wheel_linux)
        self.bind_all("<Button-5>", on_mouse_wheel_linux)

    def add_calculator_dropdown(self, parent):
        """Create a dropdown menu to choose and add calculators."""
        frame = tk.Frame(parent)
        frame.pack(pady=10, fill="x")

        tk.Label(frame, text="Choose Calculator Type:", font=("Arial", 14)).pack(side="left", padx=10)

        calculator_types = {
            "Isentropic Flow": IsentropicFlowPage,
            "Normal Shock Flow": NormalShockPage,
            "Oblique Shock Flow": ObliqueShockPage,
            "Fanno Flow": FannoFlowPage,
            "Rayleigh Flow": RayleighFlowPage
        }

        calculator_var = tk.StringVar()
        dropdown = ttk.OptionMenu(frame, calculator_var, "Select", *calculator_types.keys())
        dropdown.pack(side="left", padx=10)

        def add_calculator():
            selected_type = calculator_var.get()
            if selected_type != "Select" and selected_type in calculator_types:
                self.add_calculator_instance(calculator_types[selected_type])

        tk.Button(frame, text="Add", command=add_calculator).pack(side="left", padx=10)

        # Add Clear All Button
        tk.Button(frame, text="Clear All Calculators", command=self.clear_all_calculators).pack(side="left", padx=10)

    def add_calculator_instance(self, calculator_class):
        """Add a new calculator instance to the dynamic page."""
        # Determine the next available calculator number
        calculator_id = max(self.calculator_frames.keys(), default=0) + 1

        # Create calculator frame
        calculator_frame = tk.Frame(self.scrollable_frame, relief="ridge", borderwidth=2)
        calculator_frame.pack(pady=10, fill="x", padx=20)

        # Create and pack calculator label
        label = tk.Label(calculator_frame, text=f"Calculator {calculator_id}", font=("Arial", 14))
        label.pack(pady=5)

        # Create the calculator instance
        calculator_instance = calculator_class(calculator_frame, self)
        calculator_instance.pack(fill="x")

        # Add a clear button for this calculator
        clear_button = tk.Button(
            calculator_frame,
            text="Clear This Calculator",
            command=lambda: self.clear_single_calculator(calculator_id)
        )
        clear_button.pack(pady=5)

        # Create a new dropdown below this calculator
        dropdown_frame = tk.Frame(self.scrollable_frame)
        dropdown_frame.pack(pady=10, fill="x")
        self.add_calculator_dropdown(dropdown_frame)

        # Track the frame, label, and dropdown for this calculator
        self.calculator_frames[calculator_id] = {
            "frame": calculator_frame,
            "dropdown": dropdown_frame,
            "label": label
        }



    def clear_single_calculator(self, calculator_id):
        """Remove a single calculator and its associated dropdown."""
        if calculator_id in self.calculator_frames:
            # Destroy the calculator frame
            self.calculator_frames[calculator_id]["frame"].destroy()

            # Destroy the associated dropdown frame
            self.calculator_frames[calculator_id]["dropdown"].destroy()

            # Remove the calculator from the tracking dictionary
            del self.calculator_frames[calculator_id]



    def clear_all_calculators(self):
        """Remove all calculators and reset everything."""
        # Iterate through all calculator frames and destroy their components
        for calculator_data in self.calculator_frames.values():
            calculator_data["frame"].destroy()
            calculator_data["dropdown"].destroy()

        # Reset all tracking variables
        self.calculator_frames.clear()
        self.calculator_count = 0

        # Clear all existing dropdown menus and reinitialize the UI
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Re-add the first dropdown menu
        self.add_calculator_dropdown(self.scrollable_frame)

        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(0)

    def recalculate_calculator_numbers(self, starting_id):
        """Recalculate calculator numbering starting from the given ID."""
        sorted_ids = sorted(self.calculator_frames.keys())
        
        for new_id, old_id in enumerate(sorted_ids, start=starting_id):
            frame_data = self.calculator_frames[old_id]
            
            # Update the label for the calculator
            frame_data["label"].config(text=f"Calculator {new_id}")
            
            # Update the dictionary key
            self.calculator_frames[new_id] = self.calculator_frames.pop(old_id)
            
        # Adjust the next calculator count
        self.calculator_count = max(self.calculator_frames.keys(), default=0)