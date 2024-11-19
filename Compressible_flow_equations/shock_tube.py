import numpy as np
from scipy.optimize import minimize

class ShockTube:
    def __init__(self, gamma1, gamma4, R1, R4, T1, T4, p1gage, p4gage, patm):
        """
        Initialize the ShockTube parameters.
        """
        self.gamma1 = gamma1
        self.gamma4 = gamma4
        self.R1 = R1
        self.R4 = R4
        self.T1 = T1
        self.T4 = T4
        self.p1 = p1gage+patm
        self.p4 = p4gage+patm


        # Calculate initial speeds of sound
        self.a1 = self.calculate_a(self.R1, self.gamma1, self.T1)
        self.a4 = self.calculate_a(self.R4, self.gamma4, self.T4)

    @staticmethod
    def calculate_a(R, gamma, T):
        """Calculate speed of sound using perfect gas relations."""
        return np.sqrt(R * gamma * T)

    def calculate_p2_p1(self, p2_p1):
        """Equation 5.36 for pressure ratio across the shock."""
        numerator = (self.gamma4 - 1) * (self.a1 / self.a4) * (p2_p1 - 1)
        denominator = np.sqrt(2 * self.gamma1) * np.sqrt(2 * self.gamma1 + (self.gamma1 + 1) * (p2_p1 - 1))
        power = -((2 * self.gamma4) / (self.gamma4 - 1))
        lhs = (self.p4 / self.p1)
        rhs = p2_p1 * (1 - (numerator / denominator))**power
        return rhs - lhs

    def optimize_p2_p1(self):
        """Optimize p2/p1 using the minimize method."""
        initial_guess = 1
        result = minimize(
            lambda p2_p1: np.abs(self.calculate_p2_p1(p2_p1)),
            initial_guess,
            method='SLSQP',
            tol=1e-6
        )
        return result.x[0]

    @staticmethod
    def calculate_Si(a1, gamma1, p2_p1):
        """Equation 5.32."""
        return a1 * np.sqrt(((gamma1 + 1) / (2 * gamma1)) * p2_p1 + ((gamma1 - 1) / (2 * gamma1)))

    @staticmethod
    def calculate_mach_from_shock_speed(S, a):
        """Calculate Mach number from shock speed."""
        return S / a

    @staticmethod
    def calculate_T2_T1(gamma1, p2_p1):
        """Equation 5.37."""
        numerator = ((gamma1 - 1) / (gamma1 + 1)) * p2_p1 + 1
        denominator = 1 + ((gamma1 - 1) / (gamma1 + 1)) * (p2_p1**-1)
        return numerator / denominator

    @staticmethod
    def calculate_rho2_rho1(gamma1, p2_p1):
        """Equation 5.34."""
        numerator = ((gamma1 + 1) / (gamma1 - 1)) * p2_p1 + 1
        denominator = p2_p1 + ((gamma1 + 1) / (gamma1 - 1))
        return numerator / denominator

    @staticmethod
    def calculate_v2_and_v3(a1, gamma1, p2_p1):
        """Equation 5.35."""
        numerator = (2 * gamma1) / (gamma1 + 1)
        denominator = p2_p1 + ((gamma1 - 1) / (gamma1 + 1))
        return (a1 / gamma1) * (p2_p1 - 1) * np.sqrt(numerator / denominator)

    def run_calculations(self):

        p2_p1 = self.optimize_p2_p1()
        
        Si = self.calculate_Si(self.a1, self.gamma1, p2_p1)
        Mi = self.calculate_mach_from_shock_speed(Si, self.a1)
        p2 = p2_p1 * self.p1
        T2 = self.calculate_T2_T1(self.gamma1, p2_p1) * self.T1
        rho1 = self.p1 / (self.T1 * self.R1)
        rho2 = self.calculate_rho2_rho1(self.gamma1, p2_p1) * rho1
        v2 = self.calculate_v2_and_v3(self.a1, self.gamma1, p2_p1)

        a2 = self.calculate_a(self.R1, self.gamma1, T2)

        Sr = (-a2**2 / (v2 - Si)) - v2
        Mr = self.calculate_mach_from_shock_speed(Sr + v2, a2)
        p5 = ((3 * self.gamma4 - 1) / (self.gamma4 + 1)) - \
            ((self.gamma4 - 1) / (self.gamma4 + 1)) * p2_p1**-1
        p5 = p5 / (p2_p1**-1 + ((self.gamma4 - 1) / (self.gamma4 + 1)))
        p5 *= p2
        T5 = 1 + ((self.gamma4 - 1) / a2**2) * ((Sr + v2) * v2 - v2**2 / 2)
        T5 *= T2
        rho5 = p5 / (T5 * self.R4)

        T3 = ((p2_p1 / (self.p4 / self.p1))**((self.gamma4 - 1) / self.gamma4)) * self.T4
        rho3 = (T3 / self.T4)**(1 / (self.gamma4 - 1)) * (self.p4 / (self.T4 * self.R4))
        p3 = p2
        a3 = self.calculate_a(self.R1, self.gamma1, T3)
        a5 = self.calculate_a(self.R4,self.gamma4,T5)
        v1 = 0
        v4 = 0
        v5 = 0

        return {
            "a1": self.a1, "a2": a2, "a3": a3, "a4": self.a4, "a5": a5,  
            "rho1": rho1, "rho2": rho2, "rho3": rho3, "rho4": self.p4 / (self.T4 * self.R4), "rho5": rho5,
            "v1": v1, "v2": v2, "v3": v2, "v4": v4, "v5": v5,
            "T1": self.T1, "T2": T2, "T3": T3, "T4": self.T4, "T5": T5,
            "p1": self.p1, "p2": p2, "p3": p3, "p4": self.p4, "p5": p5,
            "Si": Si,
            "Sr": Sr,
            "Mi": Mi,
            "Mr": Mr,
            "v_CS":v2,
            "v_EW": self.a4
        }

