class IsentropicResult:
    def __init__(self, mach_number, mach_angle, pm_angle, t_t0, p_p0, rho_rho0, t_ts, p_ps, rho_rhos, a_as):
        self.mach_number = mach_number
        self.mach_angle = mach_angle
        self.pm_angle = pm_angle
        self.t_t0 = t_t0
        self.p_p0 = p_p0
        self.rho_rho0 = rho_rho0
        self.t_ts = t_ts
        self.p_ps = p_ps
        self.rho_rhos = rho_rhos
        self.a_as = a_as