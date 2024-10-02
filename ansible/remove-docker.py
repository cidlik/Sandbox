#!/usr/bin/env python3

import json
import subprocess
import sys

LABEL_OWNER = "container-owner"

def remove(container):
    subprocess.check_call(["docker", "stop", container])
    subprocess.run(["docker", "rm", container], check=False)

if __name__ == "__main__":
    containers = subprocess.check_output(["docker", "ps", "-aq"]).decode().strip()
    if not containers:
        print("Have not containers. Skip")
        sys.exit(0)

    current_user = subprocess.check_output(["whoami"]).decode().strip()
    for container in containers.split("\n"):
        raw = subprocess.check_output(
            ["docker", "inspect", "-f", "json", container]
        ).decode().strip()
        labels = json.loads(raw)[0]["Config"].get("Labels", None)
        if not LABEL_OWNER in labels:
            print(f"Remove {container}. Reason: has not '{LABEL_OWNER}' label")
            remove(container)
            continue
        if current_user == labels[LABEL_OWNER]:
            print(f"Remove {container}. Reason: container by current user")
            remove(container)
        else:
            print(f"Skip {container}. Reason: container by another user on the same host")
    sys.exit(0)
