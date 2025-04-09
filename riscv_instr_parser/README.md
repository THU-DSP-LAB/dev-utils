# RISC-V Instruction Parser

This Python script parses a 32-bit hexadecimal RISC-V instruction and displays a formatted table that separates the instruction into its respective fields according to the RISC-V specification. In addition to showing the bit field breakdown in binary, the script also provides the corresponding hexadecimal and decimal values for each field.

## Features

- **Input Format:**  
  Accepts a 32-bit hexadecimal number either with or without a `0x` prefix.
  
- **Standard Field Breakdown:**  
  Separates the instruction into these standard fields:
  - **funct7:** Bits 31:25
  - **rs2:** Bits 24:20
  - **rs1:** Bits 19:15
  - **funct3:** Bits 14:12
  - **rd:** Bits 11:7
  - **opcode:** Bits 6:0
  
- **Custom Field Grouping:**  
  In a separate section, the script displays a custom grouping that merges bits 31:25 and 24:20 into one `31:20` field, followed by `19:15`, `14:12`, `11:7`, and `6:0`.

- **Formatted Output:**  
  Outputs a neatly formatted table with:
  - A header row showing field names.
  - A binary breakdown row with individual bit values separated by spaces.
  - Rows showing the hexadecimal and decimal representations.
  - Proper alignment of all columns using consistent field widths.

## Usage

Run the script from the command line, providing a 32-bit hexadecimal number as an argument. For example:

```bash
python riscv_instr_parser.py 0021607b
```

or

```bash
python riscv_instr_parser.py 0x0021607b
```

## Example Output

```text
        |     31:25     |   24:20   |   19:15   | 14:12 |    11:7   |     6:0      
--------+---------------+-----------+-----------+-------+-----------+--------------
        | 0 0 0 0 0 0 0 | 0 0 0 1 0 | 0 0 0 1 0 | 1 1 0 | 0 0 0 0 0 | 1 1 1 1 0 1 1
--------+---------------+-----------+-----------+-------+-----------+--------------
hex,dec |     0x0,0     |   0x2,2   |   0x2,2   | 0x6,6 |   0x0,0   |   0x7B,123   
--------+---------------+-----------+-----------+-------+-----------+--------------
hex,dec |           0x2,2           |   0x2,2   | 0x6,6 |   0x0,0   |   0x7B,123   
```
