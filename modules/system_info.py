"""
System Information Collector
Gathers OS, hostname, uptime, architecture details.
"""

import platform
import socket
import psutil
from datetime import datetime


def collect():
    """Return dict with system information."""
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time

    return {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "boot_time": boot_time.isoformat(timespec="seconds"),
        "uptime_hours": round(uptime.total_seconds() / 3600, 2),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "total_ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
    }
