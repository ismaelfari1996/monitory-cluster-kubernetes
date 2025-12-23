import json
from modules.kubectl.kubectl import run

ERROR_PHASES = ["Failed", "Unknown"]

def check_pod_health():
    """
    Revisa la salud de los pods en todos los namespaces.
    Retorna SOLO pods con errores.
    """

    output = run("kubectl get pods --all-namespaces -o json")
    data = json.loads(output)

    rows = []
    has_issues = False

    for pod in data["items"]:
        ns = pod["metadata"]["namespace"]
        name = pod["metadata"]["name"]
        phase = pod["status"].get("phase", "Unknown")

        #  Errores a nivel de fase
        if phase in ERROR_PHASES:
            has_issues = True
            rows.append([
                ns,
                name,
                phase,
                "PodPhase",
                f"Pod en fase {phase}"
            ])
            continue

        #  Errores en contenedores
        statuses = pod["status"].get("containerStatuses", [])

        for c in statuses:
            state = c.get("state", {})

            # CrashLoopBackOff, Error, etc.
            if "waiting" in state:
                reason = state["waiting"].get("reason", "")
                message = state["waiting"].get("message", "")

                if reason in ["CrashLoopBackOff", "Error", "ImagePullBackOff", "ErrImagePull"]:
                    has_issues = True
                    rows.append([
                        ns,
                        name,
                        "NotReady",
                        reason,
                        message or "Contenedor en estado waiting"
                    ])
                    break

            # Contenedor terminado con error
            if "terminated" in state:
                reason = state["terminated"].get("reason", "")
                exit_code = state["terminated"].get("exitCode", 0)

                if exit_code != 0:
                    has_issues = True
                    rows.append([
                        ns,
                        name,
                        "Terminated",
                        reason or "Error",
                        f"ExitCode {exit_code}"
                    ])
                    break

    return rows, has_issues
