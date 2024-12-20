import pytest
import math
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations import isentropic_flow

def test_isentropic_temperature_ratio():
    calculation_type = "T/T0"
    value = 0.8

    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx(1.11803398)
    assert result.mach_angle == pytest.approx(63.4349488)
    assert result.pm_angle == pytest.approx(1.69461163)
    assert result.t_t0 == pytest.approx(0.8)
    assert result.p_p0 == pytest.approx(0.45794672)
    assert result.rho_rho0 == pytest.approx( 0.57243340)
    assert result.t_ts == pytest.approx(0.96)
    assert result.p_ps == pytest.approx(0.86686070)
    assert result.rho_rhos == pytest.approx(0.90297989)
    assert result.a_as == pytest.approx(1.01095376)

def test_isentropic_pressure_ratio():
    calculation_type = "p/p0"
    value = 0.8
    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx(0.57372274)
    assert result.t_t0 == pytest.approx(0.93823455)
    assert result.p_p0 == pytest.approx(0.8)
    assert result.rho_rho0 == pytest.approx(0.85266524)
    assert result.t_ts == pytest.approx( 1.12588146)
    assert result.p_ps == pytest.approx( 1.51434332)
    assert result.rho_rhos == pytest.approx( 1.34502908)
    assert result.a_as == pytest.approx( 1.22129313)

def test_isentropic_density_ratio():
    calculation_type = "rho/rho0"
    value = 0.8

    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx( 0.68323522)
   
   
    assert result.t_t0 == pytest.approx( 0.91461010)
    assert result.p_p0 == pytest.approx(0.73168808)
    assert result.rho_rho0 == pytest.approx( .8)
    assert result.t_ts == pytest.approx(1.09753212)
    assert result.p_ps == pytest.approx(1.38503370)
    assert result.rho_rhos == pytest.approx(1.26195277)
    assert result.a_as == pytest.approx(1.10707751)

def test_isentropic_subsonic_area_ratio():
    calculation_type = "A/A*(subsonic)"
    value = 1.2

    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx(0.59024789)
    assert result.t_t0 == pytest.approx( 0.93486031)
    assert result.p_p0 == pytest.approx(0.78997535)
    assert result.rho_rho0 == pytest.approx( 0.84501966)
    assert result.t_ts == pytest.approx(1.12183238)
    assert result.p_ps == pytest.approx(1.49536738)
    assert result.rho_rhos == pytest.approx( 1.33296863)
    assert result.a_as == pytest.approx(1.2)

def test_isentropic_supersonic_area_ratio():
    calculation_type = "A/A*(supersonic)"
    value = 1.2

    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx( 1.53414977)
    assert result.mach_angle == pytest.approx(40.6794797)
    assert result.pm_angle == pytest.approx(12.9127232)
    assert result.t_t0 == pytest.approx( 0.67993764)
    assert result.p_p0 == pytest.approx( 0.25920405)
    assert result.rho_rho0 == pytest.approx( 0.38121739)
    assert result.t_ts == pytest.approx( 0.81592516)
    assert result.p_ps == pytest.approx( 0.49065491)
    assert result.rho_rhos == pytest.approx(  0.60134793)
    assert result.a_as == pytest.approx(1.2)

def test_isentropic_mach_angle():
    calculation_type = "Mach Angle(deg.)"
    value = 20

    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx( 2.92380440)
    assert result.mach_angle == pytest.approx(20)
    assert result.pm_angle == pytest.approx( 48.2654699)
    assert result.t_t0 == pytest.approx(  0.36904094)
    assert result.p_p0 == pytest.approx( 0.03053239)
    assert result.rho_rho0 == pytest.approx( 0.08273444)
    assert result.t_ts == pytest.approx( 0.44284913)
    assert result.p_ps == pytest.approx(  0.05779566)
    assert result.rho_rhos == pytest.approx( 0.13050870)
    assert result.a_as == pytest.approx( 3.93807778)

def test_isentropic_PM_angle():
    calculation_type = "PM Angle(deg.)"
    value = 20

    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx( 1.77497230)
    assert result.mach_angle == pytest.approx(34.2905002)
    assert result.pm_angle == pytest.approx(19.9998981)
    assert result.t_t0 == pytest.approx( 0.61345728)
    assert result.p_p0 == pytest.approx(0.18081945)
    assert result.rho_rho0 == pytest.approx(0.29475476)
    assert result.t_ts == pytest.approx(0.73614874)
    assert result.p_ps == pytest.approx(0.34227842)
    assert result.rho_rhos == pytest.approx( 0.46495823)
    assert result.a_as == pytest.approx( 1.41225034)

def test_isentropic_mach_number():
    calculation_type = "Mach Number"
    value = 20

    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx(20)
    assert result.mach_angle == pytest.approx( 2.86598398)
    assert result.pm_angle == pytest.approx(116.195297)
    assert result.t_t0 == pytest.approx(0.01234567)
    assert result.p_p0 == pytest.approx( 2.090751581287687e-07, abs=1e-7)
    assert result.rho_rho0 == pytest.approx(1.6935087808430262e-05)
    assert result.t_ts == pytest.approx( 0.01481481)
    assert result.p_ps == pytest.approx(3.95764e-007)
    assert result.rho_rhos == pytest.approx(2.671410126530299e-05)
    assert result.a_as == pytest.approx( 15377.3437)


def test_isentropic_tt0_out_of_scope():
    flow = isentropic_flow.isentropicFlow(gamma=1.4)

    # T/T0 greater than 1
    with pytest.raises(ValueError, match="T/T0 must be between 0 and 1"):
        flow.calculate("T/T0", 1.2)

    # T/T0 less than or equal to 0
    with pytest.raises(ValueError, match="T/T0 must be between 0 and 1"):
        flow.calculate("T/T0", 0)

def test_isentropic_pp0_out_of_scope():
    flow = isentropic_flow.isentropicFlow(gamma=1.4)

    # p/p0 greater than 1
    with pytest.raises(ValueError, match="p/p0 must be between 0 and 1"):
        flow.calculate("p/p0", 1.1)

    # p/p0 less than or equal to 0
    with pytest.raises(ValueError, match="p/p0 must be between 0 and 1"):
        flow.calculate("p/p0", -0.5)

def test_isentropic_rho_rho0_out_of_scope():
    flow = isentropic_flow.isentropicFlow(gamma=1.4)

    # rho/rho0 greater than 1
    with pytest.raises(ValueError, match="rho/rho0 must be between 0 and 1"):
        flow.calculate("rho/rho0", 1.5)

    # rho/rho0 less than or equal to 0
    with pytest.raises(ValueError, match="rho/rho0 must be between 0 and 1"):
        flow.calculate("rho/rho0", 0)

def test_isentropic_area_ratio_out_of_scope():
    flow = isentropic_flow.isentropicFlow(gamma=1.4)

    # A/A* less than or equal to 1
    with pytest.raises(ValueError, match="A/A\\* must be greater than 1"):
        flow.calculate("A/A*(subsonic)", 0.9)

    with pytest.raises(ValueError, match="A/A\\* must be greater than 1"):
        flow.calculate("A/A*(supersonic)", 1.0)

def test_isentropic_mach_angle_out_of_scope():
    flow = isentropic_flow.isentropicFlow(gamma=1.4)

    # Mach angle less than or equal to 0
    with pytest.raises(ValueError, match="Mach angle must be between 0 and 90"):
        flow.calculate("Mach Angle(deg.)", -10)

    # Mach angle greater than or equal to 90
    with pytest.raises(ValueError, match="Mach angle must be between 0 and 90"):
        flow.calculate("Mach Angle(deg.)", 100)

def test_isentropic_pm_angle_out_of_scope():
    flow = isentropic_flow.isentropicFlow(gamma=1.4)

    # Prandtl-Meyer angle less than or equal to 0
    with pytest.raises(ValueError, match="Prandtl-Meyer angle must be between 0 and"):
        flow.calculate("PM Angle(deg.)", -1)

    # Prandtl-Meyer angle greater than maximum
    max_pm_angle = (math.sqrt((1.4 + 1.0) / (1.4 - 1.0)) - 1.0) * 90.0
    with pytest.raises(ValueError, match=f"Prandtl-Meyer angle must be between 0 and {max_pm_angle}"):
        flow.calculate("PM Angle(deg.)", max_pm_angle + 1)

def test_isentropic_mach_number_out_of_scope():
    flow = isentropic_flow.isentropicFlow(gamma=1.4)

    # Mach number less than or equal to 0
    with pytest.raises(ValueError, match="Mach number must be greater than 0"):
        flow.calculate("Mach Number", -5)

def test_isentropic_invalid_gamma():
    with pytest.raises(ValueError, match="gamma must be greater than 1"):
        flow = isentropic_flow.isentropicFlow(gamma=.9)
        flow.calculate("T/T0", 0.8)
