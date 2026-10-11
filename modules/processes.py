"""
Running Processes Collector
Gathers PID, name, path, user, CPU, memory for each running process.
"""

import psutil


def collect():
    """Return list of dicts, one per running process."""
    processes = []

    for proc in psutil.process_iter(
        ["pid", "name", "exe", "username", "cpu_percent",
         "memory_percent", "create_time", "status", "cmdline"]
    ):
        try:
            info = proc.info
            processes.append({
                "pid": info.get("pid"),
                "name": info.get("name"),
                "exe": info.get("exe"),
                "username": info.get("username"),
                "cpu_percent": info.get("cpu_percent"),
                "memory_percent": round(info.get("memory_percent") or 0, 2),
                "create_time": info.get("create_time"),
                "status": info.get("status"),
                "cmdline": " ".join(info.get("cmdline") or [])[:200],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return processes
