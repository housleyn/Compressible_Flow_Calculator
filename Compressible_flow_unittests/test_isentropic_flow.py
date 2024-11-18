import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations import isentropic_flow

def test_isentropic_temperature_ratio():
    calculation_type = "T/T0"
    value = 0.8

    flow = isentropic_flow.isentropicFlow(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number == pytest.approx(1.11803398), "Mach number failed for temperature ratio, ISF"
    assert result.mach_angle == pytest.approx(63.4349488), "mach angle failed for temperature ratio, ISF"
    assert result.pm_angle == pytest.approx(1.69461163), "PM angle failed for temperature ratio, isf"
    assert result.t_t0 == pytest.approx(0.8), "Temperature ratio failed for temperature ratio, isf"
    assert result.p_p0 == pytest.approx(0.45794672), "pressure ratio failed for temperature ratio, isf"
    assert result.rho_rho0 == pytest.approx( 0.57243340), "density rario failed for temeprature ratio, isf"
    assert result.t_ts == pytest.approx(0.96), "critcial t ratio failed for temperature ratio, isf"
    assert result.p_ps == pytest.approx(0.86686070), "critical pressure ratio failed for t ratio, isf"
    assert result.rho_rhos == pytest.approx(0.90297989), "critical density failed for t ratio, isf"
    assert result.a_as == pytest.approx(1.01095376), "critical area reatio failed for t ratio, isf"

