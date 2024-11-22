import pytest
import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations.shock_tube import ShockTube    

@pytest.fixture
def shock_tube():
    """
    Fixture for initializing the ShockTube class with test parameters.
    """
    return ShockTube(
        gamma1=1.4,
        gamma4=1.4,
        R1=287,
        R4=287,
        T1=289.6,
        T4=295.8,
        p1gage=-80503.21,
        p4gage=191726.18,
        patm = 86386.78
    )

def test_calculate_a(shock_tube):
    """
    Test the calculation of speed of sound.
    """
    a1 = shock_tube.calculate_a(shock_tube.R1, shock_tube.gamma1, shock_tube.T1)
    a4 = shock_tube.calculate_a(shock_tube.R4, shock_tube.gamma4, shock_tube.T4)
    assert pytest.approx(a1, 0.1) == 341.1  # Expected value for a1
    assert pytest.approx(a4, 0.1) == 344.7  # Expected value for a4


def test_calculate_Si(shock_tube):
    """
    Test calculation of Si.
    """
    p2_p1 = shock_tube.optimize_p2_p1()
    Si = shock_tube.calculate_Si(shock_tube.a1, shock_tube.gamma1, p2_p1)
    assert pytest.approx(Si, 0.1) == 724.42  # Replace with expected value for Si

def test_calculate_mach_from_shock_speed(shock_tube):
    """
    Test calculation of Mach number from shock speed.
    """
    p2_p1 = shock_tube.optimize_p2_p1()
    Si = shock_tube.calculate_Si(shock_tube.a1, shock_tube.gamma1, p2_p1)
    Mi = shock_tube.calculate_mach_from_shock_speed(Si, shock_tube.a1)
    assert pytest.approx(Mi, 0.01) == 2.12  # Replace with expected Mach number


def test_calculate_v2_and_v3(shock_tube):
    """
    Test calculation of velocity v2 and v3.
    """
    p2_p1 = shock_tube.optimize_p2_p1()
    v2 = shock_tube.calculate_v2_and_v3(shock_tube.a1, shock_tube.gamma1, p2_p1)
    assert pytest.approx(v2, 0.1) == 469.83  # Replace with expected v2 value

def test_run_calculations(shock_tube):
    """
    Test the complete `run_calculations` method.
    """
    results = shock_tube.run_calculations()

def test_calculate_a_zone_values(shock_tube):
    """
    Test calculation of speed of sound in each zone.
    """
    results = shock_tube.run_calculations()
    assert pytest.approx(results["a1"], 0.1) == 341.1  
    assert pytest.approx(results["a2"], 0.1) == 456.5  
    assert pytest.approx(results["a3"], 0.1) == 250.8  
    assert pytest.approx(results["a4"], 0.1) == 344.7  
    assert pytest.approx(results["a5"], 0.1) == 563.9  

def test_rho_zone_values(shock_tube):
    """
    Test calculation of density in each zone.
    """
    results = shock_tube.run_calculations()
    assert pytest.approx(results["rho1"], 0.01) == 0.0707881350222341  
    assert pytest.approx(results["rho2"], 0.01) == 0.20142250795605757 
    assert pytest.approx(results["rho3"], 0.01) == 0.67  
    assert pytest.approx(results["rho4"], 0.01) == 3.2759793909153228  
    assert pytest.approx(results["rho5"], 0.01) == 0.47292537554855535

def test_velocity_zone_values(shock_tube):
    """
    Test calculation of velocities in each zone.
    """
    results = shock_tube.run_calculations()
    assert pytest.approx(results["v1"], 0.1) == 0.0  
    assert pytest.approx(results["v2"], 0.1) == 469.8  
    assert pytest.approx(results["v3"], 0.1) == 469.8  
    assert pytest.approx(results["v4"], 0.1) == 0.0 
    assert pytest.approx(results["v5"], 0.1) == 0.0
      

def test_temperature_zone_values(shock_tube):
    """
    Test calculation of temperatures in each zone.
    """
    results = shock_tube.run_calculations()
    assert pytest.approx(results["T1"], 0.1) == 289.6  
    assert pytest.approx(results["T2"], 0.1) == 518.6  
    assert pytest.approx(results["T3"], 0.1) == 156.5  
    assert pytest.approx(results["T4"], 0.1) == 295.8  
    assert pytest.approx(results["T5"], 0.1) == 791.5  

def test_pressure_zone_values(shock_tube):
    """
    Test calculation of pressures in each zone.
    """
    results = shock_tube.run_calculations()
    assert pytest.approx(results["p1"], 0.1) == 5883.57  
    assert pytest.approx(results["p2"], 0.1) == 29976.8 
    assert pytest.approx(results["p3"], 0.1) == 29976.8 
    assert pytest.approx(results["p4"], 0.1) == 278113.0  
    assert pytest.approx(results["p5"], 0.1) == 107424.9 

def test_calculate_Sr_and_Mr(shock_tube):
    """
    Test calculation of reflected shock speed (S_r) and reflected Mach number (M_r).
    """
    results = shock_tube.run_calculations()
    Sr = results["Sr"]
    Mr = results["Mr"]
    assert pytest.approx(Sr, 0.1) == 348.56  # Replace with expected S_r
    assert pytest.approx(Mr, 0.01) == 1.79  # Replace with expected Mach number

def test_calculate_v_CS_and_v_EW(shock_tube):
    results = shock_tube.run_calculations()
    v_CS = results["v_CS"]
    v_EW = results["v_EW"]
    assert pytest.approx(v_CS, 0.1) == 469.83
    assert pytest.approx(v_EW, 0.1) == 344.75
