import sys

def my_center(s, width):
    """
    自定义居中：将字符串 s 填充到指定宽度
    如果额外空格数为奇数，则将多出的空格放到左侧，
    例如: my_center("abc", 4) 返回 " abc" 而非 "abc ".
    """
    total = width - len(s)
    left = (total + 1) // 2   # 多出的空格优先放左边
    right = total - left
    return " " * left + s + " " * right

def build_row(cells, widths, sep="|"):
    """
    将各单元格内容用自定义居中函数 my_center 根据各自固定宽度居中，
    然后用指定分隔符 (默认 "|" ) 拼接成一行。
    """
    row_cells = [my_center(cell, width) for cell, width in zip(cells, widths)]
    return sep.join(row_cells)

def build_dashed_row(widths, sep="+"):
    """
    根据每列宽度生成一行虚线，
    每个单元格用相应数量的 "-" 组成，列间用 sep 拼接。
    """
    cells = ['-' * w for w in widths]
    return sep.join(cells)

def format_binary_field(value, bits):
    """
    将数值 value 转为指定位数的二进制字符串（补0），
    并在各二进制位之间插入一个空格。结果长度为 2*n - 1 。
    """
    bin_str = format(value, f'0{bits}b')
    return ' '.join(bin_str)

def main():
    if len(sys.argv) < 2:
        print("Usage: python riscv_instr_parser.py <32-bit hex number>")
        sys.exit(1)
    
    # 解析输入，允许 0x 前缀或直接输入16进制数字
    hex_input = sys.argv[1].strip()
    if hex_input.lower().startswith("0x"):
        hex_input = hex_input[2:]
    try:
        instr = int(hex_input, 16)
    except ValueError:
        print("输入的不是有效的 16 进制数！")
        sys.exit(1)
    if instr >= (1 << 32):
        print("输入数字超过 32 位！")
        sys.exit(1)
    
    label_width = 8  # 左侧标签宽度

    # -------------------------
    # 第一部分：标准字段（RISC-V 常见格式）
    # 字段定义：(表头, 起始位, 结束位, 位数)
    standard_fields = [
        ("31:25", 31, 25, 7),
        ("24:20", 24, 20, 5),
        ("19:15", 19, 15, 5),
        ("14:12", 14, 12, 3),
        ("11:7", 11, 7, 5),
        ("6:0", 6, 0, 7),
    ]
    
    std_headers = []
    std_bin_strs = []
    std_hexdec = []
    std_widths = []
    for header, start, end, bits in standard_fields:
        mask = (1 << (start - end + 1)) - 1
        value = (instr >> end) & mask
        std_headers.append(header)
        std_bin_strs.append(format_binary_field(value, bits))
        std_hexdec.append(f"0x{value:X},{value}")
        # 默认宽度按公式：(2*bits - 1) + 2
        w = (bits * 2 - 1) + 2
        # 对标准字段，"6:0" 固定宽度为 14
        if header == "6:0":
            w = 14
        std_widths.append(w)
    
    # 构造标准部分的各行
    # 第1行：标题，左侧标签空白
    row1 = " " * label_width + "|" + build_row(std_headers, std_widths)
    # 第2行：虚线
    row2 = "-" * label_width + "+" + build_dashed_row(std_widths)
    # 第3行：二进制显示行
    row3 = " " * label_width + "|" + build_row(std_bin_strs, std_widths)
    # 第4行：虚线
    row4 = row2
    # 第5行：hex,dec 行
    row5 = "hex,dec".ljust(label_width) + "|" + build_row(std_hexdec, std_widths)
    # 第6行：虚线
    row6 = row2

    # -------------------------
    # 第二部分：自定义字段划分
    # 合并 31:25 与 24:20 为 "31:20"，其余字段依次为 19:15, 14:12, 11:7, 6:0
    custom_fields = [
        ("31:20", 31, 20, 12),
        ("19:15", 19, 15, 5),
        ("14:12", 14, 12, 3),
        ("11:7", 11, 7, 5),
        ("6:0", 6, 0, 7),
    ]
    cust_hexdec = []
    cust_widths = []
    for header, start, end, bits in custom_fields:
        mask = (1 << (start - end + 1)) - 1
        value = (instr >> end) & mask
        cust_hexdec.append(f"0x{value:X},{value}")
        # 默认宽度计算同上
        w = (bits * 2 - 1) + 2
        # 对自定义字段，如果 header 为 "31:20"，固定宽度为 27；如果 header 为 "6:0"，固定为 14
        if header == "31:20":
            w = 27
        elif header == "6:0":
            w = 14
        cust_widths.append(w)
    
    row7 = "hex,dec".ljust(label_width) + "|" + build_row(cust_hexdec, cust_widths)
    
    # 输出所有行
    print(row1)
    print(row2)
    print(row3)
    print(row4)
    print(row5)
    print(row6)
    print(row7)

if __name__ == "__main__":
    main()
