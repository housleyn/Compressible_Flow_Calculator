import numpy as np
from scipy.optimize import root_scalar

class RayleighFlow:

    def __init__(self, gamma):

        if gamma <= 1.0:
            raise ValueError("Gamma (γ) must be greater than 1")
        self.gamma = gamma

    def calculate_p_ps(self, M):
        return (1 + self.gamma) / (1 + self.gamma * M**2)

    def calculate_T_Ts(self, M):
        return ((1 + self.gamma)**2 * M**2) / ((1 + self.gamma * M**2)**2)

    def calculate_T0_T0s(self, M):
        return ((1 + self.gamma) * M**2 * (2 + (self.gamma - 1) * M**2)) / ((1 + self.gamma * M**2)**2)

    def calculate_p0_p0s(self, M):
        return ((1 + self.gamma) / (1 + self.gamma * M**2)) * ((2 + (self.gamma - 1) * M**2) / (self.gamma + 1))**(self.gamma / (self.gamma - 1))
    
    def calculate_mach_number_p_ps(self,target_p_ps):
        return np.sqrt(((1+self.gamma)/self.gamma)*(target_p_ps**-1)-(1/self.gamma))
    
    def calculate_mach_number(self, target_p0_p0s, solution_type='subsonic'):
        if solution_type == 'subsonic':
            max_p0_p0s_subsonic = self.calculate_p0_p0s(0)  
            if target_p0_p0s > max_p0_p0s_subsonic:
                raise ValueError(f"Error: For subsonic flow, p0/p0* must be ≤ {max_p0_p0s_subsonic:.4f} and >1")
            if target_p0_p0s < 1.0:
                raise ValueError(f"Error: For subsonic flow, p0/p0* must be ≤ {max_p0_p0s_subsonic:.4f} and >1")

        if target_p0_p0s < 1.0:
            raise ValueError("Error: The input p0/p0* must be > 1")

        critical_p0_p0s = self.calculate_p0_p0s(1)
        if abs(target_p0_p0s - critical_p0_p0s) < 1e-6:
            return 1.0  # M = 1

        if solution_type == 'subsonic':
            bracket = (0.01, 0.99)
        elif solution_type == 'supersonic':
            bracket = (1.01, 5)
        else:
            raise ValueError("Invalid solution type. Choose 'subsonic' or 'supersonic'.")

        def p0_p0s_difference(M):
            return self.calculate_p0_p0s(M) - target_p0_p0s

        sol = root_scalar(p0_p0s_difference, bracket=bracket, method='brentq', xtol=1e-11)
        if sol.converged:
            return sol.root
        else:
            raise RuntimeError("Solver failed to converge. Check the input range and try again.")

    def calculate_mach_from_T_Ts(self, target_T_Ts, solution_type):
        if solution_type == 'below T_max':
            return (1 + self.gamma - np.sqrt((1 + self.gamma)**2 - 4 * self.gamma * target_T_Ts)) / (2 * self.gamma * np.sqrt(target_T_Ts))
        elif solution_type == 'above T_max':
            return (1 + self.gamma + np.sqrt((1 + self.gamma)**2 - 4 * self.gamma * target_T_Ts)) / (2 * self.gamma * np.sqrt(target_T_Ts))
        else:
            raise ValueError("Invalid solution type. Choose 'below T_max' or 'above T_max'.")

    def calculate_mach_from_T0_T0s(self, target_T0_T0s, solution_type='subsonic'):
      gamma = self.gamma

      # Define the minimum T0/T0s for supersonic flow
      min_T0_T0s_supersonic = self.calculate_T0_T0s(1e6)  # Approximates high Mach number behavior

      if solution_type == 'subsonic':
          if target_T0_T0s > 1 :
              raise ValueError("Exiting: For subsonic flow, T0/T0s must be between 0 and 1.")
              
          result_squared = ((1 + gamma) * (1 - np.sqrt(1 - target_T0_T0s)) - gamma * target_T0_T0s) / (gamma**2 * (target_T0_T0s - 1) + 1)

      elif solution_type == 'supersonic':
          if target_T0_T0s > 1 or target_T0_T0s < min_T0_T0s_supersonic:
              raise ValueError(f"Exiting: For supersonic flow, T0/T0s must be between {min_T0_T0s_supersonic} and 1.")
              
          result_squared = ((1 + gamma) * (1 + np.sqrt(1 - target_T0_T0s)) - gamma * target_T0_T0s) / (gamma**2 * (target_T0_T0s - 1) + 1)

      else:
          print("Exiting: Invalid solution type. Choose 'subsonic' or 'supersonic'.")
          return  # Exit the function early

      if result_squared < 0:
          print("Exiting: No real solution exists for the given T0/T0s.")
          return  # Exit the function early
    
      return np.sqrt(result_squared)