from ..qrcode import Qrcode

import pytest


class TestDataEncoding:
    # Ensures numeric mode correctly encodes raw data
    def test_numeric(self):
        code = Qrcode("1234567890", generate_code=False)
        code.analyse()
        code.data_encode()
        assert (
            code.raw_data_bit_string
            == "00010000001010000111101101110010001100010101000000000000111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001"
        )

    # Ensures alphanumeric mode is detected
    def test_alphanumeric(self):
        code = Qrcode("1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ", generate_code=False)
        code.analyse()
        code.data_encode()
        assert (
            code.raw_data_bit_string
            == "00100001001000000010111100010001011000111001110010100001100110010101001110011010100010100101010000101010111000010110011110101110011001011111101011000101000110010101101101000010011010110010110111000001110000111010000011101100000100011110110000010001111011000001000111101100"
        )

    # Ensures kanji mode is detected
    def test_kanji(self):
        code = Qrcode("今日は", generate_code=False)
        code.analyse()
        code.data_encode()
        assert (
            code.raw_data_bit_string
            == "10000000001101001011000010111000111010000010100110100000111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001"
        )

    # Ensures byte mode is detected
    def test_byte(self):
        code = Qrcode("This is bytemode text: ;&$", generate_code=False)
        code.analyse()
        code.data_encode()
        assert (
            code.raw_data_bit_string
            == "01000001101001010100011010000110100101110011001000000110100101110011001000000110001001111001011101000110010101101101011011110110010001100101001000000111010001100101011110000111010000111010001000000011101100100110001001000000111011000001000111101100000100011110110000010001"
        )

    # Ensures eci (defaulting to utf-8) mode is detected
    @pytest.mark.skip(
        reason="Extended channel interpretation data encoding has not been implemented yet."
    )
    def test_extended_channel_interpretation(self):
        code = Qrcode("This is extended channel text: ˇ", generate_code=False)
        code.analyse()
        code.data_encode()
        assert code.raw_data_bit_string == ""
