# ELP-BASE — Edge Linux Platform (Base Platform)

ELP-BASE is a reusable **Edge Linux Platform base platform** designed for industrial IoT and edge computing scenarios.

This repository provides a **clean, portable and extensible foundation** for building Edge Linux Platform products, separating **platform capabilities** from **project-specific configuration and features**.

ELP-BASE is **not a final product**.  
It is intended to be consumed and extended by downstream projects via Git subtrees.

---

## 🎯 Project Goals

The main goals of ELP-BASE are:

- Provide a **reusable Edge Linux Platform platform**, not a single-purpose solution
- Enforce a clear separation between:
  - **Capabilities (platform)**
  - **Configuration (projects / environments)**
- Enable **local-first data processing**, with cloud as an optional capability
- Be fully **portable and reproducible** using Docker Compose
- Be suitable for **headless / embedded Linux systems**
- Serve as a **professional reference architecture** (CV / portfolio ready)

---

## 🧠 Architectural Principles

ELP-BASE follows these core principles:

### Capability vs Configuration
- The platform defines **what the gateway can do**
- Projects define **how it is configured**
- No project-specific logic lives in the base stack

### Local First, Cloud Optional
- All ingestion and persistence happen locally
- Cloud connectivity is **opt-in**, never mandatory
- The gateway remains functional offline

### Explicit Composition
- Docker Compose files are **explicitly composed**
- No hidden magic or implicit behavior
- Optional features are enabled via overlays

### Platform, Not a Product
- No assumptions about customers, networks or deployments
- Designed to be extended, not modified

---

## 🧩 High-Level Architecture

Core data flow:

```text
Devices / Publishers
        ↓
 Local MQTT Broker
        ↓
  Data Ingestor
   - Validate
   - Normalize
   - Persist
        ↓
 Internal Events Bus
        ↓
 (Optional) Cloud Connector
```

### Core Components

| Component | Responsibility |
|----------|----------------|
| MQTT Broker | Local message ingestion |
| Data Ingestor | Validation, normalization and persistence |
| MariaDB | Local persistence |
| Cloud Connector (optional) | Publish normalized events to cloud |


## 📁 Repository Layout

```text
services/                 # Reusable service implementations
  ├── data-ingestor/
  └── cloud-connector/

stack/
  ├── compose/             # Docker Compose definitions (platform)
  │   ├── base.yml         # Core stack (always on)
  │   └── overlays/        # Optional capabilities
  │       └── cloud-hivemq.yml
  │
  ├── docker-compose.yml   # Base entrypoint (core only)
  ├── configs/             # Runtime configuration (bind-mounted)
  │   └── mosquitto/
  ├── volumes/             # Runtime state (dev only)
  │   └── mosquitto/
  │
  ├── .env.example         # Environment template (no secrets)
  └── .env                 # Local runtime env (not versioned)
  ```

## ▶️ Running the Stack

### Core Platform (Local Edge Only)

```bash
cd stack
docker compose up -d
```

This starts:
- Local MQTT broker
- Data ingestor
- Local persistence

### Core + Cloud Capability (Opt-In)

```bash
cd stack
docker compose --env-file .env \
  -f compose/base.yml \
  -f compose/overlays/cloud-hivemq.yml \
  up -d
```

Cloud connectivity is enabled only when the overlay is explicitly included.

## 🔐 Configuration & Secrets

- `.env` files are **never committed**
- `.env.example` documents required variables
- Secrets are injected at runtime only
- Configuration is always external to the platform code


## 🧱 Extensibility Model

ELP-BASE is designed to be extended via:

- Git subtrees for downstream projects
- Additional Docker Compose overlays
- External configuration and secrets

Examples of downstream extensions (not included here):

- VPN connectivity (WireGuard)
- SNMP / legacy monitoring
- Multi-cloud publishing
- Project-specific routing or filtering

## 📌 Current Status

- Core platform stable
- Local ingestion and persistence working
- Cloud publishing validated via overlay
- Ready to be consumed by downstream projects

## ⚠️ Disclaimer

This repository represents a **base platform**, not a complete solution.

Downstream projects are expected to:
- Provide their own configuration
- Enable only required capabilities
- Add project-specific documentation