import json
import socket
from modules.kubectl.kubectl import run

def tcp_check(host, port, timeout=3):
    try:
        socket.create_connection((host, port), timeout=timeout)
        return "OK", "-"
    except Exception as e:
        return "ERROR", str(e)

def get_services_health():
    """
    Checks Service health:
    - HTTP for common ports.
    - TCP for middleware (Kafka, Postgres, etc.).

    Returns:
        tuple: A tuple containing:
            - rows (list): Rows formatted for table output.
            - has_errors (bool): True if any service check fails.
    """

    output = run("kubectl get svc -A -o json")
    data = json.loads(output)

    rows = []
    has_errors = False

    for item in data["items"]:
        name = item["metadata"]["name"]
        ns = item["metadata"]["namespace"]

        # Ignore services without an IP
        if item["spec"].get("clusterIP") == "None":
            continue

        for p in item["spec"].get("ports", []):
            port = p.get("port")
            fqdn = f"{name}.{ns}.svc.cluster.local"
            status, msg = tcp_check(fqdn, port)

            if status != "OK":
                has_errors = True

            rows.append([
                ns,
                name,
                port,
                status,
                msg
            ])

    return rows, has_errors
