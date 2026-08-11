import numpy as np
from .version import Error_Correction_Level

FORMAT_INFO_MASK = 0b101010000010010  # XOR mask for format info
FORMAT_GENERATOR = 0b10100110111      # What to divide error correction by

EC_LEVEL_BITS = {  # 2 bits for the EC level
    Error_Correction_Level.L: 0b01,
    Error_Correction_Level.M: 0b00,
    Error_Correction_Level.Q: 0b11,
    Error_Correction_Level.H: 0b10
}

def change_reserved_areas(matrix):
    """
    Changes all reserved areas to light and dark modules.
    """
    new_matrix = np.array(matrix) 
    new_matrix[new_matrix == 3] = 0 # 3 = 0
    new_matrix[new_matrix == 4] = 1 # 4 = 1
    return new_matrix



def pad_generator(format_bits):
    """
    Pads the generator string with 0's so length matches
    the format string
    """
    # Find difference in length
    padding = format_bits.bit_length() - FORMAT_GENERATOR.bit_length()
    return FORMAT_GENERATOR << padding  # Add that many 0's


def generate_ec_string(format_bits):
    """
    Creates the 10 error correction bits
    """
    while format_bits.bit_length() > 10:  # Do until length less than 10
        padded_generator = pad_generator(format_bits)
        format_bits = format_bits ^ padded_generator  # XOR format string with generator
    return format_bits


def generate_format_string(ec_level, mask_pattern):
    """
    Creates completed format string.
    Makes 5 bit string with error correction level and masking number.
    Pads format bits and appends the error correction bits.
    returns a bitstream length 15.
    """
    ec_bits = EC_LEVEL_BITS[ec_level]

    # Append mask pattern in bits to make string length 5
    format_bits = (ec_bits << 3) | mask_pattern

    padded_format_bits = (format_bits << 10)  # Add 10 zeros to right
    # Get error correction bits:
    ec_string = generate_ec_string(padded_format_bits)
    # Create 15 bit string:
    pre_mask_format_info = (format_bits << 10) | ec_string

    # XOR with mask
    final_format_info = pre_mask_format_info ^ FORMAT_INFO_MASK
    final_format_info_str = format(final_format_info, '015b')  # Pad to length 15
    return final_format_info_str


def place_format_string(matrix, format_string):
    """
    Places the format code into the qrcode matrix.
    """
    indexV = 0
    indexH = 0

    for r in range(len(matrix) - 1, -1, -1):
        # Vertical placement:
        if matrix[r][8] == 2:
            matrix[r][8] = int(format_string[indexV])  # Vertical
            indexV += 1
    # Horizontal placement:
    for c in range(len(matrix)):
        if matrix[8][c] == 2:
            matrix[8][c] = int(format_string[indexH])
            indexH += 1
    return matrix


def pad_matrix(matrix):
    """
    Adds a 4x4 white border around the QR code.
    """
    size = len(matrix)
    new_size = size + 8

    new_matrix = np.full((new_size, new_size), 0)
    for r in range(size):
        for c in range(size):
            new_matrix[r + 4][c + 4] = matrix[r][c]

    return new_matrix


def format_code(self):
    """
    Calls class to create the format string.
    Calls function to place function string into matrix.
    """
    # Create format bit string with ec level and mask pattern number
    format_string = generate_format_string(self.args["error_correction_level"], self.mask_pattern)
    self.format_string = format_string

    # Place into matrix
    binary_matrix = change_reserved_areas(self.masked)
    new_matrix = place_format_string(binary_matrix, format_string)
    padded_matrix = pad_matrix(new_matrix)  # Add border to matrix
    self.code = padded_matrix