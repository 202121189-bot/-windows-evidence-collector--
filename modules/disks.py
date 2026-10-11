"""
Disks & Volumes Collector
Gathers partitions, filesystems, usage.
"""

import psutil


def collect():
    """Return list of dicts, one per mounted partition."""
    disks = []

    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "opts": part.opts,
                "total_gb": round(usage.total / (1024 ** 3), 2),
                "used_gb": round(usage.used / (1024 ** 3), 2),
                "free_gb": round(usage.free / (1024 ** 3), 2),
                "percent_used": usage.percent,
            })
        except PermissionError:
            continue

    return disks
