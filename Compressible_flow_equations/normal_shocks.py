import math 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flow_utilities import flow_utilities
from normalShockResult import normalShockResult

class NormalShock:
    def __init__(self, gamma):
        self.gamma = gamma
        self.utils = flow_utilities(gamma)  # Instance of Flow Utilities

    def calculate(self, calculation_type, v):
        g = self.gamma
        if g <= 1.0:
            raise ValueError("gamma must be greater than 1")

        if calculation_type == "M2":
            if v >= 1.0 or v <= math.sqrt((g - 1.0) / (2.0 * g)):
                raise ValueError(f"M2 must be between {math.sqrt((g - 1.0) / (2.0 * g))} and 1")
            m1 = self.utils.m2(v)

        elif calculation_type == "p2/p1":
            if v <= 1.0:
                raise ValueError("p2/p1 must be greater than 1")
            m1 = math.sqrt((v - 1.0) * (g + 1.0) / (2.0 * g) + 1.0)

        elif calculation_type == "rho2/rho1":
            if v <= 1.0 or v >= (g + 1.0) / (g - 1.0):
                raise ValueError(f"rho2/rho1 must be between 1 and {(g + 1.0) / (g - 1.0)}")
            m1 = math.sqrt(2.0 * v / (g + 1.0 - v * (g - 1.0)))

        elif calculation_type == "T2/T1":
            if v <= 1.0:
                raise ValueError("T2/T1 must be greater than 1")
            aa = 2.0 * g * (g - 1.0)
            bb = 4.0 * g - (g - 1.0) * (g - 1.0) - v * (g + 1.0) * (g + 1.0)
            cc = -2.0 * (g - 1.0)
            m1 = math.sqrt((-bb + math.sqrt(bb * bb - 4.0 * aa * cc)) / (2.0 * aa))

        elif calculation_type == "p02/p01":
          if v >= 1.0 or v <= 0.0:
              raise ValueError("p02/p01 must be between 0 and 1")
          mnew = 2.0
          m1 = 0.0
          while abs(mnew - m1) > 0.00001:
              m1 = mnew

              al = (g + 1.0) * m1 * m1 / ((g - 1.0) * m1 * m1 + 2.0)
              be = (g + 1.0) / (2.0 * g * m1 * m1 - (g - 1.0))

              # Check for division by zero or negative roots
              if (2.0 * g * m1 * m1 - (g - 1.0)) <= 0:
                  raise ValueError("Negative square root or division error detected.")

              daldm1 = (2.0 / m1 - 2.0 * m1 * (g - 1.0) / ((g - 1.0) * m1 * m1 + 2.0)) * al
              dbedm1 = -4.0 * g * m1 * be / (2.0 * g * m1 * m1 - (g - 1.0))

              fm = math.pow(al, g / (g - 1.0)) * math.pow(be, 1.0 / (g - 1.0)) - v
              fdm = g / (g - 1.0) * math.pow(al, 1.0 / (g - 1.0)) * daldm1 * math.pow(be, 1.0 / (g - 1.0)) + \
                    math.pow(al, g / (g - 1.0)) / (g - 1.0) * math.pow(be, (2.0 - g) / (g - 1.0)) * dbedm1

              if abs(fdm) < 1e-10:  # Threshold for division safety
                  raise ValueError("fdm too small, could result in division by zero")

              mnew = m1 - fm / fdm


        elif calculation_type == "p1/p02":
            vmax = math.pow((g + 1.0) / 2.0, -g / (g - 1.0))
            if v >= vmax or v <= 0.0:
                raise ValueError(f"p1/p02 must be between 0 and {vmax}")
            mnew = 2.0
            m1 = 0.0
            while abs(mnew - m1) > 0.00001:
                m1 = mnew
                al = (g + 1.0) * m1 * m1 / 2.0
                be = (g + 1.0) / (2.0 * g * m1 * m1 - (g - 1.0))
                daldm1 = m1 * (g + 1.0)
                dbedm1 = -4.0 * g * m1 * be / (2.0 * g * m1 * m1 - (g - 1.0))
                fm = math.pow(al, g / (g - 1.0)) * math.pow(be, 1.0 / (g - 1.0)) - 1.0 / v
                fdm = g / (g - 1.0) * math.pow(al, 1.0 / (g - 1.0)) * daldm1 * math.pow(be, 1.0 / (g - 1.0)) + math.pow(al, g / (g - 1.0)) / (g - 1.0) * math.pow(be, (2.0 - g) / (g - 1.0))
                mnew = m1 - fm / fdm

        elif calculation_type == "M1":
            if v <= 1.0:
                raise ValueError("Mach number must be greater than 1")
            m1 = v

        else:
            raise ValueError(f"Unknown calculation type: {calculation_type}")

        # Use utility methods from Flow_Utilities for calculations
        m2_value = self.utils.m2(m1)
        p2p1 = 1.0 + 2.0 * g / (g + 1.0) * (m1 * m1 - 1.0)
        p02p01 = self.utils.pp0(m1) / self.utils.pp0(m2_value) * p2p1
        r2r1 = self.utils.rr0(m2_value) / self.utils.rr0(m1) * p02p01
        t2t1 = self.utils.tt0(m2_value) / self.utils.tt0(m1)
        p1p02 = self.utils.pp0(m1) / p02p01


        mach_number1= m1
        mach_number2= m2_value

        return normalShockResult(mach_number1, mach_number2, p2p1, p02p01, r2r1, t2t1, p1p02)
