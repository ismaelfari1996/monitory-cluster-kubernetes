import subprocess
from modules.kubectl.kubectl import run

def get_nfs_filesystem_usage(mount_point="/mnt/nfs"):
    """
    Executes the df -h command against the NFS mount to return 
    human-readable usage and capacity data.
    """

    try:
        output = run(f"df -hP {mount_point} | tail -1")
        parts = output.split()

        filesystem = parts[0].split(":")
        filesystem=filesystem[0]
        size = parts[1]
        used = parts[2]
        avail = parts[3]
        use_pct = parts[4]
        #mounted_on = parts[5]

        return {
            "filesystem": filesystem,
            "size": size,
            "used": used,
            "available": avail,
            "use_pct": use_pct
        }

    except Exception as e:
        return {
            "ERROR": str(e)
        }
