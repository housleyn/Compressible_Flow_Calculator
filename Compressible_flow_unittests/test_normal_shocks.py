import sys
sys.path.append("C:\\Compressible Fluid Calculator\\Compressible_flow_equations")
from normal_shocks import add_two_numbers 

def test_add_two_numbers():
    assert add_two_numbers(2,2) == 4