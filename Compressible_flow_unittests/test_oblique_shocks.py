import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations import oblique_shocks


def test_turn_angle_weak_shock():
    shock = oblique_shocks.ObliqueShock(gamma=1.4)
    result = shock.calculate("Turn angle (weak shock)", m1=2.5, a=15)
    assert pytest.approx(result["Wave Angle"], abs=1e-2) == 36.9449003
    assert pytest.approx(result["Turn Angle"], abs=1e-2) == 15.0
    assert pytest.approx(result["M1n"], abs=1e-2) == 1.50261680
    assert pytest.approx(result["M2n"], abs=1e-2) == 0.70016434
    assert pytest.approx(result["M2"], abs=1e-2) == 1.87352598
    assert pytest.approx(result["p2/p1"], abs=1e-2) == 2.46750012
    assert pytest.approx(result["p02/p01"], abs=1e-2) == 0.92895488
    assert pytest.approx(result["rho2/rho1"], abs=1e-2) == 1.86654863
    assert pytest.approx(result["T2/T1"], abs=1e-2) == 1.32195866

def test_turn_angle_strong_shock():
    shock = oblique_shocks.ObliqueShock(gamma=1.4)
    result = shock.calculate("Turn angle (strong shock)", m1=2.5, a=15)
    assert pytest.approx(result["Wave Angle"], abs=1e-2) == 83.0673437
    assert pytest.approx(result["Turn Angle"], abs=1e-2) == 15.0
    assert pytest.approx(result["M1n"], abs=1e-2) == 2.48172176
    assert pytest.approx(result["M2n"], abs=1e-2) == 0.51476083
    assert pytest.approx(result["M2"], abs=1e-2) ==  0.55492430
    assert pytest.approx(result["p2/p1"], abs=1e-2) == 7.01876676
    assert pytest.approx(result["p02/p01"], abs=1e-2) ==  0.50637036
    assert pytest.approx(result["rho2/rho1"], abs=1e-2) == 3.31157331
    assert pytest.approx(result["T2/T1"], abs=1e-2) == 2.11946591

def test_wave_angle():
    shock = oblique_shocks.ObliqueShock(gamma=1.4)
    result = shock.calculate("Wave angle", m1=3.0, a=45)
    assert pytest.approx(result["Wave Angle"], abs=1e-2) ==  45.0000000
    assert pytest.approx(result["Turn Angle"], abs=1e-2) ==  25.6154843
    assert pytest.approx(result["M1n"], abs=1e-2) ==  2.12132034
    assert pytest.approx(result["M2n"], abs=1e-2) == 0.55809982
    assert pytest.approx(result["M2"], abs=1e-2) ==   1.68149856
    assert pytest.approx(result["p2/p1"], abs=1e-2) ==  5.08333333
    assert pytest.approx(result["p02/p01"], abs=1e-2) ==  0.66430738
    assert pytest.approx(result["rho2/rho1"], abs=1e-2) ==  2.84210526
    assert pytest.approx(result["T2/T1"], abs=1e-2) ==  1.78858024

def test_m1n():
    shock = oblique_shocks.ObliqueShock(gamma=1.4)
    result = shock.calculate("M1n", m1=3.0, a=1.5)
    assert pytest.approx(result["Wave Angle"], abs=1e-2) ==  29.9999999
    assert pytest.approx(result["Turn Angle"], abs=1e-2) ==   12.7735070
    assert pytest.approx(result["M1n"], abs=1e-2) ==  1.5
    assert pytest.approx(result["M2n"], abs=1e-2) == 0.70108874
    assert pytest.approx(result["M2"], abs=1e-2) ==   2.36734554
    assert pytest.approx(result["p2/p1"], abs=1e-2) ==  2.45833333
    assert pytest.approx(result["p02/p01"], abs=1e-2) ==  0.92978651
    assert pytest.approx(result["rho2/rho1"], abs=1e-2) ==  1.86206896
    assert pytest.approx(result["T2/T1"], abs=1e-2) ==  1.32021604

def test_invalid_gamma():
    with pytest.raises(ValueError, match="Gamma must be greater than 1"):
        shock = oblique_shocks.ObliqueShock(gamma=0.9)

def test_invalid_m1():
    shock = shock = oblique_shocks.ObliqueShock(gamma=1.4)
    with pytest.raises(ValueError, match="M1 must be greater than 1"):
        shock.calculate("Turn angle (weak shock)", m1=0.5, a=15)

def test_invalid_turn_angle():
    shock = shock = oblique_shocks.ObliqueShock(gamma=1.4)
    with pytest.raises(ValueError, match="Turning angle must be between 0 and 90 degrees"):
        shock.calculate("Turn angle (weak shock)", m1=2.5, a=95)

    with pytest.raises(ValueError, match="Turning angle must be between 0 and 90 degrees"):
        shock.calculate("Turn angle (strong shock)", m1=2.5, a=-5)

def test_invalid_wave_angle():
    shock = shock = oblique_shocks.ObliqueShock(gamma=1.4)
    with pytest.raises(ValueError, match="Wave angle must be between Mach angle and 90 degrees"):
        shock.calculate("Wave angle", m1=2.0, a=20)  # Below Mach angle

    with pytest.raises(ValueError, match="Wave angle must be between Mach angle and 90 degrees"):
        shock.calculate("Wave angle", m1=2.0, a=95)  # Above 90 degrees

def test_invalid_m1n():
    shock = shock = oblique_shocks.ObliqueShock(gamma=1.4)
    with pytest.raises(ValueError, match="M1n must be between 1 and M1"):
        shock.calculate("M1n", m1=3.0, a=0.5)  # Below 1

    with pytest.raises(ValueError, match="M1n must be between 1 and M1"):
        shock.calculate("M1n", m1=3.0, a=4.0)  # Above M1
