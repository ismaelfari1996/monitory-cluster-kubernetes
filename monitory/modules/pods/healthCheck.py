import json
from modules.kubectl.kubectl import run

ERROR_PHASES = ["Failed", "Unknown"]

def check_pod_health():
    """
    Monitors pod health across all namespaces. Returns ONLY failed or error-state pods
    """

    output = run("kubectl get pods --all-namespaces -o json")
    data = json.loads(output)

    rows = []
    has_issues = False

    for pod in data["items"]:
        ns = pod["metadata"]["namespace"]
        name = pod["metadata"]["name"]
        phase = pod["status"].get("phase", "Unknown")

        #  Errors level phases
        if phase in ERROR_PHASES:
            has_issues = True
            rows.append([
                ns,
                name,
                phase,
                "PodPhase",
                f"Pod in phase {phase}"
            ])
            continue

        #  Containers error
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
                        message or "Container waiting"
                    ])
                    break

            # Containers finiched with errors
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
