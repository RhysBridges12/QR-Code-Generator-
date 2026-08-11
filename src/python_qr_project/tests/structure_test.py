import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from python_qr_project.qrcode.structure import structure_message

class DummyQR:
    def __init__(self, data, ecc, version_number):
        self.data_padded = data
        self.ecc = ecc
        self.version = type('Version', (), {'number': version_number})()

def test_version_1():
    obj = DummyQR(data=list(range(19)), ecc=list(range(7)), version_number=1) # 0 to 18 and 0 to 6.
    structure_message(obj)
    assert hasattr(obj, 'final_bit_string')

    # 19 data codewords + 7 ECC codewords = 26 codewords - * 8 bits = 208bits
    assert len(obj.final_bit_string) == 208
    assert set(obj.final_bit_string).issubset({'0', '1'})

def test_version_2():
    obj = DummyQR(data=list(range(34)), ecc=list(range(10)), version_number=2) # 0 to 33 and 0 to 9
    structure_message(obj)
    assert hasattr(obj, 'final_bit_string')

    #34 data codewords + 10 ECC codewords = 44 codewords. - * 8bits = 352bits + 7 remainder bits = 359 bits
    assert len(obj.final_bit_string) == 359
    assert obj.final_bit_string.endswith('0' * 7)

def test_invalid_version():
    obj = DummyQR(data=[0], ecc=[0], version_number=3)
    try:
        structure_message(obj)
        assert False # If no error is raised then the test should fail as we are expecting an error
    except ValueError:
        pass # If there is a ValueError as expected, then test passes.