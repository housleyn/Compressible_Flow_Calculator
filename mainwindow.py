import tkinter as tk
from GUI_configuration.HomePage import HomePage
from GUI_configuration.IsentropicFlowPage import IsentropicFlowPage
from GUI_configuration.NormalShockPage import NormalShockPage
from GUI_configuration.obliqueShockPage import ObliqueShocksPage
from GUI_configuration.fannoFlowPage import FannoFlowPage
from GUI_configuration.rayleighFlowPage import RayleighFlowPage
from GUI_configuration.shockTubePage import ShockTubesPage
from GUI_configuration.normalShockLocationPage import NormalShockLocationsPage

class CompressibleFlowApp(tk.Tk):
    """Main application to manage multiple pages."""
    def __init__(self):
        super().__init__()
        self.title("Compressible Flow Calculator")
        self.geometry("800x600")

        # Container to hold all pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Dictionary to hold page frames
        self.frames = {}

        # Initialize pages
        for Page in (HomePage, IsentropicFlowPage, NormalShockPage, ObliqueShocksPage, 
                     FannoFlowPage, RayleighFlowPage, ShockTubesPage, NormalShockLocationsPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page by default
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()
