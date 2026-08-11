# Wrapper class that holds all properties (python doesnt have structs)
class Qrcode:
    from .analysis import analyse, Mode
    from .data_encoding import data_encode
    from .error_correction import ecc_encode
    from .structure import structure_message
    from .placement import place_modules
    from .masking import mask
    from .formatting import format_code

    from .version import Version, Error_Correction_Level, Version_Size

    versions = Version.get_versions()

    def __init__(self, data, generate_code=True, **kwargs):
        """
        Create a qrcode metadata wrapper, using the given data.

        Parameters
        ----------
        data : str
          Data that will be the contents of the code.
        generate_code : bool, default=True
          Whether to generate the qrcode immediately upon creation of the metadata object.

        Returns
        -------
        { Qrcode }
          An instance of the Qrcode metadata wrapper class.

        """
        # theoretically this will allow for mixing modes in the future, or for structured append mode etc
        self.data = data if isinstance(data, list) else [data]

        # Default parameters for code generation: kwargs will take priority and override the defaults.
        self.args = {
            "byte_mode_utf8": False,
            "eci_charset": "utf-8",
            "allow_dropping_chars": False,
            "force_byte_mode": False,
            "error_correction_level": self.Error_Correction_Level.L,
        } | kwargs

        # Generate qrcode using self.args properties and self.data contents
        if generate_code:
            self.generate()

    # Storing intermediate steps allows for easier implementation of step-by-step display later
    def generate(self):
        if self.args["debug"]:
            print(f"The contents of the code will be:\n{self.data}\n")

        self.analyse()
        if self.args["debug"]:
            print(f"The mode for {self.data} is:\n{self.data_modes}\n")

        self.data_encode()
        if self.args["debug"]:
            print(f"The qrcode version is:\n{self.version.number}")
            print(f"The qrcode size is:\n{self.version.size}px")
            print(
                f"The qrcode indicators are :\n{self.data_mode_indicators} {self.character_count_indicators}"
            )
            print(f"The encoded data is:\n{self.raw_data_bit_string}\n")

        self.ecc_encode()

        self.structure_message()

        self.place_modules()
        if self.args["debug"]:
            print(f"Created matrix:\n{self.print_matrix}")

        self.mask()

        self.format_code()
        if self.args["debug"]:
            print(f"Format bits:\n{self.format_string}")

            print(f"Final code:\n${self.code}")
