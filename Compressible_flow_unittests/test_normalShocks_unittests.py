import sys
sys.path.append("C:\\Compressible Fluid Calculator\\Compressible_flow_calculator")
from normalHello import print_hello_world2
def test_print_hello_world2():
    assert print_hello_world2() == "hello world"