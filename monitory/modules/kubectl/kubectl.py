import subprocess
import sys

def run(cmd):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR ejecutando: {cmd}")
        print(result.stderr)
        sys.exit(2)
    return result.stdout
