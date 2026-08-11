def structure_message(self):
    REMAINDER_BITS = {
        1: 0,
        2: 7,
    }

    data_codewords = self.data_padded
    ecc_codewords = list(self.ecc) if isinstance(self.ecc, tuple) else self.ecc
    version = self.version.number

    # Interleave data codewords with ecc codewords :
    interleaved = data_codewords + ecc_codewords
    final_bit_string = ''.join(f'{byte:08b}' for byte in interleaved)

    # Add required remainder bits :
    if version in REMAINDER_BITS:
        final_bit_string += '0' * REMAINDER_BITS[version]
    else:
        raise ValueError("Error : Remainder bit count undefined")

    self.final_bit_string = final_bit_string
    