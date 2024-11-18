import sys
sys.path.append("C:\\Compressible Fluid Calculator\\Compressible_flow_equations")

from isentropic_flow import print_hello_world

def test_print_hello_world():
    assert print_hello_world() == "Hello, World!"