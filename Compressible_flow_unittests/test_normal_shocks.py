import sys
import os
import pytest
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Compressible_flow_equations import normal_shocks

def test_normal_mach_number1():
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
    
    
    
def test_normal_mach_number2():
    calculation_type = "M2"
    value = .5

    flow = normal_shocks.NormalShock(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number1 == pytest.approx(2.64575131)
    assert result.mach_number2 == pytest.approx(.5)
    assert result.p02p01 == pytest.approx(0.44311166)
    assert result.p1p02 == pytest.approx( 0.10537739)
    assert result.p2p1 == pytest.approx( 7.99999999)
    assert result.r2r1 == pytest.approx( 3.49999999)
    assert result.t2t1== pytest.approx( 2.28571428)

def test_normal_static_pressure_ratio():
    calculation_type = "p2/p1"
    value = 2

    flow = normal_shocks.NormalShock(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number1 == pytest.approx(1.36277028)
    assert result.mach_number2 == pytest.approx( 0.75592894)
    assert result.p02p01 == pytest.approx(0.96696730)
    assert result.p1p02 == pytest.approx( 0.34235922)
    assert result.p2p1 == pytest.approx( 2)
    assert result.r2r1 == pytest.approx(  1.625)
    assert result.t2t1== pytest.approx(  1.23076923)

def test_normal_density_ratio():
    calculation_type = "rho2/rho1"
    value = 2

    flow = normal_shocks.NormalShock(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number1 == pytest.approx(1.58113883)
    assert result.mach_number2 == pytest.approx( 0.67419986)
    assert result.p02p01 == pytest.approx(0.90213856)
    assert result.p1p02 == pytest.approx( 0.26816824)
    assert result.p2p1 == pytest.approx( 2.75000000)
    assert result.r2r1 == pytest.approx(2)
    assert result.t2t1== pytest.approx( 1.37500000)

def test_normal_temperature_ratio():
    calculation_type = "T2/T1"
    value = 2

    flow = normal_shocks.NormalShock(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number1 == pytest.approx(2.35735168)
    assert result.mach_number2 == pytest.approx(  0.52778166)
    assert result.p02p01 == pytest.approx( 0.55831602)
    assert result.p1p02 == pytest.approx(  0.13095066)
    assert result.p2p1 == pytest.approx(  6.31662479)
    assert result.r2r1 == pytest.approx( 3.15831239)
    assert result.t2t1== pytest.approx(2)

def test_normal_total_pressure_ratio():
    calculation_type = "p02/p01"
    value = .5

    flow = normal_shocks.NormalShock(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number1 == pytest.approx( 2.49754104)
    assert result.mach_number2 == pytest.approx(  0.51322553)
    assert result.p02p01 == pytest.approx(  0.50000000)
    assert result.p1p02 == pytest.approx(  0.11750394)
    assert result.p2p1 == pytest.approx(   7.11066317)
    assert result.r2r1 == pytest.approx( 3.33041726)
    assert result.t2t1== pytest.approx(2.13506674)

def test_normal_initial_static_pressure_and_final_total_pressure_ratio():
    calculation_type = "p1/p02"
    value = .5

    flow = normal_shocks.NormalShock(gamma=1.4)
    result = flow.calculate(calculation_type,value)

    assert result.mach_number1 == pytest.approx(1.0466303111521074)
    assert result.mach_number2 == pytest.approx(0.9560994967782105)
    assert result.p02p01 == pytest.approx(  0.99988055)
    assert result.p1p02 == pytest.approx(   0.49995471780815337)
    assert result.p2p1 == pytest.approx(1.1113408429260834)
    assert result.r2r1 == pytest.approx( 1.078284001136606)
    assert result.t2t1== pytest.approx(1.0306568972131949)

def test_normal_mach_number2_out_of_scope():
    gamma = 1.4
    flow = normal_shocks.NormalShock(gamma)
    lower_limit = math.sqrt((gamma - 1.0)/(2.0*gamma))  # Calculate the lower bound for M2

    # M2 greater than or equal to 1
    with pytest.raises(ValueError, match=f"M2 must be between {lower_limit} and 1"):
        flow.calculate("M2", 1.5)

    # M2 less than or equal to lower limit
    with pytest.raises(ValueError, match=f"M2 must be between {lower_limit} and 1"):
        flow.calculate("M2", 0.0)
def test_normal_pressure_ratio_out_of_scope():
    flow = normal_shocks.NormalShock(gamma=1.4)

    # p2/p1 less than or equal to 1
    with pytest.raises(ValueError, match="p2/p1 must be greater than 1"):
        flow.calculate("p2/p1", 0.9)
def test_normal_density_ratio_out_of_scope():
    gamma = 1.4
    flow = normal_shocks.NormalShock(gamma)
    upper_limit = (gamma + 1)/ (gamma - 1)  # Calculate the upper bound for rho2/rho1

    # rho2/rho1 greater than upper limit
    with pytest.raises(ValueError, match=f"rho2/rho1 must be between 1 and {upper_limit}"):
        flow.calculate("rho2/rho1", 10)

    # rho2/rho1 less than or equal to 1
    with pytest.raises(ValueError, match=f"rho2/rho1 must be between 1 and {upper_limit}"):
        flow.calculate("rho2/rho1", 0.9)
def test_normal_temperature_ratio_out_of_scope():
    flow = normal_shocks.NormalShock(gamma=1.4)

    # T2/T1 less than or equal to 1
    with pytest.raises(ValueError, match="T2/T1 must be greater than 1"):
        flow.calculate("T2/T1", 0.8)
def test_normal_total_pressure_ratio_out_of_scope():
    flow = normal_shocks.NormalShock(gamma=1.4)

    # p02/p01 greater than or equal to 1
    with pytest.raises(ValueError, match="p02/p01 must be between 0 and 1"):
        flow.calculate("p02/p01", 1.2)

    # p02/p01 less than or equal to 0
    with pytest.raises(ValueError, match="p02/p01 must be between 0 and 1"):
        flow.calculate("p02/p01", -0.5)
def test_normal_static_pressure_to_final_pressure_ratio_out_of_scope():
    flow = normal_shocks.NormalShock(gamma=1.4)
    vmax = math.pow((1.4 + 1.0) / 2.0, -1.4 / (1.4 - 1.0))  # Calculate the upper bound for p1/p02

    # p1/p02 greater than vmax
    with pytest.raises(ValueError, match=f"p1/p02 must be between 0 and {vmax}"):
        flow.calculate("p1/p02", vmax + 1)

    # p1/p02 less than or equal to 0
    with pytest.raises(ValueError, match=f"p1/p02 must be between 0 and {vmax}"):
        flow.calculate("p1/p02", -1)
def test_normal_mach_number1_out_of_scope():
    flow = normal_shocks.NormalShock(gamma=1.4)

    # M1 less than or equal to 1
    with pytest.raises(ValueError, match="Mach number must be greater than 1"):
        flow.calculate("M1", 0.9)
def test_normal_invalid_gamma():
    with pytest.raises(ValueError, match="gamma must be greater than 1"):
        flow = normal_shocks.NormalShock(gamma=.9)
        flow.calculate("M1", 2.0)
