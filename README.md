# Windows Evidence Collector

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg)
![Domain](https://img.shields.io/badge/Domain-DFIR-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A DFIR (Digital Forensics & Incident Response) tool that collects digital evidence from a Windows system in a structured, forensically sound manner.

## Features

- **System Information** - OS, hostname, uptime, CPU, RAM
- **Running Processes** - PID, name, path, user, CPU, memory
- **Network Connections** - active TCP/UDP, listening ports
- **Users & Sessions** - local accounts, active logons
- **IP Configuration** - interfaces, DNS, routing table
- **Event Logs Metadata** - Security/System/Application stats
- **Disks & Volumes** - capacity, usage, filesystems
- **SHA-256 Manifest** - integrity verification (chain of custody)
- **HTML Report** - ready-to-read forensic report

## Requirements

- Python 3.8+
- Windows 10/11 (recommended)
- PowerShell 5.1+

Install dependencies:

```bash
pip install -r requirements.txt