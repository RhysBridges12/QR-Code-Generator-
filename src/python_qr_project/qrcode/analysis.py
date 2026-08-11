from enum import Enum
import re


class Mode(Enum):
    """
    Wrapper for the binary data mode indicators for each possible data mode.
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, mode_indicator, character_count_indicator_length):
        self.mode_indicator = mode_indicator
        self.character_count_indicator_length = character_count_indicator_length

    NUMERIC = int("0001", 2), [10, 12, 14]
    ALPHANUMERIC = int("0010", 2), [9, 11, 13]
    BYTE = int("0100", 2), [8, 16, 16]
    KANJI = int("1000", 2), [8, 10, 12]
    EXTENDED_CHANNEL_INTERPRETATION = int("0111", 2), [0, 0, 0]
    STRUCTURED_APPEND = int("0011", 2), [0, 0, 0]
    FNC1_IN_FIRST = int("0101", 2), [0, 0, 0]
    FNC1_IN_SECOND = int("1001", 2), [0, 0, 0]
    END_OF_MESSAGE = int("0000", 2), [0, 0, 0]


def analyse(self):
    """
    Select optimum data mode using the data contents.

    Raises
    ------
    TypeError
        The data character sequence cannot be encoded in any of the available data modes.
    """

    def is_alphanum(data):
        """
        Validate if the data contents can be encoded as an alphanum.

        Parameters
        ----------
        data : str
          Code data input string.

        Returns
        -------
        { bool }
          Whether the data can be encoded as an alphanum.
        """
        alphanum_check = re.match(
            "([0-9]|[A-Z]|[$]|[%]|[*]|[+]|[-]|[.]|[/]|[:]|[ ])+", data
        )
        return (
            alphanum_check
            and len(alphanum_check.group()) == len(data)
            and not self.args["force_byte_mode"]
        )

    def is_kanji(data):
        """
        Validate if the data contents can be encoded as kanji .

        Parameters
        ----------
        data : str
          Code data input string.

        Returns
        -------
        { bool }
          Whether the data can be encoded as an kanji.
        """
        converted_data = data.encode("shift_jis", "ignore")
        double_bytes = [x for x in zip(converted_data[::2], converted_data[1::2])]
        double_bytes = list(map(lambda b: int((b[0] << 8) | b[1]), double_bytes))
        for char in double_bytes:
            # check in range of qr code's limited jis charset
            if (
                not (char >= 0x8140 and char <= 0x9FFC)
                and not (char >= 0xE040 and char <= 0xEBBF)
                and not self.args["allow_dropping_chars"]
            ):
                return False
        return data.encode("shift_jis", "ignore").decode("shift_jis", "ignore") == data

    self.data_modes = []
    self.data_mode_indicators = []
    for i, data in enumerate(self.data):
        # check for numeric mode
        if data.isnumeric() and not self.args["force_byte_mode"]:
            self.data_modes.append(Mode.NUMERIC)

        # check for alphanumeric, not a standard charset so use regex - means we have to check for none
        elif is_alphanum(data):
            self.data_modes.append(Mode.ALPHANUMERIC)

        # Option to permit breaking spec by using utf-8 in byte mode
        elif data.encode("iso-8859-1", "ignore").decode(
            "iso-8859-1", "ignore"
        ) == data or (
            self.args["byte_mode_utf8"]
            and data.encode("utf-8", "ignore").decode("utf-8", "ignore") == data
        ):
            self.data_modes.append(Mode.BYTE)

        # Check for kanji characters - allows for use of smaller charset
        elif is_kanji(data):
            self.data_modes.append(Mode.KANJI)

        # otherwise try to encode using ECI and explicitly stating the charset - default is utf-8, but can be any
        elif (
            data.encode(self.args["eci_charset"], "ignore").decode(
                self.args["eci_charset"], "ignore"
            )
            == data
            # option to permit continuing with ECI even if some chars will be dropped at encoding
            or self.args["allow_dropping_chars"]
        ):
            self.data_modes.append(Mode.EXTENDED_CHANNEL_INTERPRETATION)
        else:  # Data didnt match any of the charsets - couldn't find a way of serialising it
            raise TypeError("Invalid input character sequence")
        self.data_mode_indicators.append(
            format(self.data_modes[i].mode_indicator, "04b")
        )
