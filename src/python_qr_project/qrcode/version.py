from enum import Enum

from .analysis import Mode


class Error_Correction_Level(Enum):
    L = 0
    M = 1
    Q = 2
    H = 3


class Version_Size(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class Version:
    """
    Wrapper for metadata about a qrcode - capacities, codeword counts et al.
    """

    def __init__(self, number, levels):
        self.number = number
        self.size = (number * 4) + 17
        self.levels = levels
        if number <= 9:
            self.version_size = Version_Size.SMALL
        elif number <= 26:
            self.version_size = Version_Size.MEDIUM
        else:
            self.version_size = Version_Size.LARGE

        self.total_data_codewords = {}
        for level_key, level in levels.items():
            # Pretty sure this holds true for all
            self.total_data_codewords[level_key] = level[Mode.BYTE] + 2

    @staticmethod
    def get_versions():
        return [
            Version(
                1,
                {
                    Error_Correction_Level.L: {
                        Mode.NUMERIC: 41,
                        Mode.ALPHANUMERIC: 25,
                        Mode.BYTE: 17,
                        Mode.KANJI: 10,
                    },
                    Error_Correction_Level.M: {
                        Mode.NUMERIC: 34,
                        Mode.ALPHANUMERIC: 20,
                        Mode.BYTE: 14,
                        Mode.KANJI: 8,
                    },
                    Error_Correction_Level.Q: {
                        Mode.NUMERIC: 27,
                        Mode.ALPHANUMERIC: 16,
                        Mode.BYTE: 11,
                        Mode.KANJI: 7,
                    },
                    Error_Correction_Level.H: {
                        Mode.NUMERIC: 17,
                        Mode.ALPHANUMERIC: 10,
                        Mode.BYTE: 7,
                        Mode.KANJI: 4,
                    },
                },
            ),
            Version(
                2,
                {
                    Error_Correction_Level.L: {
                        Mode.NUMERIC: 77,
                        Mode.ALPHANUMERIC: 47,
                        Mode.BYTE: 32,
                        Mode.KANJI: 20,
                    },
                    Error_Correction_Level.M: {
                        Mode.NUMERIC: 63,
                        Mode.ALPHANUMERIC: 38,
                        Mode.BYTE: 26,
                        Mode.KANJI: 16,
                    },
                    Error_Correction_Level.Q: {
                        Mode.NUMERIC: 48,
                        Mode.ALPHANUMERIC: 29,
                        Mode.BYTE: 20,
                        Mode.KANJI: 12,
                    },
                    Error_Correction_Level.H: {
                        Mode.NUMERIC: 34,
                        Mode.ALPHANUMERIC: 20,
                        Mode.BYTE: 14,
                        Mode.KANJI: 8,
                    },
                },
            ),
        ]


"""
  Version(
      ,
      {
          Error_Correction_Level.L: {
              Mode.NUMERIC: ,
              Mode.ALPHANUMERIC: ,
              Mode.BYTE: ,
              Mode.KANJI: ,
          },
          Error_Correction_Level.M: {
              Mode.NUMERIC: ,
              Mode.ALPHANUMERIC: ,
              Mode.BYTE: ,
              Mode.KANJI: ,
          },
          Error_Correction_Level.Q: {
              Mode.NUMERIC: ,
              Mode.ALPHANUMERIC: ,
              Mode.BYTE: ,
              Mode.KANJI: ,
          },
          Error_Correction_Level.H: {
              Mode.NUMERIC: ,
              Mode.ALPHANUMERIC: ,
              Mode.BYTE: ,
              Mode.KANJI: ,
          },
      },
  ),
"""
