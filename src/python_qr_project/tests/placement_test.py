from ..qrcode.placement import QR_matrix

import numpy as np
import numpy.testing as npt


class TestPlacement:
    def setup_method(self):
        self.data_v1 = (
            "0001010100000000000111111111011100111110101011000111010101011100000011101010001010100000000000111100010101000000000001111111110111001111101010110001110101010111000000111010100000000000111111111011100111110101"
        )
        self.data_v2 = (
            "00010101000001111111101111111101110011111010101100011101010101110000001110101000101010000000001111111110111001111101010110001110101010111000000111010100000000000111111111011100111110101111000101010000001111111110111001111101010110001110101010111000000111010100000000000111111111011100111110101111111110111001111101010110001110101010111000000111010100010101001"
        )
        
        # v1 matrix
        qrv1 = QR_matrix(data=self.data_v1, version=1)
        self.matrix1 = qrv1.populate_matrix()

        # v2 matrix
        qrv2 = QR_matrix(data=self.data_v2, version=2)
        self.matrix2 = qrv2.populate_matrix()


        self.finder = [
            [4, 4, 4, 4, 4, 4, 4],
            [4, 3, 3, 3, 3, 3, 4],
            [4, 3, 4, 4, 4, 3, 4],
            [4, 3, 4, 4, 4, 3, 4],
            [4, 3, 4, 4, 4, 3, 4],
            [4, 3, 3, 3, 3, 3, 4],
            [4, 4, 4, 4, 4, 4, 4],
        ]

        self.alignment = [
            [4, 4, 4, 4, 4],
            [4, 3, 3, 3, 4],
            [4, 3, 4, 3, 4],
            [4, 3, 3, 3, 4],
            [4, 4, 4, 4, 4],
        ]

        self.expected_v1 = [
            [4, 4, 4, 4, 4, 4, 4, 3, 2, 0, 1, 1, 1, 3, 4, 4, 4, 4, 4, 4, 4],
            [4, 3, 3, 3, 3, 3, 4, 3, 2, 0, 1, 1, 1, 3, 4, 3, 3, 3, 3, 3, 4],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 0, 1, 0, 0, 3, 4, 3, 4, 4, 4, 3, 4],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 1, 1, 1, 1, 3, 4, 3, 4, 4, 4, 3, 4],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 0, 0, 1, 0, 3, 4, 3, 4, 4, 4, 3, 4],
            [4, 3, 3, 3, 3, 3, 4, 3, 2, 1, 0, 1, 1, 3, 4, 3, 3, 3, 3, 3, 4],
            [4, 4, 4, 4, 4, 4, 4, 3, 4, 3, 4, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4],
            [3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3],
            [2, 2, 2, 2, 2, 2, 4, 2, 2, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 0, 1, 1, 1, 1, 3, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 1, 4, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 4, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
            [3, 3, 3, 3, 3, 3, 3, 3, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 4, 4, 3, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [4, 3, 3, 3, 3, 3, 4, 3, 2, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
            [4, 3, 3, 3, 3, 3, 4, 3, 2, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            [4, 4, 4, 4, 4, 4, 4, 3, 2, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        ]

        self.expected_v2 = [
            [4, 4, 4, 4, 4, 4, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 1, 3, 4, 4, 4, 4, 4, 4, 4],
            [4, 3, 3, 3, 3, 3, 4, 3, 2, 0, 0, 1, 1, 0, 0, 0, 1, 3, 4, 3, 3, 3, 3, 3, 4],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 1, 1, 1, 0, 0, 0, 0, 1, 3, 4, 3, 4, 4, 4, 3, 4],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 0, 1, 1, 0, 0, 0, 1, 1, 3, 4, 3, 4, 4, 4, 3, 4],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 0, 1, 1, 0, 0, 0, 0, 0, 3, 4, 3, 4, 4, 4, 3, 4],
            [4, 3, 3, 3, 3, 3, 4, 3, 2, 0, 1, 1, 0, 1, 1, 0, 0, 3, 4, 3, 3, 3, 3, 3, 4],
            [4, 4, 4, 4, 4, 4, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4],
            [3, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0, 1, 1, 1, 1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3],
            [2, 2, 2, 2, 2, 2, 4, 2, 2, 0, 0, 1, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 0, 0, 1, 1, 1, 3, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 4, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 0, 1, 3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 1, 3, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 1, 1, 0, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 4, 1, 1, 0, 1, 0, 0, 1, 0, 1, 4, 4, 4, 4, 4, 1, 1, 1, 1],
            [3, 3, 3, 3, 3, 3, 3, 3, 4, 1, 1, 1, 1, 1, 0, 1, 4, 3, 3, 3, 4, 0, 0, 1, 1],
            [4, 4, 4, 4, 4, 4, 4, 3, 2, 0, 1, 1, 0, 1, 1, 0, 4, 3, 4, 3, 4, 1, 0, 1, 0],
            [4, 3, 3, 3, 3, 3, 4, 3, 2, 1, 0, 1, 1, 0, 1, 1, 4, 3, 3, 3, 4, 1, 1, 0, 0],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 1, 1, 1, 1, 0, 0, 0, 4, 4, 4, 4, 4, 1, 0, 0, 0],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
            [4, 3, 4, 4, 4, 3, 4, 3, 2, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
            [4, 3, 3, 3, 3, 3, 4, 3, 2, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0],
            [4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        ]


    def test_qrcode_matrix_size(self):
        # v1 size
        assert self.matrix1.shape == (21, 21) 
        # v2 size
        assert self.matrix2.shape == (25, 25)

    
    def test_finder_patterns(self):
        # Top left finder v1
        npt.assert_array_equal(self.matrix1[0:7, 0:7], self.finder)
        # Top right finder v2
        npt.assert_array_equal(self.matrix2[0:7, -7:], self.finder)
        # Bottom left finder v2
        npt.assert_array_equal(self.matrix2[-7:, 0:7], self.finder)


    def test_separator(self):
        # Top left seperator v1
        npt.assert_array_equal(self.matrix1[0:8, 7], np.full(8, 3))
        npt.assert_array_equal(self.matrix1[7, 0:8], np.full(8, 3))
        # Top right separator v1
        npt.assert_array_equal(self.matrix1[0:8, -8], np.full(8, 3))
        npt.assert_array_equal(self.matrix1[7, -8:], np.full(8, 3))
        # Bottom left separator v2
        npt.assert_array_equal(self.matrix2[-8:, 7], np.full(8, 3))
        npt.assert_array_equal(self.matrix2[-8, 0:8], np.full(8, 3))


    def test_alignment(self):
        region = self.matrix2[16:21, 16:21]
        npt.assert_array_equal(region, self.alignment)

    
    def test_timing_patterns(self):
        size1 = self.matrix1.shape[0]
        size2 = self.matrix2.shape[0]
        row_range = range(8, size1 - 8) # Vertical timing for v1
        col_range = range(8, size2 - 8) # Horizontal timing for v2

        vertical_timing = ''.join(str(int(self.matrix1[6][r])) for r in row_range) # v1
        horizontal_timing = ''.join(str(int(self.matrix2[c][6])) for c in col_range) #v2

        # Example timing pattern
        expected = "434343434343434"

        assert vertical_timing in expected # v1
        assert horizontal_timing in expected # v2


    def test_reserved_areas(self):
        # Test dark squares
        assert self.matrix1[13][8] == 4
        assert self.matrix2[17][8] == 4

        # Top left format info v1
        npt.assert_array_equal(self.matrix1[0:6, 8], np.full((6,), 2))
        npt.assert_array_equal(self.matrix1[7:9, 8], np.full((2,), 2))
        npt.assert_array_equal(self.matrix1[8, 0:6], np.full((6,), 2))
        npt.assert_array_equal(self.matrix1[8, 7:9], np.full((2,), 2))

        # Top right format info v2
        npt.assert_array_equal(self.matrix2[8, -8:], np.full((8,), 2))

        # Bottom left format info v2
        npt.assert_array_equal(self.matrix2[-7:, 8], np.full((7,), 2))

    def test_final_matrix(self):
        npt.assert_array_equal(self.matrix1, self.expected_v1)
        npt.assert_array_equal(self.matrix2, self.expected_v2)
        