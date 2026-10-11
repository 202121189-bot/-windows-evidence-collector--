"""
IP Configuration Collector
Gathers IP addresses, MACs, DNS, and routing table.
"""

import psutil
import subprocess


def collect():
    """Return dict with interfaces, DNS, and routes."""
    result = {"interfaces": {}, "dns": [], "routes": []}

    try:
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for iface, addr_list in addrs.items():
            iface_data = {
                "is_up": stats[iface].isup if iface in stats else None,
                "speed_mbps": stats[iface].speed if iface in stats else None,
                "addresses": [],
            }
            for addr in addr_list:
                iface_data["addresses"].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast,
                })
            result["interfaces"][iface] = iface_data
    except Exception as e:
        result["interfaces_error"] = str(e)

    try:
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command",
             "Get-DnsClientServerAddress | Select-Object InterfaceAlias,ServerAddresses | ConvertTo-Json"],
            stderr=subprocess.DEVNULL, timeout=15,
        ).decode("utf-8", errors="ignore").strip()
        if output:
            result["dns"] = output
    except Exception as e:
        result["dns_error"] = str(e)

    try:
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command",
             "Get-NetRoute | Select-Object DestinationPrefix,NextHop,InterfaceAlias,RouteMetric | ConvertTo-Json"],
            stderr=subprocess.DEVNULL, timeout=15,
        ).decode("utf-8", errors="ignore").strip()
        if output:
            result["routes"] = output
    except Exception as e:
        result["routes_error"] = str(e)

    return result
