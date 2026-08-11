# QR Code Generator

> **USER WARNING: NEVER SCAN A QR CODE FROM AN UNTRUSTED SOURCE.**

This application was created with guidance from [Thonky's QR Code Tutorial](https://www.thonky.com/qr-code-tutorial/).

## Description of Functionality

This application creates a QR code from arbitrary user input and is capable of generating Version 1 and Version 2 QR codes.

Input data is converted into byte-mode data and encoded into a bitstream containing mode indicators and a character count.

Reed-Solomon error correction codewords are generated at one of four levels:

- Low (L)
- Medium (M)
- Quartile (Q)
- High (H)

The error correction codewords are appended to the encoded data before the complete bitstream is structured and mapped into the QR code matrix.

The QR matrix is constructed with the required structural components, including:

- Finder patterns
- Separators
- Alignment patterns
- Timing patterns
- Reserved areas for format information
- The dark module

Masking patterns are then applied to the QR matrix to reduce large areas of a single colour and improve the readability of the QR code by scanners.

Format information is generated containing the selected error correction level and masking pattern. This information is then placed within the matrix to assist QR code decoding.

The completed QR code is converted into an image and displayed below the user input field.

## My Contributions

This was a collaborative group project. My primary contributions focused on the QR matrix construction and formatting stages of the generation pipeline.

I contributed to the implementation of:

- **QR Matrix Placement** – Implemented the placement of finder patterns, separators, alignment patterns, timing patterns, reserved format-information areas and the dark module within the QR matrix.
- **Format Information** – Implemented the generation and placement of QR format information, including error-correction level and masking pattern data.
- **Testing** – Developed and contributed to automated tests for the QR placement and formatting components.
- **Integration** – Integrated all components with the wider QR generation pipeline using Git-based version control.

## Installation

**Supported operating systems:** Windows and Linux

### Windows

Install Python using Windows Package Manager:

```bash
winget install python3
```

Close and reopen the terminal, then create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the project and development dependencies:

```bash
pip install .[dev]
```

After the initial setup, activate the virtual environment before running the application:

```bash
.venv\Scripts\activate
```





