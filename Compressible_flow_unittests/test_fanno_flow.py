import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.fanno_flow import FannoFlow

@pytest.fixture
def fanno():
    return FannoFlow(gamma=1.4)

def test_4fLmax_D_limit(fanno):
    expected_limit = 0.8215081164811903
    assert fanno.fLmax_D_limit == pytest.approx(expected_limit)

def test_calculate_4fLmax_D(fanno):
    M = 2.0
    expected = 0.30499650
    assert fanno.calculate_4fLmax_D(M) == pytest.approx(expected)

def test_calculate_properties_4fL_D_subsonic(fanno):
    result = fanno.calculate("4fL*/D(subsonic)", 0.1)
    assert result["4fL*/D"] == pytest.approx(0.1)
    assert result["M"] < 1.0

def test_calculate_properties_4fL_D_supersonic(fanno):
    result = fanno.calculate("4fL*/D(supersonic)", 0.3)
    assert result["4fL*/D"] == pytest.approx(0.3)
    assert result["M"] > 1.0

def test_calculate_properties_p_pstar(fanno):
    result = fanno.calculate("p/p*", 0.5)
    assert result["p/p*"] == pytest.approx(0.5)

def test_invalid_gamma():
    with pytest.raises(ValueError, match="Gamma must be greater than 1."):
        FannoFlow(gamma=0.9)

def test_invalid_calculation_type(fanno):
    with pytest.raises(ValueError, match="Invalid calculation type"):
        fanno.calculate("Invalid Type", 0.5)
