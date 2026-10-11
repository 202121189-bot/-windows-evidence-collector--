#!/usr/bin/env python3
"""
Windows Evidence Collector
===========================
A DFIR tool that collects digital evidence from a Windows system.
"""

import os
import sys
import csv
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from modules import (
    system_info,
    processes,
    network,
    users,
    ip_config,
    event_logs,
    disks,
)


def calculate_sha256(filepath, chunk_size=8192):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def write_csv(path, rows, fieldnames=None):
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def banner(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def collect_all():
    data = {}

    banner("[1/7] System Information")
    data["system_info"] = system_info.collect()
    print(f"  [+] Hostname: {data['system_info']['hostname']}")
    print(f"  [+] OS: {data['system_info']['os']} {data['system_info']['os_release']}")

    banner("[2/7] Running Processes")
    data["processes"] = processes.collect()
    print(f"  [+] Total processes: {len(data['processes'])}")

    banner("[3/7] Network Connections")
    data["network"] = network.collect()
    print(f"  [+] Total connections: {len(data['network'])}")

    banner("[4/7] Users & Sessions")
    data["users"] = users.collect()
    print(f"  [+] Local users: {len(data['users'].get('local_users', []))}")

    banner("[5/7] IP Configuration")
    data["ip_config"] = ip_config.collect()
    print(f"  [+] Interfaces: {len(data['ip_config'].get('interfaces', {}))}")

    banner("[6/7] Event Logs Metadata")
    data["event_logs"] = event_logs.collect()
    print(f"  [+] Logs collected: {len(data['event_logs'])}")

    banner("[7/7] Disks & Volumes")
    data["disks"] = disks.collect()
    print(f"  [+] Disks: {len(data['disks'])}")

    return data


def save_all_outputs(data, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_dir = output_dir / "json"
    csv_dir = output_dir / "csv"
    json_dir.mkdir(exist_ok=True)
    csv_dir.mkdir(exist_ok=True)

    for key, value in data.items():
        write_json(json_dir / f"{key}.json", value)

    if data.get("processes"):
        write_csv(csv_dir / "processes.csv", data["processes"])
    if data.get("network"):
        write_csv(csv_dir / "network.csv", data["network"])
    if data.get("disks"):
        write_csv(csv_dir / "disks.csv", data["disks"])
    if data.get("users", {}).get("local_users"):
        write_csv(csv_dir / "users.csv", data["users"]["local_users"])

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    collected_at = datetime.now().isoformat(timespec="seconds")
    try:
        collector_name = os.getlogin()
    except Exception:
        collector_name = "unknown"

    manifest = {}

    html_content = template.render(
        data=data,
        collected_at=collected_at,
        collector_name=collector_name,
        hostname=data["system_info"]["hostname"],
        manifest=manifest,
    )

    report_path = output_dir / "report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    for file in sorted(output_dir.rglob("*")):
        if file.is_file() and file.name != "manifest.json":
            rel = file.relative_to(output_dir).as_posix()
            manifest[rel] = calculate_sha256(file)

    write_json(output_dir / "manifest.json", manifest)

    html_content = template.render(
        data=data,
        collected_at=collected_at,
        collector_name=collector_name,
        hostname=data["system_info"]["hostname"],
        manifest=manifest,
    )
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return manifest


def main():
    parser = argparse.ArgumentParser(description="Windows Evidence Collector - DFIR tool")
    parser.add_argument("-o", "--output", default=None)
    args = parser.parse_args()

    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"output/evidence_{timestamp}"
    else:
        output_dir = args.output

    print("\n" + "=" * 60)
    print("  WINDOWS EVIDENCE COLLECTOR - DFIR")
    print("=" * 60)
    print(f"  Output: {output_dir}")
    print(f"  Started: {datetime.now().isoformat(timespec='seconds')}")

    data = collect_all()

    banner("Saving Outputs")
    manifest = save_all_outputs(data, output_dir)

    print(f"  [+] Files saved: {len(manifest)}")
    print(f"  [+] Report: {output_dir}/report.html")
    print(f"  [+] Manifest: {output_dir}/manifest.json")

    banner("DONE")
    print(f"  Open the report: {output_dir}\\report.html\n")


if __name__ == "__main__":
    main()