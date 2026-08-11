def ecc_encode(self):
    """
    Encodes input data with Reed-Solomon error correction Version 1-L or 2-L.  
    """
    data = int(self.raw_data_bit_string, 2).to_bytes(len(self.raw_data_bit_string) // 8, byteorder='big')
    version = self.version.number
    # Define parameters for QR Code versions (Version : {data codewords, ECC codewords})
    qr_versions = {
        1: {"data_len": 19, "ecc_len": 7},
        2: {"data_len": 34, "ecc_len": 10}
    }

    # Check if version is supported
    if version not in qr_versions:
        raise ValueError("Only versions 1 and 2 (Level L) are supported.")

    # Extract parameters for selected version
    data_len = qr_versions[version]["data_len"]
    ecc_len = qr_versions[version]["ecc_len"]

    # QR codes use Galois Fields (GF) with the primitive polynomial x^8 + x^4 + x^3 + x^2 + 1 (0x11D)
    GF256_PRIM = 0x11D

    # Lookup tables for fast GF(256) arithmetic
    EXP_TABLE = [0] * 512  # Extended, prevents numbers from reseting to 1
    LOG_TABLE = [0] * 256

    # Initialize logarithm and exponent tables for GF
    def init_tables():
        x = 1
        for i in range(255):
            EXP_TABLE[i] = x
            LOG_TABLE[x] = i
            x <<= 1  # times by 2 in GF
            if x & 0x100:  # If overflow (>= 256), reduce using primitive polynomial
                x ^= GF256_PRIM
        for i in range(255, 512):
            EXP_TABLE[i] = EXP_TABLE[i - 255]  # Copy to support larger indices

    init_tables()

    def gf_mul(x, y):
        """Times a pair of numbers in Galois Field using log/exp tables"""
        if x == 0 or y == 0:
            return 0
        return EXP_TABLE[LOG_TABLE[x] + LOG_TABLE[y]]

    def poly_mul(p, q):
        """times two polynomials over GF"""
        res = [0] * (len(p) + len(q) - 1)
        for i in range(len(p)):
            for j in range(len(q)):
                res[i + j] ^= gf_mul(p[i], q[j])  # XOR = addition in GF
        return res

    def rs_generator_poly(nsym):
        """Build the generator polynomial"""
        g = [1]
        for i in range(nsym):
            g = poly_mul(g, [1, EXP_TABLE[i]])
        return g

    def rs_encode_msg(msg, nsym):
        """Encodes the message using Reed-Solomon"""
        gen = rs_generator_poly(nsym)
        msg_out = msg + [0] * nsym  # Append ECC space
        for i in range(len(msg)):
            coef = msg_out[i]
            if coef != 0:
                for j in range(len(gen)):
                    msg_out[i + j] ^= gf_mul(gen[j], coef)
        return msg + msg_out[-nsym:]  # Append the last nsym ECC bytes

    # Checks data against the allowed limit
    if len(data) > data_len:
        raise ValueError(f"Too much data for QR Code Version {version}-L (max {data_len} bytes)")

    # Pad input data to required number of data codewords
    data_padded = list(data) + [0] * (data_len - len(data))

    # Generate full codeword list
    full_codewords = rs_encode_msg(data_padded, ecc_len)

    self.data_padded = data_padded          # 19 or 34 bytes depending on version 1 or version 2
    self.ecc = full_codewords[-ecc_len:]   # Last 7 or 10 ECC bytes
    self.codewordsful = full_codewords      # Combined list of 26 or 44 codewords