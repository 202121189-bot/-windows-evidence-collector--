"""
Event Logs Metadata Collector
Gathers metadata for Security, System, Application logs.
"""

import subprocess
import json


LOG_NAMES = ["Security", "System", "Application"]


def collect():
    """Return dict with metadata for each event log."""
    result = {}

    for log_name in LOG_NAMES:
        try:
            ps_cmd = (
                f"$log = Get-WinEvent -ListLog '{log_name}' -ErrorAction Stop; "
                f"@{{"
                f"LogName=$log.LogName;"
                f"RecordCount=$log.RecordCount;"
                f"FileSizeMB=[math]::Round($log.FileSize/1MB,2);"
                f"IsEnabled=$log.IsEnabled;"
                f"LastWriteTime=$log.LastWriteTime.ToString('o')"
                f"}} | ConvertTo-Json"
            )
            output = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                stderr=subprocess.DEVNULL, timeout=20,
            ).decode("utf-8", errors="ignore").strip()

            result[log_name] = json.loads(output) if output else {"error": "empty"}
        except Exception as e:
            result[log_name] = {"error": str(e)}

    return result
