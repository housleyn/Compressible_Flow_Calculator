import numpy as np
from scipy.optimize import root_scalar

class FannoFlow:
    def __init__(self, gamma):
        if gamma <= 1:
            raise ValueError("Gamma must be greater than 1.")
        self.gamma = gamma
        self.fLmax_D_limit = self.calculate_4fLmax_D_limit()

    def calculate_4fLmax_D_limit(self):
        gamma = self.gamma
        return ((gamma + 1) / (2 * gamma)) * np.log((gamma + 1) / (gamma - 1)) - 1 / gamma

    def calculate(self, calculation_type, value):
        g = self.gamma

        if calculation_type == "4fL*/D(subsonic)":
            if value <= 0:
                raise ValueError("4fL*/D(subsonic) must be greater than 0.")
            m = self.solve_4fLmax_D(value, subsonic=True)

        elif calculation_type == "4fL*/D(supersonic)":
            if value <= 0 or value >= self.fLmax_D_limit:
                raise ValueError(f"4fL*/D(supersonic) must be between 0 and {self.fLmax_D_limit}.")
            m = self.solve_4fLmax_D(value, subsonic=False)

        elif calculation_type == "p/p*":
            if value <= 0:
                raise ValueError("p/p* must be greater than 0.")
            m = self.solve_for_M(value, self.calculate_p_pstar)

        elif calculation_type == "rho/rho*":
            if value <= 0:
                raise ValueError("rho/rho* must be greater than 0.")
            m = self.solve_for_M(value, self.calculate_rho_rhostar)

        elif calculation_type == "T/T*":
            if value <= 0 or value >= 1.2:
                raise ValueError("T/T* must be between 0 and 1.2.")
            m = self.solve_for_M(value, self.calculate_T_Tstar)

        elif calculation_type == "Mach Number":
            if value <= 0:
                raise ValueError("Mach number must be greater than 0.")
            m = value

        else:
            raise ValueError(f"Invalid calculation type: {calculation_type}.")

        return {
            "M": m,
            "T/T*": self.calculate_T_Tstar(m),
            "p/p*": self.calculate_p_pstar(m),
            "rho/rho*": self.calculate_rho_rhostar(m),
            "4fL*/D": self.calculate_4fLmax_D(m),
        }

    def solve_4fLmax_D(self, input_value, subsonic=True):
        def subsonic_eq(M):
            return self.calculate_4fLmax_D(M) - input_value

        def supersonic_eq(M):
            return self.calculate_4fLmax_D(M) - input_value

        if subsonic:
            result = root_scalar(subsonic_eq, bracket=[0.01, 1], method="brentq")
        else:
            result = root_scalar(supersonic_eq, bracket=[1, 500], method="brentq")

        if result.converged:
            return result.root
        else:
            raise ValueError("Root finding did not converge.")

    def solve_for_M(self, input_value, func):
        def equation(M):
            return func(M) - input_value

        result = root_scalar(equation, bracket=[0.01, 100], method="brentq")
        if result.converged:
            return result.root
        else:
            raise ValueError("Root finding did not converge.")

    def calculate_4fLmax_D(self, M):
        gamma = self.gamma
        return ((gamma + 1) / (2 * gamma)) * np.log(((gamma + 1) / 2) / (1 + ((gamma - 1) / 2) * M**2)) - (1 / gamma) * (1 - (1 / M**2)) - ((gamma + 1) / (2 * gamma)) * np.log(1 / M**2)

    def calculate_p_pstar(self, M):
        gamma = self.gamma
        return (1 / M) * ((gamma + 1) / (2 + (gamma - 1) * M**2))**0.5

    def calculate_rho_rhostar(self, M):
        gamma = self.gamma
        return (1 / M) * ((2 + (gamma - 1) * M**2) / (gamma + 1))**0.5

    def calculate_T_Tstar(self, M):
        gamma = self.gamma
        return (gamma + 1) / (2 + (gamma - 1) * M**2)
