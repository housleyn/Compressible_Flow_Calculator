import math 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flow_utilities import flow_utilities
from IsentropicResult import IsentropicResult

class isentropicFlow:
    def __init__(self, gamma):
        self.gamma = gamma  # Store gamma as a class attribute
        self.utilities = flow_utilities(self.gamma)  # Instance of Flow Utilities

    # Method to calculate based on descriptive string types
    def calculate(self, calculation_type, value):
        g = self.gamma
        if g <= 1.0:
            raise ValueError("gamma must be greater than 1")

        if calculation_type == "T/T0":
            if value >= 1.0 or value <= 0.0:
                raise ValueError("T/T0 must be between 0 and 1")
            m = math.sqrt(2.0 * ((1.0 / value) - 1.0) / (g - 1.0))

        elif calculation_type == "p/p0":
            if value >= 1.0 or value <= 0.0:
                raise ValueError("p/p0 must be between 0 and 1")
            m = math.sqrt(2.0 * ((1.0 / math.pow(value, (g - 1.0) / g)) - 1.0) / (g - 1.0))

        elif calculation_type == "rho/rho0":
            if value >= 1.0 or value <= 0.0:
                raise ValueError("rho/rho0 must be between 0 and 1")
            m = math.sqrt(2.0 * ((1.0 / math.pow(value, (g - 1.0))) - 1.0) / (g - 1.0))

        elif calculation_type == "A/A*(subsonic)" or calculation_type == "area_ratio_supersonic":
            if value <= 1.0:
                raise ValueError("A/A* must be greater than 1")
            mnew = 0.00001
            m = 0.0
            if calculation_type == "A/A*(supersonic)":
                mnew = 2.0
            while abs(mnew - m) > 0.000001:
                m = mnew
                phi = self.utilities.aas(m)
                s = (3.0 - g) / (1.0 + g)
                mnew = m - (phi - value) / (math.pow(phi * m, s) - phi / m)

        elif calculation_type == "Mach Angle(deg.)":
            if value <= 0.0 or value >= 90.0:
                raise ValueError("Mach angle must be between 0 and 90")
            m = 1.0 / math.sin(value * math.pi / 180.0)

        elif calculation_type == "PM angle(deg.)":
            numax = (math.sqrt((g + 1.0) / (g - 1.0)) - 1.0) * 90.0
            if value <= 0.0 or value >= numax:
                raise ValueError(f"Prandtl-Meyer angle must be between 0 and {numax}")
            mnew = 2.0
            m = 0.0
            while abs(mnew - m) > 0.00001:
                m = mnew
                fm = (self.utilities.nu(m) - value) * math.pi / 180.0
                fdm = math.sqrt(m * m - 1.0) / (1 + 0.5 * (g - 1.0) * m * m) / m
                mnew = m - fm / fdm

        elif calculation_type == "Mach Number":
            if value <= 0.0:
                raise ValueError("Mach number must be greater than 0")
            m = value

        else:
            raise ValueError("Invalid calculation type")




        mach_number = m
        mach_angle = math.asin(1.0 / m) * 180 / math.pi if m > 1.0 else 90.0 if m == 1 else ""
        pm_angle = self.utilities.nu(m) if m > 1.0 else 0.0 if m == 1 else ""
        t_t0 = self.utilities.tt0(m)
        p_p0 = self.utilities.pp0(m)
        rho_rho0 = self.utilities.rr0(m)
        t_ts = self.utilities.tts(m)
        p_ps = self.utilities.pps(m)
        rho_rhos = self.utilities.rrs(m)
        a_as = self.utilities.aas(m)


        return IsentropicResult(mach_number, mach_angle, pm_angle, t_t0, p_p0, rho_rho0, t_ts, p_ps, rho_rhos, a_as)
