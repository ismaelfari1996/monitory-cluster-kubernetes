def print_table(rows, headers):
    rows = [[str(cell) for cell in row] for row in rows]
    headers = [str(h) for h in headers]

    col_widths = [len(h) for h in headers]

    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

    print(sep)
    print("| " + " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers))) + " |")
    print(sep)

    for row in rows:
        print("| " + " | ".join(row[i].ljust(col_widths[i]) for i in range(len(row))) + " |")

    print(sep)

#----Function to nfs volumen manitory
def parse_k8s_storage_to_kb(value):
    """
    Convierte valores tipo 10Gi, 500Mi a KB
    """
    if value.endswith("Gi"):
        return int(float(value.replace("Gi", "")) * 1024 * 1024)
    if value.endswith("Mi"):
        return int(float(value.replace("Mi", "")) * 1024)
    if value.endswith("Ki"):
        return int(float(value.replace("Ki", "")))
    return 0

def format_kb(kb):
    """
    Convierte KB a formato humano
    """
    if kb >= 1024 * 1024:
        return f"{kb / (1024 * 1024):.1f} GiB"
    if kb >= 1024:
        return f"{kb / 1024:.1f} MiB"
    return f"{kb} KiB"