import numpy as np

class QR_matrix:
    # Static 7x7 pattern used in top left, top right and bottom left
    # of QR code.
    FINDER_PATTERN = [
        [4, 4, 4, 4, 4, 4, 4],
        [4, 3, 3, 3, 3, 3, 4],
        [4, 3, 4, 4, 4, 3, 4],
        [4, 3, 4, 4, 4, 3, 4],
        [4, 3, 4, 4, 4, 3, 4],
        [4, 3, 3, 3, 3, 3, 4],
        [4, 4, 4, 4, 4, 4, 4],
    ]

    # Static 5x5 pattern used for QR code alignment
    ALIGNMENT_PATTERN = [
        [4, 4, 4, 4, 4],
        [4, 3, 3, 3, 4],
        [4, 3, 4, 3, 4],
        [4, 3, 3, 3, 4],
        [4, 4, 4, 4, 4],
    ]


    def __init__ (self, data: str, version: int):
        """
        Initialise QR matrix with the structured final message and
        version, create the empty matrix.

        Args:
            data (str): String of 0 and 1's
            version (int): QR code version, 1 or 2 in this implementation
        """
        self.data = data
        self.version = version
        self.size = 21 if version == 1 else 25
        self.matrix = np.full((self.size, self.size), -1) # create matrix of -1.
        # Coordinates for alignment pattern for v2 code.
        self.align_pat = (6, 18) if version == 2 else (0, 0)


    def place_finder(self):
        """
        Place finder patterns in top left, top right and bottom left of QR code
        """
        for r in range(7):
            for c in range(7):
                self.matrix[r][c] = self.FINDER_PATTERN[r][c]
                self.matrix[r][self.size - c - 1] = self.FINDER_PATTERN[r][c]
                self.matrix[self.size - r - 1][c] = self.FINDER_PATTERN[r][c]
    
    
    def place_seperator(self):
        """
        Add white border (0's) around inside edges of finders
        """
        self.matrix[0:8, 7] = 3 # Top left seperator
        self.matrix[7, 0:8] = 3
    
        self.matrix[0:8, self.size - 8] = 3 # Top right seperator
        self.matrix[7, self.size - 8:self.size] = 3
    
        self.matrix[self.size - 8:self.size, 7] = 3 # Bottom left seperator
        self.matrix[self.size - 8, 0:8] = 3


    def check_location(self, row, col):
        """
        See if 5x5 region with top left position (row, col)
        is completely free for an an alignment pattern

        Args:
            row: Starting row
            col: Starting column
        
        Returns:
            True if 5x5 is free or false if not
        """
        for r in range(5):
            for c in range(5):
                if self.matrix[row + r][col + c] == -1:
                    continue
                else:
                    return False
        return True


    def place_alignment(self):
        """
        Place alignment patterns in available locations

        """
        a, b = self.align_pat

        locations = [ # Create coordinates of locations 
            (a - 2, a - 2),
            (a - 2, b - 2),
            (b - 2, a - 2),
            (b - 2, b - 2),
        ]

        # Do for all locations
        for (row, col) in locations:
            if self.check_location(row, col):
                for r in range(5):
                    for c in range(5):
                        # Paste alignment pattern in
                        self.matrix[row + r][col + c] = self.ALIGNMENT_PATTERN[r][c]


    def place_timings(self):
        """
        Place timing patterns into 6th row and column
        Helps QR code to determine orientation
        """
        for c in range(self.size):
            # Only do in available spaces:
            if self.matrix[6][c] == -1 and self.matrix[c][6] == -1:
                # Alternate 0 and 1's
                self.matrix[6][c], self.matrix[c][6] = [4, 4] if c % 2 == 0 else [3, 3]
    

    def place_reserved(self):
        """
        Reserve areas of the QR code for dark module and format information.
        2 is used for now as a placeholder.
        """
        self.matrix[(4 * self.version) + 9][8] = 4 # Dark module
        
        # Bottom left format info
        self.matrix[self.size - 7:self.size, 8] = 2
        
        # Top left format info
        self.matrix[0:6, 8] = 2
        self.matrix[7:9, 8] = 2
        self.matrix[8, 0:6] = 2
        self.matrix[8, 7:9] = 2
    
        # Top right format info
        self.matrix[8, self.size - 8:self.size] = 2


    def place_data(self):
        """
        Places bit stream into matrix in a zigzag pattern,
        filled spaces are skipped.
        """
        index = 0
        for col in range(self.size - 1, -1, -2): # For each pair of columns:
            if ((self.size - 1 - col) // 2) % 2 == 0:
                rows = range(self.size - 1, -1, -1) # size -> 0
            else:
                rows = range(self.size) # 0 -> size
            for row in rows:
                for i in [0, 1]: # For both columns:
                    column = col - i
                    if index < len(self.data): # If data stream not empty:
                        if self.matrix[row][column] == -1 and index < len(self.data):
                            self.matrix[row][column] = self.data[index]
                            index += 1 # Next data bit
                            
                            
    def populate_matrix(self):
        """
        Calls all functions to add data to the matrix.
        Adds finders, seperators, aligners, timings and reserved areas.
        """
        self.place_finder()
        self.place_seperator()
        self.place_alignment()
        self.place_timings()
        self.place_reserved()
        self.place_data()
        
        return self.matrix

    def print_mat(self):
        """
        Visualises the matrix as a string.
        # = 1, . = 0
        """
        lines = []
        for row in self.matrix:
            line = " ".join(
                "#" if val == 1 else
                "." if val == 0 else
                "F" if val == 2 else
                "." if val == 3 else
                "#" if val == 4 else
                " " for val in row
            )
            lines.append(line)
        return "\n".join(lines)


def place_modules(self):
    """
    Returns the matrix once all modules are placed
    called from QRCode.py 
    """    
    matrix = QR_matrix(data=self.final_bit_string, version=self.version.number)
    matrix.populate_matrix()
    
    self.matrix = matrix.matrix
    self.print_matrix = matrix.print_mat()
    
