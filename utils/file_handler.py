def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]
    lines = []

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                all_lines = file.readlines()

                # remove header
                for line in all_lines[1:]:
                    line = line.strip()
                    if line:
                        lines.append(line)

            return lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print("Error: File not found")
            return []

    print("Error: Unable to read file due to encoding issues")
    return []
