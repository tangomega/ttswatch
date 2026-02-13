# TTSWatch – Project Specification

## Overview
**TTSWatch** is a Linux-based monitoring and automation server designed to observe FortiGate firewall devices and provide status visibility, license tracking, firmware awareness, and automated configuration backups.

The goal is to create a lightweight, self-hosted alternative for small environments and homelabs that need monitoring and alerting without full enterprise management complexity.

---

## Version 1 Goals (MVP)

TTSWatch Version 1 focuses on **monitoring and backup only**, not centralized management.

### Core Features
- Device online / offline monitoring
- System uptime tracking
- CPU and memory usage polling
- Firmware version detection
- License expiration tracking
- Nightly automated configuration backups
- Historical data storage
- Basic alert notifications (Email or Discord webhook)

---

## Out of Scope – Version 1

The following features are **intentionally excluded** from V1:

- Policy or firewall rule management
- Centralized configuration editing
- VPN management
- Log analytics / SIEM functionality
- Automatic firmware upgrades
- Multi-user authentication
- Role-based access control
- Advanced UI themes or branding
- Multi-tenant environments

---

## Inputs

Required:
- FortiGate device IP address
- REST API key (read-only)
- Polling interval (minutes)

Optional (Future):
- Device nickname / label
- Site or location tag
- Alert thresholds

---

## Outputs

- Web dashboard displaying device health and metadata
- Alert notifications (Email / Discord / Slack webhook)
- Encrypted configuration backup files
- Historical logs of device status and metrics

---

## Success Criteria

Version 1 is considered complete when:

- Device health metrics display correctly
- Firmware version is visible and flagged if outdated
- License expiration alerts trigger correctly
- Nightly configuration backups run automatically
- Historical status data is stored in a database
- System runs unattended without manual commands

---

## Target Scale (V1)

- 1–3 FortiGate devices
- Single organization or homelab
- Single administrator

---

## Technical Direction (Initial)

### Platform
- Linux Server (Ubuntu LTS or Debian)

### Language
- Python 3.x

### Storage
- SQLite (initial)
- PostgreSQL (future scalability)

### Scheduling
- Cron or systemd timers

### Dashboard
- Grafana or lightweight Flask/FastAPI web app

---

## Security Considerations

- Read-only API credentials
- Encrypted secret storage
- HTTPS dashboard access
- IP-restricted API usage
- Network isolation (VLAN or firewall rules)
- Rate-limited polling intervals

---

## Future Expansion (Post-V1 Ideas)

- Multi-device auto-discovery
- Advanced dashboards
- RBAC authentication
- Ticketing system integration
- Update advisories
- Docker deployment package

---

## Project Philosophy

TTSWatch prioritizes:
- Simplicity
- Reliability
- Security awareness
- Automation
- Maintainability
- Clear documentation

The intent is to build a practical monitoring system first, then iterate responsibly rather than over-engineering from the beginning.
