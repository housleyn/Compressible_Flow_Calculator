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

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling
        self.bind_mouse_wheel(canvas)

        # Track the number of calculators dynamically
        self.calculator_count = 0
        self.scrollable_frame = scrollable_frame

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

    def add_calculator_instance(self, calculator_class):
        """Add a new calculator instance to the dynamic page."""
        self.calculator_count += 1
        calculator_frame = tk.Frame(self.scrollable_frame, relief="ridge", borderwidth=2)
        calculator_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(calculator_frame, text=f"Calculator {self.calculator_count}", font=("Arial", 14)).pack(pady=5)

        # Create the calculator instance
        calculator_instance = calculator_class(calculator_frame, self)
        calculator_instance.pack(fill="x")

        # Add a new dropdown menu below this calculator
        self.add_calculator_dropdown(self.scrollable_frame)
