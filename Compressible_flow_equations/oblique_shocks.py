import math

class ObliqueShock:
    def __init__(self, gamma):
        if gamma <= 1.0:
            raise ValueError("Gamma must be greater than 1.")
        self.gamma = gamma

    def calculate(self, calculation_type, m1, a):
        """
        Parameters:
        - calculation_type: str, one of ["Turn angle (weak shock)", "Turn angle (strong shock)", "Wave angle", "M1n"]
        - m1: float, upstream Mach number
        - a: float, input angle (degrees)
        
        Returns: dict, calculated oblique shock properties.
        """
        if m1 <= 1.0:
            raise ValueError("M1 must be greater than 1.")

        g = self.gamma
        a_rad = math.radians(a)

        if calculation_type in ["Turn angle (weak shock)", "Turn angle (strong shock)"]:
            if a <= 0.0 or a >= 90.0:
                raise ValueError("Turning angle must be between 0 and 90 degrees.")
            delta = a_rad
            if calculation_type == "Turn angle (weak shock)":
                theta_weak, _ = self._calculate_wave_angle_iterative(g, m1, delta)
                beta = math.radians(theta_weak)
            else:
                _, theta_strong = self._calculate_wave_angle_iterative(g, m1, delta)
                beta = math.radians(theta_strong)

        elif calculation_type == "Wave angle":
            if a <= math.degrees(math.asin(1.0 / m1)) or a >= 90.0:
                raise ValueError("Wave angle must be between Mach angle and 90 degrees.")
            beta = math.radians(a)
            delta = self._calculate_turn_angle(g, m1, beta)

        elif calculation_type == "M1n":
            if a <= 1.0 or a >= m1:
                raise ValueError("M1n must be between 1 and M1.")
            beta = math.asin(a / m1)
            delta = self._calculate_turn_angle(g, m1, beta)

        else:
            raise ValueError(f"Invalid calculation type: {calculation_type}")

        m1n = m1 * math.sin(beta)
        m2n = self._calculate_m2(g, m1n)
        delta_deg = a if calculation_type in ["Turn angle (weak shock)", "Turn angle (strong shock)"] else math.degrees(delta)
        beta_deg = math.degrees(beta)
        m2 = m2n / math.sin(beta - delta)
        p2p1 = 1.0 + 2.0 * g / (g + 1.0) * (m1n**2 - 1.0)
        p02p01 = self._calculate_p02p01(g, m1n, m2n)
        r2r1 = self._calculate_rho_ratio(g, m1n, m2n, p02p01)
        t2t1 = self._calculate_temp_ratio(g, m1n, m2n)

        return {
            "Wave Angle": beta_deg,
            "Turn Angle": delta_deg,
            "M1n": m1n,
            "M2n": m2n,
            "M2": m2,
            "p2/p1": p2p1,
            "p02/p01": p02p01,
            "rho2/rho1": r2r1,
            "T2/T1": t2t1
        }


    def _calculate_wave_angle_iterative(self, g, m1, delta):
        """
        Calculate wave angle (beta) iteratively based on the given delta (turning angle).
        This method distinguishes between weak shock (theta) and strong shock (theta2).
        """
        x = [math.sqrt(m1**2 - 1)]
        error = 1.0
        tolerance = 1e-7
        i = 0

        A = m1**2 - 1
        B = ((g + 1) / 2) * m1**4 * math.tan(delta)
        C = (1 + ((g + 1) / 2) * m1**2) * math.tan(delta)

        while error > tolerance:
            x_new = math.sqrt(A - (B / (x[i] + C)))
            x.append(x_new)
            error = abs(x[i + 1] - x[i])
            i += 1

        x_weak = x[-1]  # Converged value for the weak shock
        theta_weak = math.degrees(math.atan(1 / x_weak))

        # Calculate strong shock solution
        numerator = 0.5 * (-(x_weak + C) + math.sqrt((x_weak + C) * (C - 3 * x_weak) + 4 * A))
        theta_strong = math.degrees(math.atan(1 / numerator))

        return theta_weak, theta_strong

    def _calculate_turn_angle(self, g, m1, beta):
        """
        Calculate the turning angle (delta) for a given wave angle (beta).
        """
        numerator = m1**2 * math.sin(2 * beta) - 2 / math.tan(beta)
        denominator = 2 + m1**2 * (g + math.cos(2 * beta))
        return math.atan(numerator / denominator)

    def _calculate_m2(self, g, m1n):
        """
        Calculate downstream Mach number normal to the shock.
        """
        return math.sqrt((1 + 0.5 * (g - 1) * m1n**2) / (g * m1n**2 - 0.5 * (g - 1)))

    def _calculate_p02p01(self, g, m1n, m2n):
        """
        Calculate total pressure ratio across the shock.
        """
        p2p1 = 1.0 + 2.0 * g / (g + 1.0) * (m1n**2 - 1.0)
        return self._calculate_pp0(g, m1n) / self._calculate_pp0(g, m2n) * p2p1

    def _calculate_rho_ratio(self, g, m1n, m2n, p02p01):
        """
        Calculate density ratio across the shock.
        """
        return self._calculate_rr0(g, m2n) / self._calculate_rr0(g, m1n) * p02p01

    def _calculate_temp_ratio(self, g, m1n, m2n):
        """
        Calculate temperature ratio across the shock.
        """
        return self._calculate_tt0(g, m2n) / self._calculate_tt0(g, m1n)

    def _calculate_pp0(self, g, m):
        """
        Calculate static-to-total pressure ratio.
        """
        return (1.0 + (g - 1.0) / 2.0 * m**2) ** (-g / (g - 1.0))

    def _calculate_rr0(self, g, m):
        """
        Calculate static-to-total density ratio.
        """
        return (1.0 + (g - 1.0) / 2.0 * m**2) ** (-1.0 / (g - 1.0))

    def _calculate_tt0(self, g, m):
        """
        Calculate static-to-total temperature ratio.
        """
        return (1.0 + (g - 1.0) / 2.0 * m**2) ** -1.0
