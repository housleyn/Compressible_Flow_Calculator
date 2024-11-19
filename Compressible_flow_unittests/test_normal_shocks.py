import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations import normal_shocks

def test_isentropic_temperature_ratio():
    calculation_type = "M1"
    value = 2.0

    flow = normal_shocks.NormalShock(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number1 == pytest.approx(2)
    assert result.mach_number2 == pytest.approx(0.57735026)
    assert result.p02p01 == pytest.approx(  0.72087386)
    assert result.p1p02 == pytest.approx( 0.17729110)
    assert result.p2p1 == pytest.approx( 4.5)
    assert result.r2r1 == pytest.approx(2.66666666)
    assert result.t2t1== pytest.approx( 1.6875)
    
    
    


