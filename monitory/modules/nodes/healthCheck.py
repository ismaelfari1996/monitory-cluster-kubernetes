import json
from modules.kubectl.kubectl import run

def check_nodes():
    output = run("kubectl get nodes -o json")
    data = json.loads(output)

    rows = []
    has_not_ready = False

    for node in data["items"]:
        name = node["metadata"]["name"]
        conditions = node["status"]["conditions"]

        ready = next(c for c in conditions if c["type"] == "Ready")
        status = ready["status"]

        if status == "True":
            rows.append([name, "Ready", "-", "-"])
        else:
            has_not_ready = True
            rows.append([
                name,
                status,
                ready.get("reason", "N/A"),
                ready.get("message", "N/A")
            ])

    return rows, has_not_ready
