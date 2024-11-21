import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.rayleigh_flow import RayleighFlow

def test_rayleigh_invalid_gamma():
    # Test gamma less than or equal to 1
    with pytest.raises(ValueError, match="Gamma \\(γ\\) must be greater than 1"):
        RayleighFlow(gamma=1.0)

def test_rayleigh_p0_p0s_out_of_scope():
    flow = RayleighFlow(gamma=1.4)

    # Test p0/p0s out of valid range for subsonic flow
    with pytest.raises(ValueError, match="Error: For subsonic flow, p0/p0\\* must be ≤ .* and >1"):
        flow.calculate_mach_number(target_p0_p0s=2.0, solution_type='subsonic')

    # Test p0/p0s less than 1
    with pytest.raises(ValueError, match="Error: The input p0/p0\\* must be > 1"):
        flow.calculate_mach_number(target_p0_p0s=0.8, solution_type='supersonic')

def test_rayleigh_T0_T0s_out_of_scope():
    flow = RayleighFlow(gamma=1.4)

    # Subsonic T0/T0s greater than 1
    with pytest.raises(ValueError, match="Exiting: For subsonic flow, T0/T0s must be between 0 and 1."):flow.calculate_mach_from_T0_T0s(1.2,"subsonic")

    # Supersonic T0/T0s less than min value
    with pytest.raises(ValueError, match="For supersonic flow, T0/T0s must be between .* and 1"):
        flow.calculate_mach_from_T0_T0s(0.1, "supersonic")

def test_rayleigh_T_Ts_out_of_scope():
    flow = RayleighFlow(gamma=1.4)

    # Below T_max
    with pytest.raises(ValueError, match="Invalid solution type. Choose 'below T_max' or 'above T_max'"):
        flow.calculate_mach_from_T_Ts(0.5, "invalid_type")

def test_rayleigh_calculations():
    flow = RayleighFlow(gamma=1.4)
    M = 2.0
    assert flow.calculate_p_ps(M) == pytest.approx( 0.36363636, rel=1e-5)
    assert flow.calculate_T_Ts(M) == pytest.approx(0.52892561, rel=1e-5)
    assert flow.calculate_T0_T0s(M) == pytest.approx(0.79338842, rel=1e-5)
    assert flow.calculate_p0_p0s(M) == pytest.approx(1.50309597, rel=1e-5)

def test_rayleigh_calculate_mach_number():
    flow = RayleighFlow(gamma=1.4)

    # Subsonic case
    M_subsonic = flow.calculate_mach_number(target_p0_p0s=1.2, solution_type='subsonic')
    assert M_subsonic == pytest.approx( 0.29635869, rel=1e-2)

    # Supersonic case
    M_supersonic = flow.calculate_mach_number(target_p0_p0s=1.2, solution_type='supersonic')
    assert M_supersonic == pytest.approx( 1.63973575, rel=1e-2)

def test_rayleigh_mach_from_T0_T0s():
    flow = RayleighFlow(gamma=1.4)

    # Subsonic case
    M_subsonic = flow.calculate_mach_from_T0_T0s(target_T0_T0s=0.5, solution_type='subsonic')
    assert M_subsonic == pytest.approx(0.38364861, rel=1e-5)

    # Supersonic case
    M_supersonic = flow.calculate_mach_from_T0_T0s(target_T0_T0s=0.5, solution_type='supersonic')
    assert M_supersonic == pytest.approx(13.0327592, rel=1e-5)

def test_rayleigh_mach_from_T_Ts():
    flow = RayleighFlow(gamma=1.4)

    # Below T_max case
    M_below_Tmax = flow.calculate_mach_from_T_Ts(target_T_Ts=0.5, solution_type='below T_max')
    assert M_below_Tmax == pytest.approx(0.34321697, rel=1e-5)

    # Above T_max case
    M_above_Tmax = flow.calculate_mach_from_T_Ts(target_T_Ts=0.5, solution_type='above T_max')
    assert M_above_Tmax == pytest.approx( 2.08114912, rel=1e-5)
