# Canada Capital Gains Calculator
The goal of this project is to create a tool that:
- keeps track of the sale/purchase history of an asset (e.g. an ETF, a stock, etc.)
- and that calculates the Capital Gains resulting from all sales of this asset in a given fiscal year.

The tool uses the **Adjusted Cost Base** as the cost basis to determine the capital gains, as this is the official way to calculate capital gains in Canada.

**DISCLAIMER: This tool was built for personal use. The contributors of this project are not responsible for any misreporting of capital gains resulting from the use of this tool to prepare your tax declarations.**

## Getting Started

1. Create a virtual environment: 
    - Python 3.12.2
    - Install requirements.txt

1. Execute main.py
    - `python main.py`

### Testing

- Execute the test suite with command: 
    - `pytest`

### Playing with the samples

- Execute a sample (e.g. simple_use_case.py) with command: 
    - `python -m samples.simple_use_case`

## Authors
- Alexandre Dorais

## License 
This project is licensed under the BSD 3-Clause License - see the LICENSE.md file for details.
