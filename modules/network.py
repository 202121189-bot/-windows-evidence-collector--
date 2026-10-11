"""
Network Connections Collector
Gathers active TCP/UDP connections and listening ports.
"""

import psutil


def _addr_to_str(addr):
    """Convert (ip, port) tuple to 'ip:port' string."""
    if not addr:
        return ""
    return f"{addr[0]}:{addr[1]}"


def collect():
    """Return list of dicts, one per network connection."""
    connections = []

    for conn in psutil.net_connections(kind="inet"):
        try:
            connections.append({
                "fd": conn.fd,
                "family": str(conn.family),
                "type": str(conn.type),
                "local_address": _addr_to_str(conn.laddr),
                "remote_address": _addr_to_str(conn.raddr),
                "status": conn.status,
                "pid": conn.pid,
            })
        except Exception:
            continue

    return connections
