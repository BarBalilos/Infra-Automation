# 🚀 Infra-Automation

A Python-based **infrastructure provisioning simulator** that lets you create and manage virtual machine (VM) configurations, with automated service installation (via Bash) and detailed logging.  
This project is part of a **rolling DevOps course** — later stages will integrate with **AWS** and **Terraform** to provision real resources.

---

## ✨ Features

- 🖥️ **Virtual Machine Creation**: Create VMs with customizable CPU, RAM, and OS.  
- 🏗️ **Object-Oriented Design**: VM definitions are managed via a `Machine` class (`src/machine.py`) for clean modularity.  
- 📜 **Bash Logging**: The installer script logs installation progress and errors for traceability.  
- 📝 **Configuration Management**: Configs stored in JSON (`configs/instances.json`) and TXT (`configs/instances.txt`).  
- 🔧 **Automated Service Installation**: Simulates Nginx installation using a Bash script (`scripts/service_installer.sh`).  
- 📋 **Input Validation**: Basic validation ensures correct VM specs (future upgrade: `pydantic` / `jsonschema`).    
- 📊 **Logging**: All events recorded in `logs/provisioning.log` using Python’s `logging` module.  
- 🛡️ **Error Handling**: Handles invalid inputs, subprocess errors, and missing files gracefully.  

---

## 📂 Project Structure

```

infra-automation/
├── configs/                                # VM configs
│ ├── instances.json
│ └── instances.txt
├── logs/                                   # Logs
│ └── provisioning.log
├── scripts/                                # Automation scripts
│ └── service_installer.sh
├── src/                                    # Source code
│ ├── machine.py
│ ├── input_helpers.py
│ └── logger.py
├── infra_simulator.py                      # Main orchestration script
└── README.md                               # Documentation

```

## 📦 Requirements

## Windows:
  - WSL installed
  - Ubuntu distribution installed in WSL

## Linux/macOS:
  - bash shell available

### Python Dependencies
- Python 3.10+  
- jsonschema>=4.0.0 *(planned for future validation, not currently used — manual validation is implemented in `machine.py` and `input_helpers.py`)*  
- (install via `pip install -r requirements.txt`)

### System-Level Requirements
The following are required depending on your operating system:

| Operating System | Requirement                                      |
|------------------|--------------------------------------------------|
| Linux / macOS    | Bash shell (typically pre-installed)             |
| Windows          | One of the following Bash environments:          |
|                  | • **Git Bash** (recommended)                     |
|                  | • **WSL with Ubuntu** (run `wsl --install -d Ubuntu`) |

---


### ⚙️ Setup Instructions

1. **Clone the Repository:**

```bash
git clone https://github.com/BarBalilos/infra-automation.git
cd infra-automation
```

2. **(Optional) Create a Virtual Environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS

# OR

.\.venv\Scripts\activate    # Windows
```

3. **Run the Simulator**

```bash
python infra_simulator.py
```

You will be prompted to enter VM details (name, OS, CPU, RAM).
The configurations are saved to configs/instances.json.

4. **Run the Service Installer**

```bash
./scripts/service_installer.sh
```

This simulates installing Nginx (or another service).
Progress is logged in logs/provisioning.log.

---

#### 📝 Example Workflow

⚠️ Note on Inputs:
- CPU and RAM values must be entered as **integers only**.
- Examples:
  - CPU: `2` (✅ correct), not `2vCPU` (❌ wrong)
  - RAM: `4` (✅ correct), not `4GB` (❌ wrong)

```text
Machine name (or 'done'): web-server
OS (Ubuntu/CentOS): Ubuntu
vCPU (1-64): 2
RAM in GB (1-512): 4
```

Generated JSON (configs/instances.json):

```json
[
  {
    "name": "web-server",
    "os": "Ubuntu",
    "cpu": 2,
    "ram_gb": 4
  }
]
```


```text
Log Output (logs/provisioning.log):


2025-09-05 10:23:54 | INFO | Provisioning started
2025-09-05 10:23:55 | INFO | Machine created: web-server (Ubuntu, 2 vCPU, 4GB RAM)
2025-09-05 10:23:56 | INFO | Nginx installation completed
```

---


## 🚀 Next Steps

Planned future enhancements:

- Provision real AWS EC2 instances.

- Manage infrastructure with Terraform.

- Add more services (databases, monitoring tools, etc.).

- Improve validation with libraries like pydantic or jsonschema.



## 📖 Notes
- Logs are stored in logs/provisioning.log.

- Both Python and Bash scripts include logging for visibility and troubleshooting.

- This is a simulation project for learning — no real VMs are created yet.

- Code is modular and designed for extension in future phases.