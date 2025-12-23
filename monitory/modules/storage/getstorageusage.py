import subprocess
import json
import os
from modules.kubectl.kubectl import run
from modules.utils.utils import parse_k8s_storage_to_kb
from modules.utils.utils import format_kb

def get_dir_size_kb(path):
    """
    Returns directory size in GiB using the du command.
    """
    try:
        output = run(f"du -s {path} 2>/dev/null")
        used_kb = int(output.split()[0])
        return used_kb
    except Exception:
        return None

def get_nfs_usage_by_pv(nfs_mount="/mnt/nfs"):
    """
    Retrieves real NFS disk usage per Persistent Volume (PV).
    """

    rows = []
    has_pressure = False

    pv_data = json.loads(run("kubectl get pv -o json"))

    for pv in pv_data["items"]:
        if "nfs" not in pv["spec"]:
            continue

        pv_name = pv["metadata"]["name"]
        nfs_path = pv["spec"]["nfs"]["path"]          
        capacity = pv["spec"]["capacity"]["storage"]

        # Skip nfs mount pv
        if nfs_path == "/nfs/": # Adjust the PV volume path used to mount the NFS share in the monitoring pod.
            continue

        # Removes the /nfs mount point from the string to build the absolute underlying path.
        relative_path = nfs_path.replace("/nfs", "", 1)
        real_path = os.path.join(nfs_mount, relative_path.lstrip("/"))

        used_kb = get_dir_size_kb(real_path)
        cap_kb = parse_k8s_storage_to_kb(capacity)

        if used_kb is None or cap_kb <= 0:
            pct = "N/A"
            estado = "UNKNOW"
        else:
            pct_val = round((used_kb / cap_kb) * 100, 1)
            pct = f"{pct_val} %"
            estado = "WARNING: Storage usage is at or above 80%" if pct_val >= 80 else "OK"

            if pct_val >= 80:
                has_pressure = True

        rows.append([
            pv_name,
            nfs_path,
            f"{int(used_kb)/(1024*1024):.1f} GiB" if int(used_kb)/(1024*1024) is not None else "N/A",
            f"{int(cap_kb)/(1024*1024):.1f} GiB",
            pct,
            estado
        ])

    return rows, has_pressure
