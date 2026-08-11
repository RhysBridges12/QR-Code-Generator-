from ..qrcode import Qrcode

import pytest


class TestAnalysis:
    # Ensures numeric mode is detected
    def test_numeric(self):
        code = Qrcode("1234567890", generate_code=False)
        code.analyse()
        assert code.data_modes[0] == Qrcode.Mode.NUMERIC

    # Ensures alphanumeric mode is detected
    def test_alphanumeric(self):
        code = Qrcode("1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ", generate_code=False)
        code.analyse()
        assert code.data_modes[0] == Qrcode.Mode.ALPHANUMERIC

    def test_alphanum_lowers_become_byte(self):
        code = Qrcode("1234567890abcdefghijklmnopqrstuvwxyz", generate_code=False)
        code.analyse()
        assert code.data_modes[0] == Qrcode.Mode.BYTE

    # Ensures kanji mode is detected
    def test_kanji(self):
        code = Qrcode("今日は", generate_code=False)
        code.analyse()
        assert code.data_modes[0] == Qrcode.Mode.KANJI

    # Ensures byte mode is detected
    def test_byte(self):
        code = Qrcode("This is bytemode text: ;&$", generate_code=False)
        code.analyse()
        assert code.data_modes[0] == Qrcode.Mode.BYTE

    # Ensures eci (defaulting to utf-8) mode is detected
    def test_extended_channel_interpretation(self):
        code = Qrcode("This is extended channel text: ˇ", generate_code=False)
        code.analyse()
        assert code.data_modes[0] == Qrcode.Mode.EXTENDED_CHANNEL_INTERPRETATION

    # ensures that dropped char check works and that eci charset change works
    def test_invalid_chars(self):
        # force eci to use more limited encoding to check the edge
        code = Qrcode("utf-8 string ˇ", generate_code=False, eci_charset="iso-8859-1")
        with pytest.raises(TypeError):
            code.analyse()

    # ensure dropping chars option works
    def test_invalid_chars_with_dropping(self):
        # force eci to use more limited encoding to check the edge
        code = Qrcode(
            "utf-8 string ˇ",
            generate_code=False,
            eci_charset="iso-8859-1",
            allow_dropping_chars=True,
        )

        code.analyse()
