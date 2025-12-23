from modules.kubectl.kubectl import run

def get_node_resources():
    """
    Retrieves CPU and memory usage per node using kubectl top nodes.
    Returns:
        tuple: A tuple containing:
            - rows (list): A list of data formatted for table output.
            - has_pressure (bool): True if any node exceeds basic resource thresholds.
    """

    output = run("kubectl top nodes --no-headers")

    rows = []
    has_pressure = False

    for line in output.strip().splitlines():
        # Example:
        # worker01   250m   65%   2048Mi   70%
        parts = line.split()

        if len(parts) < 5:
            continue

        node = parts[0]
        cpu = parts[1]
        cpu_pct = parts[2]
        mem = parts[3]
        mem_pct = parts[4]

        # Basic thresholds, you cant set the value
        if cpu_pct.replace('%', '').isdigit() and int(cpu_pct.replace('%', '')) > 80:
            has_pressure = True
        if mem_pct.replace('%', '').isdigit() and int(mem_pct.replace('%', '')) > 80:
            has_pressure = True

        rows.append([
            node,
            cpu,
            cpu_pct,
            mem,
            mem_pct
        ])

    return rows, has_pressure
