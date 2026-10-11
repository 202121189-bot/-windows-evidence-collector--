"""
Users Collector
Gathers local user accounts and logged-in sessions.
"""

import subprocess
import json


def collect():
    """Return dict with local users and active sessions."""
    result = {"local_users": [], "active_sessions": []}

    try:
        ps_cmd = (
            "Get-LocalUser | "
            "Select-Object Name,Enabled,LastLogon,PasswordRequired,Description | "
            "ConvertTo-Json -Depth 2"
        )
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            stderr=subprocess.DEVNULL,
            timeout=15,
        ).decode("utf-8", errors="ignore").strip()

        if output:
            data = json.loads(output)
            result["local_users"] = data if isinstance(data, list) else [data]
    except Exception as e:
        result["local_users_error"] = str(e)

    try:
        output = subprocess.check_output(
            ["quser"],
            stderr=subprocess.DEVNULL,
            timeout=10,
        ).decode("utf-8", errors="ignore")
        result["active_sessions"] = output.strip().splitlines()
    except Exception as e:
        result["active_sessions_error"] = str(e)

    return result
