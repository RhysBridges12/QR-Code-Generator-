def data_encode(self):
    """
    Determines the minimum version to use for a qrcode for self.data.
    Also encoded self.data in the selected data mode, self.data_mode.
    """
    self.data_char_counts = list(map(lambda d: len(d), self.data))
    self.ec_level = self.args["error_correction_level"]
    # Do not know how to implement this to support multi-type codes
    self.version = None
    for version in self.versions:
        if (
            self.data_char_counts[0]
            <= version.levels[self.args["error_correction_level"]][self.data_modes[0]]
        ):
            self.version = version
            break

    if self.version is None:
        raise NotImplementedError(
            f"No suitable qr code version found for data with length {self.data_char_counts[0]} chars. Max implementation is at {self.versions[-1].levels[self.args['error_correction_level']][self.data_modes[0]]} chars"
        )

    self.character_count_bitseq_lengths = []
    for length, mode in zip(self.data_char_counts, self.data_modes):
        self.character_count_bitseq_lengths.append(
            mode.character_count_indicator_length[int(self.version.version_size.value)]
        )

    self.character_count_indicators = []
    for count, indicator_length in zip(
        self.data_char_counts, self.character_count_bitseq_lengths
    ):
        self.character_count_indicators.append(format(count, f"0{indicator_length}b"))

    self.encoded_data = []
    for data, data_mode in zip(self.data, self.data_modes):
        match data_mode:
            case self.Mode.NUMERIC:
                self.encoded_data.append(encode_numeric(data))
            case self.Mode.ALPHANUMERIC:
                self.encoded_data.append(encode_alphanumeric(data))
            case self.Mode.BYTE:
                self.encoded_data.append(encode_byte(data, self.args["byte_mode_utf8"]))
            case self.Mode.KANJI:
                self.encoded_data.append(encode_kanji(data))
            case _:
                pass
    self.encoded_data = sum(self.encoded_data, [])

    self.total_data_bits = (
        self.version.total_data_codewords[self.args["error_correction_level"]] * 8
    )
    self.raw_data_bit_string = "".join(
        [
            self.data_mode_indicators[0],
            self.character_count_indicators[0],
            *self.encoded_data,
        ]
    )

    # Add max length 4 terminator to end of bit sequence
    if len(self.raw_data_bit_string) < self.total_data_bits:
        self.raw_data_bit_string += (
            min(self.total_data_bits - len(self.raw_data_bit_string), 4) * "0"
        )

    # if bit sequence is not a multiple of 8, add 0s to make it so
    if len(self.raw_data_bit_string) % 8 != 0:
        self.raw_data_bit_string += (8 - (len(self.raw_data_bit_string) % 8)) * "0"

    # Add final pad bytes
    while len(self.raw_data_bit_string) != self.total_data_bits:
        self.raw_data_bit_string += "11101100"
        if len(self.raw_data_bit_string) != self.total_data_bits:
            self.raw_data_bit_string += "00010001"


@staticmethod
def encode_numeric(data):
    """
    Encode a numeric input string into the binary format.
    Assumes that previous operations have sanitised input data and it is valid.

    Parameters
    ----------
    data : str
      Numeric input string.

    Returns
    -------
    { str }
      Binary string of encoded data.
    """
    group_length = 3
    groups = [data[i : i + group_length] for i in range(0, len(data), group_length)]
    binary_groups = []
    for group in groups:
        match len(group):
            case 3:
                binary_groups.append(format(int(group), "010b"))
            case 2:
                binary_groups.append(format(int(group), "07b"))
            case 1:
                binary_groups.append(format(int(group), "04b"))

    return binary_groups


@staticmethod
def encode_alphanumeric(data):
    """
    Encode an alphanumeric input string into the binary format.
    Assumes that previous operations have sanitised input data and it is valid.

    Parameters
    ----------
    data : str
      Alphaumeric input string.

    Returns
    -------
    { str }
      Binary string of encoded data.
    """
    group_length = 2
    groups = [data[i : i + group_length] for i in range(0, len(data), group_length)]
    binary_groups = []
    representations = dict(map(lambda t: (str(t[0]), t[1]), enumerate(range(10)))) | {
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
        "G": 16,
        "H": 17,
        "I": 18,
        "J": 19,
        "K": 20,
        "L": 21,
        "M": 22,
        "N": 23,
        "O": 24,
        "P": 25,
        "Q": 26,
        "R": 27,
        "S": 28,
        "T": 29,
        "U": 30,
        "V": 31,
        "W": 32,
        "X": 33,
        "Y": 34,
        "Z": 35,
        " ": 36,
        "$": 37,
        "%": 38,
        "*": 39,
        "+": 40,
        "-": 41,
        ".": 42,
        "/": 43,
        ":": 44,
    }

    odd_num_of_char = (len(groups[-1]) % 2) != 0
    print(groups)
    if odd_num_of_char:
        last = groups.pop(len(groups) - 1)

    for i, j in groups:
        binary_groups.append(
            format((representations[i] * 45) + representations[j], "011b")
        )

    if odd_num_of_char:
        binary_groups.append(format(representations[last], "06b"))

    return binary_groups


@staticmethod
def encode_byte(data, byte_mode_utf8):
    """
    Encode a byte input string into the binary format.
    Assumes that previous operations have sanitised input data and it is valid.

    Parameters
    ----------
    data : str
      Byte input string.

    Returns
    -------
    { str }
      Binary string of encoded data.
    """
    converted_data = (
        data.encode("iso-8859-1") if not byte_mode_utf8 else data.encode("utf-8")
    )
    binary_chars = []
    for char in converted_data:
        print(char)
        binary_chars.append(format(int(char), "08b"))
    return binary_chars


@staticmethod
def encode_kanji(data):
    """
    Encode a kanji input string into the binary format.
    Assumes that previous operations have sanitised input data and it is valid.

    Parameters
    ----------
    data : str
      Kanji input string.

    Returns
    -------
    { str }
      Binary string of encoded data.
    """
    converted_data = data.encode("shift_jis")
    double_bytes = [x for x in zip(converted_data[::2], converted_data[1::2])]
    double_bytes = list(map(lambda b: int((b[0] << 8) | b[1]), double_bytes))
    binary_chars = []
    for char in double_bytes:
        offset_char = 0
        if char >= 0x8140 and char <= 0x9FFC:
            offset_char = char - 0x8140
        elif char >= 0xE040 and char <= 0xEBBF:
            offset_char = char - 0xC140
        else:
            # Character is out of qr code jis range, cannot include it
            print(f"Character {char} was passed")
            pass
        msb, lsb = offset_char.to_bytes(2, "big")
        msb *= 0xC0
        msb += lsb
        binary_chars.append(format(msb, "013b"))
    return binary_chars


@staticmethod
def encode_eci(data):
    """
    Encode an arbitrary input string into the ECI binary format.
    Assumes that previous operations have sanitised input data and it is valid.
    TODO implementatoin of this for utf-8 chars that cannot be represented in bytemode.

    Parameters
    ----------
    data : str
      Text input string.

    Returns
    -------
    { str }
      Binary string of encoded data.
    """
    raise NotImplementedError("Eci encoding not implemented yet")
